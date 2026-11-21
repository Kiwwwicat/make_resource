from pixelkit import blob, rect, rotate


def draw(c):
    # 똑바로(머리 위, 꼬리 아래) 만든 뒤 마지막에 -45도 돌린다. 등은 오른쪽, 배는 왼쪽.
    R = lambda m: rotate(m, -45, 12, 17.5)
    body = blob([(15, 2.5), (19.5, 4), (23, 9), (24, 15), (21.5, 20.5), (18, 24), (14, 24), (10.5, 20.5), (8, 15),
                 (8.5, 9), (11, 4.5)])
    tail = blob([(13.5, 21), (17.5, 21), (23, 28.5), (22.5, 30.5), (16, 27), (9.5, 30.5), (9, 28)])
    dorsal = blob([(20, 9), (24.5, 10), (26, 16), (21, 15.5)])
    c.fill(R(tail), "orange", round=2)
    c.fill(R(dorsal), "orange", round=2)
    bodyR = R(body)
    c.cast(bodyR)
    c.fill(bodyR, "orange")
    # 배: 왼쪽 아래 밝은 살색
    belly = {(x, y) for (x, y) in body if x <= 10.5 and y >= 11}
    c.recolor(R(belly), "tan3")
    # 석쇠 자국: 몸통 안쪽에 짧게 2줄
    for y in (12, 17):
        c.recolor(R({(x, y) for x in range(12, 21)} & body), "orange1")
    # 아가미 선, 눈
    c.recolor(R({(11, 7), (11, 8), (12, 9), (12, 10)}), "orange1")
    c.fill(R({(12, 5), (13, 5), (12, 6), (13, 6)}), "cream4")
    c.recolor(R({(12, 6)}), "gray0")
