#!/usr/bin/env python3
"""AI 생성 원본(큰 '가짜 픽셀아트' 이미지, 마젠타 배경) -> 규격 32x32 아이콘.

  python tools/convert.py food/apple      source/food/apple.png -> pixels/food/apple.png
  python tools/convert.py food            source/food/*.png 전부
  python tools/convert.py --sheet source/food/sheets/sheet01.png food a b c d   2x2 시트를 칸별로

단계: ① 픽셀 격자 주기/위상 추정 ② 칸마다 대표색 추출 ③ 배경(마젠타) 제거
④ 30x30 안에 맞춤(필요 시 정수비 축소) ⑤ 마스터 팔레트로 양자화
⑥ 가시 픽셀·고립 픽셀 정리 ⑦ 외곽선 보정 ⑧ 중앙 정렬.
"""
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import pixelkit as pk  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INNER = 30  # 외곽선 포함 최대 크기 (0, 31 행/열은 항상 투명)


def is_bg(a):
    """배경 판정: 귀퉁이 대표색(마젠타/시안)과 가깝고 테두리에서 이어진 영역,
    또는 대표색과 거의 같은 색(도넛 구멍 등 안쪽에 갇힌 배경)."""
    from collections import deque
    c = np.concatenate([a[:8, :8].reshape(-1, 3), a[:8, -8:].reshape(-1, 3),
                        a[-8:, :8].reshape(-1, 3), a[-8:, -8:].reshape(-1, 3)])
    key = np.median(c, axis=0)
    dist = np.sqrt(((a.astype(float) - key) ** 2).sum(axis=-1))
    near = dist < 95
    h, w = near.shape
    seen = np.zeros_like(near)
    q = deque()
    for x in range(w):
        q.append((0, x)); q.append((h - 1, x))
    for y in range(h):
        q.append((y, 0)); q.append((y, w - 1))
    while q:
        y, x = q.popleft()
        if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not near[y, x]:
            continue
        seen[y, x] = True
        q.extend(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
    saturated = key.max() - key.min() > 100   # 흰 배경이면 갇힌 흰색(크림 등)은 지우지 않는다
    return seen | ((dist < 40) & saturated)


def cell_size(a):
    """같은 색이 이어지는 구간 길이의 최빈값 = 픽셀 한 칸의 크기 (가로/세로 공통)."""
    f = a.astype(int)
    hist = np.zeros(200)
    for arr in (f, f.transpose(1, 0, 2)):
        for row in arr[::4]:
            change = np.abs(np.diff(row, axis=0)).sum(axis=1) > 40
            idx = np.flatnonzero(change)
            runs = np.diff(idx)
            for r in runs[(runs >= 5) & (runs < 200)]:
                hist[r] += 1
    sm = np.convolve(hist, np.ones(5), mode="same")
    return float(np.argmax(sm))


def find_grid(a, base=None):
    """칸 크기 근처에서 가로/세로 각각 (주기, 위상)을 정밀 추정.
    base(시트 전체에서 구한 칸 크기)가 주어지면 ±5%, 아니면 자체 추정값 ±12%."""
    tol = 0.05 if base else 0.12
    base = base or cell_size(a)
    out = []
    f = a.astype(float)
    for axis in (1, 0):
        d = np.abs(np.diff(f, axis=axis)).sum(axis=2).sum(axis=1 - axis)
        d = d / (d.max() + 1e-9)
        best = (-1, base, 0)
        n = len(d)
        for p in np.arange(base * (1 - tol), base * (1 + tol), 0.02):
            for o in np.arange(0, p, 0.5):
                idx = np.round(np.arange(o, n, p)).astype(int)
                idx = idx[(idx >= 0) & (idx < n)]
                mid = np.round(np.arange(o + p / 2, n, p)).astype(int)
                mid = mid[(mid >= 0) & (mid < n)]
                score = d[idx].mean() - d[mid].mean()
                if score > best[0]:
                    best = (score, p, o)
        out.append((best[1], best[2]))
    return out  # [(px, ox), (py, oy)]


def sample(a, grid):
    (px, ox), (py, oy) = grid
    h, w = a.shape[:2]
    xs = np.arange(ox - px if ox > px * 0.5 else ox, w, px)
    ys = np.arange(oy - py if oy > py * 0.5 else oy, h, py)
    bg = is_bg(a)
    cells, alpha = [], []
    for y0 in ys:
        row, arow = [], []
        for x0 in xs:
            xa, xb = int(round(x0 + px * 0.25)), int(round(x0 + px * 0.75))
            ya, yb = int(round(y0 + py * 0.25)), int(round(y0 + py * 0.75))
            xa, ya = max(xa, 0), max(ya, 0)
            blk = a[ya:max(yb, ya + 1), xa:max(xb, xa + 1)]
            if blk.size == 0:
                row.append((0, 0, 0)); arow.append(False); continue
            row.append(tuple(np.median(blk.reshape(-1, 3), axis=0)))
            arow.append(bg[ya:max(yb, ya + 1), xa:max(xb, xa + 1)].mean() < 0.5)
        cells.append(row); alpha.append(arow)
    return np.array(cells, dtype=float), np.array(alpha, dtype=bool)


def lab(rgb):
    """sRGB(0-255) -> 대략적인 지각 균등 공간 (Oklab)."""
    c = np.asarray(rgb, dtype=float) / 255
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    l = 0.4122214708 * c[..., 0] + 0.5363325363 * c[..., 1] + 0.0514459929 * c[..., 2]
    m = 0.2119034982 * c[..., 0] + 0.6806995451 * c[..., 1] + 0.1073969566 * c[..., 2]
    s = 0.0883024619 * c[..., 0] + 0.2817188376 * c[..., 1] + 0.6299787005 * c[..., 2]
    l, m, s = np.cbrt(l), np.cbrt(m), np.cbrt(s)
    return np.stack([0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
                     1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
                     0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s], axis=-1)


PAL = [(r, s) for r in pk.PALETTE for s in range(5)]
PAL_LAB = lab(np.array([pk.rgb(r, s)[:3] for r, s in PAL]))


def quantize(cells, alpha):
    L = lab(cells)
    out = {}
    for y in range(cells.shape[0]):
        for x in range(cells.shape[1]):
            if alpha[y, x]:
                d = ((PAL_LAB - L[y, x]) ** 2 * np.array([1.0, 2.0, 2.0])).sum(axis=1)
                out[(x, y)] = PAL[int(d.argmin())]
    return out


def denoise(pix):
    """한 픽셀에만 쓰인 색(경계 번짐으로 생긴 잡색)을 그 아이콘의 주요 색 중 가장 가까운 것으로 합친다.
    스프링클·씨앗처럼 같은 색이 여러 번 나오는 디테일은 건드리지 않는다."""
    cnt = Counter(pix.values())
    major = [c for c, n in cnt.items() if n >= 3]
    if not major:
        return pix
    mlab = lab(np.array([pk.rgb(*c)[:3] for c in major]))
    for p, c in list(pix.items()):
        if cnt[c] == 1:
            d = ((mlab - lab(np.array(pk.rgb(*c)[:3]))) ** 2).sum(axis=1)
            pix[p] = major[int(d.argmin())]
    return pix


def fit(pix):
    """30x30에 맞추고 중앙 정렬. 넘치면 '덮는 칸들의 다수색'으로 축소."""
    xs = [p[0] for p in pix]; ys = [p[1] for p in pix]
    x0, y0 = min(xs), min(ys)
    w, h = max(xs) - x0 + 1, max(ys) - y0 + 1
    scale = max(w, h) / INNER if max(w, h) > INNER else 1.0
    if scale > 1:
        nw, nh = max(1, round(w / scale)), max(1, round(h / scale))
        new = {}
        for j in range(nh):
            for i in range(nw):
                votes, total = Counter(), 0.0
                xa, xb = x0 + i * w / nw, x0 + (i + 1) * w / nw
                ya, yb = y0 + j * h / nh, y0 + (j + 1) * h / nh
                for sy in range(int(ya), int(np.ceil(yb))):
                    for sx in range(int(xa), int(np.ceil(xb))):
                        area = (min(xb, sx + 1) - max(xa, sx)) * (min(yb, sy + 1) - max(ya, sy))
                        total += area
                        if (sx, sy) in pix:
                            votes[pix[(sx, sy)]] += area
                if votes and sum(votes.values()) >= total * 0.5:
                    # 어두운 외곽선(0단계)은 얇아서 묻히기 쉬우므로 가중치를 준다
                    for c in votes:
                        if c[1] == 0:
                            votes[c] *= 1.15
                    new[(i, j)] = votes.most_common(1)[0][0]
        pix, x0, y0, w, h = new, 0, 0, nw, nh
    dx = (pk.SIZE - w) // 2 - x0
    dy = (pk.SIZE - h) // 2 - y0
    return {(x + dx, y + dy): c for (x, y), c in pix.items()}, scale


def clean(pix):
    """가시 픽셀 제거, 1px 홈 메우기, 외곽선 보정. (씨앗·스프링클 같은 내부 1px 디테일은 보존)"""
    D4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for _ in range(3):
        sil = set(pix)
        sp = pk._spikes(sil)
        # 어느 방향으로도 2px 이상 이어지지 않는 돌출 1px 도 제거
        for (x, y) in sil:
            if sum((x + dx, y + dy) in sil for dx, dy in D4) == 0:
                sp.add((x, y))
        for p in sp:
            del pix[p]
        for (x, y) in pk._notches(set(pix)):
            near = [pix[(x + dx, y + dy)] for dx, dy in D4 if (x + dx, y + dy) in pix]
            pix[(x, y)] = Counter(near).most_common(1)[0][0]
        if not sp:
            break
    # 외곽선 보정: 투명과 맞닿은 픽셀은 안쪽 색의 램프를 따르는 0단계로 통일
    sil = set(pix)
    edge = {(x, y) for (x, y) in sil if any((x + dx, y + dy) not in sil for dx, dy in D4)}
    new = {}
    for (x, y) in edge:
        inner = [pix[q][0] for q in ((x + i, y + j) for i in (-1, 0, 1) for j in (-1, 0, 1))
                 if q in sil and q not in edge and pix[q][1] >= 1]
        new[(x, y)] = ((Counter(inner).most_common(1)[0][0] if inner else pix[(x, y)][0]), 0)
    pix.update(new)
    return pix


def convert(cat, icon_id, a=None, base=None):
    if a is None:
        a = np.array(Image.open(ROOT / "source" / cat / f"{icon_id}.png").convert("RGB"))
    grid = find_grid(a, base)
    cells, alpha = sample(a, grid)
    pix = quantize(cells, alpha)
    xs = [p[0] for p in pix]; ys = [p[1] for p in pix]
    raw = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1)
    pix, scale = fit(pix)
    pix = clean(denoise(pix))
    img = Image.new("RGBA", (pk.SIZE, pk.SIZE), (0, 0, 0, 0))
    for (x, y), (ramp, s) in pix.items():
        if 0 <= x < pk.SIZE and 0 <= y < pk.SIZE:
            img.putpixel((x, y), pk.rgb(ramp, s))
    dest = ROOT / "pixels" / cat / f"{icon_id}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    note = "" if scale == 1 else f"  (축소 {scale:.2f}배)"
    if max(raw) < 20:
        note += "  ** 20칸 미만: 작게 나옴"
    print(f"{cat}/{icon_id}: 격자 {grid[0][0]:.2f}x{grid[1][0]:.2f}px, 원본 {raw[0]}x{raw[1]}칸{note}")
    return scale == 1


