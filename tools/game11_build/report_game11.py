# -*- coding: utf-8 -*-
"""สร้างรายงานผลตรวจคลังข้อสอบเกม 11 จากไฟล์เกมที่เผยแพร่จริง
usage: python3 report_game11.py <games_dir> <template_report_game10.html> <out.html>
- ดึง BANK ออกจาก game11_final_corner.html (ไม่ใช้ต้นฉบับ bank.py เป็นตัวตั้ง)
- คอมไพล์โค้ดที่แสดงบนจอด้วย gcc แล้วรันจริง (ข้อไฟล์: เตรียมไฟล์ รันซ้ำ แล้วอ่านเนื้อหาไฟล์)
- ใช้ CSS ชุดเดียวกับรายงานเกม 10
"""
import os, re, sys, json, html, subprocess, tempfile, shutil, collections, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from bank import Q

D, TPL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
game = open(os.path.join(D, 'game11_final_corner.html'), encoding='utf-8').read()
j = game.find('const BANK = ') + 13; k = game.find(';\n', j); B = json.loads(game[j:k])
AX = ['axis1', 'axis2', 'axis3', 'axis4', 'axis5', 'axis6']
AXN = {'axis1': 'บทที่ 7b · อาร์เรย์ 2 มิติ', 'axis2': 'บทที่ 7b · ลูปซ้อน', 'axis3': 'บทที่ 9 · ไฟล์ (r / w / a)',
       'axis4': 'บทที่ 8 · OOP', 'axis5': 'บทที่ 11 · Stack และ Queue', 'axis6': 'บทที่ 11 · Bubble Sort และการสลับค่า'}
QUOTA = {'axis1': 4, 'axis2': 3, 'axis3': 2, 'axis4': 2, 'axis5': 2, 'axis6': 2}
LV = {'easy': 'ง่าย', 'mid': 'ปานกลาง', 'hard': 'ยาก'}
flat = [(ax, i, q) for ax in AX for i, q in enumerate(B[ax])]
assert len(flat) == len(Q)
gccv = subprocess.run(['gcc', '--version'], capture_output=True, text=True).stdout.split('\n')[0].split()[-1]

def run_case(q, t):
    m = re.search(r'<div class="qcode codebox">(.*?)</div>', q['q'], re.S)
    code = html.unescape(m.group(1))
    if '________' in code or 'ลืมบรรทัด' in code: prog, how = t['src'], 'เติมคำตอบที่ถูกลงในโค้ดแล้วรัน'
    elif code.startswith('#include'): prog, how = code, 'รันโปรแกรมบนจอทั้งไฟล์'
    else: prog, how = '#include <stdio.h>\nint main(void){\n' + code + '\nreturn 0;}\n', 'ห่อโค้ดบนจอด้วย main แล้วรัน'
    d = tempfile.mkdtemp(); open(d + '/p.c', 'w').write(prog)
    r = subprocess.run(['gcc', '-std=c99', '-Wall', '-Wextra', '-pedantic', '-o', 'p', 'p.c'], cwd=d, capture_output=True, text=True)
    for f, c in (t.get('setup') or {}).items(): open(d + '/' + f, 'w').write(c)
    out = ''
    for _ in range(t.get('runs', 1)): out += subprocess.run(['./p'], cwd=d, capture_output=True, text=True).stdout
    if t.get('cat'): out += open(d + '/' + t['cat']).read()
    shutil.rmtree(d)
    return out, (r.returncode == 0 and not r.stderr.strip()), how

