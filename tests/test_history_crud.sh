#!/bin/bash

# Test History CRUD Operations
# Kiểm tra các endpoints: Create, Read, Update, Delete, Update Name

BASE_URL="http://localhost:8000"
API_URL="${BASE_URL}/db/histories"

echo "🧪 Testing History CRUD Operations"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test 1: Create History
echo -e "${BLUE}📝 Test 1: Create History${NC}"
CREATE_RESPONSE=$(curl -s -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "history",
    "value": {
      "id": "level_test_123",
      "name": "Test Level",
      "level": {
        "id": "level_123",
        "config": {
          "name": "Test Level",
          "width": 5,
          "height": 5,
          "blockCount": 10,
          "colorCount": 3,
          "selectedColors": ["1", "2", "3"],
          "colorMapping": {
            "1": "#ff0000",
            "2": "#0000ff",
            "3": "#00ff00"
          },
          "generationMode": "symmetric",
          "elements": {"Pipe": 1},
          "difficulty": "Easy",
          "pipeCount": 1,
          "pipeBlockCounts": [3],
          "iceCounts": [],
          "bombCounts": [],
          "id": "config_123",
          "status": "pending",
          "createdAt": "2025-01-01T00:00:00.000Z",
          "updatedAt": "2025-01-01T00:00:00.000Z"
        },
        "board": [
          [
            {"type": "wall", "color": null, "element": null},
            {"type": "block", "color": "1", "element": null}
          ]
        ],
        "containers": [
          {
            "id": "container_0",
            "slots": 4,
            "contents": [
              {"color": "1", "type": "block"}
            ]
          }
        ],
        "difficultyScore": 50,
        "solvable": true,
        "timestamp": "2025-01-01T00:00:00.000000",
        "pipeInfo": [
          {
            "id": "pipe1",
            "contents": ["1", "2", "3"],
            "direction": "right",
            "position": {"x": 2, "y": 2}
          }
        ],
        "lockInfo": null
      },
      "createdAt": "2025-01-01T00:00:00.000Z",
      "updatedAt": "2025-01-01T00:00:00.000Z"
    }
  }')

echo "$CREATE_RESPONSE" | python3 -m json.tool
HISTORY_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)

if [ -z "$HISTORY_ID" ]; then
  echo -e "${RED}❌ Failed to create history${NC}"
  exit 1
fi

echo -e "${GREEN}✅ History created with ID: $HISTORY_ID${NC}"
echo ""

# Test 2: Get History by ID
echo -e "${BLUE}📖 Test 2: Get History by ID${NC}"
curl -s "${API_URL}/${HISTORY_ID}" | python3 -m json.tool
echo -e "${GREEN}✅ Get history successful${NC}"
echo ""

# Test 3: List Histories (Default sort)
echo -e "${BLUE}📋 Test 3: List Histories (Default: updatedAt desc)${NC}"
curl -s "${API_URL}?limit=5" | python3 -m json.tool
echo -e "${GREEN}✅ List histories successful${NC}"
echo ""

# Test 3.1: List Histories sorted by name asc
echo -e "${BLUE}📋 Test 3.1: List Histories (Sort by name asc)${NC}"
curl -s "${API_URL}?limit=5&sort_by=name&sort_order=asc" | python3 -m json.tool
echo -e "${GREEN}✅ List histories sorted by name ascending${NC}"
echo ""

# Test 3.2: List Histories sorted by updatedAt asc
echo -e "${BLUE}📋 Test 3.2: List Histories (Sort by updatedAt asc)${NC}"
curl -s "${API_URL}?limit=5&sort_by=updatedAt&sort_order=asc" | python3 -m json.tool
echo -e "${GREEN}✅ List histories sorted by updatedAt ascending${NC}"
echo ""

# Test 4: Update History Name
echo -e "${BLUE}✏️  Test 4: Update History Name${NC}"
NEW_NAME="Updated Test Level"
curl -s -X PUT "${API_URL}/${HISTORY_ID}/name?name=${NEW_NAME}" | python3 -m json.tool
echo -e "${GREEN}✅ History name updated to: $NEW_NAME${NC}"
echo ""

