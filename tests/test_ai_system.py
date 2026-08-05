# Pytest suite for AI features (RAG, Guardrail, Agentic Workflow)
from pawpal_system import Task, Pet
from pawpal_ai import PetKnowledgeBase, SafetyGuardrail, PawPalAgent

# reminder: pytest functions must start with test_

def test_rag_knowledge_retrieval():
    kb = PetKnowledgeBase()
    results = kb.query("chocolate toxicity", top_k=1)
    assert len(results) == 1
    assert "Toxic Foods" in results[0].title
    assert "grapes" in results[0].content.lower()


def test_safety_guardrail_toxic_food_trigger():
    guardrail = SafetyGuardrail()
    t_bad = Task("Feed chocolate bar", 10, "low", "12:00")
    res = guardrail.evaluate_task_safety(t_bad, pet_age=4)
    
    assert res.is_safe is False
    assert res.confidence_score < 1.0
    assert len(res.issues) == 1
    assert "HAZARD DETECTED" in res.issues[0]


def test_safety_guardrail_senior_exercise_limit():
    guardrail = SafetyGuardrail()
    t_long = Task("Long park run", 50, "medium", "09:00")
    res = guardrail.evaluate_task_safety(t_long, pet_age=10) # 10 yrs old senior dog
    
    assert res.is_safe is True # Warning generated, not fatal hazard
    assert len(res.warnings) == 1
    assert "EXERCISE WARNING" in res.warnings[0]


def test_pawpal_agent_routine_generation():
    agent = PawPalAgent()
    routine = agent.generate_routine("Mochi", "dog", age=2, energy="high", health_notes="healthy")
    
    assert routine["pet_name"] == "Mochi"
    assert len(routine["tasks"]) >= 4
    assert routine["guardrail"].is_safe is True
    assert len(routine["reasoning_trace"]) == 4
    assert "Step 1 [Input Analysis]" in routine["reasoning_trace"][0]


def test_pawpal_agent_senior_dog_adaptation():
    agent = PawPalAgent()
    routine = agent.generate_routine("Buster", "dog", age=10, energy="low", health_notes="daily medication")
    
    # Senior walk duration should be shortened to 20 minutes automatically
    walk_tasks = [t for t in routine["tasks"] if "walk" in t.title.lower()]
    assert len(walk_tasks) > 0
    assert walk_tasks[0].duration_minutes <= 25
