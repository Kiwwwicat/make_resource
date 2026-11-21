from pixelkit import blob, poly, rect, line


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
    c.fill(side, "yellow1")
    c.fill(line(23, 14, 28, 9), "yellow2")
    c.recolor(side & rect(0, 22, 31, 22), "red1")
    c.recolor(side & rect(0, 20, 31, 21), "cream1")
    c.fill(top, "cream3")
    c.fill(line(4, 14, 8, 10), "cream4")
    c.fill(line(8, 9, 28, 9), "cream4")
    c.fill(line(3, 14, 23, 14), "cream4")
    # strawberry: 위가 넓고 아래가 좁은 유기적 형태, 케이크 윗면에 그림자
    berry = blob([(12, 6), (16, 4.8), (20.5, 5.8), (20, 9), (17.5, 12), (15.5, 12.4), (13, 10)])
    c.cast(berry)
    c.fill(berry, "red")
    c.fill({(15, 8), (18, 7), (16, 10), (19, 9), (13, 9)}, "red1")
    leaf = blob([(12.5, 5), (14, 3), (16.5, 2.3), (19, 3), (20, 5), (16.5, 5.5)])
    c.fill(leaf, "green2")
    c.fill({(13, 4), (14, 3), (15, 3)}, "green3")
    c.fill({(18, 5), (19, 5), (19, 4)}, "green1")
