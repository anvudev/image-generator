#!/bin/bash

echo "🧪 Testing Mirai Puzzle API v2.0"
echo "======================================================"

BASE_URL="http://localhost:8000"

# Test 1: Root endpoint
echo "📍 Test 1: Root endpoint"
curl -s $BASE_URL | python3 -m json.tool
echo ""

# Test 2: Health check
echo "📍 Test 2: Health check"
curl -s $BASE_URL/healthz | python3 -m json.tool
echo ""

# Test 3: Get palette
echo "📍 Test 3: Get palette"
curl -s $BASE_URL/image/palette | python3 -m json.tool
echo ""

# Test 4: Create image in database
echo "📍 Test 4: Create image in database"
IMAGE_RESPONSE=$(curl -s -X POST $BASE_URL/db/images \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_image.png",
    "matrix": [[1,2,12],[3,4,12]],
    "palette": {"1":"#ff0000","2":"#0000ff","3":"#00ff00","4":"#ffff00","12":"#ffffff"},
    "cols": 3,
    "rows": 2,
    "metadata": {"test": true}
  }')

echo "$IMAGE_RESPONSE" | python3 -m json.tool

# Extract image ID
IMAGE_ID=$(echo "$IMAGE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['_id'])" 2>/dev/null)

if [ -n "$IMAGE_ID" ]; then
    echo ""
    echo "✅ Created image with ID: $IMAGE_ID"
    
    # Test 5: Get image by ID
    echo ""
    echo "📍 Test 5: Get image by ID"
    curl -s $BASE_URL/db/images/$IMAGE_ID | python3 -m json.tool
    
    # Test 6: Update image
    echo ""
    echo "📍 Test 6: Update image"
    curl -s -X PUT $BASE_URL/db/images/$IMAGE_ID \
      -H "Content-Type: application/json" \
      -d '{"name": "updated_test_image.png"}' | python3 -m json.tool
    
    # Test 7: List images
    echo ""
    echo "📍 Test 7: List images"
    curl -s "$BASE_URL/db/images?skip=0&limit=5" | python3 -m json.tool
    
    # Test 8: Delete image
    echo ""
    echo "📍 Test 8: Delete image"
    curl -s -X DELETE $BASE_URL/db/images/$IMAGE_ID | python3 -m json.tool
else
    echo "❌ Failed to create image"
fi

echo ""
echo "======================================================"
echo "✨ Test completed!"

