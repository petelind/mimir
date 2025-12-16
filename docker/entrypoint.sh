#!/bin/bash
set -e

# Create data directory if it doesn't exist
mkdir -p /app/data

# Set default values
export MIMIR_USER=${MIMIR_USER:-admin}
export MIMIR_EMAIL=${MIMIR_EMAIL:-admin@localhost}
export MIMIR_DB_PATH=/app/data/mimir.db

echo "═══════════════════════════════════════════════════════"
echo "🎭 Mimir - Your Self-Evolving Engineering Playbook"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Container Configuration:"
echo "  User: $MIMIR_USER"
echo "  Email: $MIMIR_EMAIL"
echo "  Database: $MIMIR_DB_PATH"
echo "  Data Volume: /app/data"
echo ""

# Check if database exists
if [ ! -f "$MIMIR_DB_PATH" ]; then
    echo "📦 First-time setup: Initializing database..."
    echo ""
    
    # Run migrations
    echo "Running Django migrations..."
    python manage.py migrate --noinput
    
    # Create superuser
    echo "Creating superuser: $MIMIR_USER"
    python manage.py shell << EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='$MIMIR_USER').exists():
    User.objects.create_superuser('$MIMIR_USER', '$MIMIR_EMAIL', 'changeme')
    print('✓ Superuser created successfully')
else:
    print('✓ Superuser already exists')
EOF
    
    echo ""
    echo "✅ Database initialized successfully!"
    echo ""
    echo "⚠️  IMPORTANT: Default password is 'changeme'"
    echo "   Please change it after first login!"
    echo ""
else
    echo "✅ Database found at $MIMIR_DB_PATH"
    echo "   Running migrations to ensure schema is up to date..."
    python manage.py migrate --noinput
    echo ""
fi

echo "═══════════════════════════════════════════════════════"
echo "🚀 Starting Mimir Services"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Services:"
echo "  ✓ Django GUI on http://0.0.0.0:8000"
echo "  ✓ MCP Server (stdio) for $MIMIR_USER"
echo ""
echo "Logs are streamed to stdout/stderr"
echo "═══════════════════════════════════════════════════════"
echo ""

# Start supervisor
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
