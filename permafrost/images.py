from pathlib import Path
from PIL import Image

IMAGE_EXTS = [
    "jpg",
    "jpeg",
    "png"
]

MAX_WIDTH = 800
QUALITY = 84

def is_image(path: str) -> bool:
    ext = path.split(".")[-1]
    if ext in IMAGE_EXTS:
        return True
    return False

def optimize_image(image_path: str) -> str:
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    new_path = path.with_suffix(".webp")

    with Image.open(path) as img:
        # resize if wider than max_width
        if img.width > MAX_WIDTH:
            new_height = int(img.height * (MAX_WIDTH / img.width))
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)

        # ensure compatible mode
        if img.mode in ("RGBA", "LA"):
            img = img.convert("RGBA")
        elif img.mode == "P":
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        img.save(new_path, "WEBP", quality=QUALITY)

    return new_path.name
