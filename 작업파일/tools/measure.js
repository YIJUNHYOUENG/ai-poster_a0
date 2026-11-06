(async () => {
  await document.fonts.ready;
  await new Promise(r => setTimeout(r, 300));
  const root = [...document.body.children].find(e => e.tagName === 'DIV');
  const rows = [...root.children].map(k => {
    const r = k.getBoundingClientRect();
    const cs = getComputedStyle(k);
    const kids = [...k.querySelectorAll('*')];
    const cb = Math.max(...kids.map(c => c.getBoundingClientRect().bottom), r.top);
    return [(k.querySelector('h1,h2,h3') || k).textContent.trim().slice(0, 8), Math.round(r.top), Math.round(r.bottom), Math.round(cb), Math.round(r.bottom - parseFloat(cs.paddingBottom) - cb)];
  });
  const all = [...root.querySelectorAll('*')];
  const rr = root.getBoundingClientRect();
  const clipped = all.filter(e => { const q = e.getBoundingClientRect(); return q.width > 0 && (q.right > rr.right + 0.5 || q.bottom > rr.bottom + 0.5); }).map(e => e.tagName + ':' + e.textContent.trim().slice(0, 12)).slice(0, 8);
  const hs = [...root.querySelectorAll('h1,h2')].map(h => [h.textContent.trim().slice(0, 6), Math.round(h.getBoundingClientRect().height / parseFloat(getComputedStyle(h).lineHeight))]);
  const o = document.createElement('pre'); o.id = 'measure-out';
  o.textContent = 'MEASURE' + JSON.stringify({rows, clipped, hs}) + 'END';
  document.body.appendChild(o);
})();
