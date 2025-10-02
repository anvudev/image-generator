"""
Common helper functions
"""

from typing import Any, Optional
from datetime import datetime
from fastapi import HTTPException


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """
    Chuyển đổi mã màu hex sang RGB

    Args:
        hex_color: Mã màu hex (ví dụ: "#ff0000" hoặc "ff0000")

    Returns:
        Tuple (R, G, B) với giá trị từ 0-255
    """
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Chuyển đổi RGB sang mã màu hex

    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)

    Returns:
        Mã màu hex (ví dụ: "#ff0000")
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def format_response(
    success: bool = True,
    message: str = "",
    data: Optional[Any] = None,
    error: Optional[str] = None,
) -> dict:
    """
    Format chuẩn cho API response

    Args:
        success: Trạng thái thành công
        message: Thông báo
        data: Dữ liệu trả về
        error: Thông báo lỗi (nếu có)

    Returns:
        Dictionary với format chuẩn
    """
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if message:
        response["message"] = message

    if data is not None:
        response["data"] = data

    if error:
        response["error"] = error

    return response


def handle_error(
    status_code: int, message: str, detail: Optional[str] = None
) -> HTTPException:
    """
    Tạo HTTPException với format chuẩn

    Args:
        status_code: HTTP status code
        message: Thông báo lỗi chính
        detail: Chi tiết lỗi (optional)

    Returns:
        HTTPException
    """
    error_detail = {"message": message}
    if detail:
        error_detail["detail"] = detail

    return HTTPException(status_code=status_code, detail=error_detail)


def validate_object_id(object_id: str) -> bool:
    """
    Kiểm tra ObjectId của MongoDB có hợp lệ không

    Args:
        object_id: String cần kiểm tra

    Returns:
        True nếu hợp lệ, False nếu không
    """
    from bson import ObjectId
    from bson.errors import InvalidId

    try:
        ObjectId(object_id)
        return True
    except (InvalidId, TypeError):
        return False


def get_current_timestamp() -> str:
    """
    Lấy timestamp hiện tại theo format ISO

    Returns:
        Timestamp string
    """
    return datetime.utcnow().isoformat()


def paginate_results(items: list, page: int = 1, page_size: int = 10) -> dict:
    """
    Phân trang kết quả

    Args:
        items: Danh sách items
        page: Số trang (bắt đầu từ 1)
        page_size: Số items mỗi trang

    Returns:
        Dictionary với items và metadata phân trang
    """
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size

    return {
        "items": items[start:end],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": (total + page_size - 1) // page_size,
            "has_next": end < total,
            "has_prev": page > 1,
        },
    }


def parse_numeric_string(value: str) -> float:
    """
    Parse string thành số, fallback về 0 nếu không parse được

    Args:
        value: String cần parse

    Returns:
        Float value hoặc 0 nếu không parse được
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def sort_histories_by_name(histories: list[dict], order: str = "asc") -> list[dict]:
    """
    Sort histories theo name với numeric comparison

    Logic:
    - Nếu name là số (ví dụ: "4", "41", "51") → sort theo giá trị số
    - Nếu name là text → sort theo alphabet
    - Mixed: số trước, text sau (khi asc), text trước, số sau (khi desc)

    Args:
        histories: List of history documents
        order: "asc" hoặc "desc"

    Returns:
        Sorted list
    """

    def get_sort_key(history: dict) -> tuple:
        """
        Tạo sort key cho history
        Returns: (is_text, numeric_value, string_value)

        Với asc: (False, số, "") sẽ đứng trước (True, 0, "text")
        Với desc: reverse sẽ đảo ngược thứ tự
        """
        try:
            name = history.get("value", {}).get("name", "")

            # Try to parse as number
            try:
                numeric_value = float(name)
                # Nếu parse thành công, return (False, số, "")
                # False để số đứng trước text khi sort asc
                return (False, numeric_value, "")
            except (ValueError, TypeError):
                # Nếu không parse được, return (True, 0, string)
                # True để text đứng sau số khi sort asc
                return (True, 0, name.lower())
        except Exception:
            return (True, 0, "")

    # Sort
    sorted_histories = sorted(histories, key=get_sort_key, reverse=(order == "desc"))

    return sorted_histories
