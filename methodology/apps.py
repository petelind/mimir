from django.apps import AppConfig


class MethodologyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "methodology"
    
    def ready(self):
        """Import signals when app is ready."""
        import methodology.signals  # noqa: F401
