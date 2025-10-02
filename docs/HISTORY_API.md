# 🔌 History API Documentation

## 📋 Tổng quan

API endpoints để quản lý histories (lịch sử level game puzzle).

**Base URL**: `http://localhost:8000/db/histories`

## 🚀 Endpoints

### 1. **Create History**

Tạo mới history record với đầy đủ thông tin level.

```http
POST /api/histories
Content-Type: application/json
```

**Request Body:**

```json
{
  "key": "history",
  "value": {
    "id": "level_1758776397330_j48tfcloc",
    "name": "Level 18",
    "level": {
      "id": "level_1758776347816",
      "config": { ... },
      "board": [ ... ],
      "containers": [ ... ],
      "difficultyScore": 117,
      "solvable": true,
      "timestamp": "2025-09-25T04:59:07.816000",
      "pipeInfo": [ ... ],
      "lockInfo": null
    },
    "createdAt": "2025-09-25T04:59:57.330Z",
    "updatedAt": "2025-09-25T04:59:57.330Z"
  }
}
```

**Response:**

```json
{
  "success": true,
  "message": "History created successfully",
  "data": {
    "_id": "68d4cc4db1bcb499b9ef54e9",
    "key": "history",
    "value": { ... },
    "timestamp": "2025-09-25T04:59:57.333000"
  }
}
```

**cURL Example:**

```bash
# From file
curl -X POST http://localhost:8000/api/histories \
  -H "Content-Type: application/json" \
  -d @history_data.json

# Inline
curl -X POST http://localhost:8000/api/histories \
  -H "Content-Type: application/json" \
  -d '{
    "key": "history",
    "value": {
      "id": "level_123",
      "name": "18",
      "level": { ... },
      "createdAt": "2025-09-25T04:59:57.330Z",
      "updatedAt": "2025-09-25T04:59:57.330Z"
    }
  }'
```

**💡 Tips:**

- `key` mặc định là `"history"`, có thể bỏ qua trong request
- `name` có thể là số (`"4"`, `"41"`) hoặc text (`"Level 1"`)
- Tất cả fields trong `level.config` đều required
- `board` là 2D array của `CellModel`
- `pipeInfo` và `lockInfo` có thể null
- API tự động thêm `timestamp` khi tạo

---

### 2. **List Histories**

Lấy danh sách histories với phân trang, sorting và search.

```http
GET /api/histories?skip=0&limit=10&sort_by=updatedAt&sort_order=desc&search=level
```

**Query Parameters:**

- `skip` (optional): Số records bỏ qua (default: 0)
- `limit` (optional): Số records tối đa (default: 10, max: 100)
- `collection` (optional): Filter theo collection
- `document_id` (optional): Filter theo document ID
- `search` (optional): Tìm kiếm theo name (case-insensitive)
- `sort_by` (optional): Field để sort - `name` hoặc `updatedAt` (default: `updatedAt`)
- `sort_order` (optional): Thứ tự sort - `asc` hoặc `desc` (default: `desc`)

**🔍 Search Feature:**

- Case-insensitive search trên `value.name`
- Hỗ trợ partial match (tìm "lev" sẽ match "Level 1", "level 2")
- Có thể kết hợp với sort và filter

**⭐ Smart Numeric Sort:**
Khi sort by `name`, API tự động detect và sort đúng:

- Numeric names (`"4"`, `"5"`, `"41"`, `"51"`) → Sort theo giá trị số (4 < 5 < 41 < 51)
- Text names (`"Level A"`, `"Level B"`) → Sort theo alphabet
- Mixed: Số trước, text sau (khi ascending)

**Response:**

```json
{
  "success": true,
  "message": "Retrieved 10 histories",
  "data": {
    "items": [
      {
        "_id": "68d4cc4db1bcb499b9ef54e9",
        "key": "history",
        "value": {
          "id": "level_123",
          "name": "Level 18",
          "level": { ... },
          "createdAt": "2025-09-25T04:59:57.330Z",
          "updatedAt": "2025-09-25T04:59:57.330Z"
        },
        "updatedAt": "2025-09-25T04:59:57.333000"
      }
    ],
    "pagination": {
      "skip": 0,
      "limit": 10,
      "total": 50,
      "has_more": true
    },
    "sort": {
      "by": "updatedAt",
      "order": "desc"
    },
    "search": null
  }
}
```

