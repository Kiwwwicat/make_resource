from pixelkit import blob


def draw(c):
    # 흰자: 번져 나간 불규칙한 형태, 아래쪽으로 처지고 오른쪽 위가 살짝 튀어나옴
    white = blob([
        (9, 6), (15, 3.5), (21, 5), (26, 9), (27.5, 15), (25, 21), (26.5, 25), (20, 28), (13, 27.5),
        (7, 25), (3.5, 19.5), (4.5, 12),
    ])
    c.fill(white, "cream", round=3)
    # 노른자: 흰자 위에 살짝 솟은 구
    yolk = blob([(11, 10), (16, 8.5), (20.5, 11.5), (21, 16.5), (17, 20), (12, 19.5), (9.5, 15)])
    c.cast(yolk)
    c.fill(yolk, "yellow")
    # 흰자 가장자리 그늘 (바닥 쪽)
    c.recolor({(x, y) for (x, y) in white if (x + 2, y + 2) not in white} - yolk, "cream1")
