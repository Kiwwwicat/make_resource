from pixelkit import blob, rect, rotate


def draw(c):
    # 뼈 손잡이: 똑바로(위가 살코기 쪽) 만든 뒤 -45도... 아래쪽이 왼쪽 아래로 가도록 돌린다
    shaft = rect(14, 12, 17, 27)
    knob = blob([(13.5, 26), (12.5, 28.5), (14.5, 30), (16, 28.5), (17.5, 30), (19.5, 28.5), (18.5, 26)])
    bone = rotate(shaft | knob, 45)
    c.fill(bone, "cream", round=2)
    # 살코기: 위쪽(오른쪽 위)이 통통하고 뼈 쪽으로 좁아지는 물방울형
    meat = blob([
        (12, 16), (12.5, 9), (17.5, 4.5), (24, 5.5), (27.5, 10.5), (26.5, 16.5), (21.5, 20), (16.5, 22), (13, 21),
    ])
    c.cast(meat)
    c.fill(meat, "orange", round=None)
    # 노릇한 껍질 그늘 (우하단), 윗면에 밝은 노란 윤기
    c.recolor({(x, y) for (x, y) in meat if (x + 2, y + 2) not in meat}, "orange1")
    c.recolor({(23, 11), (24, 11), (24, 12), (20, 17), (21, 17)}, "brown1")
    c.fill({(16, 8), (17, 7), (16, 9)}, "yellow3")
    c.fill({(17, 8)}, "yellow4")
