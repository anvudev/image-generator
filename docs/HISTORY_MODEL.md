# 📚 History Model Documentation

## 🎯 Tổng quan

Collection `histories` lưu trữ lịch sử các level game puzzle với cấu trúc phức tạp bao gồm:
- Thông tin level (config, board, containers)
- Thông tin game elements (pipes, barrels, ice, bombs)
- Điểm độ khó và khả năng giải được

## 📊 Cấu trúc dữ liệu

### **Root Level**

```json
{
  "_id": "ObjectId",
  "key": "history",
  "value": { ... },
  "updatedAt": "ISO datetime"
}
```

### **Value Object**

```json
{
  "id": "level_1758776397330_j48tfcloc",
  "name": "18",
  "level": { ... },
  "createdAt": "2025-09-25T04:59:57.330Z",
  "updatedAt": "2025-09-25T04:59:57.330Z"
}
```

### **Level Object**

```json
{
  "id": "level_1758776347816",
  "config": { ... },
  "board": [ ... ],
  "containers": [ ... ],
  "difficultyScore": 117,
  "solvable": true,
  "timestamp": "2025-09-25T04:59:07.816000",
  "pipeInfo": [ ... ],
  "lockInfo": null
}
```

## 🔧 Các Models

### **1. CellModel**
Đại diện cho một ô trên board game.

```python
class CellModel(BaseModel):
    type: str              # "wall" | "empty" | "block"
    color: Optional[str]   # Màu của block (nếu có)
    element: Optional[str] # "Pipe" | "Barrel" | "Ice" | "Bomb"
```

**Ví dụ:**
```json
{
  "type": "block",
  "color": "1",
  "element": "Barrel"
}
```

### **2. ContainerContentModel**
Nội dung trong container.

```python
class ContainerContentModel(BaseModel):
    color: str  # Màu của block
    type: str   # "block"
```

### **3. ContainerModel**
Container chứa các blocks.

```python
class ContainerModel(BaseModel):
    id: str                              # "container_0"
    slots: int                           # Số slot
    contents: list[ContainerContentModel] # Nội dung
```

**Ví dụ:**
```json
{
  "id": "container_0",
  "slots": 4,
  "contents": [
    {"color": "1", "type": "block"},
    {"color": "3", "type": "block"}
  ]
}
```

### **4. PipeInfoModel**
Thông tin về pipe trong game.

```python
class PipeInfoModel(BaseModel):
    id: str                    # "pipe1"
    contents: list[str]        # ["5", "8", "4", "3"]
    direction: str             # "left" | "right" | "up" | "down"
    position: dict[str, int]   # {"x": 4, "y": 6}
```

**Ví dụ:**
```json
{
  "id": "pipe1",
  "contents": ["5", "8", "4", "3", "3", "8"],
  "direction": "right",
  "position": {"x": 4, "y": 6}
}
```

### **5. LevelConfigModel**
Cấu hình của level.

```python
class LevelConfigModel(BaseModel):
    name: str                      # Tên level
    width: int                     # Chiều rộng board
    height: int                    # Chiều cao board
    blockCount: int                # Số lượng block
    colorCount: int                # Số lượng màu
    selectedColors: list[str]      # ["1", "2", "3", ...]
    colorMapping: dict[str, str]   # {"1": "#ff0000", ...}
    generationMode: str            # "symmetric" | "random"
    elements: dict[str, int]       # {"Pipe": 2, "Barrel": 20}
    difficulty: str                # "Easy" | "Medium" | "Hard"
    pipeCount: int                 # Số lượng pipe
    pipeBlockCounts: list[int]     # [6, 6]
    iceCounts: list[int]           # [2]
    bombCounts: list[int]          # [2]
    id: str                        # Config ID
    status: str                    # "pending" | "completed"
    createdAt: str                 # ISO datetime
    updatedAt: str                 # ISO datetime
```

### **6. LevelModel**
Dữ liệu đầy đủ của level.

```python
class LevelModel(BaseModel):
    id: str                              # Level ID
    config: LevelConfigModel             # Cấu hình
    board: list[list[CellModel]]         # Board 2D
    containers: list[ContainerModel]     # Containers
    difficultyScore: int                 # Điểm độ khó
    solvable: bool                       # Có giải được không
    timestamp: str                       # Timestamp
    pipeInfo: Optional[list[PipeInfoModel]]  # Thông tin pipes
    lockInfo: Optional[Any]              # Thông tin lock
```

### **7. HistoryValueModel**
Value trong history document.

