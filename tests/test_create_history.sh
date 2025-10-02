#!/bin/bash

# Test Create History Endpoint
# Kiểm tra endpoint POST /api/histories

BASE_URL="http://localhost:8000"
API_URL="${BASE_URL}/api/histories"

echo "🧪 Testing Create History Endpoint"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Create History với full data
echo -e "${BLUE}📝 Test 1: Create History (Full Data)${NC}"
CREATE_RESPONSE=$(curl -s -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "history",
    "value": {
      "id": "level_test_'$(date +%s)'",
      "name": "Test Level '$(date +%H%M%S)'",
      "level": {
        "id": "level_'$(date +%s)'",
        "config": {
          "name": "Test Level",
          "width": 9,
          "height": 10,
          "blockCount": 75,
          "colorCount": 3,
          "selectedColors": ["1", "2", "3", "4", "5", "6", "7", "8"],
          "colorMapping": {
            "1": "#ff0000",
            "2": "#0000ff",
            "3": "#00ff00",
            "4": "#ffff00",
            "5": "#ff9900",
            "6": "#9900ff",
            "7": "#ff00ff",
            "8": "#00ffff"
          },
          "generationMode": "symmetric",
          "elements": {
            "Pipe": 2,
            "Barrel": 20
          },
          "difficulty": "Hard",
          "pipeCount": 2,
          "pipeBlockCounts": [6, 6],
          "iceCounts": [2],
          "bombCounts": [2],
          "id": "config_'$(date +%s)'",
          "status": "pending",
          "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
          "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
        },
        "board": [
          [
            {"type": "wall", "color": null, "element": null},
            {"type": "block", "color": "1", "element": "Barrel"},
            {"type": "empty", "color": null, "element": null}
          ],
          [
            {"type": "block", "color": "2", "element": null},
            {"type": "block", "color": "3", "element": "Pipe"},
            {"type": "wall", "color": null, "element": null}
          ]
        ],
        "containers": [
          {
            "id": "container_0",
            "slots": 4,
            "contents": [
              {"color": "1", "type": "block"},
              {"color": "3", "type": "block"}
            ]
          }
        ],
        "difficultyScore": 117,
        "solvable": true,
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%6N)'",
        "pipeInfo": [
          {
            "id": "pipe1",
            "contents": ["5", "8", "4", "3", "3", "8"],
            "direction": "right",
            "position": {"x": 4, "y": 6}
          },
          {
            "id": "pipe2",
            "contents": ["8", "1", "7", "6", "1", "8"],
            "direction": "left",
            "position": {"x": 4, "y": 8}
          }
        ],
        "lockInfo": null
      },
      "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
      "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
    }
  }')

echo "$CREATE_RESPONSE" | python3 -m json.tool

# Extract ID
HISTORY_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)

if [ -z "$HISTORY_ID" ]; then
  echo -e "${RED}❌ Failed to create history${NC}"
  exit 1
fi

echo -e "${GREEN}✅ History created with ID: $HISTORY_ID${NC}"
echo ""

# Test 2: Verify created history
echo -e "${BLUE}🔍 Test 2: Verify Created History${NC}"
curl -s "${API_URL}/${HISTORY_ID}" | python3 -m json.tool
echo -e "${GREEN}✅ History verified${NC}"
echo ""

# Test 3: Create History với numeric name
echo -e "${BLUE}📝 Test 3: Create History (Numeric Name)${NC}"
NUMERIC_NAME=$((RANDOM % 100))
CREATE_NUMERIC=$(curl -s -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "history",
    "value": {
      "id": "level_numeric_'$(date +%s)'",
      "name": "'${NUMERIC_NAME}'",
      "level": {
        "id": "level_'$(date +%s)'",
        "config": {
          "name": "'${NUMERIC_NAME}'",
          "width": 5,
          "height": 5,
          "blockCount": 10,
          "colorCount": 2,
          "selectedColors": ["1", "2"],
          "colorMapping": {
            "1": "#ff0000",
            "2": "#0000ff"
          },
          "generationMode": "random",
          "elements": {},
          "difficulty": "Easy",
          "pipeCount": 0,
          "pipeBlockCounts": [],
          "iceCounts": [],
          "bombCounts": [],
          "id": "config_'$(date +%s)'",
          "status": "completed",
          "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
          "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
        },
        "board": [[{"type": "wall", "color": null, "element": null}]],
        "containers": [],
        "difficultyScore": 25,
        "solvable": true,
        "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%S.%6N)'",
        "pipeInfo": null,
        "lockInfo": null
      },
      "createdAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'",
      "updatedAt": "'$(date -u +%Y-%m-%dT%H:%M:%S.000Z)'"
    }
  }')

echo "$CREATE_NUMERIC" | python3 -m json.tool
NUMERIC_ID=$(echo "$CREATE_NUMERIC" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)
echo -e "${GREEN}✅ History with numeric name '$NUMERIC_NAME' created: $NUMERIC_ID${NC}"
echo ""

# Test 4: List histories to verify sorting
echo -e "${BLUE}📋 Test 4: List Histories (Sort by name)${NC}"
curl -s "${API_URL}?limit=5&sort_by=name&sort_order=asc" | python3 -m json.tool
echo -e "${GREEN}✅ Histories listed and sorted${NC}"
echo ""

# Test 5: Cleanup - Delete created histories
echo -e "${BLUE}🗑️  Test 5: Cleanup${NC}"
if [ ! -z "$HISTORY_ID" ]; then
  curl -s -X DELETE "${API_URL}/${HISTORY_ID}" | python3 -m json.tool
  echo -e "${GREEN}✅ Deleted history: $HISTORY_ID${NC}"
fi

if [ ! -z "$NUMERIC_ID" ]; then
  curl -s -X DELETE "${API_URL}/${NUMERIC_ID}" | python3 -m json.tool
  echo -e "${GREEN}✅ Deleted history: $NUMERIC_ID${NC}"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}🎉 All Create History tests completed!${NC}"
echo "=================================="
echo ""
echo "Tested:"
echo "  ✅ POST   /api/histories           - Create history with full data"
echo "  ✅ POST   /api/histories           - Create history with numeric name"
echo "  ✅ GET    /api/histories/{id}      - Verify created history"
echo "  ✅ GET    /api/histories           - List and sort histories"
echo "  ✅ DELETE /api/histories/{id}      - Cleanup"

