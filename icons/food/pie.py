from pixelkit import ellipse, poly, line, rect


def draw(c):
    # tin/rim side then lid
    side = ellipse(15.5, 19, 13, 8) | ellipse(15.5, 15.5, 13, 8)
    c.fill(side & rect(0, 17, 31, 30), "tan1")
    c.fill(ellipse(15.5, 17, 13.5, 8.5) - rect(0, 0, 31, 17) , "tan2")
    top = ellipse(15.5, 15, 13.5, 9)
    c.fill(top, "tan")
    c.fill(ellipse(15.5, 15, 10, 6.5), "tan2")
    # lattice strips
    for k in range(-2, 4):
        x = 9 + k * 4
        c.fill(line(x, 20, x + 8, 10), "tan3")
    for k in range(-2, 4):
        x = 7 + k * 4
        c.fill(line(x + 10, 20, x + 2, 10), "tan3")
    c.fill(ellipse(15.5, 15, 10, 6.5) ^ ellipse(15.5, 15, 10, 6.5), "tan3")
