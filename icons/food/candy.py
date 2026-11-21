from pixelkit import ellipse, poly, line


def draw(c):
    # wrapper twists (behind body)
    left = poly([(9, 14), (3, 8), (2, 10), (4, 15), (2, 21), (3, 23), (9, 17)])
    right = poly([(22, 14), (28, 8), (29, 10), (27, 15), (29, 21), (28, 23), (22, 17)])
    c.fill(left, "teal2")
    c.fill(right, "teal2")
    c.line(8, 15, 3, 10, "teal3")
    c.line(8, 16, 4, 20, "teal1")
    c.line(23, 15, 28, 10, "teal3")
    c.line(23, 16, 27, 20, "teal1")
    # body
    body = ellipse(15.5, 15.5, 8.5, 8)
    c.fill(body, "red")
    # diagonal cream stripes
    for k in (-3, 3):
        c.recolor(line(14 + k, 8, 11 + k, 23, 2) & body, "cream3")
    c.fill({(11, 10), (12, 9), (13, 8), (10, 11), (10, 12)}, "red4")
    # twist ties
    c.rect(8, 13, 9, 18, "teal1")
    c.rect(22, 13, 23, 18, "teal1")
