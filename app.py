from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
import json

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


@app.post("/convert")
async def convert_image(
    file: UploadFile = File(..., description="Ảnh đầu vào (png/jpg/webp)"),
    cols: int = 30,
    rows: int = 30,
    # Cho phép override palette bằng JSON string trong multipart (tuỳ chọn)
    palette_override: str | None = Form(default=None),
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

    # Palette: dùng override nếu có, ngược lại dùng mặc định
    if palette_override:
        try:
            p = json.loads(palette_override)
            # chấp nhận key là string hoặc int
            palette = {int(k): str(v) for k, v in p.items()}
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"palette_override không hợp lệ: {e}"
            )
    else:
        palette = DEFAULT_PALETTE

    palette_rgb = build_palette_rgb(palette)

    # Resize về kích thước mong muốn
    img = img.resize((cols, rows), Image.NEAREST)

    # Tạo ma trận chỉ số theo palette
    matrix: list[list[int]] = []
    px = img.load()
    for y in range(rows):
        row = []
        for x in range(cols):
            rgb = px[x, y]
            idx = closest_palette_index(rgb, palette_rgb)
            row.append(idx)
        matrix.append(row)

    output = {
        "meta": {"cols": cols, "rows": rows, "palette": palette, "mode": "index"},
        "matrix": matrix,
    }
    return output