**cURL Examples:**

```bash
# Default: Sort by updatedAt desc
curl "http://localhost:8000/api/histories?skip=0&limit=10"

# Search by name (case-insensitive)
curl "http://localhost:8000/api/histories?search=level"

# Search for numeric names
curl "http://localhost:8000/api/histories?search=18"

# Search + Sort by name ascending
curl "http://localhost:8000/api/histories?search=level&sort_by=name&sort_order=asc"

# Search + Pagination
curl "http://localhost:8000/api/histories?search=level&skip=10&limit=20"

# Sort by name ascending
curl "http://localhost:8000/api/histories?sort_by=name&sort_order=asc"

# Sort by updatedAt ascending
curl "http://localhost:8000/api/histories?sort_by=updatedAt&sort_order=asc"

# Sort by name descending with pagination
curl "http://localhost:8000/api/histories?skip=10&limit=20&sort_by=name&sort_order=desc"
```

---

### 3. **Get History by ID**

Lấy history theo ID.

```http
GET /db/histories/{history_id}
```

**Path Parameters:**

- `history_id`: MongoDB ObjectId của history

**Response:**

```json
{
  "success": true,
  "data": {
    "_id": "68d4cc4db1bcb499b9ef54e9",
    "key": "history",
    "value": {
      "id": "level_1758776397330_j48tfcloc",
      "name": "Level 18",
      "level": { ... },
      "createdAt": "2025-09-25T04:59:57.330Z",
      "updatedAt": "2025-09-25T04:59:57.330Z"
    },
    "updatedAt": "2025-09-25T04:59:57.333000"
  }
}
```

**Error Response (404):**

```json
{
  "detail": "History not found"
}
```

**cURL Example:**

```bash
curl http://localhost:8000/db/histories/68d4cc4db1bcb499b9ef54e9
```

---

### 4. **Update History Level**

Cập nhật level data của history (board, config, containers, etc.)

```http
PUT /api/histories/{history_id}
Content-Type: application/json
```

**Path Parameters:**

- `history_id`: History ID (value.id, không phải MongoDB \_id)

**Request Body:**

Chỉ cần gửi level data, không cần wrapper `key` và `value`:

```json
{
  "board": [
    [
      { "type": "wall", "color": null, "element": null },
      { "type": "block", "color": "1", "element": null }
    ]
  ],
  "config": {
    "name": "Updated Level",
    "width": 9,
    "height": 10,
    "blockCount": 30,
    "colorCount": 3,
    "selectedColors": ["1", "2", "3"],
    "colorMapping": {
      "1": "#ff0000",
      "2": "#0000ff",
      "3": "#00ff00"
    },
    "generationMode": "random",
    "elements": {},
    "difficulty": "Hard"
  },
  "containers": [],
  "difficultyScore": 75,
  "solvable": true,
  "pipeInfo": null,
  "lockInfo": null
}
```

**Response:**

```json
{
  "success": true,
  "message": "History level updated successfully",
  "data": {
    "_id": "68d4cc4db1bcb499b9ef54e9",
    "key": "history",
    "value": {
      "id": "level_1758776397330_j48tfcloc",
      "name": "Level 18",
      "level": {
        "board": [...],
        "config": {...},
        "containers": [],
        "difficultyScore": 75,
        "solvable": true,
        ...
      },
      "updatedAt": "2025-09-25T05:00:00.000Z"
    },
    "updatedAt": "2025-09-25T05:00:00.000Z"
  }
}
```

**cURL Example:**

