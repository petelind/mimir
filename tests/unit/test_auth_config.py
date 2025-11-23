"""Unit tests for authentication configuration."""
from django.conf import settings


def test_login_url_configured():
    """Test LOGIN_URL is set correctly."""
    assert settings.LOGIN_URL == "/auth/user/login/"


def test_login_redirect_url_configured():
    """Test LOGIN_REDIRECT_URL is set correctly."""
    assert settings.LOGIN_REDIRECT_URL == "/dashboard/"


def test_logout_redirect_url_configured():
    """Test LOGOUT_REDIRECT_URL is set correctly."""
    assert settings.LOGOUT_REDIRECT_URL == "/auth/user/login/"


def test_session_cookie_age_default():
    """Test SESSION_COOKIE_AGE is set to 2 weeks by default."""
    assert settings.SESSION_COOKIE_AGE == 1209600


def test_session_save_every_request_enabled():
    """Test SESSION_SAVE_EVERY_REQUEST is enabled."""
    assert settings.SESSION_SAVE_EVERY_REQUEST is True


def test_session_cookie_httponly_enabled():
    """Test SESSION_COOKIE_HTTPONLY is enabled."""
    assert settings.SESSION_COOKIE_HTTPONLY is True


def test_session_cookie_samesite_configured():
    """Test SESSION_COOKIE_SAMESITE is set."""
    assert settings.SESSION_COOKIE_SAMESITE == "Lax"


def test_accounts_app_installed():
    """Test accounts app is in INSTALLED_APPS."""
    assert "accounts" in settings.INSTALLED_APPS


def test_auth_apps_installed():
    """Test Django auth apps are installed."""
    assert "django.contrib.auth" in settings.INSTALLED_APPS
    assert "django.contrib.sessions" in settings.INSTALLED_APPS
