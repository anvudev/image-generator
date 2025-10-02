#!/bin/bash

echo "🔍 Docker Network Debugging Script"
echo "===================================="
echo ""

# 1. Check all running containers
echo "📦 1. All Running Containers:"
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Networks}}\t{{.Status}}"
echo ""

# 2. Check cloudflared network
echo "🌐 2. Cloudflared Network Details:"
docker network inspect cloudflared --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}'
echo ""

# 3. Check if mirai-mongodb exists
echo "🗄️  3. MongoDB Container Check:"
docker ps -a --filter "name=mongo" --format "table {{.ID}}\t{{.Names}}\t{{.Networks}}\t{{.Status}}"
echo ""

# 4. Check API container network
echo "🔌 4. API Container Network:"
API_CONTAINER=$(docker ps --filter "name=mirai-pixel-api" --format "{{.ID}}")
if [ ! -z "$API_CONTAINER" ]; then
    docker inspect $API_CONTAINER --format '{{range $net, $conf := .NetworkSettings.Networks}}Network: {{$net}}, IP: {{$conf.IPAddress}}{{"\n"}}{{end}}'
else
    echo "❌ mirai-pixel-api container not found"
fi
echo ""

# 5. Test DNS resolution from API container
echo "🧪 5. DNS Resolution Test (from API container):"
if [ ! -z "$API_CONTAINER" ]; then
    echo "Testing: mirai-mongodb"
    docker exec $API_CONTAINER getent hosts mirai-mongodb 2>&1 || echo "❌ Cannot resolve mirai-mongodb"
    echo ""
    echo "Testing: mongodb"
    docker exec $API_CONTAINER getent hosts mongodb 2>&1 || echo "❌ Cannot resolve mongodb"
else
    echo "❌ Cannot test - API container not running"
fi
echo ""

# 6. Check MongoDB container name
echo "🔍 6. Find MongoDB Container:"
MONGO_CONTAINER=$(docker ps --filter "name=mongo" --format "{{.Names}}")
if [ ! -z "$MONGO_CONTAINER" ]; then
    echo "✅ Found: $MONGO_CONTAINER"
    echo "Network:"
    docker inspect $MONGO_CONTAINER --format '{{range $net, $conf := .NetworkSettings.Networks}}  - {{$net}}: {{$conf.IPAddress}}{{"\n"}}{{end}}'
else
    echo "❌ No MongoDB container found"
fi
echo ""

# 7. Suggest fix
echo "💡 Suggested Fixes:"
echo "==================="
if [ ! -z "$MONGO_CONTAINER" ]; then
    echo "1. Update docker-compose.yml:"
    echo "   MONGODB_URI=mongodb://$MONGO_CONTAINER:27017/"
    echo ""
    echo "2. Or create network alias:"
    echo "   docker network connect cloudflared $MONGO_CONTAINER --alias mirai-mongodb"
else
    echo "❌ MongoDB container not found. Please start it first."
fi
echo ""

echo "🎯 Quick Fix Command:"
if [ ! -z "$MONGO_CONTAINER" ] && [ "$MONGO_CONTAINER" != "mirai-mongodb" ]; then
    echo "docker network connect cloudflared $MONGO_CONTAINER --alias mirai-mongodb"
fi

