"""
Demo script để thử nghiệm palette override
"""
import requests
import json

def demo_palette_override():
    """Demo các tính năng palette override"""
    
    print("🎨 DEMO: Palette Override Feature")
    print("=" * 50)
    
    # 1. Lấy thông tin palette
    print("📋 1. Danh sách màu có sẵn:")
    try:
        response = requests.get("http://localhost:8000/palette")
        if response.status_code == 200:
            data = response.json()
            palette = data['palette']
            
            print("   Chỉ số | Màu     | Mô tả")
            print("   -------|---------|----------")
            color_names = {
                "1": "Đỏ", "2": "Xanh dương", "3": "Xanh lá", "4": "Vàng",
                "5": "Cam", "6": "Tím", "7": "Hồng", "8": "Cyan",
                "9": "Xanh nhạt", "10": "Nâu", "11": "Xám", "12": "Trắng"
            }
            
            for idx, color in palette.items():
                name = color_names.get(idx, "Unknown")
                print(f"   {idx:>6} | {color:>7} | {name}")
                
        else:
            print(f"   ❌ Lỗi: {response.status_code}")
            return
            
    except Exception as e:
        print(f"   ❌ Lỗi kết nối: {e}")
        return
    
    print("\n" + "=" * 50)
    
    # 2. Các ví dụ sử dụng
    examples = [
        {
            "name": "🔴 Chỉ màu đỏ",
            "palette": "1",
            "description": "Chỉ sử dụng màu đỏ"
        },
        {
            "name": "🌈 4 màu cơ bản",
            "palette": "1,2,3,4",
            "description": "Đỏ, xanh dương, xanh lá, vàng"
        },
        {
            "name": "🎨 Tông pastel",
            "palette": "[7,8,9,11]",
            "description": "Hồng, cyan, xanh nhạt, xám"
        },
        {
            "name": "🔥 Tông nóng",
            "palette": "[1,4,5]",
            "description": "Đỏ, vàng, cam"
        },
        {
            "name": "❄️ Tông lạnh",
            "palette": "[2,3,8,9]",
            "description": "Xanh dương, xanh lá, cyan, xanh nhạt"
        }
    ]
    
    print("💡 2. Ví dụ sử dụng palette_override:")
    for i, example in enumerate(examples, 1):
        print(f"\n   {i}. {example['name']}")
        print(f"      palette_override={example['palette']}")
        print(f"      → {example['description']}")
        
        # Tạo curl command
        curl_cmd = f"""curl -X POST \\
  -F "file=@your_image.png" \\
  -F "cols=30" \\
  -F "rows=30" \\
  -F "palette_override={example['palette']}" \\
  http://localhost:8000/convert"""
        
        print(f"      Command:")
        for line in curl_cmd.split('\n'):
            print(f"        {line}")
    
    print("\n" + "=" * 50)
    
    # 3. Test lỗi
    print("⚠️  3. Test các trường hợp lỗi:")
    
    error_cases = [
        {
            "palette": "1,99",
            "error": "Chỉ số 99 không tồn tại (chỉ có 1-12)"
        },
        {
            "palette": "abc,def",
            "error": "Format không hợp lệ (phải là số)"
        },
        {
            "palette": "1,2,3,",
            "error": "Có dấu phẩy thừa"
        }
    ]
    
    for i, case in enumerate(error_cases, 1):
        print(f"\n   {i}. palette_override={case['palette']}")
        print(f"      → Lỗi: {case['error']}")
    
    print("\n" + "=" * 50)
    print("✨ Demo hoàn thành!")
    print("\n💡 Để test thực tế:")
    print("   1. Chuẩn bị file ảnh (PNG/JPG/WebP)")
    print("   2. Sử dụng curl command ở trên")
    print("   3. Hoặc dùng Postman/Insomnia để test")

if __name__ == "__main__":
    demo_palette_override()
