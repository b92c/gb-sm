#!/usr/bin/env python3
"""
Media and Assets Generator for Gracie Barra São Mateus
Generates:
1. assets/img/modalidade-feminina.jpg
2. assets/img/og-image.jpg
3. Favicons & Apple Touch Icons (in root and assets/img/)
4. Optimizes JPEGs (hero <= 200KB, cards <= 120KB, etc.)
5. Generates high-quality WebP versions for all visual assets
"""

import math
import os
import struct
import subprocess
import zlib

ROOT_DIR = "/Users/b92c/repos/gb-sm"
IMG_DIR = os.path.join(ROOT_DIR, "assets", "img")
SCRATCH_DIR = "/tmp/gb_assets_scratch"
os.makedirs(SCRATCH_DIR, exist_ok=True)

# -------------------------------------------------------------
# Font Definition (Clean Geometric Sans-Serif Vector Font)
# -------------------------------------------------------------
def get_font():
    return {
        'A': [(0, 16, 5, 0), (5, 0, 10, 16), (2, 10, 8, 10)],
        'B': [(0, 0, 0, 16), (0, 0, 7, 0), (7, 0, 10, 4), (10, 4, 7, 8), (0, 8, 7, 8), (7, 8, 10, 12), (10, 12, 7, 16), (7, 16, 0, 16)],
        'C': [(10, 3, 7, 0), (7, 0, 3, 0), (3, 0, 0, 3), (0, 3, 0, 13), (0, 13, 3, 16), (3, 16, 7, 16), (7, 16, 10, 13)],
        'D': [(0, 0, 0, 16), (0, 0, 6, 0), (6, 0, 10, 4), (10, 4, 10, 12), (10, 12, 6, 16), (6, 16, 0, 16)],
        'E': [(10, 0, 0, 0), (0, 0, 0, 16), (0, 16, 10, 16), (0, 8, 7, 8)],
        'F': [(10, 0, 0, 0), (0, 0, 0, 16), (0, 8, 7, 8)],
        'G': [(10, 3, 7, 0), (7, 0, 3, 0), (3, 0, 0, 3), (0, 3, 0, 13), (0, 13, 3, 16), (3, 16, 7, 16), (7, 16, 10, 13), (10, 13, 10, 8), (10, 8, 5, 8)],
        'H': [(0, 0, 0, 16), (10, 0, 10, 16), (0, 8, 10, 8)],
        'I': [(5, 0, 5, 16), (2, 0, 8, 0), (2, 16, 8, 16)],
        'J': [(1, 0, 9, 0), (6, 0, 6, 12), (6, 12, 4, 16), (4, 16, 0, 14)],
        'K': [(0, 0, 0, 16), (10, 0, 0, 9), (2, 7, 10, 16)],
        'L': [(0, 0, 0, 16), (0, 16, 9, 16)],
        'M': [(0, 16, 0, 0), (0, 0, 5, 8), (5, 8, 10, 0), (10, 0, 10, 16)],
        'N': [(0, 16, 0, 0), (0, 0, 10, 16), (10, 16, 10, 0)],
        'O': [(3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13), (0, 13, 0, 3), (0, 3, 3, 0)],
        'P': [(0, 0, 0, 16), (0, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 5), (10, 5, 7, 8), (7, 8, 0, 8)],
        'Q': [(3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13), (0, 13, 0, 3), (0, 3, 3, 0), (6, 12, 11, 17)],
        'R': [(0, 0, 0, 16), (0, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 5), (10, 5, 7, 8), (7, 8, 0, 8), (6, 8, 10, 16)],
        'S': [(10, 3, 7, 0), (7, 0, 3, 0), (3, 0, 0, 3), (0, 3, 2, 7), (2, 7, 8, 9), (8, 9, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13)],
        'T': [(0, 0, 10, 0), (5, 0, 5, 16)],
        'U': [(0, 0, 0, 13), (0, 13, 3, 16), (3, 16, 7, 16), (7, 16, 10, 13), (10, 13, 10, 0)],
        'V': [(0, 0, 5, 16), (5, 16, 10, 0)],
        'W': [(0, 0, 2, 16), (2, 16, 5, 6), (5, 6, 8, 16), (8, 16, 10, 0)],
        'X': [(0, 0, 10, 16), (10, 0, 0, 16)],
        'Y': [(0, 0, 5, 7), (10, 0, 5, 7), (5, 7, 5, 16)],
        'Z': [(0, 0, 10, 0), (10, 0, 0, 16), (0, 16, 10, 16)],
        'Ã': [(0, 16, 5, 0), (5, 0, 10, 16), (2, 10, 8, 10), (2, -3, 5, -5), (5, -5, 8, -3)],
        'Á': [(0, 16, 5, 0), (5, 0, 10, 16), (2, 10, 8, 10), (3, -2, 7, -5)],
        'É': [(10, 0, 0, 0), (0, 0, 0, 16), (0, 16, 10, 16), (0, 8, 7, 8), (3, -2, 7, -5)],
        'Í': [(5, 0, 5, 16), (2, 0, 8, 0), (2, 16, 8, 16), (3, -2, 7, -5)],
        'Ó': [(3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13), (0, 13, 0, 3), (0, 3, 3, 0), (3, -2, 7, -5)],
        'Ú': [(0, 0, 0, 13), (0, 13, 3, 16), (3, 16, 7, 16), (7, 16, 10, 13), (10, 13, 10, 0), (3, -2, 7, -5)],
        '-': [(2, 8, 8, 8)],
        '–': [(1, 8, 9, 8)],
        '·': [(4, 8, 6, 8)],
        '.': [(4, 15, 6, 15)],
        ',': [(4, 15, 6, 15), (6, 15, 3, 18)],
        ':': [(5, 4, 5, 5), (5, 11, 5, 12)],
        '/': [(1, 16, 9, 0)],
        '0': [(3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13), (0, 13, 0, 3), (0, 3, 3, 0), (8, 2, 2, 14)],
        '1': [(2, 3, 5, 0), (5, 0, 5, 16), (1, 16, 9, 16)],
        '2': [(1, 3, 4, 0), (4, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 6), (10, 6, 0, 16), (0, 16, 10, 16)],
        '3': [(0, 0, 10, 0), (10, 0, 5, 7), (5, 7, 8, 7), (8, 7, 10, 9), (10, 9, 10, 13), (10, 13, 7, 16), (7, 16, 1, 16)],
        '4': [(8, 16, 8, 0), (8, 0, 0, 10), (0, 10, 10, 10)],
        '5': [(10, 0, 0, 0), (0, 0, 0, 7), (0, 7, 7, 7), (7, 7, 10, 10), (10, 10, 10, 13), (10, 13, 7, 16), (7, 16, 0, 16)],
        '6': [(8, 2, 5, 0), (5, 0, 2, 0), (2, 0, 0, 4), (0, 4, 0, 13), (0, 13, 3, 16), (3, 16, 7, 16), (7, 16, 10, 13), (10, 13, 10, 9), (10, 9, 7, 7), (7, 7, 0, 7)],
        '7': [(0, 0, 10, 0), (10, 0, 3, 16)],
        '8': [(3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 8, 8), (8, 8, 10, 13), (10, 13, 7, 16), (7, 16, 3, 16), (3, 16, 0, 13), (0, 13, 2, 8), (2, 8, 0, 3), (0, 3, 3, 0), (2, 8, 8, 8)],
        '9': [(10, 9, 3, 9), (3, 9, 0, 7), (0, 7, 0, 3), (0, 3, 3, 0), (3, 0, 7, 0), (7, 0, 10, 3), (10, 3, 10, 12), (10, 12, 8, 16), (8, 16, 2, 16)],
        ' ': []
    }

