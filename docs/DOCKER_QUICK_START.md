# 🐳 Mimir Docker Quick Start

This guide helps you run Mimir using Docker with persistent storage.

## Prerequisites

- Docker installed and running
- (Optional) Access to Azure Container Registry for pulling images

## Option 1: Run from Azure Container Registry (Recommended)

Pull and run the latest production image:

```bash
# Pull the image
docker pull acrmimir.azurecr.io/mimir:latest

# Run with persistent storage
docker run -d \
  --name mimir \
  -p 8000:8000 \
  -v $(pwd)/mimir-data:/app/data \
  -e MIMIR_USER=admin \
  -e MIMIR_EMAIL=admin@localhost \
  acrmimir.azurecr.io/mimir:latest

# View logs
docker logs -f mimir

# Access the UI at http://localhost:8000
```

## Option 2: Build and Run Locally

Build from source and run:

```bash
# Build the image
docker build -t mimir:local .

# Run with persistent storage
docker run -d \
  --name mimir \
  -p 8000:8000 \
  -v $(pwd)/mimir-data:/app/data \
  -e MIMIR_USER=admin \
  -e MIMIR_EMAIL=admin@localhost \
  mimir:local

# View logs
docker logs -f mimir
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MIMIR_USER` | `admin` | Username for the default superuser |
| `MIMIR_EMAIL` | `admin@localhost` | Email for the default superuser |
| `MIMIR_DB_PATH` | `/app/data/mimir.db` | Database file path |
| `DJANGO_DEBUG` | `True` | Enable/disable Django debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,0.0.0.0` | Allowed hosts for Django |

## First-Time Setup

On first run, the container will:
1. ✅ Create the database at `/app/data/mimir.db`
2. ✅ Run all Django migrations
3. ✅ Create a superuser with username `MIMIR_USER`
4. ✅ Import default FeatureFactory playbook (17 objects)
5. ✅ Start Django GUI (port 8000) and MCP server

**Default credentials:**
- Username: Value of `MIMIR_USER` (default: `admin`)
- Password: `changeme` ⚠️ **Change this immediately after first login!**

## Container Services

The container runs two services via supervisor:

1. **Django GUI** (port 8000)
   - Gunicorn WSGI server with 2 workers
   - Web interface for playbook management
   - Accessible at http://localhost:8000

2. **MCP Server** (stdio)
   - Model Context Protocol server
   - Provides AI assistant access to playbooks
   - Configured for user specified in `MIMIR_USER`

## Volume Mount

The container uses a volume mount at `/app/data` for persistent storage:

```
./mimir-data/           # Your local directory
├── mimir.db           # SQLite database (persists between restarts)
├── app.log            # Application logs
└── tests.log          # Test logs
```

**Important:** Always mount a volume to preserve your data between container updates!

## Container Management

### View Logs
```bash
# Follow logs in real-time
docker logs -f mimir

# View last 100 lines
docker logs --tail 100 mimir
```

### Stop Container
```bash
docker stop mimir
```

### Start Stopped Container
```bash
docker start mimir
```

### Remove Container
```bash
docker stop mimir
docker rm mimir
```

### Update to Latest Version
```bash
# Stop and remove old container
docker stop mimir
docker rm mimir

# Pull latest image
docker pull acrmimir.azurecr.io/mimir:latest

# Run new container (same volume preserves data!)
docker run -d \
  --name mimir \
  -p 8000:8000 \
  -v $(pwd)/mimir-data:/app/data \
  -e MIMIR_USER=admin \
  -e MIMIR_EMAIL=admin@localhost \
  acrmimir.azurecr.io/mimir:latest
```

## Health Check

The container includes a health check that verifies Django is responding:

```bash
# Check container health
docker inspect mimir --format='{{.State.Health.Status}}'

# Should show: healthy
```

## Troubleshooting

### Container won't start
```bash
# Check logs for errors
docker logs mimir

# Verify volume mount exists
ls -la mimir-data/

# Check if port 8000 is already in use
lsof -i :8000
```

### Database issues
```bash
# Backup current database
cp mimir-data/mimir.db mimir-data/mimir.db.backup

# Start fresh (WARNING: deletes all data!)
rm -rf mimir-data/
mkdir mimir-data
docker restart mimir
```

### Can't access web UI
```bash
# Verify container is running
docker ps | grep mimir

# Check Django logs
docker logs mimir | grep gunicorn

# Test from inside container
docker exec mimir curl -s http://localhost:8000 | head
```

## Testing the Build

Use the included test script:

```bash
# Run automated build and test
./docker/test-build.sh

# This will:
# - Build the image
# - Start a test container on port 8001
# - Verify services are running
# - Show logs and health status
```

## Next Steps

1. **Access the UI**: http://localhost:8000
2. **Login**: Use your configured username and password `changeme`
3. **Change Password**: Go to Settings immediately
4. **Configure MCP**: Set up your IDE to connect to the MCP server
5. **Create Playbooks**: Start building your engineering playbooks

## Need Help?

- 📖 Full documentation: `docs/architecture/SAO.md`
- 🔧 Azure setup: `docs/AZURE_SETUP.md`
- 🐛 Issues: https://github.com/petelind/mimir/issues
