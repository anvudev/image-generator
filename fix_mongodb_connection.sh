#!/bin/bash

echo "🔧 Fixing MongoDB Connection"
echo "============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Show current status
echo -e "${YELLOW}📊 Current Status:${NC}"
echo "MongoDB container: mongodb (172.21.0.7)"
echo "API container: mirai-pixel-api (172.21.0.3)"
echo "Network: cloudflared"
echo ""

# 2. Test current connection
echo -e "${YELLOW}🧪 Testing current connection...${NC}"
docker exec mirai-pixel-api wget -q -O- http://localhost:8000/api/histories?limit=1 2>&1 | head -5
echo ""

# 3. Update docker-compose.yml
echo -e "${YELLOW}📝 Updating docker-compose.yml...${NC}"
cat > docker-compose.yml << 'EOF'
services:
  # API Service
  pixel-api:
    build: .
    container_name: mirai-pixel-api
    restart: unless-stopped
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
      - MONGODB_DATABASE=Mirai_Puzzle
    networks:
      - cloudflared
    expose:
      - "8000"

networks:
  cloudflared:
    external: true
    name: cloudflared
EOF

echo -e "${GREEN}✅ docker-compose.yml updated${NC}"
echo ""

# 4. Recreate container
echo -e "${YELLOW}🔄 Recreating API container...${NC}"
docker compose up -d --force-recreate pixel-api

echo ""
echo -e "${YELLOW}⏳ Waiting for container to start...${NC}"
sleep 5

# 5. Check logs
echo ""
echo -e "${YELLOW}📋 Container logs:${NC}"
docker logs mirai-pixel-api --tail 10
echo ""

# 6. Test connection
echo -e "${YELLOW}🧪 Testing new connection...${NC}"
sleep 2

RESPONSE=$(curl -s http://localhost:8000/api/histories?limit=1)
if echo "$RESPONSE" | grep -q '"success": true'; then
    echo -e "${GREEN}✅ SUCCESS! MongoDB connection working!${NC}"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null | head -20
else
    echo -e "${RED}❌ Still failing. Response:${NC}"
    echo "$RESPONSE"
    echo ""
    echo -e "${YELLOW}💡 Try manual fix:${NC}"
    echo "docker restart mirai-pixel-api"
    echo "docker logs mirai-pixel-api"
fi

echo ""
echo "============================="
echo -e "${GREEN}🎉 Fix completed!${NC}"
echo "============================="

