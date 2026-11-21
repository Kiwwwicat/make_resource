from pixelkit import ellipse, line


def draw(c):
    c.fill(line(9, 19, 16, 5), "brown2")
    c.fill(line(22, 20, 17, 5), "brown2")
    c.fill(line(16, 4, 17, 5, 2), "brown1")
    c.grid(18, 3, [
        ".aab.",
        "aabbb",
        ".bbcc",
        "..cc.",
    ], {"a": "green3", "b": "green2", "c": "green1"})
    c.fill(ellipse(9, 22.5, 6.5, 6.5), "red")
    c.fill(ellipse(22, 23, 6.5, 6.5), "red")
    c.fill({(6, 21), (6, 20), (7, 19), (8, 19)}, "red4")
    c.fill({(19, 21), (19, 20), (20, 19), (21, 19)}, "red4")
