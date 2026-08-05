# AI Interactions & Intermediate Reasoning Log

---

## Agentic Workflow & Intermediate Reasoning Traces (SF7 / Stretch 2)

### Task Assigned to Agent
Design and execute a multi-step routine planner (`PawPalAgent`) that ingests a pet's profile (species, age, energy level, health notes), retrieves safety rules via RAG, synthesizes candidate care tasks, and validates the candidate routine using safety guardrails.

### Agent Intermediate Reasoning Traces

```
Step 1 [Input Analysis]: Planning routine for Buster (dog, 10 years old, high energy). Notes: 'daily medication'.
Step 2 [RAG Retrieval]: Retrieved knowledge docs -> ['Hydration & Mental Enrichment', 'Senior Pet & Puppy Exercise Limits']
Step 3 [Task Synthesis]: Generated 6 candidate tasks.
Step 4 [Guardrail Check]: Safety pass=True, Confidence Score=1.0. Issues=0, Warnings=0
```

### Generated Routine Output:
- `08:00 on 2026-08-05` - Morning walk (20 min) [high]
- `08:45 on 2026-08-05` - Breakfast feeding (15 min) [high]
- `09:15 on 2026-08-05` - Daily medication (5 min) [high]
- `13:00 on 2026-08-05` - Puzzle toy enrichment (25 min) [medium]
- `18:00 on 2026-08-05` - Evening walk (20 min) [medium]
- `18:45 on 2026-08-05` - Dinner feeding (15 min) [high]

### Verification & Manual Adjustments
- **What was verified**: Verified that the agent correctly shortened the walk duration for senior pet Buster (age 10) from 35 minutes down to 20 minutes to prevent joint fatigue.
- **What was fixed**: Ensured the medication task (09:15) was scheduled cleanly after breakfast (08:45) rather than simultaneously with the morning walk.

---

## Prompt Comparison & Specialization (SF11 / Stretch 3)

| Metric / Aspect | Option A (Unconstrained Baseline Prompt) | Option B (Specialized Few-Shot + Guardrailed Prompt) |
|---|---|---|
| **Model / Tool Used** | Gemini / Unconstrained LLM Prompt | PawPal Specialized System Prompt Engine |
| **Prompt** | "Create a care schedule for a 10 year old dog with high energy and daily medication." | Structured few-shot prompt enforcing JSON Task schema, RAG doc context, age exercise rules, and strict time format. |
| **Response Summary** | Freeform text narrative suggesting long 60-minute runs and feeding whenever convenient. | Structured task list output with explicit start times, capped exercise durations (20 min), and spaced medication slots. |
| **What Was Useful** | Gave good ideas for pet mental enrichment games. | Generated clean, executable Task objects ready for direct UI rendering. |
| **Problems Noticed** | Suggested 60-minute run for a senior 10yo dog and did not specify exact time slots. | Required strict regex validation for time string formats (HH:MM). |
| **Decision** | Rejected for direct scheduling engine. | **Selected for final implementation**. |

### Final Decision Rationale
Option B (Specialized Few-Shot Prompting) was selected because pet safety and deterministic time scheduling require strict schema enforcement and guardrail verification. Unconstrained narrative prompts risk toxic advice and unsafe exercise durations.
