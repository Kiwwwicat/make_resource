from pixelkit import ellipse, line, poly


def draw(c):
    # 뼈 손잡이 (왼쪽 아래)
    shaft = line(8, 22, 15, 15, 3)
    knobs = ellipse(5.5, 24.5, 2.5, 2.5) | ellipse(8.5, 27.5, 2.3, 2.3)
    bone = shaft | knobs
    c.fill(bone, "cream3")
    c.fill({(x, y) for (x, y) in bone if (x + 1, y + 1) not in bone or ((x + 1, y) not in bone and (x, y + 1) not in bone)}, "cream2")
    c.fill({(4, 23), (5, 22), (7, 26)}, "cream4")
    # 살코기: 오른쪽 위가 통통하고 아래로 좁아진다
    meat = ellipse(19.5, 11.5, 8.5, 8) | poly([(11, 13), (16, 20), (22, 17), (14, 7)]) | ellipse(15, 15, 5.5, 5.5)
    c.fill(meat, "orange", light=2, shadow=4)
    # 노릇한 껍질 얼룩
    c.fill({(22, 13), (23, 13), (23, 14), (24, 14), (22, 17), (21, 18)}, "brown1")
    c.fill({(18, 16), (19, 16), (19, 17), (13, 19)}, "brown1")
    c.fill({(15, 8), (16, 7), (17, 7), (14, 9), (15, 9)}, "yellow3")
    c.fill({(16, 8), (15, 8)}, "yellow4")
    c.fill({(20, 9), (21, 9), (21, 10)}, "orange1")
