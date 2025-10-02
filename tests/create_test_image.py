"""
Tạo ảnh test đơn giản bằng cách tạo file PNG thủ công
"""

def create_simple_png():
    """Tạo một file PNG đơn giản 2x2 pixels với 2 màu"""
    
    # PNG header
    png_signature = b'\x89PNG\r\n\x1a\n'
    
    # IHDR chunk (Image Header)
    width = 2
    height = 2
    bit_depth = 8
    color_type = 2  # RGB
    compression = 0
    filter_method = 0
    interlace = 0
    
    ihdr_data = (
        width.to_bytes(4, 'big') +
        height.to_bytes(4, 'big') +
        bit_depth.to_bytes(1, 'big') +
        color_type.to_bytes(1, 'big') +
        compression.to_bytes(1, 'big') +
        filter_method.to_bytes(1, 'big') +
        interlace.to_bytes(1, 'big')
    )
    
    # CRC calculation (simplified - using a basic implementation)
    def crc32(data):
        import zlib
        return zlib.crc32(data) & 0xffffffff
    
    ihdr_crc = crc32(b'IHDR' + ihdr_data)
    ihdr_chunk = (
        len(ihdr_data).to_bytes(4, 'big') +
        b'IHDR' +
        ihdr_data +
        ihdr_crc.to_bytes(4, 'big')
    )
    
    # IDAT chunk (Image Data)
    # 2x2 RGB image: red, white, white, white
    # Each row needs a filter byte (0 = no filter)
    image_data = (
        b'\x00' +  # Filter byte for row 1
        b'\xff\x00\x00' +  # Red pixel (255, 0, 0)
        b'\xff\xff\xff' +  # White pixel (255, 255, 255)
        b'\x00' +  # Filter byte for row 2
        b'\xff\xff\xff' +  # White pixel (255, 255, 255)
        b'\xff\xff\xff'    # White pixel (255, 255, 255)
    )
    
    # Compress the image data
    import zlib
    compressed_data = zlib.compress(image_data)
    
    idat_crc = crc32(b'IDAT' + compressed_data)
    idat_chunk = (
        len(compressed_data).to_bytes(4, 'big') +
        b'IDAT' +
        compressed_data +
        idat_crc.to_bytes(4, 'big')
    )
    
    # IEND chunk (End of image)
    iend_crc = crc32(b'IEND')
    iend_chunk = (
        b'\x00\x00\x00\x00' +  # Length = 0
        b'IEND' +
        iend_crc.to_bytes(4, 'big')
    )
    
    # Combine all chunks
    png_data = png_signature + ihdr_chunk + idat_chunk + iend_chunk
    
    return png_data

def main():
    print("🎨 Tạo ảnh test PNG đơn giản...")
    
    try:
        png_data = create_simple_png()
        
        # Lưu file
        with open('test_simple.png', 'wb') as f:
            f.write(png_data)
        
        print("✅ Đã tạo test_simple.png (2x2 pixels: 1 đỏ, 3 trắng)")
        print("📊 File size:", len(png_data), "bytes")
        
        # Test với API
        print("\n🧪 Testing với API...")
        import requests
        
        with open('test_simple.png', 'rb') as f:
            files = {'file': ('test_simple.png', f, 'image/png')}
            data = {'cols': 2, 'rows': 2}
            
            response = requests.post('http://localhost:8000/convert', files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ API call successful!")
                print(f"📊 Response palette: {result['meta']['palette']}")
                print(f"📊 Matrix: {result['matrix']}")
                
                # Kiểm tra
                palette = result['meta']['palette']
                matrix = result['matrix']
                
                # Lấy unique indices từ matrix
                unique_indices = set()
                for row in matrix:
                    for idx in row:
                        unique_indices.add(idx)
                
                palette_indices = set(int(k) for k in palette.keys())
                
                print(f"\n🔍 Phân tích:")
                print(f"   Matrix indices: {sorted(unique_indices)}")
                print(f"   Palette indices: {sorted(palette_indices)}")
                
                if unique_indices == palette_indices:
                    print("✅ PASS: Palette chỉ chứa màu có trong ảnh!")
                else:
                    print("❌ FAIL: Có sự không khớp")
                
                # Kiểm tra số lượng màu
                expected_colors = 2  # Đỏ và trắng
                actual_colors = len(palette)
                
                if actual_colors <= expected_colors:
                    print(f"✅ PASS: Chỉ có {actual_colors} màu (≤ {expected_colors} expected)")
                else:
                    print(f"❌ FAIL: Có {actual_colors} màu (> {expected_colors} expected)")
                    
            else:
                print(f"❌ API error: {response.status_code}")
                print(f"   Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
