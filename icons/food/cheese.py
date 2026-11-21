from pixelkit import poly, line, rect


def draw(c):
    # 쐐기형 치즈. 각진 물체는 면 단위 고정색:
    # 윗면=3(가장 밝음), 정면=2(중간), 오른쪽 끝면=1(가장 어두움)
    top = poly([(3, 18), (16, 8), (28, 10), (22, 14)])
    front = poly([(3, 19), (22, 15), (22, 25), (3, 26)])
    end = poly([(23, 15), (28, 11), (28, 21), (23, 25)])
    c.fill(front, "yellow2")
    c.fill(end, "yellow1")
    c.fill(top, "yellow3")
    # 모서리 하이라이트 1px
    c.fill(line(4, 18, 16, 9), "yellow4")
    c.fill(line(4, 19, 22, 15), "yellow4")
    c.fill(line(23, 14, 27, 11), "yellow2")
    # 정면 아랫면 그늘, 끝면 아랫 가장자리
    c.fill(line(3, 26, 22, 25), "yellow1")
    c.fill(line(4, 25, 22, 24), "yellow1")
    # 구멍: 모서리를 깎은 3x3 / 2x2. 안쪽은 어둡게(1), 좌상단 안쪽 가장자리는 0
    def hole(x, y, n):
        w = 4 if n == 3 else n
        m = rect(x, y, x + w - 1, y + n - 1)
        if n == 3:
            m -= {(x, y), (x + 3, y), (x, y + 2), (x + 3, y + 2)}
        c.fill(m, "yellow1")
        c.fill({(px, py) for (px, py) in m if (px, py - 1) not in m}, "yellow0")
        return m
    hole(7, 20, 3)
    hole(15, 19, 2)
    hole(12, 23, 2)
    hole(25, 15, 2)
    c.fill({(18, 11), (19, 11), (20, 11), (19, 12)}, "yellow2")  # 윗면 오목한 곳
    c.fill({(18, 11)}, "yellow1")
