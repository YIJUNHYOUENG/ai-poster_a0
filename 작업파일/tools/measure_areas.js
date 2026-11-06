(async () => {
  await document.fonts.ready;
  await new Promise(r => setTimeout(r, 300));
  const root = [...document.body.children].find(e => e.tagName === 'DIV');
  const R0 = root.getBoundingClientRect();
  const MM = R0.width / 841;
  const res = [];
  for (const el of root.querySelectorAll('[data-area]')) {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    const innerBottom = r.bottom - parseFloat(cs.paddingBottom) - parseFloat(cs.borderBottomWidth);
    const innerRight = r.right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth);
    let maxB = -Infinity, maxR = -Infinity;
    for (const k of el.querySelectorAll('*')) {
      const q = k.getBoundingClientRect();
      if (q.width === 0 && q.height === 0) continue;
      maxB = Math.max(maxB, q.bottom); maxR = Math.max(maxR, q.right);
    }
    // text overflowing its own box (nowrap labels, figure boxes)
    const tight = [...el.querySelectorAll('*')].filter(k => k.scrollWidth > k.clientWidth + 1 && getComputedStyle(k).display !== 'inline' && k.clientWidth > 0).map(k => k.textContent.trim().slice(0, 18));
    res.push({ area: el.dataset.area, specMM: +el.dataset.mm, boxMM: +(r.height / MM).toFixed(1),
      overBottomMM: +((maxB - innerBottom) / MM).toFixed(1), overRightPx: Math.round(maxR - innerRight), spareMM: +((innerBottom - maxB) / MM).toFixed(1), tight: tight.slice(0, 4) });
  }
  const all = [...root.querySelectorAll('*')];
  const pageBottom = Math.max(...all.map(e => e.getBoundingClientRect().bottom));
  const fonts = {};
  for (const n of all) { if (n.childNodes.length && [...n.childNodes].some(c => c.nodeType === 3 && c.textContent.trim())) { const f = parseFloat(getComputedStyle(n).fontSize); fonts[f.toFixed(2)] = (fonts[f.toFixed(2)] || 0) + 1; } }
  const o = document.createElement('pre'); o.id = 'area-out';
  o.textContent = 'AREAS' + JSON.stringify({ areas: res, pageBottomMM: +((pageBottom - R0.top) / MM).toFixed(1), fonts }) + 'ENDA';
  document.body.appendChild(o);
})();
