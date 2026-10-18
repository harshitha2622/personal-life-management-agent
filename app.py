import streamlit as st
from datetime import date, datetime

from database.db import (
    initialize_database,
    add_task,
    get_tasks,
    update_task_status,
    delete_task,
    add_goal,
    get_goals,
    update_goal_progress,
    delete_goal,
)

# ---------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------

st.set_page_config(
    page_title="LifeOS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------

initialize_database()

# ---------------------------------------
# CUSTOM STYLING
# ---------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMetric"] {
            background: rgba(128, 128, 128, 0.08);
            padding: 18px;
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

with st.sidebar:

    st.title("🧠 LifeOS AI")

    st.caption("Your Personal Life Management Agent")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "My Tasks",
            "My Goals",
            "Daily Planner",
            "Habits",
            "Analytics",
            "AI Assistant",
        ],
    )

    st.divider()

    st.caption("Plan better. Live better.")

# ---------------------------------------
# LOAD TASKS FROM SQLITE
# ---------------------------------------

tasks = get_tasks()

# ---------------------------------------
# DASHBOARD
# ---------------------------------------

if page == "Dashboard":

    st.title("Welcome to LifeOS AI 👋")

    st.write(
        "Your personal space to plan, organize, and grow."
    )

    total_tasks = len(tasks)

    completed_tasks = sum(
        task["completed"] for task in tasks
    )

    pending_tasks = total_tasks - completed_tasks

    completion_rate = (
        completed_tasks / total_tasks * 100
        if total_tasks > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total_tasks)

    col2.metric("Completed", completed_tasks)

    col3.metric("Pending", pending_tasks)

    col4.metric(
        "Completion Rate",
        f"{completion_rate:.0f}%",
    )

    st.divider()

    st.subheader("Today's Tasks")

    today = date.today().isoformat()

    todays_tasks = [
        task for task in tasks
        if task["deadline"] == today
    ]

    if not todays_tasks:

        st.info("No tasks are due today.")

    else:

        for task in todays_tasks:

            status = (
                "✅" if task["completed"]
                else "⏳"
            )

            st.write(
                f"{status} {task['title']}"
            )

    st.divider()

    if st.button("➕ Create a New Task"):

        st.session_state.quick_add = True

    if st.session_state.get("quick_add", False):

        with st.form("quick_task_form"):

            quick_title = st.text_input("Task title")

            submitted = st.form_submit_button("Save Task")

            if submitted:

                if quick_title.strip():

                    add_task(
                        title=quick_title.strip(),
                        priority="Medium",
                        duration=30,
                        deadline=today,
                        created_at=datetime.now().isoformat(),
                    )

                    st.session_state.quick_add = False

                    st.success("Task saved successfully!")

                    st.rerun()

                else:

                    st.warning("Enter a task title.")

# ---------------------------------------
# TASK MANAGER
# ---------------------------------------

elif page == "My Tasks":

    st.title("📝 My Tasks")

    st.write(
        "Create, prioritize, and track your tasks."
    )

    with st.form(
        "add_task_form",
        clear_on_submit=True,
    ):

        title = st.text_input("Task title")

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"],
        )

        duration = st.number_input(
            "Estimated duration (minutes)",
            min_value=5,
            max_value=1440,
            value=30,
            step=5,
        )

        deadline = st.date_input(
            "Deadline",
            value=date.today(),
        )

        submitted = st.form_submit_button("Add Task")

        if submitted:

            if title.strip():

                add_task(
                    title=title.strip(),
                    priority=priority,
                    duration=int(duration),
                    deadline=deadline.isoformat(),
                    created_at=datetime.now().isoformat(),
                )

                st.success("Task saved successfully!")

                st.rerun()

            else:

                st.warning("Please enter a task title.")

    st.divider()

    st.subheader("Your Task List")

    tasks = get_tasks()

    if not tasks:

        st.info("No tasks yet. Add your first task!")

    for task in tasks:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.write(f"**{task['title']}**")

                st.caption(
                    f"Priority: {task['priority']} | "
                    f"Duration: {task['duration']} minutes | "
                    f"Deadline: {task['deadline']}"
                )

            with col2:

                completed = st.checkbox(
                    "Completed",
                    value=bool(task["completed"]),
                    key=f"complete_{task['id']}",
                )

                if completed != bool(task["completed"]):

                    update_task_status(
                        task["id"],
                        completed,
                    )

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task['id']}",
                ):

                    delete_task(task["id"])

                    st.rerun()

# ---------------------------------------
# FUTURE MODULES
# ---------------------------------------

elif page == "My Goals":

    st.title("🎯 My Goals")

    st.info(
        "Goal management will be implemented next."
    )

elif page == "Daily Planner":

    st.title("📅 Daily Planner")

    st.info(
        "Intelligent scheduling will be implemented next."
    )

elif page == "Habits":

    st.title("🔁 Habit Tracker")

    st.info(
        "Habit tracking will be implemented next."
    )

elif page == "Analytics":

    st.title("📊 Productivity Analytics")

    st.info(
        "Productivity analytics will be implemented next."
    )

elif page == "AI Assistant":

    st.title("🤖 LifeOS AI Assistant")

    st.info(
        "The AI agent will be integrated in a later phase."
    )