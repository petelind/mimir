"""Pytest configuration and fixtures for Mimir tests."""

import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Configure database for E2E tests and load fixtures.
    
    Loads test data from tests/fixtures/e2e_seed.json once at session start.
    """
    with django_db_blocker.unblock():
        # Load E2E test fixtures
        call_command('loaddata', 'tests/fixtures/e2e_seed.json')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Enable database access for all tests by default.
    """
    pass
