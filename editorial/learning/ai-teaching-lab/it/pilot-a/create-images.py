"""Create two synthetic geometry fixtures with only the Python standard library.

No external assets, fonts, network, personal data or image-generation service.
Run from any directory: python3 path/to/create-images.py
"""
from pathlib import Path
import struct
import zlib

WIDTH, HEIGHT = 960, 540
BLUE = (32, 91, 235)
ORANGE = (233, 126, 23)
INK = (17, 24, 39)
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
}


def fixture(filename, shapes):
    pixels = bytearray([255]) * (WIDTH * HEIGHT * 3)

    def put(x, y, color):
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            index = (y * WIDTH + x) * 3
            pixels[index:index + 3] = bytes(color)

    def line(a, b, color, radius):
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = max(abs(dx), abs(dy))
        for step in range(length + 1):
            x = round(a[0] + dx * step / length)
            y = round(a[1] + dy * step / length)
            for ox in range(-radius, radius + 1):
                for oy in range(-radius, radius + 1):
                    put(x + ox, y + oy, color)

    for label, points, color, position in shapes:
        for a, b in zip(points, points[1:] + points[:1]):
            line(a, b, INK, 5)
        for a, b in zip(points, points[1:] + points[:1]):
            line(a, b, color, 3)
        for row, pattern in enumerate(GLYPHS[label]):
            for col, mark in enumerate(pattern):
                if mark == "1":
                    for x in range(7):
                        for y in range(7):
                            put(position[0] + col * 7 + x,
                                position[1] + row * 7 + y, INK)

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    rows = b"".join(b"\0" + pixels[y * WIDTH * 3:(y + 1) * WIDTH * 3]
                    for y in range(HEIGHT))
    encoded = (b"\x89PNG\r\n\x1a\n"
               + chunk(b"IHDR", struct.pack(">2I5B", WIDTH, HEIGHT, 8, 2, 0, 0, 0))
               + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))
    Path(__file__).with_name(filename).write_bytes(encoded)


fixture("confronto-forme-01.png", [
    ("A", [(270, 95), (80, 410), (460, 410)], BLUE, (250, 445)),
    ("B", [(620, 115), (865, 165), (840, 410), (590, 375)], ORANGE, (710, 445)),
])
fixture("confronto-forme-02.png", [
    ("C", [(90, 145), (440, 255), (185, 410)], ORANGE, (250, 445)),
    ("D", [(615, 130), (850, 130), (850, 390), (615, 390)], BLUE, (710, 445)),
])
