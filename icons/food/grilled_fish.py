from pixelkit import SIZE, line, poly


def rot_ellipse(cx, cy, a, b, ang_deg):
    """대각선으로 기울인 타원 (a=긴 반지름, b=짧은 반지름)."""
    import math
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
    # 꼬리 (오른쪽 아래)
    tail = poly([(21, 21), (28, 28), (28, 20), (25, 16)]) | poly([(21, 21), (28, 28), (19, 28), (17, 24)])
    c.fill(tail, "orange2")
    c.fill(line(22, 22, 27, 27), "orange1")
    # 지느러미 (등/배)
    c.fill(poly([(10, 8), (12, 4), (17, 6), (17, 9)]), "orange1")
    c.fill(poly([(12, 21), (11, 26), (17, 24), (18, 21)]), "orange1")
    # 몸통
    body = rot_ellipse(14.5, 15.5, 12.5, 7, 40)
    c.fill(body, "orange", light=2, shadow=3)
    # 배 쪽 밝은 살색
    c.fill({(x, y) for (x, y) in body if (x - 15.5) * 0.77 - (y - 15.5) * 0.64 < -4 and False}, "cream3")
    # 석쇠 자국
    for k in (0, 1, 2):
        c.fill(line(11 + 4 * k, 17 + 0 * k - 4 + 4 * k - 4 * k + 0, 14 + 4 * k, 20 - 4 + 4 * k - 0) & body, "brown1") if False else None
    c.fill(line(12, 10, 17, 15) & body, "brown1")
    c.fill(line(15, 8, 21, 14) & body, "brown1")
    c.fill(line(10, 14, 15, 19) & body, "brown1")
    # 눈
    c.fill({(6, 9), (7, 9), (6, 10), (7, 10)}, "cream4")
    c.px(7, 10, "brown0")
    # 하이라이트
    c.fill({(8, 7), (9, 6), (10, 6)}, "orange4")
