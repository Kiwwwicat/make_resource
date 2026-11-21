from pixelkit import blob, line


def draw(c):
    # wrapper twists (behind body): ragged fans, slightly different left/right
    left = blob([(9, 14), (6.5, 10.5), (3, 7.5), (2.5, 11.5), (4.5, 15.5), (2.5, 19.5), (3, 24), (7, 20.5), (9, 18)])
    right = blob([(22, 14), (25, 10), (28.5, 8.5), (29, 12.5), (26.5, 15.5), (28.5, 20), (27, 23.5), (24, 20.5), (22, 18)])
    c.fill(left, "teal", round=2)
    c.fill(right, "teal", round=2)
    # crease lines in the wrapper
    c.line(8, 14, 4, 10, "teal1")
    c.line(8, 17, 4, 21, "teal1")
    c.line(23, 14, 27, 10, "teal3")
    c.line(23, 17, 27, 21, "teal1")
    # body: plump, asymmetric, heavier at the bottom right
    body = blob([
        (14.5, 6), (20, 6.5), (24.5, 10.5), (25, 16), (23, 22), (17.5, 25), (11, 24.5),
        (6.5, 20.5), (6, 14), (9, 8.5),
    ])
    c.cast(body)
    c.fill(body, "red")
    # diagonal cream stripes, kept on top of the shaded body
    for k in (-3, 3):
        c.recolor(line(15 + k, 6, 12 + k, 25, 2) & body, "cream3")
    c.fill({(11, 10), (12, 9), (13, 8), (10, 11), (9, 12)}, "red4")
    # twist ties
    c.rect(6, 13, 7, 18, "teal1")
    c.rect(25, 13, 26, 18, "teal1")
