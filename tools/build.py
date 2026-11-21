#!/usr/bin/env python3
"""아이콘 빌드/검사 CLI.

  python tools/build.py food/apple      아이콘 1개: 검사 + 미리보기(build/preview/food/apple.png)
  python tools/build.py food            카테고리 전체: 검사 + dist/ 납품물 + 대조 시트
  python tools/build.py --all           모든 카테고리

아이콘 소스는 icons/<category>/<id>.py 이며 `def draw(c):` 하나를 정의한다.
카테고리 목록/순서는 catalog/<category>.csv 를 따른다.
"""
import csv
import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import pixelkit as pk  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCALES = (1, 2, 4)  # 32, 64, 128px
BG_DARK, BG_LIGHT = (38, 38, 46, 255), (236, 232, 222, 255)


def render(cat, icon_id):
    """pixels/<cat>/<id>.png (AI 원본을 변환한 확정 픽셀)가 있으면 그것을,
    없으면 icons/<cat>/<id>.py (코드로 그린 아이콘)를 렌더한다."""
    png = ROOT / "pixels" / cat / f"{icon_id}.png"
    if png.exists():
        img = Image.open(png).convert("RGBA")
        back = {pk.rgb(r, s): (r, s) for r in pk.PALETTE for s in range(5)}
        c = pk.Canvas()
        bad = 0
        for y in range(pk.SIZE):
            for x in range(pk.SIZE):
                px = img.getpixel((x, y))
                if px[3] == 0:
                    continue
                if px in back:
                    c.pix[(x, y)] = back[px]
                else:
                    bad += 1
        err, warn = c.lint(lo=1, hi=30, max_ramps=9, max_colors=28)
        warn = [w for w in warn if "고립 픽셀" not in w]
        if bad:
            err.append(f"팔레트 밖 색 또는 반투명 픽셀 {bad}개")
        return img, (err, warn)
    path = ROOT / "icons" / cat / f"{icon_id}.py"
    spec = importlib.util.spec_from_file_location(f"icon_{cat}_{icon_id}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    c = pk.Canvas()
    mod.draw(c)
    img = Image.new("RGBA", (pk.SIZE, pk.SIZE), (0, 0, 0, 0))
    for (x, y), (ramp, shade) in c.finish().items():
        if 0 <= x < pk.SIZE and 0 <= y < pk.SIZE:
            img.putpixel((x, y), pk.rgb(ramp, shade))
    return img, c.lint()


def to_svg(img):
    """32x32 픽셀을 그대로 담은 SVG. viewBox는 0 0 32 32 고정, 같은 색 가로 구간은 사각형 하나로 묶는다.
    확대해도 흐려지지 않도록 crispEdges 지정."""
    w, h = img.size
    rects = []
    for y in range(h):
        x = 0
        while x < w:
            px = img.getpixel((x, y))
            if px[3] == 0:
                x += 1
                continue
            x0 = x
            while x < w and img.getpixel((x, y)) == px:
                x += 1
            rects.append(f'<rect x="{x0}" y="{y}" width="{x - x0}" height="1" fill="#{px[0]:02x}{px[1]:02x}{px[2]:02x}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges">\n' + "\n".join(rects) + "\n</svg>\n")


def up(img, k):
    return img.resize((img.width * k, img.height * k), Image.NEAREST)


def on_bg(img, bg):
    out = Image.new("RGBA", img.size, bg)
    out.alpha_composite(img)
    return out


def checker(size, cell):
    out = Image.new("RGBA", (size, size), (200, 200, 200, 255))
    d = ImageDraw.Draw(out)
    for y in range(0, size, cell):
        for x in range(0, size, cell):
            if (x // cell + y // cell) % 2:
                d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=(160, 160, 160, 255))
    return out


def preview(img, dest):
    """작업용 미리보기: 10배 확대(체커) + 실제 크기 x2 (어두운/밝은 배경)."""
    k = 10
    big = checker(pk.SIZE * k, k)
    big.alpha_composite(up(img, k))
    out = Image.new("RGBA", (pk.SIZE * k + 80, pk.SIZE * k), (90, 90, 100, 255))
    out.paste(big, (0, 0))
    out.paste(on_bg(up(img, 2), BG_DARK), (pk.SIZE * k + 8, 8))
    out.paste(on_bg(up(img, 2), BG_LIGHT), (pk.SIZE * k + 8, 80))
    out.paste(on_bg(img, BG_DARK), (pk.SIZE * k + 8, 152))
    out.paste(on_bg(img, BG_LIGHT), (pk.SIZE * k + 44, 152))
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest)


