# 🚀 Quick Start Guide

## ⚠️ Lưu ý quan trọng về PORT

Server mặc định chạy trên **port 8000**, không phải 8001!

```bash
✅ Đúng: http://localhost:8000
❌ Sai:  http://localhost:8001
```

## 🏃 Chạy Server

### Option 1: Chạy với uvicorn (Development)

```bash
# Activate virtual environment
source .venv/bin/activate

# Chạy server
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Hoặc
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Chạy trực tiếp với Python

```bash
source .venv/bin/activate
python -m app.main
```

### Option 3: Chạy với Docker

```bash
docker compose up --build
```

## 📍 API Endpoints

### Root & Health
- `GET http://localhost:8000/` - API info
- `GET http://localhost:8000/healthz` - Health check
- `GET http://localhost:8000/docs` - Swagger UI
- `GET http://localhost:8000/redoc` - ReDoc

### Image Converter (`/image`)
- `GET http://localhost:8000/image/palette` - Lấy bảng màu
- `POST http://localhost:8000/image/convert` - Convert ảnh

### Database (`/db`)

#### Images
- `POST http://localhost:8000/db/images` - Tạo image
- `GET http://localhost:8000/db/images` - List images
- `GET http://localhost:8000/db/images/{id}` - Get image by ID
- `PUT http://localhost:8000/db/images/{id}` - Update image
- `DELETE http://localhost:8000/db/images/{id}` - Delete image

#### Histories
- `POST http://localhost:8000/db/histories` - Tạo history
- `GET http://localhost:8000/db/histories` - List histories

#### Imports
- `POST http://localhost:8000/db/imports` - Tạo import
- `GET http://localhost:8000/db/imports` - List imports
- `GET http://localhost:8000/db/imports/{id}` - Get import by ID
- `PUT http://localhost:8000/db/imports/{id}/status` - Update status

## 🧪 Test nhanh

### Test với curl

```bash
# Root endpoint
curl http://localhost:8000

# Health check
curl http://localhost:8000/healthz

# Get palette
curl http://localhost:8000/image/palette

# Convert image
curl -X POST http://localhost:8000/image/convert \
  -F "file=@image.png" \
  -F "cols=30" \
  -F "rows=30"

# Create image record
curl -X POST http://localhost:8000/db/images \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-image",
    "url": "https://example.com/image.png",
    "matrix": [[1,2,3],[4,5,6]],
    "palette": {"1": "#ff0000", "2": "#00ff00"},
    "cols": 3,
    "rows": 2
  }'

# List images
curl http://localhost:8000/db/images

# Get image by ID
curl http://localhost:8000/db/images/{id}
```

### Test với browser

Mở trình duyệt và truy cập:
- http://localhost:8000 - API info
- http://localhost:8000/docs - Interactive API docs
- http://localhost:8000/image/palette - Xem bảng màu

## 🔧 Troubleshooting

### Lỗi: Connection refused

**Nguyên nhân**: Server chưa chạy hoặc sai port

**Giải pháp**:
```bash
# Kiểm tra server có đang chạy không
ps aux | grep uvicorn

# Kiểm tra port
lsof -i :8000

# Chạy lại server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Lỗi: ModuleNotFoundError

**Nguyên nhân**: Chưa cài dependencies

**Giải pháp**:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Lỗi: MongoDB connection failed

**Nguyên nhân**: MongoDB chưa chạy

**Giải pháp**:
```bash
# Chạy MongoDB với Docker
docker compose up mongodb -d

# Hoặc chạy MongoDB local
sudo systemctl start mongodb
```

### Endpoint /db/* không có

**Nguyên nhân**: Database module bị comment out

**Giải pháp**: Đã được fix! Database module đã được enable.

## 📝 Thay đổi Port

### Thay đổi port khi chạy local

```bash
# Chạy trên port 8001
uvicorn app:app --reload --host 0.0.0.0 --port 8001

# Chạy trên port 3000
uvicorn app:app --reload --host 0.0.0.0 --port 3000
```

### Thay đổi port trong Docker

Sửa `docker-compose.yml`:
```yaml
services:
  pixel-api:
    ports:
      - "8001:8000"  # External:Internal
```

## 🎯 Next Steps

1. ✅ Server đã chạy
2. ✅ Test các endpoints
3. ✅ Xem API docs tại `/docs`
4. 📝 Tích hợp với frontend
5. 🧪 Viết tests
6. 🚀 Deploy lên production

## 💡 Tips

- Dùng `/docs` để test API interactively
- Dùng `/redoc` để xem documentation đẹp hơn
- Check logs để debug: `docker compose logs -f`
- Dùng Postman/Insomnia cho testing phức tạp
- Enable CORS nếu gọi từ frontend khác domain

## 📚 More Info

- [README.md](README.md) - Full documentation
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migration from v1.0
- [API Documentation](http://localhost:8000/docs) - Interactive docs

