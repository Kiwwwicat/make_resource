from pixelkit import ellipse, poly, rect


def draw(c):
    # saucer
    saucer = ellipse(15.5, 24.5, 13, 2.5)
    c.fill(saucer, "cream3")
    c.fill({(x, y) for (x, y) in saucer if (x, y + 1) not in saucer or (x + 1, y) not in saucer}, "cream2")
    c.fill({(x, y) for (x, y) in saucer if ((x, y - 1) not in saucer and x < 17) or ((x - 1, y) not in saucer and y < 25)}, "cream4")

    # handle (behind cup, right)
    outer = ellipse(25.5, 16, 3.5, 4.5)
    inner = ellipse(26, 16, 1.5, 2.5)
    ring = outer - inner
    c.fill(ring, "cream3")
    c.fill({(x, y) for (x, y) in ring if (x, y + 1) not in ring or (x + 1, y) not in ring}, "cream2")

    # cup silhouette
    body = poly([(8, 11), (23, 11), (22, 15), (20, 19), (18, 21), (13, 21), (11, 19), (9, 15)])
    cup = body | ellipse(15.5, 11, 8, 2.5)
    c.cast(cup)
    c.fill(cup, "cream3")
    rows = {}
    for (x, y) in cup:
        lo, hi = rows.get(y, (99, -99))
        rows[y] = (min(lo, x), max(hi, x))
    c.fill({(x, y) for (x, y) in cup if y >= 12 and x > rows[y][1] - 3}, "cream2")
    c.fill({(x, y) for (x, y) in cup if y == 21}, "cream2")
    c.fill({(rows[y][0] + 2, y) for y in range(13, 20)}, "cream4")
    # blue band
    band = {(x, y) for (x, y) in cup if y == 15}
    c.fill(band, "blue2")
    c.fill({(x, y) for (x, y) in band if x > rows[y][1] - 3}, "blue1")
    # tea opening
    op = ellipse(15.5, 11, 7, 2.5)
    back = {(x, y) for (x, y) in op if (x, y - 1) not in op}
    tea = op - back
    c.fill(tea, "brown2")
    c.fill(back, "cream2")
    c.fill({(x, y) for (x, y) in tea if (x - 1, y) not in tea or (x, y - 1) not in tea} - {(x, y) for (x, y) in tea if x > 12 or y > 11}, "brown3")

    # steam
    for x0 in (11, 19):
        for dx, dy in [(1, 0), (0, 1), (0, 2), (1, 3)]:
            c.px(x0 + dx, 3 + dy, "gray3")
