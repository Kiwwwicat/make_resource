from pixelkit import ellipse, poly, rect, rotate


def draw(c):
    R = lambda m: rotate({(x - 3, y) for (x, y) in m}, -45)
    # 똑바로(머리 왼쪽, 꼬리 오른쪽) 만든 뒤 마지막에 돌린다
    body = ellipse(12.5, 16, 10.5, 4.6) | poly([(20, 13), (27, 15), (27, 17), (20, 19)])
    tail = poly([(25, 15), (30, 10), (28, 16), (30, 22), (25, 17)])
    dorsal = poly([(12, 12), (15, 9), (18, 12)])
    c.fill(R(tail), "orange2")
    c.fill(R(dorsal), "orange1")
    bodyR = R(body)
    c.fill(bodyR, "orange", light=2, shadow=2)
    # 밝은 배 (아래쪽)
    belly = {(x, y) for (x, y) in body if y >= 18 and x < 22}
    c.recolor(R(belly), "tan3")
    # 꼬리 가운데 홈 쪽 어두운 선
    c.recolor(R({(26, 16), (27, 16), (28, 16)}), "orange1")
    # 석쇠 자국 3줄
    for x in (9, 13, 17):
        c.recolor(R(rect(x, 10, x, 22) & body), "brown1")
    # 아가미 선
    c.recolor(R({(6, 14), (6, 15), (6, 16), (6, 17), (6, 18)}), "orange1")
    # 눈
    c.fill(R({(4, 15), (5, 15), (4, 16), (5, 16)}), "cream4")
    c.recolor(R({(4, 16)}), "gray0")
    # 하이라이트
    c.recolor(R({(10, 13), (11, 13), (12, 13), (7, 14)}), "orange4")
