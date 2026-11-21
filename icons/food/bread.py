from pixelkit import ellipse, line


def draw(c):
    # 둥근 시골빵: 위쪽이 부푼 돔 + 아래 약간 넓은 밑단
    body = ellipse(15.5, 17, 13, 10.8) | ellipse(15.5, 21, 11.5, 7.5)
    c.fill(body, "tan")
    # 바닥 쪽 진한 구움색
    c.recolor({(x, y) for x in range(32) for y in range(25, 30)}, "tan1")
    # 칼집 3개: 속살(밝음) + 아래쪽 어두운 가장자리
    for (x0, y0, x1, y1) in [(8, 17, 12, 11), (13, 18, 17, 12), (18, 19, 22, 13)]:
        c.fill(line(x0, y0 + 1, x1, y1 + 1), "tan1")
        c.fill(line(x0, y0, x1, y1), "cream3")
    # 하이라이트
    c.fill({(7, 14), (8, 12), (9, 11), (10, 10), (7, 13)}, "tan4")
    c.fill({(12, 8), (13, 7), (14, 7)}, "tan4")
