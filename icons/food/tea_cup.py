from pixelkit import ellipse, rect


def draw(c):
    # saucer
    sauc = ellipse(15.5, 24.5, 13, 3.6)
    c.fill(sauc, "cream3")
    c.fill({(x, y) for (x, y) in sauc if (x + 1, y + 1) not in sauc or (x, y + 1) not in sauc}, "cream2")
    c.fill(ellipse(15.5, 23.8, 8, 1.6), "cream2")
    # handle (right)
    ring = (ellipse(24.5, 15.5, 4.4, 4.2) - ellipse(24.5, 15.5, 2, 2)) - rect(0, 0, 21, 31)
    c.fill(ring, "cream3")
    c.fill({(x, y) for (x, y) in ring if (x + 1, y + 1) not in ring}, "cream2")
    # cup body, flat-shaded in vertical bands (rounder = darker toward right/bottom)
    body = (ellipse(14.5, 12, 9.5, 10) & rect(0, 11, 31, 31)) | rect(5, 11, 24, 13)
    c.fill(body, "cream3")
    c.fill({(x, y) for (x, y) in body if (x + 3, y + 1) not in body or (x + 1, y + 3) not in body}, "cream2")
    c.fill({(x, y) for (x, y) in body if (x + 1, y + 1) not in body and (x, y) in body and y > 17}, "cream1")
    # blue band
    c.recolor(rect(0, 16, 31, 16) & body, "blue2")
    c.recolor(rect(0, 17, 31, 17) & body, "blue1")
    # tea surface
    c.fill(ellipse(14.5, 11.5, 9.5, 2.4), "cream4")
    c.fill(ellipse(14.5, 11.8, 8.2, 1.7), "brown2")
    c.fill(rect(8, 11, 11, 11), "brown3")
    c.fill({(6, 14), (6, 15), (7, 16)} if False else {(6, 13), (6, 14)}, "cream4")
    # steam
    for x0 in (10, 17):
        for i, (dx, y) in enumerate([(0, 8), (1, 7), (1, 6), (0, 5), (0, 4), (1, 3), (1, 2)]):
            c.px(x0 + dx, y, "gray4")
            c.px(x0 + dx + 1, y, "gray3")
