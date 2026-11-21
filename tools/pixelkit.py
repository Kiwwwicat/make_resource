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
    "cream":  ["5f4a44", "b8a999", "d8c7a8", "f2e8cf", "fffaf0"],
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
def _spikes(mask):
    """평평한 변 위에 혼자 튀어나온 1px (가시). 뾰족한 끝(1->3px)은 허용."""
    bad = set()
    for (x, y) in mask:
        nb = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) in mask]
        if len(nb) != 1:
            continue
        dx, dy = nb[0]
        qx, qy = x + dx, y + dy
        px_, py_ = dy, dx  # 수직 방향
        if all((qx + k * px_, qy + k * py_) in mask for k in (-2, -1, 1, 2)):
            bad.add((x, y))
    return bad


def _notches(mask):
    """평평한 변에 혼자 파인 1px."""
    D = ((1, 0), (-1, 0), (0, 1), (0, -1))
    cand = {(x + dx, y + dy) for (x, y) in mask for dx, dy in D} - mask
    bad = set()
    for (x, y) in cand:
        miss = [d for d in D if (x + d[0], y + d[1]) not in mask]
        if len(miss) != 1:
            continue
        ex, ey = miss[0][1], miss[0][0]  # 변 방향
        if all((x + k * ex, y + k * ey) in mask for k in (-2, -1, 1, 2)):
            bad.add((x, y))
    return bad


def despike(mask):
    """실루엣의 가시 픽셀을 깎고 1px 홈을 메운다. ellipse/blob/자동 명암 fill에 자동 적용."""
    mask = set(mask)
    for _ in range(3):
        sp = _spikes(mask)
        mask -= sp
        no = _notches(mask)
        mask |= no
        if not sp and not no:
            break
    return mask


def blob(points, steps=10):
    """조절점들을 부드럽게 잇는 닫힌 곡선(Catmull-Rom)으로 채운 유기적 실루엣.
    과일·고기·빵처럼 자연물은 타원 합성 대신 이것으로 외형을 잡는다 (조절점 6~12개, 시계 방향)."""
    n = len(points)
    curve = []
    for i in range(n):
        p0, p1, p2, p3 = (points[(i + k - 1) % n] for k in range(4))
        for t in (j / steps for j in range(steps)):
            t2, t3 = t * t, t * t * t
            curve.append(tuple(
                0.5 * (2 * p1[a] + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                       + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out = set()
    m = len(curve)
    for y in range(SIZE):
        for x in range(SIZE):
            inside = False
            for i in range(m):
                (xa, ya), (xb, yb) = curve[i], curve[(i + 1) % m]
                if (ya > y) != (yb > y) and x < (xb - xa) * (y - ya) / (yb - ya) + xa:
                    inside = not inside
            if inside:
                out.add((x, y))
    return despike(out)


def _volume(mask, round_=None):
    """좌상단 광원의 입체 명암. 가장자리에서 안쪽으로 부풀어 오른 높이맵을 만들고
    법선·광원 내적을 1/2/3/4 단계로 양자화한다. round_ = 모서리가 둥글어지는 깊이(px).
    None이면 덩어리 전체가 돔(공)처럼, 작은 값이면 납작한 판의 모서리만 둥글게."""
    import math
    outside = {(x + dx, y + dy) for (x, y) in mask
               for dx in (-1, 0, 1) for dy in (-1, 0, 1)} - mask
    dist = {p: min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in outside) - 0.5 for p in mask}
    R = max(dist.values())
    r = max(1.0, min(R, round_) if round_ else R)
    H = {}
    for p, d in dist.items():
        t = min(d / r, 1.0)
        H[p] = r * math.sqrt(max(0.0, 1 - (1 - t) ** 2))
    for _ in range(2):  # 높이맵을 살짝 흐려 계단 무늬 제거
        H = {(x, y): sum(H.get((x + i, y + j), 0.0) for i in (-1, 0, 1) for j in (-1, 0, 1)) / 9
             for (x, y) in mask}
    L = (-0.45, -0.42, 0.79)
    shades, val = {}, {}
    for (x, y) in mask:
        gx = (H.get((x + 1, y), 0.0) - H.get((x - 1, y), 0.0)) / 2
        gy = (H.get((x, y + 1), 0.0) - H.get((x, y - 1), 0.0)) / 2
        nl = math.sqrt(gx * gx + gy * gy + 1)
        v = (-gx * L[0] - gy * L[1] + L[2]) / nl
        val[(x, y)] = v
        shades[(x, y)] = 1 if v < 0.45 else 2 if v < 0.83 else 3 if v < 0.975 else 4
    # 하이라이트(4)는 3~4px 한 덩어리, 작은 덩어리에는 생략
    hi = sorted((p for p in shades if shades[p] == 4), key=lambda p: (-val[p], p))
    keep = set()
    if len(hi) >= 2:  # 가장 밝은 점 주변 2x2 + 꼬리 1px 형태로 정리
        bx, by = hi[0]
        keep = {q for q in ((bx, by), (bx + 1, by), (bx, by + 1), (bx - 1, by + 1)) if shades.get(q, 0) >= 3}
    for p in hi:
        shades[p] = 3
    for p in keep:
        shades[p] = 4
    # 고립된 명암 픽셀 정리
    for _ in range(2):
        for (x, y), s_ in list(shades.items()):
            nb = [shades[q] for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)) if q in shades]
            if nb and s_ not in nb and s_ != 4:
                shades[(x, y)] = Counter(nb).most_common(1)[0][0]
    return shades


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
    return despike(out)


