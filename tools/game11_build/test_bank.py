import os, subprocess, tempfile, shutil, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from bank import Q

def src_of(q):
    t = q['test']
    if t.get('src'): return t['src']
    body = '\n'.join('    ' + l for l in q['code'].split('\n'))
    return '#include <stdio.h>\n\nint main(void) {\n' + body + '\n    return 0;\n}\n'

ok = bad = 0
report = []
for n, q in enumerate(Q):
    t = q['test']
    # ตัวเลือกไม่ซ้ำกัน
    assert len(set(q['c'])) == 4, ('dup choice', n)
    if not t:
        continue
    d = tempfile.mkdtemp()
    open(os.path.join(d, 'p.c'), 'w').write(src_of(q))
    r = subprocess.run(['gcc', '-std=c99', '-Wall', '-Wextra', '-pedantic', '-o', 'p', 'p.c'], cwd=d, capture_output=True, text=True)
    if r.returncode or r.stderr.strip():
        print('COMPILE', n, q['ax'], r.stderr); bad += 1; continue
    for f, c in (t.get('setup') or {}).items():
        open(os.path.join(d, f), 'w').write(c)
    out = ''
    for _ in range(t.get('runs', 1)):
        out += subprocess.run(['./p'], cwd=d, capture_output=True, text=True).stdout
    if t.get('cat'):
        out += open(os.path.join(d, t['cat'])).read()
    good = out == t['expect']
    if t.get('same'):
        good = good and q['c'][q['a']] == t['expect']
    shutil.rmtree(d)
    status = 'PASS' if good else 'FAIL'
    if good: ok += 1
    else: bad += 1
    report.append((n, q['ax'], q['lv'], status, repr(out), q['c'][q['a']]))
for r in report: print(*r, sep=' | ')
cnt = collections.Counter((q['ax'], q['lv']) for q in Q)
print('total', len(Q), 'with code', ok + bad, 'pass', ok, 'fail', bad)
for ax in sorted(set(q['ax'] for q in Q)):
    print(ax, {lv: cnt[(ax, lv)] for lv in ('easy', 'mid', 'hard')})
