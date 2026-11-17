// BrainAware static demo. Plain ES module, no build step.
function getVar(n) { return getComputedStyle(document.documentElement).getPropertyValue(n).trim(); }
const $ = (s, r = document) => r.querySelector(s);
const SVGNS = 'http://www.w3.org/2000/svg';
function svg(tag, attrs = {}, parent) {
  const e = document.createElementNS(SVGNS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}

async function loadBin(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(url + ' ' + r.status);
  const buf = new Uint8Array(await r.arrayBuffer());
  if (buf[0] === 0x1f && buf[1] === 0x8b) {
    const ds = new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'));
    return new Uint8Array(await new Response(ds).arrayBuffer());
  }
  return buf;
}

// state
const S = {
  shape: null, cases: [], caseIdx: 0, vol: null, brain: null, hippo: null,
  cur: { x: 91, y: 109, z: 60 }, sprite: null, volCache: new Map(),
};

const views = {};
for (const fig of document.querySelectorAll('.view[data-plane]')) {
  views[fig.dataset.plane] = {
    fig, canvas: $('canvas', fig), range: $('input', fig), idx: $('.idx', fig),
  };
}

async function init() {
  const meta = await (await fetch('data/cases.json')).json();
  S.shape = meta.shape;
  S.cases = meta.cases.slice().sort((a, b) => a.age - b.age);
  const sel = $('#case-select');
  S.cases.forEach((c, i) => {
    const o = document.createElement('option');
    o.value = i;
    o.textContent = `${c.id} · ${c.age} y ${c.sex} · ${c.site.split(',')[0]}`;
    sel.appendChild(o);
  });
  sel.addEventListener('change', () => selectCase(+sel.value));

  const [X, Y, Z] = S.shape;
  setupView('axial', Z, v => S.cur.z = v, () => S.cur.z);
  setupView('coronal', Y, v => S.cur.y = v, () => S.cur.y);
  setupView('sagittal', X, v => S.cur.x = v, () => S.cur.x);
  for (const id of ['#t-hippo', '#t-strip', '#t-range']) $(id).addEventListener('change', drawAll);

  [S.brain, S.hippo] = await Promise.all([loadBin('data/brainmask.u8.gz'), loadBin('data/hippo.u8.gz')]);
  // start at the hippocampus centroid
  let sx = 0, sy = 0, sz = 0, n = 0;
  for (let z = 0; z < Z; z++) for (let y = 0; y < Y; y++) for (let x = 0; x < X; x++) {
    if (S.hippo[(z * Y + y) * X + x]) { sx += x; sy += y; sz += z; n++; }
  }
  if (n) S.cur = { x: Math.round(sx / n) - 25, y: Math.round(sy / n), z: Math.round(sz / n) };

  $('#input-range').addEventListener('input', e => {
    S.cur.z = curCase().slices[+e.target.value];
    drawAll();
  });
  $('#copy-bib').addEventListener('click', async () => {
    try { await navigator.clipboard.writeText($('#bibtex').textContent); $('#copy-bib').textContent = 'Copied'; }
    catch { $('#copy-bib').textContent = 'Select and copy'; }
    setTimeout(() => $('#copy-bib').textContent = 'Copy BibTeX', 1500);
  });

  await selectCase(0);
  init3D();
}

const curCase = () => S.cases[S.caseIdx];

async function selectCase(i) {
  S.caseIdx = i;
  $('#case-select').value = i;
  const c = curCase();
  renderMeta(c);
  const r = $('#input-range');
  r.min = 0; r.max = c.slices.length - 1;

  const sprite = new Image();
  sprite.src = `data/${c.id}/inputs.jpg`;
  $('#input-sprite').src = sprite.src;
  S.sprite = null;
  sprite.onload = () => { if (curCase() === c) { S.sprite = sprite; drawInput(); } };

  for (const v of Object.values(views)) v.canvas.style.opacity = .35;
  let vol = S.volCache.get(c.id);
  if (!vol) {
    vol = await loadBin(`data/${c.id}/t1.u8.gz`);
    S.volCache.set(c.id, vol);
  }
  if (curCase() !== c) return;
  S.vol = vol;
  for (const v of Object.values(views)) v.canvas.style.opacity = 1;
  drawAll();
  if (three.ready) load3DCase(c);
}

function renderMeta(c) {
  const z0 = c.slices[0], z1 = c.slices[c.slices.length - 1];
  $('#case-meta').innerHTML = `
    <dt>Scan</dt><dd>${c.file}</dd>
    <dt>Subject</dt><dd>${c.age} y, ${c.sex === 'F' ? 'female' : 'male'}, healthy volunteer</dd>
    <dt>Site</dt><dd>${c.site}</dd>
    <dt>Slices</dt><dd>${c.slices.length} axial (z ${z0}–${z1})</dd>`;
}

function drawInput() {
  const c = curCase();
  const k = c.slices.indexOf(S.cur.z);
  const ctx = $('#input-canvas').getContext('2d');
  const meta = $('#input-meta');
  const r = $('#input-range');
  if (k < 0) {
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, 150, 150);
    ctx.fillStyle = '#9fb3cc'; ctx.font = '11px system-ui'; ctx.textAlign = 'center';
    ctx.fillText('axial slice not used', 75, 72); ctx.fillText('by the model', 75, 86);
    meta.innerHTML = `z = ${S.cur.z} is outside the hippocampus range`;
    return;
  }
  r.value = k;
  if (S.sprite) {
    const col = k % 10, row = Math.floor(k / 10);
    ctx.drawImage(S.sprite, col * 150, row * 150, 150, 150, 0, 0, 150, 150);
  }
  meta.innerHTML = `<div class="row"><span>z = ${S.cur.z}</span><span>${k + 1} / ${c.slices.length}</span></div>`;
}

