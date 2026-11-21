from pixelkit import blob


def draw(c):
    # 둥근 삼각형 밥 덩어리: 꼭대기는 좁고 둥글고, 아래가 넓게 처짐. 살짝 비대칭.
    rice = blob([
        (14.5, 4.5), (18, 6), (22, 13), (26.5, 21), (26, 26),
        (21, 28), (11, 28.2), (5.5, 26.5), (4.5, 21.5), (9, 13), (12, 6.5),
    ])
    c.fill(rice, "cream", round=8)
    # 김 띠: 아래 가운데를 감싸는 띠
    nori = blob([(10.5, 22.5), (15, 22), (20, 22.5), (20.5, 28), (15, 28.5), (10, 28)])
    c.cast(nori)
    nori &= rice
    c.fill(nori, "gray1")
    c.fill({(x, y) for (x, y) in nori if (x, y - 1) not in nori or (x - 1, y) not in nori}, "gray2")
    c.fill({(x, y) for (x, y) in nori if (x + 1, y) not in nori or (x, y + 1) not in nori}, "gray0")
    # 밥알 무늬 (2px, 3~4개만)
    for x, y in [(14, 11), (18, 16), (10, 18), (22, 22)]:
        c.fill({(x, y), (x + 1, y)}, "cream2")
