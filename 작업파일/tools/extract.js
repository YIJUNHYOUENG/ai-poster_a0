(async () => {
  await document.fonts.ready;
  await new Promise(r => setTimeout(r, 300));
  const root = [...document.body.children].find(e => e.tagName === 'DIV');
  const R0 = root.getBoundingClientRect();
  const out = { W: R0.width, H: R0.height, rects: [], ovals: [], texts: [], lines: [], images: [], chart: null };
  const box = (r) => ({ x: r.left - R0.left, y: r.top - R0.top, w: r.width, h: r.height });
  const parseColor = (c) => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(',').map(s => parseFloat(s)); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const inSkip = (el) => !!el.closest('svg, .math');

  // effective background behind an element (for alpha blending)
  const bgOf = (el) => {
    const stack = [];
    for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
      const c = parseColor(getComputedStyle(e).backgroundColor);
      if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; }
    }
    let base = { r: 255, g: 255, b: 255 };
    for (let i = stack.length - 1; i >= 0; i--) { const c = stack[i]; base = { r: c.r * c.a + base.r * (1 - c.a), g: c.g * c.a + base.g * (1 - c.a), b: c.b * c.a + base.b * (1 - c.a) }; }
    return base;
  };
  const solid = (c, el) => { if (c.a >= 1) return c; const b = bgOf(el); return { r: c.r * c.a + b.r * (1 - c.a), g: c.g * c.a + b.g * (1 - c.a), b: c.b * c.a + b.b * (1 - c.a), a: 1 }; };
  const hex = (c) => [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();

  { const rb = parseColor(getComputedStyle(root).backgroundColor); out.bg = rb && rb.a > 0 ? hex(rb) : 'FFFFFF'; }
  const all = [...root.querySelectorAll('*')];
  const order = new Map(all.map((e, i) => [e, i]));
  // backgrounds and borders
  for (const el of all) {
    if (inSkip(el)) continue;
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const rad = cs.borderTopLeftRadius;
    if (rad.endsWith('%') ? parseFloat(rad) >= 50 : parseFloat(rad) >= Math.min(r.width, r.height) / 2 - 0.5) {
      const ob = parseColor(cs.backgroundColor), bw = parseFloat(cs.borderTopWidth), bc = parseColor(cs.borderTopColor);
      out.ovals.push({ ...box(r), fill: ob && ob.a > 0 ? hex(solid(ob, el.parentElement)) : null, lineW: bw, line: bw > 0 && bc ? hex(solid(bc, el.parentElement)) : null, z: order.get(el) });
      continue;
    }
    const bg = parseColor(cs.backgroundColor);
    const sides = ['Top', 'Right', 'Bottom', 'Left'].map(sd => [parseFloat(cs['border' + sd + 'Width']), cs['border' + sd + 'Style'], cs['border' + sd + 'Color']]);
    const uniform = sides[0][0] > 0 && sides[0][1] !== 'none' && sides.every(x => x[0] === sides[0][0] && x[1] === sides[0][1] && x[2] === sides[0][2]);
    if (uniform) {
      const pb = el.parentElement ? bgOf(el.parentElement) : { r: 255, g: 255, b: 255 };
      const fill = bg && bg.a > 0 ? hex({ r: bg.r * bg.a + pb.r * (1 - bg.a), g: bg.g * bg.a + pb.g * (1 - bg.a), b: bg.b * bg.a + pb.b * (1 - bg.a) }) : null;
      out.rects.push({ ...box(r), color: fill, radius: parseFloat(cs.borderTopLeftRadius) || 0, lineW: sides[0][0], line: hex(solid(parseColor(sides[0][2]), el.parentElement)), dash: sides[0][1] === 'dashed', z: order.get(el) });
      continue;
    }
    if (bg && bg.a > 0) {
      const parentBg = el.parentElement ? bgOf(el.parentElement) : { r: 255, g: 255, b: 255 };
      const c = { r: bg.r * bg.a + parentBg.r * (1 - bg.a), g: bg.g * bg.a + parentBg.g * (1 - bg.a), b: bg.b * bg.a + parentBg.b * (1 - bg.a) };
      out.rects.push({ ...box(r), color: hex(c), radius: parseFloat(cs.borderTopLeftRadius) || 0, z: order.get(el) });
    }
    for (const side of ['Top', 'Bottom', 'Left', 'Right']) {
      const w = parseFloat(cs['border' + side + 'Width']);
      if (w > 0 && cs['border' + side + 'Style'] !== 'none') {
        const c = parseColor(cs['border' + side + 'Color']);
        const b = box(r);
        const g = side === 'Top' ? { x: b.x, y: b.y, w: b.w, h: w } : side === 'Bottom' ? { x: b.x, y: b.y + b.h - w, w: b.w, h: w }
          : side === 'Left' ? { x: b.x, y: b.y, w: w, h: b.h } : { x: b.x + b.w - w, y: b.y, w: w, h: b.h };
        out.rects.push({ ...g, color: hex(solid(c, el)), z: order.get(el) + 0.5 });
      }
    }
  }

  // text blocks
  const isInline = (e) => { const d = getComputedStyle(e).display; return d === 'inline' || e.tagName === 'BR'; };
  const blocks = all.filter(el => {
    if (inSkip(el) || isInline(el)) return false;
    // swatches: textless inline-blocks are drawn as rects and may sit inside a line of text
    const swatch = (c) => getComputedStyle(c).display === 'inline-block' && !c.textContent.trim();
    if (![...el.children].every(c => isInline(c) || swatch(c) || c.tagName.toLowerCase() === 'svg')) return false;
    const tw = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    let n; while ((n = tw.nextNode())) { if (!n.parentElement.closest('svg') && n.textContent.trim()) return true; }
    return false;
  });
  const range = document.createRange();
  for (const el of blocks) {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
    const bl = parseFloat(cs.borderLeftWidth), bt = parseFloat(cs.borderTopWidth), bbw = parseFloat(cs.borderBottomWidth);
    let content = { x: r.left - R0.left + pl + bl, y: r.top - R0.top + pt + bt, w: r.width - pl - pr - bl * 2, h: r.height - pt - pb - bt - bbw };
    // rotated label: keep the unrotated box around the same centre, one line, and the angle
    let rot = 0;
    const tm = cs.transform.match(/matrix\(([^)]+)\)/);
    if (tm) { const q = tm[1].split(',').map(parseFloat); rot = Math.round(Math.atan2(q[1], q[0]) * 180 / Math.PI); }
    if (rot) {
      const w0 = el.offsetWidth - pl - pr, h0 = el.offsetHeight - pt - pb, cx = r.left - R0.left + r.width / 2, cy = r.top - R0.top + r.height / 2;
      content = { x: cx - w0 / 2, y: cy - h0 / 2, w: w0, h: h0 };
    }
    const runs = [];
    let lineTop = null, first = true, minX = Infinity, maxX = -Infinity, minY = Infinity;
    const nodes = [];
    const collect = (n) => {
      for (const c of n.childNodes) {
        if (c.nodeType === 3) nodes.push({ t: c });
        else if (c.nodeType === 1) {
          if (c.tagName.toLowerCase() === 'svg') continue;
          if (c.tagName === 'BR') { nodes.push({ br: true }); continue; }
          collect(c);
        }
      }
    };
    collect(el);
    for (const it of nodes) {
      if (it.br) { runs.push({ text: '\n' }); lineTop = null; continue; }
      const t = it.t, s = t.textContent;
      const pcs = getComputedStyle(t.parentElement);
      const col = solid(parseColor(pcs.color), t.parentElement);
      let va = 'base';
      for (let e = t.parentElement; e && e !== el; e = e.parentElement) { const v = getComputedStyle(e).verticalAlign; if (v === 'sub') va = 'sub'; if (v === 'super') va = 'sup'; }
      const style = { size: parseFloat(pcs.fontSize), bold: parseInt(pcs.fontWeight) >= 600, italic: pcs.fontStyle === 'italic', color: hex(col), va, ls: pcs.letterSpacing === 'normal' ? 0 : parseFloat(pcs.letterSpacing) };
      let buf = '';
      for (let i = 0; i < s.length; i++) {
        range.setStart(t, i); range.setEnd(t, i + 1);
        const rs = range.getClientRects();
        if (!rs.length) { continue; }
        const q = rs[0];
        if (q.width > 0) { minX = Math.min(minX, q.left); maxX = Math.max(maxX, q.right); minY = Math.min(minY, q.top); }
        const isSpace = /\s/.test(s[i]);
        // lineTop holds the vertical centre of the current line's first glyph; a glyph whose centre
        // sits more than half a line below it starts a new line (mixed sizes on one line stay together)
        const mid = (q.top + q.bottom) / 2;
        const blockLh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3;
        if (!rot && !isSpace && lineTop !== null && mid > lineTop + blockLh * 0.5 && va === 'base') {
          buf = buf.replace(/\s+$/, '');
          if (buf) runs.push({ text: buf, ...style }); buf = '';
          runs.push({ text: '\n' });
          lineTop = mid;
        }
        if (!isSpace && lineTop === null && va === 'base') lineTop = mid;
        buf += s[i];
      }
      if (buf) runs.push({ text: buf, ...style });
    }
    // collapse whitespace like the browser
    const clean = [];
    for (const rn of runs) {
      if (rn.text === '\n') { if (clean.length && clean[clean.length - 1].text !== '\n') { const l = clean[clean.length - 1]; l.text = l.text.replace(/\s+$/, ''); } clean.push(rn); continue; }
      let tx = rn.text.replace(/\s+/g, ' ');
      const prev = clean[clean.length - 1];
      if (!prev || prev.text === '\n' || /\s$/.test(prev.text)) tx = tx.replace(/^\s+/, '');
      if (tx) clean.push({ ...rn, text: tx });
    }
    while (clean.length && clean[clean.length - 1].text === '\n') clean.pop();
    if (clean.length) { const l = clean[clean.length - 1]; l.text = l.text.replace(/\s+$/, ''); }
    const disp = cs.display;
    const flexCenter = (disp === 'flex' || disp === 'inline-flex') && cs.alignItems === 'center';
    out.texts.push({
      tag: el.tagName, ...content, runs: clean,
      align: (disp === 'flex' && cs.justifyContent === 'center') ? 'center' : (cs.textAlign === 'start' ? 'left' : cs.textAlign === 'end' ? 'right' : cs.textAlign),
      lh: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3,
      middle: flexCenter,
      bullet: cs.display === 'list-item',
      textX: rot ? content.x : minX - R0.left, textY: rot ? content.y : minY - R0.top, rot
    });
  }

  // svgs
  for (const svg of root.querySelectorAll('svg')) {
    const r = box(svg.getBoundingClientRect());
    if ((svg.getAttribute('aria-label') || '').startsWith('그림 2')) { out.chart = r; continue; }
    if (svg.parentElement.tagName === 'SPAN') { out.images.push({ ...r, kind: 'legend', z: order.get(svg) }); continue; }
    if ([...svg.querySelectorAll(':scope > path')].some(p => /Z\s*$/.test(p.getAttribute('d') || ''))) { out.images.push({ ...r, kind: 'icon', z: order.get(svg) }); continue; }
    const vb = (svg.getAttribute('viewBox') || `0 0 ${r.w} ${r.h}`).split(/\s+/).map(Number);
    const sx = r.w / vb[2], sy = r.h / vb[3];
    for (const p of svg.querySelectorAll(':scope > path')) {
      const m = p.getAttribute('d').match(/M\s*([\d.]+)\s+([\d.]+)\s+L\s*([\d.]+)\s+([\d.]+)/);
      if (!m) continue;
      let [x1, y1, x2, y2] = m.slice(1).map(Number);
      const pcs = getComputedStyle(p);
      const sw = parseFloat(pcs.strokeWidth);
      const arrow = !!p.getAttribute('marker-end');
      if (arrow) { const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy); x2 += dx / L * 2 * sw; y2 += dy / L * 2 * sw; }
      out.lines.push({ x1: r.x + x1 * sx, y1: r.y + y1 * sy, x2: r.x + x2 * sx, y2: r.y + y2 * sy, sw, color: hex(parseColor(pcs.stroke)), arrow, z: order.get(svg) });
    }
  }
  for (const m of root.querySelectorAll('.math')) out.images.push({ ...box(m.getBoundingClientRect()), kind: 'math', z: order.get(m) });

  const o = document.createElement('pre'); o.id = 'extract-out';
  o.textContent = 'EXTRACT' + JSON.stringify(out) + 'ENDX';
  document.body.appendChild(o);
})();
