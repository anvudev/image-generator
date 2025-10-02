"""
Database Routes
API endpoints cho MongoDB operations
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.utils.helpers import format_response
from .service import database_service
from .models import (
    HistoryLevelModel,
    ImageCreateRequest,
    ImageUpdateRequest,
    HistoryCreateRequest,
    HistoryUpdateRequest,
    HistoryItemCreateRequest,
    ImportCreateRequest,
)

router = APIRouter(prefix="/api", tags=["Database"])


# ==================== IMAGES ENDPOINTS ====================


@router.post("/images")
async def create_image(data: ImageCreateRequest):
    """
    Tạo mới image document

    Args:
        data: ImageCreateRequest

    Returns:
        Created image document
    """
    try:
        result = await database_service.create_image(data)
        return format_response(
            success=True, message="Image created successfully", data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images/{image_id}")
async def get_image(image_id: str):
    """
    Lấy image theo ID

    Args:
        image_id: ID của image

    Returns:
        Image document
    """
    result = await database_service.get_image(image_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return format_response(
        success=True, message="Image retrieved successfully", data=result
    )


@router.get("/images")
async def list_images(
    skip: int = Query(0, ge=0, description="Số documents bỏ qua"),
    limit: int = Query(10, ge=1, le=100, description="Số documents tối đa"),
    sort_by: str = Query("created_at", description="Field để sort"),
    sort_order: int = Query(-1, ge=-1, le=1, description="1 (asc) hoặc -1 (desc)"),
):
    """
    Lấy danh sách images với phân trang

    Returns:
        List of images
    """
    try:
        items = await database_service.list_images(skip, limit, sort_by, sort_order)
        total = await database_service.count_images()

        return format_response(
            success=True,
            message=f"Retrieved {len(items)} images",
            data={
                "items": items,
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "total": total,
                    "has_more": skip + limit < total,
                },
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/images/{image_id}")
async def update_image(image_id: str, data: ImageUpdateRequest):
    """
    Cập nhật image

    Args:
        image_id: ID của image
        data: ImageUpdateRequest

    Returns:
        Updated image document
    """
    result = await database_service.update_image(image_id, data)

    if result is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return format_response(
        success=True, message="Image updated successfully", data=result
    )


@router.delete("/images/{image_id}")
async def delete_image(image_id: str):
    """
    Xóa image

    Args:
        image_id: ID của image

    Returns:
        Success message
    """
    success = await database_service.delete_image(image_id)

    if not success:
        raise HTTPException(status_code=404, detail="Image not found")

    return format_response(success=True, message="Image deleted successfully")


# ==================== HISTORIES ENDPOINTS ====================


@router.post("/histories")
async def create_history(data: HistoryItemCreateRequest):
    """
    Tạo history record mới

    Request body phải chứa:
    - key: "history" (default)
    - value: HistoryValueModel với đầy đủ thông tin level
    """
    try:
        result = await database_service.create_history_item(data)
        return format_response(
            success=True, message="History created successfully", data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/histories")
async def list_histories(
    collection: Optional[str] = Query(None, description="Filter by collection"),
    document_id: Optional[str] = Query(None, description="Filter by document_id"),
    search: Optional[str] = Query(None, description="Search by name"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("updatedAt", description="Sort field: 'name' or 'updatedAt'"),
    sort_order: str = Query("desc", description="Sort order: 'asc' or 'desc'"),
):
    """
    Lấy danh sách histories với sorting và search

    - **search**: Tìm kiếm theo name (case-insensitive)
    - **sort_by**: Field để sort ('name' hoặc 'updatedAt')
    - **sort_order**: Thứ tự sort ('asc' hoặc 'desc')
    """
    try:
        # Validate sort parameters
        if sort_by not in ["name", "updatedAt"]:
            raise HTTPException(
                status_code=400, detail="sort_by must be 'name' or 'updatedAt'"
            )
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(
                status_code=400, detail="sort_order must be 'asc' or 'desc'"
            )

        items = await database_service.list_histories(
            collection, document_id, skip, limit, sort_by, sort_order, search
        )
        total = await database_service.count_histories(collection, document_id, search)

        message = f"Retrieved {len(items)} histories"
        if search:
            message = f"Found {len(items)} histories matching '{search}'"

        return format_response(
            success=True,
            message=message,
            data={
                "items": items,
                "pagination": {
                    "skip": skip,
                    "limit": limit,
                    "total": total,
                    "has_more": skip + limit < total,
                },
                "sort": {
                    "by": sort_by,
                    "order": sort_order,
                },
                "search": search,
            },
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/histories/{history_id}")
async def delete_history(history_id: str):
    """Xóa history"""
    success = await database_service.delete_history(history_id)
    if not success:
        raise HTTPException(status_code=404, detail="History not found")
    return format_response(success=True, message="History deleted successfully")


@router.put("/histories/{history_id}")
async def update_history(history_id: str, request: dict):
    """
    Cập nhật history level data

    Accept 2 formats:
    1. Direct level data: {board, config, containers, ...}
    2. Wrapped: {level: {board, config, containers, ...}}

    Request body: HistoryLevelModel hoặc {level: HistoryLevelModel}
    """
    try:
        # Check if data is wrapped in "level" key
        if "level" in request and "board" not in request:
            # Format 2: {level: {...}}
            level_data = request["level"]
        else:
            # Format 1: Direct data
            level_data = request

        # Validate with Pydantic
        validated_data = HistoryLevelModel(**level_data)

        result = await database_service.update_history(history_id, validated_data)
        if result is None:
            raise HTTPException(status_code=404, detail="History not found")
        return format_response(
            success=True, message="History level updated successfully", data=result
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/histories/{history_id}/name")
async def update_history_name(history_id: str, request: dict):
    """
    Cập nhật tên history item.value.name

    Request body:
    {
        "name": "New Name"
    }
    """
    name = request.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="Field 'name' is required")

    result = await database_service.update_history_name(history_id, name)
    if result is None:
        raise HTTPException(status_code=404, detail="History not found")
    return format_response(
        success=True, message="History name updated successfully", data=result
    )


# ==================== IMPORTS ENDPOINTS ====================


@router.post("/imports")
async def create_import(data: ImportCreateRequest):
    """Tạo import record"""
    try:
        result = await database_service.create_import(data)
        return format_response(
            success=True, message="Import created successfully", data=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/imports/{import_id}")
async def get_import(import_id: str):
    """Lấy import theo ID"""
    result = await database_service.get_import(import_id)

    if result is None:
        raise HTTPException(status_code=404, detail="Import not found")

    return format_response(
        success=True, message="Import retrieved successfully", data=result
    )


@router.put("/imports/{import_id}/status")
async def update_import_status(
    import_id: str,
    status: str,
    processed_items: Optional[int] = None,
    failed_items: Optional[int] = None,
    error_message: Optional[str] = None,
):
    """Cập nhật trạng thái import"""
    result = await database_service.update_import_status(
        import_id, status, processed_items, failed_items, error_message
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Import not found")

    return format_response(
        success=True, message="Import status updated successfully", data=result
    )


@router.get("/imports")
async def list_imports(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)
):
    """Lấy danh sách imports"""
    try:
        items = await database_service.list_imports(skip, limit)
        return format_response(
            success=True,
            message=f"Retrieved {len(items)} imports",
            data={"items": items},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
