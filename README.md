# 🎨 Mirai Puzzle API v2.0

API cho Mirai Puzzle - Image Converter & Database Management

## 📁 Cấu trúc dự án

```
ImageGenPython/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app chính
│   ├── config.py               # Configuration
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── image_converter/    # Module gen ảnh
│   │   │   ├── __init__.py
│   │   │   ├── routes.py       # API routes
│   │   │   ├── service.py      # Business logic
│   │   │   └── utils.py        # Helper functions
│   │   └── database/           # Module MongoDB
│   │       ├── __init__.py
│   │       ├── routes.py       # API routes
│   │       ├── service.py      # Business logic
│   │       ├── models.py       # Data models
│   │       └── connection.py   # MongoDB connection
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Common helpers
├── tests/                      # Test files
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 🚀 Cài đặt & Chạy

### 1. Sử dụng Docker (Khuyến nghị)

```bash
# Build và chạy tất cả services (API + MongoDB)
docker compose up --build

# Chạy ở background
docker compose up -d

# Xem logs
docker compose logs -f

# Dừng services
docker compose down
```

### 2. Chạy local (Development)

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Copy .env.example thành .env và chỉnh sửa nếu cần
cp .env.example .env

# Chạy MongoDB (nếu chưa có)
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Chạy API
python -m app.main
# hoặc
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

Sau khi chạy server, truy cập:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Modules

### 1. Image Converter Module (`/image`)

Chuyển đổi ảnh thành pixel art với palette màu.

#### Endpoints:

- `GET /image/palette` - Lấy bảng màu mặc định
- `POST /image/convert` - Chuyển đổi ảnh thành pixel art

#### Ví dụ:

```bash
# Lấy palette
curl http://localhost:8000/image/palette

# Convert ảnh
curl -X POST \
  -F "file=@image.png" \
  -F "cols=30" \
  -F "rows=30" \
  http://localhost:8000/image/convert
```

### 2. Database Module (`/db`)

Quản lý MongoDB operations cho 3 collections: images, histories, imports.

#### Images Endpoints:

- `POST /db/images` - Tạo mới image
- `GET /db/images` - Lấy danh sách images (có phân trang)
- `GET /db/images/{id}` - Lấy image theo ID
- `PUT /db/images/{id}` - Cập nhật image
- `DELETE /db/images/{id}` - Xóa image

#### Histories Endpoints:

- `POST /db/histories` - Tạo history record
- `GET /db/histories` - Lấy danh sách histories

#### Imports Endpoints:

- `POST /db/imports` - Tạo import record
- `GET /db/imports` - Lấy danh sách imports
- `GET /db/imports/{id}` - Lấy import theo ID
- `PUT /db/imports/{id}/status` - Cập nhật trạng thái import

#### Ví dụ:

```bash
# Tạo image
curl -X POST http://localhost:8000/db/images \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test.png",
    "matrix": [[1,2],[3,4]],
    "palette": {"1":"#ff0000","2":"#0000ff"},
    "cols": 2,
    "rows": 2
  }'

# Lấy danh sách images
curl "http://localhost:8000/db/images?skip=0&limit=10"

# Lấy image theo ID
curl http://localhost:8000/db/images/{image_id}

# Cập nhật image
curl -X PUT http://localhost:8000/db/images/{image_id} \
  -H "Content-Type: application/json" \
  -d '{"name": "updated_name.png"}'

# Xóa image
curl -X DELETE http://localhost:8000/db/images/{image_id}
```

## 🔧 Configuration

Cấu hình trong file `.env` hoặc `app/config.py`:

```python
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=Mirai_Puzzle

# Image Settings
DEFAULT_COLS=30
DEFAULT_ROWS=30
MAX_IMAGE_SIZE=10485760  # 10MB
```

## 🗄️ MongoDB Collections

### 1. `images`
Lưu trữ thông tin ảnh đã convert:
- `name`: Tên ảnh
- `url`: URL ảnh gốc (optional)
- `matrix`: Ma trận pixel
- `palette`: Bảng màu sử dụng
- `cols`, `rows`: Kích thước
- `created_at`, `updated_at`: Timestamps
- `metadata`: Metadata bổ sung (optional)

### 2. `histories`
Lưu lịch sử thay đổi:
- `action`: create/update/delete
- `collection`: Collection bị ảnh hưởng
- `document_id`: ID của document
- `user_id`: ID người dùng (optional)
- `changes`: Chi tiết thay đổi
- `timestamp`: Thời gian

### 3. `imports`
Theo dõi quá trình import:
- `source`: Nguồn import
- `status`: pending/processing/completed/failed
- `total_items`, `processed_items`, `failed_items`: Thống kê
- `started_at`, `completed_at`: Timestamps
- `error_message`: Thông báo lỗi (nếu có)

## 🧪 Testing

```bash
# Chạy tests
python -m pytest tests/

# Test với curl
./tests/test_api.sh
```

## 📝 Development

### Thêm module mới:

1. Tạo folder trong `app/modules/`
2. Tạo các file: `__init__.py`, `routes.py`, `service.py`
3. Import router trong `app/main.py`

### Thêm helper functions:

Thêm vào `app/utils/helpers.py`

## 🐛 Troubleshooting

### MongoDB connection error:
```bash
# Kiểm tra MongoDB đang chạy
docker ps | grep mongo

# Restart MongoDB
docker restart mirai-mongodb
```

### Port already in use:
```bash
# Tìm process đang dùng port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

## 📄 License

MIT License

## 👥 Contributors

- Your Name

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Motor Documentation](https://motor.readthedocs.io/)

