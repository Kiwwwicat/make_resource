from pixelkit import ellipse, line


def draw(c):
    # 둥근 시골빵: 위쪽이 부푼 돔 + 아래 약간 넓은 밑단
    body = ellipse(15.5, 15.5, 13, 9.5) | ellipse(15.5, 19.5, 12, 7.5)
    c.fill(body, "tan")
    # 바닥 쪽 진한 구움색
    c.recolor({(x, y) for x in range(32) for y in range(24, 30)}, "tan1")
    # 칼집 3개: 속살(밝음) + 아래쪽 어두운 가장자리
    for (x0, y0, x1, y1) in [(8, 16, 12, 10), (13, 17, 17, 11), (18, 18, 22, 12)]:
        c.fill(line(x0, y0 + 1, x1, y1 + 1), "tan1")
        c.fill(line(x0, y0, x1, y1), "cream3")
    # 하이라이트
    c.fill({(6, 13), (7, 12), (8, 11), (9, 10), (6, 14)}, "tan4")
    c.fill({(11, 8), (12, 7), (13, 7)}, "tan4")
