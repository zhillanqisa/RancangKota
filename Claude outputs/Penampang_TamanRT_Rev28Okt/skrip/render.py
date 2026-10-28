import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Circle
from penampang import ROADS, ops_for, dim_ops, COL

plt.rcParams['font.family'] = 'Inter'

def draw_ops(ax, ops, scale_txt=1.0, pt_per_m=None):
    for o in ops:
        if o['k'] == 'poly':
            ax.add_patch(MPoly(o['pts'], closed=True, fc=o['fill'], ec=o['ec'], lw=o['lw'], zorder=o['z']))
        elif o['k'] == 'line':
            xs, ys = zip(*o['pts']); ax.plot(xs, ys, color=o['color'], lw=o['lw'], ls=o['ls'], zorder=o['z'], solid_capstyle='butt')
        elif o['k'] == 'circle':
            fc = o['fill'] if o['fill'] != 'none' else 'none'
            ax.add_patch(Circle(o['c'], o['r'], fc=fc, ec=o['ec'], lw=1.0 if fc == 'none' else 0.3, zorder=o['z']))
        elif o['k'] == 'text':
            ax.text(*o['xy'], o['s'], fontsize=o['size'] * (0.17 * pt_per_m if pt_per_m else 4.6) * scale_txt, ha=o['ha'], va=o['va'], color=o['color'],
                    fontweight=o['weight'], rotation=o['rot'], zorder=6, linespacing=1.05)

def section_figure(key, which, out, title=None, width_in=9.0, scale_txt=1.0, sides=True, bg='none'):
    r = ROADS[key]
    els = r[which]
    ops, dims, total = ops_for(els)
    ops += dim_ops(dims, total_label='Ruang milik jalan' if which == 'ren' else 'Ruang milik jalan eksisting')
    h_m = 15.0
    fig = plt.figure(figsize=(width_in, width_in * h_m / (total + 1.0)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(-0.5, total + 0.5); ax.set_ylim(-5.4, h_m - 5.4)
    ax.set_aspect('equal'); ax.axis('off')
    draw_ops(ax, ops, scale_txt, pt_per_m=width_in * 72 / (total + 1.0))
    t = title or ('%s - %s' % (r['nama'], 'Eksisting' if which == 'eks' else 'Rencana'))
    fs = 13 * width_in / 9.0 * scale_txt
    ax.text(total / 2, h_m - 5.6, t, ha='center', va='top', fontsize=fs, fontweight='bold', color=COL['garis'])
    ax.text(total / 2, h_m - 5.6 - 0.95, '(%s)' % r['ket'], ha='center', va='top', fontsize=fs * 0.6, color='#5b5e44')
    if sides:
        ax.text(-0.3, h_m - 5.6 - 0.2, r['kiri'], ha='left', va='top', fontsize=fs * 0.55, color='#5b5e44', style='italic')
        ax.text(total + 0.3, h_m - 5.6 - 0.2, r['kanan'], ha='right', va='top', fontsize=fs * 0.55, color='#5b5e44', style='italic')
    fig.savefig(out, dpi=220, transparent=(bg == 'none'), facecolor=bg if bg != 'none' else None)
    plt.close(fig)

if __name__ == '__main__':
    import os; os.makedirs('../out/penampang', exist_ok=True)
    for k in ROADS:
        for w in ('eks', 'ren'):
            section_figure(k, w, f'../out/penampang/{k}_{w}.png', width_in=7.0)
            print('ok', k, w)
