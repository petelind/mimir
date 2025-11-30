"""
Django management command to run the MCP server.

Usage:
    python manage.py mcp_server --user=<username>
"""
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


class Command(BaseCommand):
    help = 'Run the MCP (Model Context Protocol) server'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username for MCP context (e.g., admin, maria)'
        )

    def handle(self, *args, **options):
        username = options['user']
        
        # Get user from database
        try:
            user = User.objects.get(username=username)
            logger.info(f'MCP Server: Starting for user {username} (id={user.id})')
            self.stdout.write(self.style.SUCCESS(f'MCP Server: User context set to {username}'))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User "{username}" not found in database'))
            self.stderr.write(self.style.WARNING('Available users:'))
            for u in User.objects.all()[:10]:
                self.stderr.write(f'  - {u.username}')
            return
        
        # Set user context
        from mcp_integration.context import set_current_user
        set_current_user(user)
        
        # Initialize and run FastMCP server
        from mcp_integration.tools import initialize_mcp
        mcp = initialize_mcp()
        
        self.stdout.write(self.style.SUCCESS('MCP Server: Starting FastMCP server...'))
        logger.info('MCP Server: FastMCP initialized with 16 tools')
        
        # Run the server

        # Run the server with explicit stdio transport
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
        mcp.run(transport="stdio")
