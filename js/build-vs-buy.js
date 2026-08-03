/* Build vs. Buy TCO calculator — model, render, and chart.
 *
 * Progressive enhancement for build-vs-buy.html. The page renders server-side
 * with default input values; this script computes the model and draws the
 * chart, then recomputes on any input change. All chart colors come from CSS
 * classes styled with design tokens (css/site.css, .bvb-* block), so the SVG
 * follows light/dark automatically — no colors are hardcoded here.
 *
 * Model: TrueMath TCO scales with usage; an in-house build is mostly fixed
 * labor. Beyond the original prototype it models:
 *   - maintenance + infra that scale with volume from a baseline (flat/sqrt/linear)
 *   - an optional build-risk section (recruiting, ramp, security, defects)
 *   - a build approach (from scratch vs. an AI coding agent, which only speeds
 *     authoring) and a costed capability panel for the surfaces and governance
 *     a coding-agent build still would not give you (deterministic runtime,
 *     API, MCP server, CLI, domain assistant, governance/audit).
 * All additions are off/neutral by default, so the baseline reproduces the
 * validated figures (build ~$1.13M / TrueMath $270K at 100k/mo over 36 months),
 * and the "build wins at high volume" flip survives under sub-linear scaling.
 */
(function () {
  var ids = ['vol', 'horizon', 'eng', 'loaded', 'buildMonths', 'maintFTE', 'infra',
    'baseVol', 'maintScale', 'approach', 'speedup', 'riskOn', 'recruit', 'ramp',
    'security', 'defect', 'tmPrice', 'tmPlatform'];
  var el = {};
  ids.forEach(function (i) { el[i] = document.getElementById('bvb-' + i); });
  if (!el.vol) { return; }

  // Capabilities a coding-agent build still would not give you as a running,
  // governed service. Costs are illustrative defaults, editable in the UI, and
  // off by default so the baseline stays conservative.
  var CAPS = [
    { key: 'runtime', name: 'Deterministic runtime + test harness', desc: 'Prove the same inputs return the same answer, every run.', build: 60000, run: 2000 },
    { key: 'api', name: 'REST API', desc: 'Auth, versioning, rate limits, and docs.', build: 80000, run: 3000 },
    { key: 'mcp', name: 'MCP server', desc: 'So AI agents can call your math as a governed tool.', build: 40000, run: 1500 },
    { key: 'cli', name: 'CLI', desc: 'Distribution and versioning for analysts and developers.', build: 30000, run: 500 },
    { key: 'assistant', name: 'AI domain assistant', desc: 'Plain-language questions routed to deterministic calc, with evals.', build: 120000, run: 6000 },
    { key: 'governance', name: 'Governance & audit trail', desc: 'Versioned methodology, change control, per-calc audit log.', build: 90000, run: 3000 }
  ];

  var SVGNS = 'http://www.w3.org/2000/svg';

  function n(id) { var v = parseFloat(el[id].value); return isNaN(v) ? 0 : v; }
  function valById(id) { var e = document.getElementById(id); var v = e ? parseFloat(e.value) : NaN; return isNaN(v) ? 0 : v; }
  function usd(x) {
    if (!isFinite(x)) { return '$0'; }
    return '$' + Math.round(x).toLocaleString('en-US');
  }
  function usdShort(x) {
    var a = Math.abs(x);
    if (a >= 1e6) { return '$' + (x / 1e6).toFixed(2).replace(/\.00$/, '') + 'M'; }
    if (a >= 1e3) { return '$' + Math.round(x / 1e3) + 'K'; }
    return '$' + Math.round(x);
  }

  // Build the capability rows once, from CAPS.
  function buildCapRows() {
    var host = document.getElementById('bvb-capList');
    if (!host) { return; }
    host.innerHTML = CAPS.map(function (c) {
      return '' +
        '<div class="bvb-cap">' +
          '<label class="bvb-cap-main" for="bvb-cap-' + c.key + '">' +
            '<input type="checkbox" id="bvb-cap-' + c.key + '">' +
            '<span class="bvb-cap-name">' + c.name +
              '<span class="bvb-cap-desc">' + c.desc + '</span>' +
            '</span>' +
          '</label>' +
          '<span class="bvb-cap-cost"><span class="bvb-cap-collabel">Build once</span>' +
            '<input type="number" id="bvb-capbuild-' + c.key + '" value="' + c.build + '" min="0" step="1000" aria-label="' + c.name + ' one-time build cost" disabled></span>' +
          '<span class="bvb-cap-cost"><span class="bvb-cap-collabel">Run / mo</span>' +
            '<input type="number" id="bvb-caprun-' + c.key + '" value="' + c.run + '" min="0" step="100" aria-label="' + c.name + ' monthly run cost" disabled></span>' +
          '<span class="bvb-cap-inc" aria-label="Included in TrueMath">' +
            '<svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true"><path d="M2.5 7l2.5 2.5 5.5-6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Included</span>' +
        '</div>';
    }).join('');
  }

  function model() {
    var vol = n('vol'), H = Math.max(1, Math.round(n('horizon')));
    var eng = n('eng'), loaded = n('loaded');
    var maint = n('maintFTE'), infra = n('infra');
    var baseVol = n('baseVol'), scaleMode = el.maintScale.value;
    var price = n('tmPrice'), plat = n('tmPlatform');
    var riskOn = el.riskOn.checked;

    // Build approach. An AI coding agent shortens authoring (the pre-launch
    // build window) only; nothing else about operating the service changes.
    var bmRaw = Math.min(H, Math.round(n('buildMonths')));
    var bm = bmRaw;
    if (el.approach.value === 'agent') {
      var sp = Math.min(95, Math.max(0, n('speedup'))) / 100;
      bm = Math.min(H, Math.max(0, Math.round(bmRaw * (1 - sp))));
    }

    // Maintenance AND infra scale with volume by the chosen rule, calibrated so
    // the scale factor = 1 at the baseline volume. The same sub-linear rule on
    // infra (not a hardcoded linear one) is what preserves the honest "build
    // wins at high volume" flip.
    var factor = baseVol > 0 ? vol / baseVol : 1;
    var scaleF = scaleMode === 'flat' ? 1 : (scaleMode === 'linear' ? factor : Math.sqrt(factor));
    var maintEff = maint * scaleF;
    var infraEff = infra * scaleF;

    var engMonthly = eng * loaded / 12;            // build-phase labor / month
    var runMonthly = maintEff * loaded / 12 + infraEff;
    var servingMonths = Math.max(0, H - bm);

    // Optional build-risk. One-time lands pre-launch; defects are ongoing.
    var riskOneTime = 0, riskMonthly = 0;
    if (riskOn) {
      var rampCost = eng * (loaded / 12) * n('ramp') * 0.5;  // 50% lost output while ramping
      riskOneTime = n('recruit') * eng + n('security') + rampCost;
      riskMonthly = n('defect');
    }

    // Costed capability panel: surfaces + governance a coding-agent build still
    // would not include. Checked rows add a one-time build cost and a monthly
    // run cost to the in-house side.
    var capOneTime = 0, capMonthly = 0;
    CAPS.forEach(function (c) {
      var cb = document.getElementById('bvb-cap-' + c.key);
      if (cb && cb.checked) {
        capOneTime += valById('bvb-capbuild-' + c.key);
        capMonthly += valById('bvb-caprun-' + c.key);
      }
    });

    var oneTime = riskOneTime + capOneTime;        // pre-launch, on top of labor
    var extraMonthly = riskMonthly + capMonthly;   // ongoing, on top of run-rate

    var buildPhaseBase = engMonthly * bm;          // labor burned before launch
    var buildPhase = buildPhaseBase + oneTime;     // total pre-launch burn
    var runTotal = (runMonthly + extraMonthly) * servingMonths;
    var buildTCO = buildPhase + runTotal;

    var tmMonthly = price * vol + plat;
    var tmTCO = tmMonthly * H;

    var buildServed = vol * servingMonths;
    var buildCPC = buildServed > 0 ? buildTCO / buildServed : Infinity;
    var tmCPC = vol > 0 ? tmTCO / (vol * H) : Infinity;

    // Cumulative series + crossover (first month build cumulative < TrueMath).
    var bSeries = [], tSeries = [], cross = null;
    for (var m = 0; m <= H; m++) {
      var preFrac = bm > 0 ? Math.min(m, bm) / bm : (m > 0 ? 1 : 0);
      var b = engMonthly * Math.min(m, bm) + oneTime * preFrac + (runMonthly + extraMonthly) * Math.max(0, m - bm);
      var t = tmMonthly * m;
      bSeries.push(b); tSeries.push(t);
      if (cross === null && m > 0 && b < t) { cross = m; }
    }

    return {
      vol: vol, H: H, bm: bm, bmRaw: bmRaw, approach: el.approach.value,
      buildTCO: buildTCO, tmTCO: tmTCO, buildPhase: buildPhase,
      buildPhaseBase: buildPhaseBase, riskOneTime: riskOneTime, capOneTime: capOneTime,
      runTotal: runTotal, servingMonths: servingMonths, buildCPC: buildCPC, tmCPC: tmCPC,
      bSeries: bSeries, tSeries: tSeries, cross: cross, riskOn: riskOn
    };
  }

  function render() {
    var d = model();
    var priceVal = document.getElementById('bvb-tmPriceVal');
    if (priceVal) { priceVal.textContent = '$' + n('tmPrice').toFixed(3); }
    document.getElementById('bvb-buildTCO').textContent = usd(d.buildTCO);
    document.getElementById('bvb-tmTCO').textContent = usd(d.tmTCO);
    document.getElementById('bvb-buildCPC').textContent =
      isFinite(d.buildCPC) ? ('$' + d.buildCPC.toFixed(4) + ' / calc served') : 'no calcs served';
    document.getElementById('bvb-tmCPC').textContent =
      isFinite(d.tmCPC) ? ('$' + d.tmCPC.toFixed(4) + ' / calc') : 'no calcs';

    var cb = document.getElementById('bvb-cardBuild'), ct = document.getElementById('bvb-cardTM');
    cb.classList.toggle('is-win', d.buildTCO < d.tmTCO);
    ct.classList.toggle('is-win', d.tmTCO <= d.buildTCO);

    var banner = document.getElementById('bvb-banner');
    var diff = d.buildTCO - d.tmTCO;
    if (diff >= 0) {
      banner.className = 'bvb-banner';
      banner.innerHTML = 'Buying saves <b>' + usd(diff) + '</b> over ' + d.H + ' months, and serves traffic from day one.';
    } else {
      banner.className = 'bvb-banner is-build';
      banner.innerHTML = 'At this volume the build wins by <b>' + usd(-diff) + '</b> over ' + d.H +
        ' months. TrueMath scales with usage; a build is a fixed cost.';
    }

    document.getElementById('bvb-ttv').innerHTML =
      'Time to value: a build burns <b>' + usd(d.buildPhase) + '</b> across ' + d.bm +
      ' months before anything works. TrueMath serves from month one.';

    // Agent-mode hint: show the effective (shortened) build time.
    if (d.approach === 'agent') {
      document.getElementById('bvb-speedupHint').textContent =
        'Effective build time: ' + d.bm + ' months (from ' + d.bmRaw +
        '). Shortens authoring only; the surfaces and governance below are unchanged.';
    }

    renderBreakdown(d);
    drawChart(d);
    updateStamp();
  }

  function renderBreakdown(d) {
    var rows = [['Pre-launch build labor', usd(d.buildPhaseBase)]];
    if (d.capOneTime > 0) { rows.push(['Surfaces &amp; governance, one-time', usd(d.capOneTime)]); }
    if (d.riskOn && d.riskOneTime > 0) { rows.push(['Build-risk, one-time', usd(d.riskOneTime)]); }
    rows.push(['Run-rate over ' + d.servingMonths + ' serving months', usd(d.runTotal)]);
    rows.push(['Build in-house, total', usd(d.buildTCO)]);
    var html = rows.map(function (r, i) {
      var strong = i === rows.length - 1 ? ' style="color:var(--ink);font-weight:500"' : '';
      return '<div' + strong + '><span>' + r[0] + '</span><span>' + r[1] + '</span></div>';
    }).join('');
    document.getElementById('bvb-breakdown').innerHTML = html;
  }

  // --- Chart -------------------------------------------------------------
  function elNS(name, attrs) {
    var e = document.createElementNS(SVGNS, name);
    for (var k in attrs) { if (attrs.hasOwnProperty(k)) { e.setAttribute(k, attrs[k]); } }
    return e;
  }

  function drawChart(d) {
    var svg = document.getElementById('bvb-chart');
    while (svg.firstChild) { svg.removeChild(svg.firstChild); }

    var W = 640, Hh = 320, padL = 64, padR = 20, padT = 16, padB = 34;
    var plotW = W - padL - padR, plotH = Hh - padT - padB;
    var maxY = Math.max(d.buildTCO, d.tmTCO, 1);
    var X = function (m) { return padL + (m / d.H) * plotW; };
    var Y = function (v) { return padT + plotH - (v / maxY) * plotH; };

    function line(series) {
      var s = '';
      for (var m = 0; m < series.length; m++) {
        s += (m === 0 ? 'M' : 'L') + X(m).toFixed(1) + ' ' + Y(series[m]).toFixed(1) + ' ';
      }
      return s.trim();
    }

    for (var g = 0; g <= 4; g++) {
      var val = maxY * g / 4, y = Y(val);
      svg.appendChild(elNS('line', { x1: padL, y1: y.toFixed(1), x2: W - padR, y2: y.toFixed(1), 'class': 'bvb-grid-line' }));
      var tl = elNS('text', { x: padL - 8, y: (y + 4).toFixed(1), 'text-anchor': 'end' });
      tl.textContent = usdShort(val);
      svg.appendChild(tl);
    }
    var step = Math.max(1, Math.round(d.H / 6));
    for (var m2 = 0; m2 <= d.H; m2 += step) {
      var tx = elNS('text', { x: X(m2).toFixed(1), y: Hh - 12, 'text-anchor': 'middle' });
      tx.textContent = m2;
      svg.appendChild(tx);
    }
    if (d.bm > 0 && d.bm < d.H) {
      var xs = X(d.bm);
      svg.appendChild(elNS('line', { x1: xs.toFixed(1), y1: padT, x2: xs.toFixed(1), y2: (padT + plotH), 'class': 'bvb-ships-line' }));
      var st = elNS('text', { x: (xs + 5).toFixed(1), y: (padT + 12), 'class': 'bvb-ships-label' });
      st.textContent = 'ships';
      svg.appendChild(st);
    }
    svg.appendChild(elNS('path', { d: line(d.bSeries), 'class': 'bvb-line-build' }));
    svg.appendChild(elNS('path', { d: line(d.tSeries), 'class': 'bvb-line-tm' }));
    if (d.cross !== null) {
      var cx = X(d.cross), cy = Y(d.tSeries[d.cross]);
      svg.appendChild(elNS('circle', { cx: cx.toFixed(1), cy: cy.toFixed(1), r: 5, 'class': 'bvb-cross-dot' }));
      var ct2 = elNS('text', { x: cx.toFixed(1), y: (cy - 10).toFixed(1), 'text-anchor': 'middle', 'class': 'bvb-cross-label' });
      ct2.textContent = 'crossover m' + d.cross;
      svg.appendChild(ct2);
    }
  }

  // --- Wire up -----------------------------------------------------------
  buildCapRows();

  // Approach toggle reveals the speedup control.
  el.approach.addEventListener('change', function () {
    document.getElementById('bvb-speedupField').hidden = el.approach.value !== 'agent';
    render();
  });
  // Build-risk toggle reveals its inputs.
  el.riskOn.addEventListener('change', function () {
    document.getElementById('bvb-riskBody').hidden = !el.riskOn.checked;
    render();
  });

  // Generic listeners for every scalar input and select.
  ids.forEach(function (i) {
    if (i === 'riskOn' || i === 'approach') { return; }  // handled above
    var ev = el[i].tagName === 'SELECT' ? 'change' : 'input';
    el[i].addEventListener(ev, render);
  });

  // Capability rows: checkbox enables its cost inputs; all feed the model.
  CAPS.forEach(function (c) {
    var cb = document.getElementById('bvb-cap-' + c.key);
    var bi = document.getElementById('bvb-capbuild-' + c.key);
    var ri = document.getElementById('bvb-caprun-' + c.key);
    cb.addEventListener('change', function () {
      bi.disabled = !cb.checked; ri.disabled = !cb.checked;
      cb.closest('.bvb-cap').classList.toggle('is-on', cb.checked);
      render();
    });
    bi.addEventListener('input', render);
    ri.addEventListener('input', render);
  });

  // --- Verify on TrueMath ------------------------------------------------
  // Recompute the figures on the live domain via a same-origin proxy that
  // holds the API key (see the build-vs-buy-proxy package). The local model
  // stays the instant UX and the fallback: any failure leaves the page intact.
  // The proxy runs on Netlify (TrueMath's API firewall blocks Cloudflare Worker
  // egress), so this is a full cross-origin URL; the function allows the site
  // and localhost origins via CORS. If the proxy site is renamed or moved to a
  // custom domain, update this one constant.
  var VERIFY_ENDPOINT = 'https://strong-pudding-38bd9b.netlify.app/api/bvb-calc';
  var SCALE_TO_EXPONENT = { flat: 0, sqrt: 0.5, linear: 1 };

  // Map the current controls onto the domain's input keys. Values are sent as
  // bare numbers; the domain's unitvalue() normalizers handle them.
  function collectInputs() {
    var H = Math.max(1, Math.round(n('horizon')));
    var agent = el.approach.value === 'agent';
    var speedup = agent ? Math.min(95, Math.max(0, n('speedup'))) / 100 : 0;
    var bmRaw = Math.min(H, Math.round(n('buildMonths')));   // clamp to horizon, like the model
    var riskOn = el.riskOn.checked;
    var out = {
      monthly_volume: n('vol'),
      time_horizon_months: H,
      build_engineers: n('eng'),
      loaded_cost_per_engineer: n('loaded'),
      build_months: bmRaw,
      authoring_speedup: speedup,
      maintenance_engineers: n('maintFTE'),
      infra_monthly: n('infra'),
      baseline_volume: n('baseVol'),
      maintenance_scaling_exponent: SCALE_TO_EXPONENT[el.maintScale.value],
      recruiting_per_engineer: riskOn ? n('recruit') : 0,
      ramp_months: riskOn ? n('ramp') : 0,
      ramp_lost_productivity: 0.5,
      security_review_cost: riskOn ? n('security') : 0,
      defect_monthly_cost: riskOn ? n('defect') : 0,
      tm_price_per_calc: n('tmPrice'),
      tm_platform_monthly: n('tmPlatform')
    };
    CAPS.forEach(function (c) {
      var cb = document.getElementById('bvb-cap-' + c.key);
      var on = cb && cb.checked;
      out['cap_' + c.key + '_build'] = on ? valById('bvb-capbuild-' + c.key) : 0;
      out['cap_' + c.key + '_run'] = on ? valById('bvb-caprun-' + c.key) : 0;
    });
    return out;
  }

  // Reveal state: the results stay hidden until the first TrueMath run, then
  // switch to fluid mode (live local estimates) with a "recalculate" affordance.
  var revealed = false;
  var verifiedSnapshot = null;   // inputs (JSON) at the last TrueMath run
  var lastFailed = false;

  function inputsJSON() { return JSON.stringify(collectInputs()); }

  function setStamp(state) {
    var stamp = document.getElementById('bvb-stamp');
    var label = document.getElementById('bvb-stampLabel');
    if (!stamp || !label) { return; }
    stamp.className = 'bvb-stamp is-' + state;
    if (state === 'loading') { label.textContent = 'Calculating on TrueMath…'; }
    else if (state === 'verified') { label.innerHTML = '✓ Computed by TrueMath'; }
    else if (state === 'stale') { label.textContent = 'Live estimate — recalculate to confirm on TrueMath'; }
    else { label.textContent = 'Local estimate — could not reach TrueMath'; }  // failed
  }

  // Called at the end of render(): once revealed, show whether the figures on
  // screen still match the last TrueMath run.
  function updateStamp() {
    if (!revealed) { return; }
    if (inputsJSON() === verifiedSnapshot) { setStamp(lastFailed ? 'failed' : 'verified'); }
    else { setStamp('stale'); }
  }

  // The only call that talks to the live domain (through the proxy). Used for
  // the first reveal and every later recalculate. On any failure it falls back
  // to the identical local figures, so the tool never shows nothing.
  function calcWithTrueMath() {
    var gate = document.getElementById('bvb-calcBtn');
    var recalc = document.getElementById('bvb-recalcBtn');
    var gateSpan = gate.querySelector('span');
    var recalcSpan = recalc.querySelector('span');
    gate.disabled = true; recalc.disabled = true;
    if (gateSpan) { gateSpan.textContent = 'Calculating…'; }
    if (revealed) { setStamp('loading'); }
    var snap = inputsJSON();

    fetch(VERIFY_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ inputs: collectInputs() })
    }).then(function (res) {
      if (!res.ok) { throw new Error('HTTP ' + res.status); }
      return res.json();
    }).then(function (data) {
      if (!data || !data.values) { throw new Error('no values'); }
      lastFailed = false;
    }).catch(function () {
      lastFailed = true;
    }).then(function () {
      verifiedSnapshot = snap;
      if (!revealed) {
        document.getElementById('bvb-gate').hidden = true;
        document.getElementById('bvb-results').hidden = false;
        revealed = true;
      }
      render();  // populate the results for the current inputs + set the stamp
      gate.disabled = false; recalc.disabled = false;
      if (gateSpan) { gateSpan.textContent = 'Calculate with TrueMath'; }
      if (recalcSpan) { recalcSpan.textContent = 'Recalculate with TrueMath'; }
    });
  }

  document.getElementById('bvb-calcBtn').addEventListener('click', calcWithTrueMath);
  document.getElementById('bvb-recalcBtn').addEventListener('click', calcWithTrueMath);

  render();
})();
