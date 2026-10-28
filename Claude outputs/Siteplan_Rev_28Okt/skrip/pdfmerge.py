import io
from pypdf import PdfReader, PdfWriter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
W_PT, H_PT = 3370.0, 2384.0
def new_overlay():
    fig = plt.figure(figsize=(W_PT / 72, H_PT / 72))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W_PT); ax.set_ylim(H_PT, 0); ax.axis('off')
    fig.patch.set_alpha(0)
    return fig, ax
def merge(src_pdf, fig, out_pdf):
    buf = io.BytesIO(); fig.savefig(buf, format='pdf', transparent=True); plt.close(fig); buf.seek(0)
    base = PdfReader(src_pdf).pages[0]
    base.transfer_rotation_to_content()
    ov = PdfReader(buf).pages[0]
    base.merge_page(ov)
    w = PdfWriter(); w.add_page(base); w.compress_identical_objects() if hasattr(w, 'compress_identical_objects') else None
    with open(out_pdf, 'wb') as f: w.write(f)
