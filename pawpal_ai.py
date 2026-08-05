# AI engine and RAG / Guardrail components for PawPal+ Applied AI System
import re
from dataclasses import dataclass, field
from pawpal_system import Task, Pet, Scheduler

dbg_mode = True  # dead var
agent_run_count = 0  # dead var


@dataclass
class KnowledgeDoc:
    id: str
    category: str
    title: str
    content: str
    keywords: list[str] = field(default_factory=list)


class PetKnowledgeBase:
    """RAG Component: In-memory document indexing and keyword/semantic lookup."""

    def __init__(self):
        self.docs = []
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        # Index core pet care documents
        self.docs = [
            KnowledgeDoc(
                id="doc_toxic_foods",
                category="Safety & Toxicity",
                title="Toxic Foods for Dogs & Cats",
                content=(
                    "DANGEROUS TOXIC FOODS: Chocolate, grapes, raisins, onions, garlic, "
                    "xylitol, macadamia nuts, avocado, caffeine, and alcohol are strictly toxic to pets. "
                    "Grapes and raisins cause acute kidney failure in dogs. Onions and garlic damage red blood cells."
                ),
                keywords=["toxic", "poison", "food", "grapes", "chocolate", "onions", "garlic", "xylitol", "diet"]
            ),
            KnowledgeDoc(
                id="doc_senior_exercise",
                category="Exercise Guidelines",
                title="Senior Pet & Puppy Exercise Limits",
                content=(
                    "Senior dogs (aged 8+ years) and young puppies (<6 months) require low-impact exercise. "
                    "Single exercise sessions should not exceed 30 minutes to prevent joint strain, hyperthermia, or cardiac fatigue. "
                    "Split long activities into short 15-minute gentle walks."
                ),
                keywords=["senior", "puppy", "exercise", "walk", "duration", "age", "joint", "fatigue"]
            ),
            KnowledgeDoc(
                id="doc_medication_timing",
                category="Health Care",
                title="Pet Medication & Health Administration",
                content=(
                    "Medications (insulin, heartworm, antibiotics, pain relievers) must be administered with strict spacing. "
                    "Always feed pet prior to oral medication unless prescribed on empty stomach. "
                    "Never schedule medication at the exact same minute as intense physical exercise."
                ),
                keywords=["medication", "meds", "pills", "insulin", "health", "timing", "schedule"]
            ),
            KnowledgeDoc(
                id="doc_hydration_enrichment",
                category="Daily Care",
                title="Hydration & Mental Enrichment",
                content=(
                    "Pets require fresh water available at all times. High-energy breeds (Border Collies, Huskies, Shepherds) "
                    "require 45-60 minutes of daily mental enrichment (puzzle toys, scent work) to avoid anxiety."
                ),
                keywords=["water", "hydration", "enrichment", "puzzle", "play", "energy", "mental"]
            ),
        ]

    def query(self, search_text: str, top_k: int = 2) -> list[KnowledgeDoc]:
        """Simple TF-IDF style keyword relevance matching for RAG retrieval."""
        search_terms = re.findall(r'\w+', search_text.lower())
        scored = []
        
        for d in self.docs:
            score = 0
            doc_text = f"{d.title} {d.content} {' '.join(d.keywords)}".lower()
            for term in search_terms:
                if len(term) > 2 and term in doc_text:
                    score += 1
                    # Give extra weight if term matches title or explicit keywords
                    if term in d.title.lower() or term in [k.lower() for k in d.keywords]:
                        score += 2
            if score > 0:
                scored.append((score, d))
                
        # Sort descending by relevance score
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for sc, doc in scored[:top_k]]


@dataclass
class GuardrailResult:
    is_safe: bool
    confidence_score: float
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


