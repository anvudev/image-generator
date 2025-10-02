"""
Database Models
Pydantic models cho MongoDB collections
"""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class ImageModel(BaseModel):
    """Model cho collection 'images'"""

    name: str = Field(..., description="Tên ảnh")
    url: Optional[str] = Field(None, description="URL ảnh gốc")
    matrix: list[list[int]] = Field(..., description="Ma trận pixel")
    palette: dict[int, str] = Field(..., description="Bảng màu sử dụng")
    cols: int = Field(..., description="Số cột")
    rows: int = Field(..., description="Số hàng")
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Metadata bổ sung"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "my_image.png",
                "url": "https://example.com/image.png",
                "matrix": [[1, 2], [3, 4]],
                "palette": {"1": "#ff0000", "2": "#0000ff"},
                "cols": 2,
                "rows": 2,
                "metadata": {"author": "user123"},
            }
        }


# Nested models for History/Level structure
class CellModel(BaseModel):
    """Model cho một ô trên board"""

    type: str = Field(..., description="Loại ô (wall/empty/block)")
    color: Optional[str] = Field(None, description="Màu của block")
    element: Optional[str] = Field(
        None, description="Element đặc biệt (Pipe/Barrel/Ice/Bomb)"
    )


class ContainerContentModel(BaseModel):
    """Model cho nội dung trong container"""

    color: str = Field(..., description="Màu của block")
    type: str = Field(..., description="Loại (block)")


class ContainerModel(BaseModel):
    """Model cho container"""

    id: str = Field(..., description="Container ID")
    slots: int = Field(..., description="Số slot")
    contents: list[ContainerContentModel] = Field(
        default_factory=list, description="Nội dung"
    )


class PipeInfoModel(BaseModel):
    """Model cho thông tin pipe"""

    id: str = Field(..., description="Pipe ID")
    contents: list[str] = Field(..., description="Màu trong pipe")
    direction: str = Field(..., description="Hướng (left/right/up/down)")
    position: dict[str, int] = Field(..., description="Vị trí {x, y}")


class LevelConfigModel(BaseModel):
    """Model cho config của level"""

    name: str = Field(..., description="Tên level")
    width: int = Field(..., description="Chiều rộng board")
    height: int = Field(..., description="Chiều cao board")
    blockCount: int = Field(..., description="Số lượng block")
    colorCount: int = Field(..., description="Số lượng màu")
    selectedColors: list[str] = Field(..., description="Các màu được chọn")
    colorMapping: dict[str, str] = Field(..., description="Mapping màu ID -> hex")
    generationMode: str = Field(..., description="Chế độ gen (symmetric/random)")
    elements: dict[str, int] = Field(
        default_factory=dict, description="Các element đặc biệt"
    )
    difficulty: str = Field(..., description="Độ khó (Easy/Medium/Hard)")
    pipeCount: int = Field(default=0, description="Số lượng pipe")
    pipeBlockCounts: list[int] = Field(
        default_factory=list, description="Số block mỗi pipe"
    )
    iceCounts: list[int] = Field(default_factory=list, description="Số lượng ice")
    bombCounts: list[int] = Field(default_factory=list, description="Số lượng bomb")
    id: Optional[str] = Field(None, description="Config ID (auto-generated)")
    status: str = Field(default="pending", description="Trạng thái")
    createdAt: Optional[str] = Field(None, description="Thời gian tạo (auto-generated)")
    updatedAt: Optional[str] = Field(
        None, description="Thời gian cập nhật (auto-generated)"
    )


class LevelModel(BaseModel):
    """Model cho level data"""

    id: Optional[str] = Field(None, description="Level ID (auto-generated)")
    config: LevelConfigModel = Field(..., description="Cấu hình level")
    board: list[list[CellModel]] = Field(..., description="Board game 2D")
    containers: list[ContainerModel] = Field(..., description="Các container")
    difficultyScore: int = Field(..., description="Điểm độ khó")
    solvable: bool = Field(..., description="Level có giải được không")
    timestamp: Optional[str] = Field(None, description="Timestamp (auto-generated)")
    pipeInfo: Optional[list[PipeInfoModel]] = Field(None, description="Thông tin pipes")
    lockInfo: Optional[Any] = Field(None, description="Thông tin lock")


class HistoryValueModel(BaseModel):
    """Model cho value trong history"""

    id: Optional[str] = Field(None, description="History value ID (auto-generated)")
    name: str = Field(..., description="Tên level")
    level: LevelModel = Field(..., description="Dữ liệu level")
    createdAt: Optional[str] = Field(None, description="Thời gian tạo (auto-generated)")
    updatedAt: Optional[str] = Field(
        None, description="Thời gian cập nhật (auto-generated)"
    )


