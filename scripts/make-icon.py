#!/usr/bin/env python3
"""Draw assets/icon.png from the theme's own ANSI palette.

The marketplace wants a 128x128 PNG. Rather than keep a binary that nobody can
edit and that drifts from the theme the moment a colour changes, this reads the
palette out of the theme file and draws the icon: a rainbow arc on the theme's
own near-black background.

    python3 scripts/make-icon.py            # draw it
    python3 scripts/make-icon.py --check    # is the committed one still right?

Pure standard library — zlib and struct are enough to write a PNG, and a theme
extension should not need a build toolchain to produce its own icon.
"""

from __future__ import annotations

import json
import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
THEME = ROOT / "themes" / "12-bit-rainbow-color-theme.json"
OUT = ROOT / "assets" / "icon.png"

SIZE = 128
SUPERSAMPLE = 4  # Rendered at 4x and box-filtered down; the arc has curved edges.
CORNER_RADIUS = 26

# Rainbow order, by the ANSI slot each one occupies in the terminal palette.
BAND_SLOTS = [
    "terminal.ansiRed",
    "terminal.ansiBrightRed",
    "terminal.ansiYellow",
    "terminal.ansiGreen",
    "terminal.ansiCyan",
    "terminal.ansiBlue",
    "terminal.ansiMagenta",
]

INNER_RADIUS = 27.0
OUTER_RADIUS = 61.0


def load_palette() -> tuple[tuple[int, int, int], list[tuple[int, int, int]]]:
    colors = json.loads(THEME.read_text())["colors"]

    missing = [slot for slot in BAND_SLOTS if slot not in colors]
    if missing:
        raise SystemExit(f"theme is missing {', '.join(missing)} — icon cannot be drawn from it")

    return to_rgb(colors["editor.background"]), [to_rgb(colors[slot]) for slot in BAND_SLOTS]


def to_rgb(value: str) -> tuple[int, int, int]:
    """`#rrggbb` or `#rrggbbaa` to an (r, g, b) triple; alpha is dropped."""
    digits = value.lstrip("#")
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def render(background: tuple[int, int, int], bands: list[tuple[int, int, int]]) -> bytearray:
    scale = SUPERSAMPLE
    big = SIZE * scale

    # Arc geometry, in supersampled units.
    cx, cy = big / 2, big * 0.72
    inner, outer = INNER_RADIUS * scale, OUTER_RADIUS * scale
    band_width = (outer - inner) / len(bands)
    radius = CORNER_RADIUS * scale

    # Accumulate RGBA sums per output pixel, then divide. Cheaper than keeping
    # the whole supersampled bitmap around.
    sums = [[0, 0, 0, 0] for _ in range(SIZE * SIZE)]

    for y in range(big):
        row_out = (y // scale) * SIZE
        dy = y + 0.5 - cy

        for x in range(big):
            px = x + 0.5
            py = y + 0.5

            if not inside_rounded_square(px, py, big, radius):
                continue  # Transparent corner.

            dx = px - cx
            colour = background

            # Only the upper half is drawn, so it reads as an arc, not a ring.
            if dy <= 0:
                distance = (dx * dx + dy * dy) ** 0.5
                if inner <= distance < outer:
                    colour = bands[min(int((distance - inner) / band_width), len(bands) - 1)]

            cell = sums[row_out + (x // scale)]
            cell[0] += colour[0]
            cell[1] += colour[1]
            cell[2] += colour[2]
            cell[3] += 255

    samples = scale * scale
    pixels = bytearray()
    for cell in sums:
        alpha = cell[3] // samples
        if alpha == 0:
            pixels += b"\x00\x00\x00\x00"
            continue
        # Un-premultiply: colour sums only accumulated over covered samples.
        covered = cell[3] / 255
        pixels += bytes(
            (
                round(cell[0] / covered),
                round(cell[1] / covered),
                round(cell[2] / covered),
                alpha,
            )
        )

    return pixels


def inside_rounded_square(x: float, y: float, size: float, radius: float) -> bool:
    near_x = min(max(x, radius), size - radius)
    near_y = min(max(y, radius), size - radius)
    dx, dy = x - near_x, y - near_y
    return dx * dx + dy * dy <= radius * radius


def write_png(path: pathlib.Path, pixels: bytearray) -> None:
    stride = SIZE * 4
    raw = bytearray()
    for row in range(SIZE):
        raw.append(0)  # Filter type 0 (None). The image is small; filtering earns nothing.
        raw += pixels[row * stride : (row + 1) * stride]

    def chunk(kind: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + kind
            + payload
            + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)
        )

    header = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)  # 8-bit RGBA
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def read_png_pixels(path: pathlib.Path) -> bytearray | None:
    """Decode an 8-bit RGBA PNG back to raw pixels, or None if it is not one.

    `--check` compares pixels rather than file bytes deliberately: zlib's output
    is not guaranteed identical across versions, so a byte comparison would fail
    on a CI runner whose zlib differs from the machine that drew the icon —
    reporting drift where there is none.
    """
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None

    offset = 8
    idat = bytearray()
    width = height = 0

    while offset < len(data):
        (length,) = struct.unpack(">I", data[offset : offset + 4])
        kind = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        offset += 12 + length  # length + type + payload + crc

        if kind == b"IHDR":
            width, height, depth, colour_type = struct.unpack(">IIBB", payload[:10])
            if (depth, colour_type) != (8, 6):
                return None
        elif kind == b"IDAT":
            idat += payload
        elif kind == b"IEND":
            break

    if (width, height) != (SIZE, SIZE):
        return None

    raw = zlib.decompress(bytes(idat))
    stride = SIZE * 4
    out = bytearray()
    previous = bytearray(stride)

    for row in range(SIZE):
        start = row * (stride + 1)
        filter_type = raw[start]
        line = bytearray(raw[start + 1 : start + 1 + stride])

        for i in range(stride):
            left = line[i - 4] if i >= 4 else 0
            up = previous[i]
            upleft = previous[i - 4] if i >= 4 else 0

            if filter_type == 1:
                line[i] = (line[i] + left) & 0xFF
            elif filter_type == 2:
                line[i] = (line[i] + up) & 0xFF
            elif filter_type == 3:
                line[i] = (line[i] + (left + up) // 2) & 0xFF
            elif filter_type == 4:
                line[i] = (line[i] + paeth(left, up, upleft)) & 0xFF
            elif filter_type != 0:
                return None

        out += line
        previous = line

    return out


def paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    return b if pb <= pc else c


def main() -> None:
    background, bands = load_palette()
    expected = render(background, bands)

    if "--check" in sys.argv:
        if not OUT.exists():
            raise SystemExit(f"{OUT.relative_to(ROOT)} is missing — run `npm run icon`")
        if read_png_pixels(OUT) != expected:
            raise SystemExit(
                f"{OUT.relative_to(ROOT)} is not what this script draws — "
                "run `npm run icon` and commit the result"
            )
        print(f"✓ {OUT.relative_to(ROOT)} matches the palette")
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_png(OUT, expected)
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes, {SIZE}x{SIZE})")


if __name__ == "__main__":
    main()
