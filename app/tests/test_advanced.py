from unittest.mock import patch
import pytest

from app.src.tasks import filter_tasks_by_priority

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "category": "School", "completed": True, "due_date": "2025-05-03"},
        {"id": 2, "title": "Task 2", "priority": "Low", "category": "Personal", "completed": False, "due_date": "2025-04-10"},
        {"id": 3, "title": "Task 3", "priority": "Medium", "category": "Work", "completed": False, "due_date": "2025-04-01"},
        {"id": 4, "title": "Task 4", "priority": "Medium", "category": "Work", "completed": False, "due_date": "2025-04-01"},
        {"id": 5, "title": "Task 5", "priority": "High", "category": "School", "completed": False, "due_date": "2025-04-01"},
        {"id": 6, "title": "Task 6", "priority": "Medium", "category": "Work", "completed": True, "due_date": "2025-04-01"},
    ]

@pytest.mark.parametrize("priority,expected_count", [
    ("High", 2),
    ("Medium", 3),
    ("Low", 1),
])
def test_filter_by_priority(sample_tasks, priority, expected_count):
    result = filter_tasks_by_priority(sample_tasks, priority)
    assert len(result) == expected_count