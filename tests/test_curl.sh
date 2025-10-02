#!/bin/bash

echo "🚀 Testing Palette Override Feature with curl"
echo "=================================================="

# Test 1: Get palette info
echo "🧪 Test 1: Get palette info"
curl -s http://localhost:8000/palette | jq '.'
echo ""

# Test 2: Health check
echo "🧪 Test 2: Health check"
curl -s http://localhost:8000/healthz | jq '.'
echo ""

# Test 3: Create a simple test image
echo "🧪 Test 3: Creating test image..."
# Tạo một ảnh test đơn giản bằng ImageMagick (nếu có)
if command -v convert &> /dev/null; then
    convert -size 10x10 xc:red test_red.png
    echo "✅ Created test_red.png"
    
    # Test với palette override
    echo "🧪 Test 4: Convert with palette override (chỉ dùng màu đỏ và xanh lá)"
    curl -X POST \
      -F "file=@test_red.png" \
      -F "cols=5" \
      -F "rows=5" \
      -F "palette_override=1,3" \
      http://localhost:8000/convert \
      | jq '.meta.palette'
    
    echo ""
    echo "🧪 Test 5: Convert with JSON array format"
    curl -X POST \
      -F "file=@test_red.png" \
      -F "cols=5" \
      -F "rows=5" \
      -F "palette_override=[1,2,4]" \
      http://localhost:8000/convert \
      | jq '.meta.palette'
    
    echo ""
    echo "🧪 Test 6: Test error case - invalid palette index"
    curl -X POST \
      -F "file=@test_red.png" \
      -F "cols=5" \
      -F "rows=5" \
      -F "palette_override=1,99" \
      http://localhost:8000/convert \
      | jq '.detail'
    
    # Cleanup
    rm -f test_red.png
else
    echo "❌ ImageMagick not found. Skipping image tests."
    echo "💡 Install with: sudo apt-get install imagemagick"
fi

echo ""
echo "=================================================="
echo "✨ Test completed!"
