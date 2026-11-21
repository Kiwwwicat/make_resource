"""pixelkit - 32x32 픽셀 아이콘을 '코드로' 그리기 위한 최소 도구.

균일한 품질을 위해 다음을 도구가 강제한다.
  * 마스터 팔레트 밖의 색은 쓸 수 없다 (램프 12개 x 5단계).
  * 명암은 좌상단 광원 기준으로 자동 생성된다 (램프 이름만 주면 됨).
  * 외곽선은 빌드 시 자동으로 1px 생성된다 (직접 그리지 않는다).
  * lint()가 여백/크기/중심/색 수 규칙을 검사한다.
"""
from collections import Counter

SIZE = 32
FILL_MIN, FILL_MAX = 2, 29  # 채색 가능 영역. 외곽선 포함 시 1..30, 0과 31은 항상 투명.

# 램프: [0]=외곽선, [1]=어두움, [2]=기본, [3]=밝음, [4]=하이라이트
PALETTE = {
    "red":    ["5a1a2b", "9c2a36", "d2433b", "ee6f52", "fba98a"],
    "orange": ["6b2a1e", "b5501f", "e5822a", "f6a945", "fdd27d"],
    "yellow": ["7a4a1a", "c48a22", "f0c132", "fbe064", "fff4ad"],
    "green":  ["1f3b2c", "2f6b3a", "55a23f", "8fcb4f", "c9ec85"],
    "teal":   ["173a43", "22696b", "34a08e", "6fd0ad", "b5efd0"],
    "blue":   ["1f2a56", "2e4f9c", "3f84d6", "6bb9ee", "b3e3fa"],
    "purple": ["33204f", "5a3590", "8a55c2", "b384e2", "dcbdf5"],
    "pink":   ["5e2147", "a83a6b", "dd6090", "f394b0", "fdc9d2"],
    "brown":  ["33201f", "5c3829", "8a5634", "b57b46", "d9a868"],
    "tan":    ["5a3a26", "9a6a3c", "c99755", "e6c17e", "f6e0ab"],
    "cream":  ["5f4a44", "a8907c", "d8c7a8", "f2e8cf", "fffaf0"],
    "gray":   ["23232e", "4a4c5c", "7c8090", "b0b6c2", "e2e7ee"],
}


def rgb(ramp, shade):
    h = PALETTE[ramp][shade]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def parse_color(color):
    """'red' -> ('red', None) 자동 명암 / 'red3' -> ('red', 3) 고정 단계."""
    if color and color[-1].isdigit():
        ramp, shade = color[:-1], int(color[-1])
    else:
        ramp, shade = color, None
    if ramp not in PALETTE or (shade is not None and not 0 <= shade <= 4):
        raise ValueError(f"팔레트에 없는 색: {color!r} (램프: {', '.join(PALETTE)}; 단계 0-4)")
    return ramp, shade


# ---------------------------------------------------------------- 마스크(픽셀 집합)
def rect(x0, y0, x1, y1):
    """양 끝 포함 사각형."""
    return {(x, y) for x in range(min(x0, x1), max(x0, x1) + 1)
            for y in range(min(y0, y1), max(y0, y1) + 1)}


def ellipse(cx, cy, rx, ry):
    """중심(cx,cy), 반지름(rx,ry). 짝수 폭은 cx=15.5 처럼 .5 중심을 쓴다."""
    out = set()
    if rx <= 0 or ry <= 0:
        return out
    for y in range(SIZE):
        for x in range(SIZE):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                out.add((x, y))
    return out


def line(x0, y0, x1, y1, width=1):
    """브레젠험 직선. width>1 이면 오른쪽/아래로 두꺼워진다."""
    pts = set()
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, x, y = dx + dy, x0, y0
    while True:
        for i in range(width):
            for j in range(width):
                pts.add((x + i, y + j))
        if (x, y) == (x1, y1):
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy
    return pts


def poly(points):
    """꼭짓점 목록으로 채운 다각형 (변 포함)."""
    out = set()
    n = len(points)
    for i in range(n):
        out |= line(*points[i], *points[(i + 1) % n])
    for y in range(SIZE):
        for x in range(SIZE):
            inside = False
            for i in range(n):
                (xa, ya), (xb, yb) = points[i], points[(i + 1) % n]
                if (ya > y) != (yb > y) and x < (xb - xa) * (y - ya) / (yb - ya) + xa:
                    inside = not inside
            if inside:
                out.add((x, y))
    return out


def rotate(mask, deg, cx=15.5, cy=15.5):
    """마스크를 (cx,cy) 기준 시계 방향으로 deg도 회전. 가는 물체의 대각선 배치용.
    똑바로 세워서 만든 뒤 마지막에 돌린다 (보통 45 또는 -45)."""
    import math
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out = set()
    for y in range(SIZE):
        for x in range(SIZE):
            dx, dy = x - cx, y - cy
            src = (round(cx + dx * ca + dy * sa), round(cy - dx * sa + dy * ca))
            if src in mask:
                out.add((x, y))
    return out


def grid(x, y, rows):
    """문자 그림 -> {문자: 마스크}. '.' 과 공백은 무시."""
    out = {}
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch not in ". ":
                out.setdefault(ch, set()).add((x + i, y + j))
    return out


