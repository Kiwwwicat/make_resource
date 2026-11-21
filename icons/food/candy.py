from pixelkit import blob, poly, line, rect


def draw(c):
    # wrapper ends: tight knot at the ball, fan widening to the canvas edge, zig-zag outer edge
    left = poly([(8, 15), (2, 10), (4, 12.5), (2, 15), (4, 17.5), (2, 20), (8, 16)]) | rect(7, 15, 8, 16)
    right = poly([(23, 15), (29, 9), (27, 12), (29, 14.5), (27, 17.5), (29, 21), (23, 16)]) | rect(23, 15, 24, 16)
    c.fill(left, "teal2")
    c.fill(right, "teal2")
    # creases radiating from the knot
    c.recolor(line(7, 15, 3, 11) | line(7, 15, 4, 14), "teal1")
    c.recolor(line(7, 16, 3, 17) | line(6, 16, 3, 19), "teal3")
    c.recolor(line(7, 16, 3, 20), "teal1")
    c.recolor(line(24, 15, 28, 10) | line(24, 15, 27, 14), "teal3")
    c.recolor(line(24, 16, 28, 16), "teal1")
    c.recolor(line(24, 16, 28, 21) | line(25, 17, 28, 21), "teal1")
    c.recolor(line(24, 15, 28, 12), "teal1")
    # ball
    ball = blob([(15.5, 8), (20, 9), (22.5, 13), (22.5, 18), (20, 22), (15.5, 23.5), (11, 22),
                 (8.5, 18.5), (8.5, 13), (11, 9)])
    c.cast(ball)
    c.fill(ball, "red")
    # two curved cream stripes
    for k in (-3, 3):
        s = line(14 + k, 8, 13 + k, 14) | line(13 + k, 14, 14 + k, 23)
        c.recolor(s | {(x + 1, y) for x, y in s}, "cream3")
