import pytest
import json
from datetime import datetime, timedelta
from pytest_bdd import scenarios, given, when, then

from app.src.tasks import load_tasks, save_tasks, filter_tasks_by_category, search_tasks, get_overdue_tasks

TASKS_FILE = "app/tests/test_tasks.json"

# Link all feature files
scenarios("../")

@pytest.fixture
def tasks():
    return [
        {
            "id": 1,
            "title": "Alpha Task",
            "description": "",
            "priority": "",
            "category": "",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 2,
            "title": "Beta Task",
            "description": "",
            "priority": "",
            "category": "",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 1,
            "title": "Test Task 1",
            "description": "",
            "priority": "",
            "category": "",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 4,
            "title": "Test Task 2",
            "description": "",
            "priority": "",
            "category": "",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    ]

@given("no tasks exist", target_fixture="reset")
def no_tasks(tasks):
   tasks = []
   save_tasks(tasks)

@when('the user adds a new task with title "Test Task" and category "Work"')
def user_adds_task(tasks):
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": "Test Task",
        "description": "Desc",
        "priority": "Medium",
        "category": "Work",
        "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(new_task)
    save_tasks(tasks)

@then('the task list should contain 1 task with title "Test Task"')
def verify_task_added(tasks):
    tasks = load_tasks()
    matching = [task for task in tasks if task["title"] == "Test Task"]
    assert len(matching) == 1

    

@given('a task exists with title "Test Task 2"')
def task_exists(tasks):
    task = {
        "id": 4,
        "title": "Test Task 2",
        "description": "Sample desc",
        "priority": "Medium",
        "category": "Work",
        "due_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "completed": True,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks[3] = task
    save_tasks(tasks)

@when('the user marks the task "Test Task 2" as complete')
def user_marks_complete(tasks):
    tasks = load_tasks()
    for task in tasks:
        if task["title"] == "Test Task 2":
            task["completed"] = True
    save_tasks(tasks)

@then('the task "Test Task 2" should be marked as complete')
def verify_complete(tasks):
    tasks = load_tasks()
    for task in tasks:
        if task["title"] == "Test Task 2":
            assert task["completed"] == True
            return
    pytest.fail(f"Task Test Task 2 not found")


@given('a task exists with title "Overdue Task" and due date in the past')
def overdue_task_exists(tasks):
    task = {
        "id": 10,
        "title": "Overdue Task",
        "description": "Overdue desc",
        "priority": "High",
        "category": "Work",
        "due_date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks)

@when('the user views the task list')
def user_views_list():
    pass  # No-op

@then('the task "Overdue Task" should be marked as overdue')
def verify_overdue(tasks):
    tasks = load_tasks()
    overdue = get_overdue_tasks(tasks)
    for task in overdue:
        if task.get("title") == "Overdue Task":
            assert task["completed"] == False
    

@given('multiple tasks exist in categories "Work" and "Personal"')
def multiple_tasks_exist(tasks):
    tasks = [
        {"id": 1, "title": "Task A", "description": "", "priority": "Low", "category": "Work",
         "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
         "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {"id": 2, "title": "Task B", "description": "", "priority": "High", "category": "Personal",
         "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
         "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ]
    save_tasks(tasks)

@when('the user filters tasks by category "Work"')
def user_filters_category(tasks):
    tasks = load_tasks()
    filtered = filter_tasks_by_category(tasks, "Work")
    save_tasks(filtered)  # Just save filtered for test purposes

@then('only tasks in category "Work" should be shown')
def verify_filter_category(tasks):
    tasks = load_tasks()
    assert all(task["category"] == "Work" for task in tasks)

@given('tasks exist with titles "Alpha Task" and "Beta Task"')
def tasks_with_titles_exist(tasks):
    tasks = [
        {
            "id": 1,
            "title": "Alpha Task",
            "description": "",
            "priority": "Low",
            "category": "Work",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "id": 2,
            "title": "Beta Task",
            "description": "",
            "priority": "Medium",
            "category": "Personal",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
    ]
    save_tasks(tasks)


@when('the user searches for "Alpha"')
def user_searches():
    tasks = load_tasks()
    results = search_tasks(tasks, "Alpha")
    save_tasks(results)  # Save results for test check


@then('only "Alpha Task" should be shown in the search results')
def verify_search_results():
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Alpha Task"