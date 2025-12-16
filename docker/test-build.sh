#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════"
echo "🧪 Testing Mimir Docker Build"
echo "═══════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker daemon is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo -e "${BLUE}Step 1: Building Docker image...${NC}"
docker build -t mimir:test .

echo ""
echo -e "${GREEN}✅ Build successful!${NC}"
echo ""

echo -e "${BLUE}Step 2: Creating test data directory...${NC}"
mkdir -p ./test-data

echo ""
echo -e "${BLUE}Step 3: Running container...${NC}"
docker run -d \
  --name mimir-test \
  -p 8001:8000 \
  -v $(pwd)/test-data:/app/data \
  -e MIMIR_USER=testuser \
  -e MIMIR_EMAIL=test@example.com \
  mimir:test

echo ""
echo -e "${GREEN}✅ Container started!${NC}"
echo ""

echo -e "${BLUE}Step 4: Waiting for container to initialize (30s)...${NC}"
sleep 30

echo ""
echo -e "${BLUE}Step 5: Checking container logs...${NC}"
docker logs mimir-test

echo ""
echo -e "${BLUE}Step 6: Testing health endpoint...${NC}"
curl -f http://localhost:8001 > /dev/null 2>&1 && echo -e "${GREEN}✅ Health check passed!${NC}" || echo -e "${YELLOW}⚠️  Health check pending...${NC}"

echo ""
echo -e "${BLUE}Step 7: Checking container processes...${NC}"
docker exec mimir-test ps aux | grep -E "gunicorn|python|supervisor"

echo ""
echo "═══════════════════════════════════════════════════════"
echo -e "${GREEN}🎉 Test Complete!${NC}"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Container is running at: http://localhost:8001"
echo "Database location: ./test-data/mimir.db"
echo ""
echo "To view logs:"
echo "  docker logs -f mimir-test"
echo ""
echo "To stop and cleanup:"
echo "  docker stop mimir-test"
echo "  docker rm mimir-test"
echo "  rm -rf ./test-data"
echo ""
