"""
Test script để kiểm tra tính năng chỉ trả về màu thực sự có trong ảnh
"""
import requests
from PIL import Image
import io
import base64

def create_simple_test_image():
    """Tạo một ảnh test đơn giản với 3 màu: đỏ, xanh lá, trắng"""
    # Tạo ảnh 6x6 pixels
    img = Image.new('RGB', (6, 6), 'white')
    pixels = img.load()
    
    # Tô một số pixel màu đỏ
    for x in range(2):
        for y in range(2):
            pixels[x, y] = (255, 0, 0)  # Đỏ
    
    # Tô một số pixel màu xanh lá
    for x in range(2, 4):
        for y in range(2, 4):
            pixels[x, y] = (0, 255, 0)  # Xanh lá
    
    # Phần còn lại để trắng (đã set sẵn)
    
    # Lưu vào BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes.getvalue()

def test_actual_colors_only():
    """Test xem API có chỉ trả về màu thực sự có trong ảnh không"""
    print("🧪 Testing: Chỉ trả về màu có trong ảnh")
    print("=" * 50)
    
    # Tạo ảnh test
    print("📸 Tạo ảnh test với 3 màu: đỏ, xanh lá, trắng...")
    image_data = create_simple_test_image()
    
    # Gửi request
    try:
        files = {'file': ('test.png', image_data, 'image/png')}
        data = {
            'cols': 6,
            'rows': 6
        }
        
        response = requests.post('http://localhost:8000/convert', files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API hoạt động thành công!")
            print(f"📊 Kích thước: {result['meta']['cols']}x{result['meta']['rows']}")
            print(f"🎨 Số màu trong palette trả về: {len(result['meta']['palette'])}")
            
            print("\n🎨 Các màu được trả về:")
            palette = result['meta']['palette']
            
            # Mapping tên màu
            color_names = {
                "1": "Đỏ", "2": "Xanh dương", "3": "Xanh lá", "4": "Vàng",
                "5": "Cam", "6": "Tím", "7": "Hồng", "8": "Cyan",
                "9": "Xanh nhạt", "10": "Nâu", "11": "Xám", "12": "Trắng"
            }
            
            for idx, color in palette.items():
                name = color_names.get(str(idx), "Unknown")
                print(f"   {idx}: {color} ({name})")
            
            # Kiểm tra matrix
            matrix = result['matrix']
            unique_indices = set()
            for row in matrix:
                for idx in row:
                    unique_indices.add(idx)
            
            print(f"\n📋 Các chỉ số màu trong matrix: {sorted(unique_indices)}")
            print(f"📋 Các chỉ số màu trong palette: {sorted([int(k) for k in palette.keys()])}")
            
            # Kiểm tra xem có khớp không
            matrix_indices = set(unique_indices)
            palette_indices = set(int(k) for k in palette.keys())
            
            if matrix_indices == palette_indices:
                print("✅ PASS: Palette chỉ chứa màu thực sự có trong ảnh!")
            else:
                print("❌ FAIL: Có sự không khớp giữa matrix và palette")
                print(f"   Matrix có: {matrix_indices}")
                print(f"   Palette có: {palette_indices}")
            
            # Hiển thị matrix để debug
            print(f"\n🔍 Matrix preview (6x6):")
            for i, row in enumerate(matrix):
                print(f"   Row {i}: {row}")
                
        else:
            print(f"❌ API error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_palette_endpoint():
    """Test endpoint /palette"""
    print("\n🧪 Testing: /palette endpoint")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/palette")
        if response.status_code == 200:
            data = response.json()
            print("✅ Palette endpoint works!")
            print(f"📋 Total colors available: {len(data['palette'])}")
            print(f"📝 Description: {data['description']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("🚀 Testing: Actual Colors Only Feature")
    print("=" * 60)
    
    test_palette_endpoint()
    test_actual_colors_only()
    
    print("\n" + "=" * 60)
    print("✨ Test completed!")
    print("\n💡 Kết quả mong đợi:")
    print("   - Palette chỉ chứa 3 màu: đỏ (1), xanh lá (3), trắng (12)")
    print("   - Matrix chỉ chứa các chỉ số: 1, 3, 12")
    print("   - Không có màu nào khác trong palette response")