```bash
curl -X PUT http://localhost:8000/api/histories/level_1758776397330_j48tfcloc \
  -H "Content-Type: application/json" \
  -d '{
    "board": [[{"type": "wall", "color": null, "element": null}]],
    "config": {
      "name": "Updated",
      "width": 9,
      "height": 10,
      "blockCount": 30,
      "colorCount": 3,
      "selectedColors": ["1", "2", "3"],
      "colorMapping": {"1": "#ff0000", "2": "#0000ff", "3": "#00ff00"},
      "generationMode": "random",
      "elements": {},
      "difficulty": "Hard"
    },
    "containers": [],
    "difficultyScore": 75,
    "solvable": true,
    "pipeInfo": null,
    "lockInfo": null
  }'
```

**💡 Note:**

- Chỉ gửi level data, không cần `key` và `value` wrapper
- Tất cả fields trong `HistoryLevelModel` đều required (trừ optional fields)
- `value.updatedAt` và `updatedAt` sẽ tự động update

---

### 5. **Update History Name**

Cập nhật chỉ tên của history (value.name).

```http
PUT /api/histories/{history_id}/name
Content-Type: application/json
```

**Path Parameters:**

- `history_id`: ID của history (value.id, không phải MongoDB \_id)

**Request Body:**

```json
{
  "name": "New Level Name"
}
```

**Response:**

```json
{
  "success": true,
  "message": "History name updated successfully",
  "data": {
    "_id": "68d4cc4db1bcb499b9ef54e9",
    "key": "history",
    "value": {
      "id": "level_1758776397330_j48tfcloc",
      "name": "New Level Name",
      "level": { ... },
      "createdAt": "2025-09-25T04:59:57.330Z",
      "updatedAt": "2025-09-25T05:00:00.000Z"
    },
    "updatedAt": "2025-09-25T05:00:00.000Z"
  }
}
```

**cURL Example:**

```bash
curl -X PUT http://localhost:8000/api/histories/level_1758776397330_j48tfcloc/name \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Name"}'
```

---

### 6. **Delete History** ✨ NEW

Xóa history theo ID.

```http
DELETE /db/histories/{history_id}
```

**Path Parameters:**

- `history_id`: MongoDB ObjectId của history

**Response:**

```json
{
  "success": true,
  "message": "History deleted successfully"
}
```

**Error Response (404):**

```json
{
  "detail": "History not found"
}
```

**cURL Example:**

```bash
curl -X DELETE http://localhost:8000/db/histories/68d4cc4db1bcb499b9ef54e9
```

---

## 📊 Response Format

Tất cả responses đều follow format chuẩn:

### Success Response:

```json
{
  "success": true,
  "message": "Operation message",
  "data": { ... }
}
```

### Error Response:

```json
{
  "detail": "Error message"
}
```

## 🔍 Query Examples

### List với filter:

```bash
# Lấy 20 histories đầu tiên
curl "http://localhost:8000/db/histories?limit=20"

# Skip 10 records đầu
curl "http://localhost:8000/db/histories?skip=10&limit=10"
```

### Update partial data:

```bash
# Chỉ update name
curl -X PUT "http://localhost:8000/db/histories/{id}/name?name=New%20Name"

# Update toàn bộ value
curl -X PUT http://localhost:8000/db/histories/{id} \
  -H "Content-Type: application/json" \
  -d '{"value": {...}}'
```

## 🧪 Testing

Chạy test script:

```bash
./tests/test_history_crud.sh
```

Test script sẽ:

1. ✅ Create history
2. ✅ Get history by ID
3. ✅ List histories
4. ✅ Update history name
5. ✅ Update full history
6. ✅ Verify update
7. ✅ Delete history
8. ✅ Verify deletion

## 💡 Tips

1. **Validation**: Pydantic tự động validate request body
2. **ObjectId**: MongoDB ObjectId phải hợp lệ (24 hex characters)
3. **Timestamps**: Tự động update `updatedAt` khi update
4. **Nested Update**: Có thể update nested fields với dot notation
5. **Partial Update**: Chỉ gửi fields cần update

## 🔧 Error Codes

- `400`: Bad Request (invalid data)
- `404`: History not found
- `422`: Validation Error (Pydantic)
- `500`: Internal Server Error

## 📚 Related Documentation

- [History Model](./HISTORY_MODEL.md) - Chi tiết về data structure
- [Quick Start](../QUICK_START.md) - Hướng dẫn setup
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI
