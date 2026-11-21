from pixelkit import blob, poly, line


def draw(c):
    # whole fish, side view, head at left
    tail = poly([(21, 14), (28, 8), (25, 16), (28, 24), (21, 18)])
    dorsal = poly([(10, 12), (13, 7), (18, 12)])
    body = blob([(3, 16), (6, 13), (10, 11), (15, 11), (19.5, 13.5), (22, 15), (22, 17.5),
                 (19.5, 18.5), (15, 21), (10, 21.5), (6, 19.5)])
    c.fill(tail, "orange2")
    c.fill({p for p in tail if p[1] >= 17}, "orange1")
    c.fill(dorsal, "orange2")
    c.recolor({p for p in dorsal if p[0] >= 15}, "orange1")
    c.cast(body)
    c.fill(body, "orange")
    # belly
    belly = {p for p in body if p[1] >= 18}
    c.recolor(belly, "tan3")
    c.recolor({p for p in belly if p[1] >= 20}, "tan2")
    # pectoral fin
    c.fill(poly([(12, 17), (14, 17), (11, 19)]), "orange1")
    # grill marks
    for x in (11, 15, 19):
        c.recolor(line(x, 12, x + 2, 16) & body, "brown1")
    # gill, eye
    c.recolor({(8, 14), (9, 15), (9, 16)}, "orange1")
    c.px(6, 15, "brown0")
    c.px(7, 15, "cream4")
