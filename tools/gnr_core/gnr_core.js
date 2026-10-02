/* ================================================================
   GNR-CORE v7.0 — สคริปต์ร่วมของทุกเกม (โหลดหลังสคริปต์หลักของเกม)
   ใช้ตัวแปรระดับโกลบอลของเกม: state, AC, ACT, acColors, acResize, acStepGeom,
   showSummary, radarData, radarChart, goto_, exportCSV, MAX_STARS
   ================================================================ */
(function(){
  'use strict';
  var CFG = window.GNR_CFG || {game:'game', title:'GNR1007', padExtra:16};
  var ID_KEY = 'gnr1007_student', RES_KEY = 'gnr1007_results', SECRET = 'ru2569', MASK = 'xxxxxxxxxx';
  function $(s){ return document.querySelector(s); }
  function el(tag, cls, html){ var e=document.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e; }
  function escH(s){ return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function css(n){ return (getComputedStyle(document.documentElement).getPropertyValue(n)||'').trim(); }
  function isLight(){ return document.documentElement.getAttribute('data-theme')==='light'; }
  function rgba(hex,a){
    var h=(hex||'').replace('#','');
    if(h.length===3) h=h.split('').map(function(c){return c+c;}).join('');
    if(!/^[0-9a-f]{6}$/i.test(h)) return hex;
    var n=parseInt(h,16); return 'rgba('+(n>>16&255)+','+(n>>8&255)+','+(n&255)+','+a+')';
  }

  /* ---------------- ตัวตนผู้เรียน ---------------- */
  function checkId(raw){
    var v=(raw||'').trim();
    if(v.toLowerCase()===SECRET) return {ok:true, sid:MASK, via:'code'};
    var d=v.replace(/[\s-]/g,'');
    if(!d) return {ok:false, msg:'กรุณากรอกรหัสนักศึกษา 10 หลัก'};
    if(/^\d+$/.test(d)){
      if(d.length!==10) return {ok:false, msg:'รหัสนักศึกษาต้องมี 10 หลัก (ตอนนี้ '+d.length+' หลัก)'};
      if(!/^[5-7]\d{9}$/.test(d)) return {ok:false, msg:'รหัสนักศึกษาต้องขึ้นต้นด้วยปีที่เข้าศึกษา เช่น 69xxxxxxxx'};
      return {ok:true, sid:d, via:'id'};
    }
    return {ok:false, msg:'กรอกได้เฉพาะตัวเลข 10 หลัก หรือรหัสลับที่ได้รับจากผู้สอน'};
  }
  function getId(){ try{ var o=JSON.parse(sessionStorage.getItem(ID_KEY)||'null'); return (o&&o.sid)?o:null; }catch(e){ return null; } }
  function setId(o){ try{ sessionStorage.setItem(ID_KEY, JSON.stringify(o)); }catch(e){} }
  window.GNRID = {check:checkId, get:getId, set:function(raw,nick){ var r=checkId(raw); if(r.ok) setId({sid:r.sid,via:r.via,raw:raw,nick:nick||''}); return r; }};

  function setupLogin(){
    var nameIn=$('#playerName'); if(!nameIn) return;
    var nameLbl=document.querySelector('label[for="playerName"]');
    var host=nameLbl||nameIn;
    var box=el('div','gnr-idbox',
      '<label for="gnrSid">รหัสนักศึกษา <span class="gnr-count" id="gnrCount">0/10</span></label>'+
      '<input type="text" id="gnrSid" maxlength="12" autocomplete="off" spellcheck="false" placeholder="เช่น 69xxxxxxxx">'+
      '<div class="gnr-hint">กรอก <b>รหัสนักศึกษา 10 หลัก</b> เป็นตัวเลขล้วน ขึ้นต้นด้วยปีที่เข้าศึกษา ตัวอย่าง <b>69</b>xxxxxxxx (รหัสปี 2569)</div>'+
      '<div class="err" id="gnrSidErr"></div><div class="gnr-idnote" id="gnrIdNote"></div>');
    box.style.marginBottom='14px';
    host.parentNode.insertBefore(box, host);
    if(nameLbl) nameLbl.textContent='ชื่อเล่น (แสดงบนใบรายงานผล)';
    nameIn.placeholder='เช่น ต้นกล้า';
    var sid=$('#gnrSid'), cnt=$('#gnrCount'), err=$('#gnrSidErr'), note=$('#gnrIdNote');
    function live(){
      var v=sid.value.trim(), d=v.replace(/[\s-]/g,'');
      err.classList.remove('show');
      if(v.toLowerCase()===SECRET){ cnt.textContent='รหัสลับ'; cnt.className='gnr-count ok'; note.textContent='ใช้รหัสลับ · ใบรายงานผลจะแสดงรหัสเป็น '+MASK; return; }
      cnt.textContent=(/^\d*$/.test(d)?d.length:'-')+'/10';
      var r=checkId(v); cnt.className='gnr-count'+(r.ok?' ok':'');
      note.textContent=r.ok?'รูปแบบรหัสนักศึกษาถูกต้อง':'';
    }
    sid.addEventListener('input', live);
    sid.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); nameIn.focus(); } });
    var cur=getId();
    if(cur){ sid.value=cur.raw||(cur.via==='id'?cur.sid:''); if(cur.nick && !nameIn.value) nameIn.value=cur.nick; live(); }
    /* ตรวจก่อนเริ่มเกม (จับใน capture phase เพื่อให้ทำงานก่อนตัวจัดการเดิมของเกม) */
    document.addEventListener('click', function(e){
      var b=e.target.closest && e.target.closest('#btnStart,#wResume'); if(!b) return;
      var r=checkId(sid.value);
      if(!r.ok){
        e.stopPropagation(); e.preventDefault();
        err.textContent=r.msg; err.classList.remove('show'); void err.offsetWidth; err.classList.add('show');
        sid.focus(); return;
      }
      var nick=nameIn.value.trim();
      if(!nick){ var prev=getId(); nick=(prev&&prev.nick)||''; }
      setId({sid:r.sid, via:r.via, raw:sid.value.trim(), nick:nick});
    }, true);
  }

  /* ---------------- ปุ่มกลับหน้ารวม + สลับธีมบนหน้าแรกของเกม ---------------- */
  var ICON_THEME='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.9" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor"/></svg>';
  var ICON_HOME='<svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 11 12 4l8.5 7"/><path d="M6 9.5V20h12V9.5"/></svg>';
  function toggleTheme(){
    var t=isLight()?'dark':'light';
    document.documentElement.setAttribute('data-theme',t);
    try{ localStorage.setItem('gnr1007_theme',t); }catch(e){}
    setTimeout(onTheme,30);
  }
  function setupChrome(){
    var bt=$('#btnTheme'); if(bt){ bt.innerHTML=ICON_THEME; }
    var right=document.querySelector('.tb-right');
    if(right && !$('#btnHome')){
      var h=el('a','icon-btn',ICON_HOME); h.id='btnHome'; h.href='index.html'; h.title='กลับหน้ารวมเกม'; h.setAttribute('aria-label','กลับหน้ารวมเกม');
      h.style.textDecoration='none'; right.insertBefore(h,right.firstChild);
    }
    var wel=$('#scr-welcome');
    if(wel && !$('#gnrWelBar')){
      var bar=el('div','', '<a class="icon-btn" href="index.html" title="กลับหน้ารวมเกม" aria-label="กลับหน้ารวมเกม" style="text-decoration:none">'+ICON_HOME+'</a>'+
        '<button class="icon-btn" type="button" id="gnrWelTheme" title="สลับโหมดสว่าง/มืด" aria-label="สลับโหมดสว่างหรือมืด">'+ICON_THEME+'</button>');
      bar.id='gnrWelBar'; bar.style.cssText='position:absolute;top:14px;right:14px;display:flex;gap:8px;z-index:5';
      wel.style.position='relative'; wel.appendChild(bar);
      $('#gnrWelTheme').addEventListener('click',toggleTheme);
    }
  }

  /* ---------------- ARCADE: แถบสถานะด้านซ้าย ---------------- */
  function setupArcade(){
    var cv=$('#acv'); if(!cv || cv.parentNode.classList.contains('gnr-cvwrap')) return;
    var w=el('div','gnr-cvwrap'); cv.parentNode.insertBefore(w,cv); w.appendChild(cv);
    var exit=$('#acExit'); if(exit){ exit.textContent='ออก (ESC)'; }
    if(typeof acResize==='function'){
      acResize=function(){
        var c=$('#acv'); if(!c) return;
        var dpr=Math.min(2,window.devicePixelRatio||1);
        AC.W=c.clientWidth||120; AC.H=c.clientHeight||300;
        AC.padT=(CFG.padExtra||16)+14;
        c.width=Math.max(1,AC.W*dpr); c.height=Math.max(1,AC.H*dpr);
        var ctx=c.getContext('2d'); if(ctx&&ctx.setTransform) ctx.setTransform(dpr,0,0,dpr,0,0);
        shortWords(ctx);
      };
    }
    if(typeof acStepGeom==='function'){
      acStepGeom=function(i){
        var n=AC.qs.length||1, padB=30, padT=AC.padT||36, W=AC.W;
        var h=Math.max(60,AC.H-padB-padT), y=AC.H-padB-(i*(h/n));
        if(W<200){ /* รางแคบ: ขั้นบันไดสลับซ้าย-ขวา ไต่ขึ้นแนวตั้ง */
          var ww=Math.max(30,Math.min(96,W*0.5)), room=Math.max(0,W-ww-12);
          return {x:6+((i%2)?room:0), y:y, w:ww, h:9};
        }
        var w2=Math.max(56,Math.min(118,W*0.30)), usable=Math.max(20,W-w2-24);
        return {x:12+(n<=1?0:(i/n)*usable), y:y, w:w2, h:9};
      };
    }
  }
  function shortWords(ctx){
    if(typeof ACT==='undefined') return;
    if(!ACT._o) ACT._o={top:ACT.topWord, ground:ACT.groundWord};
    var room=AC.W-12;
    try{ ctx.font='11px Kanit,sans-serif'; }catch(e){}
    function fit(s,alt){ try{ return ctx.measureText(s).width<=room?s:alt; }catch(e){ return s; } }
    ACT.topWord=fit(ACT._o.top,'ยอด');
    ACT.groundWord=fit(ACT._o.ground,'เริ่ม');
  }

  /* ---------------- ข้อความใน SVG (ภาพประกอบบทเรียน) ให้อ่านได้ในโหมดสว่าง ----------------
     ภาพประกอบเดิมออกแบบบนพื้นมืด จึงใช้สีข้อความสว่างแบบฝังตาย เมื่ออยู่บนพื้นขาวจะจางมาก
     วิธีแก้: หาสีพื้นใต้ข้อความจริง (รูปทรงที่วาดก่อนและครอบข้อความอยู่) แล้วเข้มสีเฉพาะที่ความต่างสีต่ำ */
  var _cvs=document.createElement('canvas').getContext('2d');
  function toRGB(c){
    if(!c||c==='none'||c==='transparent') return null;
    try{ _cvs.fillStyle='#000'; _cvs.fillStyle=c; c=_cvs.fillStyle; }catch(e){ return null; }
    var m=/^#([0-9a-f]{6})$/i.exec(c);
    if(m){ var n=parseInt(m[1],16); return [n>>16&255,n>>8&255,n&255,1]; }
    m=/rgba?\(([^)]+)\)/.exec(c); if(!m) return null;
    var p=m[1].split(',').map(parseFloat); return [p[0],p[1],p[2],p.length>3?p[3]:1];
  }
  function L(c){ function f(v){ v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4);} return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); }
  function CR(a,b){ var x=L(a),y=L(b); return (Math.max(x,y)+0.05)/(Math.min(x,y)+0.05); }
  function mix(top,bot,a){ return [top[0]*a+bot[0]*(1-a),top[1]*a+bot[1]*(1-a),top[2]*a+bot[2]*(1-a),1]; }
  function darkenTo(c,bg,target){
    var r=c.slice(); for(var i=0;i<40 && CR(r,bg)<target;i++){ r=[r[0]*0.88,r[1]*0.88,r[2]*0.88,1]; } return 'rgb('+r.slice(0,3).map(Math.round).join(',')+')';
  }
  function fixSvgText(root){
    var light=isLight(), page=[250,251,253,1];
    Array.prototype.forEach.call((root||document).querySelectorAll('svg text'),function(t){
      if(t.closest('#arcade')||t.closest('.chartbox')) return;
      if(t.hasAttribute('data-ofill')){ t.style.fill=''; }
      if(!light) return;
      var cs=getComputedStyle(t), fg=toRGB(cs.fill); if(!fg) return;
      var svg=t.ownerSVGElement; if(!svg) return;
      var bb; try{ bb=t.getBBox(); }catch(e){ return; } if(!bb.width) return;
      var cx=bb.x+bb.width/2, cy=bb.y+bb.height/2, bg=page;
      var shapes=svg.querySelectorAll('rect,circle,ellipse,path,polygon');
      for(var i=0;i<shapes.length;i++){
        var s=shapes[i];
        if(!(s.compareDocumentPosition(t)&Node.DOCUMENT_POSITION_FOLLOWING)) continue;
        var sb; try{ sb=s.getBBox(); }catch(e){ continue; }
        if(cx<sb.x||cx>sb.x+sb.width||cy<sb.y||cy>sb.y+sb.height) continue;
        var sc=getComputedStyle(s), f=toRGB(sc.fill); if(!f||f[3]===0) continue;
        var a=f[3]*(parseFloat(sc.fillOpacity)||1)*(parseFloat(sc.opacity)||1);
        if(sb.width*sb.height<60) continue;
        bg=mix(f,bg,Math.min(1,a));
      }
      if(CR(fg,bg)>=3.2) return;
      if(L(bg)>0.4){ t.setAttribute('data-ofill','1'); t.style.fill=darkenTo(fg,bg,4.5); }
    });
  }
  var svgT=null; function queueSvgFix(){ clearTimeout(svgT); svgT=setTimeout(function(){ try{ fixSvgText(); }catch(e){} },60); }

  /* ---------------- สีกราฟตามธีม ---------------- */
  function wrapLabel(s){
    s=String(s); if(s.length<=12) return s;
    var words=[];
    try{ var seg=new Intl.Segmenter('th',{granularity:'word'}); for(var it of seg.segment(s)) words.push(it.segment); }
    catch(e){ words=s.split(/(\s+)/); }
    var lines=[''], lim=Math.max(10,Math.ceil(s.length/2)+1);
    words.forEach(function(w){ var cur=lines[lines.length-1]; if(cur && (cur+w).trim().length>lim){ lines.push(w.trim()); } else { lines[lines.length-1]=cur+w; } });
    return lines.map(function(x){return x.trim();}).filter(Boolean);
  }
  function styleChart(){
    var tx=css('--text')||'#e6edf6', mu=css('--muted')||'#8ca0b8', em=css('--ember')||'#22d3ee', gd=css('--gold')||'#fbbf24';
    var grid=isLight()?'rgba(16,24,38,.16)':'rgba(255,255,255,.16)';
    try{
      if(typeof radarChart!=='undefined' && radarChart && typeof Chart!=='undefined'){
        /* สร้างกราฟใหม่ทั้งตัวด้วยสีตามธีม (ไม่แก้ options เดิมผ่าน proxy ของ Chart.js) */
        var cv=radarChart.canvas, d=radarData(), old=radarChart.data.datasets;
        var labels=d.labels.map(wrapLabel);
        var l0=(old[0]&&old[0].label)||'Pretest', l1=(old[1]&&old[1].label)||'Posttest';
        var pc=(CFG.game==='game10')?gd:em;
        radarChart.destroy();
        radarChart=new Chart(cv,{type:'radar',
          data:{labels:labels,datasets:[
            {label:l0,data:d.preData,borderColor:mu,backgroundColor:rgba(mu,.12),pointBackgroundColor:mu,borderDash:[5,4],borderWidth:2},
            {label:l1,data:d.postData,borderColor:pc,backgroundColor:rgba(pc,.22),pointBackgroundColor:pc,borderWidth:2.5}]},
          options:{responsive:true,maintainAspectRatio:false,animation:{duration:500},
            layout:{padding:{left:16,right:16,top:2,bottom:0}},
            plugins:{legend:{position:'bottom',labels:{color:tx,font:{family:'Kanit',size:12},boxWidth:14}}},
            scales:{r:{min:0,max:100,ticks:{display:true,stepSize:50,backdropColor:'rgba(0,0,0,0)',color:mu,font:{size:9}},
              grid:{color:grid},angleLines:{color:grid},pointLabels:{color:tx,font:{family:'Kanit',size:11}}}}}});
      }
    }catch(e){ console.warn('gnr chart',e); }
    var fb=$('#radarFallback'); if(fb) Array.prototype.forEach.call(fb.querySelectorAll('text'),function(t){ if(!/Posttest|หลัง/.test(t.textContent)) t.setAttribute('fill',tx); });
  }
  function onTheme(){
    try{ if(typeof AC!=='undefined' && AC.on && typeof acColors==='function') AC.col=acColors(); }catch(e){}
    styleChart(); queueSvgFix();
  }

  /* ---------------- หน้าสรุปผลแบบแดชบอร์ด ---------------- */
  function maxQ(){ try{ return (typeof MAX_STARS!=='undefined')?MAX_STARS:6; }catch(e){ return 6; } }
  function pct(a,b){ return b?Math.round(a/b*100):0; }
  function axes(){
    try{
      var d=radarData(), out=[];
      d.labels.forEach(function(l,i){ if(/ภาพรวม/.test(l)) return; out.push({label:l, pre:d.preData[i]||0, post:d.postData[i]||0}); });
      return out;
    }catch(e){ return []; }
  }
  function cheer(nick, pre, post, max, weakName){
    var p=pct(post,max), d=post-pre, lvl, big, body;
    if(p>=100){ lvl='ความพร้อมสอบ: พร้อมมาก'; big='ยอดเยี่ยม '+nick+' — ถูกครบทุกข้อ';
      body='คุณเข้าใจหัวข้อนี้ครบถ้วนแล้ว ความแม่นยำระดับนี้คือสิ่งที่ข้อสอบ กว ด้านการเขียนโปรแกรมต้องการ ลองเล่นซ้ำเพื่อเจอชุดคำถามใหม่ หรืออธิบายให้เพื่อนฟัง เพราะการสอนผู้อื่นคือการทบทวนที่ดีที่สุด'; }
    else if(p>=67){ lvl='ความพร้อมสอบ: พร้อม'; big='ดีมาก '+nick+' — อีกนิดเดียวก็เต็ม';
      body='พื้นฐานของคุณแน่นแล้ว เหลือเพียง <b>'+escH(weakName)+'</b> ที่ต้องเก็บให้ครบ ทบทวนอีกเพียงรอบเดียวก็พร้อมเข้าห้องสอบอย่างมั่นใจ'; }
    else if(p>=34){ lvl='ความพร้อมสอบ: กำลังพัฒนา'; big='กำลังมาถูกทาง '+nick;
      body='คุณจับแก่นของหัวข้อนี้ได้แล้วบางส่วน เริ่มจาก <b>'+escH(weakName)+'</b> ก่อน อ่านเฉลยทีละข้อแล้วลองใหม่ ทุกรอบที่เล่นซ้ำคือคะแนนที่เพิ่มขึ้นในห้องสอบจริง'; }
    else { lvl='ความพร้อมสอบ: เริ่มต้น'; big='ทุกคนเริ่มจากจุดนี้ '+nick;
      body='คะแนนรอบนี้คือแผนที่บอกว่าควรเริ่มตรงไหน ไม่ใช่ตัวตัดสินความสามารถ กลับไปที่ <b>'+escH(weakName)+'</b> ทำห้องทดลองให้ครบ แล้วกลับมาทดสอบอีกครั้ง ความเข้าใจเกิดจากการลงมือซ้ำ'; }
    var add = d>0 ? ' · พัฒนาขึ้น <b>+'+d+' ข้อ</b> จากก่อนเรียน แสดงว่าการเรียนรอบนี้ได้ผลจริง'
            : d===0 ? (p>=67?' · รักษามาตรฐานได้คงที่ทั้งก่อนและหลังเรียน':' · คะแนนยังคงที่ ลองเปลี่ยนวิธีทบทวนด้วยการทำห้องทดลองซ้ำ')
            : ' · คะแนนลดลงเล็กน้อยเป็นเรื่องปกติเมื่อเจอคำถามชุดใหม่ อย่าเพิ่งท้อ';
    return '<span class="lvl">'+lvl+'</span><p class="big">'+escH(big)+'</p><p>'+body+add+'</p>';
  }
  function saveResult(id, pre, post, max){
    try{
      var all=JSON.parse(localStorage.getItem(RES_KEY)||'{}'); var k=id.sid||MASK;
      all[k]=all[k]||{}; var old=all[k][CFG.game]||{};
      all[k][CFG.game]={pre:pre, post:post, max:max, best:Math.max(post, old.best||0), nick:id.nick||'', at:new Date().toISOString(), plays:(old.plays||0)+1};
      localStorage.setItem(RES_KEY, JSON.stringify(all));
    }catch(e){}
  }
  var built=false;
  function buildDash(){
    var sec=$('#scr-summary'); if(!sec) return null;
    var panel=sec.querySelector('.panel'); if(!panel) return null;
    if(built) return panel;
    built=true;
    var tag=panel.querySelector('.tag'), h2=panel.querySelector('h2');
    var head=el('div','gnr-head'); if(tag) head.appendChild(tag); if(h2) head.appendChild(h2);
    head.appendChild(el('span','gnr-when','')); panel.insertBefore(head, panel.firstChild);
    var dash=el('div','gnr-dash');
    var a=el('div','gnr-col a'), b=el('div','gnr-col b'), c=el('div','gnr-col c');
    /* คอลัมน์ A: ตัวตน + ก่อน/หลังเรียน */
    var idb=el('div','gnr-box gnr-id','<div class="ava" id="gnrAva"></div><div><div class="nick" id="gnrNick">—</div><div class="sid"><small>รหัสนักศึกษา</small><span id="gnrSidShow">—</span></div></div><div class="gm" id="gnrGame"></div>');
    a.appendChild(idb);
    var sc=el('div','gnr-box gnr-score','<h4>คะแนน Pretest → Posttest</h4>');
    ['.cmp-grid','#sumMsg'].forEach(function(s){ var x=panel.querySelector(s); if(x) sc.appendChild(x); });
    a.appendChild(sc);
    var hud=panel.querySelector('.hud'); if(hud) a.appendChild(hud);
    /* คอลัมน์ B: เรดาร์ + จุดเด่น/จุดด้อย */
    var rb=el('div','gnr-box gnr-radar','<h4>เรดาร์ทักษะรายด้าน</h4>');
    var cb=panel.querySelector('.chartbox'); if(cb) rb.appendChild(cb);
    b.appendChild(rb);
    b.appendChild(el('div','gnr-sw','<div class="sw good"><h5>จุดเด่น</h5><div id="gnrGood"></div></div><div class="sw weak"><h5>ควรเสริม</h5><div id="gnrWeak"></div></div>'));
    /* คอลัมน์ C: กำลังใจ + แท็บรายละเอียด + ปุ่ม */
    c.appendChild(el('div','gnr-cheer',''));
    var tabs=el('div','gnr-tabs'), body=el('div','gnr-tabbody');
    var panes=[['คำแนะนำ','#sumAdvice'],['รายหัวข้อ','#sumDistrictStars'],['รายบท','#sumAxisRows'],['เหรียญตรา','#sumBadges']];
    if(panel.querySelector('#sumPlan')){
      var pw=el('div','gnr-plan'); pw.style.cssText='gap:10px';
      ['#sumPlan','#sumPitLinks'].forEach(function(s){ var x=panel.querySelector(s); if(x){ x.style.display='grid'; pw.appendChild(x);} });
      panes.push(['แผนซ้อม',pw]);
    }
    panes.forEach(function(p,i){
      var node=(typeof p[1]==='string')?panel.querySelector(p[1]):p[1]; if(!node) return;
      body.appendChild(node);
      var bt=el('button','',p[0]); bt.type='button';
      bt.addEventListener('click',function(){ Array.prototype.forEach.call(tabs.children,function(x){x.classList.remove('on');}); Array.prototype.forEach.call(body.children,function(x){x.classList.remove('on');}); bt.classList.add('on'); node.classList.add('on'); });
      tabs.appendChild(bt);
    });
    if(tabs.firstChild){ tabs.firstChild.classList.add('on'); body.firstChild.classList.add('on'); }
    c.appendChild(tabs); c.appendChild(body);
    var br=panel.querySelector('.btn-row');
    if(br){ var hm=el('a','btn','หน้ารวมเกม'); hm.href='index.html'; hm.style.textAlign='center'; hm.style.textDecoration='none'; br.appendChild(hm); c.appendChild(br); }
    c.appendChild(el('div','gnr-note','ภาพหน้าจอนี้ใช้เป็นหลักฐานผลการฝึกได้ · ปุ่ม CSV ด้านบนบันทึกคะแนนพร้อมรหัสนักศึกษาส่งอาจารย์'));
    dash.appendChild(a); dash.appendChild(b); dash.appendChild(c);
    panel.appendChild(dash);
    sec.classList.add('gnr-done');
    var st=document.createElement('style'); st.textContent='.gnr-tabbody>.badges.on{display:flex !important;flex-wrap:wrap;gap:6px}';
    document.head.appendChild(st);
    return panel;
  }
  function fitDash(){
    var d=document.querySelector('.gnr-dash'); if(!d) return;
    if(window.innerWidth<=980){ d.style.removeProperty('--gnr-dash-h'); return; }
    var top=d.getBoundingClientRect().top+window.scrollY;
    var h=Math.max(430, window.innerHeight-top-22);
    d.style.setProperty('--gnr-dash-h', h+'px');
  }
  function enhanceSummary(){
    var panel=buildDash(); if(!panel) return;
    var id=getId()||{sid:MASK, nick:''};
    var nick=(typeof state!=='undefined' && state.name)||id.nick||'ผู้เล่น';
    var max=maxQ(), pre=+(state.pre||0), post=+(state.post||0);
    $('#gnrNick').textContent=nick;
    $('#gnrSidShow').textContent=id.sid||MASK;
    var ava=$('#chipAva'); $('#gnrAva').innerHTML=ava?ava.innerHTML:'';
    var who=$('#sumWho');
    $('#gnrGame').textContent=CFG.title+' · GNR1007'+(who&&who.textContent?' · '+who.textContent.split('·').slice(1).join('·').trim():'');
    document.querySelector('.gnr-when').textContent=new Date().toLocaleString('th-TH',{dateStyle:'medium',timeStyle:'short'});
    var ax=axes(), good=ax.filter(function(x){return x.post>=100;}), weak=ax.filter(function(x){return x.post<=50;});
    good.sort(function(p,q){return q.post-p.post;}); weak.sort(function(p,q){return p.post-q.post;});
    function li(x){ var dd=x.post-x.pre; return '<li><span>'+escH(x.label)+'</span><span>'+x.post+'%'+(dd?(' ('+(dd>0?'+':'')+dd+')'):'')+'</span></li>'; }
    var best=ax.slice().sort(function(p,q){return q.post-p.post;})[0];
    $('#gnrGood').innerHTML=good.length?'<ul>'+good.slice(0,4).map(li).join('')+'</ul>':'<div class="none">ยังไม่มีหัวข้อที่ได้เต็ม'+(best?' · ใกล้ที่สุดคือ '+escH(best.label)+' ('+best.post+'%)':'')+'</div>';
    $('#gnrWeak').innerHTML=weak.length?'<ul>'+weak.slice(0,4).map(li).join('')+'</ul>':'<div class="none">ไม่มีหัวข้อที่ต่ำกว่า 50% ยอดเยี่ยมมาก</div>';
    var weakName=weak.length?weak[0].label:(ax.slice().sort(function(p,q){return p.post-q.post;})[0]||{label:'หัวข้อที่ได้คะแนนน้อยที่สุด'}).label;
    document.querySelector('.gnr-cheer').innerHTML=cheer(nick, pre, post, max, weakName);
    saveResult({sid:id.sid, nick:nick}, pre, post, max);
    styleChart();
    requestAnimationFrame(function(){ fitDash(); setTimeout(function(){ fitDash(); try{ if(radarChart) radarChart.resize(); }catch(e){} },120); });
  }

  /* ---------------- ห่อฟังก์ชันเดิมของเกม ---------------- */
  function wrap(){
    if(typeof showSummary==='function'){
      var _s=showSummary;
      showSummary=function(){ var r=_s.apply(this,arguments); try{ enhanceSummary(); }catch(e){ console.warn('gnr summary',e); } return r; };
    }
    if(typeof drawRadar==='function'){
      var _d=drawRadar;
      drawRadar=function(){ var r=_d.apply(this,arguments); styleChart(); return r; };
    }
    if(typeof goto_==='function'){
      var _g=goto_;
      goto_=function(id){ var r=_g.apply(this,arguments); document.body.classList.toggle('gnr-sum', id==='scr-summary'); queueSvgFix(); return r; };
    }
    if(typeof exportCSV==='function'){
      var _x=exportCSV;
      exportCSV=function(){
        var id=getId(), old=state.name;
        state.name=(old||'')+' | '+((id&&id.sid)||MASK);
        try{ return _x.apply(this,arguments); } finally { state.name=old; }
      };
    }
  }

  document.addEventListener('click',function(e){ if(e.target.closest && e.target.closest('#btnTheme')) setTimeout(onTheme,30); });
  window.addEventListener('resize',function(){ if(document.body.classList.contains('gnr-sum')) fitDash(); });

  setupChrome(); setupLogin(); setupArcade(); wrap();
  if(window.MutationObserver){ new MutationObserver(function(ms){ for(var i=0;i<ms.length;i++){ var n=ms[i].target; if(n.closest && !n.closest('#arcade') && !n.closest('.chartbox')){ queueSvgFix(); return; } } }).observe(document.body,{childList:true,subtree:true}); }
  queueSvgFix();
  var foot=document.querySelector('footer .fmono'); if(foot) foot.textContent+=' · UI v7.1';
})();