def line(x0, y0, x1, y1, width=1):
    """브레젠험 직선. width>1 이면 오른쪽/아래로 두꺼워진다."""
    pts = set()
    x0, y0, x1, y1 = round(x0), round(y0), round(x1), round(y1)
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

    def fill(self, mask, color, round=None, light=None, shadow=None):
        """mask를 칠한다.
        color='red3' (단계 포함) -> 그 색 그대로.
        color='red'  (램프 이름) -> 자동 입체 명암. round=None이면 덩어리 전체가 둥글게,
            round=2~4면 납작한 물체의 모서리만 둥글게 (빵 윗면, 접시, 병 몸통 등).
        light/shadow 는 구버전 띠 명암(호환용). 새 아이콘에서는 쓰지 않는다."""
        ramp, shade = parse_color(color)
        mask = set(mask)
        if not mask:
            return mask
        if shade is not None:
            for p in mask:
                self.pix[p] = (ramp, shade)
            return mask
        mask = despike(mask)
        if light is None and shadow is None:
            for p, s in _volume(mask, round).items():
                self.pix[p] = (ramp, s)
            return mask
        light, shadow = light or 0, shadow or 0
        for (x, y) in mask:
            s = 2
            if any((x + k, y + k) not in mask for k in range(1, shadow + 1)):
                s = 1
            elif any((x - k, y - k) not in mask for k in range(1, light + 1)):
                s = 3
            self.pix[(x, y)] = (ramp, s)
        return mask

    def cast(self, mask, dx=1, dy=1, depth=2):
        """mask(위에 얹힌 부품)가 아래 물체에 드리우는 그림자: 우하단으로 depth px 만큼
        이미 칠해진 픽셀을 한 단계 어둡게. 부품을 fill 하기 '전에' 호출한다."""
        mask = set(mask)
        hit = {(x + dx * k, y + dy * k) for (x, y) in mask for k in range(1, depth + 1)} - mask
        for p in hit & set(self.pix):
            ramp, s = self.pix[p]
            self.pix[p] = (ramp, max(1, min(s, 3) - 1))

    def blob(self, points, color, **kw):
        return self.fill(blob(points), color, **kw)

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

    def lint(self, lo=FILL_MIN, hi=FILL_MAX, max_ramps=5, max_colors=16):
        """(errors, warnings) 목록. errors가 있으면 납품 불가."""
        err, warn = [], []
        if not self.pix:
            return ["아무것도 그려지지 않음"], []
        xs = [p[0] for p in self.pix]
        ys = [p[1] for p in self.pix]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if x0 < lo or y0 < lo or x1 > hi or y1 > hi:
            err.append(f"채색 영역 초과: x {x0}..{x1}, y {y0}..{y1} (허용 {lo}..{hi})")
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if max(w, h) < 22:
            err.append(f"너무 작음: {w}x{h} (긴 변이 22px 이상이어야 함, 권장 24~28)")
        if min(w, h) < 8:
            warn.append(f"매우 가늚: {w}x{h} - 대각선 배치를 고려")
        cx, cy = (x0 + x1) / 2 - 15.5, (y0 + y1) / 2 - 15.5
        if abs(cx) > 1.5 or abs(cy) > 1.5:
            err.append(f"중심 어긋남: dx={cx:+.1f}, dy={cy:+.1f} (허용 ±1.5)")
        ramps = Counter(r for r, _ in self.pix.values())
        if len(ramps) > max_ramps:
            err.append(f"램프 과다: {len(ramps)}개 {sorted(ramps)} (최대 {max_ramps})")
        colors = set(self.pix.values())
        if len(colors) > max_colors:
            err.append(f"색 과다: {len(colors)}색 (최대 {max_colors})")
        if len(colors) < 3:
            err.append("명암 없음: 3색 미만")
        sp = sorted(_spikes(set(self.pix)))
        if sp:
            err.append(f"가시 픽셀 {len(sp)}개 {sp[:6]} - 평평한 변 위에 1px만 튀어나옴. 지우거나 2px 이상으로")
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
