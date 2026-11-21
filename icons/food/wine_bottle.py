import math


def draw(c):
    ang = math.radians(40)          # neck points to upper right
    ca, sa = math.cos(ang), math.sin(ang)

    def shape(test):
        out = set()
        for y in range(32):
            for x in range(32):
                dx, dy = x - 15.5, y - 15.5
                lx = dx * ca + dy * sa      # local: +y points down the bottle
                ly = -dx * sa + dy * ca
                if test(lx, ly):
                    out.add((x, y))
        return out

    # simpler explicit profile
    def width(ly):
        if ly > 13.5 or ly < -13.5:
            return -1
        if ly >= 2:
            return 5.3 if ly < 12.5 else 4.3
        if ly >= -4:
            return 2.4 + (ly + 4) / 6 * 2.9      # shoulder
        return 2.4
    glass = shape(lambda x, y: abs(x) <= width(y))
    c.fill(glass, "green1")
    c.fill({(x, y) for (x, y) in glass if (x + 1, y + 1) not in glass}, "green0")
    c.fill({(x, y) for (x, y) in glass if (x - 1, y - 1) not in glass}, "green2")
    # foil cap on neck tip
    foil = shape(lambda x, y: -13.5 <= y < -9 and abs(x) <= 2.4)
    c.fill(foil, "red2")
    c.fill({(x, y) for (x, y) in foil if (x - 1, y - 1) not in foil}, "red3")
    c.fill({(x, y) for (x, y) in foil if (x + 1, y + 1) not in foil}, "red1")
    # label
    label = shape(lambda x, y: 5 <= y <= 11.5 and abs(x) <= 5.3)
    c.fill(label, "cream2")
    c.fill({(x, y) for (x, y) in label if (x + 1, y + 1) not in label}, "cream1")
    c.fill({(x, y) for (x, y) in label if (x - 1, y - 1) not in label}, "cream3")
    # label crest
    c.recolor(shape(lambda x, y: 7.3 <= y <= 9.3 and abs(x) <= 1.8), "red2")
    # glass highlight along left side of body
    c.fill(shape(lambda x, y: -3 <= y <= 3.5 and -4.3 <= x <= -3.3), "green2")
    c.fill(shape(lambda x, y: -0.5 <= y <= 2 and -4.3 <= x <= -3.3), "green3")
