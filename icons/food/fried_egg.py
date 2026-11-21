from pixelkit import ellipse


def draw(c):
    # 흰자: 여러 타원을 겹쳐 불규칙한 번진 모양
    white = (ellipse(12, 13, 8.5, 7.5) | ellipse(20, 15, 8, 8) | ellipse(15, 21, 9, 6.5)
             | ellipse(8, 20, 5, 4.5) | ellipse(23, 9, 4.5, 4))
    c.fill(white, "cream", light=2, shadow=2)
    c.recolor({p for p, v in c.pix.items() if v == ("cream", 2)}, "cream3")
    # 노른자
    c.fill(ellipse(14.5, 15, 5, 5), "yellow", light=1, shadow=2)
    # 노른자 하이라이트
    c.fill({(12, 12), (13, 11), (12, 13)}, "yellow4")
    # 흰자 하이라이트
    c.fill({(6, 14), (6, 15), (7, 12), (8, 10), (9, 9)}, "cream4")
