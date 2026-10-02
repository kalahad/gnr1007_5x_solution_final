# -*- coding: utf-8 -*-
"""สร้าง game11_final_corner.html จากแม่แบบ game10_championship.html (UI v7.0)
usage: python3 build_game11.py <games_dir>
"""
import os, re, sys, json, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bank import Q

D = sys.argv[1] if len(sys.argv) > 1 else '.'
s = open(os.path.join(D, 'game10_championship.html'), encoding='utf-8').read()
M1, M2 = '<!-- GNR-CORE:BEGIN -->', '<!-- GNR-CORE:END -->'
s = re.sub(re.escape(M1) + r'.*?' + re.escape(M2) + r'\n?', '', s, flags=re.S)

def R(old, new, count=1):
    global s
    n = s.count(old)
    assert n >= 1, 'not found: ' + old[:90]
    if count == 1: assert n == 1, 'ambiguous (%d): %s' % (n, old[:90])
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)

def RX(pat, new, flags=re.S):
    global s
    s2, n = re.subn(pat, lambda m: new, s, count=1, flags=flags)
    assert n == 1, 'regex not found: ' + pat[:90]
    s = s2

# ------------------------------------------------------------------ head
R('<title>CHAMPIONSHIP FINAL : รอบชิงแชมป์ | GNR1007</title>', '<title>FINAL CORNER : โค้งสุดท้ายพิชิต กว. | GNR1007</title>')
RX(r'<meta name="description" content="[^"]*">', '<meta name="description" content="ด่านที่ 11 ทดสอบก่อนสอบจริงด้วยเนื้อหาครั้งที่ 4 อาร์เรย์ 2 มิติ ลูปซ้อน ไฟล์ OOP Stack Queue และ Bubble Sort 15 ข้อ จับเวลา 108 วินาทีต่อข้อ พร้อมเรดาร์ 6 แกน — GNR1007 · ผศ.ดร.กุลวลัญช์ วรุณสิน มหาวิทยาลัยรามคำแหง">')
R('<meta property="og:title" content="CHAMPIONSHIP FINAL : รอบชิงแชมป์">', '<meta property="og:title" content="FINAL CORNER : โค้งสุดท้ายพิชิต กว.">')
RX(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="โค้งสุดท้ายก่อนสอบ 15 ข้อ 6 หัวข้อของครั้งที่ 4 วัดผลก่อน-หลัง บอกแนวคิดที่ยังพลาดและจุดเด่นรายหัวข้อ">')
# ดาว 15 ดวง: ย่อขนาดให้อยู่ในแถวเดียว/สองแถวบนมือถือ
R('</head>', '<style id="g11-extra">\n'
  '#reveal .star{width:clamp(16px,5.4vw,30px);height:clamp(16px,5.4vw,30px)}\n'
  '#reveal .star-row{gap:clamp(2px,.9vw,6px);max-width:560px;margin-left:auto;margin-right:auto}\n'
  '.star-row.sm .star{width:15px;height:15px}.star-row.sm{gap:2px;max-width:190px;margin-left:auto;margin-right:auto}\n'
  '.advice li.head{background:none !important;border:none !important;box-shadow:none !important;padding:10px 2px 0 !important;font-weight:600;font-size:.86rem;color:var(--text)}\n'
  '.advice li.head::before{content:none}\n'
  '.advice li.miss::before{content:"\\2715";color:var(--red)}.advice li.hit::before{content:"\\2713";color:var(--corner)}\n'
  '.advice li small{display:block;color:var(--muted);font-size:.74rem;margin-left:1.3em}\n'
  '</style>\n</head>')

R('   CHAMPIONSHIP FINAL : รอบชิงแชมป์  v1.0 "GNR GRAND PRIX · CLIMB MODE"', '   FINAL CORNER : โค้งสุดท้ายพิชิต กว.  v1.0 "GNR GRAND PRIX · CLIMB MODE" — ด่านที่ 11')
R('   ทบทวนบทที่ 1-7a และบทที่ 10 ก่อนสอบกลางภาค 13 กันยายน 2569', '   ทดสอบก่อนสอบจริง เนื้อหาครั้งที่ 4 (26 ก.ย. 2569) บทที่ 7b, 9, 8, 11 · แม่แบบจาก CHAMPIONSHIP (เกม 10)')
# ------------------------------------------------------------------ arcade / reveal / brand
R('ข้อ <b id="acProg">0/7</b>', 'ข้อ <b id="acProg">0/15</b>')
R('<div class="rv-score" id="rvScore">0/7</div>', '<div class="rv-score" id="rvScore">0/15</div>')
R('<span>CHAMPIONSHIP FINAL</span>', '<span>FINAL CORNER</span>')
R('aria-label="สนามแข่งกลางคืนพร้อมถ้วยรางวัลและป้ายนับรอบเจ็ดรอบ"', 'aria-label="สนามแข่งกลางคืนพร้อมถ้วยรางวัลด่านที่ 11"')
R('fill="#150a2c" font-weight="700">7</text>', 'fill="#150a2c" font-weight="700">11</text>')
R('>7 LAPS · 7 CHAPTERS · 108 SECONDS EACH</text>', '>15 LAPS · 6 SKILLS · 108 SECONDS EACH</text>')
R('<h1 class="title">CHAMPIONSHIP FINAL : รอบชิงแชมป์</h1>', '<h1 class="title">FINAL CORNER : โค้งสุดท้ายพิชิต กว.</h1>')
RX(r'<p class="subtitle">.*?</p>',
   '<p class="subtitle">ด่านที่ 11 โค้งสุดท้ายของฤดูกาล GNR GRAND PRIX — ทดสอบก่อนสอบจริงด้วยเนื้อหา <b>ครั้งที่ 4 ทั้งหมด</b> '
   'คืออาร์เรย์ 2 มิติ ลูปซ้อน ไฟล์ OOP Stack/Queue และ Bubble Sort วิ่ง <b>15 รอบ เท่ากับ 15 ข้อ</b> จับเวลา <b>108 วินาทีต่อข้อ</b> '
   'จบแล้วรับเรดาร์ 6 แกน พร้อมรายชื่อแนวคิดที่ยังพลาดและจุดเด่นของตัวเอง</p>')
RX(r'<div class="feature-row">.*?</div>',
   '<div class="feature-row"><span>บทที่ 7b · 9 · 8 · 11</span><span>15 ข้อต่อรอบ</span><span>จับเวลา 108 วินาทีต่อข้อ</span>'
   '<span>คลังข้อสอบ %d ข้อ</span><span>ง่าย 60 : กลาง 30 : ยาก 10</span><span>เรดาร์ 6 แกน</span>'
   '<span>ผ่าน 9/15 = เกณฑ์ 60%% ของ กว.</span><span>ส่งออกคะแนน CSV</span></div>' % len(Q))

HOWTO = ('<div class="howto">\n'
 '      <div class="hk"><b>แตะ</b><span>เล่นด้วยการแตะคำตอบอย่างเดียว ไม่มีปุ่มเดิน ไม่มีปุ่มกระโดด</span></div>\n'
 '      <div class="hk"><b>ตอบถูก</b><span>วิ่งครบเพิ่มอีก 1 รอบทันที · ต่อเนื่องหลายข้อได้โบนัส Combo</span></div>\n'
 '      <div class="hk"><b>ตอบผิด</b><span>ไม่ตกรอบ ไม่มีแพ้ — อ่านเฉลยแล้วไปข้อถัดไปได้เลย</span></div>\n'
 '      <div class="hk"><b>108 วินาที</b><span>หมดเวลาข้อไหนถือว่าข้อนั้นไม่ได้คะแนน แต่ยังอ่านเฉลยและไปต่อได้</span></div>\n'
 '      <div class="hk"><b>1 2 3 4</b><span>ทางลัดสำหรับคอมพิวเตอร์ (บนมือถือใช้แตะปุ่มใหญ่)</span></div>\n'
 '      <div class="hk"><b>ดาว</b><span>ตอบถูก 1 ข้อ = 1 ดาว เต็ม 15 ข้อ = 15 ดาว · ได้ 9 ดาวขึ้นไปเท่ากับผ่านเกณฑ์ 60%</span></div>\n'
 '    </div>')
RX(r'<!-- ===== PRETEST ===== -->.*?<!-- ===== SUMMARY ===== -->', '''<!-- ===== PRETEST ===== -->
<section id="scr-pretest" class="screen">
  <div class="panel">
    <span class="tag">Checkpoint 00 · Qualifying</span>
    <h2>รอบคัดเลือก — วัดความพร้อมก่อนทบทวน</h2>
    <p class="muted">15 ข้อ ครอบคลุมเนื้อหาครั้งที่ 4 ทั้งหมด แบ่งเป็น อาร์เรย์ 2 มิติ 4 ข้อ ลูปซ้อน 3 ข้อ ไฟล์ 2 ข้อ OOP 2 ข้อ
      Stack/Queue 2 ข้อ และ Bubble Sort 2 ข้อ จับเวลา <b>108 วินาทีต่อข้อ</b> เท่าเกณฑ์ของสนามสอบจริง
      ผลชุดนี้คือ <b>เส้นฐาน</b> ที่ใช้เทียบกับรอบชิงแชมป์</p>
    ''' + HOWTO + '''
    <div class="btn-row"><button class="btn primary" id="preLaunch" style="flex:1">ออกสตาร์ทรอบคัดเลือก</button></div>
  </div>
</section>

<!-- ===== PIT WALK ===== -->
<section id="scr-pitwalk" class="screen">
  <div class="panel">
    <span class="tag">Pit Walk · ทบทวนรายหัวข้อ</span>
    <h2>เดินพิท: ทบทวนทีละหัวข้อก่อนเข้าโค้งสุดท้าย</h2>
    <p>แต่ละการ์ดคือ <b>หนึ่งหัวข้อของครั้งที่ 4</b> เปิดดูจุดหลอก กว. ที่ออกบ่อยที่สุดของหัวข้อนั้น
      แล้วลง <b>ซ้อมรอบละ 3 ข้อ</b> เพื่อเช็กว่าเข้าใจจริง บางหัวข้อมีปุ่มเปิดเกมพื้นฐานที่เกี่ยวข้องให้ทวนต่อ</p>
    <p class="muted">ผลรอบซ้อมไม่นับเป็นดาว แต่ระบบใช้ประกอบการจัดลำดับ <b>ตารางซ้อม 8 วัน</b> ในหน้ารายงานผล
      หัวข้อที่ยังไม่ได้ซ้อมจะถูกถือว่าเป็นจุดที่ต้องดูก่อน</p>
    <div class="pitgrid" id="pitGrid"></div>
    <div class="status-line" id="pitStatus">ซ้อมครบกี่หัวข้อแล้วจะแสดงตรงนี้</div>
    <div class="btn-row"><button class="btn primary" id="goPost" style="flex:1">พร้อมแล้ว ลงรอบชิงแชมป์</button></div>
  </div>
</section>

<!-- ===== POSTTEST ===== -->
<section id="scr-posttest" class="screen">
  <div class="panel">
    <span class="tag">Checkpoint 02 · Final Corner</span>
    <h2>รอบชิงแชมป์ — โค้งสุดท้ายก่อนสอบจริง</h2>
    <p class="muted">15 ข้อชุดใหม่ สัดส่วนหัวข้อเท่ารอบคัดเลือก ระบบเลี่ยงข้อที่เคยออกไปแล้ว จับเวลา <b>108 วินาทีต่อข้อ</b> เช่นเดิม
      จบรอบนี้แล้วจะได้เรดาร์ 6 แกน รายชื่อแนวคิดที่ยังพลาด จุดเด่น และตารางซ้อมรายวัน</p>
    ''' + HOWTO + '''
    <div class="btn-row"><button class="btn primary" id="postLaunch" style="flex:1">ออกสตาร์ทรอบชิงแชมป์</button></div>
  </div>
</section>

<!-- ===== SUMMARY ===== -->''')

R('<h2>สรุปผลภารกิจ CHAMPIONSHIP FINAL</h2>', '<h2>สรุปผลภารกิจ FINAL CORNER</h2>')
R('<h3 style="margin-top:20px">Car Setup Radar — เรดาร์ 7 แกน</h3>', '<h3 style="margin-top:20px">Car Setup Radar — เรดาร์ 6 แกน</h3>')
RX(r'<p class="muted">แต่ละแกนคือหนึ่งบท คิดจากข้อของบทนั้น.*?</p>',
   '<p class="muted">แต่ละแกนคือหนึ่งหัวข้อของครั้งที่ 4 คิดเป็นร้อยละของข้อที่ตอบถูกในหัวข้อนั้น '
   'รูปที่ซ้อนกันคือก่อนทบทวนเทียบกับหลังทบทวน <b>แกนไหนบุ๋มเข้าหาศูนย์กลางคือจุดที่ต้องจูนก่อน</b></p>')
R('<h3 style="margin-top:20px">ผลรายบท</h3>', '<h3 style="margin-top:20px">ผลรายหัวข้อ</h3>')
R('ระบบเรียงบทจากแกนที่อ่อนที่สุดไปแข็งที่สุด', 'ระบบเรียงหัวข้อจากแกนที่อ่อนที่สุดไปแข็งที่สุด')
R('บทที่อ่อนที่สุดจะถูกวางไว้ทั้งวันแรกและวันสุดท้าย', 'หัวข้อที่อ่อนที่สุดจะถูกวางไว้ทั้งวันแรกและวันสุดท้าย')
R('<h3 style="margin-top:20px">กลับเข้าพิท — เปิดเกมประจำบทที่ยังอ่อน</h3>', '<h3 style="margin-top:20px">กลับเข้าพิท — เปิดเกมพื้นฐานของหัวข้อที่ยังอ่อน</h3>')
R('<h3 style="margin-top:20px">ข้อเสนอแนะเฉพาะบุคคล</h3>', '<h3 style="margin-top:20px">วิเคราะห์ความเข้าใจรายแนวคิด และข้อเสนอแนะ</h3>')
R('<button class="btn primary" id="btnReview">ทบทวนบทที่อ่อนที่สุด</button>', '<button class="btn primary" id="btnReview">ทบทวนหัวข้อที่อ่อนที่สุด</button>')
RX(r'<footer>.*?</footer>', '''<footer>
  <p><b>GNR1007</b> · การโปรแกรมคอมพิวเตอร์สำหรับวิศวกร — ด่านที่ 11 ทดสอบก่อนสอบจริง เนื้อหาครั้งที่ 4 (26 ก.ย. 2569) บทที่ 7b, 9, 8 และ 11</p>
  <p>ผศ.ดร.กุลวลัญช์ วรุณสิน · สาขาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์ มหาวิทยาลัยรามคำแหง</p>
  <p class="fmono">FINAL CORNER v1.0 — GNR GRAND PRIX · CLIMB MODE (TAP-ONLY) · MOBILE FIRST · SINGLE-FILE BUILD</p>
</footer>''')

# ------------------------------------------------------------------ AXES
AXES_JS = r'''/* ============ 4) หกแกน = หกหัวข้อของเนื้อหาครั้งที่ 4 ============ */
const AXES = [
  {key:'axis1', lap:1, ch:'บทที่ 7b', name:'อาร์เรย์ 2 มิติ', short:'อาร์เรย์ 2 มิติ',
   tag:'a[แถว][หลัก] · แนวทแยงหลักและรอง · ขนาดหน่วยความจำ',
   hint:['<code>a[i][j]</code> คือ <b>แถว i หลัก j</b> — แถวก่อน หลักตาม และวาดตารางเล็ก ๆ ข้างโจทย์ทุกครั้ง',
         'ตัวเลือกหลอกมักเป็นค่าของ <code>a[j][i]</code> เสมอ ตรวจให้แน่ว่าไม่ได้สลับแถวกับหลัก',
         'แนวทแยงหลักคือ <code>m[i][i]</code> (ซ้ายบนลงขวาล่าง) แนวทแยงรองคือ <code>m[i][n-1-i]</code> (ขวาบนลงซ้ายล่าง)',
         'ขนาดหน่วยความจำ = <b>แถว × หลัก × ขนาดชนิดข้อมูล</b> เช่น <code>int a[3][4]</code> = 3 × 4 × 4 = 48 ไบต์'],
   games:[['game9_lap_timer.html','เกม 9 · LAP TIMER']]},
  {key:'axis2', lap:2, ch:'บทที่ 7b', name:'ลูปซ้อน (Nested Loop)', short:'ลูปซ้อน',
   tag:'นับรอบ · ลูปในเริ่มที่ i · ตีตารางทดค่า',
   hint:['ลูปนอกขยับ 1 ก้าว ลูปในวิ่งจนครบ — ถ้าจุดเริ่มคงที่ จำนวนรอบรวมคือ <b>รอบนอก × รอบใน</b>',
         'ถ้าลูปในเริ่มที่ <code>j = i</code> รอบจะเป็นทรงสามเหลี่ยม เช่น 3 + 2 + 1 = 6 ไม่ใช่ 3 × 3',
         '<code>&lt;</code> กับ <code>&lt;=</code> ต่างกัน 1 รอบ ให้เขียนค่ารอบแรกและรอบสุดท้ายกำกับไว้เสมอ',
         '<code>break</code> ในลูปในออกจากลูปในชั้นเดียว ลูปนอกยังทำรอบถัดไปตามปกติ',
         'ลูปซ้อนใหญ่ ๆ ใช้เวลามาก ในห้องสอบให้ข้ามไว้ทำท้ายสุด'],
   games:[['game5_loop_factory.html','เกม 5 · LOOP FACTORY'],['game6_trace_detective.html','เกม 6 · TRACE DETECTIVE']]},
  {key:'axis3', lap:3, ch:'บทที่ 9', name:'ไฟล์ (r / w / a)', short:'ไฟล์',
   tag:'fopen → ใช้งาน → fclose · โหมด r w a · เช็ก NULL',
   hint:['<code>"r"</code> อ่านอย่างเดียว ไฟล์ต้องมีอยู่จริง ถ้าไม่มีจะได้ <b>NULL</b> และไม่สร้างไฟล์ให้',
         '<code>"w"</code> <b>ล้างไฟล์ทันทีที่เปิด</b> แม้ยังไม่ fprintf — รันซ้ำก็ล้างซ้ำทุกครั้ง',
         '<code>"a"</code> เขียนต่อท้ายของเดิม และสร้างไฟล์ใหม่ให้ถ้ายังไม่มี',
         'พิธีกรรม 3 ขั้นคือ fopen → ใช้งาน (เช็ก NULL ก่อน) → fclose ถ้าไม่ปิด ข้อมูลอาจค้างใน buffer'],
   games:[]},
  {key:'axis4', lap:4, ch:'บทที่ 8', name:'การเขียนโปรแกรมเชิงวัตถุ (OOP)', short:'OOP',
   tag:'Class กับ Object · 4 เสาหลัก',
   hint:['<b>Class</b> คือพิมพ์เขียว <b>Object</b> คือของจริงที่สร้างจากพิมพ์เขียว',
         'Encapsulation ห่อหุ้ม (ซ่อนข้อมูล) · Inheritance สืบทอด · Polymorphism พ้องรูป · Abstraction นามธรรม',
         'Polymorphism คือ Method ชื่อเดียวทำงานต่างกันตามชนิด Object ไม่ใช่การสืบทอด',
         'Encapsulation เน้นป้องกันข้อมูล ส่วน Abstraction เน้นโชว์เฉพาะที่จำเป็น — และภาษา C ไม่มี Class'],
   games:[]},
  {key:'axis5', lap:5, ch:'บทที่ 11', name:'Stack และ Queue', short:'Stack / Queue',
   tag:'LIFO กับ FIFO · push pop · enqueue dequeue',
   hint:['<b>Stack = LIFO</b> เหมือนถาดซ้อน push และ pop ที่ Top เท่านั้น',
         '<b>Queue = FIFO</b> เหมือนเข้าแถว เข้าท้ายแถว ออกหัวแถว',
         'push 1, 2, 3 แล้ว pop ได้ 3 ไม่ใช่ 1 — ตีตารางสถานะหลังทุกคำสั่ง',
         'Undo และการเรียกฟังก์ชันใช้ Stack · คิวเครื่องพิมพ์และคิวงานเซิร์ฟเวอร์ใช้ Queue'],
   games:[['game8_pit_crew.html','เกม 8 · PIT CREW']]},
  {key:'axis6', lap:6, ch:'บทที่ 11', name:'Bubble Sort และการสลับค่า', short:'Bubble Sort',
   tag:'สลับด้วย temp · หลังรอบที่ 1 · จำนวนรอบ n-1',
   hint:['เทียบคู่ติดกันจากซ้ายไปขวา ตัวใหญ่ลอยไปท้ายทีละรอบ — <b>หนึ่งรอบ หนึ่งแชมป์เข้าที่</b>',
         'หลังรอบที่ 1 การันตีเพียงตัวใหญ่สุดอยู่ท้าย ตัวที่เหลือยังไม่เรียง',
         'ข้อมูล n ตัวใช้ <b>ไม่เกิน n-1 รอบ</b> และรอบแรกเทียบ n-1 คู่',
         'การสลับค่าต้องมี <code>temp</code> ถ้าเขียน <code>a = b; b = a;</code> ค่าเดิมของ a จะหายทันที'],
   games:[['game9_lap_timer.html','เกม 9 · LAP TIMER']]}
];
const AXIS_BY_KEY = {}; AXES.forEach(a => { AXIS_BY_KEY[a.key] = a; });
const SKILL_LABELS = {}; AXES.forEach(a => { SKILL_LABELS[a.key] = a.ch + ' ' + a.short; });
const QUOTA = {axis1:4, axis2:3, axis3:2, axis4:2, axis5:2, axis6:2};   /* 15 ข้อต่อรอบ ถ่วงน้ำหนักบทที่ 7b */
const Q_TOTAL = 15;
const LV_LABEL = {easy:'ง่าย', mid:'ปานกลาง', hard:'ยาก'};
'''
RX(r'/\* ============ 4\) แกนทั้งเจ็ด.*?const LV_LABEL = \{[^\n]*\n', AXES_JS)

# ------------------------------------------------------------------ BANK
def CD(code): return '<div class="qcode codebox">' + html.escape(code, quote=False) + '</div>'
bank = {}
for q in Q:
    txt = q['q'] + (CD(q['code']) if q['code'] else '') + (q['after'] or '')
    bank.setdefault(q['ax'], []).append({'q': txt, 'c': q['c'], 'a': q['a'], 'e': q['e'], 'lv': q['lv'], 'k': q['k']})
RX(r'const BANK = \{"axis1".*?\]\};\n', 'const BANK = ' + json.dumps(bank, ensure_ascii=False) + ';\n')
R('   - สัดส่วนความยาก ง่าย 60 : กลาง 30 : ยาก 10 เท่าสัดส่วนของข้อสอบจริง',
  '   - สัดส่วนความยาก ง่าย 60 : กลาง 30 : ยาก 10 เท่าสัดส่วนของข้อสอบจริง\n'
  '   - ไม่ใช้ pointer (ยกเว้น FILE * ของบทที่ 9 ที่สอนจริง) struct recursion และ rand\n'
  '   - k คือแนวคิดของข้อ ใช้สรุปว่าผู้เรียนยังขาดความเข้าใจเรื่องใด')

# ------------------------------------------------------------------ STATE / STARS
R("const SKEY = 'championshipfinal_v1_state';", "const SKEY = 'finalcorner_v1_state';")
R('  preTimeouts:0, postTimeouts:0,', '  preTimeouts:0, postTimeouts:0, preLog:[], postLog:[],')
RX(r'/\* ============ 7\) STAR SYSTEM.*?const MAX_STARS = 7;[^\n]*\n', '''/* ============ 7) STAR SYSTEM — เต็ม 15 ดวง เท่ากับ 15 ข้อ · 9 ดวง = เกณฑ์ผ่าน 60% ============ */
const STAR_TABLE = [
  {min:15, stars:15, rank:'PERFECT CORNER', msg:'ถูกครบทั้ง 15 ข้อ เนื้อหาครั้งที่ 4 แน่นทุกหัวข้อ พร้อมเข้าห้องสอบเต็มที่ เหลือแค่รักษาความเร็วต่อข้อไว้ให้ได้'},
  {min:13, stars:13, rank:'RACE WINNER',    msg:'แม่นมาก เหลือเพียงแนวคิดเล็กน้อยที่ยังพลาด ดูรายการแนวคิดในรายงานผลแล้วทวนเฉพาะจุดนั้น'},
  {min:11, stars:11, rank:'PODIUM FINISH',  msg:'ผ่านเกณฑ์อย่างมั่นคง มีบางหัวข้อที่ยังต้องจูน ใช้เรดาร์และตารางซ้อมไล่ให้ครบก่อนวันสอบ'},
  {min:9,  stars:9,  rank:'POINTS FINISH',  msg:'ผ่านเกณฑ์ 60% แล้ว แต่ยังเฉียดเส้น ควรกลับไปทวนหัวข้อที่เรดาร์บุ๋มก่อนสอบจริง'},
  {min:6,  stars:6,  rank:'MIDFIELD',       msg:'ยังไม่ถึงเกณฑ์ 60% พื้นฐานมีอยู่แต่ยังกระจายไม่ทั่ว เริ่มจากแนวคิดที่ระบบบอกว่ายังพลาด'},
  {min:3,  stars:3,  rank:'BACKMARKER',     msg:'ยังต้องใช้เวลาอีกพอสมควร ทวนสไลด์ครั้งที่ 4 ทีละหัวข้อ ซ้อมในหน้าเดินพิท แล้วกลับมาวัดใหม่'},
  {min:0,  stars:0,  rank:'FORMATION LAP',  msg:'ยังไม่คุ้นเนื้อหา ไม่เป็นไรเลย เริ่มจากหัวข้อแรกในตารางซ้อมได้ทันที'}
];
const MAX_STARS = 15;   /* เต็ม 15 ข้อ = เต็ม 15 ดาว · 1 ดาว = ตอบถูก 1 ข้อ */
''')

# ------------------------------------------------------------------ NAV
R("if(s.key==='posttest'&&state.post!==null) sub=state.post+'/7';", "if(s.key==='posttest'&&state.post!==null) sub=state.post+'/'+Q_TOTAL;")
R("if(s.key==='pretest'&&state.pre!==null) sub=state.pre+'/7';", "if(s.key==='pretest'&&state.pre!==null) sub=state.pre+'/'+Q_TOTAL;")
R("if(s.key==='pitwalk') sub=practicedCount()+'/7';", "if(s.key==='pitwalk') sub=practicedCount()+'/'+AKEYS.length;")

# ------------------------------------------------------------------ question selection
R("function randomizeChoices(q){const order=shuffle(q.c.map((c,i)=>i));return {q:q.q,e:q.e,lv:q.lv,c:order.map(i=>q.c[i]),a:order.indexOf(q.a)};}",
  "function randomizeChoices(q){const order=shuffle(q.c.map((c,i)=>i));return {q:q.q,e:q.e,lv:q.lv,k:q.k,c:order.map(i=>q.c[i]),a:order.indexOf(q.a)};}")
RX(r'/\* หนึ่งข้อต่อหนึ่งบท ครบทั้งเจ็ดบท.*?return picks;[^\n]*\n\}\n', '''/* 15 ข้อต่อรอบ ตามโควตา 4/3/2/2/2/2 และคุมความยาก 60 : 30 : 10
   ยาก 1 ข้อ (10%) วางไว้ในหัวข้อเมทริกซ์ (แกน 1 หรือ 2) · กลาง 5 ข้อ (30%) · ง่าย 9 ข้อ (60%) */
function stratifiedExam(exclude){
  const ex=exclude||[], slots=[];
  AKEYS.forEach(k=>{ for(let i=0;i<QUOTA[k];i++) slots.push({k:k,want:'easy'}); });
  const hardAt=shuffle(slots.map((s,i)=>i).filter(i=>slots[i].k==='axis1'||slots[i].k==='axis2'))[0];
  slots[hardAt].want='hard';
  shuffle(slots.map((s,i)=>i).filter(i=>slots[i].want==='easy')).slice(0,5).forEach(i=>{ slots[i].want='mid'; });
  const LVO={easy:0,mid:1,hard:2};
  slots.sort((p,q)=>(AKEYS.indexOf(p.k)-AKEYS.indexOf(q.k))||(LVO[p.want]-LVO[q.want]));
  const used=[], picks=[];
  slots.forEach(sl=>{
    const all=BANK[sl.k].map((q,i)=>({q:q,id:sl.k+'#'+i})).filter(o=>used.indexOf(o.id)<0);
    let pool=all.filter(o=>ex.indexOf(o.id)<0 && o.q.lv===sl.want);
    if(!pool.length) pool=all.filter(o=>ex.indexOf(o.id)<0);
    if(!pool.length) pool=all;
    const o=pick(pool); used.push(o.id);
    picks.push(Object.assign({},randomizeChoices(o.q),{axis:sl.k,qid:o.id}));
  });
  return picks;   /* เรียงตามลำดับหัวข้อในสไลด์ครั้งที่ 4 */
}
''')

# ------------------------------------------------------------------ arcade engine
R("AC.byA=zeroByAxis();", "AC.byA=zeroByAxis(); AC.log=[];")
R("      if(q.axis) AC.byA[q.axis]=1;", "      if(q.axis) AC.byA[q.axis]=(AC.byA[q.axis]||0)+1;")
R("    const head = (ci===-1)", "    AC.log.push({axis:q.axis,k:q.k||'',ok:ci===q.a});\n    const head = (ci===-1)")
R("  const vals=used.map(k=>AC.byA[k]?1:0);",
  "  const cnt=k=>AC.qs.filter(q=>q.axis===k).length||1;\n  const vals=used.map(k=>Math.min(1,(AC.byA[k]||0)/cnt(k)));")
R("'<circle cx=\"'+p[0].toFixed(1)+'\" cy=\"'+p[1].toFixed(1)+'\" r=\"3.6\" fill=\"'+(v?'var(--corner)':'var(--red)')+'\"/>';",
  "'<circle cx=\"'+p[0].toFixed(1)+'\" cy=\"'+p[1].toFixed(1)+'\" r=\"3.6\" fill=\"'+(v>=1?'var(--corner)':'var(--red)')+'\"/>';")
R("s+='<div class=\"legend\">'+used.map((k,i)=>'<div><i style=\"background:'+(AC.byA[k]?'var(--corner)':'var(--red)')+'\"></i>'+\n     (i+1)+'. '+AXIS_BY_KEY[k].ch+' '+AXIS_BY_KEY[k].short+' — <b>'+(AC.byA[k]?'ผ่าน':'ยังไม่ผ่าน')+'</b></div>').join('')+'</div>';",
  "s+='<div class=\"legend\">'+used.map((k,i)=>'<div><i style=\"background:'+((AC.byA[k]||0)>=cnt(k)?'var(--corner)':'var(--red)')+'\"></i>'+\n     (i+1)+'. '+AXIS_BY_KEY[k].short+' — <b>'+(AC.byA[k]||0)+'/'+cnt(k)+'</b></div>').join('')+'</div>';")
R("if(AC.onDone) AC.onDone({correct:AC.correct,byA:AC.byA,time:timeSec,score:AC.score,timeouts:AC.timeouts,avg:avg});",
  "if(AC.onDone) AC.onDone({correct:AC.correct,byA:AC.byA,log:AC.log,time:timeSec,score:AC.score,timeouts:AC.timeouts,avg:avg});")

# ------------------------------------------------------------------ launchers
R("const qs=stratifiedSeven(kind==='post' ? (state.preIds||[]) : []);", "const qs=stratifiedExam(kind==='post' ? (state.preIds||[]) : []);")
R("acStart(kind, qs, (kind==='pre'?'QUALIFYING NIGHT · ก่อนทบทวน':'CHAMPIONSHIP FINAL · หลังทบทวน'), res=>{",
  "acStart(kind, qs, (kind==='pre'?'QUALIFYING · ก่อนทบทวน':'FINAL CORNER · หลังทบทวน'), res=>{")
R("if(kind==='pre'){state.pre=res.correct;state.preByA=res.byA;state.preTime=res.time;state.preTimeouts=res.timeouts;}",
  "if(kind==='pre'){state.pre=res.correct;state.preByA=res.byA;state.preLog=res.log;state.preTime=res.time;state.preTimeouts=res.timeouts;}")
R("else{state.post=res.correct;state.postByA=res.byA;state.postTime=res.time;state.postTimeouts=res.timeouts;}",
  "else{state.post=res.correct;state.postByA=res.byA;state.postLog=res.log;state.postTime=res.time;state.postTimeouts=res.timeouts;}")
R("$('#rvL1').textContent=kind==='pre'?'QUALIFYING COMPLETE':'CHAMPIONSHIP COMPLETE';", "$('#rvL1').textContent=kind==='pre'?'QUALIFYING COMPLETE':'FINAL CORNER COMPLETE';")
R("$('#rvScore').textContent=score+'/7';", "$('#rvScore').textContent=score+'/'+Q_TOTAL;")
R("'นี่คือสภาพรถตั้งต้นของคุณ — ไปเดินพิททบทวนทีละบทแล้วกลับมาวัดใหม่ในรอบชิงแชมป์'", "'นี่คือเส้นฐานของคุณ — ไปเดินพิททบทวนทีละหัวข้อแล้วกลับมาวัดใหม่ในรอบชิงแชมป์'")
R("if(kind==='post'&&info.stars>=6){", "if(kind==='post'&&info.stars>=13){")

# ------------------------------------------------------------------ pit walk
R("el.className='status-line'+(n===7?' ok':'');", "el.className='status-line'+(n===AKEYS.length?' ok':'');")
R("el.innerHTML='ซ้อมไปแล้ว <b>'+n+'/7</b> บท · ทำได้เต็ม 3/3 แล้ว <b>'+full+'</b> บท'+",
  "el.innerHTML='ซ้อมไปแล้ว <b>'+n+'/'+AKEYS.length+'</b> หัวข้อ · ทำได้เต็ม 3/3 แล้ว <b>'+full+'</b> หัวข้อ'+")
R("(n<7?' — บทที่ยังไม่ได้ซ้อมจะถูกจัดไว้ต้นตารางซ้อม 8 วันโดยอัตโนมัติ':' — ครบทุกบทแล้ว ลงรอบชิงแชมป์ได้เลย');",
  "(n<AKEYS.length?' — หัวข้อที่ยังไม่ได้ซ้อมจะถูกจัดไว้ต้นตารางซ้อม 8 วันโดยอัตโนมัติ':' — ครบทุกหัวข้อแล้ว ลงรอบชิงแชมป์ได้เลย');")
R("(res.correct===3?' — แม่นเต็มสิบ บทนี้พร้อมแล้ว':", "(res.correct===3?' — แม่นเต็มสิบ หัวข้อนี้พร้อมแล้ว':")
R("'<span class=\"lap\">รอบ '+ax.lap+'</span>'+", "'<span class=\"lap\">หัวข้อ '+ax.lap+'</span>'+")
R("ax.games.map(g=>'<a class=\"pitlink\" href=\"'+g[0]+'\" target=\"_blank\" rel=\"noopener\">กลับเข้าพิท: '+g[1]+'</a>').join('')+",
  "ax.games.map(g=>'<a class=\"pitlink\" href=\"'+g[0]+'\" target=\"_blank\" rel=\"noopener\">ทวนพื้นฐาน: '+g[1]+'</a>').join('')+")
R("(pr&&pr.runs?('รอบล่าสุด ตอบถูก <b>'+pr.last+'/3</b> ข้อ · ซ้อมไปแล้ว '+pr.runs+' รอบ · สถิติดีที่สุด '+pr.best+'/3')\n                      :'ยังไม่ได้ลงซ้อมบทนี้')+",
  "(pr&&pr.runs?('รอบล่าสุด ตอบถูก <b>'+pr.last+'/3</b> ข้อ · ซ้อมไปแล้ว '+pr.runs+' รอบ · สถิติดีที่สุด '+pr.best+'/3')\n                      :'ยังไม่ได้ลงซ้อมหัวข้อนี้')+")
R("if(practicedCount()===0 && !confirm('ยังไม่ได้ลงซ้อมสักบทเลย ต้องการลงรอบชิงแชมป์เลยหรือไม่')) return;",
  "if(practicedCount()===0 && !confirm('ยังไม่ได้ลงซ้อมสักหัวข้อเลย ต้องการลงรอบชิงแชมป์เลยหรือไม่')) return;")

# ------------------------------------------------------------------ summary logic
R("{id:'perfect',  name:'GRAND SLAM',       desc:'รอบชิงแชมป์ถูกครบ 7 ข้อ',            test:s => s.post === 7},",
  "{id:'perfect',  name:'GRAND SLAM',       desc:'รอบชิงแชมป์ถูกครบ 15 ข้อ',           test:s => s.post === 15},\n"
  "  {id:'pass60',   name:'LICENSE READY',    desc:'รอบชิงแชมป์ได้ 9/15 ขึ้นไป (เกณฑ์ 60%)', test:s => (s.post||0) >= 9},")
R("{id:'recon',    name:'FULL RECON',       desc:'ลงซ้อมครบทั้ง 7 บทในหน้าเดินพิท',    test:",
  "{id:'recon',    name:'FULL RECON',       desc:'ลงซ้อมครบทั้ง 6 หัวข้อในหน้าเดินพิท', test:")
R("/* จัดลำดับบทจากอ่อนสุดไปแข็งสุด", "/* สัดส่วนที่ตอบถูกของแต่ละแกน (0-1) */\nfunction ratio(byA,k){ return Math.min(1,(byA&&byA[k]||0)/QUOTA[k]); }\n/* จัดลำดับหัวข้อจากอ่อนสุดไปแข็งสุด")
R("    const post=(state.post!==null)?(state.postByA[ax.key]||0):0;\n    const pre=(state.pre!==null)?(state.preByA[ax.key]||0):0;",
  "    const post=(state.post!==null)?ratio(state.postByA,ax.key):0;\n    const pre=(state.pre!==null)?ratio(state.preByA,ax.key):0;")
R("      ? 'ทวนรวมทุกบทอย่างเร็ว แล้วปิดท้ายด้วย <b>'+ax.ch+' '+ax.short+'</b> ซึ่งเป็นแกนที่อ่อนที่สุด'\n      : (r.post? 'บทนี้ผ่านในรอบชิงแชมป์แล้ว ใช้เวลาสั้น ๆ ทวนจุดหลอกให้แม่นขึ้น' :\n                 'ยังไม่ผ่านในรอบชิงแชมป์ ควรอ่านสรุปแล้วเล่นเกมประจำบทให้จบอย่างน้อยหนึ่งรอบ');",
  "      ? 'ทวนรวมทุกหัวข้ออย่างเร็ว แล้วปิดท้ายด้วย <b>'+ax.short+'</b> ซึ่งเป็นแกนที่อ่อนที่สุด'\n      : (r.post>=1? 'หัวข้อนี้ถูกครบในรอบชิงแชมป์แล้ว ใช้เวลาสั้น ๆ ทวนจุดหลอกให้แม่นขึ้น' :\n                 'ยังพลาดในรอบชิงแชมป์ ('+Math.round(r.post*100)+'%) อ่านสไลด์ครั้งที่ 4 หัวข้อนี้แล้วซ้อมในหน้าเดินพิทจนได้ 3/3');")
R("'<span class=\"g\">'+ax.games.map(g=>g[1].split(' · ')[0]).join(' · ')+'</span>';",
  "'<span class=\"g\">'+(ax.games.length?ax.games.map(g=>g[1].split(' · ')[0]).join(' · '):'ด่าน 11')+'</span>';")
R("a.innerHTML=(r.post?'':'<b style=\"color:var(--red)\">ต้องจูน</b> ')+r.ax.ch+' → '+g[1];",
  "a.innerHTML=(r.post>=1?'':'<b style=\"color:var(--red)\">ต้องจูน</b> ')+r.ax.short+' → '+g[1];")
R("      '<div class=\"mono\" style=\"font-size:.78rem\">ก่อน '+(pre?'ผ่าน':'ไม่ผ่าน')+' → หลัง '+(post?'ผ่าน':'ไม่ผ่าน')+'</div>'+",
  "      '<div class=\"mono\" style=\"font-size:.78rem\">ก่อน '+pre+'/'+QUOTA[ax.key]+' → หลัง '+post+'/'+QUOTA[ax.key]+'</div>'+")
R("$('#sumPre').textContent=(state.pre===null?'-':state.pre)+'/7';", "$('#sumPre').textContent=(state.pre===null?'-':state.pre)+'/'+Q_TOTAL;")
R("$('#sumPost').textContent=(state.post===null?'-':state.post)+'/7';", "$('#sumPost').textContent=(state.post===null?'-':state.post)+'/'+Q_TOTAL;")
R("msg.textContent=postInfo.stars>=6?", "msg.textContent=postInfo.stars>=13?")
R("'ดาวยังคงที่ที่ '+postInfo.stars+' ดวง — ดูเรดาร์ว่าแกนไหนบุ๋มแล้วทวนเฉพาะบทนั้นก่อน'", "'ดาวยังคงที่ที่ '+postInfo.stars+' ดวง — ดูเรดาร์ว่าแกนไหนบุ๋มแล้วทวนเฉพาะหัวข้อนั้นก่อน'")
R("msg.textContent='รอบนี้ดาวยังไม่ขึ้น ถือเป็นข้อมูลที่มีค่า — ตารางซ้อมด้านล่างจัดลำดับบทที่ควรทวนก่อนไว้ให้แล้ว';",
  "msg.textContent='รอบนี้ดาวยังไม่ขึ้น ถือเป็นข้อมูลที่มีค่า — ดูรายการแนวคิดที่ยังพลาดแล้วทวนตามลำดับในตารางซ้อม';")

# วิเคราะห์รายแนวคิด: ใส่ไว้ต้นแท็บคำแนะนำ
R("  const rank=axisRank(), weak=rank[0].ax, tips=[];\n  tips.push('บทที่ควรทวนก่อนที่สุดคือ <b>'+weak.ch+' '+weak.name+'</b> — กดปุ่มกลับเข้าพิทด้านบนเพื่อเปิดเกมประจำบทนี้ได้ทันที');",
  "  renderConcepts(adv);\n  const rank=axisRank(), weak=rank[0].ax, tips=[];\n"
  "  tips.push('หัวข้อที่ควรทวนก่อนที่สุดคือ <b>'+weak.ch+' '+weak.name+'</b> — กดปุ่มทบทวนด้านล่างเพื่อเปิดจุดหลอกและซ้อม 3 ข้อของหัวข้อนี้ได้ทันที');")
R("  if(notPracticed.length) tips.push('ยังไม่ได้ลงซ้อมอีก <b>'+notPracticed.length+' บท</b> คือ '+\n    notPracticed.map(k=>AXIS_BY_KEY[k].ch).join(', ')+' — การซ้อมรอบละ 3 ข้อใช้เวลาไม่ถึงห้านาทีต่อบท และช่วยให้ตารางซ้อมแม่นขึ้น');",
  "  if(notPracticed.length) tips.push('ยังไม่ได้ลงซ้อมอีก <b>'+notPracticed.length+' หัวข้อ</b> คือ '+\n    notPracticed.map(k=>AXIS_BY_KEY[k].short).join(', ')+' — การซ้อมรอบละ 3 ข้อใช้เวลาไม่ถึงห้านาทีต่อหัวข้อ และช่วยให้ตารางซ้อมแม่นขึ้น');")
R("const avg=(state.postTime&&state.post!==null)?(state.postTime/7):0;", "const avg=(state.postTime&&state.post!==null)?(state.postTime/Q_TOTAL):0;")
R("  if(state.maxCombo<3) tips.push('ยังตอบถูกติดกันไม่ถึง 3 ข้อ ลองซ้อมรอบประจำบทซ้ำจนได้ 3/3 สักสองสามบท จะช่วยยืนยันว่าเข้าใจจริงไม่ใช่เดา');",
  "  if(state.maxCombo<3) tips.push('ยังตอบถูกติดกันไม่ถึง 3 ข้อ ลองซ้อมรายหัวข้อซ้ำจนได้ 3/3 สักสองสามหัวข้อ จะช่วยยืนยันว่าเข้าใจจริงไม่ใช่เดา');")
RX(r"  if\(state\.post===7\) tips\.push\([^\n]*\n",
   "  if(state.post===15) tips.push('ถูกครบทั้ง 15 ข้อแล้ว ขั้นต่อไปคือเล่นซ้ำเพื่อเจอชุดคำถามใหม่และลดเวลาต่อข้อ เพราะในห้องสอบจริงความเร็วมีค่าเท่ากับความแม่น');\n"
   "  else if((state.post||0)>=9) tips.push('ผ่านเกณฑ์ 60% แล้ว ('+state.post+'/15) — เก็บแนวคิดที่ยังพลาดให้ครบจะช่วยเผื่อคะแนนไว้ชดเชยวิชาอื่นในการสอบ กว.');\n"
   "  else tips.push('ยังไม่ถึงเกณฑ์ 60% (ต้องได้ 9/15) — เริ่มจากแนวคิดที่ยังพลาดด้านบน ทวนสไลด์ครั้งที่ 4 แล้วกลับมาวัดใหม่');\n")
R("$('#btnReview').textContent='ทบทวน: '+weak.ch+' '+weak.short;", "$('#btnReview').textContent='ทบทวน: '+weak.short;")

CONCEPTS_JS = r'''
/* ---- วิเคราะห์รายแนวคิด: ยังขาดความเข้าใจเรื่องใด และเรื่องใดเป็นจุดเด่น ----
   ใช้ผลรอบชิงแชมป์เป็นหลัก (ถ้ายังไม่มีใช้รอบคัดเลือก) แต่ละข้อมีแนวคิด k กำกับ */
function conceptStats(){
  const log=(state.post!==null&&state.postLog&&state.postLog.length)?state.postLog:(state.preLog||[]);
  const miss={}, hit={};
  log.forEach(r=>{ const key=r.axis+'|'+r.k; (r.ok?hit:miss)[key]=(r.ok?hit:miss)[key]||{axis:r.axis,k:r.k,n:0}; (r.ok?hit:miss)[key].n++; });
  Object.keys(miss).forEach(key=>{ delete hit[key]; });
  return {miss:Object.values(miss), hit:Object.values(hit), n:log.length};
}
function renderConcepts(host){
  const st=conceptStats(); if(!st.n) return;
  const strong=AXES.filter(ax=>ratio(state.postByA,ax.key)>=1).map(ax=>ax.short);
  const weakAx=AXES.filter(ax=>ratio(state.postByA,ax.key)<=0.5);
  const order=k=>AKEYS.indexOf(k);
  const miss=st.miss.slice().sort((a,b)=>order(a.axis)-order(b.axis));
  let h='<li class="head">ยังขาดความเข้าใจเรื่องต่อไปนี้ ('+miss.length+' แนวคิด)</li>';
  h+=miss.length?miss.map(m=>'<li class="miss">'+m.k+'<small>'+AXIS_BY_KEY[m.axis].ch+' · '+AXIS_BY_KEY[m.axis].short+(m.n>1?' · พลาด '+m.n+' ข้อ':'')+'</small></li>').join('')
                :'<li class="hit">ไม่มีแนวคิดที่พลาดในรอบล่าสุด ยอดเยี่ยมมาก</li>';
  if(weakAx.length) h+='<li>หัวข้อที่ได้ไม่เกิน 50% คือ <b>'+weakAx.map(a=>a.short).join(', ')+'</b> — ทวนสไลด์ครั้งที่ 4 หัวข้อนี้ก่อน แล้วซ้อมในหน้าเดินพิทจนได้ 3/3</li>';
  h+='<li class="head">จุดเด่นของคุณ</li>';
  h+=strong.length?'<li class="hit">ตอบถูกครบทุกข้อในหัวข้อ <b>'+strong.join(', ')+'</b></li>':'<li>ยังไม่มีหัวข้อที่ถูกครบทุกข้อ ใกล้ที่สุดดูได้จากเรดาร์</li>';
  h+=st.hit.sort((a,b)=>order(a.axis)-order(b.axis)).slice(0,6).map(m=>'<li class="hit">'+m.k+'<small>'+AXIS_BY_KEY[m.axis].short+'</small></li>').join('');
  h+='<li class="head">ข้อเสนอแนะ</li>';
  host.insertAdjacentHTML('beforeend',h);
}
/* ---- CSV export (สำหรับอาจารย์เก็บคะแนน) ---- */'''
R("/* ---- CSV export (สำหรับอาจารย์เก็บคะแนน) ---- */", CONCEPTS_JS)
R("  head.push('pre_time_s','post_time_s','pre_timeouts','post_timeouts','xp','max_combo','timestamp');",
  "  head.push('pre_time_s','post_time_s','pre_timeouts','post_timeouts','xp','max_combo','missed_concepts','timestamp');")
R("  row.push(state.preTime||0,state.postTime||0,state.preTimeouts||0,state.postTimeouts||0,state.xp,state.maxCombo,new Date().toISOString());",
  "  row.push(state.preTime||0,state.postTime||0,state.preTimeouts||0,state.postTimeouts||0,state.xp,state.maxCombo,\n"
  "    conceptStats().miss.map(m=>m.k).join(' ; '),new Date().toISOString());")
R("a.download='GNR1007_D3_final_'+", "a.download='GNR1007_D4_finalcorner_'+")
R("  const labels=AXES.map(a=>a.ch);   /* ป้ายแกนใช้ชื่อบทสั้น ๆ เพื่อไม่ให้ตัวหนังสือล้นขอบบนจอมือถือ */\n  const preData=AKEYS.map(k=>(state.preByA[k]?100:0));\n  const postData=AKEYS.map(k=>(state.postByA[k]?100:0));",
  "  const labels=AXES.map(a=>a.short);   /* ป้ายแกนใช้ชื่อหัวข้อสั้น ๆ เพื่อไม่ให้ตัวหนังสือล้นขอบบนจอมือถือ */\n  const preData=AKEYS.map(k=>Math.round(ratio(state.preByA,k)*100));\n  const postData=AKEYS.map(k=>Math.round(ratio(state.postByA,k)*100));")

R('    const r=isLast?rank[0]:rank[i];', '    const r=isLast?rank[0]:(i<rank.length?rank[i]:rank[Math.min(rank.length-1,i-rank.length+1)]);   /* 8 วัน แต่มี 6 หัวข้อ: วันที่ 7 ทวนหัวข้อที่อ่อนอันดับสองซ้ำ */')
R('return {ax:ax, post:post, pre:pre, pr:pr, score: post*2 + prScore};', 'return {ax:ax, post:post, pre:pre, pr:pr, score: post*10 + prScore};   /* ผลสอบจริงมาก่อน ผลซ้อมใช้ตัดสินเมื่อเท่ากัน */')
R("    const lab=isTop?ACT.topWord:(i===0?ACT.groundWord:ACT.floorWord+' '+i);",
  "    const lab=isTop?ACT.topWord:(i===0?ACT.groundWord:ACT.floorWord+' '+i);\n"
  "    const showLab=isTop||i===0||n<=10||isNext||(i%3===0&&i<n-1);   /* 15 ขั้น: แสดงป้ายทุก 3 ขั้น กันตัวหนังสือซ้อน */")
R("    ctx.fillText(lab,lx,below?(g.y+g.h+15):(g.y-6));", "    if(showLab) ctx.fillText(lab,lx,below?(g.y+g.h+15):(g.y-6));")
R("  ctx.fillText(AC.W<150?(AC.floor+'/'+n):('วิ่งครบ '+AC.floor+' / '+n+' รอบ'),AC.W-12,AC.H-11);",
  "  if(AC.W>=150) ctx.fillText('วิ่งครบ '+AC.floor+' / '+n+' รอบ',AC.W-12,AC.H-11);   /* รางแคบบนมือถือ: ตัวนับอยู่ในแถบสถานะแล้ว */")
# ตรวจว่าไม่เหลือเลข 7 ที่ผูกกับเกมเดิม
left = [m.group(0) for m in re.finditer(r"[^\n]*(/7'|'/7|เจ็ด|stratifiedSeven|CHAMPIONSHIP FINAL)[^\n]*", s)]
assert not left, left
out = os.path.join(D, 'game11_final_corner.html')
open(out, 'w', encoding='utf-8').write(s)
print('wrote', out, len(s), 'bytes; bank', {k: len(v) for k, v in bank.items()})
