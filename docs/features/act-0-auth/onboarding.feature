Feature: ✅ FOB-ONBOARDING-1 First-Time User Onboarding
  As a new user (Maria)
  I want to complete onboarding
  So that I understand how to use FOB

  Scenario: ✅ ONBOARD-01 Welcome screen
    Given Maria just registered
    When she lands on FOB-ONBOARDING-1
    Then she sees "Welcome to FOB" message
    And she sees onboarding steps overview

  Scenario: ONBOARD-02 Create first playbook
    Given Maria is in onboarding
    When she clicks [Create My First Playbook]
    Then she is guided through playbook creation
    And she creates a sample playbook

  Scenario: ONBOARD-03 Tour of features ✅
    Given Maria completed first playbook
    When she proceeds with tour
    Then she sees highlights of: Workflows, Activities, Artifacts, Sync

Scenario: ONBOARD-04 Skip onboarding ✅
    Given Maria is in onboarding
    When she clicks [Skip Tour]
    Then she is redirected to FOB-DASHBOARD-1

  Scenario: ONBOARD-05 Complete onboarding ✅
    Given Maria finished the tour
    When she clicks [Get Started]
    Then onboarding is marked complete
    And she is redirected to FOB-DASHBOARD-1