/* ---------- 5) จอคอมพิวเตอร์: จัดหน้าบทเรียนเป็น 2 คอลัมน์ (UI v7.1) ----------
   ห่อเนื้อหาเป็นกลุ่ม (หัวข้อ h3 ติดกับเนื้อหาถัดไป · ห้องทดลองทั้งชุดเป็นกลุ่มเดียว) แล้วให้ CSS แบ่งคอลัมน์
   ย้ายโหนดเดิม ไม่คัดลอก จึงไม่กระทบ id/ตัวจัดการเหตุการณ์ของเกม · จอเล็กกว่า 1200px กลุ่มเป็น display:contents (เหมือนเดิม) */
(function(){
  'use strict';
  var IDS=/^scr-(lesson\d|pitwalk)$/;
  function blk(){ var d=document.createElement('div'); d.className='gnr-blk'; return d; }
  function isText(n){ return n.tagName==='P' || n.classList.contains('status-line') || n.classList.contains('readout-line'); }
  function build(sec){
    var panel=sec.querySelector(':scope>.panel'); if(!panel||panel.querySelector('.gnr-flow')) return;
    var kids=[].slice.call(panel.children), i=0;
    while(i<kids.length && (kids[i].classList.contains('tag')||/^H[12]$/.test(kids[i].tagName))) i++;   /* หัวเรื่องอยู่นอกคอลัมน์ */
    var end=kids.length; if(end>i && kids[end-1].classList.contains('btn-row')) end--;                     /* ปุ่มไปต่อท้ายสุดอยู่นอกคอลัมน์ */
    var body=kids.slice(i,end); if(body.length<3) return;
    var flow=document.createElement('div'); flow.className='gnr-flow';
    panel.insertBefore(flow, kids[end]||null);
    var cur=null, keep=0, lab=false;
    body.forEach(function(n){
      if(n.tagName==='H3'){ lab=/ห้องทดลอง|LAB|ทดลอง/i.test(n.textContent); cur=blk(); if(lab) cur.classList.add('gnr-lab'); flow.appendChild(cur); cur.appendChild(n); keep=1; return; }
      if(lab){ cur.appendChild(n); return; }
      if(cur && keep){ cur.appendChild(n); if(!isText(n)) keep=0; return; }
      if(isText(n) && cur && cur.lastElementChild && isText(cur.lastElementChild)){ cur.appendChild(n); return; }
      cur=blk(); flow.appendChild(cur); cur.appendChild(n);
      if(isText(n)) keep=1; else keep=0;   /* ย่อหน้าบรรยายติดกับภาพ/ตารางที่ตามมา */
    });
    sec.classList.add('gnr-cols');
  }
  /* ย่อทั้งหน้าลงเล็กน้อย (ไม่ต่ำกว่า 80% · จอกว้าง >= 1700px ไม่ต่ำกว่า 75%) เมื่อเนื้อหายาวเกินจอไม่มาก เพื่อให้ไม่ต้องเลื่อน · เฉพาะจอคอม (กว้าง >= 1100px และใช้เมาส์) */
  var MINZ=0.8, fitT=0, fitting=false;
  function desk(){ return innerWidth>=1100 && !(window.matchMedia && matchMedia('(pointer:coarse)').matches); }
  function fit(){
    if(fitting) return; fitting=true;
    var a=document.querySelector('.screen.active'), z=1;
    [].slice.call(document.querySelectorAll('.screen')).forEach(function(s){ if(s!==a) s.style.zoom=''; });
    if(a && desk() && !document.body.classList.contains('gnr-sum')){
      a.style.zoom='';
      var doc=document.documentElement.scrollHeight, h=a.getBoundingClientRect().height, over=doc-innerHeight;
      if(over>2 && h>0){ z=Math.max(innerWidth>=1700?0.75:MINZ, Math.floor((h-over-6)/h*100)/100); }
      a.style.zoom = z<1 ? String(z) : '';
    } else if(a){ a.style.zoom=''; }
    fitting=false;
  }
  function queueFit(){ clearTimeout(fitT); fitT=setTimeout(fit,60); }
  window.GNR_fit=fit;
  function sync(){
    var a=document.querySelector('.screen.active');
    document.body.classList.toggle('gnr-wide', !!(a && IDS.test(a.id)));
    queueFit();
  }
  window.addEventListener('resize',queueFit);
  if(window.ResizeObserver){ var ro=new ResizeObserver(function(){ if(!fitting) queueFit(); }); [].slice.call(document.querySelectorAll('.screen')).forEach(function(s){ var p=s.querySelector(':scope>.panel'); if(p) ro.observe(p); }); }
  [].slice.call(document.querySelectorAll('.screen')).forEach(function(s){ if(/^scr-lesson\d$/.test(s.id)) build(s); });   /* pitwalk: ขยายกว้าง + การ์ด 2 คอลัมน์ด้วย CSS */
  sync();
  if(window.MutationObserver){ var mo=new MutationObserver(sync); [].slice.call(document.querySelectorAll('.screen')).forEach(function(s){ mo.observe(s,{attributes:true,attributeFilter:['class']}); }); }
})();
