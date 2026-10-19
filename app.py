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

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="LifeOS AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# DATABASE INITIALIZATION
# =====================================================

initialize_database()

# =====================================================
# CUSTOM STYLING
# =====================================================

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

        div[data-testid="stMetric"] {
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

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

# =====================================================
# DASHBOARD
# =====================================================

if page == "Dashboard":

    st.title("Welcome to LifeOS AI 👋")

    st.write(
        "Your personal space to plan, organize, and grow."
    )

    tasks = get_tasks()
    goals = get_goals()

    total_tasks = len(tasks)

    completed_tasks = sum(
        bool(task["completed"])
        for task in tasks
    )

    pending_tasks = total_tasks - completed_tasks

    completion_rate = (
        completed_tasks / total_tasks * 100
        if total_tasks > 0
        else 0
    )

    # Dashboard metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Tasks",
        total_tasks,
    )

    col2.metric(
        "Completed",
        completed_tasks,
    )

    col3.metric(
        "Pending",
        pending_tasks,
    )

    col4.metric(
        "Completion Rate",
        f"{completion_rate:.0f}%",
    )

    st.divider()

    # Today's tasks

    st.subheader("📅 Today's Tasks")

    today = date.today().isoformat()

    todays_tasks = [
        task
        for task in tasks
        if task["deadline"] == today
    ]

    if not todays_tasks:

        st.info("No tasks are due today.")

    else:

        for task in todays_tasks:

            status = (
                "✅"
                if task["completed"]
                else "⏳"
            )

            st.write(
                f"{status} **{task['title']}**"
            )

            st.caption(
                f"Priority: {task['priority']} | "
                f"Duration: {task['duration']} minutes"
            )

    st.divider()

    # Goal overview

    st.subheader("🎯 Goal Overview")

    total_goals = len(goals)

    completed_goals = sum(
        goal["status"] == "Completed"
        for goal in goals
    )

    goal_col1, goal_col2 = st.columns(2)

    goal_col1.metric(
        "Total Goals",
        total_goals,
    )

    goal_col2.metric(
        "Completed Goals",
        completed_goals,
    )

    st.divider()

    # Quick task creation

    st.subheader("⚡ Quick Actions")

    if st.button(
        "➕ Create a New Task",
        use_container_width=False,
    ):

        st.session_state["show_quick_task_form"] = True

    if st.session_state.get(
        "show_quick_task_form",
        False,
    ):

        with st.form("quick_task_form"):

            quick_title = st.text_input(
                "Task title",
                placeholder="Example: Practice Python DSA",
            )

            quick_priority = st.selectbox(
                "Priority",
                ["High", "Medium", "Low"],
            )

            quick_deadline = st.date_input(
                "Deadline",
                value=date.today(),
                key="quick_task_deadline",
            )

            submitted = st.form_submit_button(
                "Save Task",
                use_container_width=True,
            )

            if submitted:

                if not quick_title.strip():

                    st.error("Please enter a task title.")

                else:

                    add_task(
                        title=quick_title.strip(),
                        priority=quick_priority,
                        duration=30,
                        deadline=quick_deadline.isoformat(),
                        created_at=datetime.now().isoformat(),
                    )

                    st.session_state[
                        "show_quick_task_form"
                    ] = False

                    st.success("Task saved successfully!")

                    st.rerun()

# =====================================================
# TASK MANAGEMENT
# =====================================================

elif page == "My Tasks":

    st.title("📝 My Tasks")

    st.write(
        "Organize your daily activities and track your progress."
    )

    # Create task

    with st.form(
        "add_task_form",
        clear_on_submit=True,
    ):

        title = st.text_input(
            "Task title",
            placeholder="Example: Complete Python practice",
        )

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

        submitted = st.form_submit_button(
            "➕ Add Task",
            use_container_width=True,
        )

        if submitted:

            if not title.strip():

                st.error("Please enter a task title.")

            else:

                add_task(
                    title=title.strip(),
                    priority=priority,
                    duration=int(duration),
                    deadline=deadline.isoformat(),
                    created_at=datetime.now().isoformat(),
                )

                st.success("Task saved successfully!")

                st.rerun()

    st.divider()

    # Retrieve saved tasks

    tasks = get_tasks()

    st.subheader("Your Task List")

    if not tasks:

        st.info(
            "Your task list is empty. Create your first task above!"
        )

    # Display tasks

    for task in tasks:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                if task["completed"]:

                    st.markdown(
                        f"~~{task['title']}~~"
                    )

                else:

                    st.markdown(
                        f"**{task['title']}**"
                    )

                st.caption(
                    f"Priority: {task['priority']} | "
                    f"Duration: {task['duration']} minutes | "
                    f"Deadline: {task['deadline']}"
                )

                if task["deadline"] < date.today().isoformat() and not task["completed"]:

                    st.warning("⚠️ This task is overdue.")

            with col2:

                completed = st.checkbox(
                    "Completed",
                    value=bool(task["completed"]),
                    key=f"complete_task_{task['id']}",
                )

                if completed != bool(task["completed"]):

                    update_task_status(
                        task["id"],
                        completed,
                    )

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_task_{task['id']}",
                ):

                    delete_task(task["id"])

                    st.rerun()

