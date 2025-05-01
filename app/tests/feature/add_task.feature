Feature: Add a new task
  Scenario: User adds a task with title, description, priority, category, and due date
    Given no tasks exist
    When the user adds a new task with title "Test Task" and category "Work"
    Then the task list should contain 1 task with title "Test Task"