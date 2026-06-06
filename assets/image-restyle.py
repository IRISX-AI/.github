from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageFilter

SCRIPT_DIR = Path(__file__).resolve().parent

def resolve_path(path):
    p = Path(path)
    return p if p.is_absolute() else SCRIPT_DIR / p

def create_glowing_logo(input_path, output_path):
    input_path = resolve_path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # 1. Open image and crop it to a perfect square
    img = Image.open(input_path).convert("RGBA")
    size = min(img.size)
    img = img.crop(((img.width - size) // 2, (img.height - size) // 2, 
                    (img.width + size) // 2, (img.height + size) // 2))
    img = img.resize((400, 400), Image.Resampling.LANCZOS)  

    # 2. Create a circular mask
    mask = Image.new("L", (400, 400), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((10, 10, 390, 390), fill=255)

    # 3. Apply the mask to make the image circular
    circular_img = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    circular_img.paste(img, (0, 0), mask=mask)

    # 4. Create the background glow (Cyan: #06B6D4)
    glow_canvas = Image.new("RGBA", (460, 460), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_canvas)
    glow_draw.ellipse((20, 20, 440, 440), fill=(6, 182, 212, 150))
    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(15))

    # 5. Paste the circular image onto the glow and draw a solid border
    glow_canvas.paste(circular_img, (30, 30), mask=circular_img)
    final_draw = ImageDraw.Draw(glow_canvas)
    final_draw.ellipse((30, 30, 430, 430), outline=(6, 182, 212, 255), width=6)

    # 6. Save as a transparent PNG
    output_path = resolve_path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    glow_canvas.save(output_path, format="PNG")
    print(f"✅ Success! Saved as {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a glowing logo from an input image.")
    parser.add_argument("input", nargs="?", default="icon.jpg", help="Input image file path")
    parser.add_argument("output", nargs="?", default="icon_glowing.png", help="Output PNG file path")
    args = parser.parse_args()
    create_glowing_logo(args.input, args.output)