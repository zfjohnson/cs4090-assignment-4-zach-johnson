Feature: Get overdue tasks
  Scenario: User views overdue tasks
    Given a task exists with title "Overdue Task" and due date in the past
    When the user views the task list
    Then the task "Overdue Task" should be marked as overdue