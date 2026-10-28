import re
PAT = re.compile(r'<path ([^>]*?)/>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
def col(s):
    m = re.match(r'rgb\(([\d.]+)%, ([\d.]+)%, ([\d.]+)%\)', s or '')
    return tuple(round(float(v) * 2.55) for v in m.groups()) if m else None
def parse_d(d):
    toks = re.findall(r'[MLCZ]|-?[\d.]+', d)
    rings, cur, i, cmd = [], [], 0, None
    while i < len(toks):
        t = toks[i]
        if t in 'MLCZ':
            cmd = t; i += 1
            if t == 'Z':
                if cur: rings.append((cur, True)); cur = []
                continue
            if t == 'M' and cur: rings.append((cur, False)); cur = []
        if cmd in ('M', 'L'):
            cur.append((float(toks[i]), float(toks[i + 1]))); i += 2
        elif cmd == 'C':
            p0 = cur[-1]; p1 = (float(toks[i]), float(toks[i+1])); p2 = (float(toks[i+2]), float(toks[i+3])); p3 = (float(toks[i+4]), float(toks[i+5])); i += 6
            for k in range(1, 7):
                t_ = k / 6; a = (1 - t_)
                cur.append((a**3*p0[0]+3*a*a*t_*p1[0]+3*a*t_*t_*p2[0]+t_**3*p3[0], a**3*p0[1]+3*a*a*t_*p1[1]+3*a*t_*t_*p2[1]+t_**3*p3[1]))
        else:
            i += 1
    if cur: rings.append((cur, False))
    return rings
def iter_paths(fn):
    s = open(fn).read()
    s = s[s.find('</defs>'):]
    for m in PAT.finditer(s):
        a = dict(ATTR.findall(m.group(1)))
        tr = a.get('transform')
        M = (1, 0, 0, 1, 0, 0)
        if tr:
            M = tuple(float(v) for v in re.findall(r'-?[\d.]+', tr))
        rings = parse_d(a.get('d', ''))
        out = []
        for pts, closed in rings:
            out.append(([(M[0]*x + M[2]*y + M[4], M[1]*x + M[3]*y + M[5]) for x, y in pts], closed))
        yield dict(fill=col(a.get('fill')) if a.get('fill') not in (None, 'none') else None,
                   stroke=col(a.get('stroke')) if a.get('stroke') not in (None, 'none') else None,
                   sw=float(a.get('stroke-width', 1)) * abs(M[0] or M[1]) if 'stroke-width' in a else 0,
                   rings=out, start=m.start())
