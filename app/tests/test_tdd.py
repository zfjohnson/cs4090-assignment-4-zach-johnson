import pytest
from app.src.tasks import sort_tasks, suggest_task, get_progress
from datetime import datetime
from datetime import timedelta

def test_sort_tasks():
    tasks = [
        {"id": 1, "title": "Task 1", "due_date": "2023-10-01", "priority": "High"},
        {"id": 2, "title": "Task 2", "due_date": "2023-09-01", "priority": "Low"},
        {"id": 3, "title": "Task 3", "due_date": "2023-11-01", "priority": "Medium"},
    ]
    
    # Test sorting by due date
    sorted_tasks = sort_tasks(tasks, "Due Date")
    assert sorted_tasks[0]["id"] == 2
    assert sorted_tasks[1]["id"] == 1
    assert sorted_tasks[2]["id"] == 3
    
    # Test sorting by priority (High to Low)
    sorted_tasks = sort_tasks(tasks, "Priority (High to Low)")
    assert sorted_tasks[0]["id"] == 1
    assert sorted_tasks[1]["id"] == 3
    assert sorted_tasks[2]["id"] == 2
    
    # Test sorting by priority (Low to High)
    sorted_tasks = sort_tasks(tasks, "Priority (Low to High)")
    assert sorted_tasks[0]["id"] == 2
    assert sorted_tasks[1]["id"] == 3
    assert sorted_tasks[2]["id"] == 1

def test_suggest_task():
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_later = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    three_days_later = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    four_days_later = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    seven_days_later = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    eight_days_later = (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d")
    # Should choose the task due within 1 day
    tasks = [
        {"id": 1, "title": "Task 1", "due_date": tomorrow, "priority": "Low"},
        {"id": 2, "title": "Task 2", "due_date": two_days_later, "priority": "High"},
    ]
    
    # Test suggesting a task
    suggested_task = suggest_task(tasks)
    assert suggested_task["id"] == 1

    tasks = [
        {"id": 1, "title": "Task 1", "due_date": three_days_later, "priority": "Medium"},
        {"id": 2, "title": "Task 2", "due_date": four_days_later, "priority": "High"},
    ]

    suggested_task = suggest_task(tasks)
    assert suggested_task["id"] == 1
    tasks = [
        {"id": 1, "title": "Task 1", "due_date": seven_days_later, "priority": "High"},
        {"id": 2, "title": "Task 2", "due_date": eight_days_later, "priority": "High"},
    ]
    suggested_task = suggest_task(tasks)
    assert suggested_task["id"] == 1

    tasks = [
        {"id": 1, "title": "Task 1", "due_date": today, "priority": "High"},
        {"id": 2, "title": "Task 2", "due_date": tomorrow, "priority": "Low"},
    ]
    suggested_task = suggest_task(tasks)
    assert suggested_task["id"] == 1

def test_get_progress():
    tasks = [
        {"id": 1, "title": "Task 1", "completed": True},
        {"id": 2, "title": "Task 2", "completed": False},
        {"id": 3, "title": "Task 3", "completed": True},
    ]
    
    progress, completed_tasks = get_progress(tasks)
    assert progress == 66.67
    assert completed_tasks == 2
    tasks = []
    progress, completed_tasks = get_progress(tasks)
    assert progress == 0
    assert completed_tasks == 0
