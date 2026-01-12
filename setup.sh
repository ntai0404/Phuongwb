#!/bin/bash

# Initial Setup Script for New Architecture
# This script helps set up the system for first-time use

set -e

echo "========================================="
echo "Phuong Web - Initial Setup"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker compose is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose are installed${NC}"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env file created${NC}"
    else
        echo -e "${YELLOW}! .env.example not found, creating minimal .env${NC}"
        cat > .env << EOF
DB_HOST=postgres
DB_PORT=5432
DB_NAME=newsdb
DB_USER=postgres
DB_PASSWORD=postgres

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

QDRANT_HOST=qdrant
QDRANT_PORT=6333

RECOMMENDATION_URL=http://recommendation-service:8001
SECRET_KEY=$(openssl rand -hex 32)
EOF
        echo -e "${GREEN}✓ Minimal .env file created${NC}"
    fi
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi
echo ""

# Start services
echo -e "${YELLOW}Starting services...${NC}"
echo "This may take several minutes on first run (downloading images and models)"
echo ""

docker compose up -d

echo ""
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Check service health
echo ""
echo "Checking service health..."
echo ""

# Check Core API
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Core API Service is healthy${NC}"
else
    echo -e "${RED}✗ Core API Service is not responding${NC}"
fi

# Check Recommendation Service
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Recommendation Service is healthy${NC}"
else
    echo -e "${YELLOW}! Recommendation Service is still starting (this can take a few minutes)${NC}"
fi

# Check Summary Service
if curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Summary Service is healthy${NC}"
else
    echo -e "${YELLOW}! Summary Service is still starting (this can take a few minutes)${NC}"
fi

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Services are starting up. Please wait a few minutes for all services to be fully ready."
echo ""
echo -e "${GREEN}Access Points:${NC}"
echo "  - Frontend:              http://localhost:3000"
echo "  - Core API:              http://localhost:8080"
echo "  - Recommendation:        http://localhost:8001"
echo "  - Summary:               http://localhost:8002"
echo "  - RabbitMQ Management:   http://localhost:15672 (guest/guest)"
echo "  - Qdrant Dashboard:      http://localhost:6333/dashboard"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "  1. Create an admin user:"
echo "     curl -X POST http://localhost:8080/api/v1/auth/register \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"username\":\"admin\",\"email\":\"admin@example.com\",\"password\":\"yourpassword\"}'"
echo ""
echo "  2. Promote user to admin (manual database update required on first user):"
echo "     docker exec -it phuong-postgres psql -U postgres -d newsdb -c \"UPDATE users SET role='admin' WHERE username='admin';\""
echo ""
echo "  3. Login to get access token:"
echo "     curl -X POST http://localhost:8080/api/v1/auth/login \\"
echo "       -H 'Content-Type: application/json' \\"
echo "       -d '{\"username\":\"admin\",\"password\":\"yourpassword\"}'"
echo ""
echo "  4. Add RSS sources and trigger crawl (see API_EXAMPLES.md)"
echo ""
echo -e "${GREEN}View logs:${NC}"
echo "  docker compose logs -f"
echo ""
echo "For detailed documentation, see:"
echo "  - ARCHITECTURE.md - System architecture"
echo "  - API_EXAMPLES.md - API usage examples"
echo "  - MIGRATION.md - Migration guide"
echo ""
