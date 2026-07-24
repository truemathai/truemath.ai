/* TrueMath vertical landing pages — interactive demo.
   Progressive enhancement: the page renders fully without JS (all prompts and
   results are in the HTML). When JS runs we add `tmv-js` to <body>, which
   collapses the launchers and hides each result behind an "Ask" button so the
   calculation reveals step by step. Charts are drawn here from a plain array of
   numbers in `data-values`, auto-scaled — no per-vertical chart code. */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.body.classList.add("tmv-js");

  /* ---------- launcher open/close ---------- */
  document.querySelectorAll(".tmv-lhead").forEach(function (head) {
    head.addEventListener("click", function () {
      head.closest(".tmv-launcher").classList.toggle("open");
    });
  });

  /* ---------- Ask: reveal the result ---------- */
  document.querySelectorAll(".tmv-ask").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (btn.disabled) return;
      var launcher = btn.closest(".tmv-launcher");
      var hint = btn.previousElementSibling;
      btn.disabled = true;
      btn.innerHTML = '<span class="tmv-spin"></span> Running';
      if (hint) hint.textContent = "Running the calculation…";

      setTimeout(function () {
        launcher.classList.add("spent");
        var status = launcher.querySelector(".tmv-status");
        if (status) status.innerHTML = '<span style="color:#12B886;font-weight:700">✓ run</span>';
        revealSteps(launcher);
        drawCharts(launcher);
      }, reduce ? 0 : 450);
    });
  });

  /* Reveal the result one step at a time, growing the box as each appears.
     Steps start collapsed (display:none), so the scrollable content grows step
     by step — the scrollbar tracks real content instead of pre-claiming full
     height. The view follows each new step to the bottom edge as it lands. */
  function revealSteps(launcher) {
    var scroll = launcher.querySelector(".tmv-scroll");
    var steps = launcher.querySelector(".tmv-steps");
    var items = steps ? Array.prototype.slice.call(steps.children) : [];
    var finalEl = launcher.querySelector(".tmv-finalwrap");

    items.forEach(function (el) { el.style.display = "none"; });
    if (finalEl) finalEl.style.display = "none";

    if (reduce) {
      items.forEach(function (el) { el.style.display = ""; });
      if (finalEl) finalEl.style.display = "";
      if (scroll) scroll.scrollTop = 0;
      return;
    }

    function show(el) {
      el.style.display = "";
      el.style.opacity = "0";
      el.style.transition = "opacity .18s ease";
      requestAnimationFrame(function () { el.style.opacity = "1"; });
      if (scroll) scroll.scrollTop = scroll.scrollHeight;
    }

    var i = 0;
    (function next() {
      if (i < items.length) {
        show(items[i]);
        i++;
        setTimeout(next, 230);
      } else if (finalEl) {
        show(finalEl);
      }
    })();
  }

  /* ---------- charts ---------- */
  function drawCharts(scope) {
    scope.querySelectorAll(".tmv-chart").forEach(function (el) {
      if (el.dataset.drawn) return;
      var data;
      try { data = JSON.parse(el.getAttribute("data-values")); } catch (e) { return; }
      if (!data || !data.length) return;
      el.innerHTML = buildChart(data, el.getAttribute("data-label") || "");
      el.dataset.drawn = "1";
    });
  }

  function niceNum(x) {
    if (x <= 0) return 1;
    var exp = Math.floor(Math.log10(x)), f = x / Math.pow(10, exp), nice;
    nice = f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10;
    return nice * Math.pow(10, exp);
  }

  function fmtY(v) {
    var a = Math.abs(v), s = v < 0 ? "-" : "";
    if (a >= 1000) return s + "$" + Math.round(a / 100) / 10 + "k";
    return s + "$" + Math.round(a);
  }

  /* Full-dollar label with thousands separators, e.g. $2,628,000. */
  function fmtFull(v) {
    return "$" + Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  /* Grouped two-series bar chart: each row is [seriesA, seriesB]. Reproduces
     the TrueMath equity-payback chart — Cumulative Distributions (red) beside
     Equity Invested (gold), full-dollar axis, one group per year. */
  function buildGroupedChart(rows, axisLabel) {
    var x0 = 64, x1 = 636, yTop = 12, yBot = 224, plotH = yBot - yTop;
    var all = [0];
    rows.forEach(function (r) { all.push(r[0], r[1]); });
    var lo = Math.min.apply(null, all), hi = Math.max.apply(null, all);
    var step = niceNum((hi - lo) / 10) || 1;
    var vMin = Math.floor(lo / step) * step, vMax = Math.ceil(hi / step) * step;
    if (vMax === vMin) vMax = vMin + step;
    var span = vMax - vMin;
    var y = function (v) { return yBot - ((v - vMin) / span) * plotH; };
    var base = y(0);
    var n = rows.length, gap = (x1 - x0) / n;
    var barW = gap * 0.30, gapBetween = gap * 0.06;
    var leftPad = (gap - (2 * barW + gapBetween)) / 2;

    var grid = "";
    for (var gv = vMin; gv <= vMax + step / 2; gv += step) {
      var gy = y(gv);
      grid += '<line x1="' + x0 + '" y1="' + gy.toFixed(1) + '" x2="' + x1 + '" y2="' + gy.toFixed(1) + '" stroke="#E7E1EE" stroke-width="1"/>' +
        '<text x="' + (x0 - 6) + '" y="' + (gy + 3).toFixed(1) + '" text-anchor="end" font-size="8" fill="#8A7E99">' + fmtFull(gv) + "</text>";
    }

    var bars = "", ticks = "";
    rows.forEach(function (r, i) {
      var gx = x0 + gap * i + leftPad, gx2 = gx + barW + gapBetween;
      var y1 = y(r[0]), y2 = y(r[1]);
      bars += '<rect x="' + gx.toFixed(1) + '" y="' + Math.min(y1, base).toFixed(1) + '" width="' + barW.toFixed(1) + '" height="' + Math.max(Math.abs(base - y1), 0.6).toFixed(1) + '" rx=".5" fill="#D14D57"/>' +
        '<rect x="' + gx2.toFixed(1) + '" y="' + Math.min(y2, base).toFixed(1) + '" width="' + barW.toFixed(1) + '" height="' + Math.max(Math.abs(base - y2), 0.6).toFixed(1) + '" rx=".5" fill="#E2C04A"/>';
      ticks += '<text x="' + (x0 + gap * i + gap / 2).toFixed(1) + '" y="238" text-anchor="middle" font-size="9" fill="#8A7E99">' + (i + 1) + "</text>";
    });

    return '<svg viewBox="0 0 660 270" role="img">' + grid +
      '<line x1="' + x0 + '" y1="' + yTop + '" x2="' + x0 + '" y2="' + yBot + '" stroke="#D8D2E0" stroke-width="1"/>' +
      bars + ticks +
      (axisLabel ? '<text x="' + ((x0 + x1) / 2).toFixed(0) + '" y="258" text-anchor="middle" font-size="10" fill="#8A7E99">' + axisLabel + "</text>" : "") +
      "</svg>";
  }

  /* Build an auto-scaled bar chart. `data` is any array of numbers; the axis
     bounds, zero line, ticks and labels are all derived from the data. Rows of
     [a, b] pairs render as a grouped two-series chart instead. */
  function buildChart(data, axisLabel) {
    if (Array.isArray(data[0])) return buildGroupedChart(data, axisLabel);
    var x0 = 52, x1 = 636, yTop = 10, yBot = 228, plotH = yBot - yTop;
    var lo = Math.min(0, Math.min.apply(null, data));
    var hi = Math.max(0, Math.max.apply(null, data));
    var step = niceNum((hi - lo) / 4) || 1;
    var vMin = Math.floor(lo / step) * step;
    var vMax = Math.ceil(hi / step) * step;
    if (vMax === vMin) vMax = vMin + step;
    var span = vMax - vMin;
    var y = function (v) { return yBot - ((v - vMin) / span) * plotH; };
    var zeroY = y(0);
    var n = data.length, gap = (x1 - x0) / n, bw = gap * 0.72;

    var bars = "";
    data.forEach(function (v, i) {
      var vy = y(v), x = x0 + gap * i + (gap - bw) / 2;
      var top = Math.min(vy, zeroY), h = Math.max(Math.abs(zeroY - vy), 0.6);
      bars += '<rect x="' + x.toFixed(1) + '" y="' + top.toFixed(1) + '" width="' + bw.toFixed(1) +
        '" height="' + h.toFixed(1) + '" rx=".5" fill="' + (v < 0 ? "#E08A90" : "#D14D57") + '"/>';
    });

    var ticks = "", every = Math.max(1, Math.round(n / 7));
    for (var m = 1; m <= n; m += every) {
      var tx = x0 + gap * (m - 1) + gap / 2;
      ticks += '<text x="' + tx.toFixed(1) + '" y="242" text-anchor="middle" font-size="8" fill="#8A7E99">' + m + "</text>";
    }

    return '<svg viewBox="0 0 660 270" role="img">' +
      '<line x1="' + x0 + '" y1="' + yTop + '" x2="' + x0 + '" y2="' + yBot + '" stroke="#D8D2E0" stroke-width="1"/>' +
      '<line x1="' + x0 + '" y1="' + zeroY.toFixed(1) + '" x2="' + x1 + '" y2="' + zeroY.toFixed(1) + '" stroke="#C9C2D4" stroke-width="1" stroke-dasharray="3 3"/>' +
      '<text x="46" y="' + (zeroY + 3).toFixed(1) + '" text-anchor="end" font-size="9" fill="#8A7E99">$0</text>' +
      '<text x="46" y="14" text-anchor="end" font-size="9" fill="#8A7E99">' + fmtY(vMax) + "</text>" +
      '<text x="46" y="' + yBot + '" text-anchor="end" font-size="9" fill="#8A7E99">' + fmtY(vMin) + "</text>" +
      bars + ticks +
      (axisLabel ? '<text x="344" y="262" text-anchor="middle" font-size="10" fill="#8A7E99">' + axisLabel + "</text>" : "") +
      "</svg>";
  }
})();
