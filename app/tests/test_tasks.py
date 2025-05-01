import pytest
from app.src.tasks import load_tasks, save_tasks, generate_unique_id, filter_tasks_by_priority, filter_tasks_by_category, filter_tasks_by_completion, search_tasks, get_overdue_tasks
from datetime import datetime

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "School", "completed": True, "due_date": "2025-05-03"},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "completed": False, "due_date": "2025-04-10"},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "Work", "completed": False, "due_date": "2025-04-01"}
    ]

def test_load():
    # Test loading tasks from a valid JSON file
    tasks = load_tasks("src/tasks.json")
    assert isinstance(tasks, list)
    assert all(isinstance(task, dict) for task in tasks)

    # Test from an empty file
    tasks = load_tasks("empty_tasks.json")
    assert tasks == []

    # Test from a non-existent file
    tasks = load_tasks("non_existent_file.json")
    assert tasks == []

def test_save():
    # Test saving tasks to a JSON file
    tasks = [{"id": 1, "title": "Test Task", "completed": False}]
    save_tasks(tasks, "app/tests/test_tasks.json")
    
    loaded_tasks = load_tasks("app/tests/test_tasks.json")
    assert loaded_tasks == tasks

def test_generate_unique_id():
    # Test generating unique IDs
    tasks = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    new_id = generate_unique_id(tasks)
    assert new_id == 3

    tasks = []
    new_id = generate_unique_id(tasks)
    assert new_id == 1

def test_filter_tasks_by_priority(sample_tasks):
    filtered_tasks = filter_tasks_by_priority(sample_tasks, "High")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 1

    filtered_tasks = filter_tasks_by_priority(sample_tasks, "Low")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 2

    filtered_tasks = filter_tasks_by_priority(sample_tasks, "Medium")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 3

    filtered_tasks = filter_tasks_by_priority(sample_tasks, "Non-existent")
    assert len(filtered_tasks) == 0

def test_filter_tasks_by_category(sample_tasks):
    filtered_tasks = filter_tasks_by_category(sample_tasks, "School")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 1

    filtered_tasks = filter_tasks_by_category(sample_tasks, "Personal")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 2

    filtered_tasks = filter_tasks_by_category(sample_tasks, "Work")
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 3

    filtered_tasks = filter_tasks_by_category(sample_tasks, "Non-existent")
    assert len(filtered_tasks) == 0

def test_filter_tasks_by_completion(sample_tasks):
    filtered_tasks = filter_tasks_by_completion(sample_tasks)
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["id"] == 1

    filtered_tasks = filter_tasks_by_completion(sample_tasks, False)
    assert len(filtered_tasks) == 2
    assert filtered_tasks[0]["id"] == 2
    assert filtered_tasks[1]["id"] == 3

def test_search_tasks():
    tasks = [{"id": 1, "title": "Task 1"}, {"id": 2, "title": "Task 2"}]
    search_result = search_tasks(tasks, "Task 1")
    assert len(search_result) == 1
    assert search_result[0]["id"] == 1

    search_result = search_tasks(tasks, "Non-existent Task")
    assert len(search_result) == 0
    tasks = []
    search_result = search_tasks(tasks, "Task 1")
    assert len(search_result) == 0


def test_get_overdue_tasks():
    print(datetime.now().strftime("%Y-%m-%d"))
    tasks =[{"id": 1, "title": "Task 1", "completed": False, "due_date": "2025-05-03"}, 
            {"id": 2, "title": "Task 2", "completed": True, "due_date": "2025-04-10"},
            {"id": 3, "title": "Task 3", "completed": False, "due_date": "2025-04-01"}]
    overdue_tasks = get_overdue_tasks(tasks)
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0]["id"] == 3