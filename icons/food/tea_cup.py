from pixelkit import blob, rect, line


def draw(c):
    # saucer: wide flat dish, a touch lopsided
    saucer = blob([(15, 21.5), (22, 22), (28, 24), (28, 26.5), (22, 28.5), (14, 28.7), (6, 28), (2.5, 26), (3, 23.5), (8, 22)])
    c.fill(saucer, "cream", round=2)
    # handle (behind the cup, right)
    outer = blob([(20, 10), (25.5, 9), (29, 13), (28.5, 18.5), (24.5, 21.5), (20, 20)])
    inner = blob([(22, 13), (25, 12.5), (26.5, 15), (25.5, 17.5), (22.5, 17.5)])
    c.fill(outer - inner, "cream", round=2)
    # cup body: bowl, wider at the rim, rounded bottom
    cup = blob([(4.5, 10.5), (13, 9.5), (21.5, 10.5), (21.5, 15.5), (19.5, 21.5), (14, 24.5), (8.5, 22), (5.5, 16.5)])
    c.cast(cup)
    c.fill(cup, "cream", round=3)
    # blue band
    c.recolor(rect(0, 17, 31, 17) & cup, "blue2")
    c.recolor(rect(0, 18, 31, 18) & cup, "blue1")
    # tea surface seen from slightly above
    tea = blob([(5, 10.8), (13, 9.6), (21.5, 10.8), (20.5, 12.6), (13, 13.6), (6.5, 12.6)])
    c.fill(tea, "brown", round=2)
    # vertical glaze highlight on the left of the cup
    c.fill({(6, y) for y in range(15, 21)}, "cream4")
    # steam: two short wisps
    for x0 in (10, 17):
        for dx, y in [(0, 7), (1, 6), (1, 5), (0, 4), (0, 3)]:
            c.px(x0 + dx, y, "gray3")
