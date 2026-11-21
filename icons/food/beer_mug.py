from pixelkit import blob, rect


def draw(c):
    # handle (behind): chunky loop on the right
    outer = blob([(20, 11), (25, 10.5), (28.5, 14), (28.5, 20), (25.5, 24.5), (20, 24)])
    inner = blob([(20, 14), (23.5, 14), (25.5, 16.5), (25, 20), (23, 21.5), (20, 21)])
    handle = outer - inner - rect(0, 0, 20, 31)
    c.fill(handle, "gray", round=2)
    # glass body: slightly wider at the top, thick base
    glass = blob([(4.5, 9), (21.5, 9), (21, 18), (21.5, 27.5), (19.5, 29), (6.5, 29), (4.5, 27.5), (5, 18)])
    c.fill(glass, "gray", round=2)
    # beer inside the glass
    beer = blob([(6.5, 9), (19.5, 9), (19.2, 18), (19.5, 25), (18, 26.2), (8, 26.2), (6.5, 25), (6.8, 18)])
    c.fill(beer, "yellow", round=3)
    # glass highlight streak (left) and bubbles
    c.fill({(5, y) for y in range(13, 24)}, "gray3")
    c.fill({(5, y) for y in range(15, 19)}, "gray4")
    c.fill({(7, y) for y in range(15, 23)}, "yellow3")
    for p in [(11, 21), (14, 16), (12, 13), (16, 22)]:
        c.px(*p, "yellow3")
    c.fill({(x, 28) for x in range(8, 19)}, "gray1")
    # foam: lumpy cloud over the rim with one drip running down the front
    foam = blob([
        (4, 11), (3.5, 7.5), (6.5, 5.5), (8.5, 3.2), (12, 4.2), (14.5, 2.5), (18, 4), (20, 5.2), (23, 7), (22.5, 11),
        (19.5, 12.5), (15, 11.5), (10, 12.5), (6, 12.5),
    ])
    drip = blob([(7, 11), (10, 11), (10.5, 15), (9.5, 18.5), (7.5, 18.5), (6.5, 15)])
    foam = foam | drip
    c.cast(foam)
    c.fill(foam, "cream", round=3)
    c.fill({(8, 6), (9, 5), (10, 4)}, "cream4")