def convert_sheet(path, cat, ids, cols=2):
    """한 장에 여러 아이콘이 격자로 놓인 시트를 칸별로 잘라 변환. ids는 좌->우, 위->아래 순서,
    건너뛸 칸은 '-'."""
    a = np.array(Image.open(path).convert("RGB"))
    rows = cols   # 시트는 항상 정사각 격자 (빈 칸은 '-')
    h, w = a.shape[0] // rows, a.shape[1] // cols
    base = cell_size(a)   # 한 시트의 아이콘들은 같은 픽셀 격자를 쓴다
    for i, iid in enumerate(ids):
        if iid != "-":
            r, c = divmod(i, cols)
            convert(cat, iid, a[r * h:(r + 1) * h, c * w:(c + 1) * w], base)


def main(argv):
    if not argv:
        print(__doc__); return 2
    if argv[0] == "--sheet":   # --sheet <png> <category> [--cols N] <id> <id> ...
        rest, cols = argv[3:], 2
        if rest and rest[0] == "--cols":
            cols, rest = int(rest[1]), rest[2:]
        convert_sheet(argv[1], argv[2], rest, cols)
        return 0
    for t in argv:
        if "/" in t:
            convert(*t.split("/", 1))
        else:
            for f in sorted((ROOT / "source" / t).glob("*.png")):
                convert(t, f.stem)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
