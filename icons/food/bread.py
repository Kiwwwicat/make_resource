from pixelkit import blob, line


def draw(c):
    # 밑단: 진하게 구워진 껍질 (뒤쪽, 먼저)
    base = blob([(5, 21), (9, 20), (23, 20), (27.5, 21.5), (28, 25), (24, 28), (16, 28.5), (8, 28), (4, 25)])
    c.fill(base, "brown", round=3)
    # 돔: 높이가 확실한 둥근 덩어리, 아래가 살짝 넓다
    dome = blob([(15, 5.5), (21, 6.5), (26, 11), (28, 17), (27, 23), (21, 25), (11, 25), (5, 23), (4, 17), (6.5, 11), (10, 7)])
    c.cast(dome)
    c.fill(dome, "tan")
    # 칼집 3개: 돔 윗면을 따라 부채꼴로 휘어진다. 속살 + 아래 그늘
    slashes = [
        [(8, 17), (9, 14), (11, 12)],
        [(13, 18), (14, 15), (16, 11)],
        [(19, 18), (20, 15), (23, 13)],
    ]
    for pts in slashes:
        m = line(*pts[0], *pts[1], width=2) | line(*pts[1], *pts[2], width=2)
        c.recolor({(x + 1, y + 1) for (x, y) in m}, "tan1")
        c.recolor(m, "cream3")
    # 밀가루 흔적 (윗면, 몇 점만)
    c.recolor({(16, 8), (17, 8), (12, 9)}, "cream3")
