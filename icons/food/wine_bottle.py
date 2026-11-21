from pixelkit import blob, rect, rotate


def draw(c):
    # Built upright (neck up), then turned 45 degrees so the neck points to the upper right.
    def turn(mask):
        return rotate(mask, 45)

    glass = blob([
        (14, 2.5), (17.5, 2.5), (17.8, 9), (18.2, 12), (20.5, 14.2), (22, 17), (22.2, 22),
        (21.8, 27), (20, 29.2), (15.5, 29.7), (11.5, 29.2), (9.5, 27), (9.2, 22), (9.6, 17),
        (11.5, 14.2), (13.3, 12), (13.4, 9),
    ])
    c.fill(turn(glass), "green", round=3)
    # foil cap over the neck
    foil = turn(rect(14, 2, 17, 6))
    c.cast(foil)
    c.fill(foil, "red", round=2)
    # label: plain cream band with two short lines
    label = turn(rect(9, 21, 22, 27))
    c.cast(label)
    c.fill(label, "cream", round=2)
    c.fill(turn(rect(13, 22, 18, 22)), "brown1")
    c.fill(turn(rect(13, 26, 17, 26)), "brown1")
    # vertical glass highlight streak on the left of the body
    c.fill(turn(rect(11, 15, 11, 20)), "green3")
    c.fill(turn(rect(11, 16, 11, 17)), "green4")
