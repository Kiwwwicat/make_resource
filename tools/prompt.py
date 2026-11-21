#!/usr/bin/env python3
"""카테고리 목록(catalog/<category>.csv)에서 4x4 시트 생성용 프롬프트를 만든다.

  python tools/prompt.py food          시트별 프롬프트와, 받은 이미지를 변환할 명령을 출력

규격(32x32 캔버스, 아이콘 28px, 화풍, 배경색)은 여기 한 곳에 고정되어 있으므로
아이콘을 추가할 때는 catalog에 한 줄(prompt_en 포함)만 쓰면 된다.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORD = ["Row 1", "Row 2", "Row 3", "Row 4"]
# 한 장의 격자 크기. 4 = 16개/장(가장 저렴), 3 = 9개/장(아이콘이 더 크게 나옴).
# 작고 둥근 물체(음식 등)는 4x4에서 18~20px로 작게 나와 3x3을 쓴다.
GRID = {"default": 4, "food": 3}

# 요청 크기(px). 실제로는 요청보다 작게 나오는 경향이 있고, 작고 둥근 물체일수록 더 그렇다 (실측: 28 요청 시
# 가구 24~30px, 음식 17~24px). 변환 결과가 22px 미만이면 lint가 막으므로 그 카테고리의 값을 올려 재생성한다.
ASK_SIZE = {"default": 28}

STYLE = (
    "Each icon is very low resolution and chunky: exactly {n} pixels wide and {n} pixels tall, enlarged so each "
    "pixel is a big crisp perfect square block. Every icon is drawn large, at the same size, and fills about 90 percent "
    "of its cell without touching the neighbouring icons. Style of a 16-bit era RPG inventory icon: clean dark "
    "coloured 1-pixel outline, light from the upper left, 3 shades per colour, one small highlight, no stray "
    "pixels, no dithering, no anti-aliasing, no gradients, no blur. Nothing else in the image: no white areas "
    "outside the icons, no dividing lines, no frames, no shadows on the ground, no text, no labels."
)


def sheets(cat):
    rows = list(csv.DictReader(open(ROOT / "catalog" / f"{cat}.csv", encoding="utf-8")))
    per = GRID.get(cat, GRID["default"]) ** 2
    for n in range(0, len(rows), per):
        yield n // per + 1, rows[n:n + per]


def prompt(rows, cat="default"):
    cols = GRID.get(cat, GRID["default"])
    lines = []
    for r in range(0, len(rows), cols):
        items = "; ".join(x["prompt_en"] for x in rows[r:r + cols])
        lines.append(f"{ORD[r // cols]}, left to right: {items}.")
    return (
        "The entire image background is a perfectly flat solid pure magenta colour (#FF00FF), edge to edge. "
        f"On this magenta background there are exactly {len(rows)} separate pixel art game item icons arranged in "
        f"a strict, evenly spaced {cols} by {cols} grid, one centred in each cell, all in the same style and on the same "
        "pixel grid. " + " ".join(lines) + " " + STYLE.format(n=ASK_SIZE.get(cat, ASK_SIZE["default"]))
    )


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cat = argv[0]
    for no, rows in sheets(cat):
        png = f"source/{cat}/sheets/{cat}_{no:02d}.png"
        print(f"=== {cat} 시트 {no} ({len(rows)}개) -> {png}")
        print(prompt(rows, cat))
        cols = GRID.get(cat, GRID["default"])
        ids = [r["id"] for r in rows] + ["-"] * (cols * cols - len(rows))
        print(f"--- 변환: python tools/convert.py --sheet {png} {cat} --cols {cols} " + " ".join(ids))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
