from pixelkit import ellipse, rect, line


def draw(c):
    # side wall (tin edge) = top ellipse shifted down, behind the top
    side = ellipse(15.5, 18.5, 13, 8.5)
    c.fill(side, "tan1")
    c.fill(ellipse(15.5, 17.5, 13, 8.5) & rect(0, 0, 8, 31), "tan2")  # soft left light
    # crust rim and filling
    top = ellipse(15.5, 14, 13, 8.5)
    c.fill(top, "tan3")
    inner = ellipse(15.5, 14.5, 11, 6.6)
    c.fill(inner, "red1")
    c.fill(ellipse(14.5, 13.5, 9.5, 5.2), "red2")
    # lattice strips (dough), 2px wide, clipped to filling
    for k in range(-3, 4):
        x = 15 + k * 6
        c.fill(line(x - 6, 20, x + 6, 8, 1) & inner, "tan3")
        c.fill(line(x + 6, 20, x - 6, 8, 1) & inner, "tan3")
    for x, y in [(6, 9), (24, 8), (16, 5), (4, 13)]:
        c.px(x, y, "tan4")
    # side shadow band
    c.fill({(x, y) for (x, y) in side if y >= 24 and (x, y) not in top}, "tan1")