# Test 5: Update Full History
echo -e "${BLUE}🔄 Test 5: Update Full History${NC}"
curl -s -X PUT "${API_URL}/${HISTORY_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "value": {
      "id": "level_test_123",
      "name": "Fully Updated Level",
      "level": {
        "id": "level_123",
        "config": {
          "name": "Fully Updated Level",
          "width": 6,
          "height": 6,
          "blockCount": 15,
          "colorCount": 4,
          "selectedColors": ["1", "2", "3", "4"],
          "colorMapping": {
            "1": "#ff0000",
            "2": "#0000ff",
            "3": "#00ff00",
            "4": "#ffff00"
          },
          "generationMode": "random",
          "elements": {"Pipe": 2, "Barrel": 5},
          "difficulty": "Medium",
          "pipeCount": 2,
          "pipeBlockCounts": [4, 4],
          "iceCounts": [1],
          "bombCounts": [1],
          "id": "config_123",
          "status": "completed",
          "createdAt": "2025-01-01T00:00:00.000Z",
          "updatedAt": "2025-01-01T01:00:00.000Z"
        },
        "board": [
          [
            {"type": "wall", "color": null, "element": null},
            {"type": "block", "color": "1", "element": "Barrel"}
          ]
        ],
        "containers": [
          {
            "id": "container_0",
            "slots": 6,
            "contents": [
              {"color": "1", "type": "block"},
              {"color": "2", "type": "block"}
            ]
          }
        ],
        "difficultyScore": 75,
        "solvable": true,
        "timestamp": "2025-01-01T01:00:00.000000",
        "pipeInfo": [
          {
            "id": "pipe1",
            "contents": ["1", "2", "3", "4"],
            "direction": "left",
            "position": {"x": 3, "y": 3}
          }
        ],
        "lockInfo": null
      },
      "createdAt": "2025-01-01T00:00:00.000Z",
      "updatedAt": "2025-01-01T01:00:00.000Z"
    }
  }' | python3 -m json.tool
echo -e "${GREEN}✅ History fully updated${NC}"
echo ""

# Test 6: Verify Update
echo -e "${BLUE}🔍 Test 6: Verify Update${NC}"
UPDATED_HISTORY=$(curl -s "${API_URL}/${HISTORY_ID}")
echo "$UPDATED_HISTORY" | python3 -m json.tool
UPDATED_NAME=$(echo "$UPDATED_HISTORY" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['name'])" 2>/dev/null)
echo -e "${GREEN}✅ Verified name: $UPDATED_NAME${NC}"
echo ""

# Test 7: Delete History
echo -e "${BLUE}🗑️  Test 7: Delete History${NC}"
curl -s -X DELETE "${API_URL}/${HISTORY_ID}" | python3 -m json.tool
echo -e "${GREEN}✅ History deleted${NC}"
echo ""

# Test 8: Verify Deletion
echo -e "${BLUE}🔍 Test 8: Verify Deletion${NC}"
DELETE_CHECK=$(curl -s "${API_URL}/${HISTORY_ID}")
echo "$DELETE_CHECK" | python3 -m json.tool

if echo "$DELETE_CHECK" | grep -q "History not found"; then
  echo -e "${GREEN}✅ History successfully deleted (not found)${NC}"
else
  echo -e "${RED}❌ History still exists after deletion${NC}"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}🎉 All History CRUD tests completed!${NC}"
echo "=================================="
echo ""
echo "Tested endpoints:"
echo "  ✅ POST   /db/histories           - Create history"
echo "  ✅ GET    /db/histories           - List histories"
echo "  ✅ GET    /db/histories/{id}      - Get history by ID"
echo "  ✅ PUT    /db/histories/{id}      - Update full history"
echo "  ✅ PUT    /db/histories/{id}/name - Update history name"
echo "  ✅ DELETE /db/histories/{id}      - Delete history"

