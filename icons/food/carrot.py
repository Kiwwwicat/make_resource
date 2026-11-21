from pixelkit import blob, despike, line, rotate

TILT = 45  # 똑바로 세워 만든 뒤 오른쪽으로 45도 눕힌다


def draw(c):
    # 잎 (뒤): 위로 뻗은 세 갈래, 가운데가 가장 길고 좌우가 약간 다르다
    leaves = [
        blob([(14.5, 11), (11, 7.5), (9.5, 3), (13, 4.5), (15.5, 8)]),
        blob([(15, 11), (14.5, 6), (16.5, 1), (18.5, 5.5), (18, 11)]),
        blob([(17.5, 11), (19.5, 7), (23.5, 4), (23.5, 8), (20.5, 11.5)]),
    ]
    foliage = despike(rotate(leaves[0] | leaves[1] | leaves[2], TILT, 12, 14))
    # 당근 몸통: 어깨가 넓고 끝이 가늘게 휘어 내려간다 (아래가 약간 왼쪽으로 쏠림)
    root = blob([
        (15.5, 10.3), (19, 10.8), (20.8, 13.5), (20.2, 18), (18.4, 23), (16.4, 27),
        (14.6, 30), (13.2, 27), (11.8, 22.5), (10.6, 17.5), (10.8, 13), (12.5, 10.8),
    ])
    body = despike(rotate(root, TILT, 12, 14))
    c.fill(foliage, "green")
    c.cast(body)
    c.fill(body, "orange")
    # 가로 주름 (똑바로 그린 뒤 같이 회전)
    ridges = rotate(line(11, 15, 14, 16) | line(17, 18, 20, 17) | line(12, 21, 15, 22)
                    | line(15, 25, 17, 25), TILT, 12, 14)
    c.recolor(ridges & body, "orange1")
