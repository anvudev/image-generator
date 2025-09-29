# 🎨 Palette Override Feature

## Tổng quan

Tính năng **Palette Override** cho phép bạn tùy chỉnh bảng màu được sử dụng khi chuyển đổi ảnh thành pixel art. Thay vì sử dụng tất cả 12 màu mặc định, bạn có thể chọn chỉ một số màu cụ thể.

## 🚀 Cách sử dụng

### 1. Xem danh sách màu có sẵn

```bash
GET /palette
```

**Response:**
```json
{
  "palette": {
    "1": "#ff0000",  // Đỏ
    "2": "#0000ff",  // Xanh dương
    "3": "#00ff00",  // Xanh lá
    "4": "#ffff00",  // Vàng
    "5": "#ff9900",  // Cam
    "6": "#9900ff",  // Tím
    "7": "#ff00ff",  // Hồng
    "8": "#00ffff",  // Cyan
    "9": "#4a86e8",  // Xanh nhạt
    "10": "#876670", // Nâu
    "11": "#b7b7b7", // Xám
    "12": "#ffffff"  // Trắng
  },
  "usage": {
    "description": "Sử dụng chỉ số này trong palette_override",
    "examples": [
      "1,2,3,4 (chỉ dùng đỏ, xanh dương, xanh lá, vàng)",
      "[1,5,7] (chỉ dùng đỏ, cam, hồng)",
      "1,2,3,4,5,6,7,8,9,10,11,12 (dùng tất cả màu)"
    ]
  }
}
```

### 2. Sử dụng Palette Override

Khi gọi API `/convert`, thêm parameter `palette_override` với danh sách số của các màu bạn muốn sử dụng.

#### Format 1: Comma-separated
```bash
curl -X POST \
  -F "file=@image.png" \
  -F "cols=30" \
  -F "rows=30" \
  -F "palette_override=1,2,3,4" \
  http://localhost:8000/convert
```

#### Format 2: JSON Array
```bash
curl -X POST \
  -F "file=@image.png" \
  -F "cols=30" \
  -F "rows=30" \
  -F "palette_override=[1,5,7]" \
  http://localhost:8000/convert
```

## 📝 Ví dụ thực tế

### Chỉ dùng màu đỏ và xanh lá
```bash
palette_override=1,3
```
Kết quả: Ảnh sẽ chỉ sử dụng màu đỏ (#ff0000) và xanh lá (#00ff00)

### Tạo hiệu ứng retro với 4 màu cơ bản
```bash
palette_override=1,2,3,4
```
Kết quả: Ảnh sẽ có phong cách retro với đỏ, xanh dương, xanh lá, vàng

### Tông màu pastel
```bash
palette_override=[7,8,9,11]
```
Kết quả: Sử dụng hồng, cyan, xanh nhạt, xám

## ⚠️ Lưu ý

1. **Chỉ số hợp lệ**: Chỉ sử dụng số từ 1-12
2. **Format hỗ trợ**: 
   - `1,2,3,4` (comma-separated)
   - `[1,2,3,4]` (JSON array)
3. **Lỗi thường gặp**:
   - Sử dụng số ngoài phạm vi 1-12 → Error 400
   - Format sai → Error 400

## 🧪 Test

Chạy test để kiểm tra tính năng:

```bash
# Test cơ bản
python3 simple_test.py

# Test với curl
curl -s http://localhost:8000/palette
```

## 🔧 Kỹ thuật

- **Backward compatible**: Nếu không truyền `palette_override`, sẽ sử dụng tất cả 12 màu mặc định
- **Validation**: Kiểm tra tất cả chỉ số có trong DEFAULT_PALETTE
- **Error handling**: Trả về lỗi chi tiết khi format không đúng
- **Flexible parsing**: Hỗ trợ nhiều format input khác nhau
