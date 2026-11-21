from pixelkit import ellipse, poly, rect, line


def draw(c):
    front = rect(3, 14, 22, 27)
    side = poly([(23, 14), (28, 9), (28, 22), (23, 27)])
    top = poly([(3, 14), (8, 9), (28, 9), (23, 14)])
    # cut face layers (flat fixed colours)
    c.fill(front, "yellow3")
    c.fill(rect(3, 14, 22, 15), "cream3")          # top cream
    c.fill(rect(3, 20, 22, 21), "cream3")          # middle cream
    c.fill(rect(3, 22, 22, 22), "red2")            # jam line
    c.fill(rect(3, 26, 22, 27), "yellow1")         # bottom shade
    c.fill(rect(3, 23, 22, 25), "yellow2")
    c.fill(rect(3, 16, 22, 19), "yellow2")
    c.fill(rect(3, 16, 22, 16), "yellow3")
    # sponge crumb pores
    for x, y in [(7, 18), (14, 17), (18, 24), (9, 24)]:
        c.px(x, y, "yellow1")
    # right side face (shadow) and top
    c.fill(side, "cream1")
    c.fill(line(23, 14, 28, 9), "cream2")
    c.recolor(side & rect(0, 16, 31, 19) | side & rect(0, 23, 31, 25), "yellow1")
    c.recolor(side & rect(0, 22, 31, 22), "red1")
    c.fill(top, "cream3")
    c.fill(line(4, 14, 8, 10), "cream4")
    c.fill(line(8, 9, 28, 9), "cream4")
    c.fill(line(3, 14, 23, 14), "cream4")
    # strawberry
    c.fill(ellipse(16, 8, 4.5, 4), "red")
    c.fill({(13, 7), (13, 6), (14, 5)}, "red4")
    c.fill({(15, 8), (17, 7), (16, 10), (18, 9)}, "red1")
    c.fill({(14, 3), (15, 4), (16, 4), (17, 3), (18, 3), (16, 3), (15, 3)}, "green2")
    c.fill({(16, 2), (17, 2)}, "green3")
