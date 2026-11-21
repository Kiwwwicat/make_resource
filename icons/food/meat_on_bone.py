from pixelkit import blob, rect, rotate, line


def draw(c):
    # 뼈: 똑바로 세워 만든 뒤 45도 돌린다 (양 끝 마디가 크게 튀어나옴)
    shaft = rect(14, 4, 17, 27)
    top = blob([(13.5, 6), (12.5, 3), (14.5, 1), (16, 2.5), (17.5, 1), (19.5, 3), (18.5, 6)])
    bot = blob([(13.5, 25), (12.5, 28), (14.5, 30), (16, 28.5), (17.5, 30), (19.5, 28), (18.5, 25)])
    bone = rotate(shaft | top | bot, 45)
    c.fill(bone, "cream", round=2)
    # 고기: 로스트 덩어리, 아래로 처지고 왼쪽 위가 살짝 솟음
    meat = blob([
        (9, 11), (14, 7.5), (19.5, 8.5), (23.5, 12.5), (23.5, 18.5), (20, 23), (14, 24), (8.5, 21.5), (6.5, 16),
    ])
    c.cast(meat)
    c.fill(meat, "orange", round=None)
    # 구운 겉면: 아래쪽 가장자리는 진한 갈색, 그릴 자국
    c.recolor({(x, y) for (x, y) in meat if (x + 3, y + 3) not in meat}, "brown2")
    c.recolor({(x, y) for (x, y) in meat if (x + 2, y + 2) not in meat}, "brown1")
    c.recolor(line(9, 17, 13, 21) | line(12, 14, 18, 20) | line(16, 12, 21, 17), "brown2")
    # 작은 윤기
    c.fill({(10, 11), (11, 10), (10, 12)}, "yellow3")
    c.fill({(11, 11)}, "yellow4")
