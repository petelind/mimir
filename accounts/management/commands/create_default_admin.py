"""Management command to create default admin user."""
import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Create default admin user for development."""
    
    help = 'Creates default admin user (username: admin, password: admin)'
    
    def handle(self, *args, **options):
        """Execute command to create default admin user."""
        username = 'admin'
        password = 'admin'
        email = 'admin@example.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'User "{username}" already exists. Skipping creation.'
                )
            )
            logger.info(f'User "{username}" already exists')
            return
        
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created superuser "{username}" with password "{password}"'
                )
            )
            logger.info(f'Created superuser "{username}"')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Error creating superuser: {e}'
                )
            )
            logger.error(f'Error creating superuser: {e}')
            raise
