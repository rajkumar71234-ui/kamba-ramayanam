/* Kamba Ramayanam reading site.
 * One page; the part after # says what to show:
 *   #home            home page (also the default)
 *   #bala            list of padalams in Bala Kandam
 *   #bala-1          Bala Kandam, padalam 1 (0 = பாயிரம்)
 *   #bala-1-p16      ... opened at poem 16
 *   #bala-p480       poem 480, in whichever padalam holds it
 * Content comes from the JSON files in /data.
 */
(function () {
  "use strict";

  var app = document.getElementById("app");
  var META = null;
  var cache = {};

  // ---------- small helpers ----------
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  // **bold** marks the poem's own words inside the word-by-word meaning
  function rich(s) {
    return esc(s).replace(/\*\*([^*]+?)\*\*/g, "<b>$1</b>");
  }
  function plain(s) { return String(s == null ? "" : s).replace(/\*\*/g, ""); }
  function pad2(n) { return ("0" + n).slice(-2); }
  function getJSON(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " → " + r.status);
      return r.json();
    });
  }
  // Browser storage can be missing (private mode, embedded viewers): never let it break the page.
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem("kr:" + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("kr:" + k, JSON.stringify(v)); } catch (e) { /* ignore */ } }
  };
  // How the voice reads: speed (× the normal pace) and pitch (1 = the voice's own). Kept between visits.
  var SPEEDS = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.25, 1.5, 1.75, 2];
  var PITCHES = [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5];
  function nearest(list, v) {
    v = Number(v);
    if (!isFinite(v)) return 1;
    var best = list[0];
    for (var i = 0; i < list.length; i++) if (Math.abs(list[i] - v) < Math.abs(best - v)) best = list[i];
    return best;
  }
  var Voice = { speed: nearest(SPEEDS, store.get("speed", 1)), pitch: nearest(PITCHES, store.get("pitch", 1)) };
  function kandamOf(k) {
    for (var i = 0; i < META.kandams.length; i++) if (META.kandams[i].n === k) return META.kandams[i];
    return null;
  }
  function kandamBySlug(slug) {
    for (var i = 0; i < META.kandams.length; i++) if (META.kandams[i].slug === slug) return META.kandams[i];
    return null;
  }
  function padalamOf(kd, n) {
    var list = kd.padalams || [];
    for (var i = 0; i < list.length; i++) if (list[i].n === n) return list[i];
    return null;
  }
  function padalamOfPoem(kd, p) {
    var list = kd.padalams || [];
    for (var i = 0; i < list.length; i++) if (p >= list[i].from && p <= list[i].to) return list[i];
    return null;
  }
  function kandamLink(kd) { return "#" + kd.slug; }
  function padalamLink(kd, n, p) { return "#" + kd.slug + "-" + n + (p ? "-p" + p : ""); }
  function padalamLabel(pd) { return pd.n === 0 ? "பாயிரம்" : "படலம் " + pd.n; }
  function issueUrl(title, body) {
    var repo = META.site && META.site.repo;
    if (!repo) return null;
    return "https://github.com/" + repo + "/issues/new?title=" + encodeURIComponent(title) +
      "&body=" + encodeURIComponent(body);
  }
  function showError(msg) {
    app.innerHTML = '<div class="card error">பக்கத்தை ஏற்ற முடியவில்லை. ' + esc(msg) +
      ' <br><a href="#home">முகப்புக்குத் திரும்பு</a></div>';
  }
  function crumbs(items) {
    return '<nav class="crumbs" aria-label="வழி">' + items.map(function (it, i) {
      var sep = i ? '<span class="sep">›</span>' : "";
      return sep + (it.href ? '<a href="' + it.href + '">' + esc(it.text) + "</a>" : '<span class="here">' + esc(it.text) + "</span>");
    }).join("") + "</nav>";
  }
  // The bar that stays at the top while reading: where you are, and (on padalam pages) the reading controls.
  function topbar(items, extra) {
    return '<div class="topbar" id="topbar">' + crumbs(items) + (extra || "") + "</div>";
  }
  function controlsHtml() {
    function opts(list, cur, fmt) {
      return list.map(function (v) {
        return '<option value="' + v + '"' + (v === cur ? " selected" : "") + ">" + fmt(v) + "</option>";
      }).join("");
    }
    var h = '<div class="controls" role="toolbar" aria-label="படிக்கும், கேட்கும் அமைப்பு">';
    if (Speech.ok) {
      h += '<label class="ctl" title="குரல் படிக்கும் வேகம்"><span>வேகம்</span><select id="spSel">' +
        opts(SPEEDS, Voice.speed, function (v) { return v + "×"; }) + "</select></label>" +
        '<label class="ctl" title="குரலின் சுருதி (தாழ்வு / உயர்வு)"><span>சுருதி</span><select id="ptSel">' +
        opts(PITCHES, Voice.pitch, function (v) { return v.toFixed(1); }) + "</select></label>";
    }
    h += '<div class="seg" aria-label="எழுத்து அளவு"><button type="button" id="fsDown" aria-label="எழுத்தைச் சிறிதாக்கு">அ−</button>' +
      '<button type="button" id="fsUp" aria-label="எழுத்தைப் பெரிதாக்கு">அ+</button></div></div>';
    return h;
  }
  function setTitle(t) { document.title = t ? t + " · " + META.site.title : META.site.title + " — பாடல்கள், தமிழ் உரை, ஓவியங்கள்"; }

  // ---------- home ----------
  function renderHome() {
    setTitle("");
    var last = store.get("last", null);
    var lastKd = last ? kandamOf(last.k) : null;
    var lastPd = lastKd ? padalamOf(lastKd, last.n) : null;
    var bala = kandamOf(1);
    var html = '<section class="hero">' +
      "<h1>" + esc(META.site.title) + "</h1>" +
      '<p class="tag">' + esc(META.site.tagline) + "</p>" +
      "<p>கவிச்சக்கரவர்த்தி கம்பர் தமிழில் இயற்றிய இராமாவதாரம். ஒவ்வொரு படலத்துக்கும் கதைச் சுருக்கம், " +
      "எல்லாப் பாடல்களும் — ஒவ்வொன்றுக்கும் பதவுரை, விளக்கம் — காட்சி ஓவியங்கள், கேட்டு மகிழ ஒலி வசதி.</p>" +
      '<p class="note">கம்பர் வால்மீகியின் வழியில் நின்றாலும், கதையைத் தமிழ் மரபுக்கு ஏற்பப் பல இடங்களில் மாற்றியும் விரித்தும் பாடியுள்ளார். ' +
      (META.site.valmiki ? 'ஸம்ஸ்கிருத மூலத்தைப் படிக்க: <a href="' + esc(META.site.valmiki) + '">வால்மீகி ராமாயணம்</a>.' : "") + "</p>" +
      "</section>";

    if (lastKd && lastPd) {
      html += '<div class="card continue"><div><small>கடைசியாகப் படித்தது</small><br><b>' +
        esc(lastKd.ta) + " · " + esc(lastPd.title) + "</b>" + (last.p ? " — பாடல் " + esc(last.p) : "") +
        '</div><a class="btn" href="' + padalamLink(lastKd, lastPd.n, last.p) + '">தொடர்ந்து படிக்க</a></div>';
    }

    if (bala && bala.padalams && bala.padalams.length) {
      var f = bala.padalams[0];
      html += '<h2 class="section">இப்போது படிக்கலாம்</h2>' +
        '<a class="card feature" href="' + padalamLink(bala, f.n) + '">' +
        '<img src="img/1/' + pad2(f.n) + '/chapter.svg" alt="" width="800" height="500">' +
        '<div class="body"><div class="eyebrow">' + esc(bala.ta) + " · " + esc(padalamLabel(f)) + "</div>" +
        "<h3>" + esc(f.title) + "</h3><p>" + esc(f.summary || "") + "</p></div></a>";
    }

    html += '<h2 class="section">ஆறு காண்டங்கள்</h2><div class="kandams">';
    META.kandams.forEach(function (kd) {
      var ready = (kd.padalams || []).length;
      html += '<a class="card kandam-card' + (ready ? "" : " soon") + '" href="' + kandamLink(kd) + '">' +
        '<span class="num">' + kd.n + "</span><h3>" + esc(kd.ta) + "</h3>" +
        "<p>" + esc(kd.about) + "</p>" +
        '<div class="progress" aria-hidden="true"><i style="width:' + (ready ? 100 : 0) + '%"></i></div>' +
        '<div class="progress-label">' + (ready ? ready + " பகுதிகள் · " + kd.poems + " பாடல்கள் · படிக்கத் தயார்" : "விரைவில்") + "</div></a>";
    });
    html += "</div>";
    app.innerHTML = html;
  }

  // ---------- kandam ----------
  function renderKandam(kd) {
    setTitle(kd.ta);
    var list = kd.padalams || [];
    var html = topbar([{ text: "முகப்பு", href: "#home" }, { text: kd.ta }]) +
      '<h1 class="kandam-title">' + esc(kd.ta) + "</h1>" +
      "<p>" + esc(kd.about) + "</p>";
    if (!list.length) {
      app.innerHTML = html + '<div class="card error">இந்தக் காண்டம் இன்னும் தயாராகவில்லை — விரைவில் சேர்க்கப்படும்.</div>';
      return;
    }
    html += '<p class="legend">' + list.length + " பகுதிகள் (பாயிரம் + " + (list.length - 1) + " படலங்கள்) · " + kd.poems + " பாடல்கள்</p>" +
      '<form class="card goto" id="gotoForm"><label for="gotoNum">பாடல் எண்ணுக்குச் செல்ல</label>' +
      '<input id="gotoNum" type="number" inputmode="numeric" min="1" max="' + kd.poems + '" placeholder="1 – ' + kd.poems + '">' +
      '<button class="btn" type="submit">செல்</button></form>' +
      '<div class="padalams">';
    list.forEach(function (pd) {
      html += '<a class="card padalam-card" href="' + padalamLink(kd, pd.n) + '">' +
        '<img loading="lazy" src="img/' + kd.n + "/" + pad2(pd.n) + '/chapter.svg" alt="" width="800" height="500">' +
        '<div class="body"><div class="eyebrow">' + esc(padalamLabel(pd)) + " · பாடல் " + pd.from + "–" + pd.to + "</div>" +
        "<h3>" + esc(pd.title) + "</h3>" +
        (pd.summary ? "<p>" + esc(pd.summary) + "</p>" : "") +
        (pd.scenes ? '<span class="tagpill">காட்சி ஓவியங்களுடன்</span>' : "") + "</div></a>";
    });
    html += "</div>";
    app.innerHTML = html;
    document.getElementById("gotoForm").onsubmit = function (e) {
      e.preventDefault();
      var p = parseInt(document.getElementById("gotoNum").value, 10);
      var pd = padalamOfPoem(kd, p);
      if (pd) location.hash = padalamLink(kd, pd.n, p);
    };
  }

  // ---------- padalam ----------
  function neighbour(kd, n, step) {
    var list = kd.padalams || [];
    for (var i = 0; i < list.length; i++) {
      if (list[i].n === n) {
        var j = i + step;
        return j >= 0 && j < list.length ? list[j] : null;
      }
    }
    return null;
  }
  function pagerItem(kd, pd, label, cls) {
    if (!pd) return '<span class="' + cls + '"><small>' + label + "</small>—</span>";
    return '<a class="' + cls + '" href="' + padalamLink(kd, pd.n) + '"><small>' + label + "</small>" + esc(pd.title) + "</a>";
  }

  // One poem: its picture (right), number and ▶ button, the verse, then விளக்கம் — the பதவுரை first, then the explanation.
  function poemHtml(kd, d, it, metre) {
    var rep = issueUrl("பிழை: " + kd.ta + " பாடல் " + it.n,
      kd.ta + ", " + d.title + ", பாடல் " + it.n + "\n\nஎன்ன பிழை? (பாடல் / பதவுரை / விளக்கம் / ஓவியம்):\n\n");
    var lines = it.lines.map(function (l) { return '<span class="line">' + esc(l) + "</span>"; }).join("");
    var play = Speech.ok ? ' data-play="' + it.n + '"' : "";
    var notes = "";
    if (it.notes && it.notes.length) {
      notes = '<div class="notes">' + it.notes.map(function (x) {
        if (x.q) return '<p class="quote">' + x.q.map(function (l) { return '<span class="line">' + esc(l) + "</span>"; }).join("") + "</p>";
        return "<p>" + rich(x.p) + "</p>";
      }).join("") + "</div>";
    }
    var vil = "";
    if (it.pad || notes) {
      vil = '<section class="vil" aria-label="பாடல் ' + it.n + ' விளக்கம்"><h4 class="vil-head">விளக்கம்</h4>' +
        (it.pad ? '<div class="pad"><b class="lbl">பதவுரை</b>' + rich(it.pad) + "</div>" : "") + notes + "</section>";
    }
    return '<article class="card poem" id="p' + it.n + '">' +
      (it.pic ? '<figure class="poem-pic"' + play + '><img loading="lazy" decoding="async" src="' + esc(it.pic) + '" alt="' + esc(it.alt || "") +
        '" title="' + esc(it.alt || "") + '" width="240" height="240"></figure>' : "") +
      '<div class="poem-top"><span class="vnum">பாடல் ' + it.n + "</span>" +
      (Speech.ok ? '<button type="button" class="play-poem"' + play + ' aria-label="பாடல் ' + it.n + ' — பாடலும் விளக்கமும் கேட்க">' +
        ICON.play + '<span class="pp-t">கேட்க</span></button>' : "") +
      (metre ? '<span class="metre">' + esc(metre) + "</span>" : "") + "</div>" +
      '<p class="verse' + (it.lines.length === 8 ? " eight" : "") + '"' + play + ">" + lines + "</p>" +
      vil +
      '<div class="vtools"><button type="button" data-copy="' + it.n + '">இணைப்பை நகலெடு</button>' +
      (rep ? '<a href="' + rep + '" target="_blank" rel="noopener">பிழை தெரிவிக்க</a>' : "") + "</div></article>";
  }

  // Put every item (sub-heading, metre, poem) into the scene of the poem it leads to.
  function groupIntoScenes(d) {
    var scenes = (d.scenes || []).slice();
    var buckets = scenes.length ? scenes.map(function (sc) { return { scene: sc, items: [] }; }) : [{ scene: null, items: [] }];
    var pending = [];
    function bucketFor(n) {
      if (!scenes.length) return buckets[0];
      for (var i = 0; i < scenes.length; i++) if (n >= scenes[i].from && n <= scenes[i].to) return buckets[i];
      return buckets[buckets.length - 1];
    }
    d.items.forEach(function (it) {
      if (it.type !== "poem") { pending.push(it); return; }
      var b = bucketFor(it.n);
      b.items = b.items.concat(pending, [it]);
      pending = [];
    });
    if (pending.length) buckets[buckets.length - 1].items = buckets[buckets.length - 1].items.concat(pending);
    return buckets;
  }

  function renderPadalam(kd, pd, d, poem) {
    var label = padalamLabel(pd);
    setTitle(d.title);
    store.set("last", { k: kd.n, n: pd.n, p: poem || 0 });
    var poems = d.items.filter(function (it) { return it.type === "poem"; });

    var html = topbar([{ text: "முகப்பு", href: "#home" }, { text: kd.ta, href: kandamLink(kd) }, { text: d.title }], controlsHtml()) +
      '<header class="chap-head"><div class="eyebrow">' + esc(kd.ta) + " · " + esc(label) +
      " · பாடல் " + d.from + "–" + d.to + " (" + poems.length + ")</div><h1>" + esc(d.title) + "</h1>" +
      (d.subtitle ? '<p class="sub">' + esc(d.subtitle) + "</p>" : "") + "</header>" +
      '<figure class="card hero-fig"><img src="' + esc(d.chapter_image.src) + '" alt="' + esc(d.chapter_image.alt) +
      '" width="800" height="500"><figcaption>' + esc(d.chapter_image.alt) + "</figcaption></figure>" +
      '<section class="card story"><div class="story-head"><h2>கதைச் சுருக்கம்</h2>' +
      (Speech.ok ? '<button type="button" class="listen" id="listenStory">' + ICON.speaker + "கேட்க</button>" : "") + "</div>" +
      d.story.map(function (p, i) { return '<p id="sp' + i + '">' + esc(p) + "</p>"; }).join("") + "</section>";

    if (d.intro && d.intro.length) {
      html += '<details class="card intro"><summary>உரையாசிரியர் முன்னுரை</summary>' +
        d.intro.map(function (x) {
          return x.q ? '<p class="quote">' + x.q.map(function (l) { return '<span class="line">' + esc(l) + "</span>"; }).join("") + "</p>" : "<p>" + rich(x.p) + "</p>";
        }).join("") + "</details>";
    }

    if (Speech.ok) {
      html += '<button type="button" class="listen big" id="listenPoems">' + ICON.speaker + "எல்லாப் பாடல்களையும் விளக்கத்துடன் கேட்க</button>" +
        '<p class="listen-tip">எந்தப் பாடலையும் தொட்டால் (அல்லது ▶ கேட்க), அந்தப் பாடலும் அதன் விளக்கமும் படிக்கப்பட்டு, அடுத்த பாடல்களுக்குத் தானாகச் செல்லும்.</p>';
    }

    var metre = "";
    groupIntoScenes(d).forEach(function (b) {
      var sc = b.scene;
      if (sc) {
        html += '<section class="scene" id="scene' + sc.id + '"><div class="scene-head"><span class="badge">காட்சி ' + sc.id +
          "</span><h2>" + esc(sc.title) + '</h2><span class="range">பா. ' + sc.from + (sc.to > sc.from ? "–" + sc.to : "") + "</span></div>" +
          '<figure class="card scene-fig"><img loading="lazy" src="' + esc(sc.src) + '" alt="' + esc(sc.caption) +
          '" width="800" height="500"><figcaption>' + esc(sc.caption) + "</figcaption></figure>";
      } else {
        html += '<section class="scene plain">';
      }
      b.items.forEach(function (it) {
        if (it.type === "heading") html += '<h3 class="subhead">' + esc(it.text) + "</h3>";
        else if (it.type === "metre") metre = it.text;
        else { html += poemHtml(kd, d, it, metre); metre = ""; }
      });
      html += "</section>";
    });

    html += '<nav class="pager">' + pagerItem(kd, neighbour(kd, pd.n, -1), "← முந்தைய படலம்", "prev") +
      pagerItem(kd, neighbour(kd, pd.n, 1), "அடுத்த படலம் →", "next") + "</nav>";
    html += '<p class="legend">' + esc(d.source || "") + "</p>";

    app.innerHTML = html;
    wirePadalamControls(kd, pd, d);
    if (poem) {
      var el = document.getElementById("p" + poem);
      if (el) setTimeout(function () { el.scrollIntoView({ block: "start" }); }, 30);
    }
  }

  function applyFont(px) { document.documentElement.style.setProperty("--fs", px + "px"); }

  function wirePadalamControls(kd, pd, d) {
    var fs = store.get("fs", 17);
    applyFont(fs);
    document.getElementById("fsUp").onclick = function () { fs = Math.min(24, fs + 1); applyFont(fs); store.set("fs", fs); };
    document.getElementById("fsDown").onclick = function () { fs = Math.max(14, fs - 1); applyFont(fs); store.set("fs", fs); };
    var sp = document.getElementById("spSel"), pt = document.getElementById("ptSel");
    if (sp) sp.onchange = function () { Voice.speed = nearest(SPEEDS, sp.value); store.set("speed", Voice.speed); Player.refresh(); };
    if (pt) pt.onchange = function () { Voice.pitch = nearest(PITCHES, pt.value); store.set("pitch", Voice.pitch); Player.refresh(); };
    var ls = document.getElementById("listenStory");
    if (ls) ls.onclick = function () { Player.start("story", d, 0); };
    var lp = document.getElementById("listenPoems");
    if (lp) lp.onclick = function () { Player.start("poems", d, 0); };
    app.onclick = function (e) {
      var pl = e.target.closest("[data-play]");
      if (pl) {
        // a tap that ends a text selection is not a request to listen
        var sel = window.getSelection ? String(window.getSelection()) : "";
        if (sel && !pl.classList.contains("play-poem")) return;
        var n = parseInt(pl.getAttribute("data-play"), 10);
        if (Player.isOn("poems", n)) Player.toggle();
        else Player.start("poems", d, Player.groupOfPoem(d, n));
        return;
      }
      var b = e.target.closest("button[data-copy]"); if (!b) return;
      var url = location.href.split("#")[0] + padalamLink(kd, pd.n, b.getAttribute("data-copy"));
      var original = b.textContent;
      var say = function (t) { b.textContent = t; setTimeout(function () { b.textContent = original; }, 1800); };
      try {
        navigator.clipboard.writeText(url).then(function () { say("நகலெடுக்கப்பட்டது ✓"); },
          function () { say(url); });
      } catch (err) { say(url); }
    };
  }

  // ---------- read aloud (the phone's / browser's own text-to-speech voice) ----------
  var ICON = {
    speaker: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.6 6a8.6 8.6 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    speakerSm: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>',
    play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
    pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>',
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h2.4v14H6zM20 5v14L9 12z"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15.6 5H18v14h-2.4zM4 5v14l11-7z"/></svg>',
    stop: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.5 6.5h11v11h-11z"/></svg>'
  };

  var Speech = (function () {
    var synth = window.speechSynthesis;
    var ok = !!(synth && window.SpeechSynthesisUtterance);
    var voices = [];
    function load() { try { voices = synth.getVoices() || []; } catch (e) { voices = []; } }
    if (ok) {
      load();
      try { synth.addEventListener("voiceschanged", load); } catch (e) { synth.onvoiceschanged = load; }
    }
    // Pick the best Tamil voice: natural/neural voices first (Edge), then online ones, then any.
    function voiceFor(prefix) {
      load();
      var best = null, bestScore = -1;
      for (var i = 0; i < voices.length; i++) {
        var v = voices[i], l = String(v.lang || "").toLowerCase().replace(/_/g, "-");
        if (!(l === prefix || l.indexOf(prefix + "-") === 0)) continue;
        var score = (/natural|neural/i.test(v.name) ? 4 : 0) + (/online|google/i.test(v.name) ? 2 : 0) + (l === prefix + "-in" ? 1 : 0);
        if (score > bestScore) { best = v; bestScore = score; }
      }
      return best;
    }
    return { ok: ok, synth: synth, voiceFor: voiceFor };
  })();

  // Text clean-up so the voice reads naturally
  function ttsTamil(t) {
    return plain(t).replace(/[‘’“”"]/g, "").replace(/\s+-\s*|\s*-\s+/g, ", ").replace(/\(\s*\)/g, "")
      .replace(/\s+/g, " ").trim();
  }
  function sentences(t) {
    var parts = String(t).match(/[^.!?;—]+[.!?;—]*\s*/g) || [String(t)];
    var out = [];
    parts.forEach(function (p) {
      p = p.trim();
      if (!p) return;
      if (out.length && p.length < 12) out[out.length - 1] += " " + p; else out.push(p);
    });
    return out;
  }

  function noTamilVoiceTip() {
    var ua = navigator.userAgent || "";
    var base = "இந்தக் கருவியில் தமிழ்க் குரல் இல்லை. ";
    if (/Android/i.test(ua)) return base + "Settings → Google Text-to-speech → தமிழ் (Tamil) குரலைப் பதிவிறக்கவும்.";
    if (/iPhone|iPad|iPod/i.test(ua)) return base + "Settings → Accessibility → Spoken Content → Voices → Tamil குரலைப் பதிவிறக்கவும்.";
    if (/Edg\//.test(ua)) return base + "Windows Settings → Time & language → Speech → Tamil குரலைச் சேர்க்கவும்.";
    return base + "கணினியில் Microsoft Edge உலாவியில் திறந்தால் தமிழ்க் குரல் கிடைக்கும்.";
  }

  var Player = (function () {
    var st = { items: [], groups: [], i: 0, playing: false, paused: false, cur: null, title: "", errors: 0, note: "", mode: "", lastG: -1 };
    var bar = null;
    function $(id) { return document.getElementById(id); }

    function ensureBar() {
      if (bar) return;
      bar = document.createElement("div");
      bar.className = "player"; bar.id = "player"; bar.hidden = true;
      bar.setAttribute("role", "region"); bar.setAttribute("aria-label", "ஒலி இயக்கி");
      bar.innerHTML = '<div class="pl-info"><b id="plTitle"></b><span id="plPos"></span><span id="plMsg" class="pl-msg"></span></div>' +
        '<div class="pl-btns">' +
        '<button type="button" id="plPrev" aria-label="முந்தையது">' + ICON.prev + "</button>" +
        '<button type="button" id="plPlay" class="pl-main" aria-label="இடைநிறுத்து">' + ICON.pause + "</button>" +
        '<button type="button" id="plNext" aria-label="அடுத்தது">' + ICON.next + "</button>" +
        '<button type="button" id="plStop" aria-label="நிறுத்து">' + ICON.stop + "</button></div>";
      document.body.appendChild(bar);
      $("plPrev").onclick = prev;
      $("plNext").onclick = next;
      $("plStop").onclick = stop;
      $("plPlay").onclick = function () { if (st.paused) resume(); else pause(); };
    }

    // What is read, in order. For each poem: its number, the poem, then விளக்கம் — the பதவுரை and the explanation —
    // and then straight on to the next poem.
    function build(mode, d) {
      st.items = []; st.groups = []; st.mode = mode;
      var ta = Speech.voiceFor("ta");
      st.note = ta ? "" : noTamilVoiceTip();
      function add(g, text, rate) {
        if (text && String(text).trim()) st.items.push({ g: g, text: String(text).trim(), lang: "ta-IN", voice: ta, rate: rate });
      }
      if (mode === "story") {
        st.title = "கதைச் சுருக்கம்";
        d.story.forEach(function (p, gi) {
          st.groups.push({ id: "sp" + gi, n: gi, start: st.items.length, label: "பகுதி " + (gi + 1) + " / " + d.story.length });
          sentences(ttsTamil(p)).forEach(function (x) { add(gi, x, 0.95); });
        });
      } else {
        st.title = d.title + " — பாடலும் விளக்கமும்";
        var poems = d.items.filter(function (it) { return it.type === "poem"; });
        poems.forEach(function (it, gi) {
          st.groups.push({ id: "p" + it.n, n: it.n, start: st.items.length, label: "பாடல் " + it.n + " (" + (gi + 1) + " / " + poems.length + ")" });
          add(gi, "பாடல் " + it.n + ".", 0.95);
          it.lines.forEach(function (l) { add(gi, ttsTamil(l), 0.82); });
          var hasNotes = it.notes && it.notes.length;
          if (it.pad || hasNotes) add(gi, "விளக்கம்.", 0.95);
          if (it.pad) {
            add(gi, "பதவுரை.", 0.95);
            sentences(ttsTamil(it.pad)).forEach(function (x) { add(gi, x, 0.95); });
          }
          if (hasNotes) {
            it.notes.forEach(function (n) {
              if (n.q) n.q.forEach(function (l) { add(gi, ttsTamil(l), 0.85); });
              else sentences(ttsTamil(n.p)).forEach(function (x) { add(gi, x, 0.95); });
            });
          }
        });
      }
    }

    function groupOf(i) { return st.items[i] ? st.items[i].g : -1; }
    function groupStart(g) { return st.groups[g] ? st.groups[g].start : st.items.length; }
    function msg(t) { if ($("plMsg")) $("plMsg").textContent = t || ""; }

    function show() {
      var g = groupOf(st.i);
      var fresh = g !== st.lastG;
      st.lastG = g;
      var old = document.querySelectorAll(".speaking");
      for (var k = 0; k < old.length; k++) old[k].classList.remove("speaking");
      var el = st.groups[g] ? document.getElementById(st.groups[g].id) : null;
      if (el) {
        el.classList.add("speaking");
        var tb = document.getElementById("topbar");
        var top = tb ? tb.getBoundingClientRect().bottom : 0;
        var r = el.getBoundingClientRect();
        // bring a newly started poem into view, below the top bar
        if (fresh && (r.top < top + 4 || r.top > window.innerHeight - 160)) {
          window.scrollBy({ top: r.top - top - 12, behavior: "smooth" });
        }
      }
      $("plTitle").textContent = st.title;
      $("plPos").textContent = st.groups[g] ? st.groups[g].label : "";
      var b = $("plPlay");
      b.innerHTML = st.paused ? ICON.play : ICON.pause;
      b.setAttribute("aria-label", st.paused ? "தொடர்ந்து கேட்க" : "இடைநிறுத்து");
    }

    function cancelNow() {
      st.cur = null;
      try { Speech.synth.cancel(); } catch (e) { /* ignore */ }
    }

    function speakCurrent() {
      if (!st.playing || st.paused) return;
      if (st.i >= st.items.length) { stop(); return; }
      show();
      var it = st.items[st.i];
      var u = new SpeechSynthesisUtterance(it.text);
      u.lang = it.lang;
      if (it.voice) u.voice = it.voice;
      u.rate = Math.max(0.1, Math.min(10, (it.rate || 1) * Voice.speed));
      u.pitch = Math.max(0, Math.min(2, Voice.pitch));
      u.onend = function () {
        if (u !== st.cur || !st.playing || st.paused) return;
        st.errors = 0;
        st.i++;
        speakCurrent();
      };
      u.onerror = function (e) {
        if (u !== st.cur) return;
        var er = e && e.error;
        if (er === "interrupted" || er === "canceled") return;
        st.errors++;
        if (st.errors >= 3) { msg("குரலை இயக்க முடியவில்லை. " + st.note); st.paused = true; st.cur = null; show(); return; }
        st.i++;
        setTimeout(speakCurrent, 150);
      };
      st.cur = u;
      try { Speech.synth.speak(u); } catch (e) { msg("குரலை இயக்க முடியவில்லை."); }
    }

    function go(i) {
      cancelNow();
      st.i = Math.max(0, Math.min(i, st.items.length - 1));
      st.paused = false;
      setTimeout(speakCurrent, 80);
    }

    function start(mode, d, fromGroup) {
      if (!Speech.ok) return;
      ensureBar();
      cancelNow();
      build(mode, d);
      st.playing = true; st.paused = false; st.errors = 0; st.lastG = -1;
      st.i = groupStart(Math.max(0, Math.min(fromGroup || 0, st.groups.length - 1)));
      bar.hidden = false;
      document.body.classList.add("has-player");
      msg(st.note);
      show();
      setTimeout(speakCurrent, 80);
    }
    function pause() { if (!st.playing) return; st.paused = true; cancelNow(); show(); }
    function resume() { if (!st.playing) return; st.paused = false; show(); setTimeout(speakCurrent, 80); }
    function prev() { if (!st.playing) return; var g = groupOf(st.i); go(groupStart(Math.max(0, g - 1))); }
    function next() {
      if (!st.playing) return;
      var g = groupOf(st.i);
      if (g + 1 < st.groups.length) go(groupStart(g + 1)); else stop();
    }
    function stop() {
      st.playing = false; st.paused = false;
      cancelNow();
      var old = document.querySelectorAll(".speaking");
      for (var k = 0; k < old.length; k++) old[k].classList.remove("speaking");
      if (bar) bar.hidden = true;
      document.body.classList.remove("has-player");
    }
    function groupOfPoem(d, n) {
      var poems = d.items.filter(function (it) { return it.type === "poem"; });
      for (var i = 0; i < poems.length; i++) if (poems[i].n === n) return i;
      return 0;
    }
    // new speed / pitch: say the current sentence again with the new setting
    function refresh() {
      if (!st.playing || st.paused) return;
      cancelNow();
      setTimeout(speakCurrent, 60);
    }
    function isOn(mode, n) {
      if (!st.playing || st.mode !== mode) return false;
      var g = st.groups[groupOf(st.i)];
      return !!g && g.n === n;
    }
    function toggle() { if (st.paused) resume(); else pause(); }
    return { start: start, stop: stop, pause: pause, resume: resume, prev: prev, next: next, groupOfPoem: groupOfPoem,
      refresh: refresh, isOn: isOn, toggle: toggle, state: st };
  })();
  window.__player = Player;

  // ---------- router ----------
  function route() {
    Player.stop();
    var h = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (!h || h === "home") { renderHome(); window.scrollTo(0, 0); return; }
    var m = h.match(/^([a-z]+)(?:-(\d+))?(?:-p(\d+))?$/);
    var kd = m ? kandamBySlug(m[1]) : null;
    if (!kd) { renderHome(); window.scrollTo(0, 0); return; }
    var poem = m[3] ? parseInt(m[3], 10) : 0;
    var pd = null;
    if (m[2] != null) pd = padalamOf(kd, parseInt(m[2], 10));
    else if (poem) pd = padalamOfPoem(kd, poem);
    if (!pd) { renderKandam(kd); window.scrollTo(0, 0); return; }
    var key = kd.n + "/" + pad2(pd.n);
    var go = function (d) { renderPadalam(kd, pd, d, poem); if (!poem) window.scrollTo(0, 0); };
    if (cache[key]) return go(cache[key]);
    app.innerHTML = '<div class="loading">ஏற்றுகிறது…</div>';
    getJSON("data/" + key + ".json").then(function (d) { cache[key] = d; go(d); }).catch(function (e) { showError(e.message); });
  }

  // back-to-top button
  var topBtn = document.querySelector(".to-top");
  if (topBtn) {
    window.addEventListener("scroll", function () { topBtn.classList.toggle("show", window.scrollY > 900); }, { passive: true });
    topBtn.addEventListener("click", function () { window.scrollTo(0, 0); });
  }

  getJSON("data/kandams.json").then(function (meta) {
    META = meta;
    window.addEventListener("hashchange", route);
    route();
  }).catch(function (e) { showError(e.message); });
})();