// slice viewers
function planeDims(plane) {
  const [X, Y, Z] = S.shape;
  if (plane === 'axial') return [X, Y];
  if (plane === 'coronal') return [X, Z];
  return [Y, Z];
}
// canvas pixel (c, r) -> voxel (x, y, z)
function toVoxel(plane, c, r) {
  const [X, Y, Z] = S.shape;
  const v = { ...S.cur };
  if (plane === 'axial') { v.x = X - 1 - c; v.y = Y - 1 - r; }
  else if (plane === 'coronal') { v.x = X - 1 - c; v.z = Z - 1 - r; }
  else { v.y = Y - 1 - c; v.z = Z - 1 - r; }
  return v;
}

function setupView(plane, n, set, get) {
  const v = views[plane];
  const [w, h] = planeDims(plane);
  v.canvas.width = w; v.canvas.height = h;
  v.range.min = 0; v.range.max = n - 1;
  v.range.addEventListener('input', () => { set(+v.range.value); drawAll(); });
  v.get = get;
  const pick = e => {
    const rect = v.canvas.getBoundingClientRect();
    const sc = Math.min(rect.width / w, rect.height / h);
    const ox = (rect.width - w * sc) / 2, oy = (rect.height - h * sc) / 2;
    const c = Math.floor((e.clientX - rect.left - ox) / sc), r = Math.floor((e.clientY - rect.top - oy) / sc);
    if (c < 0 || r < 0 || c >= w || r >= h) return;
    const p = toVoxel(plane, c, r);
    if (plane === 'axial') { S.cur.x = p.x; S.cur.y = p.y; }
    else if (plane === 'coronal') { S.cur.x = p.x; S.cur.z = p.z; }
    else { S.cur.y = p.y; S.cur.z = p.z; }
    drawAll();
  };
  let down = false;
  v.canvas.addEventListener('pointerdown', e => { down = true; v.canvas.setPointerCapture(e.pointerId); pick(e); });
  v.canvas.addEventListener('pointermove', e => { if (down) pick(e); });
  v.canvas.addEventListener('pointerup', () => { down = false; });
}

