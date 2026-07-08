/* 1xCasino — PWA install offer (standalone). Home routes only (/, /fr/, /ru/).
   Events -> Worker /pt -> Google Sheet tab 453127204. Variant B (native prompt + manual fallback, no offline). */
(function () {
  "use strict";

  var EP = "/pt";        // Worker tracking + app-login-gate endpoint
  var DENY_MAX = 5;      // stop showing after this many cancels (deny >= 5)

  var LANGS = {
    en: {
      headline: "Get the 1xCasino Web App",
      sub: "Install our app to stay on top of the latest promos and bonuses.",
      cta: "Get the app",
      close: "Close",
      manual_title: "Add to Home screen",
      manual_steps: ["Tap the menu (three dots) in your browser.", "Choose \u201CAdd to Home screen\u201D.", "Confirm \u2014 the 1xCasino icon appears on your home screen."],
      manual_note: "Open it any time straight from your home screen."
    },
    fr: {
      headline: "Installez l\u2019app web 1xCasino",
      sub: "Installez notre application pour ne rien manquer des derni\u00E8res promos et bonus.",
      cta: "Obtenir l\u2019app",
      close: "Fermer",
      manual_title: "Ajouter \u00E0 l\u2019\u00E9cran d\u2019accueil",
      manual_steps: ["Ouvrez le menu (trois points) de votre navigateur.", "Choisissez \u00AB Ajouter \u00E0 l\u2019\u00E9cran d\u2019accueil \u00BB.", "Confirmez \u2014 l\u2019ic\u00F4ne 1xCasino appara\u00EEt sur votre \u00E9cran d\u2019accueil."],
      manual_note: "Ouvrez-la \u00E0 tout moment depuis votre \u00E9cran d\u2019accueil."
    },
    ru: {
      headline: "\u0423\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u0435 \u0432\u0435\u0431-\u043F\u0440\u0438\u043B\u043E\u0436\u0435\u043D\u0438\u0435 1xCasino",
      sub: "\u0423\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u0435 \u043F\u0440\u0438\u043B\u043E\u0436\u0435\u043D\u0438\u0435, \u0447\u0442\u043E\u0431\u044B \u043D\u0435 \u043F\u0440\u043E\u043F\u0443\u0441\u043A\u0430\u0442\u044C \u0441\u0432\u0435\u0436\u0438\u0435 \u043F\u0440\u043E\u043C\u043E \u0438 \u0431\u043E\u043D\u0443\u0441\u044B.",
      cta: "\u0423\u0441\u0442\u0430\u043D\u043E\u0432\u0438\u0442\u044C \u043F\u0440\u0438\u043B\u043E\u0436\u0435\u043D\u0438\u0435",
      close: "\u0417\u0430\u043A\u0440\u044B\u0442\u044C",
      manual_title: "\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043D\u0430 \u0433\u043B\u0430\u0432\u043D\u044B\u0439 \u044D\u043A\u0440\u0430\u043D",
      manual_steps: ["\u041E\u0442\u043A\u0440\u043E\u0439\u0442\u0435 \u043C\u0435\u043D\u044E (\u0442\u0440\u0438 \u0442\u043E\u0447\u043A\u0438) \u0432 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0435.", "\u0412\u044B\u0431\u0435\u0440\u0438\u0442\u0435 \u00AB\u0414\u043E\u0431\u0430\u0432\u0438\u0442\u044C \u043D\u0430 \u0433\u043B\u0430\u0432\u043D\u044B\u0439 \u044D\u043A\u0440\u0430\u043D\u00BB.", "\u041F\u043E\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u2014 \u0438\u043A\u043E\u043D\u043A\u0430 1xCasino \u043F\u043E\u044F\u0432\u0438\u0442\u0441\u044F \u043D\u0430 \u044D\u043A\u0440\u0430\u043D\u0435."],
      manual_note: "\u041E\u0442\u043A\u0440\u044B\u0432\u0430\u0439\u0442\u0435 \u0435\u0451 \u0432 \u043B\u044E\u0431\u043E\u0439 \u043C\u043E\u043C\u0435\u043D\u0442 \u043F\u0440\u044F\u043C\u043E \u0441 \u0433\u043B\u0430\u0432\u043D\u043E\u0433\u043E \u044D\u043A\u0440\u0430\u043D\u0430."
    }
  };

  var C = { bg:"#160241", plate:"#1E035E", line:"rgba(255,255,255,.12)", text:"#FFFFFF", muted:"#BCAEE6", green:"#7EAC2F", greenH:"#8ABA38", violet:"#641EFB" };

  function lang(){ var l=(document.documentElement.lang||"en").slice(0,2).toLowerCase(); return LANGS[l]?l:"en"; }
  function T(){ return LANGS[lang()]; }
  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c];}); }

  // ---- cookies / flags ----
  function getCookie(n){ var m=document.cookie.match("(?:^|; )"+n+"=([^;]*)"); return m?decodeURIComponent(m[1]):""; }
  function setCookie(n,v,days){ var d=new Date(Date.now()+days*864e5); document.cookie=n+"="+encodeURIComponent(v)+"; path=/; expires="+d.toUTCString()+"; SameSite=Lax"; }
  function getDeny(){ return parseInt(getCookie("pwa_deny")||"0",10)||0; }
  function incDeny(){ setCookie("pwa_deny", String(getDeny()+1), 365); }
  function markInstalled(){ try{ localStorage.setItem("pwa_installed","1"); }catch(e){} }
  function installedFlag(){ try{ return localStorage.getItem("pwa_installed")==="1"; }catch(e){ return false; } }

  // ---- tracking ----
  function body(e,a){ return JSON.stringify({ e:e, a:a||"", l:lang(), p:location.pathname }); }
  function send(e,a){
    var b=body(e,a);
    try{ if(navigator.sendBeacon){ navigator.sendBeacon(EP, new Blob([b],{type:"application/json"})); return; } }catch(_){}
    try{ fetch(EP,{method:"POST",headers:{"Content-Type":"application/json"},body:b,keepalive:true,credentials:"omit"}); }catch(_){}
  }
  function check(e){ // awaits Worker decision for the app-login gate
    return fetch(EP,{method:"POST",headers:{"Content-Type":"application/json"},body:body(e,""),credentials:"omit"})
      .then(function(r){ return r.ok?r.json():null; }).catch(function(){ return null; });
  }

  // ---- native install prompt capture ----
  var deferred=null;
  window.addEventListener("beforeinstallprompt", function(ev){ ev.preventDefault(); deferred=ev; });
  window.addEventListener("appinstalled", function(){ markInstalled(); });

  function isInstalled(){
    if(installedFlag()) return Promise.resolve(true);
    if(navigator.getInstalledRelatedApps){
      return navigator.getInstalledRelatedApps().then(function(apps){
        return !!(apps && apps.some(function(a){ return a.platform==="webapp"; }));
      }).catch(function(){ return false; });
    }
    return Promise.resolve(false);
  }

  // ---- UI ----
  var styled=false;
  function injectStyle(){
    if(styled) return; styled=true;
    var css=
      ".pwa-ov{position:fixed;inset:0;z-index:2147483000;display:flex;align-items:flex-end;justify-content:center;background:rgba(6,1,22,.62);padding:14px;animation:pwaFade .18s ease}"+
      "@media(min-width:560px){.pwa-ov{align-items:center}}"+
      "@keyframes pwaFade{from{opacity:0}to{opacity:1}}"+
      ".pwa-card{position:relative;width:100%;max-width:420px;background:"+C.bg+";border:1px solid "+C.line+";border-radius:18px;padding:20px 18px 18px;box-shadow:0 18px 60px rgba(0,0,0,.5);color:"+C.text+";font-family:inherit}"+
      ".pwa-x{position:absolute;top:10px;right:10px;width:34px;height:34px;border:0;border-radius:50%;background:"+C.plate+";color:"+C.muted+";font-size:18px;line-height:34px;cursor:pointer}"+
      ".pwa-x:hover{color:#fff}"+
      ".pwa-top{display:flex;gap:14px;align-items:center}"+
      ".pwa-logo{width:60px;height:60px;border-radius:14px;flex:0 0 auto;object-fit:cover;background:"+C.plate+"}"+
      ".pwa-h{margin:0 0 4px;font-size:17px;font-weight:800;line-height:1.2}"+
      ".pwa-sub{margin:0;font-size:13px;line-height:1.35;color:"+C.muted+"}"+
      ".pwa-stars{margin:12px 0 4px;font-size:15px;letter-spacing:2px;color:#FFC107;text-align:center}"+
      ".pwa-cta{display:block;width:100%;margin-top:12px;padding:14px;border:0;border-radius:12px;background:"+C.green+";color:#0e1a03;font-size:16px;font-weight:800;cursor:pointer}"+
      ".pwa-cta:hover{background:"+C.greenH+"}"+
      ".pwa-steps{margin:14px 0 4px;padding:0;list-style:none;counter-reset:s}"+
      ".pwa-steps li{position:relative;padding:8px 0 8px 40px;font-size:14px;line-height:1.35;border-top:1px solid "+C.line+"}"+
      ".pwa-steps li:first-child{border-top:0}"+
      ".pwa-steps li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:7px;width:26px;height:26px;border-radius:50%;background:"+C.violet+";color:#fff;font-weight:800;font-size:13px;text-align:center;line-height:26px}"+
      ".pwa-note{margin:8px 0 0;font-size:12px;color:"+C.muted+";text-align:center}";
    var s=document.createElement("style"); s.textContent=css; document.head.appendChild(s);
  }

  var ov=null;
  function remove(){ if(ov){ var n=ov; ov=null; if(n.parentNode) n.parentNode.removeChild(n); } }
  function cancel(){ if(!ov) return; remove(); send("pwa_popup_click","cancel"); incDeny(); }

  function toManual(){
    var t=T();
    var steps=t.manual_steps.map(function(x){ return "<li>"+esc(x)+"</li>"; }).join("");
    ov.querySelector(".pwa-body").innerHTML=
      '<div class="pwa-top"><img class="pwa-logo" src="/assets/app_icon.webp" alt=""><div>'+
      '<p class="pwa-h">'+esc(t.manual_title)+'</p><p class="pwa-sub">'+esc(t.sub)+'</p></div></div>'+
      '<ol class="pwa-steps">'+steps+'</ol><p class="pwa-note">'+esc(t.manual_note)+'</p>';
  }

  function onGet(){
    send("pwa_popup_click","install");
    if(deferred){
      send("pwa_install_popup_show");
      var d=deferred; deferred=null;
      d.prompt();
      d.userChoice.then(function(c){
        var acc = c && c.outcome==="accepted";
        send("pwa_install_popup_click", acc?"install":"cancel");
        if(acc) markInstalled();
        remove();
      }).catch(remove);
    } else {
      toManual(); // browsers without beforeinstallprompt (Opera Mini/UC/Data Saver)
    }
  }

  function show(){
    injectStyle();
    var t=T();
    ov=document.createElement("div"); ov.className="pwa-ov";
    ov.innerHTML=
      '<div class="pwa-card" role="dialog" aria-modal="true" aria-label="'+esc(t.headline)+'">'+
        '<button class="pwa-x" type="button" aria-label="'+esc(t.close)+'">\u00D7</button>'+
        '<div class="pwa-body">'+
          '<div class="pwa-top"><img class="pwa-logo" src="/assets/app_icon.webp" alt="">'+
          '<div><p class="pwa-h">'+esc(t.headline)+'</p><p class="pwa-sub">'+esc(t.sub)+'</p></div></div>'+
          '<div class="pwa-stars">\u2605\u2605\u2605\u2605\u2605</div>'+
          '<button class="pwa-cta" type="button">'+esc(t.cta)+'</button>'+
        '</div>'+
      '</div>';
    ov.addEventListener("click", function(e){ if(e.target===ov) cancel(); });
    ov.querySelector(".pwa-x").addEventListener("click", cancel);
    ov.querySelector(".pwa-cta").addEventListener("click", onGet);
    document.body.appendChild(ov);
    send("pwa_popup_show");
  }

  // ---- service worker (scope '/') ----
  function reg(){ if("serviceWorker" in navigator){ try{ navigator.serviceWorker.register("/sw.js"); }catch(_){} } }

  // ---- flow (per visit to a home route) ----
  function run(){
    reg();
    var standalone = (window.matchMedia && matchMedia("(display-mode: standalone)").matches) || navigator.standalone===true;
    if(standalone){ markInstalled(); send("pwa_online_click"); return; }  // opened as installed PWA
    send("pwa_app_init");
    if(getDeny()>=DENY_MAX) return;                                       // Case 2: >=5 cancels
    isInstalled().then(function(inst){
      if(inst){ send("pwa_install_exist"); return; }                     // Case 3
      send("pwa_install_not_exist");
      check("app_login_check").then(function(res){                       // Worker logs app_login_exist/not_exist, returns {stop}
        if(res && res.stop) return;                                      // Case 4
        show();                                                          // Cases 5/6
      });
    });
  }

  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