# =====================================================
# GOAL MANAGEMENT
# =====================================================

elif page == "My Goals":

    st.title("🎯 My Goals")

    st.write(
        "Turn your ambitions into measurable progress."
    )

    # Create a new goal

    with st.expander(
        "➕ Create a New Goal",
        expanded=True,
    ):

        with st.form("create_goal_form"):

            title = st.text_input(
                "Goal title",
                placeholder="Example: Get placed in a Data Science role",
            )

            category = st.selectbox(
                "Category",
                [
                    "Career",
                    "Learning",
                    "Project",
                    "Health",
                    "Personal",
                    "Finance",
                    "Other",
                ],
            )

            description = st.text_area(
                "Description",
                placeholder="Describe what you want to achieve...",
            )

            col1, col2 = st.columns(2)

            with col1:

                start_date = st.date_input(
                    "Start date",
                    value=date.today(),
                    key="goal_start_date",
                )

            with col2:

                target_date = st.date_input(
                    "Target date",
                    value=date.today(),
                    key="goal_target_date",
                )

            submitted = st.form_submit_button(
                "Create Goal",
                use_container_width=True,
            )

            if submitted:

                if not title.strip():

                    st.error("Please enter a goal title.")

                elif target_date < start_date:

                    st.error(
                        "Target date cannot be earlier than the start date."
                    )

                else:

                    add_goal(
                        title=title.strip(),
                        category=category,
                        description=description.strip(),
                        start_date=start_date.isoformat(),
                        target_date=target_date.isoformat(),
                    )

                    st.success("Goal created successfully!")

                    st.rerun()

    st.divider()

    # Goal statistics

    goals = get_goals()

    total_goals = len(goals)

    completed_goals = sum(
        goal["status"] == "Completed"
        for goal in goals
    )

    active_goals = sum(
        goal["status"] == "Active"
        for goal in goals
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Goals",
        total_goals,
    )

    col2.metric(
        "Active Goals",
        active_goals,
    )

    col3.metric(
        "Completed Goals",
        completed_goals,
    )

    st.divider()

    # Display saved goals

    st.subheader("Your Goals")

    if not goals:

        st.info(
            "No goals yet. Create your first goal above!"
        )

    for goal in goals:

        with st.container(border=True):

            header_col, status_col = st.columns([4, 1])

            with header_col:

                st.subheader(goal["title"])

                st.caption(
                    f"Category: {goal['category']} | "
                    f"Target date: {goal['target_date']}"
                )

            with status_col:

                if goal["status"] == "Completed":

                    st.success("Completed")

                else:

                    st.info("Active")

            if goal["description"]:

                st.write(goal["description"])

            st.progress(
                goal["progress"] / 100,
                text=f"Progress: {goal['progress']}%",
            )

            new_progress = st.slider(
                "Update progress",
                min_value=0,
                max_value=100,
                value=goal["progress"],
                step=5,
                key=f"goal_progress_{goal['id']}",
            )

            if new_progress != goal["progress"]:

                update_goal_progress(
                    goal["id"],
                    new_progress,
                )

                st.rerun()

            if st.button(
                "🗑️ Delete Goal",
                key=f"delete_goal_{goal['id']}",
            ):

                delete_goal(goal["id"])

                st.rerun()

# =====================================================
# DAILY PLANNER
# =====================================================

elif page == "Daily Planner":

    st.title("📅 Daily Planner")

    st.write(
        "Your daily schedule and time-management workspace."
    )

    st.info(
        "Intelligent scheduling will be implemented in the next phase."
    )

# =====================================================
# HABIT TRACKER
# =====================================================

elif page == "Habits":

    st.title("🔁 Habit Tracker")

    st.info(
        "Habit tracking will be implemented in the next phase."
    )

# =====================================================
# PRODUCTIVITY ANALYTICS
# =====================================================

elif page == "Analytics":

    st.title("📊 Productivity Analytics")

    tasks = get_tasks()

    total_tasks = len(tasks)

    completed_tasks = sum(
        bool(task["completed"])
        for task in tasks
    )

    pending_tasks = total_tasks - completed_tasks

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Tasks",
        total_tasks,
    )

    col2.metric(
        "Completed Tasks",
        completed_tasks,
    )

    col3.metric(
        "Pending Tasks",
        pending_tasks,
    )

    if total_tasks > 0:

        completion_rate = (
            completed_tasks / total_tasks
        )

        st.subheader("Task Completion Progress")

        st.progress(
            completion_rate,
            text=f"{completion_rate * 100:.0f}% completed",
        )

    else:

        st.info(
            "Add some tasks to start tracking your productivity."
        )

# =====================================================
# AI ASSISTANT
# =====================================================

elif page == "AI Assistant":

    st.title("🤖 LifeOS AI Assistant")

    st.write(
        "Your personal assistant for planning and productivity."
    )

    st.info(
        "The AI agent will be integrated in the next phase."
    )

    st.caption(
        "Planned capabilities include task prioritization, "
        "goal-based planning, and schedule recommendations."
    )