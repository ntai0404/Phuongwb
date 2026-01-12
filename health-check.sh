#!/bin/bash
# Health check script for all services

echo "=== Phuong Web - Service Health Check ==="
echo ""

check_service() {
    local name=$1
    local url=$2
    
    echo -n "Checking $name... "
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo "✓ OK"
        return 0
    else
        echo "✗ FAILED"
        return 1
    fi
}

# Check all services
check_service "API Gateway" "http://localhost:8080/health"
check_service "Storage Service" "http://localhost:5000/health"
check_service "AI Summarizer" "http://localhost:8000/health"
check_service "Frontend" "http://localhost:3000"

echo ""
echo "=== Additional Services ==="
check_service "RabbitMQ Management" "http://localhost:15672"

echo ""
echo "=== Database Connections ==="
# Check PostgreSQL
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "PostgreSQL... ✓ OK"
else
    echo "PostgreSQL... ✗ FAILED"
fi

# Check Redis
if redis-cli -h localhost -p 6379 ping > /dev/null 2>&1; then
    echo "Redis... ✓ OK"
else
    echo "Redis... ✗ FAILED"
fi

echo ""
echo "Health check completed!"
