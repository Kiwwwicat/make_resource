from pixelkit import ellipse


def draw(c):
    hole = ellipse(15.5, 16, 4.2, 3.6)
    dough = ellipse(15.5, 16, 13.5, 12.5) - hole
    c.fill(dough, "tan")
    # glaze: slightly smaller and shifted up so dough rim shows at bottom
    glaze = ellipse(15.5, 15, 12, 10.5)
    c.fill(glaze, "pink")
    c.erase(hole)
    ring = ellipse(15.5, 16, 5.4, 4.6) - hole
    c.fill(ring, "pink2")
    c.fill({(x, y) for (x, y) in ring if (x + 1, y + 1) not in ring and (x+1,y+1) not in hole}, "pink1")
    c.fill({(9, 11), (10, 10), (11, 9), (12, 8), (13, 8), (8, 12)}, "pink4")
    # sprinkles
    for (x, y, col) in [(9, 15, "yellow3"), (10, 15, "yellow3"), (20, 10, "blue3"), (21, 11, "blue3"),
                        (14, 7, "cream3"), (15, 7, "cream3"), (22, 17, "yellow3"), (22, 18, "yellow3"),
                        (13, 21, "blue3"), (14, 21, "blue3"), (19, 21, "cream3"), (18, 21, "cream3"),
                        (7, 17, "blue3"), (24, 14, "cream3")]:
        c.px(x, y, col)
