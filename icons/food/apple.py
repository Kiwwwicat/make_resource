from pixelkit import ellipse, rect


def draw(c):
    # 몸통: 두 개의 타원을 합쳐 한 덩어리로 자동 명암을 준다
    body = ellipse(12, 18.5, 7.5, 9.5) | ellipse(19, 18.5, 7.5, 9.5)
    body -= rect(14, 0, 17, 10)           # 위쪽 꼭지 홈
    c.fill(body, "red")
    # 하이라이트 (좌상단) - 자동 명암 위에 수동으로 몇 픽셀만
    c.fill({(8, 14), (8, 13), (9, 12), (10, 12)}, "red4")
    # 꼭지
    c.fill({(15, 11), (15, 10), (15, 9), (16, 8), (16, 7), (17, 6)}, "brown2")
    c.fill({(16, 11), (16, 10), (16, 9)}, "brown1")
    # 잎: 작은 디테일은 grid(문자 그림)로
    c.grid(18, 5, [
        ".abb..",
        "abbbc.",
        ".bbccc",
        "..cc..",
    ], {"a": "green3", "b": "green2", "c": "green1"})
