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
      }, reduce ? 0 : 850);
    });
  });

  /* fade the result's steps in one at a time, then the final answer */
  function revealSteps(launcher) {
    var scroll = launcher.querySelector(".tmv-scroll");
    var steps = launcher.querySelector(".tmv-steps");
    var items = steps ? Array.prototype.slice.call(steps.children) : [];
    var finalEl = launcher.querySelector(".tmv-finalwrap");
    if (reduce) { if (scroll) scroll.scrollTop = scroll.scrollHeight; return; }

    items.forEach(function (el) { el.style.opacity = "0"; el.style.transition = "opacity .28s ease"; });
    if (finalEl) { finalEl.style.opacity = "0"; finalEl.style.transition = "opacity .28s ease"; }

    var i = 0;
    (function next() {
      if (i < items.length) {
        items[i].style.opacity = "1";
        if (scroll) scroll.scrollTop = scroll.scrollHeight;
        i++;
        setTimeout(next, 460);
      } else if (finalEl) {
        finalEl.style.opacity = "1";
        if (scroll) scroll.scrollTop = scroll.scrollHeight;
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

  /* Build an auto-scaled bar chart. `data` is any array of numbers; the axis
     bounds, zero line, ticks and labels are all derived from the data. */
  function buildChart(data, axisLabel) {
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