class HistoryLevelModel(BaseModel):
    """Model cho level trong history"""

    board: list[list[CellModel]] = Field(..., description="Board game 2D")
    config: LevelConfigModel = Field(..., description="Cấu hình level")
    containers: list[ContainerModel] = Field(..., description="Các container")
    difficultyScore: int = Field(..., description="Điểm độ khó")
    id: Optional[str] = Field(None, description="Level ID (auto-generated)")
    lockInfo: Optional[Any] = Field(None, description="Thông tin lock")
    solvable: bool = Field(..., description="Level có giải được không")
    timestamp: Optional[str] = Field(None, description="Timestamp (auto-generated)")
    pipeInfo: Optional[list[PipeInfoModel]] = Field(None, description="Thông tin pipes")


class HistoryModel(BaseModel):
    """Model cho collection 'histories'"""

    key: str = Field(..., description="Key (thường là 'history')")
    value: HistoryValueModel = Field(..., description="Dữ liệu history")
    updatedAt: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    class Config:
        json_schema_extra = {
            "example": {
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
                            "selectedColors": ["1", "2", "3"],
                            "colorMapping": {"1": "#ff0000", "2": "#0000ff"},
                            "generationMode": "symmetric",
                            "elements": {"Pipe": 2},
                            "difficulty": "Hard",
                            "pipeCount": 2,
                            "pipeBlockCounts": [6, 6],
                            "iceCounts": [2],
                            "bombCounts": [2],
                            "id": "import-1758771908607-13",
                            "status": "pending",
                            "createdAt": "2025-09-25T03:45:08.607Z",
                            "updatedAt": "2025-09-25T03:45:08.607Z",
                        },
                        "board": [[{"type": "wall", "color": None, "element": None}]],
                        "containers": [],
                        "difficultyScore": 117,
                        "solvable": True,
                        "timestamp": "2025-09-25T04:59:07.816000",
                        "pipeInfo": [],
                        "lockInfo": None,
                    },
                    "createdAt": "2025-09-25T04:59:57.330Z",
                    "updatedAt": "2025-09-25T04:59:57.330Z",
                },
                "updatedAt": "2025-09-25T04:59:57.333000",
            }
        }


class ImportModel(BaseModel):
    """Model cho collection 'imports'"""

    source: str = Field(..., description="Nguồn import (file/url/api)")
    status: str = Field(
        ..., description="Trạng thái (pending/processing/completed/failed)"
    )
    total_items: int = Field(default=0, description="Tổng số items")
    processed_items: int = Field(default=0, description="Số items đã xử lý")
    failed_items: int = Field(default=0, description="Số items thất bại")
    error_message: Optional[str] = Field(None, description="Thông báo lỗi")
    started_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: Optional[str] = Field(None, description="Thời gian hoàn thành")
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Metadata bổ sung"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "source": "file_upload",
                "status": "completed",
                "total_items": 100,
                "processed_items": 95,
                "failed_items": 5,
                "started_at": "2024-01-01T00:00:00",
                "completed_at": "2024-01-01T00:10:00",
            }
        }


class ImageCreateRequest(BaseModel):
    """Request model cho tạo image"""

    name: str
    url: Optional[str] = None
    matrix: list[list[int]]
    palette: dict[int, str]
    cols: int
    rows: int
    metadata: Optional[dict[str, Any]] = None


class ImageUpdateRequest(BaseModel):
    """Request model cho update image"""

    name: Optional[str] = None
    url: Optional[str] = None
    matrix: Optional[list[list[int]]] = None
    palette: Optional[dict[int, str]] = None
    cols: Optional[int] = None
    rows: Optional[int] = None
    metadata: Optional[dict[str, Any]] = None


class HistoryCreateRequest(BaseModel):
    """Request model cho tạo history"""

    value: HistoryValueModel


class HistoryUpdateRequest(BaseModel):
    """Request model cho update history"""

    key: Optional[str] = None
    value: Optional[HistoryValueModel] = None


class HistoryItemCreateRequest(BaseModel):
    """Request model cho tạo history item (simplified)"""

    key: str = "history"
    value: HistoryValueModel


class ImportCreateRequest(BaseModel):
    """Request model cho tạo import"""

    source: str
    total_items: int = 0
    metadata: Optional[dict[str, Any]] = None