function drawPlane(plane) {
  const v = views[plane];
  const [X, Y, Z] = S.shape;
  const [w, h] = planeDims(plane);
  const ctx = v.canvas.getContext('2d');
  const img = ctx.createImageData(w, h);
  const d = img.data;
  const showH = $('#t-hippo').checked, strip = $('#t-strip').checked;
  const { x: cx, y: cy, z: cz } = S.cur;
  for (let r = 0; r < h; r++) {
    for (let c = 0; c < w; c++) {
      let x, y, z;
      if (plane === 'axial') { x = X - 1 - c; y = Y - 1 - r; z = cz; }
      else if (plane === 'coronal') { x = X - 1 - c; y = cy; z = Z - 1 - r; }
      else { x = cx; y = Y - 1 - c; z = Z - 1 - r; }
      const i = (z * Y + y) * X + x;
      let g = S.vol[i];
      if (strip && !S.brain[i]) g = 0;
      let R = g, G = g, B = g;
      if (showH && S.hippo[i]) { R = g * .45 + 255 * .55; G = g * .45 + 70 * .55; B = g * .45 + 70 * .55; }
      const o = (r * w + c) * 4;
      d[o] = R; d[o + 1] = G; d[o + 2] = B; d[o + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);

  // crosshair
  ctx.lineWidth = 1;
  ctx.strokeStyle = 'rgba(79,163,255,.55)';
  let col, row;
  if (plane === 'axial') { col = X - 1 - cx; row = Y - 1 - cy; }
  else if (plane === 'coronal') { col = X - 1 - cx; row = Z - 1 - cz; }
  else { col = Y - 1 - cy; row = Z - 1 - cz; }
  ctx.beginPath();
  ctx.moveTo(col + .5, 0); ctx.lineTo(col + .5, h);
  ctx.moveTo(0, row + .5); ctx.lineTo(w, row + .5);
  ctx.stroke();

  // model slice range
  const c = curCase();
  const z0 = c.slices[0], z1 = c.slices[c.slices.length - 1];
  if ($('#t-range').checked && plane !== 'axial') {
    ctx.strokeStyle = 'rgba(255,200,60,.85)';
    ctx.setLineDash([4, 3]);
    ctx.beginPath();
    for (const zz of [z0, z1]) { const rr = Z - 1 - zz + .5; ctx.moveTo(0, rr); ctx.lineTo(w, rr); }
    ctx.stroke();
    ctx.setLineDash([]);
  }
  // orientation letters
  ctx.fillStyle = 'rgba(207,224,245,.8)';
  ctx.font = '9px system-ui';
  if (plane !== 'sagittal') { ctx.fillText('R', 3, h / 2); ctx.fillText('L', w - 9, h / 2); }
  else { ctx.fillText('A', 3, h / 2); ctx.fillText('P', w - 9, h / 2); }

  const n = plane === 'axial' ? Z : plane === 'coronal' ? Y : X;
  const val = v.get();
  v.range.value = val;
  let label = `${val} / ${n - 1}`;
  if (plane === 'axial' && val >= z0 && val <= z1) label += ' · used by model';
  v.idx.textContent = label;
}

let raf = 0;
function drawAll() {
  if (raf) return;
  raf = requestAnimationFrame(() => {
    raf = 0;
    if (!S.vol) return;
    for (const p of Object.keys(views)) drawPlane(p);
    drawInput();
  });
}

// 3D
const three = { ready: false };
async function init3D() {
  const box = $('#three-box');
  const msg = $('#three-msg');
  try {
    const THREE = await import('./vendor/three.module.min.js');
    const { OrbitControls } = await import('./vendor/OrbitControls.js');
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000);
    box.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(35, 1, 1, 2000);
    camera.position.set(-330, 60, 120);
    scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 1.1));
    const dl = new THREE.DirectionalLight(0xffffff, 1.6);
    dl.position.set(0, 0, 1);
    camera.add(dl);
    scene.add(camera);
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enablePan = false;
    controls.minDistance = 150; controls.maxDistance = 700;
    const render = () => renderer.render(scene, camera);
    controls.addEventListener('change', render);
    const resize = () => {
      const r = box.getBoundingClientRect();
      renderer.setSize(r.width, r.height, false);
      renderer.domElement.style.width = '100%';
      renderer.domElement.style.height = '100%';
      camera.aspect = r.width / r.height || 1;
      camera.updateProjectionMatrix();
      render();
    };
    new ResizeObserver(resize).observe(box);
    Object.assign(three, { THREE, scene, camera, controls, render, ready: true, group: null });

    const hip = await loadMesh('data/hippo.mesh.gz', false, 0xff4646);
    three.hippo = hip;
    hip.material.depthTest = true;
    scene.add(hip);
    for (const id of ['#t-brain3d', '#t-hippo3d']) $(id).addEventListener('change', apply3DToggles);
    await load3DCase(curCase());
    resize();
  } catch (err) {
    msg.textContent = 'WebGL not available';
    console.error(err);
  }
}

const CENTER = [91, 109, 80];
async function loadMesh(url, colored, color) {
  const { THREE } = three;
  const buf = await loadBin(url);
  const hdr = new Uint32Array(buf.buffer.slice(0, 8));
  const nv = hdr[0], nf = hdr[1];
  let off = 8;
  const pos16 = new Uint16Array(buf.buffer.slice(off, off + nv * 6)); off += nv * 6;
  const pos = new Float32Array(nv * 3);
  for (let i = 0; i < nv; i++) {
    const x = pos16[i * 3] / 10, y = pos16[i * 3 + 1] / 10, z = pos16[i * 3 + 2] / 10;
    pos[i * 3] = x - CENTER[0]; pos[i * 3 + 1] = z - CENTER[2]; pos[i * 3 + 2] = -(y - CENTER[1]);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  if (colored) {
    const col = new Uint8Array(buf.buffer.slice(off, off + nv * 3)); off += nv * 3;
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3, true));
  }
  geo.setIndex(new THREE.BufferAttribute(new Uint32Array(buf.buffer.slice(off, off + nf * 12)), 1));
  geo.computeVertexNormals();
  const mat = new THREE.MeshPhongMaterial({
    color: colored ? 0xffffff : color, vertexColors: colored, shininess: 25, side: THREE.DoubleSide,
  });
  return new THREE.Mesh(geo, mat);
}

async function load3DCase(c) {
  const msg = $('#three-msg');
  msg.style.display = 'block';
  msg.textContent = 'Loading mesh…';
  const mesh = await loadMesh(`data/${c.id}/brain.mesh.gz`, true);
  if (curCase() !== c) return;
  if (three.group) { three.scene.remove(three.group); three.group.geometry.dispose(); three.group.material.dispose(); }
  three.group = mesh;
  mesh.renderOrder = 2;
  three.scene.add(mesh);
  msg.style.display = 'none';
  apply3DToggles();
}

function apply3DToggles() {
  if (!three.group) return;
  const showB = $('#t-brain3d').checked, showH = $('#t-hippo3d').checked;
  const m = three.group.material;
  three.group.visible = showB;
  three.hippo.visible = showH;
  m.transparent = showH;
  m.opacity = showH ? 0.45 : 1;
  m.depthWrite = !showH;
  m.needsUpdate = true;
  three.render();
}

init().catch(err => {
  console.error(err);
  $('#case-meta').innerHTML = '<dd>Failed to load demo data.</dd>';
});
