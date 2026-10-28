import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle, PathPatch
from matplotlib.path import Path
from geo2 import pt, _M

def rgb(c, a=1.0): return (c[0] / 255, c[1] / 255, c[2] / 255, a)

def poly_path(poly, T):
    verts, codes = [], []
    for ring in [poly.exterior] + list(poly.interiors):
        cs = [T(*xy) for xy in ring.coords]
        verts += cs; codes += [Path.MOVETO] + [Path.LINETO] * (len(cs) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes)

def draw_scene(ax, S, sheet='A0', clip=None, zbase=10):
    s = _M[sheet]['s']                       # pt per meter
    T = lambda x, y: pt(x, y, sheet)
    mm = 72 / 25.4
    arts = []
    for p in sorted(S, key=lambda q: q.get('z', 0)):
        z = zbase + p.get('z', 0) * 0.01
        k = p['k']
        if k == 'poly':
            a = PathPatch(poly_path(p['poly'], T), fc=rgb(p['fill'], p.get('alpha', 1)), ec=rgb(p['edge']) if p.get('edge') else 'none',
                          lw=p.get('lw', 0) * 0.35 * mm * 0.5, zorder=z)
            ax.add_patch(a); arts.append(a)
        elif k in ('lines',):
            for ln in p['lines']:
                xs, ys = zip(*[T(*q) for q in ln]); a, = ax.plot(xs, ys, color=rgb(p['color']), lw=p['lw'] * 0.35 * mm * 0.5, zorder=z, solid_capstyle='butt'); arts.append(a)
        elif k == 'dash':
            xs, ys = zip(*[T(*q) for q in p['line']])
            on, off = p['dash']
            a, = ax.plot(xs, ys, color=rgb(p['color']), lw=p['lw'] * 0.35 * mm * 0.5, zorder=z, dashes=(on * s / (p['lw'] * 0.35 * mm * 0.5), off * s / (p['lw'] * 0.35 * mm * 0.5)))
            arts.append(a)
        elif k == 'thick':
            xs, ys = zip(*[T(*q) for q in p['line']]); a, = ax.plot(xs, ys, color=rgb(p['color']), lw=p['w'] * s, zorder=z, solid_capstyle='butt'); arts.append(a)
        elif k == 'circle':
            a = Circle(T(*p['c']), p['r'] * s, fc=rgb(p['fill']) if p.get('fill') else 'none', ec=rgb(p['edge']) if p.get('edge') else 'none',
                       lw=p.get('lw', 0.3) * mm * 0.35, zorder=z); ax.add_patch(a); arts.append(a)
        elif k == 'dots':
            if p['pts']:
                xs, ys = zip(*[T(*q) for q in p['pts']]); a = ax.scatter(xs, ys, s=(p['r'] * s * 2) ** 2, c=[rgb(p['color'])], lw=0, zorder=z); arts.append(a)
        elif k == 'text':
            x, y = T(*p['xy'])
            a = ax.text(x, y, p['s'], fontsize=p['h'] * s / 0.72, color=rgb(p['color']), rotation=p.get('rot', 0), ha=p.get('ha', 'left'),
                        va=p.get('va', 'baseline'), fontweight='bold' if p.get('bold') else 'normal', family='FreeSans', zorder=z); arts.append(a)
        elif k == 'bike':
            (ax_, ay), (bx, by) = p['a'], p['b']
            dx, dy = bx - ax_, by - ay; L = math.hypot(dx, dy); dx, dy = dx / L, dy / L; nx, ny = -dy, dx
            for off in (-0.35, 0.35):
                c = Circle(T(ax_ + dx * off, ay + dy * off), 0.22 * s, fc='none', ec=rgb(p['color']), lw=0.6, zorder=z); ax.add_patch(c); arts.append(c)
            xs, ys = zip(*[T(ax_ + dx * u + nx * v, ay + dy * u + ny * v) for u, v in ((-0.35, 0), (0, 0.3), (0.35, 0))])
            a, = ax.plot(xs, ys, color=rgb(p['color']), lw=0.6, zorder=z); arts.append(a)
    if clip is not None:
        for a in arts: a.set_clip_path(clip)
    return arts

def draw_kop(ax, K, z=60):
    from matplotlib.patches import Rectangle
    for p in K:
        if p['k'] == 'rect':
            ax.add_patch(Rectangle((p['x0'], p['y0']), p['x1'] - p['x0'], p['y1'] - p['y0'], fc=rgb(p['fill']),
                                   ec=rgb(p['edge']) if p.get('edge') else 'none', lw=p.get('lw', 0), zorder=z))
        elif p['k'] == 'line':
            xs, ys = zip(*p['pts'])
            kw = dict(dashes=p['dash']) if p.get('dash') else {}
            ax.plot(xs, ys, color=rgb(p['color']), lw=p['lw'], zorder=z + 1, **kw)
        elif p['k'] == 'circle':
            ax.add_patch(Circle(p['c'], p['r'], fc=rgb(p['fill']), ec=rgb(p['edge']) if p.get('edge') else 'none', lw=p.get('lw', 0), zorder=z + 2))
        elif p['k'] == 'poly':
            ax.add_patch(MPoly(p['pts'], closed=True, fc=rgb(p['fill']), ec='none', zorder=z + 2))
        elif p['k'] == 'text':
            ax.text(p['xy'][0], p['xy'][1], p['s'], fontsize=p['size'], color=rgb(p['color']), ha=p.get('ha', 'left'), va='baseline',
                    family='Liberation Sans' if False else 'FreeSans', zorder=z + 3)
