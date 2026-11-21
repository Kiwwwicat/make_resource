import math
from pixelkit import SIZE, line, poly

CX, CY = 14, 14


def rot_ellipse(cx, cy, a, b, ang_deg):
    """대각선으로 기울인 타원 (a=긴 반지름, b=짧은 반지름)."""
    t = math.radians(ang_deg)
    ct, st = math.cos(t), math.sin(t)
    out = set()
    for y in range(SIZE):
        for x in range(SIZE):
            u = (x - cx) * ct + (y - cy) * st
            v = -(x - cx) * st + (y - cy) * ct
            if (u / a) ** 2 + (v / b) ** 2 <= 1:
                out.add((x, y))
    return out


def draw(c):
    # 꼬리 (오른쪽 아래, 두 갈래)
    tail = poly([(19, 19), (29, 22), (25, 25), (22, 29)])
    c.fill(tail, "orange2")
    c.fill({(x, y) for (x, y) in tail if (x + y) >= 49 or x - y >= 3 and y > 21}, "orange1")
    # 등지느러미 (오른쪽 위) / 배지느러미 (왼쪽 아래)
    c.fill(poly([(14, 8), (19, 3), (22, 8), (19, 11)]), "orange1")
    c.fill(poly([(8, 20), (4, 24), (9, 25), (12, 22)]), "orange1")
    # 몸통
    body = rot_ellipse(CX, CY, 11.5, 6.5, 45)
    c.fill(body, "orange", light=2, shadow=3)
    # 배 (왼쪽 아래) 밝은 살
    belly = {(x, y) for (x, y) in body if (-(x - CX) + (y - CY)) * 0.707 > 3.2}
    c.recolor(belly, "orange3")
    # 석쇠 자국: 몸통을 가로지르는 짧은 줄
    for u in (-1, 3, 7):
        px, py = CX + u * 0.707, CY + u * 0.707
        mark = line(round(px + 3), round(py - 3), round(px - 3), round(py + 3))
        c.fill(mark & body, "brown1")
    # 눈, 하이라이트
    c.fill({(7, 9), (8, 9), (7, 10), (8, 10)}, "cream4")
    c.px(7, 10, "brown0")
    c.fill({(9, 7), (10, 7), (11, 8)}, "orange4")
