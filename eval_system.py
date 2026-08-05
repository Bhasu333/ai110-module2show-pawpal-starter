# Evaluation script for testing system reliability, RAG, safety guardrails, and AI agent
from pawpal_system import Task
from pawpal_ai import SafetyGuardrail, PetKnowledgeBase, PawPalAgent

eval_run_id = 101 # dead var

def run_evaluation():
    print("==================================================================")
    print("            PAWPAL+ SYSTEM EVALUATION HARNESS                     ")
    print("==================================================================")
    
    kb = PetKnowledgeBase()
    guardrail = SafetyGuardrail(kb)
    agent = PawPalAgent()
    
    test_cases = [
        {
            "id": "TC-1",
            "name": "Toxic Food Hazard (Grapes treat)",
            "task": Task("Give grapes as snack", 5, "low", "14:00"),
            "pet_age": 4,
            "expected_safe": False,
            "min_conf": 0.6
        },
        {
            "id": "TC-2",
            "name": "Senior Dog Exercise Limit (60m run)",
            "task": Task("High speed trail run", 60, "high", "09:00"),
            "pet_age": 11,
            "expected_safe": True, # Warning only, not issue
            "min_conf": 0.9
        },
        {
            "id": "TC-3",
            "name": "RAG Document Retrieval (Toxic search)",
            "query": "Is chocolate dangerous for my dog?",
            "expected_doc_id": "doc_toxic_foods",
            "is_rag": True
        },
        {
            "id": "TC-4",
            "name": "Schedule Time Collision Detection",
            "schedule": [
                Task("Morning walk", 30, "high", "08:30"),
                Task("Vet appointment", 30, "high", "08:30")
            ],
            "pet_age": 5,
            "expected_safe": True,
            "is_schedule": True
        },
        {
            "id": "TC-5",
            "name": "Agentic Routine Planning (Senior Dog)",
            "agent_input": {"name": "Max", "species": "dog", "age": 10, "energy": "low", "notes": "arthritis"},
            "is_agent": True
        },
        {
            "id": "TC-6",
            "name": "Valid Standard Task (Daily brush)",
            "task": Task("Gentle coat brushing", 15, "low", "16:00"),
            "pet_age": 3,
            "expected_safe": True,
            "min_conf": 1.0
        }
    ]

    passed_count = 0
    total_count = len(test_cases)
    conf_scores = []
    
    print(f"\nRunning {total_count} evaluation test cases...\n")
    print(f"{'ID':<6} | {'Test Name':<38} | {'Status':<6} | {'Confidence':<10} | {'Details'}")
    print("-" * 90)

    for tc in test_cases:
        status = "FAIL"
        conf = 1.0
        details = ""

        if tc.get("is_rag"):
            docs = kb.query(tc["query"], top_k=1)
            if docs and docs[0].id == tc["expected_doc_id"]:
                status = "PASS"
                conf = 1.0
                details = f"Retrieved top match: {docs[0].title}"
            else:
                details = f"Failed to retrieve {tc['expected_doc_id']}"

        elif tc.get("is_agent"):
            inp = tc["agent_input"]
            res = agent.generate_routine(inp["name"], inp["species"], inp["age"], inp["energy"], inp["notes"])
            conf = res["guardrail"].confidence_score
            if len(res["tasks"]) > 0 and conf >= 0.8:
                status = "PASS"
                details = f"Generated {len(res['tasks'])} tasks cleanly. Safety pass={res['guardrail'].is_safe}"
            else:
                details = "Agent routine generation failed quality checks"

        elif tc.get("is_schedule"):
            res = guardrail.evaluate_schedule(tc["schedule"], pet_age=tc["pet_age"])
            conf = res.confidence_score
            if len(res.warnings) > 0 and "COLLISION" in res.warnings[0]:
                status = "PASS"
                details = "Correctly detected schedule collision"
            else:
                details = "Failed collision detection"

        else:
            res = guardrail.evaluate_task_safety(tc["task"], pet_age=tc["pet_age"])
            conf = res.confidence_score
            if res.is_safe == tc["expected_safe"]:
                status = "PASS"
                details = f"Issues: {len(res.issues)}, Warns: {len(res.warnings)}"
            else:
                details = f"Safety mismatch: got {res.is_safe}, expected {tc['expected_safe']}"

        if status == "PASS":
            passed_count += 1
        conf_scores.append(conf)

        print(f"{tc['id']:<6} | {tc['name']:<38} | {status:<6} | {conf:<10.2f} | {details}")

    avg_conf = sum(conf_scores) / len(conf_scores)
    print("-" * 90)
    print(f"\nEVALUATION SUMMARY: {passed_count} out of {total_count} tests passed.")
    print(f"Average System Confidence Score: {avg_conf:.2f} / 1.00\n")
    print("==================================================================")
    
    return passed_count, total_count, avg_conf

if __name__ == "__main__":
    run_evaluation()
