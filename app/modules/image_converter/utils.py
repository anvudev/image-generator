"""
Image Converter Utilities
"""
from app.utils.helpers import hex_to_rgb


def build_palette_rgb(palette: dict[int, str]) -> dict[int, tuple[int, int, int]]:
    """
    Chuyển đổi palette từ hex sang RGB
    
    Args:
        palette: Dictionary {index: hex_color}
    
    Returns:
        Dictionary {index: (r, g, b)}
    """
    return {int(k): hex_to_rgb(v) for k, v in palette.items()}


def closest_palette_index(
    rgb: tuple[int, int, int],
    palette_rgb: dict[int, tuple[int, int, int]]
) -> int:
    """
    Tìm màu gần nhất trong palette với màu RGB cho trước
    
    Args:
        rgb: Tuple (R, G, B)
        palette_rgb: Dictionary {index: (r, g, b)}
    
    Returns:
        Index của màu gần nhất
    """
    r, g, b = rgb
    best_idx = None
    best_distance = float('inf')
    
    # Sử dụng bình phương khoảng cách Euclidean (không cần sqrt cho nhanh)
    for idx, (pr, pg, pb) in palette_rgb.items():
        distance = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if distance < best_distance:
            best_distance = distance
            best_idx = idx
    
    return best_idx


def validate_image_file(content_type: str, file_size: int, max_size: int) -> tuple[bool, str]:
    """
    Validate file ảnh
    
    Args:
        content_type: MIME type của file
        file_size: Kích thước file (bytes)
        max_size: Kích thước tối đa cho phép (bytes)
    
    Returns:
        Tuple (is_valid, error_message)
    """
    allowed_types = ["image/png", "image/jpeg", "image/webp"]
    
    if content_type not in allowed_types:
        return False, f"Chỉ hỗ trợ {', '.join(allowed_types)}"
    
    if file_size == 0:
        return False, "File rỗng"
    
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File quá lớn (tối đa {max_mb}MB)"
    
    return True, ""

