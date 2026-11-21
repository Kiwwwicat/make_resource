from pixelkit import ellipse, rect


def draw(c):
    stem = ellipse(15.5, 22, 6.5, 6.5) | rect(10, 16, 21, 24)
    stem -= rect(0, 0, 31, 15)
    c.fill(stem, "cream")
    cap = ellipse(15.5, 15, 13.5, 11.5)
    cap -= rect(0, 16, 31, 31)
    c.fill(cap, "red")
    c.fill(rect(0, 15, 31, 15) & ellipse(15.5, 15, 13.5, 11.5), "red1")
    c.fill(rect(10, 16, 21, 17) & stem, "cream1")
    for (cx, cy, r) in [(10, 11, 2.2), (19, 8, 2.2), (22, 13, 1.7), (14, 14, 1.3)]:
        c.fill(ellipse(cx, cy, r, r), "cream3")
    c.fill({(7, 12), (8, 10), (9, 9)}, "red4")