class SafetyGuardrail:
    """Reliability & Safety Guardrail engine to check inputs and AI schedule output."""

    TOXIC_ITEMS = ["chocolate", "grape", "raisin", "onion", "garlic", "xylitol", "macadamia", "avocado", "caffeine"]

    def __init__(self, kb: PetKnowledgeBase = None):
        self.kb = kb or PetKnowledgeBase()

    def evaluate_task_safety(self, task: Task, pet_age: int = 3, species: str = "dog") -> GuardrailResult:
        """Validate a single task for toxicity, duration limits, and safety."""
        issues = []
        warns = []
        conf = 1.0
        
        txt = task.title.lower()
        
        # 1. Toxic substance check
        for tox in self.TOXIC_ITEMS:
            if tox in txt:
                issues.append(f"HAZARD DETECTED: Task '{task.title}' mentions '{tox}' which is toxic to pets!")
                conf -= 0.5

        # 2. Senior / Puppy exercise duration check
        if "walk" in txt or "run" in txt or "exercise" in txt:
            if (pet_age >= 8 or pet_age <= 1) and task.duration_minutes > 30:
                warns.append(
                    f"EXERCISE WARNING: Task '{task.title}' duration ({task.duration_minutes} min) "
                    f"exceeds safe limit (30 min) for pet aged {pet_age}."
                )
                conf -= 0.2

        # 3. Format sanity check
        if not re.match(r'^\d{2}:\d{2}$', task.due_time):
            issues.append(f"INVALID TIME FORMAT: '{task.due_time}' is not valid HH:MM format.")
            conf -= 0.3

        conf = max(0.0, min(1.0, round(conf, 2)))
        return GuardrailResult(
            is_safe=(len(issues) == 0),
            confidence_score=conf,
            issues=issues,
            warnings=warns
        )

    def evaluate_schedule(self, tasks: list[Task], pet_age: int = 3, species: str = "dog") -> GuardrailResult:
        """Validate an entire list of scheduled tasks."""
        all_issues = []
        all_warns = []
        total_conf = 1.0
        
        # Check individual task safety
        for t in tasks:
            res = self.evaluate_task_safety(t, pet_age, species)
            all_issues.extend(res.issues)
            all_warns.extend(res.warnings)
            if not res.is_safe:
                total_conf -= 0.3

        # Check collisions using Scheduler
        conflicts = Scheduler.check_conflicts(tasks)
        if conflicts:
            for c in conflicts:
                all_warns.append(f"SCHEDULE COLLISION: {c}")
            total_conf -= 0.15

        total_conf = max(0.0, min(1.0, round(total_conf, 2)))
        return GuardrailResult(
            is_safe=(len(all_issues) == 0),
            confidence_score=total_conf,
            issues=all_issues,
            warnings=all_warns
        )


class PawPalAgent:
    """Agentic Workflow: Multi-step reasoning planner with tool calls (RAG & Guardrail)."""

    def __init__(self):
        self.kb = PetKnowledgeBase()
        self.guardrail = SafetyGuardrail(self.kb)

    def generate_routine(self, pet_name: str, species: str, age: int, energy: str = "medium", health_notes: str = "") -> dict:
        """
        Executes multi-step reasoning:
          Step 1: Parse input & identify constraints
          Step 2: RAG lookup for safety & guidelines
          Step 3: Generate candidate task schedule
          Step 4: Execute safety guardrail check & confidence scoring
        """
        trace = []
        trace.append(f"Step 1 [Input Analysis]: Planning routine for {pet_name} ({species}, {age} years old, {energy} energy). Notes: '{health_notes}'.")

        # Step 2: RAG retrieval
        query_str = f"{species} {energy} energy exercise {health_notes}"
        retrieved_docs = self.kb.query(query_str, top_k=2)
        doc_titles = [d.title for d in retrieved_docs]
        trace.append(f"Step 2 [RAG Retrieval]: Retrieved knowledge docs -> {doc_titles}")

        # Step 3: Few-shot / Rule-based task generation
        candidate_tasks = []
        if species.lower() == "dog":
            # Adjust walk duration based on age
            walk_dur = 20 if age >= 8 or age <= 1 else 35
            candidate_tasks.append(Task("Morning walk", walk_dur, "high", "08:00", frequency="Daily", due_date="2026-08-05"))
            candidate_tasks.append(Task("Breakfast feeding", 15, "high", "08:45", frequency="Daily", due_date="2026-08-05"))
            
            if "high" in energy.lower():
                candidate_tasks.append(Task("Puzzle toy enrichment", 25, "medium", "13:00", frequency="Daily", due_date="2026-08-05"))
            
            if "medication" in health_notes.lower() or "meds" in health_notes.lower():
                candidate_tasks.append(Task("Daily medication", 5, "high", "09:15", frequency="Daily", due_date="2026-08-05"))

            candidate_tasks.append(Task("Evening walk", walk_dur, "medium", "18:00", frequency="Daily", due_date="2026-08-05"))
            candidate_tasks.append(Task("Dinner feeding", 15, "high", "18:45", frequency="Daily", due_date="2026-08-05"))

        else: # cat or other
            candidate_tasks.append(Task("Morning cat feeding", 10, "high", "08:00", frequency="Daily", due_date="2026-08-05"))
            candidate_tasks.append(Task("Feather wand playtime", 20, "medium", "12:30", frequency="Daily", due_date="2026-08-05"))
            candidate_tasks.append(Task("Evening cat feeding", 10, "high", "18:00", frequency="Daily", due_date="2026-08-05"))

        trace.append(f"Step 3 [Task Synthesis]: Generated {len(candidate_tasks)} candidate tasks.")

        # Step 4: Guardrail evaluation
        g_res = self.guardrail.evaluate_schedule(candidate_tasks, pet_age=age, species=species)
        trace.append(f"Step 4 [Guardrail Check]: Safety pass={g_res.is_safe}, Confidence Score={g_res.confidence_score}. Issues={len(g_res.issues)}, Warnings={len(g_res.warnings)}")

        return {
            "pet_name": pet_name,
            "tasks": candidate_tasks,
            "guardrail": g_res,
            "reasoning_trace": trace,
            "retrieved_docs": retrieved_docs
        }
