Feature: Search tasks
  Scenario: User searches for a task by title
    Given tasks exist with titles "Alpha Task" and "Beta Task"
    When the user searches for "Alpha"
    Then only "Alpha Task" should be shown in the search results