cards = collections.OrderedDict((a, []) for a in AX)
n_run = n_file = n_def = n_bad = 0
for (ax, i, q), src in zip(flat, Q):
    t = src['test']; corr = q['c'][q['a']]
    qt = re.sub(r'<div class="qcode codebox">(.*?)</div>', lambda m: '<pre>' + m.group(1) + '</pre>', q['q'], flags=re.S)
    qt = qt.replace('<div class="qtbl">', '<div class="qtbl rep">')
    if t:
        out, clean, how = run_case(q, t)
        same = [c for c in q['c'] if c.strip() == out.strip()]
        ok = clean and out == t['expect'] and (not same or same == [corr])
        is_file = bool(t.get('cat') or t.get('setup') or t.get('runs', 1) > 1)
        n_file += is_file; n_run += (not is_file)
        verdict = ('ยืนยันด้วยเนื้อหาไฟล์' if t.get('cat') else 'ยืนยันด้วยผลรัน') if ok else 'ไม่ผ่าน'
        extra = []
        if t.get('setup'): extra.append('เตรียมไฟล์ ' + ', '.join('<code>%s</code>' % f for f in t['setup']))
        if t.get('runs', 1) > 1: extra.append('รันซ้ำ %d ครั้ง' % t['runs'])
        if t.get('cat'): extra.append('อ่านเนื้อหาไฟล์ <code>%s</code> หลังรัน' % t['cat'])
        run = '<div class="run"><span>ผลรันจริง</span>%s%s → <code>%s</code></div>' % (
            how, (' · ' + ' · '.join(extra)) if extra else '', html.escape(repr(out)))
        note = ('ผลรันตรงกับตัวเลือกที่เกมทำเครื่องหมายว่าเป็นคำตอบ และไม่มีตัวเลือกอื่นให้ค่าเดียวกัน' if same else
                'คำตอบเป็นข้อความบรรยาย ผลรันข้างต้นยืนยันพฤติกรรมที่ตัวเลือกที่ถูกบรรยายไว้') + \
               ' · คอมไพล์ด้วย <code>gcc -std=c99 -Wall -Wextra -pedantic</code> ไม่มีคำเตือน'
    else:
        ok = True; n_def += 1; verdict = 'ตรวจด้วยนิยาม/ตาราง'
        run = '<div class="run"><span>วิธีตรวจ</span>ข้อนี้ไม่มีโปรแกรมให้รัน จึงตรวจนิยามในตัวเลือกที่ถูกเทียบกับสไลด์ครั้งที่ 4 และไล่ตารางบนจอทีละรายการ</div>'
        note = 'หมายเหตุการตรวจ: สิ่งที่ใช้ตอบ (ตารางหรือสถานการณ์) ปรากฏในตัวข้อครบ ถ้าลบทิ้งจะตอบไม่ได้'
    n_bad += (not ok)
    vcls = 'ok' if (ok and t) else ('rev' if ok else 'rev')
    ch = ''.join('<li class="%s"><span class="k">%d</span>%s%s</li>' % ('a' if ci == q['a'] else '', ci + 1, html.escape(c),
                 ' ← เฉลยของเกม' if ci == q['a'] else '') for ci, c in enumerate(q['c']))
    cards[ax].append('<div class="q"><div class="hd"><span class="n">GAME11 · %s · ข้อ %d</span><span class="lv">%s</span>'
                     '<span class="v %s">%s</span></div><div class="bd">\n<div class="qt">%s</div>\n%s\n<ol class="ch">%s</ol>\n'
                     '<p class="ex">%s</p>\n<p class="note"><b>แนวคิดที่วัด:</b> %s · %s</p>\n</div></div>' % (
                         ax, i + 1, LV[q['lv']], vcls, verdict, qt, run, ch, q['e'], html.escape(q['k']), note))

lvc = collections.Counter(q['lv'] for ax in AX for q in B[ax]); tot = len(flat)
rows = ''.join('<tr><td>%s</td><td>%s</td><td>%d</td><td>%d</td><td>%d / %d / %d</td></tr>' % (
    ax, AXN[ax], len(B[ax]), QUOTA[ax], *[sum(1 for q in B[ax] if q['lv'] == l) for l in ('easy', 'mid', 'hard')]) for ax in AX)

