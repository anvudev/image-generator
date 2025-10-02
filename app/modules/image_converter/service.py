"""
Image Converter Service
Business logic cho việc chuyển đổi ảnh
"""
from PIL import Image
from io import BytesIO
from typing import Optional

from app.config import settings
from .utils import build_palette_rgb, closest_palette_index, validate_image_file


class ImageConverterService:
    """Service xử lý chuyển đổi ảnh thành pixel art"""
    
    def __init__(self):
        self.default_palette = settings.default_palette
    
    def validate_file(self, content_type: str, file_size: int) -> tuple[bool, str]:
        """
        Validate file upload
        
        Args:
            content_type: MIME type
            file_size: Kích thước file
        
        Returns:
            Tuple (is_valid, error_message)
        """
        return validate_image_file(
            content_type,
            file_size,
            settings.max_image_size
        )
    
    def convert_image(
        self,
        image_data: bytes,
        cols: int,
        rows: int,
        palette: Optional[dict[int, str]] = None
    ) -> dict:
        """
        Chuyển đổi ảnh thành pixel art matrix
        
        Args:
            image_data: Dữ liệu ảnh (bytes)
            cols: Số cột
            rows: Số hàng
            palette: Palette tùy chỉnh (optional, mặc định dùng default_palette)
        
        Returns:
            Dictionary chứa matrix và metadata
        
        Raises:
            ValueError: Nếu không đọc được ảnh
        """
        # Sử dụng palette mặc định nếu không có palette tùy chỉnh
        if palette is None:
            palette = self.default_palette
        
        # Đọc ảnh
        try:
            img = Image.open(BytesIO(image_data)).convert("RGB")
        except Exception as e:
            raise ValueError(f"Không đọc được ảnh: {e}")
        
        # Chuyển đổi palette sang RGB
        palette_rgb = build_palette_rgb(palette)
        
        # Resize ảnh về kích thước mong muốn
        img = img.resize((cols, rows), Image.NEAREST)
        
        # Tạo matrix và thu thập màu thực sự được sử dụng
        matrix: list[list[int]] = []
        used_colors = set()
        pixels = img.load()
        
        for y in range(rows):
            row = []
            for x in range(cols):
                rgb = pixels[x, y]
                idx = closest_palette_index(rgb, palette_rgb)
                row.append(idx)
                used_colors.add(idx)
            matrix.append(row)
        
        # Chỉ trả về các màu thực sự có trong ảnh
        actual_palette = {idx: palette[idx] for idx in used_colors}
        
        return {
            "meta": {
                "cols": cols,
                "rows": rows,
                "palette": actual_palette,
                "mode": "index",
            },
            "matrix": matrix,
        }
    
    def get_palette(self) -> dict:
        """
        Lấy palette mặc định
        
        Returns:
            Dictionary chứa palette và description
        """
        return {
            "palette": self.default_palette,
            "description": "Bảng màu mặc định được sử dụng để chuyển đổi ảnh",
        }


# Singleton instance
image_converter_service = ImageConverterService()

