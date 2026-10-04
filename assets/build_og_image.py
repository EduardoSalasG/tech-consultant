from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
S = 2  # supersampling for crisp text/edges
INK = (16, 35, 63)
BLUE = (23, 79, 138)
BLUE_STRONG = (16, 60, 106)
PALE = (185, 213, 244)
SOFT = (207, 221, 237)
WHITE = (255, 255, 255)

FONT_DIRS = [r"C:\Windows\Fonts", "/usr/share/fonts", "/System/Library/Fonts"]

def font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

f_brand = font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 26 * S)
f_head = font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 78 * S)
f_badge = font(["segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"], 40 * S)
f_node = font(["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"], 26 * S)

im = Image.new("RGB", (W * S, H * S), INK)
d = ImageDraw.Draw(im)

# subtle grid backdrop
grid = (30, 55, 90)
for x in range(0, W * S, 90 * S):
    d.line([(x, 0), (x, H * S)], fill=grid, width=S)
for y in range(0, H * S, 90 * S):
    d.line([(0, y), (W * S, y)], fill=grid, width=S)

left = 96 * S

# ES badge
bx, by, bs = left, 84 * S, 92 * S
d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=22 * S, fill=WHITE)
t = d.textbbox((0, 0), "ES", font=f_badge)
d.text((bx + (bs - (t[2] - t[0])) / 2 - t[0], by + (bs - (t[3] - t[1])) / 2 - t[1]),
       "ES", font=f_badge, fill=INK)
d.text((bx + bs + 28 * S, by + bs / 2), "ES TECH SERVICES", font=f_brand,
       fill=PALE, anchor="lm", spacing=0)
# letterspacing workaround: draw char by char
brand = "ES TECH SERVICES"
d.rectangle([bx + bs + 28 * S, by - 20 * S, bx + bs + 700 * S, by + bs + 20 * S], fill=INK)
d.line([(bx + bs + 28 * S, by - 20 * S), (bx + bs + 28 * S, by + bs + 20 * S)], fill=grid, width=S)
cx = bx + bs + 28 * S
for ch in brand:
    d.text((cx, by + bs / 2), ch, font=f_brand, fill=PALE, anchor="lm")
    cx += d.textlength(ch, font=f_brand) + 8 * S

# headline
d.text((left, 250 * S), "Tecnología para", font=f_head, fill=WHITE)
d.text((left, 340 * S), "operar mejor.", font=f_head, fill=WHITE)

# roadmap line with 4 nodes
cy = 500 * S
x0, x1 = left + 20 * S, W * S - 120 * S
step = (x1 - x0) // 3
nodes = ["Entender", "Ordenar", "Priorizar", "Medir"]
for i in range(4):
    x = x0 + i * step
    if i < 3:
        d.line([(x + 14 * S, cy), (x + step - 14 * S, cy)], fill=BLUE, width=5 * S)
    d.ellipse([x - 30 * S, cy - 30 * S, x + 30 * S, cy + 30 * S], outline=BLUE, width=3 * S)
    d.ellipse([x - 16 * S, cy - 16 * S, x + 16 * S, cy + 16 * S], fill=WHITE)
    d.text((x, cy + 58 * S), f"0{i+1} · {nodes[i]}", font=f_node, fill=SOFT, anchor="mm")

im = im.resize((W, H), Image.LANCZOS)
out = os.path.join(os.path.dirname(__file__), "og-es-tech-services.png")
im.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
