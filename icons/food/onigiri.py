from pixelkit import ellipse, poly, rect


def draw(c):
    # 둥근 삼각형 밥
    tri = poly([(14, 4), (17, 4), (27, 24), (24, 28), (7, 28), (4, 24)]) | ellipse(15.5, 7.5, 3.5, 3.5)
    tri |= ellipse(7.5, 24, 3.5, 4) | ellipse(24.5, 24, 3.5, 4)
    c.fill(tri, "cream3")
    # 오른쪽 아래 가장자리만 얇게 그림자 (cream2)
    shade = {(x, y) for (x, y) in tri
             if (x + 1, y + 1) not in tri and x + y > 31
             or ((x + 1, y) not in tri and y > 14)
             or ((x, y + 1) not in tri and x > 14)}
    c.fill(shade, "cream2")
    # 왼쪽 위 하이라이트
    c.fill({(13, 7), (14, 7), (12, 8), (11, 10), (10, 12), (9, 14)}, "cream4")
    # 밥알 무늬
    for x, y in [(15, 12), (19, 15), (12, 17), (22, 20), (9, 21), (16, 21)]:
        c.fill({(x, y), (x + 1, y)}, "cream2")
    # 김: 아래 가운데 작은 직사각형 (매우 어두운 색)
    nori = rect(11, 23, 20, 28) & tri
    c.fill(nori, "gray0")
    c.fill(rect(11, 23, 20, 23) & tri, "gray1")
    c.fill({(12, 23), (13, 23), (12, 24)}, "gray2")
