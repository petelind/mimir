Feature: FOB-ERROR-RECOVERY-1 Error Handling and Recovery
  As a methodology author (Maria)
  I want graceful error handling
  So that I can recover from failures without data loss

  Background:
    Given Maria is authenticated in FOB

  Scenario: ERROR-01 Network failure during sync
    Given Maria is syncing a playbook
    When network connection is lost
    Then she sees "Network error" notification
    And sync is paused
    When connection is restored
    Then sync resumes automatically

  Scenario: ERROR-02 Permission denied
    Given Maria tries to edit Mike's playbook
    And she doesn't have edit permission
    Then she sees "Permission denied" error
    And she is shown as read-only viewer

  Scenario: ERROR-03 Upload failure
    Given Maria uploads a large JSON file
    When upload fails
    Then she sees retry option
    And partial upload is not saved

  Scenario: ERROR-04 Corrupted playbook detection
    Given Maria opens a playbook
    When the playbook data is corrupted
    Then she sees "Playbook corrupted" error
    And she can restore from backup or delete

  Scenario: ERROR-05 Empty state handling
    Given Maria views an entity with zero records
    Then she sees helpful empty state message
    And clear action to create first item

  Scenario: ERROR-06 Session timeout
    Given Maria's session expires
    When she attempts an action
    Then she is redirected to login
    And her unsaved changes are preserved

  Scenario: ERROR-07 Validation error recovery
    Given Maria submits invalid form data
    Then she sees specific validation errors
    And form data is preserved
    And she can fix and resubmit