FONT = get_font()

# -------------------------------------------------------------
# Drawing Helpers
# -------------------------------------------------------------
def dist_to_segment(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

def draw_line(buf, w, h, x1, y1, x2, y2, color, thickness):
    pad = int(math.ceil(thickness)) + 1
    min_x = max(0, int(min(x1, x2)) - pad)
    max_x = min(w - 1, int(max(x1, x2)) + pad)
    min_y = max(0, int(min(y1, y2)) - pad)
    max_y = min(h - 1, int(max(y1, y2)) + pad)
    
    r_target, g_target, b_target = color
    half_th = thickness / 2.0

    for y in range(min_y, max_y + 1):
        row_start = y * w * 3
        for x in range(min_x, max_x + 1):
            d = dist_to_segment(x + 0.5, y + 0.5, x1, y1, x2, y2)
            if d <= half_th:
                alpha = 1.0
            elif d < half_th + 1.0:
                alpha = 1.0 - (d - half_th)
            else:
                continue
            idx = row_start + x * 3
            cb = buf[idx]
            cg = buf[idx+1]
            cr = buf[idx+2]
            buf[idx] = int(cb * (1 - alpha) + b_target * alpha)
            buf[idx+1] = int(cg * (1 - alpha) + g_target * alpha)
            buf[idx+2] = int(cr * (1 - alpha) + r_target * alpha)

def get_text_width(text, size, letter_spacing=None):
    scale_x = (size / 16.0) * 0.65
    spacing = letter_spacing if letter_spacing is not None else size * 0.22
    total = 0
    for ch in text.upper():
        if ch == ' ':
            total += size * 0.4
        else:
            total += 10 * scale_x + spacing
    return total - spacing if total > 0 else 0

def draw_text(buf, w, h, text, x, y, size, color, thickness, letter_spacing=None):
    scale_y = size / 16.0
    scale_x = scale_y * 0.65
    spacing = letter_spacing if letter_spacing is not None else size * 0.22
    cur_x = x
    for ch in text.upper():
        if ch == ' ':
            cur_x += size * 0.4
            continue
        segs = FONT.get(ch, [])
        for (x1, y1, x2, y2) in segs:
            px1 = cur_x + x1 * scale_x
            py1 = y + y1 * scale_y
            px2 = cur_x + x2 * scale_x
            py2 = y + y2 * scale_y
            draw_line(buf, w, h, px1, py1, px2, py2, color, thickness)
        cur_x += 10 * scale_x + spacing

def draw_circle(buf, w, h, cx, cy, radius, color, thickness):
    half_th = thickness / 2.0
    r_target, g_target, b_target = color
    min_x = max(0, int(cx - radius - thickness - 2))
    max_x = min(w - 1, int(cx + radius + thickness + 2))
    min_y = max(0, int(cy - radius - thickness - 2))
    max_y = min(h - 1, int(cy + radius + thickness + 2))
    for y in range(min_y, max_y + 1):
        row_start = y * w * 3
        for x in range(min_x, max_x + 1):
            d = abs(math.hypot(x + 0.5 - cx, y + 0.5 - cy) - radius)
            if d <= half_th:
                alpha = 1.0
            elif d < half_th + 1.0:
                alpha = 1.0 - (d - half_th)
            else:
                continue
            idx = row_start + x * 3
            cb = buf[idx]
            cg = buf[idx+1]
            cr = buf[idx+2]
            buf[idx] = int(cb * (1 - alpha) + b_target * alpha)
            buf[idx+1] = int(cg * (1 - alpha) + g_target * alpha)
            buf[idx+2] = int(cr * (1 - alpha) + r_target * alpha)

def draw_filled_rounded_rect(buf, w, h, x1, y1, x2, y2, radius, color, alpha=1.0):
    r_target, g_target, b_target = color
    min_x = max(0, int(x1))
    max_x = min(w - 1, int(x2))
    min_y = max(0, int(y1))
    max_y = min(h - 1, int(y2))
    for y in range(min_y, max_y + 1):
        row_start = y * w * 3
        for x in range(min_x, max_x + 1):
            # check corner distance
            dx = 0
            dy = 0
            if x < x1 + radius:
                dx = (x1 + radius) - (x + 0.5)
            elif x > x2 - radius:
                dx = (x + 0.5) - (x2 - radius)
            if y < y1 + radius:
                dy = (y1 + radius) - (y + 0.5)
            elif y > y2 - radius:
                dy = (y + 0.5) - (y2 - radius)

            d = math.hypot(dx, dy)
            if d <= radius:
                a = alpha
            elif d < radius + 1.0:
                a = alpha * (1.0 - (d - radius))
            else:
                continue

            idx = row_start + x * 3
            cb = buf[idx]
            cg = buf[idx+1]
            cr = buf[idx+2]
            buf[idx] = int(cb * (1 - a) + b_target * a)
            buf[idx+1] = int(cg * (1 - a) + g_target * a)
            buf[idx+2] = int(cr * (1 - a) + r_target * a)

# -------------------------------------------------------------
# Image Loading & Compositing
# -------------------------------------------------------------
def load_png_rgba(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8
    idat = bytearray()
    w, h = 0, 0
    while pos < len(data):
        length, chunk_type = struct.unpack('>I4s', data[pos:pos+8])
        chunk_data = data[pos+8:pos+8+length]
        pos += 12 + length
        if chunk_type == b'IHDR':
            w, h, _, _ = struct.unpack('>IIBB', chunk_data[:10])
        elif chunk_type == b'IDAT':
            idat.extend(chunk_data)

    raw = zlib.decompress(idat)
    bpp = 4
    stride = 1 + w * bpp
    pixels = bytearray(w * h * bpp)
    prev_row = bytearray(w * bpp)
    for y in range(h):
        filter_type = raw[y * stride]
        row_data = raw[y * stride + 1 : (y + 1) * stride]
        curr_row = bytearray(w * bpp)
        for x in range(w * bpp):
            x_val = row_data[x]
            a = curr_row[x - bpp] if x >= bpp else 0
            b = prev_row[x]
            c = prev_row[x - bpp] if x >= bpp else 0
            if filter_type == 0: val = x_val
            elif filter_type == 1: val = (x_val + a) & 0xff
            elif filter_type == 2: val = (x_val + b) & 0xff
            elif filter_type == 3: val = (x_val + (a + b) // 2) & 0xff
            elif filter_type == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                val = (x_val + pr) & 0xff
            curr_row[x] = val
        pixels[y * w * bpp : (y + 1) * w * bpp] = curr_row
        prev_row = curr_row
    return w, h, pixels

def composite_rgba(dst_buf, dst_w, dst_h, src_rgba, src_w, src_h, dst_x, dst_y, global_alpha=1.0):
    for sy in range(src_h):
        dy = dst_y + sy
        if dy < 0 or dy >= dst_h:
            continue
        dst_row_start = dy * dst_w * 3
        src_row_start = sy * src_w * 4
        for sx in range(src_w):
            dx = dst_x + sx
            if dx < 0 or dx >= dst_w:
                continue
            s_idx = src_row_start + sx * 4
            sr = src_rgba[s_idx]
            sg = src_rgba[s_idx+1]
            sb = src_rgba[s_idx+2]
            sa = (src_rgba[s_idx+3] / 255.0) * global_alpha
            if sa <= 0.0:
                continue
            d_idx = dst_row_start + dx * 3
            cb = dst_buf[d_idx]
            cg = dst_buf[d_idx+1]
            cr = dst_buf[d_idx+2]
            dst_buf[d_idx] = int(cb * (1.0 - sa) + sb * sa)
            dst_buf[d_idx+1] = int(cg * (1.0 - sa) + sg * sa)
            dst_buf[d_idx+2] = int(cr * (1.0 - sa) + sr * sa)

def save_bmp(buf, w, h, filename):
    row_padded = (w * 3 + 3) & ~3
    pad = b'\x00' * (row_padded - w * 3)
    data = bytearray()
    for y in reversed(range(h)):
        data.extend(buf[y * w * 3 : (y + 1) * w * 3])
        data.extend(pad)
    file_size = 54 + len(data)
    header = struct.pack('<2sIHHI', b'BM', file_size, 0, 0, 54)
    dib = struct.pack('<IIIHHIIIIII', 40, w, h, 1, 24, 0, len(data), 2835, 2835, 0, 0)
    with open(filename, 'wb') as f:
        f.write(header + dib + data)

def convert_bmp_to_jpg(bmp_path, jpg_path, quality="high"):
    subprocess.run([
        'sips', '-s', 'format', 'jpeg',
        '-s', 'formatOptions', quality,
        bmp_path, '--out', jpg_path
    ], check=True, stdout=subprocess.DEVNULL)

# -------------------------------------------------------------
# 1. Generator: modalidade-feminina.jpg
# -------------------------------------------------------------
def generate_modalidade_feminina():
    print("Generating modalidade-feminina.jpg...")
    w, h = 800, 600
    buf = bytearray(w * h * 3)

    # Base background: Deep rich dark blue-slate #151925 with subtle vignette
    # Center (cx=400, cy=300)
    cx, cy = w / 2.0, h / 2.0
    max_dist = math.hypot(cx, cy)
    for y in range(h):
        row_start = y * w * 3
        for x in range(w):
            d = math.hypot(x - cx, y - cy) / max_dist
            # Interpolate from #181E2B (center) to #0A0D12 (edges)
            r = int(24 * (1 - d) + 10 * d)
            g = int(30 * (1 - d) + 13 * d)
            b = int(43 * (1 - d) + 18 * d)
            idx = row_start + x * 3
            buf[idx] = b
            buf[idx+1] = g
            buf[idx+2] = r

    # Elegant double-line card frame
    # Outer border
    draw_line(buf, w, h, 24, 24, w - 24, 24, (42, 49, 66), 1.5)
    draw_line(buf, w, h, w - 24, 24, w - 24, h - 24, (42, 49, 66), 1.5)
    draw_line(buf, w, h, w - 24, h - 24, 24, h - 24, (42, 49, 66), 1.5)
    draw_line(buf, w, h, 24, h - 24, 24, 24, (42, 49, 66), 1.5)

    # Subtle inner corner accents in Gracie Barra red (#D7182A)
    corner_len = 28
    draw_line(buf, w, h, 24, 24, 24 + corner_len, 24, (215, 24, 42), 2.5)
    draw_line(buf, w, h, 24, 24, 24, 24 + corner_len, (215, 24, 42), 2.5)

    draw_line(buf, w, h, w - 24, 24, w - 24 - corner_len, 24, (215, 24, 42), 2.5)
    draw_line(buf, w, h, w - 24, 24, w - 24, 24 + corner_len, (215, 24, 42), 2.5)

    draw_line(buf, w, h, 24, h - 24, 24 + corner_len, h - 24, (215, 24, 42), 2.5)
    draw_line(buf, w, h, 24, h - 24, 24, h - 24 - corner_len, (215, 24, 42), 2.5)

    draw_line(buf, w, h, w - 24, h - 24, w - 24 - corner_len, h - 24, (215, 24, 42), 2.5)
    draw_line(buf, w, h, w - 24, h - 24, w - 24, h - 24 - corner_len, (215, 24, 42), 2.5)

    # Circular ambient halo behind logo
    draw_circle(buf, w, h, 400, 210, 115, (215, 24, 42), 2.0)
    draw_circle(buf, w, h, 400, 210, 125, (42, 49, 66), 1.0)

    # Scale logo to 180x180 and composite in center
    scaled_logo = os.path.join(SCRATCH_DIR, "logo_180.png")
    subprocess.run([
        'sips', '-z', '180', '180',
        os.path.join(IMG_DIR, "logo.png"),
        '--out', scaled_logo
    ], check=True, stdout=subprocess.DEVNULL)

    lw, lh, l_rgba = load_png_rgba(scaled_logo)
    composite_rgba(buf, w, h, l_rgba, lw, lh, (w - lw) // 2, 210 - lh // 2)

    # Red Pill Badge: "GRACIE BARRA"
    badge_txt = "GRACIE BARRA"
    badge_tw = get_text_width(badge_txt, 15, letter_spacing=2.5)
    badge_w = badge_tw + 36
    badge_h = 30
    bx1 = (w - badge_w) / 2
    by1 = 345
    draw_filled_rounded_rect(buf, w, h, bx1, by1, bx1 + badge_w, by1 + badge_h, 5, (215, 24, 42), alpha=1.0)
    draw_text(buf, w, h, badge_txt, bx1 + 18, by1 + 7, 15, (255, 255, 255), 2.0, letter_spacing=2.5)

    # Title: "TURMA FEMININA"
    title_txt = "TURMA FEMININA"
    title_tw = get_text_width(title_txt, 46, letter_spacing=4.0)
    draw_text(buf, w, h, title_txt, (w - title_tw) / 2, 395, 46, (255, 255, 255), 4.0, letter_spacing=4.0)

    # Subtitle: "JIU-JITSU E DEFESA PESSOAL"
    sub_txt = "JIU-JITSU E DEFESA PESSOAL"
    sub_tw = get_text_width(sub_txt, 18, letter_spacing=3.0)
    draw_text(buf, w, h, sub_txt, (w - sub_tw) / 2, 458, 18, (201, 206, 216), 2.0, letter_spacing=3.0)

    # Horizontal divider line with red diamond/dot
    draw_line(buf, w, h, 280, 500, 520, 500, (42, 49, 66), 1.0)
    draw_line(buf, w, h, 390, 500, 410, 500, (215, 24, 42), 2.5)

    # Footer note: "EM BREVE · GURIRI – SAO MATEUS"
    foot_txt = "EM BREVE · GURIRI – SAO MATEUS"
    foot_tw = get_text_width(foot_txt, 15, letter_spacing=2.0)
    draw_text(buf, w, h, foot_txt, (w - foot_tw) / 2, 522, 15, (255, 77, 90), 1.8, letter_spacing=2.0)

    bmp_out = os.path.join(SCRATCH_DIR, "modalidade-feminina.bmp")
    jpg_out = os.path.join(IMG_DIR, "modalidade-feminina.jpg")
    save_bmp(buf, w, h, bmp_out)
    convert_bmp_to_jpg(bmp_out, jpg_out, quality="high")
    print(f"Generated {jpg_out} ({os.path.getsize(jpg_out)} bytes)")

# -------------------------------------------------------------
# 2. Generator: og-image.jpg (1200x630)
# -------------------------------------------------------------
def generate_og_image():
    print("Generating og-image.jpg (1200x630)...")
    target_w, target_h = 1200, 630
    
    # 1. Scale hero-academia.jpg to height 630
    # Original is 1206x500 -> scaled width = 1206 * (630 / 500) = 1520
    scaled_hero_jpg = os.path.join(SCRATCH_DIR, "hero_og_scaled.jpg")
    scaled_hero_bmp = os.path.join(SCRATCH_DIR, "hero_og_scaled.bmp")
    subprocess.run([
        'sips', '-z', str(target_h), '1520',
        os.path.join(IMG_DIR, "hero-academia.jpg"),
        '--out', scaled_hero_jpg
    ], check=True, stdout=subprocess.DEVNULL)

    subprocess.run([
        'sips', '-s', 'format', 'bmp',
        scaled_hero_jpg, '--out', scaled_hero_bmp
    ], check=True, stdout=subprocess.DEVNULL)

    # Read scaled hero BMP
    with open(scaled_hero_bmp, 'rb') as f:
        hero_data = f.read()

    offset = struct.unpack('<I', hero_data[10:14])[0]
    hw, raw_hh, _, _ = struct.unpack('<iiHH', hero_data[18:30])
    is_top_down = raw_hh < 0
    hh = abs(raw_hh)
    row_padded = (hw * 3 + 3) & ~3

    # Create target 1200x630 buffer
    buf = bytearray(target_w * target_h * 3)

    # Offset to align hero horizontally (focus on tatame and gym equipment)
    x_offset = int((hw - target_w) * 0.4)

    for y in range(target_h):
        src_row_idx = y if is_top_down else (hh - 1 - y)
        src_row_start = offset + src_row_idx * row_padded + x_offset * 3
        dst_row_start = y * target_w * 3
        for x in range(target_w):
            idx_s = src_row_start + x * 3
            sb = hero_data[idx_s]
            sg = hero_data[idx_s+1]
            sr = hero_data[idx_s+2]

            # Smooth horizontal vignette/gradient overlay
            # x = 0..480: heavy dark slate (#0D0F14, 94% opacity)
            # x = 480..1200: fades out to ~30% dark overlay on the far right
            if x < 460:
                dark_alpha = 0.94
            else:
                progress = (x - 460) / (target_w - 460)
                # smooth ease
                dark_alpha = 0.94 - 0.60 * (progress ** 0.8)

            bg_r, bg_g, bg_b = 13, 15, 20 # #0D0F14
            final_b = int(sb * (1.0 - dark_alpha) + bg_b * dark_alpha)
            final_g = int(sg * (1.0 - dark_alpha) + bg_g * dark_alpha)
            final_r = int(sr * (1.0 - dark_alpha) + bg_r * dark_alpha)

            idx_d = dst_row_start + x * 3
            buf[idx_d] = final_b
            buf[idx_d+1] = final_g
            buf[idx_d+2] = final_r

    # Red accent stripe along the top edge (5px height)
    for y in range(5):
        for x in range(target_w):
            idx = (y * target_w + x) * 3
            buf[idx] = 42
            buf[idx+1] = 24
            buf[idx+2] = 215 # #D7182A

    # Scale logo to 130x130 for OG image
    og_logo_png = os.path.join(SCRATCH_DIR, "logo_og_130.png")
    subprocess.run([
        'sips', '-z', '130', '130',
        os.path.join(IMG_DIR, "logo.png"),
        '--out', og_logo_png
    ], check=True, stdout=subprocess.DEVNULL)

    lw, lh, l_rgba = load_png_rgba(og_logo_png)
    # Composite logo at x=80, y=90
    composite_rgba(buf, target_w, target_h, l_rgba, lw, lh, 80, 90)

    # Next to logo: Brand name and region
    # "GRACIE BARRA"
    draw_text(buf, target_w, target_h, "GRACIE BARRA", 235, 115, 42, (255, 255, 255), 4.5, letter_spacing=3.0)
    # "SAO MATEUS · ES"
    draw_text(buf, target_w, target_h, "SAO MATEUS · ES", 238, 172, 18, (255, 77, 90), 2.2, letter_spacing=4.0)

    # Horizontal red divider
    draw_line(buf, target_w, target_h, 80, 245, 680, 245, (42, 49, 66), 2.0)
    draw_line(buf, target_w, target_h, 80, 245, 220, 245, (215, 24, 42), 3.0)

    # Main Headline: "JIU-JITSU PARA TODOS."
    draw_text(buf, target_w, target_h, "JIU-JITSU", 80, 275, 62, (255, 255, 255), 5.5, letter_spacing=3.0)
    draw_text(buf, target_w, target_h, "PARA TODOS.", 80, 350, 62, (215, 24, 42), 5.5, letter_spacing=3.0)

    # Subheading: modalities list
    draw_text(buf, target_w, target_h, "GI · NO-GI · KIDS · FEMININA", 80, 445, 24, (220, 225, 235), 2.5, letter_spacing=3.5)

    # Location / professor pill badge at bottom
    loc_pill_w = 460
    loc_pill_h = 44
    draw_filled_rounded_rect(buf, target_w, target_h, 80, 505, 80 + loc_pill_w, 505 + loc_pill_h, 6, (26, 31, 43), alpha=0.9)
    # Red bullet
    draw_filled_rounded_rect(buf, target_w, target_h, 98, 522, 108, 532, 5, (215, 24, 42), alpha=1.0)
    draw_text(buf, target_w, target_h, "GURIRI · PROF. MUCIO MAIA", 124, 518, 18, (255, 255, 255), 2.0, letter_spacing=2.5)

    bmp_out = os.path.join(SCRATCH_DIR, "og-image.bmp")
    jpg_out = os.path.join(IMG_DIR, "og-image.jpg")
    save_bmp(buf, target_w, target_h, bmp_out)
    convert_bmp_to_jpg(bmp_out, jpg_out, quality="high")
    print(f"Generated {jpg_out} ({os.path.getsize(jpg_out)} bytes)")

# -------------------------------------------------------------
# 3. Favicons & Apple Touch Icon
# -------------------------------------------------------------
def generate_favicons():
    print("Generating favicons and touch icons...")
    src_logo = os.path.join(IMG_DIR, "logo.png")

    targets = [
        # (output_path, width, height, format)
        (os.path.join(IMG_DIR, "favicon.png"), 32, 32, "png"),
        (os.path.join(ROOT_DIR, "favicon.png"), 32, 32, "png"),
        (os.path.join(IMG_DIR, "apple-touch-icon.png"), 180, 180, "png"),
        (os.path.join(ROOT_DIR, "apple-touch-icon.png"), 180, 180, "png"),
        (os.path.join(IMG_DIR, "favicon.ico"), 32, 32, "ico"),
        (os.path.join(ROOT_DIR, "favicon.ico"), 32, 32, "ico"),
    ]

    for (out_path, w, h, fmt) in targets:
        cmd = ['sips', '-z', str(h), str(w)]
        if fmt != "png":
            cmd.extend(['-s', 'format', fmt])
        cmd.extend([src_logo, '--out', out_path])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"Generated {out_path} ({os.path.getsize(out_path)} bytes)")

# -------------------------------------------------------------
# 4. Image Optimization (Kids card <= 120KB, etc.)
# -------------------------------------------------------------
def optimize_jpegs():
    print("Optimizing JPEG files...")
    # modalidade-kids.jpg is currently 263KB (1360x907).
    # Resize to 760px wide (aspect-ratio 4:3 -> 760x507) and recompress
    kids_path = os.path.join(IMG_DIR, "modalidade-kids.jpg")
    tmp_kids = os.path.join(SCRATCH_DIR, "kids_optimized.jpg")
    subprocess.run([
        'sips', '-Z', '760',
        '-s', 'formatOptions', 'high',
        kids_path, '--out', tmp_kids
    ], check=True, stdout=subprocess.DEVNULL)
    
    # Overwrite if smaller and <= 120KB
    new_size = os.path.getsize(tmp_kids)
    if new_size <= 120 * 1024:
        os.replace(tmp_kids, kids_path)
        print(f"Optimized modalidade-kids.jpg down to {os.path.getsize(kids_path)} bytes (<= 120KB)")
    else:
        # Re-save with 'normal' format option
        subprocess.run([
            'sips', '-Z', '720',
            '-s', 'formatOptions', 'normal',
            kids_path, '--out', kids_path
        ], check=True, stdout=subprocess.DEVNULL)
        print(f"Optimized modalidade-kids.jpg down to {os.path.getsize(kids_path)} bytes")

# -------------------------------------------------------------
# 5. WebP Generation with cwebp
# -------------------------------------------------------------
def generate_webps():
    print("Generating WebP versions with cwebp...")
    cwebp_bin = "/opt/homebrew/bin/cwebp"
    
    # List of images to generate webp for:
    images = [
        ("hero-academia.jpg", 82, False),
        ("modalidade-gi.jpg", 82, False),
        ("modalidade-nogi.jpg", 82, False),
        ("modalidade-kids.jpg", 82, False),
        ("modalidade-feminina.jpg", 82, False),
        ("professor-mucio.jpg", 82, False),
        ("sede-guriri.jpg", 82, False),
        ("og-image.jpg", 85, False),
        ("logo.png", 90, True),  # Lossless for crisp transparent logo
    ]

    for fname, q, is_lossless in images:
        src = os.path.join(IMG_DIR, fname)
        base, _ = os.path.splitext(fname)
        dst = os.path.join(IMG_DIR, f"{base}.webp")
        cmd = [cwebp_bin]
        if is_lossless:
            cmd.extend(['-lossless'])
        else:
            cmd.extend(['-q', str(q), '-m', '6', '-sharp_yuv'])
        cmd.extend([src, '-o', dst])
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
        print(f"Generated {dst} ({os.path.getsize(dst)} bytes)")

def report_all():
    print("\n" + "=" * 70)
    print("SUMMARY OF ALL ASSETS IN assets/img/")
    print("=" * 70)
    all_files = sorted(os.listdir(IMG_DIR))
    for f in all_files:
        if f.startswith('.'):
            continue
        p = os.path.join(IMG_DIR, f)
        size = os.path.getsize(p)
        # get dimensions via sips
        res = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', p], capture_output=True, text=True)
        w, h = "?", "?"
        for line in res.stdout.splitlines():
            if 'pixelWidth:' in line:
                w = line.split(':')[-1].strip()
            elif 'pixelHeight:' in line:
                h = line.split(':')[-1].strip()
        print(f"{f:<32} {w:>5}x{h:<5} {size:>9,} bytes ({size/1024:.1f} KB)")
    print("=" * 70)

if __name__ == "__main__":
    generate_modalidade_feminina()
    generate_og_image()
    generate_favicons()
    optimize_jpegs()
    generate_webps()
    report_all()
