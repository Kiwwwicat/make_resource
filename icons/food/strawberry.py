from pixelkit import ellipse, poly


def draw(c):
    body = ellipse(15.5, 14.5, 11.5, 8.5) | poly([(5, 17), (26, 17), (16, 28)])
    c.fill(body, "red")
    c.fill({(9, 12), (9, 11), (10, 10), (11, 10)}, "red4")
    # 씨
    for (x, y) in [(10, 16), (15, 14), (20, 15), (13, 20), (18, 20), (23, 12), (16, 24), (11, 13), (21, 19)]:
        c.px(x, y, "yellow3")
    # 꼭지 잎
    c.fill({(x, 7) for x in range(11, 21)} | {(x, 8) for x in range(8, 24)} | {(x, 9) for x in range(9, 23)}
           | {(x, 10) for x in range(11, 20)}, "green2")
    c.fill({(x, 10) for x in range(11, 20)} | {(x, 9) for x in range(18, 22)}, "green1")
    c.fill({(x, 8) for x in range(9, 13)}, "green3")
    c.fill({(15, 5), (15, 6), (16, 5), (16, 6)}, "green1")
    c.fill({(15, 4), (16, 4)}, "green2")
    c.fill({(7, 9), (8, 10), (24, 9), (23, 10), (13, 11), (18, 11), (16, 11)}, "green1")
