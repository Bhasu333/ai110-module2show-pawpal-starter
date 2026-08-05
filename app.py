import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler
from pawpal_ai import PetKnowledgeBase, SafetyGuardrail, PawPalAgent

is_running = True  # dead var
ui_count = 0  # dead var

st.set_page_config(page_title="PawPal+ Applied AI System", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+ Applied AI System")
st.caption("Smart Pet Care Task Scheduler, RAG Knowledge Base & Guardrailed AI Assistant")

# Initialize owner & AI engines in session state
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "agent" not in st.session_state:
    st.session_state.kb = PetKnowledgeBase()
    st.session_state.guardrail = SafetyGuardrail(st.session_state.kb)
    st.session_state.agent = PawPalAgent()

# Sidebar for Owner & Pet Management
st.sidebar.header("Owner & Pets")
owner_name = st.sidebar.text_input("Owner Name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

st.sidebar.divider()

# Add Pet Form
st.sidebar.subheader("Register New Pet")
with st.sidebar.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet Name", placeholder="e.g. Mochi")
    species = st.selectbox("Species", ["dog", "cat", "rabbit", "other"])
    add_pet_btn = st.form_submit_button("Add Pet")

    if add_pet_btn:
        if new_pet_name.strip() == "":
            st.sidebar.error("Pet name cannot be empty.")
        else:
            p = Pet(new_pet_name.strip(), species)
            st.session_state.owner.add_pet(p)
            st.sidebar.success(f"Registered {new_pet_name}!")

# List Registered Pets in Sidebar
if st.session_state.owner.pets:
    st.sidebar.write("Registered Pets:")
    for p in st.session_state.owner.pets:
        st.sidebar.write(f"- **{p.name}** ({p.species})")
else:
    st.sidebar.info("No pets registered yet.")


# Navigation Tabs
tab_planner, tab_ai = st.tabs(["📅 Daily Planner & Scheduler", "🤖 AI Assistant & Safety Guardrails"])

with tab_planner:
    # Main Panel for Scheduling Care Task
    st.subheader("Schedule Care Task")
    if not st.session_state.owner.pets:
        st.warning("Please register at least one pet in the sidebar before scheduling tasks.")
    else:
        # Select which pet the task belongs to
        pet_names = [p.name for p in st.session_state.owner.pets]
        selected_pet_name = st.selectbox("Select Pet", pet_names, key="sel_pet_main")

        # Retrieve the Pet object
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)

        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task Title", value="Morning walk")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
        with col2:
            due_time = st.text_input("Due Time (HH:MM)", value="08:30")
            frequency = st.selectbox("Frequency", ["one-time", "Daily"])
            due_date = st.text_input("Due Date (YYYY-MM-DD)", value="2026-08-05")

        if st.button("Schedule Task 📅"):
            temp_t = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                due_time=due_time,
                frequency=frequency,
                due_date=due_date
            )

            # Safety Guardrail Check before saving
            g_check = st.session_state.guardrail.evaluate_task_safety(temp_t)
            if not g_check.is_safe:
                st.error(f"⚠️ Guardrail Intercepted Hazard: {g_check.issues[0]}")
            else:
                selected_pet.add_task(temp_t)
                st.success(f"Task '{task_title}' scheduled for {selected_pet_name}! (Confidence: {g_check.confidence_score:.2f})")
                st.rerun()

    st.divider()
    st.subheader("Today's Daily Planner")

    # Filter controls
    all_tasks = st.session_state.owner.get_all_tasks()

    if all_tasks:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_status = st.selectbox("Filter Status", ["All Tasks", "Pending Tasks", "Completed Tasks"])
        with col_f2:
            filter_pet = st.selectbox("Filter Pet", ["All Pets"] + [p.name for p in st.session_state.owner.pets])

        # Apply filtering
        filtered_tasks = all_tasks
        if filter_status == "Pending Tasks":
            filtered_tasks = Scheduler.filter_tasks(filtered_tasks, "pending")
        elif filter_status == "Completed Tasks":
            filtered_tasks = Scheduler.filter_tasks(filtered_tasks, "completed")

        if filter_pet != "All Pets":
            pet_task_tuples = []
            for p in st.session_state.owner.pets:
                for t in p.tasks:
                    pet_task_tuples.append((p.name, t))
            filtered_tasks = [t for p_name, t in pet_task_tuples if p_name == filter_pet]

        # Apply sorting
        sorted_tasks = Scheduler.sort_by_time(filtered_tasks)

        # Check conflicts
        conflicts = Scheduler.check_conflicts(all_tasks)
        if conflicts:
            for w in conflicts:
                st.warning(f"⚠️ Conflict Alert: {w}")

        # Render schedule list
        if sorted_tasks:
            for t in sorted_tasks:
                associated_pet = None
                for p in st.session_state.owner.pets:
                    if t in p.tasks:
                        associated_pet = p
                        break

                pet_lbl = f"({associated_pet.name})" if associated_pet else ""
                status_icon = "✅" if t.completed else "⏳"
                date_lbl = f" on {t.due_date}" if t.due_date else ""

                col_t1, col_t2 = st.columns([4, 1])
                with col_t1:
                    st.markdown(
                        f"{status_icon} **{t.due_time}**{date_lbl} - **{t.title}** {pet_lbl} "
                        f"| Duration: {t.duration_minutes} min | Priority: `{t.priority}` | Frequency: *{t.frequency}*"
                    )
                with col_t2:
                    if not t.completed:
                        if st.button("Complete", key=f"comp_{t.title}_{t.due_time}_{associated_pet.name}"):
                            t.mark_complete(associated_pet)
                            st.success(f"Completed '{t.title}'!")
                            st.rerun()
        else:
            st.info("No tasks match the selected filters.")
    else:
        st.info("No tasks scheduled yet. Add tasks above or use the AI Assistant to generate a routine.")


