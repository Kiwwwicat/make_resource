from pixelkit import blob, line


def draw(c):
    # 파이 틀의 옆면: 윗면보다 아래로 내려온 두께
    side = blob([
        (3, 15), (7, 8.5), (15, 6.5), (24, 8), (28.5, 14), (27, 22),
        (21, 26.5), (13, 27), (6, 23.5),
    ])
    c.fill(side, "tan1")
    c.fill({(x, y) for (x, y) in side if x < 12}, "tan2")
    # 윗면 크러스트 테두리 (살짝 비대칭)
    top = blob([
        (3, 13.5), (7, 7), (15, 4.5), (24, 6), (28.5, 12), (27, 18),
        (21, 21.5), (13, 22), (6, 19),
    ])
    c.cast(top)
    c.fill(top, "tan", round=3)
    # 속 (빨간 필링)
    filling = blob([
        (6.5, 13.5), (9.5, 8.8), (15.5, 7.4), (22.5, 8.6), (25.5, 13), (24, 17.4),
        (19.5, 19.4), (13, 19.5), (8, 17.5),
    ])
    c.fill(filling, "red", round=3)
    # 크림프(주름) 테두리: 바깥 가장자리 안쪽 1px 줄에 2px 간격의 홈, 안쪽 턱에 밝은/어두운 선
    ring = top - filling
    edge = {(x, y) for (x, y) in ring
            if any(q not in top for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))}
    inner = ring - edge
    pits = {(x, y) for (x, y) in inner
            if any(q in edge for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
            and ((x + y) // 2) % 2 == 0}
    c.fill(pits, "tan3")
    groove = {(x, y) for (x, y) in ring
              if any(q in filling for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))}
    c.fill(groove, "tan2")
    c.fill({(x, y) for (x, y) in groove if (x + 1, y + 1) in filling or (x, y + 1) in filling}, "tan1")
    # 넓은 반죽 띠 3줄 (비스듬, 3px 폭)
    for ox in (-4, 3, 10):
        strip = line(ox + 4, 21, ox + 14, 7, 3) & filling
        c.cast(strip)
        c.fill(strip, "tan3")
        c.fill({(x, y) for (x, y) in strip if (x + 1, y) not in strip or (x, y + 1) not in strip}, "tan2")
        c.fill({(x, y) for (x, y) in strip if (x - 1, y) not in strip and (x, y - 1) not in strip}, "tan4")
