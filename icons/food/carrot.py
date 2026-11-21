from pixelkit import line


def draw(c):
    # 잎 (뒤)
    c.fill(line(23, 9, 25, 3, 2) | line(23, 9, 20, 4, 2) | line(24, 10, 28, 6, 2), "green")
    c.fill({(25, 4), (24, 5), (21, 5)}, "green3")
    body = set()
    ax, ay = 3.5, 27.5
    bx, by = 24.0, 8.5
    L = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
    dx, dy = (bx - ax) / L, (by - ay) / L
    for y in range(32):
        for x in range(32):
            t = ((x - ax) * dx + (y - ay) * dy) / L
            d = abs(-(x - ax) * dy + (y - ay) * dx)
            if 0 <= t <= 1 and d <= 1.3 + 4.4 * t ** 0.8:
                body.add((x, y))
    c.fill(body, "orange", light=2, shadow=2)
    for (x, y) in [(16, 18), (19, 14), (12, 22), (9, 25)]:
        c.fill({(x, y), (x + 1, y - 1)}, "orange1")
    c.fill({(16, 13), (17, 12), (18, 11), (19, 10)}, "orange4")
