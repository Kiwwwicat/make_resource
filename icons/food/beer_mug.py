from pixelkit import ellipse, rect


def draw(c):
    # handle (behind): gray ring on the right
    ring = ellipse(23.5, 18, 5.5, 6.5) - ellipse(23.5, 18, 2.8, 3.8)
    c.fill(ring - rect(0, 0, 21, 31), "gray2")
    c.fill({(x, y) for (x, y) in ring if x > 21 and ((x+1, y+1) not in ring)}, "gray1")
    # glass body
    c.fill(rect(5, 9, 21, 28), "gray3")
    # beer
    beer = rect(6, 9, 20, 25)
    c.fill(beer, "yellow2")
    c.fill(rect(19, 9, 20, 25), "yellow1")
    c.fill(rect(6, 12, 6, 24), "yellow3")
    c.fill(rect(7, 14, 7, 20), "yellow3")
    c.fill({(7, 15), (7, 16)}, "yellow4")
    # thick glass base
    c.fill(rect(5, 26, 21, 28), "gray2")
    c.fill(rect(5, 26, 21, 26), "gray4")
    c.fill(rect(20, 27, 21, 28), "gray1")
    # bubbles
    for p in [(11, 20), (14, 16), (12, 12), (16, 22)]:
        c.px(*p, "yellow3")
    # foam overflowing the rim
    foam = (rect(5, 8, 21, 11) | ellipse(8, 7, 3.6, 3.2) | ellipse(13, 5.5, 4, 3.6)
            | ellipse(18, 7, 3.6, 3.2) | ellipse(21.5, 11.5, 2, 2.6) | ellipse(5.5, 11.5, 1.8, 2.4))
    c.fill(foam, "cream3")
    c.fill({(x, y) for (x, y) in foam if (x + 1, y + 1) not in foam or (x, y + 1) not in foam}, "cream2")
    c.fill({(9, 6), (10, 5), (11, 4), (7, 7)}, "cream4")