# ---------------------------------------------------------------- 캔버스
class Canvas:
    def __init__(self):
        self.pix = {}  # (x, y) -> (ramp, shade)

    def fill(self, mask, color, light=None, shadow=None):
        """mask를 칠한다. color가 램프 이름('red')이면 자동 명암,
        단계 포함('red3')이면 그 색 그대로. light/shadow로 명암 띠 두께 조절(0=없음)."""
        ramp, shade = parse_color(color)
        mask = set(mask)
        if not mask:
            return mask
        if shade is not None:
            for p in mask:
                self.pix[p] = (ramp, shade)
            return mask
        xs = [p[0] for p in mask]
        ys = [p[1] for p in mask]
        thick = min(max(xs) - min(xs), max(ys) - min(ys)) + 1
        if shadow is None:
            shadow = 0 if thick < 3 else max(1, round(thick / 5))
        if light is None:
            light = 0 if thick < 4 else max(1, round(thick / 9))
        for (x, y) in mask:
            s = 2
            if any((x + k, y + k) not in mask for k in range(1, shadow + 1)):
                s = 1
            elif any((x - k, y - k) not in mask for k in range(1, light + 1)):
                s = 3
            self.pix[(x, y)] = (ramp, s)
        return mask

    # 단축 메서드: 도형 하나를 바로 칠한다.
    def rect(self, x0, y0, x1, y1, color, **kw):
        return self.fill(rect(x0, y0, x1, y1), color, **kw)

    def ellipse(self, cx, cy, rx, ry, color, **kw):
        return self.fill(ellipse(cx, cy, rx, ry), color, **kw)

    def poly(self, points, color, **kw):
        return self.fill(poly(points), color, **kw)

    def line(self, x0, y0, x1, y1, color, width=1):
        return self.fill(line(x0, y0, x1, y1, width), color)

    def px(self, x, y, color):
        return self.fill({(x, y)}, color)

    def grid(self, x, y, rows, legend):
        """문자 그림으로 세부 묘사. legend = {'a': 'red3', ...} (단계 고정색 권장)."""
        for ch, mask in grid(x, y, rows).items():
            if ch not in legend:
                raise ValueError(f"grid 범례에 없는 문자: {ch!r}")
            self.fill(mask, legend[ch])

    def erase(self, mask):
        for p in mask:
            self.pix.pop(p, None)

    def recolor(self, mask, color):
        """이미 칠해진 픽셀 중 mask 안의 것만 색을 바꾼다 (무늬/그림자용)."""
        return self.fill(set(mask) & set(self.pix), color)

    # ------------------------------------------------------------ 마감
    def finish(self):
        """자동 외곽선을 붙인 최종 픽셀 dict를 돌려준다."""
        out = dict(self.pix)
        for y in range(SIZE):
            for x in range(SIZE):
                if (x, y) in self.pix:
                    continue
                near = [self.pix[q] for q in ((x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y))
                        if q in self.pix]
                if near:
                    ramp = Counter(r for r, _ in near).most_common(1)[0][0]
                    out[(x, y)] = (ramp, 0)
        return out

    def lint(self):
        """(errors, warnings) 목록. errors가 있으면 납품 불가."""
        err, warn = [], []
        if not self.pix:
            return ["아무것도 그려지지 않음"], []
        xs = [p[0] for p in self.pix]
        ys = [p[1] for p in self.pix]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x0 < FILL_MIN or y0 < FILL_MIN or x1 > FILL_MAX or y1 > FILL_MAX:
            err.append(f"채색 영역 초과: x {x0}..{x1}, y {y0}..{y1} (허용 {FILL_MIN}..{FILL_MAX})")
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if max(w, h) < 22:
            err.append(f"너무 작음: {w}x{h} (긴 변이 22px 이상이어야 함, 권장 24~28)")
        if min(w, h) < 8:
            warn.append(f"매우 가늚: {w}x{h} - 대각선 배치를 고려")
        cx, cy = (x0 + x1) / 2 - 15.5, (y0 + y1) / 2 - 15.5
        if abs(cx) > 1.5 or abs(cy) > 1.5:
            err.append(f"중심 어긋남: dx={cx:+.1f}, dy={cy:+.1f} (허용 ±1.5)")
        ramps = Counter(r for r, _ in self.pix.values())
        if len(ramps) > 5:
            err.append(f"램프 과다: {len(ramps)}개 {sorted(ramps)} (최대 5)")
        colors = set(self.pix.values())
        if len(colors) > 16:
            err.append(f"색 과다: {len(colors)}색 (최대 16)")
        if len(colors) < 3:
            err.append("명암 없음: 3색 미만")
        orphans = 0
        for (x, y), c in self.pix.items():
            if all(self.pix.get((x + i, y + j)) != c
                   for i in (-1, 0, 1) for j in (-1, 0, 1) if (i, j) != (0, 0)):
                orphans += 1
        if orphans > 8:
            warn.append(f"고립 픽셀 {orphans}개 - 노이즈처럼 보일 수 있음 (8개 이하 권장)")
        # 실루엣 조각 수
        seen, parts = set(), 0
        for p in self.pix:
            if p in seen:
                continue
            parts += 1
            stack = [p]
            while stack:
                q = stack.pop()
                if q in seen or q not in self.pix:
                    continue
                seen.add(q)
                stack += [(q[0] + i, q[1] + j) for i in (-1, 0, 1) for j in (-1, 0, 1)]
        if parts > 3:
            warn.append(f"실루엣이 {parts}조각으로 흩어짐 (3 이하 권장)")
        return err, warn
