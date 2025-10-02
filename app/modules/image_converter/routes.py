"""
Image Converter Routes
API endpoints cho chuyển đổi ảnh
"""
from fastapi import APIRouter, UploadFile, File, HTTPException

from .service import image_converter_service

router = APIRouter(prefix="/image", tags=["Image Converter"])


@router.get("/palette")
async def get_palette():
    """
    Lấy thông tin palette mặc định
    
    Returns:
        Dictionary chứa palette và description
    """
    return image_converter_service.get_palette()


@router.post("/convert")
async def convert_image(
    file: UploadFile = File(..., description="Ảnh đầu vào (png/jpg/webp)"),
    cols: int = 30,
    rows: int = 30,
):
    """
    Chuyển đổi ảnh thành pixel art matrix
    
    Args:
        file: File ảnh upload
        cols: Số cột (mặc định 30)
        rows: Số hàng (mặc định 30)
    
    Returns:
        Dictionary chứa matrix và metadata
    
    Raises:
        HTTPException: Nếu file không hợp lệ hoặc xử lý lỗi
    """
    # Đọc dữ liệu file
    data = await file.read()
    
    # Validate file
    is_valid, error_msg = image_converter_service.validate_file(
        file.content_type,
        len(data)
    )
    
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Chuyển đổi ảnh
    try:
        result = image_converter_service.convert_image(data, cols, rows)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý ảnh: {e}")

