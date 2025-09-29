from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO

app = FastAPI(title="Pixel Palette API", version="1.0.0")

# CORS (nếu gọi từ frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nhớ chỉnh domain thật nếu cần
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Palette mặc định (theo bạn)
DEFAULT_PALETTE = {
    1: "#ff0000",  # Red
    2: "#0000ff",  # Blue
    3: "#00ff00",  # Green
    4: "#ffff00",  # Yellow
    5: "#ff9900",  # Orange
    6: "#9900ff",  # Purple
    7: "#ff00ff",  # Pink
    8: "#00ffff",  # Cyan
    9: "#4a86e8",  # Light Blue
    10: "#876670",  # Brown
    11: "#b7b7b7",  # Grey
    12: "#ffffff",  # White
}


def hex_to_rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def build_palette_rgb(palette: dict[int, str]):
    return {int(k): hex_to_rgb(v) for k, v in palette.items()}


def closest_palette_index(rgb, palette_rgb):
    r, g, b = rgb
    best_idx = None
    best_d = 1e18
    # so sánh bình phương khoảng cách (không cần sqrt cho nhanh)
    for idx, (pr, pg, pb) in palette_rgb.items():
        d = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if d < best_d:
            best_d = d
            best_idx = idx
    return best_idx


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/palette")
def get_palette():
    """Trả về danh sách palette mặc định"""
    return {
        "palette": DEFAULT_PALETTE,
        "description": "Bảng màu mặc định được sử dụng để chuyển đổi ảnh",
    }


@app.post("/convert")
async def convert_image(
    file: UploadFile = File(..., description="Ảnh đầu vào (png/jpg/webp)"),
    cols: int = 30,
    rows: int = 30,
):
    # kiểm tra định dạng
    if file.content_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise HTTPException(status_code=415, detail="Chỉ hỗ trợ PNG/JPEG/WebP")

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(status_code=400, detail="File rỗng")

    try:
        img = Image.open(BytesIO(data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Không đọc được ảnh: {e}")

    # Sử dụng palette mặc định
    palette_rgb = build_palette_rgb(DEFAULT_PALETTE)

    # Resize về kích thước mong muốn
    img = img.resize((cols, rows), Image.NEAREST)

    # Tạo ma trận chỉ số theo palette và thu thập các màu thực sự được sử dụng
    matrix: list[list[int]] = []
    used_colors = set()  # Lưu các chỉ số màu thực sự được sử dụng
    px = img.load()

    for y in range(rows):
        row = []
        for x in range(cols):
            rgb = px[x, y]
            idx = closest_palette_index(rgb, palette_rgb)
            row.append(idx)
            used_colors.add(idx)  # Thêm vào set các màu đã dùng
        matrix.append(row)

    # Chỉ trả về các màu thực sự có trong ảnh
    actual_palette = {idx: DEFAULT_PALETTE[idx] for idx in used_colors}

    output = {
        "meta": {
            "cols": cols,
            "rows": rows,
            "palette": actual_palette,
            "mode": "index",
        },
        "matrix": matrix,
    }
    return output
