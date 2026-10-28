import sys, ezdxf, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, ColorPolicy, LineweightPolicy
fn, out = sys.argv[1], sys.argv[2]
doc = ezdxf.readfile(fn)
cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK, lineweight_policy=LineweightPolicy.ABSOLUTE)
with PdfPages(out) as pdf:
    for name in sys.argv[3:]:
        fig = plt.figure(figsize=(420 / 25.4, 297 / 25.4)); ax = fig.add_axes([0, 0, 1, 1])
        Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.layouts.get(name), finalize=True)
        ax.set_xlim(0, 420); ax.set_ylim(0, 297); ax.set_aspect('equal'); ax.axis('off')
        pdf.savefig(fig); plt.close(fig)
