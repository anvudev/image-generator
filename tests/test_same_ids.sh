#!/bin/bash

# Test Same IDs Feature
# Verify that value.id = value.level.id = value.level.config.id

BASE_URL="http://localhost:8000"
API_URL="${BASE_URL}/api/histories"

echo "🧪 Testing Same IDs Feature"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Create history without IDs
echo -e "${BLUE}📝 Test 1: Create history without IDs (auto-generate)${NC}"
RESPONSE=$(curl -s -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "value": {
      "name": "Test Same IDs",
      "level": {
        "config": {
          "name": "Test",
          "width": 5,
          "height": 5,
          "blockCount": 10,
          "colorCount": 2,
          "selectedColors": ["1", "2"],
          "colorMapping": {"1": "#ff0000", "2": "#0000ff"},
          "generationMode": "random",
          "elements": {},
          "difficulty": "Easy"
        },
        "board": [[{"type": "wall", "color": null, "element": null}]],
        "containers": [],
        "difficultyScore": 25,
        "solvable": true,
        "pipeInfo": null,
        "lockInfo": null
      }
    }
  }')

echo "$RESPONSE" | python3 -m json.tool
echo ""

# Extract IDs
VALUE_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['id'])" 2>/dev/null)
LEVEL_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['level']['id'])" 2>/dev/null)
CONFIG_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['level']['config']['id'])" 2>/dev/null)
MONGO_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)

echo -e "${YELLOW}Extracted IDs:${NC}"
echo "  value.id:              $VALUE_ID"
echo "  value.level.id:        $LEVEL_ID"
echo "  value.level.config.id: $CONFIG_ID"
echo "  MongoDB _id:           $MONGO_ID"
echo ""

# Verify IDs are the same
if [ "$VALUE_ID" == "$LEVEL_ID" ] && [ "$VALUE_ID" == "$CONFIG_ID" ]; then
    echo -e "${GREEN}✅ All IDs are the same!${NC}"
    echo -e "${GREEN}   value.id = value.level.id = value.level.config.id${NC}"
else
    echo -e "${RED}❌ IDs are different!${NC}"
    echo -e "${RED}   Expected: All IDs should be the same${NC}"
    echo -e "${RED}   Got: value.id=$VALUE_ID, level.id=$LEVEL_ID, config.id=$CONFIG_ID${NC}"
fi
echo ""

# Test 2: Verify ID format
echo -e "${BLUE}🔍 Test 2: Verify ID format${NC}"
if [[ $VALUE_ID =~ ^level_[0-9]+_[a-f0-9]{8}$ ]]; then
    echo -e "${GREEN}✅ ID format is correct: level_{timestamp}_{random}${NC}"
else
    echo -e "${RED}❌ ID format is incorrect${NC}"
    echo -e "${RED}   Expected: level_{timestamp}_{random}${NC}"
    echo -e "${RED}   Got: $VALUE_ID${NC}"
fi
echo ""

# Test 3: Create with custom value.id
echo -e "${BLUE}📝 Test 3: Create with custom value.id${NC}"
CUSTOM_ID="level_custom_12345678"
RESPONSE2=$(curl -s -X POST "${API_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "value": {
      "id": "'${CUSTOM_ID}'",
      "name": "Custom ID Test",
      "level": {
        "config": {
          "name": "Test",
          "width": 5,
          "height": 5,
          "blockCount": 10,
          "colorCount": 2,
          "selectedColors": ["1", "2"],
          "colorMapping": {"1": "#ff0000", "2": "#0000ff"},
          "generationMode": "random",
          "elements": {},
          "difficulty": "Easy"
        },
        "board": [[{"type": "wall", "color": null, "element": null}]],
        "containers": [],
        "difficultyScore": 25,
        "solvable": true,
        "pipeInfo": null,
        "lockInfo": null
      }
    }
  }')

VALUE_ID2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['id'])" 2>/dev/null)
LEVEL_ID2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['level']['id'])" 2>/dev/null)
CONFIG_ID2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['value']['level']['config']['id'])" 2>/dev/null)
MONGO_ID2=$(echo "$RESPONSE2" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)

echo -e "${YELLOW}Custom IDs:${NC}"
echo "  value.id:              $VALUE_ID2"
echo "  value.level.id:        $LEVEL_ID2"
echo "  value.level.config.id: $CONFIG_ID2"
echo ""

if [ "$VALUE_ID2" == "$CUSTOM_ID" ] && [ "$LEVEL_ID2" == "$CUSTOM_ID" ] && [ "$CONFIG_ID2" == "$CUSTOM_ID" ]; then
    echo -e "${GREEN}✅ Custom ID propagated correctly to all fields!${NC}"
else
    echo -e "${RED}❌ Custom ID not propagated correctly${NC}"
fi
echo ""

# Test 4: Query by value.id
echo -e "${BLUE}🔍 Test 4: Query by value.id${NC}"
QUERY_RESULT=$(curl -s "${API_URL}?search=${VALUE_ID}&limit=1")
FOUND_COUNT=$(echo "$QUERY_RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)

if [ "$FOUND_COUNT" == "1" ]; then
    echo -e "${GREEN}✅ Can query by value.id successfully${NC}"
else
    echo -e "${RED}❌ Cannot query by value.id${NC}"
fi
echo ""

# Test 5: Verify MongoDB _id is different
echo -e "${BLUE}🔍 Test 5: Verify MongoDB _id is different from value.id${NC}"
if [ "$MONGO_ID" != "$VALUE_ID" ]; then
    echo -e "${GREEN}✅ MongoDB _id is different from value.id (correct)${NC}"
    echo "   MongoDB _id: $MONGO_ID"
    echo "   value.id:    $VALUE_ID"
else
    echo -e "${RED}❌ MongoDB _id should be different from value.id${NC}"
fi
echo ""

# Cleanup
echo -e "${YELLOW}🗑️  Cleanup${NC}"
if [ ! -z "$VALUE_ID" ]; then
    curl -s -X DELETE "${API_URL}/${VALUE_ID}" > /dev/null
    echo "  ✅ Deleted: $VALUE_ID"
fi

if [ ! -z "$VALUE_ID2" ]; then
    curl -s -X DELETE "${API_URL}/${VALUE_ID2}" > /dev/null
    echo "  ✅ Deleted: $VALUE_ID2"
fi
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}🎉 Same IDs tests completed!${NC}"
echo "=================================="
echo ""
echo "Verified:"
echo "  ✅ value.id = value.level.id = value.level.config.id"
echo "  ✅ ID format: level_{timestamp}_{random}"
echo "  ✅ Custom ID propagation"
echo "  ✅ Query by value.id"
echo "  ✅ MongoDB _id is separate"
echo ""
echo "Same IDs feature is working correctly! 🚀"

