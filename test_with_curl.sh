#!/bin/bash

echo "🚀 Testing: Actual Colors Only Feature"
echo "======================================================"

# Test 1: Kiểm tra palette endpoint
echo "🧪 Test 1: Palette endpoint"
echo "GET /palette"
curl -s http://localhost:8000/palette | python3 -m json.tool
echo ""

# Test 2: Tạo ảnh test đơn giản bằng ImageMagick
echo "🧪 Test 2: Tạo ảnh test và kiểm tra actual colors"

if command -v convert &> /dev/null; then
    echo "📸 Tạo ảnh test với 2 màu: đỏ và trắng..."
    
    # Tạo ảnh 4x4 với pattern đỏ-trắng
    convert -size 4x4 xc:red red_4x4.png
    convert -size 2x2 xc:white white_2x2.png
    convert red_4x4.png white_2x2.png -gravity center -composite test_red_white.png
    
    echo "✅ Đã tạo test_red_white.png"
    
    echo ""
    echo "🔍 Test convert API với ảnh test:"
    echo "POST /convert với test_red_white.png"
    
    # Test convert
    response=$(curl -s -X POST \
      -F "file=@test_red_white.png" \
      -F "cols=4" \
      -F "rows=4" \
      http://localhost:8000/convert)
    
    echo "📊 Response:"
    echo "$response" | python3 -m json.tool
    
    # Parse và kiểm tra palette
    echo ""
    echo "🎨 Phân tích palette trong response:"
    palette_count=$(echo "$response" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    palette = data['meta']['palette']
    print(f'Số màu trong palette: {len(palette)}')
    for idx, color in palette.items():
        print(f'  {idx}: {color}')
except Exception as e:
    print(f'Error parsing: {e}')
")
    echo "$palette_count"
    
    # Cleanup
    rm -f red_4x4.png white_2x2.png test_red_white.png
    
else
    echo "❌ ImageMagick not found. Tạo ảnh test thủ công..."
    echo ""
    echo "💡 Để test thủ công:"
    echo "1. Tạo một ảnh đơn giản với 2-3 màu"
    echo "2. Chạy lệnh:"
    echo "   curl -X POST \\"
    echo "     -F \"file=@your_image.png\" \\"
    echo "     -F \"cols=10\" \\"
    echo "     -F \"rows=10\" \\"
    echo "     http://localhost:8000/convert | python3 -m json.tool"
    echo ""
    echo "3. Kiểm tra xem palette trong response có chỉ chứa màu thực sự có trong ảnh không"
fi

echo ""
echo "======================================================"
echo "✨ Test completed!"
echo ""
echo "🎯 Mục tiêu test:"
echo "   - API chỉ trả về các màu thực sự có trong ảnh"
echo "   - Không trả về toàn bộ 12 màu mặc định"
echo "   - Palette trong response khớp với matrix indices"
