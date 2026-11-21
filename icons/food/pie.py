import math
from pixelkit import ellipse, rect


def draw(c):
    N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    # (a) side wall / tin: lower part, shifted down
    wall = ellipse(15.5, 16.5, 13, 6.5)
    top = ellipse(15.5, 13, 13, 6.5)
    c.fill(wall, "tan1")
    vis = wall - top
    c.fill({(x, y) for (x, y) in vis if (x, y - 1) in top}, "tan2")
    # (b) top crust
    c.cast(top)
    c.fill(top, "tan", round=3)
    # (c) recessed filling opening
    op = ellipse(15.5, 13, 9.5, 4.5)
    c.fill(op, "red2")
    c.fill({(x, y) for (x, y) in op if (x - 1, y) not in op or (x, y - 1) not in op}, "red1")
    c.fill({(x, y) for (x, y) in op if (x - 1, y - 1) not in op and (x - 1, y) in op and (x, y - 1) in op}, "red1")
    for p in ((17, 15), (12, 16), (21, 14)):
        if p in op:
            c.px(p[0], p[1], "red3")
    # (d) lattice of straight strips
    strips = set()
    for x in (9, 14, 19):
        strips |= rect(x, 0, x + 1, 31)
    for y in (10, 14):
        strips |= rect(0, y, 31, y + 1)
    strips &= op
    c.cast(strips)
    c.fill(strips, "tan3")
    c.fill({(x, y) for (x, y) in strips if (x + 1, y) not in strips or (x, y + 1) not in strips}, "tan2")
    # (e) crimped rim along outer crust ring
    ring = [(x, y) for (x, y) in top if any((x + dx, y + dy) not in top for dx, dy in N4)]
    ring.sort(key=lambda p: math.atan2(p[1] - 13, (p[0] - 15.5) * 0.5))
    n = len(ring)
    for i, (x, y) in enumerate(ring):
        k = (i * 22 // n) % 2
        nx, ny = (x - 15.5) / 13, (y - 13) / 6.5
        lit = (-nx - ny) > 0
        if lit:
            col = "tan3" if k == 0 else "tan2"
        else:
            col = "tan2" if k == 0 else "tan1"
        c.px(x, y, col)
