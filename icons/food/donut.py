from pixelkit import blob


def draw(c):
    # dough: slightly lumpy, heavier at the bottom
    dough = blob([
        (15.5, 3.5), (22, 4.5), (27.5, 10), (28, 17), (24.5, 25), (16.5, 28.5),
        (8.5, 27), (3.5, 21), (3.5, 12), (8, 6),
    ])
    hole = blob([(15, 12.5), (18.5, 13.5), (19.5, 16.5), (17, 19.5), (13.5, 19), (11.5, 16), (12.5, 13.5)])
    c.fill(dough, "tan")
    # glaze: wavy edge with a couple of drips toward the bottom
    glaze = blob([
        (15.5, 5.5), (21.5, 6.5), (26, 11), (26, 17), (24.5, 21), (22, 23.5), (20, 21.5),
        (17.5, 24), (15, 26), (12.5, 23.5), (9.5, 24), (6.5, 20.5), (5.5, 14), (8, 8.5),
    ])
    c.cast(glaze)
    c.fill(glaze, "pink")
    # hole with depth
    c.erase(hole)
    rim = blob([(15, 11.5), (19.5, 12.5), (21, 16.5), (17.5, 20.5), (13, 20), (10.5, 16), (11.5, 12.5)]) - hole
    inner = {p for p in rim if p in c.pix}
    c.fill({(x, y) for (x, y) in inner if (x + 1, y) in hole or (x, y + 1) in hole}, "pink1")
    c.fill({(x, y) for (x, y) in inner if (x - 1, y) in hole or (x, y - 1) in hole}, "pink3")
    # sprinkles in 3 colours, short 2px bars at varied angles
    for pts, col in [
        ([(9, 12), (10, 11)], "yellow3"), ([(22, 9), (23, 10)], "yellow3"), ([(21, 23)], "yellow3"),
        ([(14, 8), (15, 8)], "blue3"), ([(23, 15), (23, 16)], "blue3"), ([(11, 22), (12, 22)], "blue3"),
        ([(18, 8)], "cream4"), ([(7, 17), (7, 18)], "cream4"), ([(20, 22), (21, 21)], "cream4"),
        ([(10, 8)], "blue3"),
    ]:
        for p in pts:
            c.px(*p, col)
    c.fill({(9, 7), (10, 7), (11, 6), (8, 9)}, "pink4")
