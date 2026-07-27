/* ==========================================================================
   TrueMath site.js
   Consolidated behaviors. Each block is guarded by element-presence checks
   so the script is safe to load on every page.
   ========================================================================== */

(function () {
  'use strict';

  /* ---------- Hamburger / mobile menu ---------- */
  (function initHamburger() {
    const hamburger = document.getElementById('navHamburger');
    const menu = document.getElementById('mobileMenu');
    if (!hamburger || !menu) return;

    function setOpen(open) {
      hamburger.classList.toggle('is-open', open);
      menu.classList.toggle('is-open', open);
      hamburger.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      hamburger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    hamburger.addEventListener('click', function () {
      setOpen(!hamburger.classList.contains('is-open'));
    });

    menu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setOpen(false); });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && hamburger.classList.contains('is-open')) setOpen(false);
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth > 960 && hamburger.classList.contains('is-open')) setOpen(false);
    });
  })();

  /* ---------- Home: hero domain rotator pill ---------- */
  (function initDomainRotator() {
    const pill = document.getElementById('carousel-pill');
    if (!pill) return;

    const domains = [
      'Financial Advisor', 'Estate Planner', 'Business Valuation Analyst',
      'M&A Advisor', 'Private Capital Investor',
      'Corporate Finance Analyst',
      'Real Estate Investor', 'Residential Real Estate Agent', 'Residential Mortgage Broker', 'CRE Acquisitions Analyst',
      'Contractor Estimator',
      'Solution Architect', 'Sales Engineer', 'Revenue Operations Analyst',
      'Commercial Lines Underwriter', 'Reinsurance Treaty Analyst',
      'Divorce Financial Analyst', 'Forensic Accountant',
      'Medical Practice Manager', 'Clinical Trial Manager',
      'and more on the way'
    ];

    let index = 0;
    function showDomain(i) {
      pill.style.opacity = '0';
      pill.style.transform = 'translateY(5px)';
      setTimeout(function () {
        pill.textContent = domains[i];
        if (i === domains.length - 1) {
          pill.style.fontStyle = 'italic';
          pill.style.opacity = '0.75';
        } else {
          pill.style.fontStyle = 'normal';
          pill.style.opacity = '1';
        }
        pill.style.transform = 'translateY(0)';
      }, 200);
    }
    showDomain(0);
    setInterval(function () {
      index = (index + 1) % domains.length;
      showDomain(index);
    }, 1000);
  })();

  /* ---------- Home: vignette carousel ---------- */
  (function initVignetteCarousel() {
    const track = document.getElementById('track');
    const dotsContainer = document.getElementById('dots');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const pauseBtn = document.getElementById('pause-btn');
    const pauseIcon = document.getElementById('pause-icon');
    const playIcon = document.getElementById('play-icon');
    if (!track || !dotsContainer || !prevBtn || !nextBtn || !pauseBtn) return;

    const originals = Array.from(track.children);
    const total = originals.length;
    if (!total) return;
    const cloneCount = 3;

    for (let i = 0; i < cloneCount; i++) {
      track.appendChild(originals[i % total].cloneNode(true));
    }
    for (let i = cloneCount - 1; i >= 0; i--) {
      track.insertBefore(originals[total - 1 - (i % total)].cloneNode(true), track.firstChild);
    }

    const allCards = Array.from(track.children);

    let rawPos = cloneCount;
    let isPaused = false;
    let autoTimer = null;
    let transitioning = false;

    originals.forEach(function (_, i) {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
      dot.addEventListener('click', function () {
        if (transitioning) return;
        rawPos = cloneCount + i;
        setPos(true);
        updateDots();
        if (!isPaused) { stopAuto(); startAuto(); }
      });
      dotsContainer.appendChild(dot);
    });

    function cardWidth() { return allCards[0].offsetWidth + 28; }

    function setPos(animated) {
      track.style.transition = animated
        ? 'transform 0.55s cubic-bezier(0.4, 0, 0.2, 1)'
        : 'none';
      track.style.transform = 'translateX(-' + (rawPos * cardWidth()) + 'px)';
      if (animated) transitioning = true;
    }

    function updateDots() {
      const logical = ((rawPos - cloneCount) % total + total) % total;
      dotsContainer.querySelectorAll('.carousel-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === logical);
      });
    }

    track.addEventListener('transitionend', function () {
      transitioning = false;
      if (rawPos >= cloneCount + total) {
        rawPos -= total;
        setPos(false);
      } else if (rawPos < cloneCount) {
        rawPos += total;
        setPos(false);
      }
      updateDots();
    });

    function advance(dir) {
      if (transitioning) return;
      rawPos += dir;
      setPos(true);
      updateDots();
    }

    function startAuto() {
      if (autoTimer) clearInterval(autoTimer);
      autoTimer = setInterval(function () { advance(1); }, 2000);
    }

    function stopAuto() {
      clearInterval(autoTimer);
      autoTimer = null;
    }

    pauseBtn.addEventListener('click', function () {
      isPaused = !isPaused;
      if (pauseIcon) pauseIcon.style.display = isPaused ? 'none' : 'block';
      if (playIcon) playIcon.style.display = isPaused ? 'block' : 'none';
      pauseBtn.classList.toggle('active', isPaused);
      if (isPaused) stopAuto(); else startAuto();
    });

    prevBtn.addEventListener('click', function () { advance(-1); if (!isPaused) { stopAuto(); startAuto(); } });
    nextBtn.addEventListener('click', function () { advance(1); if (!isPaused) { stopAuto(); startAuto(); } });

    track.addEventListener('mouseenter', function () { if (!isPaused) stopAuto(); });
    track.addEventListener('mouseleave', function () { if (!isPaused) startAuto(); });

    let touchStart = 0;
    track.addEventListener('touchstart', function (e) { touchStart = e.touches[0].clientX; if (!isPaused) stopAuto(); }, { passive: true });
    track.addEventListener('touchend', function (e) {
      const diff = touchStart - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) advance(diff > 0 ? 1 : -1);
      if (!isPaused) startAuto();
    });

    setPos(false);
    updateDots();
    startAuto();
  })();

  /* ---------- FAQ: sidebar active section observer ---------- */
  (function initFaqSidebar() {
    const sections = document.querySelectorAll('.faq-section');
    const sidebarLinks = document.querySelectorAll('.faq-sidebar-links a');
    if (!sections.length || !sidebarLinks.length) return;

    function setActive(id) {
      sidebarLinks.forEach(function (link) {
        if (link.dataset.section === id) link.classList.add('active');
        else link.classList.remove('active');
      });
    }

    // Clicking a sidebar link while a search is active hides the target
    // section. Clear the search first so the anchor jump resolves.
    sidebarLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        const input = document.getElementById('faq-search');
        if (input && input.value) {
          input.value = '';
          input.dispatchEvent(new Event('input', { bubbles: true }));
        }
      });
    });

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { rootMargin: '-20% 0px -70% 0px', threshold: 0 });

    sections.forEach(function (section) { observer.observe(section); });
  })();

  /* ---------- FAQ: open card/section from URL hash ---------- */
  (function initFaqHashOpen() {
    if (!window.location.hash) return;
    const target = document.querySelector(window.location.hash);
    if (!target) return;
    if (target.classList.contains('faq-section')) {
      target.querySelectorAll('.faq-card').forEach(function (card) { card.setAttribute('open', ''); });
    } else if (target.classList.contains('faq-card')) {
      target.setAttribute('open', '');
    }
  })();

  /* ---------- FAQ: search filter ---------- */
  (function initFaqSearch() {
    const input = document.getElementById('faq-search');
    const clearBtn = document.getElementById('faq-search-clear');
    const shortcut = document.getElementById('faq-search-shortcut');
    const noResults = document.getElementById('faq-no-results');
    const cards = document.querySelectorAll('.faq-card');
    const sections = document.querySelectorAll('.faq-section');
    if (!input || !cards.length) return;

    const cardOriginalOpen = new WeakMap();
    cards.forEach(function (card) { cardOriginalOpen.set(card, card.hasAttribute('open')); });

    function filter(query) {
      const q = query.trim().toLowerCase();
      const hasQuery = q.length > 0;

      if (clearBtn) clearBtn.classList.toggle('visible', hasQuery);
      if (shortcut) shortcut.classList.toggle('hidden', hasQuery);

      if (!hasQuery) {
        cards.forEach(function (card) {
          card.classList.remove('search-hidden');
          if (cardOriginalOpen.get(card)) card.setAttribute('open', '');
          else card.removeAttribute('open');
        });
        sections.forEach(function (s) { s.classList.remove('search-hidden'); });
        if (noResults) noResults.classList.remove('visible');
        return;
      }

      let totalMatches = 0;
      cards.forEach(function (card) {
        const summary = card.querySelector('.faq-question');
        const answer = card.querySelector('.faq-answer');
        const haystack = ((summary ? summary.textContent : '') + ' ' + (answer ? answer.textContent : '')).toLowerCase();
        const matches = haystack.includes(q);
        card.classList.toggle('search-hidden', !matches);
        if (matches) {
          totalMatches++;
          card.setAttribute('open', '');
        }
      });

      sections.forEach(function (section) {
        const sectionCards = section.querySelectorAll('.faq-card');
        const anyVisible = Array.from(sectionCards).some(function (c) { return !c.classList.contains('search-hidden'); });
        section.classList.toggle('search-hidden', !anyVisible);
      });

      if (noResults) noResults.classList.toggle('visible', totalMatches === 0);
    }

    input.addEventListener('input', function (e) { filter(e.target.value); });

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        input.value = '';
        filter('');
        input.focus();
      });
    }

    document.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        input.focus();
        input.select();
      } else if (e.key === 'Escape' && document.activeElement === input) {
        if (input.value) {
          input.value = '';
          filter('');
        } else {
          input.blur();
        }
      }
    });

    if (shortcut && !/Mac|iPhone|iPad/.test(navigator.platform)) {
      shortcut.textContent = 'Ctrl K';
    }
  })();

  /* ---------- Video playlist ----------
     Progressive enhancement for the .tmp-player widget (see
     _includes/video-player.html). Without JS/SDK the Stream iframe still plays
     the first clip and the rail links to each clip's watch page. When Cloudflare's
     player SDK is present we drive it: click a clip to play it, "Play all" runs
     the set in order, "Shuffle" runs a random order, and each clip auto-advances
     to the next via the Stream player's `ended` event. Supports multiple players
     on one page. */
  (function initVideoPlaylists() {
    if (typeof window.Stream !== 'function') return;   // Cloudflare Stream SDK required
    const players = document.querySelectorAll('[data-video-playlist]');
    if (!players.length) return;
    document.body.classList.add('tmp-js');
    Array.prototype.forEach.call(players, setupPlayer);

    function setupPlayer(player) {
      const frame = player.querySelector('.tmp-frame iframe');
      const now = player.querySelector('.tmp-now');
      const rails = Array.prototype.slice.call(player.querySelectorAll('.tmp-list'));
      if (!frame || !rails.length) return;

      const customer = player.getAttribute('data-stream-customer');
      const tabs = Array.prototype.slice.call(player.querySelectorAll('.tmp-tab'));
      const btnAll = player.querySelector('[data-action="playall"]');
      const btnShuffle = player.querySelector('[data-action="shuffle"]');

      let items = [];        // the active group's clips (rebuilt on each tab switch)
      let order = [];        // indices still to play in the running sequence
      let advancing = false; // guards against a doubled 'ended' after re-wiring
      let ctrl = null;       // current Stream controller (recreated on each load)

      function buildItems(rail) {
        return Array.prototype.slice.call(rail.querySelectorAll('.tmp-link')).map(function (a) {
          return { uid: a.getAttribute('data-uid'), title: a.getAttribute('data-title') || '', link: a };
        });
      }

      function setMode(btn) {
        [btnAll, btnShuffle].forEach(function (b) { if (b) b.classList.toggle('is-active', b === btn); });
      }

      function highlight(i) {
        player.querySelectorAll('.tmp-link').forEach(function (a) { a.removeAttribute('aria-current'); });
        if (i >= 0 && items[i]) items[i].link.setAttribute('aria-current', 'true');
        if (now) {
          now.innerHTML = i >= 0 && items[i]
            ? '<span class="tmp-now-idx">' + (i + 1) + '/' + items.length + '</span> · ' + items[i].title
            : '';
        }
      }

      function embedUrl(uid, autoplay) {
        return 'https://' + customer + '.cloudflarestream.com/' + uid +
               '/iframe?preload=metadata' + (autoplay ? '&autoplay=true' : '');
      }

      function onEnded() {
        if (advancing) return;         // one advance per clip end
        advancing = true;
        if (order.length) load(order.shift(), true);
        else { setMode(null); highlight(-1); }
      }

      // (Re)bind a Stream controller to the (reloaded) iframe so `ended` keeps
      // firing for auto-advance. The old controller is destroyed first so we
      // don't stack duplicate listeners.
      function bind() {
        if (ctrl && ctrl.destroy) { try { ctrl.destroy(); } catch (e) {} }
        ctrl = window.Stream(frame);
        ctrl.addEventListener('ended', onEnded);
      }

      // Swap the clip by pointing the iframe at a fresh Stream embed URL — the
      // reliable way to change videos (the SDK's in-place src setter is flaky).
      function load(i, autoplay) {
        const it = items[i];
        if (!it) return;
        advancing = false;
        frame.src = embedUrl(it.uid, autoplay);
        highlight(i);
        bind();
      }

      function playSequence(seq, btn) {
        order = seq;
        setMode(btn);
        const next = order.shift();
        if (next != null) load(next, true);
      }

      // Switch the active tab/group: reveal its rail, rebuild `items`, cancel any
      // running sequence. On init we keep the server-rendered iframe; on a user
      // tab click we swap the stage to that group's first clip (paused).
      function activateGroup(gi, opts) {
        opts = opts || {};
        rails.forEach(function (r, ri) { r.hidden = ri !== gi; });
        tabs.forEach(function (t, ti) {
          const on = ti === gi;
          t.classList.toggle('is-active', on);
          t.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        items = buildItems(rails[gi]);
        order = [];
        setMode(null);
        if (opts.init) { if (tabs.length) highlight(0); bind(); }
        else load(0, false);
      }

      // Clicks are delegated so they keep working after the active rail swaps.
      player.addEventListener('click', function (e) {
        const link = e.target.closest ? e.target.closest('.tmp-link') : null;
        if (!link || !player.contains(link)) return;
        e.preventDefault();
        for (let i = 0; i < items.length; i++) {
          if (items[i].link === link) { order = []; setMode(null); load(i, true); break; }
        }
      });

      tabs.forEach(function (t, ti) {
        t.addEventListener('click', function () { activateGroup(ti, {}); });
      });

      if (btnAll) btnAll.addEventListener('click', function () {
        playSequence(items.map(function (_, i) { return i; }), btnAll);
      });

      if (btnShuffle) btnShuffle.addEventListener('click', function () {
        const idx = items.map(function (_, i) { return i; });
        for (let j = idx.length - 1; j > 0; j--) {           // Fisher–Yates
          const k = Math.floor(Math.random() * (j + 1));
          const t = idx[j]; idx[j] = idx[k]; idx[k] = t;
        }
        playSequence(idx, btnShuffle);
      });

      activateGroup(0, { init: true });   // first group active, server iframe kept
    }
  })();

})();
