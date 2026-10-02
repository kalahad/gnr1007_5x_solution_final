#!/usr/bin/env python3
"""ติดตั้ง GNR-CORE v7.0 ลงในไฟล์เกมทุกไฟล์ (game1-game11) (รันซ้ำได้ ไม่ซ้อนทับ)
usage: python3 apply_core.py <games_dir>
- แทนพื้นหลังสีเข้มแบบฝังตายใน <style> ด้วย var(--ink-panel-rgb) เพื่อให้โหมดสว่างอ่านง่าย
- คำนวณสีเน้น (accent) ใหม่ให้ความต่างสี (contrast) >= 4.6:1 ทั้งโหมดมืดและสว่าง
- แทรก gnr_core.css / gnr_core.js ไว้ท้ายไฟล์ ระหว่างเครื่องหมาย GNR-CORE
"""
import re, sys, os, colorsys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'gnr_core.css'), encoding='utf-8').read()
JS = open(os.path.join(HERE, 'gnr_core.js'), encoding='utf-8').read()
M1, M2 = '<!-- GNR-CORE:BEGIN -->', '<!-- GNR-CORE:END -->'

def hex2rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def lum(rgb):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

def adjust(hexc, bg, target, darker):
    rgb = hex2rgb(hexc)
    h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in rgb])
    for _ in range(100):
        cur = tuple(round(v * 255) for v in colorsys.hls_to_rgb(h, l, s))
        if contrast(cur, bg) >= target: break
        l = max(0, l - 0.01) if darker else min(1, l + 0.01)
    return '#%02x%02x%02x' % cur

SKIP = {'bg', 'text', 'muted', 'bg-grad-mid'}
def tokens(block):
    return {k: v for k, v in re.findall(r'--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})', block) if k not in SKIP}

def process(path):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(M1) + r'.*?' + re.escape(M2) + r'\n?', '', s, flags=re.S)
    game = os.path.basename(path).split('_')[0]
    title = re.search(r'<title>(.*?)</title>', s).group(1).split(':')[0].split('|')[0].strip()
    m = re.search(r'offsetHeight\)\|\|28\)\+(\d+)\)', s)
    pad_extra = int(m.group(1)) if m else 16

    # 1) พื้นหลังเข้มแบบฝังตายใน <style> -> ตัวแปรตามธีม
    def fix_style(mm):
        css = mm.group(0)
        def rep(x):
            r, g, b = int(x.group(1)), int(x.group(2)), int(x.group(3))
            if (r, g, b) == (0, 0, 0) or max(r, g, b) >= 45: return x.group(0)
            return 'rgba(var(--ink-panel-rgb),' + x.group(4) + ')'
        return re.sub(r'rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)', rep, css)
    s = re.sub(r'<style>.*?</style>', fix_style, s, count=1, flags=re.S)

    # 2) canvas: ขั้นที่ยังไปไม่ถึงต้องมองเห็นในโหมดสว่าง + ข้อความท้ายรางแคบ
    s = s.replace("(reached?c.ember:'rgba(255,255,255,.10)')",
                  "(reached?c.ember:(document.documentElement.getAttribute('data-theme')==='light'?'rgba(16,24,38,.20)':'rgba(255,255,255,.16)'))")
    s = re.sub(r"ctx\.fillText\(((?:(?!ctx\.).)*?),AC\.W-12,AC\.H-11\);",
               lambda x: x.group(0) if 'AC.W<150' in x.group(1) else
               "ctx.fillText(AC.W<150?(AC.floor+'/'+n):(" + x.group(1) + "),AC.W-12,AC.H-11);", s)

    # 3) ข้อความที่ล้าสมัย (วันสอบกลางภาคผ่านไปแล้ว)
    s = s.replace('ตารางซ้อม 8 วัน ถึงวันสอบ 13 กันยายน 2569', 'ตารางซ้อม 8 วันก่อนสอบ')
    s = re.sub(r"const PLAN_DAYS = \[\n.*?\n\];",
               "const PLAN_DAYS = (function(){ /* UI v7.0: นับ 8 วันจากวันที่เปิดดู แทนวันที่ตายตัวของสอบกลางภาค */\n"
               "  const wd=['อาทิตย์','จันทร์','อังคาร','พุธ','พฤหัสบดี','ศุกร์','เสาร์'],mo=['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];\n"
               "  const t=new Date(), out=[];\n"
               "  for(let i=0;i<8;i++){ const d=new Date(t.getFullYear(),t.getMonth(),t.getDate()+i); out.push([d.getDate()+' '+mo[d.getMonth()],(i===0?'วันนี้ · ':'')+wd[d.getDay()]]); }\n"
               "  return out; })();", s, count=1, flags=re.S)
    s = s.replace('<span class="d">13 ก.ย.<br><small>อาทิตย์</small></span>', '<span class="d">วันสอบ<br><small>ตามตารางสอบ</small></span>')
    s = s.replace('<b>สอบกลางภาค 13.30-16.00 น.</b><small>คุมบทที่ 1-7a และบทที่ 10 · ', '<b>วันสอบจริง</b><small>ทบทวนทุกบทที่เรียน · ')

    # 4) สีเน้นใหม่ตามธีม
    dark_block = re.search(r':root\{(.*?)\}', s, re.S).group(1)
    light_block = re.search(r':root\[data-theme="light"\]\{(.*?)\}', s, re.S).group(1)
    panel_rgb = re.search(r'--panel2-rgb\s*:\s*(\d+),\s*(\d+),\s*(\d+)', dark_block)
    dark_bg = tuple(int(v) for v in panel_rgb.groups()) if panel_rgb else (16, 26, 48)
    dt, lt = tokens(dark_block), tokens(light_block)
    for k, v in dt.items():
        lt.setdefault(k, v)   # alias ที่ไม่มีค่าโหมดสว่าง -> ใช้ค่ามืดแล้วปรับให้เข้มขึ้น
    dark_vars = ';'.join('--%s:%s' % (k, adjust(v, dark_bg, 5.0, False)) for k, v in dt.items())
    light_vars = ';'.join('--%s:%s' % (k, adjust(v, (244, 247, 251), 5.2, True)) for k, v in lt.items())
    # เส้นขอบในโหมดสว่างใช้สี ember ที่เข้มขึ้น
    em_l = adjust(lt.get('ember', '#0087cc'), (244, 247, 251), 4.8, True)
    r, g, b = hex2rgb(em_l)
    light_vars += ';--line:rgba(%d,%d,%d,.26);--ember-dim:rgba(%d,%d,%d,.16)' % (r, g, b, r, g, b)
    theme_css = ':root:not([data-theme="light"]){%s}\n:root[data-theme="light"]{%s}\n' % (dark_vars, light_vars)

    block = (M1 + '\n<style id="gnr-core-css">\n' + theme_css + CSS + '</style>\n' +
             '<script>window.GNR_CFG={game:%r,title:%r,padExtra:%d};</script>\n' % (game, title, pad_extra) +
             '<script id="gnr-core-js">\n' + JS + '</script>\n' + M2 + '\n')
    s = s.replace('</body>', block + '</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    print('%-30s title=%-20s pad=%d  dark[%s]  light[%s]' % (os.path.basename(path), title, pad_extra, dark_vars, light_vars.split(';--line')[0]))

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '.'
    for f in sorted(os.listdir(d)):
        if re.match(r'game\d+_.*\.html$', f): process(os.path.join(d, f))
