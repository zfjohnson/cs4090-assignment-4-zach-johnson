Feature: Mark a task as complete
  Scenario: User marks a task as complete
    Given a task exists with title "Test Task 2"
    When the user marks the task "Test Task 2" as complete
    Then the task "Test Task 2" should be marked as complete