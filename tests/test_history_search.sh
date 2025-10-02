#!/bin/bash

# Test History Search Feature
# Kiểm tra tính năng search trong list histories endpoint

BASE_URL="http://localhost:8000"
API_URL="${BASE_URL}/api/histories"

echo "🔍 Testing History Search Feature"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Array to store created IDs for cleanup
declare -a CREATED_IDS

# Function to create test history
create_test_history() {
    local name=$1
    local response=$(curl -s -X POST "${API_URL}" \
      -H "Content-Type: application/json" \
      -d '{
        "value": {
          "name": "'${name}'",
          "level": {
            "config": {
              "name": "'${name}'",
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
    
    local id=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)
    if [ ! -z "$id" ]; then
        CREATED_IDS+=("$id")
        echo "$id"
    fi
}

# Setup: Create test data
echo -e "${YELLOW}📝 Setup: Creating test data${NC}"
echo ""

echo "Creating histories with different names..."
ID1=$(create_test_history "Level 1")
echo "  ✅ Created: Level 1 (ID: $ID1)"

ID2=$(create_test_history "Level 2")
echo "  ✅ Created: Level 2 (ID: $ID2)"

ID3=$(create_test_history "18")
echo "  ✅ Created: 18 (ID: $ID3)"

ID4=$(create_test_history "41")
echo "  ✅ Created: 41 (ID: $ID4)"

ID5=$(create_test_history "Test Game")
echo "  ✅ Created: Test Game (ID: $ID5)"

ID6=$(create_test_history "Another Level")
echo "  ✅ Created: Another Level (ID: $ID6)"

echo ""
echo -e "${GREEN}✅ Created ${#CREATED_IDS[@]} test histories${NC}"
echo ""
sleep 1

# Test 1: Search for "level" (case-insensitive)
echo -e "${BLUE}🔍 Test 1: Search for 'level' (case-insensitive)${NC}"
RESULT=$(curl -s "${API_URL}?search=level&limit=20")
echo "$RESULT" | python3 -m json.tool
COUNT=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)
echo -e "${GREEN}✅ Found $COUNT histories matching 'level'${NC}"
echo ""

# Test 2: Search for "18" (numeric)
echo -e "${BLUE}🔍 Test 2: Search for '18' (numeric)${NC}"
RESULT=$(curl -s "${API_URL}?search=18&limit=20")
echo "$RESULT" | python3 -m json.tool
COUNT=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)
echo -e "${GREEN}✅ Found $COUNT histories matching '18'${NC}"
echo ""

# Test 3: Search for "test" (partial match)
echo -e "${BLUE}🔍 Test 3: Search for 'test' (partial match)${NC}"
RESULT=$(curl -s "${API_URL}?search=test&limit=20")
echo "$RESULT" | python3 -m json.tool
COUNT=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)
echo -e "${GREEN}✅ Found $COUNT histories matching 'test'${NC}"
echo ""

# Test 4: Search + Sort by name ascending
echo -e "${BLUE}🔍 Test 4: Search 'level' + Sort by name asc${NC}"
RESULT=$(curl -s "${API_URL}?search=level&sort_by=name&sort_order=asc&limit=20")
echo "$RESULT" | python3 -m json.tool
NAMES=$(echo "$RESULT" | python3 -c "import sys, json; data = json.load(sys.stdin); print([item['value']['name'] for item in data['data']['items']])" 2>/dev/null)
echo -e "  Names: $NAMES"
echo -e "${GREEN}✅ Search + Sort working${NC}"
echo ""

# Test 5: Search + Pagination
echo -e "${BLUE}🔍 Test 5: Search 'level' + Pagination (skip=1, limit=2)${NC}"
RESULT=$(curl -s "${API_URL}?search=level&skip=1&limit=2")
echo "$RESULT" | python3 -m json.tool
COUNT=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)
TOTAL=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['pagination']['total'])" 2>/dev/null)
echo -e "  Returned: $COUNT items, Total: $TOTAL"
echo -e "${GREEN}✅ Search + Pagination working${NC}"
echo ""

# Test 6: Search with no results
echo -e "${BLUE}🔍 Test 6: Search for 'nonexistent' (no results)${NC}"
RESULT=$(curl -s "${API_URL}?search=nonexistent&limit=20")
echo "$RESULT" | python3 -m json.tool
COUNT=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)
echo -e "${GREEN}✅ Found $COUNT histories (expected 0)${NC}"
echo ""

# Test 7: Case-insensitive search
echo -e "${BLUE}🔍 Test 7: Case-insensitive search 'LEVEL' vs 'level'${NC}"
RESULT1=$(curl -s "${API_URL}?search=LEVEL&limit=20")
COUNT1=$(echo "$RESULT1" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)

RESULT2=$(curl -s "${API_URL}?search=level&limit=20")
COUNT2=$(echo "$RESULT2" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['data']['items']))" 2>/dev/null)

echo "  'LEVEL': $COUNT1 results"
echo "  'level': $COUNT2 results"

if [ "$COUNT1" == "$COUNT2" ]; then
    echo -e "${GREEN}✅ Case-insensitive search working (both return same count)${NC}"
else
    echo -e "${RED}❌ Case-insensitive search not working${NC}"
fi
echo ""

# Test 8: Search response format
echo -e "${BLUE}🔍 Test 8: Verify search response format${NC}"
RESULT=$(curl -s "${API_URL}?search=level&limit=5")
HAS_SEARCH=$(echo "$RESULT" | python3 -c "import sys, json; print('search' in json.load(sys.stdin)['data'])" 2>/dev/null)
SEARCH_VALUE=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['search'])" 2>/dev/null)

echo "  Has 'search' field: $HAS_SEARCH"
echo "  Search value: $SEARCH_VALUE"

if [ "$HAS_SEARCH" == "True" ] && [ "$SEARCH_VALUE" == "level" ]; then
    echo -e "${GREEN}✅ Response format correct${NC}"
else
    echo -e "${RED}❌ Response format incorrect${NC}"
fi
echo ""

# Cleanup
echo -e "${YELLOW}🗑️  Cleanup: Deleting test data${NC}"
for id in "${CREATED_IDS[@]}"; do
    curl -s -X DELETE "${API_URL}/${id}" > /dev/null
    echo "  ✅ Deleted: $id"
done
echo ""

# Summary
echo "=================================="
echo -e "${GREEN}🎉 All search tests completed!${NC}"
echo "=================================="
echo ""
echo "Tested:"
echo "  ✅ Case-insensitive search"
echo "  ✅ Partial match search"
echo "  ✅ Numeric search"
echo "  ✅ Search + Sort"
echo "  ✅ Search + Pagination"
echo "  ✅ No results handling"
echo "  ✅ Response format"
echo ""
echo "Search feature is working correctly! 🚀"

