from pixelkit import ellipse, rect, poly, line


def draw(c):
    # bowl body: lower half of a wide ellipse
    body = ellipse(15.5, 16, 13, 12) & rect(0, 17, 31, 29)
    body |= rect(3, 15, 28, 18)
    c.fill(body, "brown")
    # rim + stew surface
    rim = ellipse(15.5, 15.5, 13, 4.5)
    c.fill(rim, "brown3")
    c.fill(ellipse(15.5, 16, 11, 3.2), "orange2")
    c.fill(ellipse(15.5, 17, 10, 2.2), "orange1")
    c.fill(ellipse(14.5, 15.3, 9.5, 2.4), "orange2")
    # bowl base
    c.fill(rect(10, 27, 21, 28), "brown1")
    # bowl band
    c.line(5, 21, 26, 21, "brown1")
    # chunks
    c.fill({(9, 15), (10, 15), (9, 16), (10, 16)}, "orange3")
    c.fill({(19, 14), (20, 14), (19, 15), (20, 15), (21, 15)}, "red2")
    c.fill({(14, 16), (15, 16), (14, 17), (15, 17)}, "red2")
    c.fill({(16, 14), (17, 14)}, "green2")
    c.fill({(12, 17), (22, 16)}, "green2")
    c.fill({(7, 16), (8, 16)}, "orange4")
    # bowl highlight
    c.fill({(5, 19), (5, 20), (6, 22), (6, 23)}, "brown4")
    # steam
    c.fill({(10, 11), (11, 11), (10, 10), (9, 9), (9, 8), (10, 7), (10, 6), (9, 5)}, "gray3")
    c.fill({(20, 11), (21, 11), (21, 10), (22, 9), (22, 8), (21, 7), (21, 6), (22, 5)}, "gray3")
    c.fill({(15, 10), (16, 10), (16, 9), (15, 8), (15, 7), (16, 6), (16, 5), (15, 4)}, "gray4")
