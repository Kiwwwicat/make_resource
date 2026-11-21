from pixelkit import ellipse, line


def draw(c):
    c.fill(line(16, 3, 17, 8, 2), "brown2")
    c.grid(18, 3, [
        ".aabb..",
        "aabbbb.",
        "abbbbcc",
        ".bbbccc",
        "..bcc..",
    ], {"a": "green3", "b": "green2", "c": "green1"})
    for (cx, cy) in [(9, 12), (16, 11), (23, 12), (12.5, 18), (19.5, 18), (16, 24)]:
        c.fill(ellipse(cx, cy, 4, 4), "purple")
        c.px(int(cx) - 1, int(cy) - 2, "purple4")