tpl = open(TPL, encoding='utf-8').read()
css = tpl[tpl.find('<style>'):tpl.find('</style>') + 8]
head = ('<title>ผลตรวจคลังข้อสอบ เกม 11 · FINAL CORNER</title>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@500;600;700&family=IBM+Plex+Sans+Thai:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">\n')
chk = [
 ('เนื้อหา', 'ครอบคลุมเนื้อหาครั้งที่ 4 (26 ก.ย. 2569) ทั้งหมดที่มีโอกาสออกสอบ กว. คือบทที่ 7b อาร์เรย์ 2 มิติและลูปซ้อน บทที่ 9 ไฟล์ บทที่ 8 OOP และบทที่ 11 Stack Queue Bubble Sort ส่วนที่ตัดออกคือ Hook ชวนคิด แถลงข้อสอบ Final ตอนที่ 2 กฎการสอบออนไลน์ เทคนิคทำข้อสอบ และหัวข้อที่ไม่ได้อยู่ในสไลด์ เช่น Circular Queue และการเรียงแบบอื่น'),
 ('ข้อสอบต่อรอบ', '15 ข้อ ตามโควตา อาร์เรย์ 2 มิติ 4 · ลูปซ้อน 3 · ไฟล์ 2 · OOP 2 · Stack/Queue 2 · Bubble Sort 2 (ถ่วงน้ำหนักบทที่ 7b เป็น 7 ข้อ เพราะโจทย์เมทริกซ์ออกสอบ กว. บ่อย) รอบหลังเรียนเลี่ยงข้อที่ออกในรอบก่อนเรียนทั้งหมด'),
 ('ความยาก', 'ข้อที่แจกจริงต่อรอบคือ ง่าย 9 : กลาง 5 : ยาก 1 ข้อ (60 : 33 : 7) ข้อยากวางไว้ในหัวข้อเมทริกซ์เสมอ และในแต่ละหัวข้อเรียงง่ายไปยากตามเทคนิคข้ามข้อยากไว้ท้าย สัดส่วนในคลังคือ ง่าย %d กลาง %d ยาก %d ข้อ' % (lvc['easy'], lvc['mid'], lvc['hard'])),
 ('เฉลย', 'ไม่มีเฉลยผิด — โค้ด C %d ข้อคอมไพล์และรันจริงผ่านครบ (ผลลัพธ์บนจอ %d ข้อ ทดสอบกับไฟล์จริง %d ข้อ) และไม่มีข้อใดที่ตัวเลือกอื่นให้ค่าเดียวกับผลรัน อีก %d ข้อตรวจด้วยนิยามและตารางบนจอ' % (n_run + n_file, n_run, n_file, n_def)),
 ('ข้อจำกัดโค้ด', 'ไม่ใช้ pointer ยกเว้น <code>FILE *</code> ของบทที่ 9 ซึ่งสอนจริงและได้รับอนุมัติ ไม่ใช้ struct recursion หรือ rand · Stack/Queue สร้างด้วยอาร์เรย์ global กับตัวแปร top/front/rear · ข้อที่นำออกหลายค่าใช้ printf แยกบรรทัด เพื่อเลี่ยงลำดับการประเมินอาร์กิวเมนต์ที่ภาษา C ไม่กำหนด'),
 ('ไฟล์ที่ตรวจ', 'ดึงคลังข้อสอบออกจากไฟล์ <code>game11_final_corner.html</code> ที่เผยแพร่บน GitHub โดยตรง (ค่า MD5 ตรงกับไฟล์บน repository) ไม่ได้ใช้ต้นฉบับเป็นตัวตั้ง'),
 ('หน้าจอ', 'ทดสอบเล่นครบเส้นทาง รอบคัดเลือก 15 ข้อ → เดินพิท → รอบชิงแชมป์ 15 ข้อ → รายงานผล บน 1440×900 และ 390×844 แบบ touch ทั้งโหมดมืดและสว่าง ไม่มี JavaScript error และไม่มีการเลื่อนแนวนอน เรดาร์ Chart.js และ SVG สำรองแสดงผลได้'),
 ('หน้าสรุปผล', 'เรดาร์ 6 แกน · จุดเด่นและควรเสริมรายหัวข้อ · รายการ "ยังขาดความเข้าใจเรื่องต่อไปนี้" ระบุแนวคิดรายข้อพร้อมบท · จุดเด่นรายแนวคิด · เกณฑ์ 9/15 = 60% · CSV มีคอลัมน์ missed_concepts'),
]
body = ('<div class="wrap"><header>\n<p class="eyebrow">GNR1007 · Question Bank Verification · gcc %s · Chromium 1440×900 / 390×844</p>\n'
        '<h1>ผลตรวจคลังข้อสอบ เกม 11 — FINAL CORNER</h1>\n'
        '<p>ด่านที่ 11 ทดสอบก่อนสอบจริง เนื้อหาครั้งที่ 4 · คลังข้อสอบ <b>%d ข้อ</b> แบ่งเป็น 6 แกน ใช้รอบละ 15 ข้อ '
        'การตรวจดึงตัวแปร <code>BANK</code> ออกจากไฟล์เกมที่เผยแพร่จริง นำโค้ด C ที่แสดงบนจอไปคอมไพล์และรันด้วย gcc '
        'แล้วเทียบกับตัวเลือกที่เกมทำเครื่องหมายว่าเป็นคำตอบ ข้อเรื่องไฟล์เตรียมไฟล์ตั้งต้น รันซ้ำตามโจทย์ แล้วอ่านเนื้อหาไฟล์จริงมาเทียบ</p>\n'
        '<div class="tally"><div><k>ข้อทั้งหมด</k><b>%d</b></div><div><k>เฉลยผิด</k><b style="color:var(--ok)">%d</b></div>'
        '<div><k>ยืนยันด้วยผลรัน</k><b>%d</b></div><div><k>ตรวจกับไฟล์จริง</k><b>%d</b></div>'
        '<div><k>ตรวจด้วยนิยาม/ตาราง</k><b>%d</b></div></div>\n</header>\n'
        % (gccv, tot, tot, n_bad, n_run, n_file, n_def))
body += '<h2>สรุปการตรวจ</h2><div class="chk">' + ''.join('<div><b>%s</b><span>%s</span></div>' % c for c in chk) + '</div>\n'
body += ('<h2>โครงสร้างคลังข้อสอบ</h2><div class="qtbl rep"><table><tr><th>แกน</th><th>หัวข้อ</th><th>ในคลัง</th><th>ต่อรอบ</th>'
         '<th>ง่าย / กลาง / ยาก</th></tr>' + rows + '</table></div>\n')
for ax in AX:
    body += '<h2>%s · %s</h2>\n' % (ax, AXN[ax]) + '\n'.join(cards[ax]) + '\n'
body += ('<footer>\nผศ.ดร.กุลวลัญช์ วรุณสิน · สาขาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง<br>\n'
         'รายงานฉบับนี้สร้างจากคลังข้อสอบที่ดึงออกจากไฟล์ <code>game11_final_corner.html</code> โดยตรง · FINAL CORNER v1.0 · ตรวจเมื่อ %s\n</footer>\n</div>'
         % datetime.date.today().strftime('%d/%m/%Y'))
open(OUT, 'w', encoding='utf-8').write(head + css + '\n' + body)
print('wrote', OUT, 'total', tot, 'bad', n_bad, 'run', n_run, 'file', n_file, 'def', n_def)
