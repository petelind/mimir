"""MCP Django app configuration."""
from django.apps import AppConfig


class McpConfig(AppConfig):
    """Configuration for MCP (Model Context Protocol) app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcp'
    verbose_name = 'MCP Integration'
