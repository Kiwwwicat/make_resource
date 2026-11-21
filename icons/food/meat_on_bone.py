from pixelkit import ellipse, line


def draw(c):
    # 뼈: 대각선으로 양쪽이 튀어나옴 (뒤에 먼저)
    shaft = line(6, 24, 24, 6, 3)
    knobs = ellipse(4.5, 24.5, 2.5, 2.5) | ellipse(7.5, 27.5, 2.2, 2.2) | ellipse(26.5, 4.5, 2.5, 2.5) | ellipse(23.5, 3.5, 2.2, 2.2)
    bone = shaft | knobs
    c.fill(bone, "cream3")
    c.fill({(x, y) for (x, y) in bone if (x + 1, y + 1) not in bone or (x + 1, y) not in bone and (x, y + 1) not in bone}, "cream2")
    c.fill({(4, 23), (3, 24), (4, 24), (25, 3), (26, 3), (25, 4)}, "cream4")
    # 고기 덩어리
    meat = ellipse(15.5, 15.5, 9.5, 8) | ellipse(13.5, 17, 8.5, 8.5)
    c.fill(meat, "brown", light=2, shadow=3)
    # 구운 윤기 / 그릴 자국
    c.fill({(9, 12), (10, 11), (11, 10), (12, 9), (9, 13), (10, 13), (11, 12)}, "orange2")
    c.fill({(10, 12), (11, 11), (12, 10)}, "orange4")
    c.fill(line(13, 20, 18, 15) | line(16, 22, 21, 17), "brown1")
    # 뼈가 고기에서 나오는 자리 그림자
    c.fill({(21, 8), (22, 8), (21, 9)}, "cream1")
