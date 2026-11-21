import math
from pixelkit import ellipse


def draw(c):
    a = math.radians(-30)
    ca, sa = math.cos(a), math.sin(a)
    body = set()
    for y in range(32):
        for x in range(32):
            u = (x - 15.5) * ca + (y - 15.5) * sa
            v = -(x - 15.5) * sa + (y - 15.5) * ca
            if abs(u) < 11.5 and abs(v) <= 9.5 * (1 - (abs(u) / 11.5) ** 2) ** 0.5:
                body.add((x, y))
    body |= ellipse(27, 9, 2.2, 2.2) | ellipse(4, 22, 2.2, 2.2)
    c.fill(body, "yellow", light=2, shadow=2)
    c.fill({(9, 15), (9, 16), (10, 13), (11, 12), (13, 11), (10, 14)}, "yellow4")
    # 껍질 질감 점
    for (x, y) in [(15, 17), (19, 14), (12, 20), (21, 19)]:
        c.px(x, y, "yellow1")
