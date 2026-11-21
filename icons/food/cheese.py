from pixelkit import ellipse, poly


def draw(c):
    # 쐐기형 치즈. 각진 물체는 '면 단위 고정색'으로 칠한다:
    # 윗면=3(밝음), 정면=2(기본), 바닥 가장자리=1(어두움)
    top = poly([(3, 16), (22, 7), (28, 13)])
    front = poly([(3, 17), (28, 14), (28, 23), (3, 26)])
    c.fill(front, "yellow2")
    c.fill(top, "yellow3")
    c.line(4, 16, 21, 8, "yellow4")       # 윗면 좌측 모서리 하이라이트
    c.line(3, 17, 28, 14, "yellow4")      # 윗면/정면 경계
    c.line(3, 26, 28, 23, "yellow1")      # 바닥 그림자
    c.line(4, 25, 28, 22, "yellow1")
    # 구멍: 안쪽은 어둡게(1), 좌상단 안쪽 가장자리는 더 어둡게(0) -> 파인 느낌
    for (cx, cy, r) in [(9.5, 20.5, 2.1), (18.5, 19.5, 1.6), (24.5, 18.5, 1.1)]:
        hole = ellipse(cx, cy, r, r)
        c.fill(hole, "yellow1")
        c.fill({(x, y) for (x, y) in hole if (x - 1, y - 1) not in hole and (x, y - 1) not in hole}, "yellow0")
    c.fill(ellipse(17.5, 12, 2.6, 1.1), "yellow2")   # 윗면 구멍
