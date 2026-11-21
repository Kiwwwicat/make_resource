from pixelkit import ellipse, rect, poly


def draw(c):
    # saucer
    c.fill(ellipse(15.5, 24, 13, 4.2), "cream")
    c.fill(ellipse(15.5, 23.2, 7.5, 2), "cream1")
    # handle (right)
    ring = ellipse(24.5, 16.5, 4.5, 4.5) - ellipse(24.5, 16.5, 2, 2.2)
    c.fill(ring - rect(0, 0, 22, 31), "cream2")
    # cup body
    body = (ellipse(15, 13, 10, 10) & rect(0, 12, 31, 31)) | rect(5, 12, 25, 14)
    c.fill(body, "cream")
    # blue band
    c.recolor(rect(0, 16, 31, 17) & body, "blue2")
    c.recolor(rect(0, 17, 31, 17) & body, "blue1")
    # tea surface
    c.fill(ellipse(15, 12.5, 9.2, 2.3), "brown1")
    c.fill(ellipse(15, 13, 8, 1.5), "brown2")
    c.fill({(10, 12), (11, 12), (12, 12)}, "brown3")
    # rim highlight
    c.fill({(6, 14), (6, 15), (7, 16)}, "cream4")
    # steam
    for (x, y0) in [(11, 4), (17, 3)]:
        pts = [(x, y0 + 8), (x + 1, y0 + 7), (x + 1, y0 + 6), (x, y0 + 5), (x, y0 + 4),
               (x + 1, y0 + 3), (x + 1, y0 + 2)]
        for i, p in enumerate(pts):
            c.px(*p, "gray3")
            c.px(p[0] + 1, p[1], "gray2")
