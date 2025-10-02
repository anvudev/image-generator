"""
Test History Model
Kiểm tra xem model có parse đúng dữ liệu không
"""
import json
from app.modules.database.models import (
    HistoryModel,
    HistoryValueModel,
    LevelModel,
    LevelConfigModel,
    CellModel,
    ContainerModel,
    ContainerContentModel,
    PipeInfoModel
)


def test_history_model():
    """Test parsing history data"""
    
    # Sample data từ MongoDB
    sample_data = {
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
                        "3": "#00ff00",
                        "4": "#ffff00",
                        "5": "#ff9900",
                        "6": "#9900ff",
                        "7": "#ff00ff",
                        "8": "#00ffff"
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
                        {"type": "wall", "color": None, "element": None},
                        {"type": "block", "color": "1", "element": "Barrel"},
                        {"type": "empty", "color": None, "element": None}
                    ],
                    [
                        {"type": "block", "color": "2", "element": None},
                        {"type": "block", "color": "3", "element": "Pipe"},
                        {"type": "wall", "color": None, "element": None}
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
                    },
                    {
                        "id": "container_1",
                        "slots": 4,
                        "contents": []
                    }
                ],
                "difficultyScore": 117,
                "solvable": True,
                "timestamp": "2025-09-25T04:59:07.816000",
                "pipeInfo": [
                    {
                        "id": "pipe1",
                        "contents": ["5", "8", "4", "3", "3", "8"],
                        "direction": "right",
                        "position": {"x": 4, "y": 6}
                    },
                    {
                        "id": "pipe2",
                        "contents": ["8", "1", "7", "6", "1", "8"],
                        "direction": "left",
                        "position": {"x": 4, "y": 8}
                    }
                ],
                "lockInfo": None
            },
            "createdAt": "2025-09-25T04:59:57.330Z",
            "updatedAt": "2025-09-25T04:59:57.330Z"
        },
        "updatedAt": "2025-09-25T04:59:57.333000"
    }
    
    try:
        # Parse data với Pydantic model
        history = HistoryModel(**sample_data)
        
        print("✅ History Model parsed successfully!")
        print(f"\n📊 History Info:")
        print(f"  - Key: {history.key}")
        print(f"  - Level ID: {history.value.id}")
        print(f"  - Level Name: {history.value.name}")
        print(f"  - Updated At: {history.updatedAt}")
        
        print(f"\n🎮 Level Info:")
        print(f"  - ID: {history.value.level.id}")
        print(f"  - Width x Height: {history.value.level.config.width} x {history.value.level.config.height}")
        print(f"  - Block Count: {history.value.level.config.blockCount}")
        print(f"  - Color Count: {history.value.level.config.colorCount}")
        print(f"  - Difficulty: {history.value.level.config.difficulty}")
        print(f"  - Difficulty Score: {history.value.level.difficultyScore}")
        print(f"  - Solvable: {history.value.level.solvable}")
        
        print(f"\n🎨 Colors:")
        for color_id, color_hex in history.value.level.config.colorMapping.items():
            print(f"  - {color_id}: {color_hex}")
        
        print(f"\n🧩 Elements:")
        for element, count in history.value.level.config.elements.items():
            print(f"  - {element}: {count}")
        
        print(f"\n📦 Containers: {len(history.value.level.containers)}")
        for container in history.value.level.containers:
            print(f"  - {container.id}: {len(container.contents)}/{container.slots} blocks")
        
        print(f"\n🔧 Pipes: {len(history.value.level.pipeInfo or [])}")
        if history.value.level.pipeInfo:
            for pipe in history.value.level.pipeInfo:
                print(f"  - {pipe.id}: {len(pipe.contents)} blocks, direction={pipe.direction}, pos=({pipe.position['x']}, {pipe.position['y']})")
        
        print(f"\n🎯 Board: {len(history.value.level.board)} rows")
        for i, row in enumerate(history.value.level.board):
            print(f"  - Row {i}: {len(row)} cells")
            for j, cell in enumerate(row):
                if cell.type == "block":
                    element_str = f" ({cell.element})" if cell.element else ""
                    print(f"    - [{i},{j}]: {cell.type} color={cell.color}{element_str}")
        
        # Convert back to dict
        history_dict = history.model_dump()
        print(f"\n✅ Model can be converted back to dict")
        print(f"   Keys: {list(history_dict.keys())}")
        
        # Convert to JSON
        history_json = history.model_dump_json(indent=2)
        print(f"\n✅ Model can be converted to JSON")
        print(f"   JSON length: {len(history_json)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error parsing history model: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Testing History Model...\n")
    success = test_history_model()
    
    if success:
        print("\n" + "="*60)
        print("🎉 All tests passed!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ Tests failed!")
        print("="*60)
        exit(1)