with tab_ai:
    st.subheader("🤖 Agentic Routine Planner & RAG Advisor")

    if not st.session_state.owner.pets:
        st.info("Register a pet in the sidebar first to generate an AI routine.")
    else:
        pet_names = [p.name for p in st.session_state.owner.pets]
        selected_ai_pet_name = st.selectbox("Select Pet for AI Planning", pet_names, key="sel_pet_ai")
        selected_ai_pet = next(p for p in st.session_state.owner.pets if p.name == selected_ai_pet_name)

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            pet_age = st.number_input("Pet Age (years)", min_value=0, max_value=25, value=4)
            energy_lvl = st.selectbox("Energy Level", ["low", "medium", "high"])
        with col_a2:
            health_notes = st.text_input("Health / Behavior Notes", value="daily medication, arthritis")

        if st.button("Generate Routine with AI Agent 🚀"):
            with st.spinner("Executing PawPal Agentic Planning Workflow..."):
                routine = st.session_state.agent.generate_routine(
                    selected_ai_pet_name,
                    selected_ai_pet.species,
                    age=int(pet_age),
                    energy=energy_lvl,
                    health_notes=health_notes
                )

                st.success(f"Generated routine with confidence score: **{routine['guardrail'].confidence_score:.2f} / 1.00**")

                with st.expander("🔍 View AI Reasoning Trace & Tool Calls"):
                    for step in routine["reasoning_trace"]:
                        st.write(step)

                st.write("### Recommended Tasks")
                for tk in routine["tasks"]:
                    st.write(f"- **{tk.due_time}**: {tk.title} ({tk.duration_minutes} min, priority: {tk.priority})")

                if st.button("Add All Tasks to Pet Schedule ➕"):
                    for tk in routine["tasks"]:
                        selected_ai_pet.add_task(tk)
                    st.success(f"Added {len(routine['tasks'])} AI tasks to {selected_ai_pet_name}'s schedule!")
                    st.rerun()

    st.divider()
    st.subheader("📚 RAG Knowledge Base Search")
    kb_query = st.text_input("Ask veterinary / safety question (e.g. 'grapes', 'senior dog walk', 'medication')", value="grapes")
    if kb_query:
        docs = st.session_state.kb.query(kb_query, top_k=2)
        if docs:
            for d in docs:
                st.markdown(f"#### 📖 [{d.category}] {d.title}")
                st.write(d.content)
        else:
            st.info("No matching knowledge documents found.")
