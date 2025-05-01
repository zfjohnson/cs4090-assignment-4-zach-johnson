import streamlit as st
import pandas as pd
from datetime import datetime
from tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, search_tasks, get_overdue_tasks, sort_tasks, suggest_task, get_progress
import subprocess

# Additions/Bug-fixes marked with "New -"

def main():
    TEST_PATH = "app/tests/test_advanced.py"
    TEST_FUNCTION = "test_filter_by_priority"
    test_button = st.button("Run all tests")
    if test_button:
        running_text = st.text("Running tests...")
        result = subprocess.run(
            ["pytest", "--cov=app", "--html=app/tests/report.html", "--self-contained-html"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results", result.stdout + result.stderr, height=300)
        running_text.text("Tests completed!")
    if st.button("Run unit tests"):
        running_text = st.text("Running unit tests...")
        result = subprocess.run(
            ["pytest", "app/tests/unit_tests/test_tasks.py", "--tb=short"],
            capture_output=True,
            text=True
        )
        st.text_area("Unit Test Results", result.stdout + result.stderr, height=300)
        running_text.text("Unit tests completed!")
    if st.button("Run Parameterized Test"):
        running_text = st.text("Running parameterized test...")
        result = subprocess.run(
            ["pytest", f"{TEST_PATH}::{TEST_FUNCTION}", "--tb=short"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results", result.stdout + result.stderr, height=300)
        running_text.text("Test completed!")
    # New - Button to run tests
    
    
    # Buttons to run specific tests in test_tasks.py
    if st.button("Run Test: Filter by Priority"):
        result = subprocess.run(
            ["pytest", "app/tests/test_tasks.py::test_filter_tasks_by_priority"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results (Filter by Priority)", result.stdout + result.stderr, height=300)

    if st.button("Run Test: Filter by Category"):
        result = subprocess.run(
            ["pytest", "app/tests/test_tasks.py::test_filter_tasks_by_category"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results (Filter by Category)", result.stdout + result.stderr, height=300)

    if st.button("Run Test: Filter by Completion"):
        result = subprocess.run(
            ["pytest", "app/tests/test_tasks.py::test_filter_tasks_by_completion"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results (Filter by Completion)", result.stdout + result.stderr, height=300)

    if st.button("Run Test: Search Tasks"):
        result = subprocess.run(
            ["pytest", "app/tests/test_tasks.py::test_search_tasks"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results (Search Tasks)", result.stdout + result.stderr, height=300)

    if st.button("Run Test: Get Overdue Tasks"):
        result = subprocess.run(
            ["pytest", "app/tests/test_tasks.py::test_get_overdue_tasks"],
            capture_output=True,
            text=True
        )
        st.text_area("Test Results (Get Overdue Tasks)", result.stdout + result.stderr, height=300)


    # New - Button to run BDD tests
    bdd_button = st.button("BDD Tests")
    if bdd_button:
        result = subprocess.run(
            ["pytest", "app/tests/feature/steps/test_bdd_steps.py"],
            capture_output=True,
            text=True
        )
        st.text_area("BDD Test Results", result.stdout + result.stderr, height=300)
        st.text("BDD tests completed!")

    
    st.title("To-Do Application")

    # Load existing tasks
    tasks = load_tasks()
    
    # Sidebar for adding new tasks
    st.sidebar.header("Add New Task")
    
    # Task creation form
    with st.sidebar.form("new_task_form"):
        task_title = st.text_input("Task Title")
        task_description = st.text_area("Description")
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        task_category = st.selectbox("Category", ["Work", "Personal", "School", "Other"])
        task_due_date = st.date_input("Due Date")
        submit_button = st.form_submit_button("Add Task")

        if submit_button and task_title:
            new_task = {
                "id": generate_unique_id(tasks),
                "title": task_title,
                "description": task_description,
                "priority": task_priority,
                "category": task_category,
                "due_date": task_due_date.strftime("%Y-%m-%d"),
                "completed": False,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            tasks.append(new_task)
            save_tasks(tasks)
            st.sidebar.success("Task added successfully!")
    
    # Main area to display tasks
    st.header("Your Tasks")
    
    # Calculate task completion percentage
    progress, completed_tasks = get_progress(tasks)

    # Display progress bar
    st.write("### Task Completion Progress")
    st.progress(int(progress))
    st.write(f"{completed_tasks} of {len(tasks)} tasks completed ({int(progress)}%)")
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_category = st.selectbox("Filter by Category", ["All"] + list(set([task["category"] for task in tasks])))
    with col2:
        filter_priority = st.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    with col3: 
        sort_selection = st.selectbox("Sort by", ["None", "Due Date", "Priority (High to Low)", "Priority (Low to High)"])
    show_completed = st.checkbox("Show Completed Tasks")
    
    # Apply filters
    filtered_tasks = tasks.copy()
    if filter_category != "All":
        filtered_tasks = filter_tasks_by_category(filtered_tasks, filter_category)
    if filter_priority != "All":
        filtered_tasks = filter_tasks_by_priority(filtered_tasks, filter_priority)
    if not show_completed:
        filtered_tasks = [task for task in filtered_tasks if not task["completed"]]
    
    # New - Get overdue tasks
    overdue_tasks = [task.get("id") for task in get_overdue_tasks(tasks)]

    # New - Show overdue tasks
    
    if overdue_tasks:
        st.warning("You have overdue tasks!")
        for task in get_overdue_tasks(tasks):
            st.markdown(f"**{task['title']}** Due: {task['due_date']}")


    # New - Sort tasks
    sorted_tasks = sort_tasks(filtered_tasks, sort_selection)
    
    

    # New - Search functionality
    search_query = st.text_input("Search Tasks")
    if search_query:
        sorted_tasks = search_tasks(sorted_tasks, search_query)
   
    # New - Display suggested task in a colored box
    suggested_task = suggest_task(sorted_tasks)
    if suggested_task:
        st.success(f"Suggested Task: {suggested_task['title']} - {suggested_task['description']}")
        st.caption(f"Due: {suggested_task['due_date']} | Priority: {suggested_task['priority']}")
    
    st.write("### Task List")
    # Display tasks
    for task in sorted_tasks:
        col1, col2 = st.columns([4, 1])
        with col1:
            if task["completed"]:
                st.markdown(f"~~**{task['title']}**~~")
            elif task.get("id") in overdue_tasks:
                st.markdown(f"<span style='color: red;'>**{task['title']}** (Overdue)</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"**{task['title']}**")
            st.write(task["description"])
            st.caption(f"Due: {task['due_date']} | Priority: {task['priority']} | Category: {task['category']}")
        with col2:
            if st.button("Complete" if not task["completed"] else "Undo", key=f"complete_{task['id']}"):
                for t in tasks:
                    if t["id"] == task["id"]:
                        t["completed"] = not t["completed"]
                        save_tasks(tasks)
                        st.rerun()
            if st.button("Delete", key=f"delete_{task['id']}"):
                tasks = [t for t in tasks if t["id"] != task["id"]]
                save_tasks(tasks)
                st.rerun()

if __name__ == "__main__":
    main()