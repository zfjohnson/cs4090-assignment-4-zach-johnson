Feature: Filter tasks by category
  Scenario: User filters tasks by category "Work"
    Given multiple tasks exist in categories "Work" and "Personal"
    When the user filters tasks by category "Work"
    Then only tasks in category "Work" should be shown