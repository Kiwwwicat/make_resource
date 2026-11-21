from pixelkit import blob, line


def draw(c):
    # leaves first (behind), three fronds fanning to the upper right
    fa = blob([(19, 9), (17, 6), (17.5, 2.5), (20, 5.5), (21.5, 8.5)])
    fb = blob([(21.5, 8.5), (22.5, 5.5), (28.5, 2.5), (26, 7.5), (24, 9.5)])
    fc = blob([(24, 9), (26, 7.5), (29.5, 8.5), (27.5, 11), (24.5, 12)])
    leaves = fa | fb | fc
    c.fill(leaves, "green")
    c.recolor(line(21, 8, 21, 6), "green1")
    c.recolor(line(25, 9, 26, 7), "green1")
    # root along the diagonal: thick shoulder at upper right, straight taper to lower-left tip
    body = blob([(4, 27), (5.3, 24.3), (8.4, 19.4), (11.7, 14.7), (15, 10), (18.8, 6.5),
                 (22.8, 6.8), (25.2, 12.2), (21, 16), (16.3, 19.3), (11.6, 22.6), (6.7, 25.7)])
    c.cast(body)
    c.fill(body, "orange")
    # curved ridge marks across the body
    for pts in (((14, 12), (16, 12), (18, 13), (19, 15)), ((11, 16), (13, 16), (15, 17), (16, 19)),
                ((8, 20), (10, 20), (12, 21)), ((19, 9), (21, 9), (23, 10), (24, 12))):
        for a, b in zip(pts, pts[1:]):
            c.recolor(line(*a, *b) & body, "orange1")