```python
class HistoryValueModel(BaseModel):
    id: str           # History value ID
    name: str         # Tên level
    level: LevelModel # Dữ liệu level
    createdAt: str    # Thời gian tạo
    updatedAt: str    # Thời gian cập nhật
```

### **8. HistoryModel**
Model chính cho collection histories.

```python
class HistoryModel(BaseModel):
    key: str                  # "history"
    value: HistoryValueModel  # Dữ liệu history
    updatedAt: str            # Thời gian cập nhật
```

## 🚀 API Usage

### **Tạo History**

```bash
POST /db/histories
Content-Type: application/json

{
  "key": "history",
  "value": {
    "id": "level_1758776397330_j48tfcloc",
    "name": "18",
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

### **List Histories**

```bash
GET /db/histories?skip=0&limit=10
```

### **Response Format**

```json
{
  "success": true,
  "data": [
    {
      "_id": "68d4cc4db1bcb499b9ef54e9",
      "key": "history",
      "value": { ... },
      "updatedAt": "2025-09-25T04:59:57.333000"
    }
  ],
  "count": 1
}
```

## 📝 Ví dụ đầy đủ

```json
{
  "_id": "68d4cc4db1bcb499b9ef54e9",
  "key": "history",
  "value": {
    "id": "level_1758776397330_j48tfcloc",
    "name": "18",
    "level": {
      "id": "level_1758776347816",
      "config": {
        "name": "18",
        "width": 9,
        "height": 10,
        "blockCount": 75,
        "colorCount": 3,
        "selectedColors": ["1", "2", "3", "4", "5", "6", "7", "8"],
        "colorMapping": {
          "1": "#ff0000",
          "2": "#0000ff",
          "3": "#00ff00"
        },
        "generationMode": "symmetric",
        "elements": {
          "Pipe": 2,
          "Barrel": 20
        },
        "difficulty": "Hard",
        "pipeCount": 2,
        "pipeBlockCounts": [6, 6],
        "iceCounts": [2],
        "bombCounts": [2],
        "id": "import-1758771908607-13",
        "status": "pending",
        "createdAt": "2025-09-25T03:45:08.607Z",
        "updatedAt": "2025-09-25T03:45:08.607Z"
      },
      "board": [
        [
          {"type": "wall", "color": null, "element": null},
          {"type": "block", "color": "1", "element": "Barrel"}
        ]
      ],
      "containers": [
        {
          "id": "container_0",
          "slots": 4,
          "contents": [
            {"color": "1", "type": "block"},
            {"color": "3", "type": "block"}
          ]
        }
      ],
      "difficultyScore": 117,
      "solvable": true,
      "timestamp": "2025-09-25T04:59:07.816000",
      "pipeInfo": [
        {
          "id": "pipe1",
          "contents": ["5", "8", "4", "3", "3", "8"],
          "direction": "right",
          "position": {"x": 4, "y": 6}
        }
      ],
      "lockInfo": null
    },
    "createdAt": "2025-09-25T04:59:57.330Z",
    "updatedAt": "2025-09-25T04:59:57.330Z"
  },
  "updatedAt": "2025-09-25T04:59:57.333000"
}
```

## 🎮 Game Elements

### **Cell Types:**
- `wall`: Tường, không thể đặt block
- `empty`: Ô trống
- `block`: Ô có block với màu

### **Elements:**
- `Pipe`: Ống dẫn blocks
- `Barrel`: Thùng chứa
- `Ice`: Băng (cần phá)
- `Bomb`: Bom (phá nhiều blocks)

### **Difficulty Levels:**
- `Easy`: Dễ
- `Medium`: Trung bình
- `Hard`: Khó

### **Generation Modes:**
- `symmetric`: Tạo level đối xứng
- `random`: Tạo level ngẫu nhiên

## 💡 Tips

1. **Validation**: Pydantic tự động validate tất cả fields
2. **Nested Structure**: Sử dụng nested models cho cấu trúc phức tạp
3. **Optional Fields**: `pipeInfo` và `lockInfo` có thể null
4. **Timestamps**: Sử dụng ISO 8601 format
5. **Color Mapping**: Map từ ID (string) sang hex color

## 🔍 Query Examples

```python
# Tìm level theo độ khó
db.histories.find({"value.level.config.difficulty": "Hard"})

# Tìm level có thể giải được
db.histories.find({"value.level.solvable": true})

# Tìm level theo điểm độ khó
db.histories.find({"value.level.difficultyScore": {"$gte": 100}})

# Tìm level có pipe
db.histories.find({"value.level.config.pipeCount": {"$gt": 0}})
```

