import sys
sys.path.insert(0, '..')
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None
from geo import px
import taman as T

im = Image.open('../img/r24full.png').convert('RGBA')

def crop(e0, n1, e1, n0, s=2):
    x0, y0 = px(e0, n1); x1, y1 = px(e1, n0)
    c = im.crop((int(x0), int(y0), int(x1), int(y1)))
    c = c.resize((c.size[0] * s, c.size[1] * s))
    def P(E, N):
        X, Y = px(E, N); return ((X - int(x0)) * s, (Y - int(y0)) * s)
    return c, P

def draw(c, P, geoms):
    ov = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for g, fill, out in geoms:
        for p in getattr(g, 'geoms', [g]):
            if p.is_empty: continue
            d.polygon([P(*xy) for xy in p.exterior.coords], fill=fill, outline=out)
            for h in p.interiors:
                d.polygon([P(*xy) for xy in h.coords], fill=(0, 0, 0, 0))
    return Image.alpha_composite(c, ov)

for name, (bb, gs) in {
    'A': ((306030, 9156530, 306125, 9156475), [(T.A, (120, 190, 90, 160), (30, 90, 30, 255)), (T.A_jalur, (220, 200, 160, 200), None),
                                              (T.A_main, (240, 170, 60, 220), None), (T.A_lap, (150, 210, 110, 220), None),
                                              (T.A_gazebo, (150, 90, 40, 255), None), (T.A_pagar, (40, 110, 40, 200), None)]),
    'B': ((306310, 9156505, 306395, 9156455), [(T.B, (120, 190, 90, 160), (30, 90, 30, 255)), (T.B_plaza, (220, 200, 160, 220), None),
                                              (T.B_main, (240, 170, 60, 220), None), (T.B_gazebo, (150, 90, 40, 255), None),
                                              (T.B_zebra, (255, 255, 255, 230), (0, 0, 0, 255))]),
}.items():
    c, P = crop(*bb)
    out = draw(c, P, gs)
    d = ImageDraw.Draw(out)
    for pts in (T.A_pohon if name == 'A' else T.B_pohon):
        x, y = P(pts.x, pts.y); d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=(0, 90, 0, 255), width=3)
    out.convert('RGB').save(f'../img/prev_taman_{name}.png'); print(name, out.size)
