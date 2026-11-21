from pixelkit import poly, rect


def draw(c):
    tri = poly([(14, 4), (17, 4), (27, 23), (27, 26), (24, 28), (7, 28), (4, 26), (4, 23)])
    c.fill(tri, "cream", light=2, shadow=3)
    # nori wrap at bottom centre
    nori = poly([(9, 28), (22, 28), (23, 19), (8, 19)]) & tri
    c.fill(nori, "gray1")
    c.fill(rect(9, 19, 22, 20), "gray2")
    c.fill({(10, 19), (11, 19), (12, 19), (10, 20)}, "gray3")
    c.fill({(9, 24), (10, 24), (9, 25)}, "gray2")
    # rice grains
    for x, y in [(14, 9), (13, 14), (18, 13), (9, 15), (21, 17), (16, 17)]:
        c.fill({(x, y), (x + 1, y)}, "cream4")
