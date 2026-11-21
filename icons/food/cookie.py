from pixelkit import ellipse


def draw(c):
    body = ellipse(15.5, 16, 13, 12.5)
    # bite: three overlapping circles scooped from the top-right
    bite = ellipse(21, 6, 3.6, 3.6) | ellipse(25.5, 9, 3.6, 3.6) | ellipse(27, 14, 3.2, 3.2) | ellipse(24, 3, 3.6, 3.6)
    c.fill(body - bite, "tan", shadow=2, light=2)
    # bite edge: lighter inner crumb along the cut
    edge = {(x, y) for (x, y) in body - bite
            if any((x + i, y + j) in bite for i in (-1, 0, 1) for j in (-1, 0, 1))}
    c.fill(edge, "tan3")
    # chocolate chips (fixed colours, 2-3px lumps)
    chips = [(8, 11), (15, 8), (11, 17), (20, 16), (7, 22), (15, 22), (22, 22), (17, 13)]
    for x, y in chips:
        c.fill({(x, y), (x + 1, y), (x + 2, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1)}, "brown1")
        c.px(x, y, "brown2")
    # highlights top-left
    c.fill({(6, 14), (6, 15), (7, 12), (8, 11), (10, 7), (11, 6)}, "tan4")
