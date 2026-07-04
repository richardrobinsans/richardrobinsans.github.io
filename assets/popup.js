/* 1xCasino popup system — self-contained. Подключается строкой в <head>:
   <script src="/assets/popup.js" data-popup="main_v1" defer></script>
   Вариант берётся из data-popup, язык — из <html lang>, гео — из [data-geo="country"]
   уже на странице (его переписывает Cloudflare Worker). Итерации попапа = правка
   только этого файла, без регенерации страниц. */
(function () {
  "use strict";

  var EMOJI = ["🥳", "🙂", "🙁", "😢", "🤑"];

  var TXT = {
    en: {
      h: "Spin the wheel — grab your bonus!",
      segs: ["95 FS", "80 FS", "20 FS", "0 FS", "1 more chance"],
      stop: "⏹ Stop", again: "▶ Try Again",
      note1: "🤑 Try 1 more chance!", note2: "🥳 You get 95 FS!",
      r_h: "Congratulations!",
      r_pre: "You are a few steps away from your bonus! Just install our native 1xCasino app for ",
      r_geo: "your country",
      r_post: " > Log in > Check that your personal data is filled in > Get your bonus!",
      get: "Get my Bonus", no: "I don\u2019t want the Bonus", close: "Close"
    },
    fr: {
      h: "Fais tourner la roue — récupère ton bonus !",
      segs: ["95 FS", "80 FS", "20 FS", "0 FS", "1 chance de plus"],
      stop: "⏹ Stop", again: "▶ Réessayer",
      note1: "🤑 1 chance de plus !", note2: "🥳 Tu gagnes 95 FS !",
      r_h: "Félicitations !",
      r_pre: "Ton bonus est à quelques étapes ! Installe notre application native 1xCasino pour ",
      r_geo: "ton pays",
      r_post: " > Connecte-toi > Vérifie que tes données personnelles sont bien remplies > Récupère ton bonus !",
      get: "Récupérer mon bonus", no: "Je ne veux pas de bonus", close: "Fermer"
    },
    ru: {
      h: "Крути колесо — забери бонус!",
      segs: ["95 FS", "80 FS", "20 FS", "0 FS", "Ещё 1 шанс"],
      stop: "⏹ Стоп", again: "▶ Крутить ещё",
      note1: "🤑 Ещё 1 шанс!", note2: "🥳 Твой выигрыш — 95 FS!",
      r_h: "Поздравляем!",
      r_pre: "Ты в паре шагов от бонуса! Установи наше нативное приложение 1xCasino для ",
      r_geo: "своей страны",
      r_post: " > Войди > Проверь, что личные данные заполнены > Забери бонус!",
      get: "Забрать бонус", no: "Мне не нужен бонус", close: "Закрыть"
    }
  };

  var CSS = ".pp{position:fixed;inset:0;z-index:100;display:grid;place-items:center;padding:16px}"
    + ".pp[hidden]{display:none}"
    + "body.pp-open{overflow:hidden}"
    + ".pp__ov{position:absolute;inset:0;background:rgba(6,0,30,.82);backdrop-filter:blur(3px)}"
    + ".pp__card{position:relative;z-index:1;width:min(400px,100%);"
    + "height:min(536px,calc(100vh - 32px));height:min(536px,calc(100dvh - 32px));"
    + "display:flex;flex-direction:column;overflow-y:auto;overflow-x:hidden;"
    + "background:var(--plate);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);"
    + "padding:24px 18px 22px;text-align:center}"
    + ".pp__stage{margin:auto 0}.pp__stage[hidden]{display:none}"
    + ".pp__x{position:absolute;top:8px;right:8px;width:36px;height:36px;border:0;border-radius:10px;cursor:pointer;"
    + "background:var(--field);color:var(--muted);font-size:1.05rem;line-height:1;display:grid;place-items:center}"
    + ".pp__x:hover{color:var(--text)}"
    + ".pp__h{font-size:1.25rem;margin-bottom:4px;padding-inline:26px}"
    + ".ppw-wrap{position:relative;width:min(272px,72vw);aspect-ratio:1;margin:16px auto 0}"
    + ".ppw-wrap::before{content:'';position:absolute;top:-4px;left:50%;transform:translateX(-50%);"
    + "border-left:12px solid transparent;border-right:12px solid transparent;border-top:18px solid var(--green);"
    + "z-index:3;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}"
    + ".ppw-ring{position:absolute;inset:-12px;border-radius:50%;z-index:0;"
    + "background:conic-gradient(from 0deg, rgba(30,178,223,0) 0 40%, rgba(30,178,223,.65) 50%, rgba(30,178,223,0) 60%, transparent 100%);"
    + "filter:blur(2px);animation:ppRing 4.5s linear infinite}"
    + "@keyframes ppRing{to{transform:rotate(360deg)}}"
    + ".ppw{position:absolute;inset:0;border-radius:50%;border:6px solid var(--field);z-index:1;will-change:transform;overflow:hidden;"
    + "box-shadow:var(--shadow),inset 0 0 0 2px rgba(255,255,255,.06);"
    + "background:conic-gradient(var(--violet) 0 72deg,var(--chip-blue) 72deg 144deg,var(--field) 144deg 216deg,"
    + "var(--chip-blue) 216deg 288deg,var(--chip-purple) 288deg 360deg)}"
    + ".ppw__seg{position:absolute;inset:0;transform:rotate(var(--r))}"
    + ".ppw__seg b{position:absolute;left:50%;top:10px;transform:translateX(-50%);color:#fff;font-weight:800;line-height:1.15;"
    + "text-shadow:0 1px 3px rgba(0,0,0,.45);text-align:center}"
    + ".ppw__seg i{display:block;font-style:normal;font-size:1.7rem}"
    + ".ppw__seg em{display:block;font-style:normal;font-size:.88rem;font-weight:800;white-space:nowrap}"
    + ".ppw-hub{position:absolute;top:50%;left:50%;width:64px;height:64px;transform:translate(-50%,-50%);"
    + "border-radius:50%;background:var(--header);border:3px solid var(--cyan);z-index:2;display:grid;place-items:center;"
    + "font-weight:800;color:var(--cyan);font-size:.84rem;line-height:1.1;text-align:center}"
    + ".pp__note{margin-top:12px;font-weight:800;color:var(--chip-sand);min-height:1.3em}"
    + ".pp__note[hidden]{display:block;visibility:hidden}"
    + ".pp__btnrow{position:relative;margin-top:10px}"
    + ".pp__prize{width:min(190px,52vw);height:auto;margin:0 auto 8px;border-radius:14px}"
    + ".pp__cf{position:fixed;top:-46px;z-index:120;pointer-events:none;"
    + "animation-name:ppFall;animation-timing-function:linear;animation-fill-mode:forwards}"
    + "@keyframes ppFall{to{transform:translateY(115vh) rotate(560deg)}}"
    + ".pp__sub{color:var(--muted);font-size:.95rem;line-height:1.55;margin:8px 0 14px}"
    + ".pp__timer{justify-content:center;margin:0 0 16px}"
    + ".pp__timer .tunit{min-width:56px;padding:10px 12px}"
    + ".pp__timer .tunit__val{font-size:1.6rem}"
    + ".pp__timer .tsep{font-size:1.6rem;padding-top:8px}"
    + ".pp__ghost{background:none;border:0;color:var(--muted);text-decoration:underline;cursor:pointer;font-size:.9rem;margin-top:12px}"
    + ".pp__ghost:hover{color:var(--text)}"
    + "@media (prefers-reduced-motion: reduce){.ppw-ring{animation:none}}";

  function gc(n) { var m = document.cookie.match("(?:^|; )" + n + "=([^;]*)"); return m ? decodeURIComponent(m[1]) : null; }
  function sc(n, v, age) { document.cookie = n + "=" + encodeURIComponent(v) + "; path=/; max-age=" + age + "; SameSite=Lax"; }
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  function geoCountry(t) {
    var el = document.querySelector('[data-geo="country"]');
    var v = el && el.textContent ? el.textContent.trim() : "";
    return v || t.r_geo;
  }

  function injectCSS() {
    if (document.getElementById("pp-style")) return;
    var st = document.createElement("style");
    st.id = "pp-style"; st.textContent = CSS;
    document.head.appendChild(st);
  }

  /* ---- variant: main_v1 ---------------------------------------------------
     Показ на загрузке -> колесо крутится -> Stop#1 = сектор 4 (Ещё 1 шанс)
     -> Try Again -> Stop#2 = сектор 0 (95 FS) -> эмодзи-конфетти -> плашка.
     Посадка: rotation ≡ 324 - 72k (mod 360) ставит центр сектора k под стрелку. */
  function buildMainV1(lang) {
    var t = TXT[lang];
    if (gc("pp_main_v1")) return;            // сценарий уже пройден — не показываем
    injectCSS();

    var segs = "";
    for (var i = 0; i < 5; i++) {
      segs += '<div class="ppw__seg" style="--r:' + (i * 72 + 36) + 'deg">'
        + "<b><i>" + EMOJI[i] + "</i><em>" + esc(t.segs[i]) + "</em></b></div>";
    }

    var html =
      '<div class="pp" id="pp" data-pp="main_v1" hidden>'
      + '<div class="pp__ov" aria-hidden="true"></div>'
      + '<div class="pp__card" role="dialog" aria-modal="true" aria-labelledby="ppH">'
      + '<button class="pp__x" id="ppX" type="button" aria-label="' + esc(t.close) + '" data-act="close">&#10005;</button>'
      + '<div class="pp__stage" id="ppStageWheel">'
      + '<h3 class="pp__h" id="ppH">' + esc(t.h) + "</h3>"
      + '<div class="ppw-wrap"><div class="ppw-ring" aria-hidden="true"></div>'
      + '<div class="ppw" id="ppw">' + segs + "</div>"
      + '<div class="ppw-hub">🎁 FS</div></div>'
      + '<p class="pp__note" id="ppNote" hidden data-t1="' + esc(t.note1) + '" data-t2="' + esc(t.note2) + '"></p>'
      + '<p class="pp__btnrow"><button class="btn btn--lg" id="ppBtn" type="button" data-act="stop" '
      + 'data-stop="' + esc(t.stop) + '" data-again="' + esc(t.again) + '">' + esc(t.stop) + "</button></p>"
      + "</div>"
      + '<div class="pp__stage" id="ppStageResult" hidden>'
      + '<img class="pp__prize" src="/assets/prize.webp" alt="" width="354" height="212" decoding="async">'
      + '<h3 class="pp__h">' + esc(t.r_h) + "</h3>"
      + '<p class="pp__sub" id="ppSub"></p>'
      + '<div class="offer__timer pp__timer" id="ppTimer" role="timer" aria-live="off">'
      + '<div class="tunit"><span class="tunit__val" id="ppTh">24</span></div><span class="tsep" aria-hidden="true">:</span>'
      + '<div class="tunit"><span class="tunit__val" id="ppTm">00</span></div><span class="tsep" aria-hidden="true">:</span>'
      + '<div class="tunit"><span class="tunit__val" id="ppTs">00</span></div></div>'
      + '<p><button class="btn btn--lg" id="ppGet" type="button" data-act="get">' + esc(t.get) + "</button></p>"
      + '<button class="pp__ghost" id="ppNo" type="button" data-act="dismiss">' + esc(t.no) + "</button>"
      + "</div></div></div>";

    var wrap = document.createElement("div");
    wrap.innerHTML = html;
    var pp = wrap.firstChild;
    document.body.appendChild(pp);
    document.getElementById("ppSub").textContent = t.r_pre + geoCountry(t) + t.r_post;

    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var wheel = document.getElementById("ppw"), btn = document.getElementById("ppBtn"),
      xb = document.getElementById("ppX"), sw = document.getElementById("ppStageWheel"),
      sr = document.getElementById("ppStageResult"), note = document.getElementById("ppNote");
    var ang = 0, raf = null, spinning = false, attempt = 0, ended = false;

    function lock(ms) { btn.disabled = true; setTimeout(function () { btn.disabled = false; }, ms); }
    function stopRaf() { if (raf) { cancelAnimationFrame(raf); raf = null; } }
    function startSpin() {
      spinning = true; note.hidden = true;
      btn.textContent = btn.getAttribute("data-stop"); btn.setAttribute("data-act", "stop");
      lock(800);
      if (reduce) return;
      var last = null;
      function step(ts) {
        if (last !== null) { ang += (ts - last) * 0.35; wheel.style.transform = "rotate(" + ang + "deg)"; }
        last = ts; raf = requestAnimationFrame(step);
      }
      raf = requestAnimationFrame(step);
    }
    function stopAt(k, cb) {
      spinning = false; stopRaf(); btn.disabled = true;
      var target = (324 - 72 * k) % 360;
      var fin = ang + 720 + ((target - (ang % 360) + 360) % 360);
      if (reduce) { wheel.style.transform = "rotate(" + target + "deg)"; ang = target; cb(); return; }
      wheel.style.transition = "transform 3s cubic-bezier(.16,1,.3,1)";
      wheel.style.transform = "rotate(" + fin + "deg)"; ang = fin;
      setTimeout(function () { wheel.style.transition = ""; cb(); }, 3100);
    }
    btn.addEventListener("click", function () {
      if (!spinning) { attempt = 1; startSpin(); return; }
      if (attempt === 0) {
        stopAt(4, function () {
          note.textContent = note.getAttribute("data-t1"); note.hidden = false;
          btn.textContent = btn.getAttribute("data-again"); btn.setAttribute("data-act", "again");
          btn.disabled = false;
        });
      } else {
        stopAt(0, function () {
          note.textContent = note.getAttribute("data-t2"); note.hidden = false;
          confetti(function () { toResult(); });
        });
      }
    });
    function confetti(cb) {
      if (reduce) { cb(); return; }
      var EM = ["🎁", "🥳", "🤑", "🤩", "🍏", "🍎", "🍋", "🍐", "🍓", "🍊", "🍒", "🎉", "🎰", "🚀"];
      var n = 18 + Math.floor(Math.random() * 10);
      for (var i = 0; i < n; i++) {
        (function () {
          var s = document.createElement("span"); s.className = "pp__cf";
          s.textContent = EM[Math.floor(Math.random() * EM.length)];
          s.style.left = (Math.random() * 100) + "%";
          s.style.fontSize = (16 + Math.random() * 22) + "px";
          s.style.animationDelay = (Math.random() * 0.5) + "s";
          s.style.animationDuration = (1.4 + Math.random() * 1.2) + "s";
          s.addEventListener("animationend", function () { if (s.parentNode) s.parentNode.removeChild(s); });
          pp.appendChild(s);
        })();
      }
      setTimeout(cb, 2000);
    }
    function toResult() {
      ended = true; sw.hidden = true; xb.hidden = true; sr.hidden = false; startTimer();
      var g = document.getElementById("ppGet"); if (g) g.focus();
    }
    function startTimer() {
      var KEY = "bonus_deadline_24h", DUR = 24 * 60 * 60 * 1000;
      var dl = parseInt(gc(KEY), 10);
      if (!dl || isNaN(dl)) { dl = Date.now() + DUR; sc(KEY, dl, 60 * 60 * 24 * 30); }
      var hE = document.getElementById("ppTh"), mE = document.getElementById("ppTm"),
        sE = document.getElementById("ppTs"), box = document.getElementById("ppTimer"), iv;
      function pad(n) { return (n < 10 ? "0" : "") + n; }
      function tick() {
        var left = dl - Date.now(); if (left < 0) left = 0;
        var ts = Math.floor(left / 1000);
        hE.textContent = pad(Math.floor(ts / 3600));
        mE.textContent = pad(Math.floor((ts % 3600) / 60));
        sE.textContent = pad(ts % 60);
        if (left <= 0) { clearInterval(iv); box.classList.add("is-done"); }
      }
      tick(); iv = setInterval(tick, 1000);
    }
    function close(done) {
      if (done) sc("pp_main_v1", "done", 60 * 60 * 24 * 365);
      stopRaf(); pp.hidden = true; document.body.classList.remove("pp-open");
    }
    xb.addEventListener("click", function () { close(false); });
    document.getElementById("ppGet").addEventListener("click", function () { close(true); });
    document.getElementById("ppNo").addEventListener("click", function () { close(true); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !ended && !pp.hidden) close(false); });

    pp.hidden = false; document.body.classList.add("pp-open"); startSpin();
  }

  var VARIANTS = { main_v1: buildMainV1 };

  function boot() {
    var s = document.querySelector("script[data-popup]");
    var id = s ? s.getAttribute("data-popup") : null;
    if (!id || !VARIANTS[id]) return;
    var lang = (document.documentElement.getAttribute("lang") || "en").slice(0, 2).toLowerCase();
    if (!TXT[lang]) lang = "en";
    VARIANTS[id](lang);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
