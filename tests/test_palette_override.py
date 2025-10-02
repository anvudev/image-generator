"""
Test script để kiểm tra palette_override mới
"""

import requests
import json
from PIL import Image
import io


# Tạo ảnh test đơn giản
def create_test_image():
    """Tạo ảnh test 10x10 với các màu khác nhau"""
    img = Image.new("RGB", (10, 10))
    pixels = img.load()

    # Tạo pattern màu đơn giản
    for y in range(10):
        for x in range(10):
            if x < 3:
                pixels[x, y] = (255, 0, 0)  # Đỏ
            elif x < 6:
                pixels[x, y] = (0, 255, 0)  # Xanh lá
            else:
                pixels[x, y] = (0, 0, 255)  # Xanh dương

    return img


def test_palette_endpoint():
    """Test endpoint /palette"""
    print("🧪 Testing /palette endpoint...")
    try:
        response = requests.get("http://localhost:8000/palette")
        if response.status_code == 200:
            data = response.json()
            print("✅ Palette endpoint works!")
            print(f"📋 Available colors: {len(data['palette'])} colors")
            print("🎨 Examples:")
            for example in data["usage"]["examples"]:
                print(f"   - {example}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure server is running with Docker: docker compose up")


def test_convert_with_palette_override():
    """Test convert với palette_override"""
    print("\n🧪 Testing /convert with palette_override...")

    # Tạo ảnh test
    img = create_test_image()
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    test_cases = [
        {
            "name": "Chỉ dùng màu đỏ và xanh lá",
            "palette": "1,3",  # Red, Green
        },
        {
            "name": "Dùng JSON array format",
            "palette": "[1,2,4]",  # Red, Blue, Yellow
        },
        {
            "name": "Dùng nhiều màu",
            "palette": "1,2,3,4,5",  # Red, Blue, Green, Yellow, Orange
        },
        {
            "name": "Test lỗi - số không hợp lệ",
            "palette": "1,99",  # 99 không có trong DEFAULT_PALETTE
            "should_fail": True,
        },
        {"name": "Test lỗi - format sai", "palette": "abc,def", "should_fail": True},
    ]

    for test_case in test_cases:
        print(f"\n📝 Test: {test_case['name']}")
        print(f"   Palette: {test_case['palette']}")

        try:
            # Reset file pointer
            img_bytes.seek(0)

            files = {"file": ("test.png", img_bytes, "image/png")}
            data = {"cols": 5, "rows": 5, "palette_override": test_case["palette"]}

            response = requests.post(
                "http://localhost:8000/convert", files=files, data=data
            )

            if test_case.get("should_fail", False):
                if response.status_code != 200:
                    print(f"   ✅ Expected error: {response.status_code}")
                    print(
                        f"   📄 Error message: {response.json().get('detail', 'No detail')}"
                    )
                else:
                    print(f"   ❌ Should have failed but got 200")
            else:
                if response.status_code == 200:
                    result = response.json()
                    used_palette = result["meta"]["palette"]
                    print(f"   ✅ Success! Used {len(used_palette)} colors")
                    print(f"   🎨 Colors: {list(used_palette.keys())}")
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    print(f"   📄 Error: {response.json().get('detail', 'No detail')}")

        except Exception as e:
            print(f"   ❌ Exception: {e}")


if __name__ == "__main__":
    print("🚀 Testing Palette Override Feature")
    print("=" * 50)

    test_palette_endpoint()
    test_convert_with_palette_override()

    print("\n" + "=" * 50)
    print("✨ Test completed!")