def report(name, lint):
    err, warn = lint
    for e in err:
        print(f"  ERROR {name}: {e}")
    for w in warn:
        print(f"  warn  {name}: {w}")
    return not err


def catalog(cat):
    with open(ROOT / "catalog" / f"{cat}.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_one(cat, icon_id):
    img, lint = render(cat, icon_id)
    dest = ROOT / "build" / "preview" / cat / f"{icon_id}.png"
    preview(img, dest)
    ok = report(f"{cat}/{icon_id}", lint)
    print(f"{'OK  ' if ok else 'FAIL'} {cat}/{icon_id} -> {dest.relative_to(ROOT)}")
    return ok


def build_category(cat):
    rows = catalog(cat)
    done, missing, failed = [], [], []
    for row in rows:
        iid = row["id"]
        if not (ROOT / "icons" / cat / f"{iid}.py").exists() and not (ROOT / "pixels" / cat / f"{iid}.png").exists():
            missing.append(iid)
            continue
        img, lint = render(cat, iid)
        if not report(f"{cat}/{iid}", lint):
            failed.append(iid)
            continue
        done.append((iid, img))
        for k in SCALES:
            d = ROOT / "dist" / cat / f"{pk.SIZE * k}px"
            d.mkdir(parents=True, exist_ok=True)
            up(img, k).save(d / f"{iid}.png")
        d = ROOT / "dist" / cat / "svg"
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{iid}.svg").write_text(to_svg(img), encoding="utf-8")
    if done:
        cols = 8
        n_rows = (len(done) + cols - 1) // cols
        # 납품용 스프라이트 시트 (투명 배경, 32px 격자)
        sheet = Image.new("RGBA", (cols * pk.SIZE, n_rows * pk.SIZE), (0, 0, 0, 0))
        for i, (_, img) in enumerate(done):
            sheet.paste(img, ((i % cols) * pk.SIZE, (i // cols) * pk.SIZE))
        sheet.save(ROOT / "dist" / cat / f"{cat}_sheet_32px.png")
        # 검수/홍보용 대조 시트 (4배, 어두운+밝은 배경)
        k, pad = 4, 8
        cell = pk.SIZE * k + pad
        w, h = cols * cell + pad, n_rows * cell + pad
        contact = Image.new("RGBA", (w, h * 2), BG_DARK)
        contact.paste(Image.new("RGBA", (w, h), BG_LIGHT), (0, h))
        for i, (_, img) in enumerate(done):
            x, y = pad + (i % cols) * cell, pad + (i // cols) * cell
            contact.alpha_composite(up(img, k), (x, y))
            contact.alpha_composite(up(img, k), (x, y + h))
        contact.save(ROOT / "dist" / cat / f"{cat}_preview.png")
    print(f"[{cat}] 완료 {len(done)} / 실패 {len(failed)} {failed or ''} / 미작성 {len(missing)} {missing or ''}")
    return not failed


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "--all":
        targets = sorted(p.stem for p in (ROOT / "catalog").glob("*.csv"))
    else:
        targets = argv
    ok = True
    for t in targets:
        if "/" in t:
            ok &= build_one(*t.split("/", 1))
        else:
            ok &= build_category(t)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
