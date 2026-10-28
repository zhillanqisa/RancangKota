import json
_M = json.load(open('/tmp/claude-0/-home-user-RancangKota/0ec6368c-024a-5301-a292-99ebcccb0e4b/scratchpad/pagemap.json'))
K = 101.6 / 72          # px per pt untuk img/r24full.png
def pt(E, N, sheet='A0'):
    m = _M[sheet]; return (m['ox'] + m['s'] * E, m['oy'] - m['s'] * N)
def px(E, N):
    x, y = pt(E, N); return (x * K, y * K)
def utm(x, y):
    m = _M['A0']; X, Y = x / K, y / K
    return ((X - m['ox']) / m['s'], (m['oy'] - Y) / m['s'])
# konversi koordinat lama (georef dari label grid) -> UTM benar
def fix_old(E, N):
    xl = (183.64 + (E - 306000) * 2.8344); yl = (173.2 + (9156600 - N) * 2.8344)
    m = _M['A0']; return ((xl - m['ox']) / m['s'], (m['oy'] - yl) / m['s'])
