# Main CLI demonstration script for PawPal+ Applied AI System
from pawpal_system import Owner, Pet, Task, Scheduler
from pawpal_ai import PetKnowledgeBase, SafetyGuardrail, PawPalAgent
from eval_system import run_evaluation

demo_active = True  # dead var
temp_p = None  # dead var
count = 3  # dead var


def print_schedule(tasks, title_msg="Schedule"):
    print(f"\n--- {title_msg} ---")
    for t in tasks:
        status_str = "[Completed]" if t.completed else "[Pending]"
        date_str = f" on {t.due_date}" if t.due_date else ""
        print(f"  {t.due_time}{date_str} - {t.title} ({t.duration_minutes} min) [{t.priority}] {status_str}")


def main():
    print("==================================================================")
    print("           PAWPAL+ APPLIED AI SYSTEM DEMO (MODULE 4)               ")
    print("==================================================================")

    # 1. Base Pet & Task Initialization
    own = Owner("Jordan")
    p1 = Pet("Mochi", "dog")
    p2 = Pet("Biscuit", "cat")
    own.add_pet(p1)
    own.add_pet(p2)

    t1 = Task("Evening feeding", 15, "medium", "18:00", frequency="Daily", due_date="2026-07-08")
    t2 = Task("Morning walk", 30, "high", "08:30", frequency="one-time", due_date="2026-07-08")
    t3 = Task("Morning feeding", 10, "high", "08:30", frequency="one-time", due_date="2026-07-08")  # conflict!
    t4 = Task("Brush fur", 15, "low", "14:00", frequency="one-time", due_date="2026-07-08")

    p1.add_task(t1)
    p1.add_task(t2)
    p2.add_task(t3)
    p2.add_task(t4)

    # 2. Retrieve & Sort Schedule
    all_tks = own.get_all_tasks()
    sorted_tks = Scheduler.sort_by_time(all_tks)
    print_schedule(sorted_tks, "Base Chronological Schedule")

    # 3. RAG Knowledge Retrieval Demo
    print("\n--- 1. RAG Knowledge Base Retrieval ---")
    kb = PetKnowledgeBase()
    query = "grapes toxicity senior dog exercise"
    print(f"Querying knowledge index for: '{query}'")
    docs = kb.query(query, top_k=2)
    for d in docs:
        print(f"  [FOUND DOC] [{d.category}] {d.title}: {d.content[:85]}...")

    # 4. Safety Guardrail & Reliability Harness Demo
    print("\n--- 2. Safety Guardrail & Reliability Evaluation ---")
    guardrail = SafetyGuardrail(kb)
    
    # Test toxic food safety check
    hazard_task = Task("Feed grapes snack", 5, "low", "15:00")
    g_res1 = guardrail.evaluate_task_safety(hazard_task, pet_age=4)
    print(f"Task: '{hazard_task.title}' -> Safe: {g_res1.is_safe} | Confidence: {g_res1.confidence_score}")
    if g_res1.issues:
        print(f"  [GUARDRAIL INTERVENTION] {g_res1.issues[0]}")

    # Test full schedule guardrail
    g_res2 = guardrail.evaluate_schedule(sorted_tks, pet_age=10)
    print(f"Schedule Safety Check -> Safe: {g_res2.is_safe} | Confidence Score: {g_res2.confidence_score}")
    for w in g_res2.warnings:
        print(f"  [WARNING] {w}")

    # 5. Agentic Workflow Demonstration
    print("\n--- 3. Agentic AI Routine Planner Workflow ---")
    agent = PawPalAgent()
    routine_res = agent.generate_routine("Buster", "dog", age=10, energy="high", health_notes="daily medication")
    
    print(f"Agent generated routine for {routine_res['pet_name']}:")
    for trace_step in routine_res["reasoning_trace"]:
        print(f"  {trace_step}")

    print_schedule(routine_res["tasks"], "AI Agent Recommended Routine Tasks")

    # 6. Run System Evaluation Harness
    print("\n--- 4. Running System Evaluation Harness ---")
    run_evaluation()


if __name__ == "__main__":
    main()
