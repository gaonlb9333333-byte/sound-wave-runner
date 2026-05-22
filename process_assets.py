"""
Sound Wave Runner — asset processor
Generates all sprites needed by index.html
"""
import sys, os
sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.12/site-packages'))

from PIL import Image
import numpy as np

SRC  = os.path.dirname(__file__) + "/Animacije"
DEST = os.path.dirname(__file__) + "/www/assets"
DEST2= os.path.dirname(__file__) + "/assets"

def color_dist_mask(arr, bg, threshold):
    """Return boolean mask where pixels are within threshold of bg color."""
    bg = np.array(bg, dtype=np.float32)
    diff = arr[:,:,:3].astype(np.float32) - bg
    dist = np.sqrt((diff**2).sum(axis=2))
    return dist < threshold

def remove_bg_colordist(img, bg, threshold, feather=4):
    """Remove background using color-distance flood from corners."""
    img = img.convert("RGBA")
    arr = np.array(img, dtype=np.uint8)
    h, w = arr.shape[:2]
    bg_arr = np.array(bg, dtype=np.float32)
    visited = np.zeros((h, w), bool)
    queue = []
    for sy, sx in [(0,0),(0,w-1),(h-1,0),(h-1,w-1),
                   (0,w//2),(h//2,0),(h-1,w//2),(h//2,w-1)]:
        if not visited[sy, sx]:
            visited[sy, sx] = True
            queue.append((sy, sx))
    head = 0
    while head < len(queue):
        y, x = queue[head]; head += 1
        arr[y, x, 3] = 0
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                px = arr[ny, nx, :3].astype(np.float32)
                dist = float(np.sqrt(((px - bg_arr)**2).sum()))
                if dist < threshold:
                    visited[ny, nx] = True
                    queue.append((ny, nx))
    return Image.fromarray(arr, "RGBA")

def remove_checkerboard(img, threshold=38):
    """Remove gray checkerboard (transparency representation in JPEG)."""
    img = img.convert("RGBA")
    data = np.array(img, dtype=np.int32)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    avg = (r + g + b) // 3
    sat = np.maximum(np.maximum(r,g),b) - np.minimum(np.minimum(r,g),b)
    is_gray = sat < 30
    is_light = (avg > 150) & (avg < 225)
    is_dark  = (avg > 95)  & (avg < 170)
    data[:,:,3] = np.where(is_gray & (is_light | is_dark), 0, data[:,:,3])
    return Image.fromarray(data.astype(np.uint8), "RGBA")

def crop_tight(img, pad=8):
    arr = np.array(img)
    alpha = arr[:,:,3]
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    if not rows.any() or not cols.any():
        return img
    r0, r1 = np.where(rows)[0][[0,-1]]
    c0, c1 = np.where(cols)[0][[0,-1]]
    h, w = arr.shape[:2]
    r0, r1 = max(0, r0-pad), min(h, r1+pad)
    c0, c1 = max(0, c0-pad), min(w, c1+pad)
    return img.crop((c0, r0, c1, r1))

# ═══════════════════════════════════════════════════════════════════
# A) cat_anim.png — 8-frame running spritesheet from MP4
# ═══════════════════════════════════════════════════════════════════
print("\n=== A) cat_anim.png ===")
mp4_path = f"{SRC}/kling_20260517_作品_cat_runnin_5586_0.mp4"
try:
    import av as pyav
    container = pyav.open(mp4_path)
    stream = container.streams.video[0]
    total_frames = stream.frames or 96
    print(f"  Video: {stream.width}x{stream.height}, ~{total_frames} frames")
    # Collect all frames
    all_frames = []
    for packet in container.demux(stream):
        for f in packet.decode():
            all_frames.append(f.to_image())
    container.close()
    n = len(all_frames)
    print(f"  Decoded {n} frames")
    # Pick 8 evenly spaced frames
    indices = [int(i * (n-1) / 7) for i in range(8)]
    frames = [all_frames[i] for i in indices]
    # Background color: dark purple ~(38,32,49)
    bg_color = (38, 32, 49)
    FRAME_SIZE = 128
    sprite_frames = []
    for i, frame in enumerate(frames):
        cleaned = remove_bg_colordist(frame, bg_color, threshold=55)
        # Crop tight then resize to 128x128
        cropped = crop_tight(cleaned, pad=4)
        resized = cropped.resize((FRAME_SIZE, FRAME_SIZE), Image.LANCZOS)
        sprite_frames.append(resized)
    # Check motion between frames
    arr0 = np.array(sprite_frames[0]).astype(float)
    arr1 = np.array(sprite_frames[1]).astype(float)
    mean_diff = float(np.abs(arr0 - arr1).mean())
    print(f"  Mean pixel diff frame0↔frame1: {mean_diff:.2f} (must be >15)")
    # Stitch into 1024x128 spritesheet
    sheet = Image.new("RGBA", (FRAME_SIZE * 8, FRAME_SIZE), (0,0,0,0))
    for i, f in enumerate(sprite_frames):
        sheet.paste(f, (i * FRAME_SIZE, 0))
    sheet.save(f"{DEST}/cat_anim.png")
    sheet.save(f"{DEST2}/cat_anim.png")
    print(f"  Saved cat_anim.png ({sheet.size})")
except Exception as e:
    print(f"  ERROR extracting frames: {e}")
    print("  Keeping existing cat_anim.png")

# ═══════════════════════════════════════════════════════════════════
# B) speed_lines.png — speed effect overlay
# ═══════════════════════════════════════════════════════════════════
print("\n=== B) speed_lines.png ===")
sl_path = f"{SRC}/Nemanja_Gajovic_2_Speed_lines__dash_effect_za_kad_maka_jako_skoi2D_game_d7d4e4ae-86ca-4a76-951a-621893687ab9.jpg"
img = Image.open(sl_path)
# bg is near-black (2,2,2) — use color distance
result = remove_bg_colordist(img, bg=(2,2,2), threshold=48)
result = result.resize((512, 512), Image.LANCZOS)
result.save(f"{DEST}/speed_lines.png")
result.save(f"{DEST2}/speed_lines.png")
alpha_mean = float(np.array(result)[:,:,3].mean())
print(f"  Saved speed_lines.png, alpha_mean={alpha_mean:.1f}")

# ═══════════════════════════════════════════════════════════════════
# C) crystal_a/b/c — obstacle crystal sprites (all from same source)
# ═══════════════════════════════════════════════════════════════════
print("\n=== C) Crystals ===")
crystal_src = f"{SRC}/v2_watermarked-fcdf0c4d-6de1-48d2-b344-cbb2abde53e2.jpg"
base_img = Image.open(crystal_src)
# Checkerboard bg removal
base = remove_checkerboard(base_img, threshold=42)
base = crop_tight(base, pad=6)
base = base.resize((80, 120), Image.LANCZOS)
base_arr = np.array(base).astype(np.float32)

def make_crystal(base_arr, r_mult, g_mult, b_mult, name):
    arr = base_arr.copy()
    arr[:,:,0] = np.clip(arr[:,:,0] * r_mult, 0, 255)
    arr[:,:,1] = np.clip(arr[:,:,1] * g_mult, 0, 255)
    arr[:,:,2] = np.clip(arr[:,:,2] * b_mult, 0, 255)
    img = Image.fromarray(arr.astype(np.uint8), "RGBA")
    img.save(f"{DEST}/{name}")
    img.save(f"{DEST2}/{name}")
    alpha_mean = float(np.array(img)[:,:,3].mean())
    print(f"  {name}: size={img.size}, alpha_mean={alpha_mean:.1f}")

# crystal_a: purple/blue — original
make_crystal(base_arr, 1.0, 0.6, 1.3, "crystal_a.png")
# crystal_b: pink/magenta
make_crystal(base_arr, 1.5, 0.3, 1.1, "crystal_b.png")
# crystal_c: cyan/teal
make_crystal(base_arr, 0.4, 1.4, 1.5, "crystal_c.png")

# ═══════════════════════════════════════════════════════════════════
# D) cat_jump.png, cat_idle.png, cat_land.png (update from Animacije/)
# ═══════════════════════════════════════════════════════════════════
print("\n=== D) Cat pose sprites ===")

# cat_jump — speed lines cat (bg near-black after checkerboard is gray in jpeg)
img = Image.open(f"{SRC}/Nemanja_Gajovic_2_Speed_lines__dash_effect_za_kad_maka_jako_skoi2D_game_d7d4e4ae-86ca-4a76-951a-621893687ab9.jpg")
result = remove_checkerboard(img, threshold=42)
result = crop_tight(result, pad=10)
result = result.resize((280, 280), Image.LANCZOS)
result.save(f"{DEST}/cat_jump.png"); result.save(f"{DEST2}/cat_jump.png")
print(f"  cat_jump.png: {result.size}")

# cat_idle — dead cat (dark bg ~10,12,30)
img = Image.open(f"{SRC}/openart-image_1779321048002_4af9adb2_1779321048017_8a81983f.png")
result = remove_bg_colordist(img, (10,12,30), threshold=35)
result = crop_tight(result, pad=12)
result = result.resize((280, 280), Image.LANCZOS)
result.save(f"{DEST}/cat_idle.png"); result.save(f"{DEST2}/cat_idle.png")
print(f"  cat_idle.png: {result.size}")

# cat_land — landing cat (dark bg ~15,12,25)
img = Image.open(f"{SRC}/gemini-2.5-flash-image_Jump_cat_leanding-0.jpg")
arr = np.array(img.convert("RGB"))
bg_sample = arr[0,0,:3]
print(f"  cat_land bg sample: {tuple(bg_sample)}")
result = remove_bg_colordist(img, tuple(bg_sample), threshold=32)
result = crop_tight(result, pad=12)
result = result.resize((280, 280), Image.LANCZOS)
result.save(f"{DEST}/cat_land.png"); result.save(f"{DEST2}/cat_land.png")
print(f"  cat_land.png: {result.size}")

print("\n=== All assets done ===")
