import sys, ezdxf, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy, LineweightPolicy
def render(fn, layout_name, out, dpi=150, mono=True):
    doc = ezdxf.readfile(fn)
    lay = doc.layouts.get(layout_name)
    fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4)); ax = fig.add_axes([0, 0, 1, 1])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK if mono else ColorPolicy.COLOR,
                        lineweight_policy=LineweightPolicy.ABSOLUTE, lineweight_scaling=1.0)
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(lay, finalize=True)
    ax.set_xlim(0, 420); ax.set_ylim(0, 297); ax.set_aspect('equal'); ax.axis('off')
    fig.savefig(out, dpi=dpi); plt.close(fig)
if __name__ == '__main__':
    render(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 150, (sys.argv[5] != 'color') if len(sys.argv) > 5 else True)
