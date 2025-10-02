# History Create - Simplified Payload

## 🎯 **Overview**

API tự động generate các fields không cần thiết, frontend chỉ cần gửi data tối thiểu.

---

## ✅ **Auto-Generated Fields**

API sẽ tự động tạo các fields sau nếu không có trong request:

### **IDs:**

- `value.id` → `level_{timestamp}_{random}` (Base ID)
- `value.level.id` → **Same as `value.id`** ⭐
- `value.level.config.id` → **Same as `value.id`** ⭐

**Note:** Tất cả 3 IDs này sẽ giống nhau để dễ dàng tracking và query.

### **Timestamps:**

- `value.level.config.createdAt` → Current ISO timestamp
- `value.level.config.updatedAt` → Current ISO timestamp
- `value.level.timestamp` → Current timestamp with microseconds
- `value.createdAt` → Current ISO timestamp
- `value.updatedAt` → Current ISO timestamp
- `timestamp` (root) → Current ISO timestamp

---

## 📝 **Minimal Payload Example**

Frontend chỉ cần gửi:

```json
{
  "value": {
    "name": "18",
    "level": {
      "config": {
        "name": "Level",
        "width": 9,
        "height": 10,
        "blockCount": 27,
        "colorCount": 3,
        "selectedColors": ["1", "2", "3"],
        "colorMapping": {
          "1": "#664b55",
          "2": "#1b4efc",
          "3": "#08cf62"
        },
        "generationMode": "random",
        "elements": {},
        "difficulty": "Normal"
      },
      "board": [
        [
          { "type": "wall", "color": null, "element": null },
          { "type": "block", "color": "1", "element": null }
        ]
      ],
      "containers": [],
      "difficultyScore": 50,
      "solvable": true,
      "pipeInfo": null,
      "lockInfo": null
    }
  }
}
```

---

## 🔄 **What API Returns**

API sẽ trả về document đầy đủ với tất cả fields đã được generate:

```json
{
  "success": true,
  "message": "History created successfully",
  "timestamp": "2025-09-25T05:00:00.000000Z",
  "data": {
    "_id": "68d4cc4db1bcb499b9ef54e9",
    "key": "history",
    "value": {
      "id": "level_1759389769712_5cqoe8p55",
      "name": "18",
      "level": {
        "id": "level_1759389769712_5cqoe8p55",  // ⭐ Same as value.id
        "config": {
          "name": "Level",
          "width": 9,
          "height": 10,
          "blockCount": 27,
          "colorCount": 3,
          "selectedColors": ["1", "2", "3"],
          "colorMapping": {
            "1": "#664b55",
            "2": "#1b4efc",
            "3": "#08cf62"
          },
          "generationMode": "random",
          "elements": {},
          "difficulty": "Normal",
          "pipeCount": 0,
          "pipeBlockCounts": [],
          "iceCounts": [],
          "bombCounts": [],
          "id": "level_1759389769712_5cqoe8p55",  // ⭐ Same as value.id
          "status": "pending",
          "createdAt": "2025-09-25T05:00:00.000000Z",
          "updatedAt": "2025-09-25T05:00:00.000000Z"
        },
        "board": [[...]],
        "containers": [],
        "difficultyScore": 50,
        "solvable": true,
        "timestamp": "2025-09-25T05:00:00.000000",
        "pipeInfo": null,
        "lockInfo": null
      },
      "createdAt": "2025-09-25T05:00:00.000000Z",
      "updatedAt": "2025-09-25T05:00:00.000000Z"
    },
    "timestamp": "2025-09-25T05:00:00.000000Z"
  }
}
```

---

## 📋 **Required Fields**

Frontend **PHẢI** gửi các fields sau:

### **value.name** (string)

Tên level, có thể là số hoặc text:

```json
"name": "18"        // Numeric
"name": "Level 1"   // Text
```

### **value.level.config** (object)

Tất cả fields trong config đều required (trừ các fields có default):

**Required:**

- `name` (string)
- `width` (int)
- `height` (int)
- `blockCount` (int)
- `colorCount` (int)
- `selectedColors` (array of strings)
- `colorMapping` (object: color_id → hex)
- `generationMode` (string: "random" | "symmetric")
- `difficulty` (string: "Easy" | "Normal" | "Hard")

**Optional (có default):**

