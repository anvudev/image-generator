"""
Simple test script để kiểm tra palette_override mới
"""

import requests
import json


def test_palette_endpoint():
    """Test endpoint /palette"""
    print("🧪 Testing /palette endpoint...")
    try:
        response = requests.get("http://localhost:8000/palette")
        if response.status_code == 200:
            data = response.json()
            print("✅ Palette endpoint works!")
            print(f"📋 Available colors: {len(data['palette'])} colors")
            print("🎨 Palette colors:")
            for idx, color in data["palette"].items():
                print(f"   {idx}: {color}")
            print(f"\n📝 Description: {data['description']}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure server is running with Docker: docker compose up")


def test_healthz():
    """Test health endpoint"""
    print("\n🧪 Testing /healthz endpoint...")
    try:
        response = requests.get("http://localhost:8000/healthz")
        if response.status_code == 200:
            print("✅ Health endpoint works!")
            print(f"📄 Response: {response.json()}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")


if __name__ == "__main__":
    print("🚀 Testing Palette Override Feature")
    print("=" * 50)

    test_healthz()
    test_palette_endpoint()

    print("\n" + "=" * 50)
    print("✨ Test completed!")
