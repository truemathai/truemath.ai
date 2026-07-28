/* TrueMath multi-domain demo viewer (beta page only).
   Adds the domain dropdown + prompt-chip picker on top of the shared demo
   frame. The reveal/chart engine lives in vertical-demo.js (loaded first); this
   file only chooses which frame is on screen. Progressive enhancement: with no
   JS every frame is visible and this never runs — vertical-demo.js has already
   added `tmv-js` to <body>, which is what collapses the page to one frame. */
(function () {
  "use strict";

  var select = document.getElementById("tmvDomain");
  if (!select) return;

  var chips = Array.prototype.slice.call(document.querySelectorAll(".tmv-chip"));
  var groups = Array.prototype.slice.call(document.querySelectorAll(".tmv-chipgroup"));
  var frames = Array.prototype.slice.call(document.querySelectorAll(".tmv-vframe"));

  /* Show one demo: highlight its chip, reveal only its frame, and open that
     frame's launcher so the (JS-collapsed) body shows. Demo ids are unique
     across every domain, so matching on the demo id alone is safe. */
  function selectDemo(demo) {
    chips.forEach(function (c) { c.classList.toggle("is-active", c.dataset.demo === demo); });
    frames.forEach(function (f) {
      var on = f.dataset.demo === demo;
      f.classList.toggle("is-active", on);
      var launcher = f.querySelector(".tmv-launcher");
      if (launcher) launcher.classList.toggle("open", on);
    });
  }

  /* Switch domains: show that domain's chip group, then select its first
     question so a frame is always on screen. */
  function selectDomain(domain) {
    groups.forEach(function (g) { g.classList.toggle("is-active", g.dataset.domain === domain); });
    var first = document.querySelector('.tmv-chip[data-domain="' + domain + '"]');
    if (first) selectDemo(first.dataset.demo);
  }

  select.addEventListener("change", function () { selectDomain(select.value); });
  chips.forEach(function (c) {
    c.addEventListener("click", function () { selectDemo(c.dataset.demo); });
  });

  selectDomain(select.value);
})();