- `elements` (object, default: `{}`)
- `pipeCount` (int, default: `0`)
- `pipeBlockCounts` (array, default: `[]`)
- `iceCounts` (array, default: `[]`)
- `bombCounts` (array, default: `[]`)
- `status` (string, default: `"pending"`)

**Auto-generated:**

- `id`
- `createdAt`
- `updatedAt`

### **value.level.board** (2D array)

Board game với cells:

```json
"board": [
  [
    {"type": "wall", "color": null, "element": null},
    {"type": "block", "color": "1", "element": null},
    {"type": "empty", "color": null, "element": null}
  ]
]
```

**Cell types:**

- `"wall"` - Tường
- `"block"` - Block có màu
- `"empty"` - Ô trống

### **value.level.containers** (array)

Danh sách containers:

```json
"containers": [
  {
    "id": "container_0",
    "slots": 4,
    "contents": [
      {"color": "1", "type": "block"}
    ]
  }
]
```

### **value.level.difficultyScore** (int)

Điểm độ khó:

```json
"difficultyScore": 50
```

### **value.level.solvable** (bool)

Level có giải được không:

```json
"solvable": true
```

### **value.level.pipeInfo** (array | null)

Thông tin pipes (có thể null):

```json
"pipeInfo": [
  {
    "id": "pipe1",
    "contents": ["5", "8", "4"],
    "direction": "right",
    "position": {"x": 4, "y": 6}
  }
]
```

### **value.level.lockInfo** (any | null)

Thông tin lock (có thể null):

```json
"lockInfo": null
```

---

## 🚀 **cURL Example**

```bash
curl -X POST http://localhost:8000/api/histories \
  -H "Content-Type: application/json" \
  -d '{
    "value": {
      "name": "18",
      "level": {
        "config": {
          "name": "Level",
          "width": 9,
          "height": 10,
          "blockCount": 27,
          "colorCount": 3,
          "selectedColors": ["1", "2", "3"],
          "colorMapping": {
            "1": "#664b55",
            "2": "#1b4efc",
            "3": "#08cf62"
          },
          "generationMode": "random",
          "elements": {},
          "difficulty": "Normal"
        },
        "board": [[{"type": "wall", "color": null, "element": null}]],
        "containers": [],
        "difficultyScore": 50,
        "solvable": true,
        "pipeInfo": null,
        "lockInfo": null
      }
    }
  }'
```

---

## ⚠️ **Common Errors**

### **Missing Required Field**

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "value", "level", "config", "width"],
      "msg": "Field required"
    }
  ]
}
```

**Fix:** Thêm field `width` vào `config`

### **Invalid Type**

```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["body", "value", "level", "config", "width"],
      "msg": "Input should be a valid integer"
    }
  ]
}
```

**Fix:** `width` phải là số nguyên, không phải string

---

## 💡 **Tips**

1. **Key field:** Có thể bỏ qua, mặc định là `"history"`
2. **IDs:** Không cần gửi, API tự generate
3. **Timestamps:** Không cần gửi, API tự generate
4. **Numeric names:** Dùng string `"18"` thay vì number `18`
5. **Empty arrays:** Dùng `[]` thay vì `null`
6. **Null values:** Dùng `null` cho `pipeInfo` và `lockInfo` nếu không có

---

## 📊 **Field Summary**

| Field                          | Required | Auto-Generated | Default |
| ------------------------------ | -------- | -------------- | ------- |
| `value.id`                     | ❌       | ✅             | -       |
| `value.name`                   | ✅       | ❌             | -       |
| `value.level.id`               | ❌       | ✅             | -       |
| `value.level.config.*`         | ✅       | ❌             | -       |
| `value.level.config.id`        | ❌       | ✅             | -       |
| `value.level.config.createdAt` | ❌       | ✅             | -       |
| `value.level.config.updatedAt` | ❌       | ✅             | -       |
| `value.level.board`            | ✅       | ❌             | -       |
| `value.level.containers`       | ✅       | ❌             | -       |
| `value.level.difficultyScore`  | ✅       | ❌             | -       |
| `value.level.solvable`         | ✅       | ❌             | -       |
| `value.level.timestamp`        | ❌       | ✅             | -       |
| `value.createdAt`              | ❌       | ✅             | -       |
| `value.updatedAt`              | ❌       | ✅             | -       |
| `timestamp` (root)             | ❌       | ✅             | -       |

**Legend:**

- ✅ = Yes
- ❌ = No
- `-` = N/A
