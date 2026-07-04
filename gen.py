# -*- coding: utf-8 -*-
"""Generate 1xCasino landing: / /app/ /android/ /ios/ in en/fr/ru, plus /draft (RU sandbox, noindex)."""
import os
from string import Template
import datetime, json

DOMAIN = "https://1xcasino-guide.com"
LOGO = "/assets/logo.svg"
PROMO = "1xcTestCode"
YEAR = datetime.date.today().year
MANIFEST = json.dumps({
    "name": "1XC Guide",
    "short_name": "1XC Guide",
    "description": "1xCasino \u2014 guide, bonuses and app install",
    "id": "/",
    "scope": "/",
    "start_url": "/",
    "display": "standalone",
    "orientation": "portrait-primary",
    "background_color": "#19024B",
    "theme_color": "#160241",
    "lang": "en",
    "dir": "ltr",
    "categories": ["entertainment", "games"],
    "icons": (
        [{"src": f"/assets/icons/icon-{s}.png", "sizes": f"{s}x{s}", "type": "image/png", "purpose": "any"}
         for s in (72, 96, 128, 144, 152, 180, 192, 384, 512)]
        + [{"src": f"/assets/icons/icon-{s}.png", "sizes": f"{s}x{s}", "type": "image/png", "purpose": "maskable"}
           for s in (192, 512)]
    ),
}, ensure_ascii=False, indent=2)

CSS = """
:root{
  --bg:#19024B;--header:#160241;--surface:#160241;--plate:#1E035E;--field:#2E1B55;--footer:#120335;
  --line:rgba(255,255,255,.09);
  --text:#FFFFFF;--muted:#BCAEE6;--ink-blue:#215583;
  --green:#7EAC2F;--green-h:#8ABA38;--green-a:#6F9A29;
  --violet:#641EFB;--violet-h:#7434FF;--cyan:#1EB2DF;
  --chip-purple:#A134B1;--chip-blue:#3CA5FF;--chip-green:#10993C;--chip-sand:#FFDBA8;
  --maxw:1060px;--radius:16px;--btn-radius:12px;--pad:20px;
  --shadow:0 18px 44px rgba(6,0,30,.55);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;overflow-x:clip}
body{font-family:Roboto,-apple-system,"Segoe UI","Helvetica Neue",Arial,sans-serif;
  background:var(--bg);color:var(--text);line-height:1.55;overflow-x:hidden;
  background-image:
    radial-gradient(58% 44% at 85% -6%, rgba(100,30,251,.38), transparent 62%),
    radial-gradient(46% 38% at -4% 4%, rgba(30,178,223,.16), transparent 58%),
    radial-gradient(60% 50% at 50% 110%, rgba(161,52,177,.18), transparent 60%);
  background-attachment:fixed}
img{max-width:100%;height:auto;display:block}
a{color:inherit;text-decoration:none}
h1,h2,h3{line-height:1.18;font-weight:800;letter-spacing:-.01em}
.wrap{width:100%;max-width:var(--maxw);margin:0 auto;padding-inline:var(--pad)}
.section{padding-block:clamp(40px,8vw,68px)}
.section--alt{background:linear-gradient(180deg,var(--header),#14023d);border-block:1px solid var(--line)}
.eyebrow{color:var(--cyan);font-weight:700;font-size:.8rem;letter-spacing:.16em;text-transform:uppercase}
.section h2{font-size:clamp(1.45rem,5vw,2rem);margin:.35em 0 .9em}
.section h2::after{content:"";display:block;width:58px;height:3px;border-radius:3px;margin-top:12px;
  background:linear-gradient(90deg,var(--cyan),rgba(30,178,223,0))}
.rich p{color:var(--muted);margin-top:12px;font-size:1rem;line-height:1.65}
.rich p:first-of-type{margin-top:0}
.bullets{list-style:none;display:grid;gap:9px;margin-top:14px}
.bullets li{color:var(--muted);padding-left:20px;position:relative}
.bullets li::before{content:"\\2013";position:absolute;left:4px;color:var(--cyan)}
.chip{display:inline-flex;align-items:center;gap:.35em;font-size:.72rem;font-weight:800;letter-spacing:.04em;
  text-transform:uppercase;border-radius:999px;padding:4px 10px;color:#fff;line-height:1}
.chip--purple{background:var(--chip-purple)}.chip--blue{background:var(--chip-blue)}
.chip--green{background:var(--chip-green)}.chip--sand{background:var(--chip-sand);color:var(--ink-blue)}
/* Buttons — flat, matching the product (no glow or highlights) */
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5em;min-height:52px;padding:0 26px;
  border-radius:var(--btn-radius);font-weight:800;font-size:1.02rem;cursor:pointer;border:0;color:#fff;
  text-transform:uppercase;letter-spacing:.02em;background:var(--green);
  transition:background .15s,transform .15s;text-align:center}
.btn:hover{background:var(--green-h);transform:translateY(-1px)}
.btn:active{background:var(--green-a);transform:none}
.btn--lg{min-height:60px;font-size:1.1rem;padding:0 32px}
.btn--sm{min-height:42px;font-size:.88rem;padding:0 18px}
.btn--block{width:100%}
.btn--violet{background:var(--violet)}
.btn--violet:hover{background:var(--violet-h)}
.btn--violet:active{background:#5618dd}
.site-header{position:sticky;top:0;z-index:60;display:flex;align-items:center;gap:12px;padding:12px var(--pad);
  background:rgba(22,2,65,.88);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center}
.brand__logo{height:20px;width:auto}
.nav-cb{position:absolute;width:1px;height:1px;opacity:0;margin:0}
.burger{display:inline-flex;flex-direction:column;justify-content:center;gap:4px;width:42px;height:42px;padding:0 9px;cursor:pointer;border-radius:10px;flex:0 0 auto}
.site-header .burger{margin-left:auto}
.burger:hover{background:var(--field)}
.burger span{display:block;height:2px;border-radius:2px;background:var(--text);transition:transform .2s,opacity .2s}
.scrim{position:fixed;inset:0;z-index:1000;background:rgba(6,0,30,.62);opacity:0;pointer-events:none;transition:opacity .25s}
.nav-cb:checked ~ .scrim{opacity:1;pointer-events:auto}
.menu-layer{position:fixed;inset:0;z-index:1001;overflow:hidden;pointer-events:none}
.drawer{position:absolute;top:0;right:0;height:100%;width:min(284px,82vw);transform:translateX(100%);
  transition:transform .25s ease;background:var(--header);border-left:1px solid var(--line);box-shadow:var(--shadow);
  padding:16px;display:flex;flex-direction:column;gap:22px;overflow-y:auto;pointer-events:auto}
.nav-cb:checked ~ .menu-layer .drawer{transform:none}
.drawer__close{align-self:flex-end;width:38px;height:38px;display:grid;place-items:center;font-size:1.7rem;line-height:1;color:var(--muted);cursor:pointer;border-radius:9px}
.drawer__close:hover{background:var(--field);color:var(--text)}
.drawer__h{display:block;font-size:.72rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--cyan);margin-bottom:10px}
.drawer__apps{margin-top:auto}
.drawer__apps .btn{margin-bottom:10px;text-transform:none}
.langsw{display:flex;flex-direction:column;gap:4px}
.langsw a{padding:10px 12px;border-radius:9px;font-weight:700;color:var(--muted)}
.langsw a:hover{background:var(--field);color:var(--text)}
.langsw a[aria-current]{background:var(--violet);color:#fff}
.gate__one{width:min(360px,100%);margin:30px auto 0}
.badge-18{font-weight:800;font-size:.78rem;color:var(--chip-sand);border:1.5px solid var(--chip-sand);
  border-radius:8px;padding:3px 8px}
.hero{padding-block:clamp(28px,7vw,56px)}
.hero__grid{display:grid;gap:30px}
.hero h1{font-size:clamp(1.8rem,6.8vw,2.9rem);margin:.35em 0 .5em}
.hl{color:transparent;background:linear-gradient(92deg,var(--chip-sand),#ffb654);-webkit-background-clip:text;background-clip:text}
.hero__lead{color:var(--muted);font-size:clamp(.98rem,3.4vw,1.08rem)}
.hero .btn{margin-top:10px}
.appcard{display:flex;gap:14px;align-items:center;background:var(--plate);border:1px solid var(--line);
  border-radius:var(--radius);padding:14px;margin:20px 0;max-width:460px;box-shadow:var(--shadow)}
.appcard__icon{width:58px;height:58px;border-radius:14px;flex:0 0 auto;padding:9px;background:var(--field);border:1px solid var(--line)}
.appcard__name{font-size:1.05rem;display:block}
.appcard__rating{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:.85rem;color:var(--muted);margin:4px 0 7px}
.stars{color:var(--chip-sand);letter-spacing:1px}
.appcard__chips{display:flex;flex-wrap:wrap;gap:6px}
.phone-zone{position:relative;width:min(260px,72vw);margin-inline:auto}
.phone-zone::before{content:"";position:absolute;inset:-12%;border-radius:50%;z-index:-1;
  background:radial-gradient(closest-side, rgba(100,30,251,.5), rgba(30,178,223,.12) 60%, transparent 72%);
  filter:blur(6px);animation:auraPulse 5s ease-in-out infinite}
@keyframes auraPulse{0%,100%{opacity:.75;transform:scale(1)}50%{opacity:1;transform:scale(1.05)}}
.phone{aspect-ratio:9/19;border-radius:36px;padding:10px;animation:floatY 6s ease-in-out infinite;
  background:linear-gradient(160deg,#2a0b73,#140136);border:1px solid var(--line);box-shadow:var(--shadow)}
@keyframes floatY{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.phone__screen{height:100%;border-radius:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:14px;text-align:center;padding:18px;background:radial-gradient(120% 80% at 50% 0%, rgba(100,30,251,.35), transparent 60%), var(--header)}
.phone__screen small{color:var(--muted);font-size:.78rem;line-height:1.4}
.phone__logo{height:30px;opacity:.95}
.benefits{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:6px}
.benefit{display:flex;gap:12px;align-items:flex-start;background:var(--plate);border:1px solid var(--line);
  border-radius:14px;padding:14px;transition:transform .2s,border-color .2s,box-shadow .2s}
.benefit:hover{transform:translateY(-3px);border-color:rgba(30,178,223,.45);box-shadow:0 10px 26px rgba(6,0,30,.5)}
.benefit .emo{font-size:1.15rem;line-height:1;flex:0 0 auto;width:40px;height:40px;border-radius:12px;display:grid;place-items:center;
  background:linear-gradient(135deg,rgba(100,30,251,.45),rgba(100,30,251,.12));border:1px solid rgba(126,59,255,.4)}
.benefit span+span{font-weight:600;font-size:.93rem;padding-top:8px}
.cards{display:grid;gap:14px}
.card{background:var(--plate);border:1px solid var(--line);border-radius:var(--radius);padding:22px;
  transition:transform .2s,border-color .2s}
.card:hover{transform:translateY(-3px);border-color:rgba(161,52,177,.5)}
.card__ic{width:46px;height:46px;border-radius:12px;display:grid;place-items:center;
  background:linear-gradient(135deg,rgba(30,178,223,.3),rgba(30,178,223,.07));color:var(--cyan);margin-bottom:14px}
.card h3{font-size:1.08rem;margin-bottom:6px}
.card p{color:var(--muted);font-size:.95rem}
.tbl{width:100%;border-collapse:collapse;margin-top:16px;font-size:.93rem;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.tbl th,.tbl td{text-align:left;padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl thead th{background:var(--field);color:var(--text);font-weight:700}
.tbl td:first-child{color:var(--text);font-weight:600}
.tbl td{color:var(--muted)}
.tbl tbody tr:last-child td{border-bottom:0}
.tbl tbody tr{background:rgba(30,3,94,.35)}
.steps{counter-reset:s;display:grid;gap:12px;margin:16px 0 24px}
.step{position:relative;background:var(--plate);border:1px solid var(--line);border-radius:var(--radius);padding:16px 16px 16px 60px}
.step::before{counter-increment:s;content:counter(s);position:absolute;left:14px;top:14px;width:32px;height:32px;border-radius:50%;
  display:grid;place-items:center;font-weight:800;color:#fff;background:var(--violet)}
.step p{color:var(--text);font-size:.97rem;font-weight:600}
.checklist{list-style:none;display:grid;gap:10px;margin-top:16px;grid-template-columns:repeat(2,1fr)}
.checklist li{display:flex;gap:10px;align-items:center;background:var(--plate);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-weight:600}
.checklist li::before{content:"\\2713";color:var(--green);font-weight:800}
.promo{background:linear-gradient(180deg,rgba(100,30,251,.20),var(--plate));border:1px solid rgba(126,59,255,.45);
  border-radius:18px;padding:26px;text-align:center;box-shadow:var(--shadow);position:relative;overflow:hidden}
.promo::before{content:"";position:absolute;inset:-60% -20%;z-index:0;pointer-events:none;
  background:conic-gradient(from 0deg, transparent 0 84%, rgba(30,178,223,.20) 92%, transparent 100%);
  animation:promoSweep 7s linear infinite}
@keyframes promoSweep{to{transform:rotate(360deg)}}
.promo>*{position:relative;z-index:1}
.promo__code{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin:16px 0}
.promo__value{font-size:clamp(1.3rem,6vw,1.9rem);font-weight:800;letter-spacing:.08em;color:var(--chip-sand);
  background:rgba(0,0,0,.32);border:1px dashed rgba(30,178,223,.6);border-radius:12px;padding:10px 18px}
.wheel-block{text-align:center}
.wheel-wrap{position:relative;width:min(300px,82vw);aspect-ratio:1;margin:26px auto 0}
.wheel-wrap::before{content:"";position:absolute;top:-4px;left:50%;transform:translateX(-50%);
  border-left:13px solid transparent;border-right:13px solid transparent;border-top:20px solid var(--green);
  z-index:3;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
.wheel-ring{position:absolute;inset:-14px;border-radius:50%;z-index:0;
  background:conic-gradient(from 0deg, rgba(30,178,223,0) 0 40%, rgba(30,178,223,.65) 50%, rgba(30,178,223,0) 60%, transparent 100%);
  filter:blur(2px);animation:ringSpin 4.5s linear infinite}
@keyframes ringSpin{to{transform:rotate(360deg)}}
.wheel{position:absolute;inset:0;border-radius:50%;border:6px solid var(--field);z-index:1;
  box-shadow:var(--shadow),inset 0 0 0 2px rgba(255,255,255,.06);
  transition:transform 4s cubic-bezier(.16,1,.3,1);will-change:transform;
  background:conic-gradient(
    var(--violet) 0 45deg, var(--chip-blue) 45deg 90deg,
    var(--violet) 90deg 135deg, var(--chip-blue) 135deg 180deg,
    var(--violet) 180deg 225deg, var(--chip-blue) 225deg 270deg,
    var(--violet) 270deg 315deg, var(--chip-blue) 315deg 360deg)}
.seg{position:absolute;inset:0}
.seg b{position:absolute;left:50%;top:14px;transform:translateX(-50%);font-size:.82rem;font-weight:800;white-space:nowrap;color:#fff;
  text-shadow:0 1px 3px rgba(0,0,0,.45)}
.wheel-hub{position:absolute;top:50%;left:50%;width:46px;height:46px;transform:translate(-50%,-50%);
  border-radius:50%;background:var(--header);border:3px solid var(--cyan);z-index:2;display:grid;place-items:center;
  font-weight:800;color:var(--cyan);font-size:.72rem}
.wheel-result{margin-top:16px;font-weight:800;color:var(--chip-sand);min-height:1.3em}
.img-ph{margin-top:16px;border:1.5px dashed rgba(30,178,223,.35);border-radius:14px;min-height:160px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--muted);text-align:center;gap:4px;font-size:.9rem;
  background:repeating-linear-gradient(45deg,rgba(255,255,255,.02) 0 12px,transparent 12px 24px),var(--plate)}
.img-ph small{font-size:.78rem;opacity:.8}
.pay{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:22px;color:var(--muted);font-size:.86rem}
.pay span{background:var(--field);border:1px solid var(--line);border-radius:10px;padding:8px 16px;font-weight:600}
.faq details{background:var(--plate);border:1px solid var(--line);border-radius:12px;margin-bottom:10px;overflow:hidden;transition:border-color .2s}
.faq details[open]{border-color:rgba(30,178,223,.45)}
.faq summary{list-style:none;cursor:pointer;font-weight:700;padding:16px 18px;display:flex;justify-content:space-between;gap:12px;align-items:center}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";color:var(--cyan);font-size:1.4rem;line-height:1}
.faq details[open] summary::after{content:"\\2013"}
.faq details p{padding:0 18px 18px;color:var(--muted);font-size:.95rem}
.final-cta{text-align:center;padding-block:clamp(46px,10vw,80px);position:relative}
.final-cta::before{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(50% 60% at 50% 50%, rgba(100,30,251,.28), transparent 70%)}
.final-cta .wrap{position:relative}
.final-cta h2{font-size:clamp(1.5rem,5.6vw,2.3rem);margin-bottom:.6em}
.footer{background:var(--footer);border-top:1px solid var(--line);padding-block:30px;font-size:.85rem;color:var(--muted)}
.footer__top{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between;margin-bottom:18px}
.footer__links{display:flex;flex-wrap:wrap;gap:16px}
.footer__links a:hover{color:var(--text)}
.footer__logo{height:28px;opacity:.85}
.footer__bottom{display:flex;align-items:center;justify-content:space-between;gap:14px;border-top:1px solid var(--line);padding-top:16px}
.sticky-cta{position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px 14px calc(10px + env(safe-area-inset-bottom));
  background:rgba(18,3,53,.94);backdrop-filter:blur(10px);border-top:1px solid var(--line)}
body.has-sticky{padding-bottom:80px}
/* Root platform-selection page */
.gate{min-height:auto;display:grid;place-items:center;text-align:center;padding-block:clamp(40px,8vw,80px);overflow:hidden}
.gate__img{width:min(320px,78vw);margin-inline:auto}
.gate__bens{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:34px;width:min(640px,100%);margin-inline:auto}
.gben{display:flex;flex-direction:column;align-items:center;gap:8px;background:var(--plate);border:1px solid var(--line);
  border-radius:14px;padding:16px 10px;font-weight:600;font-size:.88rem;text-align:center}
.gben .emo{font-size:1.5rem;line-height:1}
.gate h1{font-size:clamp(1.7rem,6.4vw,2.7rem);margin:.7em 0 .4em}
.gate p{color:var(--muted);max-width:480px;margin-inline:auto}
.gate__btns{display:grid;gap:14px;margin-top:30px;width:min(420px,100%);margin-inline:auto}
.gate__zone{position:relative}
.gate__zone::before{content:"";position:absolute;inset:-18% -30%;z-index:-1;border-radius:50%;
  background:radial-gradient(closest-side, rgba(100,30,251,.4), transparent 70%);filter:blur(8px)}
.os-ic{width:22px;height:22px;flex:0 0 auto}
.js .rv{opacity:0;transform:translateY(16px);transition:opacity .55s ease,transform .55s ease}
.js .rv.in{opacity:1;transform:none}
.hero__cta{text-align:center;margin-top:18px}
.hero__img{width:min(360px,84%);height:auto;display:block;margin-inline:auto;margin-bottom:clamp(-48px,-10vw,-22px);filter:drop-shadow(0 18px 40px rgba(0,0,0,.45));animation:floatY 6s ease-in-out infinite}
.footer__contact{text-align:center;margin-bottom:12px}
.footer__mail{display:inline-block;background:var(--field);padding:7px 14px;border-radius:9px;color:var(--cyan);font-weight:700;font-size:.92rem;text-decoration:none;border:1px solid var(--line)}
.footer__mail:hover{filter:brightness(1.15)}
.footer__copy{text-align:center;color:var(--muted);font-size:.85rem;margin-bottom:18px}
.install{margin-top:8px}
.ckl{list-style:none;display:grid;gap:10px;margin:6px 0 0;padding:0}
.ckl__row{display:flex;gap:12px;align-items:flex-start;background:var(--plate);border:1px solid var(--line);border-radius:12px;padding:13px 14px;cursor:pointer;font-weight:600}
.ckl__cb{position:absolute;width:1px;height:1px;opacity:0;margin:0}
.ckl__box{flex:0 0 auto;width:22px;height:22px;border-radius:6px;border:2px solid var(--line);display:grid;place-items:center;margin-top:1px;transition:background .15s,border-color .15s}
.ckl__cb:checked + .ckl__box{background:var(--green);border-color:var(--green)}
.ckl__cb:checked + .ckl__box::after{content:"✓";color:#fff;font-size:.82rem;font-weight:800;line-height:1}
.ckl__cb:focus-visible + .ckl__box{outline:3px solid var(--cyan);outline-offset:2px}
.ckl__cb:checked ~ span:last-child{text-decoration:line-through;opacity:.55}
.bar{position:relative;height:48px;border-radius:12px;overflow:hidden;margin-top:18px;background:linear-gradient(90deg,var(--violet),var(--green));border:1px solid var(--line)}
.bar__mask{position:absolute;top:0;right:0;bottom:0;width:100%;background:var(--field);transition:width .45s ease}
.bar__txt{position:absolute;inset:0;display:grid;place-items:center;z-index:1;padding:0 14px;text-align:center;font-weight:800;font-size:.9rem;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.55)}
.ilink{color:var(--cyan);font-weight:700;text-decoration:underline}
.bform{margin-top:18px;background:var(--plate);border:1px solid var(--line);border-radius:var(--radius);padding:18px;transition:opacity .2s}
.bform.is-locked{opacity:.5}
.bform__t{font-weight:700;margin-bottom:12px}
.bform__row{display:flex;gap:10px;flex-wrap:wrap}
.bform__in{flex:1 1 200px;min-height:52px;padding:0 16px;border-radius:12px;background:var(--field);border:1px solid var(--line);color:var(--text);font-size:1rem}
.bform__in::placeholder{color:var(--muted)}
.bform__in:focus{outline:2px solid var(--cyan);outline-offset:1px}
.bform__lock{margin-top:10px;font-size:.85rem;color:var(--muted)}
.bform__msg{margin-top:10px;font-size:.9rem;font-weight:700}
.bform__msg.ok{color:var(--green)}
.bform__msg.err{color:#ff7676}
/* draft B5 sandbox variants */
.bar--draft{border-width:2px;border-color:rgba(255,255,255,.5)}
.ckl__row.is-locked{opacity:.4;cursor:not-allowed}
.ckl__row.is-locked .ckl__box{border-style:dashed}
.bform--draft{text-align:center}
.bform--draft.is-locked{pointer-events:none}
.bform--draft .ckl{margin-bottom:14px}
.bform--draft .bform__row{justify-content:center}
.bform--draft .bform__in{flex:0 1 280px;text-align:center}
.form-chk{display:flex;gap:12px;align-items:flex-start;text-align:left;font-weight:600;margin-bottom:16px}
.form-chk .ckl__cb:checked ~ span:last-child{text-decoration:none;opacity:1}
.reviews{margin-top:20px;max-width:560px;margin-inline:auto}
.reviews__track{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:10px;scrollbar-width:none}
.reviews__track::-webkit-scrollbar{display:none}
.review{flex:0 0 auto;width:min(280px,80%);scroll-snap-align:start;background:var(--plate);border:1px solid var(--line);border-radius:14px;padding:16px}
.review__top{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.review__ava{width:52px;height:52px;border-radius:50%;object-fit:cover;flex:0 0 auto;background:var(--field)}
.review__text{color:var(--muted);font-size:.92rem;line-height:1.5;margin:0}
.stars-rate{display:inline-block;position:relative;font-size:1rem;line-height:1;letter-spacing:1px}
.stars-rate::before{content:"★★★★★";color:rgba(255,255,255,.18)}
.stars-rate::after{content:"★★★★★";color:#f5c518;position:absolute;left:0;top:0;width:var(--r);overflow:hidden;white-space:nowrap}
.scroll-arrow{display:block;width:100%;padding:22px 0 8px;text-align:center;cursor:pointer;text-decoration:none;-webkit-tap-highlight-color:transparent}
.scroll-arrow__chev{display:inline-block;width:26px;height:26px;animation:arrowBounce 1.4s ease-in-out infinite}
.scroll-arrow__chev::before{content:"";display:block;width:100%;height:100%;border-right:3px solid var(--cyan);border-bottom:3px solid var(--cyan);transform:rotate(45deg)}
@keyframes arrowBounce{0%,100%{transform:translateY(0)}50%{transform:translateY(9px)}}
.shots{margin-top:24px}
.shots__h{font-size:1.05rem;margin-bottom:12px}
.shots__track{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:10px;scrollbar-width:none}
.shots__track::-webkit-scrollbar{display:none}
.shot{flex:0 0 66%;scroll-snap-align:start;margin:0}
.shot__cap{margin:10px 0 0;color:var(--muted);font-size:.88rem}
.shot img{width:100%;height:auto;display:block;border-radius:18px;border:1px solid var(--line)}
.shots--ios .shot img{border-radius:0;border:none}
.blockpage{min-height:100vh;min-height:100dvh;display:grid;place-items:center;padding:36px 20px;text-align:center}
.blockpage__wrap{width:min(560px,100%);display:flex;flex-direction:column;align-items:center;gap:18px}
.blockpage__img{width:min(320px,82%);height:auto}
.blockpage__logo{height:34px;width:auto}
.blockpage__h1{font-size:clamp(1.3rem,5vw,1.75rem);margin:0}
.blockpage__p{color:var(--muted);margin:0;max-width:460px;line-height:1.55}
.blockpage .btn{margin-top:8px}
/* 404 slot page */
.err404{min-height:100vh;min-height:100dvh;display:flex;flex-direction:column;position:relative;overflow:hidden;background:radial-gradient(120% 78% at 50% -6%,#2C0A6E 0%,var(--bg) 62%),var(--bg)}
.err404__main{flex:1;display:grid;place-items:center;padding:26px 16px;position:relative;z-index:1}
.err404::before{content:"";position:absolute;inset:0;z-index:0;opacity:.11;background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%27http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%27%20width%3D%2792%27%20height%3D%2792%27%3E%3Cg%20fill%3D%27%23ffffff%27%20font-size%3D%2722%27%20font-family%3D%27sans-serif%27%20text-anchor%3D%27middle%27%3E%3Ctext%20x%3D%2723%27%20y%3D%2732%27%3E%E2%99%A0%3C%2Ftext%3E%3Ctext%20x%3D%2769%27%20y%3D%2732%27%3E%E2%99%A5%3C%2Ftext%3E%3Ctext%20x%3D%2723%27%20y%3D%2778%27%3E%E2%99%A6%3C%2Ftext%3E%3Ctext%20x%3D%2769%27%20y%3D%2778%27%3E%E2%99%A3%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fsvg%3E");background-size:92px 92px}
.slot-wrap{position:relative;z-index:1;width:min(480px,94%);display:flex;flex-direction:column;align-items:center;gap:30px}
.slot{position:relative;width:100%;background:linear-gradient(180deg,#F6C948,#E19E1C);border:6px solid #C9861A;border-radius:26px;padding:52px clamp(16px,5vw,26px) 26px;box-shadow:0 24px 60px rgba(0,0,0,.5),inset 0 2px 0 rgba(255,255,255,.55)}
.slot__banner{position:absolute;top:-22px;left:50%;transform:translateX(-50%);background:linear-gradient(180deg,var(--violet-h),var(--violet));color:#fff;font-weight:800;font-size:clamp(1.05rem,4.4vw,1.45rem);letter-spacing:.5px;padding:12px 28px;border-radius:40px;white-space:nowrap;border:4px solid #fff;box-shadow:0 8px 20px rgba(0,0,0,.35);animation:bannerGlow 2.4s ease-in-out infinite}
.slot__body{position:relative;background:var(--footer);border-radius:16px;padding:14px 12px;box-shadow:inset 0 4px 16px rgba(0,0,0,.65)}
.slot__reels{display:flex;gap:8px;justify-content:center}
.reel{width:clamp(64px,20vw,86px);height:140px;overflow:hidden;border-radius:10px;position:relative;background:linear-gradient(180deg,#cfcfcf,#fff 26%,#fff 74%,#cfcfcf)}
.reel::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.28),transparent 22%,transparent 78%,rgba(0,0,0,.28))}
.reel__strip{transform:translateY(var(--rest));animation:reelSpin 2.1s cubic-bezier(.16,.84,.28,1) both}
.reel__strip span{display:block;height:108px;line-height:108px;text-align:center;font-size:84px;font-weight:800;color:var(--violet);font-family:Arial,Helvetica,sans-serif}
.reel--1 .reel__strip{animation-delay:.1s}
.reel--2 .reel__strip{animation-delay:.45s}
.reel--3 .reel__strip{animation-delay:.8s}
.slot__lever{position:absolute;top:24px;right:-18px;width:14px;height:116px;border-radius:8px;background:linear-gradient(90deg,#A96C16,#E6A52A 45%,#A96C16);transform-origin:bottom center;animation:leverPull 2.1s ease-in-out}
.slot__ball{position:absolute;top:-24px;left:50%;transform:translateX(-50%);width:32px;height:32px;border-radius:50%;background:radial-gradient(circle at 34% 28%,#8fe6ff,var(--cyan) 58%,#0f6d8c);box-shadow:0 4px 10px rgba(0,0,0,.45)}
.slot__led{margin-top:14px;background:var(--footer);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:11px 14px;text-align:center}
.slot__led span{font-family:ui-monospace,"Courier New",monospace;letter-spacing:2px;color:var(--cyan);font-size:clamp(.68rem,2.7vw,.92rem);font-weight:700;text-shadow:0 0 8px rgba(30,178,223,.7);animation:ledBlink 1.7s steps(1) infinite}
.err404__btn{font-weight:800;letter-spacing:.5px;min-width:min(280px,80%)}
@keyframes reelSpin{from{transform:translateY(var(--start))}to{transform:translateY(var(--rest))}}
@keyframes leverPull{0%{transform:translateY(0)}12%{transform:translateY(24px)}30%{transform:translateY(0)}}
@keyframes bannerGlow{0%,100%{box-shadow:0 8px 20px rgba(0,0,0,.35)}50%{box-shadow:0 8px 30px rgba(100,30,251,.75)}}
@keyframes ledBlink{0%,92%,100%{opacity:1}94%,98%{opacity:.5}}
@media (min-width:760px){
  .hero__grid{grid-template-columns:1.12fr .88fr;align-items:center}
  .hero__img{margin-bottom:0}
  .benefits{grid-template-columns:repeat(3,1fr)}
  .cards{grid-template-columns:repeat(3,1fr)}
  .steps{grid-template-columns:repeat(2,1fr)}
  .checklist{grid-template-columns:repeat(3,1fr)}
  .gate__btns{grid-template-columns:1fr 1fr}
  .gate__bens{grid-template-columns:repeat(3,1fr)}
  .sticky-cta{display:none}
  body.has-sticky{padding-bottom:0}
  .shot{flex:0 0 31%}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important;scroll-behavior:auto!important}
  .js .rv{opacity:1;transform:none}
}
:focus-visible{outline:3px solid var(--cyan);outline-offset:2px;border-radius:6px}
.offer .wrap{max-width:840px}
.offer__card{display:flex;gap:24px;align-items:center;background:linear-gradient(150deg,#2A0A78 0%,var(--plate) 62%);border:1px solid rgba(30,178,223,.38);border-radius:22px;padding:26px 30px;box-shadow:0 0 0 1px rgba(100,30,251,.18),0 22px 55px -22px rgba(30,178,223,.5)}
.offer__img{flex:0 0 auto;width:300px;max-width:100%;height:auto;filter:drop-shadow(0 12px 30px rgba(30,178,223,.55))}
.offer__body{flex:1;min-width:0}
.offer__title{margin:0 0 8px;font-size:1.5rem;line-height:1.22}
.offer__sub{margin:0 0 18px;color:var(--muted);font-size:1rem}
.offer__sub .sub-rest{color:transparent}
.offer__sub.is-typing .sub-typed::after{content:'▏';margin-left:1px;color:var(--cyan);animation:offerCaret .7s step-end infinite}
.offer__sub.is-blink{animation:offerBlink .32s ease 2}
@keyframes offerCaret{50%{opacity:0}}
@keyframes offerBlink{0%,100%{opacity:1}50%{opacity:.15}}
.offer__timer{display:inline-flex;align-items:flex-start;gap:10px;margin:0 0 22px}
.offer__timer.is-done{opacity:.5}
.tunit{display:flex;align-items:center;justify-content:center;min-width:70px;background:rgba(9,2,40,.62);border:1px solid rgba(30,178,223,.42);border-radius:14px;padding:12px 16px}
.tunit__val{font-size:2.1rem;font-weight:800;line-height:1;color:var(--cyan);font-variant-numeric:tabular-nums;text-shadow:0 0 16px rgba(30,178,223,.65)}
.tsep{font-size:2.1rem;font-weight:800;line-height:1;color:var(--cyan);opacity:.65;padding-top:9px}
.offer__cta{margin-bottom:0}
@media(max-width:640px){.offer__card{flex-direction:column;text-align:center;padding:24px 18px}.offer__img{width:min(300px,72vw)}.offer__timer{margin-left:auto;margin-right:auto;gap:8px}.offer__title{font-size:1.3rem}.tunit{min-width:54px;padding:10px 12px}.tunit__val{font-size:1.7rem}.tsep{font-size:1.7rem}}
"""

ANDROID_ICON = '<svg class="os-ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 8.5h-11A1.5 1.5 0 0 0 5 10v7a1.5 1.5 0 0 0 1.5 1.5H8V21a1 1 0 0 0 2 0v-2.5h4V21a1 1 0 0 0 2 0v-2.5h1.5A1.5 1.5 0 0 0 19 17v-7a1.5 1.5 0 0 0-1.5-1.5zM7.7 3.2a.5.5 0 0 1 .87-.5l1 1.74A6.4 6.4 0 0 1 12 4c.86 0 1.68.16 2.43.44l1-1.73a.5.5 0 1 1 .87.5l-.97 1.68A5.5 5.5 0 0 1 17.9 7.5H6.1a5.5 5.5 0 0 1 2.57-2.61z"/></svg>'
APPLE_ICON = '<svg class="os-ic" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.7 12.7c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.9-1.6 0-3.1 1-4 2.4-1.7 2.9-.4 7.3 1.2 9.7.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.2-.8s1.9.8 3.2.8c1.3 0 2.2-1.2 3-2.4.9-1.3 1.3-2.7 1.3-2.7s-2.5-1-2.6-3.8zM14.4 5.4c.7-.8 1.1-1.9 1-3-1 0-2.2.7-2.9 1.5-.6.7-1.2 1.9-1 3 1.1.1 2.2-.6 2.9-1.5z"/></svg>'

# ---------------------------------------------------------------- словари
L = {
    "en": {
        "a_h1": "Install the 1xCasino app and get an extra <span class=\"hl\">95 FS</span> in <span class=\"hl\">Aviatrix2</span>!",
        "i_chip1": "Free",
        "i_chip2": "~130MB",
        "i_b5_check": ["Download the 1xCasino app from the App Store", "Log in with your 1xcasino credentials", "Check that your profile personal data is filled in (Email added and verified, Phone added and verified, City, First name, Last name, Date of birth). This data is needed to improve the protection of your account and balance."],
        "i_b4_p1": "The download comes from the App Store and is completely safe.",
        "i_b7_list": ["To log in, use the details you entered during registration earlier.", "You can log into your 1xcasino account in any way that's convenient for you, using: Email, User ID, UserName or Phone.", "If you've forgotten your password, use the Forgot Password feature to recover it.", "If you have trouble logging in, send a message to info@1xcasino-guide.com with details of the problem and we'll help you."],
        "i_b8_p1": "This helps improve your account security, protect your money, and also restore access or pass verification in case of any account issues.",
        "i_b8_p2": "You need to check that the following are filled in:",
        "i_b8_rows": [["Email", "Filled in and verified"], ["Phone", "Filled in and verified"], ["First name", "Filled in"], ["Last name", "Filled in"], ["Country", "Filled in"], ["City", "Filled in"], ["Date of birth", "Filled in"]],
        "lang": "en",
        "c_sticky": "📲 Download",
        "c_sticky_and": "📲 Download Android APK",
        "c_ph1": "Image placeholder",
        "c_ph2": "replace with your screenshot",
        "h_title": "1xCasino App — Download for Android and iPhone",
        "h_desc": "Get the 1xCasino app: pick your device and follow a short install guide. Light app, fast even on a slow connection.",
        "h_h1": "Install our app and get an extra <span class=\"hl\">95 FS</span> in Aviatrix2!",
        "home_title": "1xCasino Guide — bonuses, tips and account safety",
        "home_desc": "Your 1xCasino guide: extra bonuses, gaming tips and advice on keeping your account safe.",
        "home_h1": "Welcome to <span class=\"hl\">1xCasino</span> Guideline",
        "home_lead": "Here you'll find extra bonuses, helpful gaming tips and advice on keeping your account safe.",
        "home_note": "Bookmark this page so you don't lose it",
        "c_lang": "Language",
        "h_lead": "Pick your device and get a step-by-step guide: how to install the app safely and claim your bonus!",
        "h_bens": [["🚀", "Less loading delays"], ["💳", "Safer &amp; stable payments"], ["🎁", "Get app-only bonus"], ["🔔", "Get instant winning alerts"], ["📶", "Optimized for slow internet"], ["💾", "Uses less traffic data"]],
        "h_android": "Android App",
        "h_ios": "iOS App",
        "a_title": "Download 1xCasino App for Android — online casino in Africa, Aviator, JexX",
        "a_desc": "Download the 1xCasino app for Android: online casino. A light app that runs fast even on a slow connection.",
        "a_eyebrow": "Download the 1xCasino app in",
        "a_geo_country": "your country",
        "a_lead": "Here you'll find a step-by-step guide on how to download the Android APK, install it, check security, and get your bonus!",
        "a_downloads": "57K+ downloads",
        "a_chip1": "Free",
        "a_chip2": "Android 7+",
        "a_chip3": "~25MB",
        "a_cta_hero": "📲 Download APK for Android",
        "a_b3_eye": "Benefits",
        "a_b3_h2": "Why install the Android app",
        "a_b4_eye": "Download",
        "a_b4_h2": "How to download and install the 1xCasino app",
        "a_b4_p1": "Download the file from this Guideline page.",
        "a_b4_p3": "Before opening the file, check the name, source, size and free space on your phone.",
        "a_b4_p3b": "If the installation was interrupted, download the app again and check the available memory on your phone. The app is ~25MB, but you need at least 100MB for the installation process itself.",
        "a_b4_th1": "What to check",
        "a_b4_th2": "What it should be",
        "a_b4_rows": [["Android", "Android 7+"], ["Free space", "~25MB"]],
        "a_b5_eye": "Install",
        "a_b5_h2": "How to install the 1xCasino App and get the bonus",
        "a_b6_eye": "Update",
        "a_b6_h2": "Why update the app?",
        "a_b6_p": "An old version of the app may open slowly or lose some features. In that case it's better to update the app. The update will be offered automatically.",
        "a_b7_eye": "Account",
        "a_b7_h2": "How to log in to the 1xcasino app",
        "a_b8_eye": "Account security",
        "a_b8_h2": "Check your personal data",
        "a_b8_p1": "This will help improve the security of your account, keep your money safe, and also restore access or pass verification in case of any problems with your account.",
        "a_b8_p2": "You need to check that the following is filled in:",
        "a_b9_eye": "Bonus",
        "a_b9_h2": "Promo code: 95 FS for installing and confirming your details",
        "a_b9_p": "Copy the promo code, install the app and activate the bonus when you sign up.",
        "a_copy": "Copy",
        "a_copied": "Copied!",
        "a_cta_bonus": "↓ Download and activate the bonus",
        "a_w_eye": "Bonus game",
        "a_w_h2": "Spin the wheel and grab your bonus",
        "a_w_p": "Tap the button — the wheel sets your free-spins bonus (20 to 95 FS), and the promo code is copied automatically.",
        "a_w_spin": "Spin the wheel",
        "a_w_again": "Copy promo code",
        "a_w_res1": "🎉 You got 95 FS! Promo code %s copied",
        "a_w_res2": "Promo code %s copied ✓",
        "a_b10_eye": "Payments",
        "a_b10_h2": "Deposit and withdrawal",
        "a_b10_p1": "Before a deposit, check the amount, currency, fee, limit and the owner of the payment method. A withdrawal may require identity verification.",
        "a_b10_p2": "Keep the receipt, a screenshot or the transaction number. If a payment hangs, this helps support sort it out faster.",
        "a_b10_b1": "Don't repeat a payment until its status is clear.",
        "a_b10_b2": "Don't send documents in private chats — only to official 1xCasino support.",
        "a_b10_th1": "Before paying",
        "a_b10_th2": "What to do",
        "a_b10_rows": [["Amount", "Check before confirming"], ["Currency", "Compare with your account currency"], ["Limit", "Check the minimum and maximum"], ["Status", "Wait for the result"], ["Confirmation", "Save the receipt or a screenshot"]],
        "a_b11_eye": "Security",
        "a_b11_h2": "Fair and secure",
        "a_b11": [["Data protection", "The connection and your account data are encrypted."], ["Fast payouts", "Withdraw via convenient local methods, without extra delays."], ["24/7 support", "The support team is available around the clock for any question."]],
        "a_b12_eye": "Q&A",
        "a_b12_h2": "Frequently asked questions",
        "a_b12": [["Is it safe?", "Yes. The app is downloaded from the official source and data is transmitted in encrypted form. Only download the APK from the buttons on this page."], ["Is the app free?", "Yes, downloading and installing the app are free. Only bets and topping up your balance can cost money, at your own choice."], ["What are the phone requirements?", "A smartphone with Android 7 or higher will work. The app is lightweight (~25MB) and runs even on low-cost devices."], ["How do I install the APK?", "Download the file, open it and, when prompted, allow installation from unknown sources. Then tap 'Install'. For details, see the 'How to download and install the 1xCasino app' section."], ["Is my data protected?", "Your connection and account data are transmitted in encrypted form."]],
        "a_b13_h2": "Ready to start? Install the app now and get the 95 FS bonus",
        "i_title": "Download 1xCasino App for iOS — online casino in Africa, Aviator, JexX",
        "i_desc": "Download the 1xCasino app for iOS: online casino. A lightweight app that runs fast on a weak connection.",
        "i_eyebrow": "iOS",
        "i_h1": "Get <span class=\"hl\">1xCasino</span> on your iPhone",
        "i_lead": "Here you'll find a step-by-step guide on how to download the iOS app and get your bonus!",
        "i_cta_hero": "📲 Download iOS app",
        "i_s_eye": "Install",
        "i_s_h2": "How to install on iPhone",
        "i_steps": ["Tap the button on this page — it opens the official 1xCasino page.", "Choose the iOS version of the app.", "Confirm the installation when iOS asks.", "Open 1xCasino and sign in to your account."],
        "i_alt_eye": "Alternative",
        "i_alt_h2": "If the app isn't available in your region",
        "i_alt_p1": "You can use 1xCasino as a web app — it works like the app and gets its own icon on your home screen.",
        "i_alt_steps": ["Open the 1xCasino mobile site in Safari.", "Tap the Share button (the square with an arrow).", "Choose “Add to Home Screen” and confirm."],
        "i_d_eye": "Good to know",
        "i_d_h2": "iPhone vs Android: what's different",
        "i_d_th1": "Item",
        "i_d_th2": "On iPhone",
        "i_d_rows": [["APK file", "Not needed — APK is an Android format"], ["“Unknown sources”", "No such setting — nothing to switch"], ["Updates", "Arrive automatically"], ["Account", "The same one — sign in with your usual details"]],
        "i_b12_eye": "Q&A",
        "i_b12_h2": "Frequently asked questions",
        "i_b12": [["Is it safe?", "Yes. The app is downloaded from an official source, and data is transmitted encrypted."], ["Is the app free?", "Yes, downloading and installing the app is free. Only bets and deposits can be paid, at your discretion."], ["What are the phone requirements?", "A smartphone on iOS 15.0 or higher will work. The app is lightweight (~130MB)."], ["How do I install the app?", "Go to the App Store and then tap Install. Details are in the 'How to download and install the 1xCasino app' section."], ["Is my data protected?", "The connection and account data are transmitted encrypted."]],
        "i_b13_h2": "Ready to start? Install the app right now and get the 95 FS bonus",
        "i_cta_final": "↓ Get the app for iPhone",
        "a_appname": "1xCasino",
        "a_b4_p2a": "Download the app file for",
        "a_b4_p2b": "only from the official sites 1xcasino.com, 1xcasino-af.com, 1xcasino.co.zm, 1xcasino.com.gh and from this Guideline page.",
        "a_b4_p4": "Your phone may show a warning because the file is not being installed from the Google Play Market. This is a normal security screen. You should only grant permission for the duration of the installation.",
        "a_slide_h": "Step-by-step guide",
        "a_slide_cap": "This is just placeholder text explaining the step",
        "a_b5_intro": "Here is a short step-by-step checklist:",
        "a_b5_check": ["Download the APK file", "Install the app on your phone", "Log in with your 1xcasino credentials", "Check that your personal data is filled in your profile (Email added and activated, Phone added and activated, City, First name, Last name, Date of birth). This data is needed to improve the protection of your account and balance."],
        "a_form_title": "Send us your USER ID — we'll check your account and send you a Promo code with a bonus that you can activate in the Promo codes section.",
        "a_form_ph": "USER ID, for example 1569699313",
        "a_form_btn": "Send",
        "a_form_err": "Enter a valid USER ID, for example 1569699313",
        "a_form_ok": "Done! Your email app will open — send the message and we'll check the account and send the promo code.",
        "a_form_locked": "Tick all the steps above to send your USER ID.",
        "a_b5_more": "Explore each step in detail",
        "a_prog": "Bonus unlock progress",
        "a_prog_send": "Send your User ID",
        "a_b7_list": ["To log in, use the details you provided when you registered earlier.", "You can log in to your 1xcasino account in any way that's convenient for you, using: Email, User ID, UserName or Phone.", "If you forgot your password, use the Forgot Password feature to recover it.", "If you have any trouble logging in, send a message to info@1xcasino-guide.com with the details of the problem and we'll help you."],
        "a_b8_th1": "What to check",
        "a_b8_th2": "What it should be",
        "a_b8_rows": [["Email", "Filled in and confirmed"], ["Phone", "Filled in and confirmed"], ["First name", "Filled in"], ["Last name", "Filled in"], ["Country", "Filled in"], ["City", "Filled in"], ["Date of birth", "Filled in"]],
    },
    "fr": {
        "a_h1": "Installe l'application 1xCasino et reçois <span class=\"hl\">95 FS</span> supplémentaires sur <span class=\"hl\">Aviatrix2</span> !",
        "i_chip1": "Gratuit",
        "i_chip2": "~130MB",
        "i_b5_check": ["Téléchargez l'application 1xCasino depuis l'App Store", "Connectez-vous avec vos identifiants 1xcasino", "Vérifiez le remplissage des données personnelles du profil (Email ajouté et confirmé, Téléphone ajouté et confirmé, Ville, Prénom, Nom, Date de naissance). Ces données servent à renforcer la protection de votre compte et de votre solde."],
        "i_b4_p1": "Le téléchargement provient de l'App Store et est totalement sûr.",
        "i_b7_list": ["Pour vous connecter, utilisez les données saisies lors de votre inscription.", "Vous pouvez vous connecter à votre compte 1xcasino de la manière qui vous convient, en utilisant : Email, User ID, UserName ou Phone.", "Si vous avez oublié votre mot de passe, utilisez la fonction Forgot Password pour le récupérer.", "Si vous rencontrez des difficultés de connexion, envoyez un message à info@1xcasino-guide.com avec les détails du problème et nous vous aiderons."],
        "i_b8_p1": "Cela aide à renforcer la sécurité de votre compte, à protéger votre argent, et aussi à restaurer l'accès ou passer une vérification en cas de problème avec le compte.",
        "i_b8_p2": "Vous devez vérifier le remplissage de :",
        "i_b8_rows": [["Email", "Rempli et confirmé"], ["Téléphone", "Rempli et confirmé"], ["Prénom", "Rempli"], ["Nom", "Rempli"], ["Pays", "Rempli"], ["Ville", "Rempli"], ["Date de naissance", "Rempli"]],
        "lang": "fr",
        "c_sticky": "📲 Télécharger",
        "c_sticky_and": "📲 Télécharger l'APK Android",
        "c_ph1": "Image — espace réservé",
        "c_ph2": "remplace par ta capture d'écran",
        "h_title": "Application 1xCasino — télécharger pour Android et iPhone",
        "h_desc": "Installe l'application 1xCasino : choisis ton appareil et suis un guide d'installation rapide. Application légère, rapide même avec une connexion lente.",
        "h_h1": "Installe notre application et reçois <span class=\"hl\">95 FS</span> supplémentaires sur Aviatrix2 !",
        "home_title": "Guide 1xCasino — bonus, conseils et sécurité du compte",
        "home_desc": "Ton guide 1xCasino : bonus supplémentaires, conseils de jeu et astuces pour sécuriser ton compte.",
        "home_h1": "Bienvenue sur <span class=\"hl\">1xCasino</span> Guideline",
        "home_lead": "Ici tu trouveras des bonus supplémentaires, des conseils de jeu utiles et des astuces pour sécuriser ton compte.",
        "home_note": "Ajoute cette page à tes favoris pour ne pas la perdre",
        "c_lang": "Langue",
        "h_lead": "Choisis ton appareil et reçois un guide pas à pas : comment installer l'application en toute sécurité et récupérer ton bonus !",
        "h_bens": [["🚀", "Moins d'attente au chargement"], ["💳", "Paiements sûrs et stables"], ["🎁", "Bonus exclusif dans l'app"], ["🔔", "Alertes de gains instantanées"], ["📶", "Optimisée pour les connexions lentes"], ["💾", "Moins de données consommées"]],
        "h_android": "Application Android",
        "h_ios": "Application iOS",
        "a_title": "Télécharger l'application 1xCasino pour Android — casino en ligne en Afrique, Aviator, JexX",
        "a_desc": "Télécharge l'application 1xCasino pour Android : casino en ligne. Application légère et rapide même avec une connexion lente.",
        "a_eyebrow": "Téléchargez l'application 1xCasino —",
        "a_geo_country": "ton pays",
        "a_lead": "Ici tu trouveras un guide étape par étape pour télécharger l'APK Android, l'installer, vérifier la sécurité et obtenir ton bonus !",
        "a_downloads": "57K+ téléchargements",
        "a_chip1": "Gratuit",
        "a_chip2": "Android 7+",
        "a_chip3": "~25MB",
        "a_cta_hero": "📲 Télécharger l'APK pour Android",
        "a_b3_eye": "Avantages",
        "a_b3_h2": "Pourquoi installer l'application Android",
        "a_b4_eye": "Téléchargement",
        "a_b4_h2": "Comment télécharger et installer l'application 1xCasino",
        "a_b4_p1": "Téléchargez le fichier depuis cette page Guideline.",
        "a_b4_p3": "Avant d'ouvrir le fichier, vérifiez le nom, la source, la taille et l'espace libre sur votre téléphone.",
        "a_b4_p3b": "Si l'installation a été interrompue, téléchargez à nouveau l'application et vérifiez la mémoire disponible sur votre téléphone. L'application pèse ~25MB, mais il vous faut au moins 100MB pour le processus d'installation.",
        "a_b4_th1": "À vérifier",
        "a_b4_th2": "Ce qui est attendu",
        "a_b4_rows": [["Android", "Android 7+"], ["Espace libre", "~25MB"]],
        "a_b5_eye": "Installation",
        "a_b5_h2": "Comment installer l'application 1xCasino et obtenir le bonus",
        "a_b6_eye": "Mise à jour",
        "a_b6_h2": "Pourquoi mettre à jour l'application ?",
        "a_b6_p": "Une ancienne version de l'application peut s'ouvrir lentement ou perdre certaines fonctions. Dans ce cas, il vaut mieux mettre à jour l'application. La mise à jour sera proposée automatiquement.",
        "a_b7_eye": "Compte",
        "a_b7_h2": "Comment se connecter à l'application 1xcasino",
        "a_b8_eye": "Sécurité du compte",
        "a_b8_h2": "Vérifiez vos données personnelles",
        "a_b8_p1": "Cela aidera à renforcer la sécurité de votre compte, à protéger votre argent, ainsi qu'à restaurer l'accès ou à passer la vérification en cas de problème avec votre compte.",
        "a_b8_p2": "Vous devez vérifier que les éléments suivants sont renseignés :",
        "a_b9_eye": "Bonus",
        "a_b9_h2": "Code promo : 95 FS pour l'installation et la confirmation des données",
        "a_b9_p": "Copie le code promo, installe l'application et active le bonus à l'inscription.",
        "a_copy": "Copier",
        "a_copied": "Copié !",
        "a_cta_bonus": "↓ Télécharger et activer le bonus",
        "a_w_eye": "Jeu bonus",
        "a_w_h2": "Fais tourner la roue et prends ton bonus",
        "a_w_p": "Appuie sur le bouton — la roue détermine ton bonus en free spins (de 20 à 95 FS), et le code promo est copié automatiquement.",
        "a_w_spin": "Lancer la roue",
        "a_w_again": "Copier le code promo",
        "a_w_res1": "🎉 95 FS ! Le code promo %s est copié",
        "a_w_res2": "Code promo %s copié ✓",
        "a_b10_eye": "Paiements",
        "a_b10_h2": "Dépôt et retrait",
        "a_b10_p1": "Avant un dépôt, vérifie le montant, la devise, les frais, la limite et le titulaire du moyen de paiement. Un retrait peut demander une vérification d'identité.",
        "a_b10_p2": "Garde le reçu, une capture d'écran ou le numéro d'opération. Si un paiement reste bloqué, cela aide le support à comprendre plus vite.",
        "a_b10_b1": "Ne répète pas un paiement tant que son statut n'est pas clair.",
        "a_b10_b2": "N'envoie pas de documents en messages privés — uniquement au support officiel 1xCasino.",
        "a_b10_th1": "Avant le paiement",
        "a_b10_th2": "Quoi faire",
        "a_b10_rows": [["Montant", "Vérifier avant de confirmer"], ["Devise", "Comparer avec la devise du compte"], ["Limite", "Voir le minimum et le maximum"], ["Statut", "Attendre le résultat de l'opération"], ["Confirmation", "Garder le reçu ou une capture"]],
        "a_b11_eye": "Sécurité",
        "a_b11_h2": "Honnête et sécurisé",
        "a_b11": [["Protection des données", "La connexion et les données du compte sont chiffrées."], ["Retraits rapides", "Retrait via des méthodes locales pratiques, sans délais inutiles."], ["Support 24/7", "L'équipe de support est disponible à tout moment pour toute question."]],
        "a_b12_eye": "Questions-réponses",
        "a_b12_h2": "Questions fréquentes",
        "a_b12": [["Est-ce sûr ?", "Oui. L'application est téléchargée depuis la source officielle et les données sont transmises sous forme chiffrée. Téléchargez l'APK uniquement via les boutons de cette page."], ["L'application est-elle gratuite ?", "Oui, le téléchargement et l'installation de l'application sont gratuits. Seuls les paris et le rechargement de votre solde peuvent être payants, selon votre choix."], ["Quelle est la configuration requise ?", "Un smartphone sous Android 7 ou plus convient. L'application est légère (~25MB) et fonctionne même sur les appareils d'entrée de gamme."], ["Comment installer l'APK ?", "Téléchargez le fichier, ouvrez-le et, à l'invite, autorisez l'installation depuis des sources inconnues. Appuyez ensuite sur « Installer ». Pour les détails, voir la section « Comment télécharger et installer l'application 1xCasino »."], ["Mes données sont-elles protégées ?", "Votre connexion et les données de votre compte sont transmises sous forme chiffrée."]],
        "a_b13_h2": "Prêt à commencer ? Installe l'application maintenant et reçois le bonus de 95 FS",
        "i_title": "Télécharger l'application 1xCasino pour iOS — casino en ligne en Afrique, Aviator, JexX",
        "i_desc": "Télécharge l'application 1xCasino pour iOS : casino en ligne. Application légère qui fonctionne vite sur une connexion faible.",
        "i_eyebrow": "iOS",
        "i_h1": "Installe <span class=\"hl\">1xCasino</span> sur ton iPhone",
        "i_lead": "Ici tu trouveras un guide étape par étape pour télécharger l'application iOS et obtenir ton bonus !",
        "i_cta_hero": "📲 Télécharger l'app iOS",
        "i_s_eye": "Installation",
        "i_s_h2": "Comment installer sur iPhone",
        "i_steps": ["Appuie sur le bouton de cette page — il ouvre la page officielle 1xCasino.", "Choisis la version iOS de l'application.", "Confirme l'installation quand iOS le demande.", "Ouvre 1xCasino et connecte-toi à ton compte."],
        "i_alt_eye": "Alternative",
        "i_alt_h2": "Si l'application n'est pas disponible dans ta région",
        "i_alt_p1": "Tu peux utiliser 1xCasino comme application web — elle fonctionne comme l'app et a sa propre icône sur l'écran d'accueil.",
        "i_alt_steps": ["Ouvre le site mobile 1xCasino dans Safari.", "Appuie sur le bouton Partager (le carré avec une flèche).", "Choisis « Sur l'écran d'accueil » et confirme."],
        "i_d_eye": "Bon à savoir",
        "i_d_h2": "iPhone vs Android : les différences",
        "i_d_th1": "Élément",
        "i_d_th2": "Sur iPhone",
        "i_d_rows": [["Fichier APK", "Inutile — l'APK est un format Android"], ["« Sources inconnues »", "Ce réglage n'existe pas — rien à activer"], ["Mises à jour", "Arrivent automatiquement"], ["Compte", "Le même — connecte-toi avec tes données habituelles"]],
        "i_b12_eye": "Questions-réponses",
        "i_b12_h2": "Questions fréquentes",
        "i_b12": [["Est-ce sûr ?", "Oui. L'application est téléchargée depuis une source officielle et les données sont transmises chiffrées."], ["L'application est-elle gratuite ?", "Oui, le téléchargement et l'installation de l'application sont gratuits. Seuls les paris et les dépôts peuvent être payants, selon votre choix."], ["Quelles sont les exigences du téléphone ?", "Un smartphone sous iOS 15.0 ou supérieur convient. L'application est légère (~130MB)."], ["Comment installer l'application ?", "Allez sur l'App Store puis appuyez sur « Installer ». Détails dans la section « Comment télécharger et installer l'application 1xCasino »."], ["Mes données sont-elles protégées ?", "La connexion et les données du compte sont transmises chiffrées."]],
        "i_b13_h2": "Prêt à commencer ? Installe l'application maintenant et reçois le bonus de 95 FS",
        "i_cta_final": "↓ Obtenir l'application iPhone",
        "a_appname": "1xCasino",
        "a_b4_p2a": "Téléchargez le fichier de l'application —",
        "a_b4_p2b": "uniquement depuis les sites officiels 1xcasino.com, 1xcasino-af.com, 1xcasino.co.zm, 1xcasino.com.gh et depuis cette page Guideline.",
        "a_b4_p4": "Votre téléphone peut afficher un avertissement car le fichier n'est pas installé depuis le Google Play Market. C'est un écran de sécurité normal. N'accordez l'autorisation que le temps de l'installation.",
        "a_slide_h": "Guide étape par étape",
        "a_slide_cap": "Ceci n'est qu'un texte provisoire expliquant l'étape",
        "a_b5_intro": "Voici une courte checklist étape par étape :",
        "a_b5_check": ["Télécharger le fichier APK", "Installer l'application sur le téléphone", "Se connecter avec vos identifiants 1xcasino", "Vérifier que vos données personnelles sont renseignées dans le profil (Email ajouté et activé, Téléphone ajouté et activé, Ville, Prénom, Nom, Date de naissance). Ces données servent à renforcer la protection de votre compte et de votre solde."],
        "a_form_title": "Envoyez votre USER ID, nous vérifierons votre compte et vous enverrons un code promo avec un bonus que vous pourrez activer dans la section Codes promo.",
        "a_form_ph": "USER ID, par exemple 1569699313",
        "a_form_btn": "Envoyer",
        "a_form_err": "Saisissez un USER ID valide, par exemple 1569699313",
        "a_form_ok": "C'est fait ! Votre messagerie va s'ouvrir — envoyez le message et nous vérifierons le compte et enverrons le code promo.",
        "a_form_locked": "Cochez toutes les étapes ci-dessus pour envoyer votre USER ID.",
        "a_b5_more": "Découvrir chaque étape en détail",
        "a_prog": "Progression du déblocage du bonus",
        "a_prog_send": "Envoyez votre User ID",
        "a_b7_list": ["Pour vous connecter, utilisez les informations que vous avez indiquées lors de votre inscription.", "Vous pouvez vous connecter à votre compte 1xcasino de la manière qui vous convient, en utilisant : Email, User ID, UserName ou Phone.", "Si vous avez oublié votre mot de passe, utilisez la fonction Forgot Password pour le récupérer.", "Si vous rencontrez des difficultés pour vous connecter, envoyez un message à info@1xcasino-guide.com en précisant le problème, et nous vous aiderons."],
        "a_b8_th1": "À vérifier",
        "a_b8_th2": "Ce qui est attendu",
        "a_b8_rows": [["Email", "Renseigné et confirmé"], ["Téléphone", "Renseigné et confirmé"], ["Prénom", "Renseigné"], ["Nom", "Renseigné"], ["Pays", "Renseigné"], ["Ville", "Renseigné"], ["Date de naissance", "Renseignée"]],
    },
    "ru": {
        "a_h1": "Установи приложение 1xCasino и получи дополнительные <span class=\"hl\">95 FS</span> в <span class=\"hl\">Aviatrix2</span>!",
        "i_chip1": "Бесплатно",
        "i_chip2": "~130MB",
        "i_b5_check": ["Скачать c App Store 1xCasino приложение", "Выполнить LogIn с вашими доступами к 1xcasino", "Проверить заполнение персональных данных в профиле (Email добавлен и активирован, Телефон добавлен и активирован, Город, Имя, Фамилия, Дата рождения). Эти данные нужны для повышения защиты Вашего аккаунта и счёта."],
        "i_b4_p1": "Загрузка происходит с App Store и полностью безопасна.",
        "i_b7_list": ["Для входа используйте свои данные, которые вы указывали во время регистрации ранее.", "Вы можете войти в аккаунт 1xcasino любым удобным для вас способом, используя: Email, User ID, UserName или Phone.", "Если вы забыли пароль, то воспользуйтесь функцией Forgot Password для восстановления.", "Если у вас возникают трудности с входом, то отправьте сообщение на info@1xcasino-guide.com с деталями проблемы, мы Вам поможем."],
        "i_b8_p1": "Это поможет повысить безопасность вашего аккаунта, сохранить Ваши деньги, а также восстановить доступ или пройти проверку в случае любых проблем с аккаунтом.",
        "i_b8_p2": "Необходимо проверить заполнение:",
        "i_b8_rows": [["Email", "Заполнен и подтверждён"], ["Телефон", "Заполнен и подтверждён"], ["Имя", "Заполнено"], ["Фамилия", "Заполнено"], ["Страна", "Заполнено"], ["Город", "Заполнено"], ["Дата рождения", "Заполнено"]],
        "lang": "ru",
        "c_sticky": "📲 Скачать",
        "c_sticky_and": "📲 Скачать Android APK",
        "c_ph1": "Изображение — заглушка",
        "c_ph2": "замени на свой скриншот",
        "h_title": "Приложение 1xCasino — скачать для Android и iPhone",
        "h_desc": "Установи приложение 1xCasino: выбери устройство и следуй короткой инструкции. Лёгкое приложение, быстро работает на слабом интернете.",
        "h_h1": "Установи наше приложение и получи дополнительные <span class=\"hl\">95 FS</span> в Aviatrix2!",
        "home_title": "Гид 1xCasino — бонусы, советы и безопасность аккаунта",
        "home_desc": "Твой гид по 1xCasino: дополнительные бонусы, советы по играм и безопасности аккаунта.",
        "home_h1": "Приветствуем на <span class=\"hl\">1xCasino</span> Guideline",
        "home_lead": "Здесь ты найдёшь дополнительные бонусы, полезные советы по играм и безопасности твоего аккаунта.",
        "home_note": "Сохрани страницу в закладки, чтобы не потерять",
        "c_lang": "Язык",
        "h_lead": "Выбирай своё устройство и получай пошаговую инструкцию, как безопасно установить приложение и получить бонус!",
        "h_bens": [["🚀", "Меньше задержек загрузки"], ["💳", "Безопасные и стабильные платежи"], ["🎁", "Бонус только в приложении"], ["🔔", "Мгновенные уведомления о выигрышах"], ["📶", "Оптимизировано для слабого интернета"], ["💾", "Меньше расхода трафика"]],
        "h_android": "Android App",
        "h_ios": "iOS App",
        "a_title": "Скачать приложение 1xCasino для Android — онлайн казино в Африке, Aviator, JexX",
        "a_desc": "Скачай приложение 1xCasino для Android: онлайн-казино. Лёгкое приложение, быстро работает на слабом интернете.",
        "a_eyebrow": "Скачай приложение 1xCasino в",
        "a_geo_country": "своей стране",
        "a_lead": "Здесь ты найдёшь пошаговую инструкцию, как скачать Android APK, установить, проверить безопасность и получить бонус!",
        "a_downloads": "57K+ загрузок",
        "a_chip1": "Бесплатно",
        "a_chip2": "Android 7+",
        "a_chip3": "~25MB",
        "a_cta_hero": "📲 Скачать APK для Android",
        "a_b3_eye": "Преимущества",
        "a_b3_h2": "Почему стоит установить Android-приложение",
        "a_b4_eye": "Загрузка",
        "a_b4_h2": "Как скачать и установить 1xCasino приложение",
        "a_b4_p1": "Скачивайте файл с текущей Guideline страницы.",
        "a_b4_p3": "Перед открытием файла проверьте имя, источник, размер и свободное место на телефоне.",
        "a_b4_p3b": "Если установка прервалась, скачайте приложение заново и проверьте доступную память на вашем телефоне. Вес приложения ~25MB, но вам необходимо как минимум 100MB для самого процесса установки.",
        "a_b4_th1": "Что проверить",
        "a_b4_th2": "Что должно быть",
        "a_b4_rows": [["Android", "Android 7+"], ["Свободная память", "~25MB"]],
        "a_b5_eye": "Установка",
        "a_b5_h2": "Как установить 1xCasino App и получить бонус",
        "a_b6_eye": "Обновление",
        "a_b6_h2": "Зачем обновлять приложение?",
        "a_b6_p": "Старая версия приложения может открываться медленно или терять часть функций. В таком случае лучше обновить приложение. Обновление будет предложено автоматически.",
        "a_b7_eye": "Аккаунт",
        "a_b7_h2": "Как выполнить логин в 1xcasino приложение",
        "a_b8_eye": "Безопасность аккаунта",
        "a_b8_h2": "Проверьте Ваши персональные данные",
        "a_b8_p1": "Это поможет повысить безопасность вашего аккаунта, сохранить Ваши деньги, а также восстановить доступ или пройти проверку в случае любых проблем с аккаунтом.",
        "a_b8_p2": "Необходимо проверить заполнение:",
        "a_b9_eye": "Бонус",
        "a_b9_h2": "Промокод на бонус 95 FS за установку и подтверждение данных",
        "a_b9_p": "Скопируй промокод, установи приложение и активируй бонус при регистрации.",
        "a_copy": "Скопировать",
        "a_copied": "Скопировано!",
        "a_cta_bonus": "↓ Скачать и активировать бонус",
        "a_w_eye": "Бонус-игра",
        "a_w_h2": "Крути рулетку и забери бонус",
        "a_w_p": "Нажми кнопку — рулетка определит твой бонус в фриспинах (от 20 до 95 FS), и промокод скопируется автоматически.",
        "a_w_spin": "Крутить рулетку",
        "a_w_again": "Скопировать промокод",
        "a_w_res1": "🎉 Выпало 95 FS! Промокод %s скопирован",
        "a_w_res2": "Промокод %s скопирован ✓",
        "a_b10_eye": "Платежи",
        "a_b10_h2": "Депозит и вывод",
        "a_b10_p1": "Перед депозитом проверьте сумму, валюту, комиссию, лимит и владельца платёжного метода. Для вывода может понадобиться проверка личности.",
        "a_b10_p2": "Сохраните чек, скриншот или номер операции. Если платёж зависнет, эта информация поможет поддержке быстрее понять ситуацию.",
        "a_b10_b1": "Не повторяйте платёж, пока статус не ясен.",
        "a_b10_b2": "Не отправляйте документы в личные чаты — только в официальную поддержку 1xCasino.",
        "a_b10_th1": "Перед платежом",
        "a_b10_th2": "Что сделать",
        "a_b10_rows": [["Сумма", "Проверить до подтверждения"], ["Валюта", "Сравнить с валютой аккаунта"], ["Лимит", "Посмотреть минимум и максимум"], ["Статус", "Дождаться результата операции"], ["Подтверждение", "Сохранить чек или скриншот"]],
        "a_b11_eye": "Безопасность",
        "a_b11_h2": "Честно и безопасно",
        "a_b11": [["Защита данных", "Соединение и данные аккаунта передаются в зашифрованном виде."], ["Быстрые выплаты", "Вывод средств удобными локальными методами, без лишних задержек."], ["Поддержка 24/7", "Команда поддержки на связи круглосуточно и поможет с любым вопросом."]],
        "a_b12_eye": "Вопросы и ответы",
        "a_b12_h2": "Частые вопросы",
        "a_b12": [["Это безопасно?", "Да. Приложение скачивается с официального источника, данные передаются в зашифрованном виде. Загружай APK только по кнопкам на этой странице."], ["Приложение бесплатное?", "Да, скачивание и установка приложения бесплатны. Платными могут быть только ставки и пополнение счёта по твоему желанию."], ["Какие требования к телефону?", "Подойдёт смартфон на Android 7 и выше. Приложение лёгкое (~25MB) и работает даже на недорогих устройствах."], ["Как установить APK?", "Скачай файл, открой его и при запросе разреши установку из неизвестных источников. Затем нажми «Установить». Подробно — в блоке «Как скачать и установить 1xCasino приложение»."], ["Мои данные защищены?", "Соединение и данные аккаунта передаются в зашифрованном виде."]],
        "a_b13_h2": "Готов начать? Установи приложение прямо сейчас и получи бонус 95 FS",
        "i_title": "Скачать приложение 1xCasino для iOS — онлайн казино в Африке, Aviator, JexX",
        "i_desc": "Скачай приложение 1xCasino для iOS: онлайн-казино. Лёгкое приложение, быстро работает на слабом интернете.",
        "i_eyebrow": "iOS",
        "i_h1": "Установи <span class=\"hl\">1xCasino</span> на свой iPhone",
        "i_lead": "Здесь ты найдёшь пошаговую инструкцию, как скачать IOS приложение и получить бонус!",
        "i_cta_hero": "📲 Скачать iOS приложение",
        "i_s_eye": "Установка",
        "i_s_h2": "Как установить на iPhone",
        "i_steps": ["Нажми кнопку на этой странице — она откроет официальную страницу 1xCasino.", "Выбери iOS-версию приложения.", "Подтверди установку, когда iOS спросит.", "Открой 1xCasino и войди в аккаунт."],
        "i_alt_eye": "Альтернатива",
        "i_alt_h2": "Если приложение недоступно в твоём регионе",
        "i_alt_p1": "Можно пользоваться 1xCasino как веб-приложением — оно работает как обычное приложение и получает свою иконку на экране «Домой».",
        "i_alt_steps": ["Открой мобильный сайт 1xCasino в Safari.", "Нажми кнопку «Поделиться» (квадрат со стрелкой).", "Выбери «На экран «Домой»» и подтверди."],
        "i_d_eye": "Полезно знать",
        "i_d_h2": "iPhone и Android: в чём разница",
        "i_d_th1": "Пункт",
        "i_d_th2": "На iPhone",
        "i_d_rows": [["APK-файл", "Не нужен — APK это формат Android"], ["«Неизвестные источники»", "Такой настройки нет — ничего включать не надо"], ["Обновления", "Приходят автоматически"], ["Аккаунт", "Тот же самый — входи со своими обычными данными"]],
        "i_b12_eye": "Вопросы и ответы",
        "i_b12_h2": "Частые вопросы",
        "i_b12": [["Это безопасно?", "Да. Приложение скачивается с официального источника, данные передаются в зашифрованном виде."], ["Приложение бесплатное?", "Да, скачивание и установка приложения бесплатны. Платными могут быть только ставки и пополнение счёта по твоему желанию."], ["Какие требования к телефону?", "Подойдёт смартфон на iOS 15.0 и выше. Приложение лёгкое (~130MB)."], ["Как установить приложение?", "Перейди в App Store и затем нажми «Установить». Подробно — в блоке «Как скачать и установить 1xCasino приложение»."], ["Мои данные защищены?", "Соединение и данные аккаунта передаются в зашифрованном виде."]],
        "i_b13_h2": "Готов начать? Установи приложение прямо сейчас и получи бонус 95 FS",
        "i_cta_final": "↓ Получить приложение для iPhone",
        "a_appname": "1xCasino",
        "a_b4_p2a": "Скачивайте файл с приложением для",
        "a_b4_p2b": "только с официальных сайтов 1xcasino.com, 1xcasino-af.com, 1xcasino.co.zm, 1xcasino.com.gh и с текущей Guideline страницы.",
        "a_b4_p4": "Ваш телефон может показать предупреждение, потому что файл ставится не из Google Play Market. Это нормальный экран безопасности. Разрешение стоит давать только на время установки.",
        "a_slide_h": "Пошаговая инструкция",
        "a_slide_cap": "Это просто текст-заглушка с объяснением шага",
        "a_b5_intro": "Ниже приведён краткий пошаговый чеклист:",
        "a_b5_check": ["Скачать APK файл", "Установить приложение на телефон", "Выполнить LogIn с вашими доступами к 1xcasino", "Проверить заполнение персональных данных в профиле (Email добавлен и активирован, Телефон добавлен и активирован, Город, Имя, Фамилия, Дата рождения). Эти данные нужны для повышения защиты Вашего аккаунта и счёта."],
        "a_form_title": "Отправьте Ваш USER ID, мы проверим ваш аккаунт и отправим Вам Промокод с бонусом, который вы сможете активировать в разделе Промокодов.",
        "a_form_ph": "USER ID, например 1569699313",
        "a_form_btn": "Отправить",
        "a_form_err": "Введите корректный USER ID, например 1569699313",
        "a_form_ok": "Готово! Откроется почта — отправьте письмо, и мы проверим аккаунт и пришлём промокод.",
        "a_form_locked": "Отметьте все шаги выше, чтобы отправить USER ID.",
        "a_b5_more": "Изучить каждый шаг подробно",
        "a_prog": "Прогресс разблокировки бонуса",
        "a_prog_send": "Отправь твою User ID",
        "a_b7_list": ["Для входа используйте свои данные, которые вы указывали во время регистрации ранее.", "Вы можете войти в аккаунт 1xcasino любым удобным для вас способом, используя: Email, User ID, UserName или Phone.", "Если вы забыли пароль, то воспользуйтесь функцией Forgot Password для восстановления.", "Если у вас возникают трудности с входом, то отправьте сообщение на info@1xcasino-guide.com с деталями проблемы, мы Вам поможем."],
        "a_b8_th1": "Что проверить",
        "a_b8_th2": "Что должно быть",
        "a_b8_rows": [["Email", "Заполнен и подтверждён"], ["Телефон", "Заполнен и подтверждён"], ["Имя", "Заполнено"], ["Фамилия", "Заполнено"], ["Страна", "Заполнено"], ["Город", "Заполнено"], ["Дата рождения", "Заполнено"]],
    },
}

# ------------------------------------------------------------ helpers
def head(t, title, desc, page):  # page: "" | "app/" | "android/" | "ios/" | "draft/"
    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#160241">
<link rel="manifest" href="/manifest.json">
 <link rel="icon" href="/assets/1xcasino.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/icons/icon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="1XC Guide">
<meta name="robots" content="index, follow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/{page}">
<link rel="alternate" hreflang="fr" href="{DOMAIN}/fr/{page}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{page}">
<style>{CSS}</style>
</head>
"""

UI_LANGS = [("en", "English"), ("fr", "Fran\u00e7ais")]

def langsw(t, page):
    items = ""
    for code, name in UI_LANGS:
        href = "/" + ("" if code == "en" else code + "/") + page
        cur = ' aria-current="true"' if t["lang"] == code else ""
        items += f'<a href="{href}"{cur}>{name}</a>'
    return f'<nav class="langsw" aria-label="Language">{items}</nav>'

def header(t, page):
    home = "/" + ("" if t["lang"] == "en" else t["lang"] + "/")
    return f"""<header class="site-header">
  <a class="brand" href="{home}" aria-label="1xCasino">
    <img class="brand__logo" src="{LOGO}" alt="1xCasino" height="20" decoding="async">
  </a>
  <label for="navtoggle" class="burger" aria-label="Menu"><span></span><span></span><span></span></label>
</header>
<input type="checkbox" id="navtoggle" class="nav-cb">
<label for="navtoggle" class="scrim" aria-hidden="true"></label>
<div class="menu-layer">
  <aside class="drawer" aria-label="Menu">
    <label for="navtoggle" class="drawer__close" aria-label="Close">×</label>
    <div class="drawer__sec">
      <span class="drawer__h">{t['c_lang']}</span>
      {langsw(t, page)}
    </div>
    <div class="drawer__sec drawer__apps">
      <a class="btn btn--block" href="{home}android/">{ANDROID_ICON} {t['h_android']}</a>
      <a class="btn btn--block btn--violet" href="{home}ios/">{APPLE_ICON} {t['h_ios']}</a>
    </div>
  </aside>
</div>
"""


def footer(t, page):
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer__contact"><a class="footer__mail" href="mailto:info@1xcasino-guide.com?subject=1xCasino%20Guide">info@1xcasino-guide.com</a></div>
    <div class="footer__copy">Copyright © {YEAR} «1xCasino»</div>
    <div class="footer__bottom">
      <span class="badge-18">18+</span>
    </div>
  </div>
</footer>
"""


def js_base():
    return """<script>
(function(){
  var y=document.getElementById('y'); if(y) y.textContent=new Date().getFullYear();
  if('IntersectionObserver' in window){
    document.documentElement.classList.add('js');
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    },{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });
  }
})();
</script>"""

def js_android(t):
    return """<script>
(function(){
  var y=document.getElementById('y'); if(y) y.textContent=new Date().getFullYear();
  function copyText(text,onDone){
    function done(){ if(onDone) onDone(); }
    function fallback(){
      var ta=document.createElement('textarea'); ta.value=text; ta.style.position='fixed'; ta.style.opacity='0';
      document.body.appendChild(ta); ta.select();
      try{ document.execCommand('copy'); }catch(e){} document.body.removeChild(ta); done();
    }
    if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(done,fallback); }
    else { fallback(); }
  }
  var copyBtn=document.getElementById('copyPromo');
  if(copyBtn){
    copyBtn.addEventListener('click',function(){
      var code=copyBtn.getAttribute('data-code')||'';
      var label=copyBtn.querySelector('.copy-label');
      copyText(code,function(){ var o=label.textContent; label.textContent=__COPIED__; setTimeout(function(){label.textContent=o;},1500); });
    });
  }
  // Wheel: always lands on 95 FS \u2014 a real fixed bonus for everyone
  var wheel=document.getElementById('wheel'),spinBtn=document.getElementById('spinBtn'),result=document.getElementById('wheelResult');
  if(wheel&&spinBtn&&result){
    var PROMO=__PROMO__,spun=false;
    var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function reveal(){
      copyText(PROMO,function(){
        result.hidden=false; result.textContent=__RES1__;
        spinBtn.disabled=false; spinBtn.querySelector('.spin-label').textContent=__AGAIN__;
      });
    }
    spinBtn.addEventListener('click',function(){
      if(!spun){
        spun=true; spinBtn.disabled=true;
        if(reduce){ wheel.style.transform='rotate(1777.5deg)'; reveal(); return; }
        var deg=1777.5+(Math.random()*24-12);
        wheel.style.transform='rotate('+deg+'deg)';
        setTimeout(reveal,4200);
      } else {
        copyText(PROMO,function(){ result.textContent=__RES2__; });
      }
    });
  }
  // B5* install flow: sequential checklist + gated form + auto-checkbox + progress
  var root=document.getElementById('install');
  if(root){
    var cks=[].slice.call(document.querySelectorAll('#dckl .ckl__cb'));
    var formChk=document.getElementById('dformChk');
    var dform=document.getElementById('dform'),duid=document.getElementById('duid'),dsend=document.getElementById('dsend'),dlock=document.getElementById('dlock'),dmsg=document.getElementById('dmsg');
    var dmask=document.getElementById('dmask'),dtxt=document.getElementById('dtxt'),dbar=document.getElementById('dbar'),sent=false;
    function validId(v){return /^[0-9]{8,12}$/.test(v);}
    function chkCount(){var n=0;for(var i=0;i<cks.length;i++){if(cks[i].checked)n++;}return n;}
    function allDone(){return cks.length>0&&chkCount()===cks.length;}
    function syncSeq(){
      for(var i=0;i<cks.length;i++){
        var en=(i===0)||cks[i-1].checked;
        if(!en&&cks[i].checked)cks[i].checked=false;
        cks[i].disabled=!en;
        var row=cks[i].parentNode;
        if(row&&row.classList)row.classList.toggle('is-locked',!en);
      }
    }
    function updateBar(){
      if(!dmask)return;
      var n=chkCount();var pct=sent?100:Math.min(n*20,80);
      dmask.style.width=(100-pct)+'%';
      if(dbar)dbar.setAttribute('aria-valuenow',pct);
      if(dtxt)dtxt.textContent=(n>=cks.length&&cks.length>0)?__PSEND__:__PROG__;
    }
    function openForm(){
      var open=allDone();
      if(dform)dform.classList.toggle('is-locked',!open);
      if(dlock)dlock.style.display=open?'none':'';
      if(formChk)formChk.checked=open;
      if(dsend)dsend.disabled=!open;
      updateBar();
    }
    for(var i=0;i<cks.length;i++){cks[i].addEventListener('change',function(){syncSeq();openForm();});}
    if(duid)duid.addEventListener('input',function(){if(dmsg)dmsg.hidden=true;});
    if(dsend)dsend.addEventListener('click',function(){
      if(!allDone())return;
      var v=duid.value.trim();
      if(!validId(v)){if(dmsg){dmsg.hidden=false;dmsg.className='bform__msg err';dmsg.textContent=__DERR__;}return;}
      window.location.href='mailto:info@1xcasino-guide.com?subject='+encodeURIComponent('App Bonus for USER ID '+v)+'&body='+encodeURIComponent('USER ID '+v);
      sent=true;updateBar();
      if(dmsg){dmsg.hidden=false;dmsg.className='bform__msg ok';dmsg.textContent=__DOK__;}
    });
    syncSeq();openForm();
  }
  if('IntersectionObserver' in window){
    document.documentElement.classList.add('js');
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    },{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });
  }
})();
</script>""".replace("__COPIED__", json.dumps(t["a_copied"], ensure_ascii=False)).replace("__PROMO__", json.dumps(PROMO, ensure_ascii=False)) \
   .replace("__RES1__", json.dumps(t["a_w_res1"] % PROMO, ensure_ascii=False)).replace("__RES2__", json.dumps(t["a_w_res2"] % PROMO, ensure_ascii=False)) \
   .replace("__AGAIN__", json.dumps(t["a_w_again"], ensure_ascii=False)) \
   .replace("__PROG__", json.dumps(t["a_prog"], ensure_ascii=False)).replace("__PSEND__", json.dumps(t["a_prog_send"], ensure_ascii=False)) \
   .replace("__DERR__", json.dumps(INSTALL_TXT[t["lang"]]["valerr"], ensure_ascii=False)).replace("__DOK__", json.dumps(t["a_form_ok"], ensure_ascii=False))

def img_ph(t):
    return f'<div class="img-ph" role="img" aria-label="{t["c_ph1"]}">{t["c_ph1"]}<small>{t["c_ph2"]}</small></div>'

def tbl(th1, th2, rows):
    body = "\n".join(f"        <tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
    return f"""    <table class="tbl">
      <thead><tr><th>{th1}</th><th>{th2}</th></tr></thead>
      <tbody>
{body}
      </tbody>
    </table>"""

# ============================================================ shared data
REVIEWS = {
 "ru": [(1,5,"Приложение работает стабильно, игры запускаются быстро — очень доволен!"),(2,4.5,"Удобный вход, приложение всегда доступно, интерфейс в целом понятный."),(3,5,"Работает стабильнее, чем сайт: выше безопасность и надёжность платежей."),(4,4,"Нравятся дополнительные бонусы и более простой, понятный интерфейс."),(5,5,"Игры работают стабильнее и не зависают, платежи и выводы удобные и безопасные.")],
 "en": [(1,5,"The app runs smoothly and games load fast — I really like it!"),(2,4.5,"Logging in is easy, the app is always available, and the interface is clear overall."),(3,5,"It works more reliably than the website, with better security and more stable payments."),(4,4,"I like the extra bonuses and the simpler, clearer interface."),(5,5,"Games run more smoothly without freezing, and deposits and withdrawals are easy and secure.")],
 "fr": [(1,5,"L'application est stable et les jeux se lancent vite — j'adore !"),(2,4.5,"Connexion facile, l'application est toujours accessible et l'interface est claire dans l'ensemble."),(3,5,"Plus stable que le site web, avec une meilleure sécurité et des paiements plus fiables."),(4,4,"J'aime les bonus supplémentaires et l'interface plus simple et claire."),(5,5,"Les jeux tournent mieux sans se figer, et les dépôts et retraits sont simples et sécurisés.")],
}
REVIEW_LBL = {
 "ru": {"eye":"Отзывы","h2":"Отзывы пользователей о приложении","of5":"из 5"},
 "en": {"eye":"Reviews","h2":"User reviews of the app","of5":"of 5"},
 "fr": {"eye":"Avis","h2":"Avis des utilisateurs sur l'application","of5":"sur 5"},
}
SLIDES = {
 "ios_install": {
  "ru": ["Откройте App Store, нажмите «Установить» и дождитесь завершения установки.","После успешной установки откройте приложение 1xCasino.","Открыв приложение, разрешите Push-уведомления — так вы получите больше бонусов, новости об акциях и оповещения по счёту.","Если язык приложения вам неудобен, перейдите в раздел «Menu».","Откройте настройки в правом верхнем углу. Там же можно гибко настроить приложение под себя.","Выберите нужный язык из доступных. Поздравляем — установка завершена, можно переходить к следующему шагу!"],
  "en": ["Open the App Store, tap Install, and wait for the installation to finish.","Once the installation is complete, open the 1xCasino app.","Once the app opens, allow Push notifications to get more bonuses, account alerts, and news about new promotions.","If the app's language isn't the one you need, go to the Menu section.","Open Settings in the top-right corner. There you can also fine-tune the app to suit your needs.","Choose your preferred language from the list. Congratulations — setup is complete, you can move to the next step!"],
  "fr": ["Ouvrez l'App Store, appuyez sur « Installer » et attendez la fin de l'installation.","Une fois l'installation terminée, ouvrez l'application 1xCasino.","À l'ouverture de l'app, autorisez les notifications Push pour plus de bonus, des alertes de compte et les promos.","Si la langue de l'application ne vous convient pas, allez dans la section « Menu ».","Ouvrez les paramètres en haut à droite. Vous pouvez aussi y adapter l'application à vos besoins.","Choisissez votre langue parmi celles proposées. Félicitations, l'installation est terminée, passez à l'étape suivante !"],
 },
 "install": {
  "ru": ["Загрузите APK, нажав одну из доступных кнопок на странице Guideline.","Разрешите загрузку файла 1xCasinoAfrica.apk с одного из сайтов-зеркал 1xCasino. Загрузка с этого сайта полностью безопасна.","Откройте раздел «Загрузки» на телефоне и нажмите на скачанный файл 1xCasinoAfrica.apk, чтобы начать установку.","Если установка из «Неизвестных источников» запрещена, откройте настройки и разрешите установку для вашего браузера.","В примере показан Chrome, но разрешите установку для того браузера, в котором вы скачали 1xCasinoAfrica.apk.","Телефон предложит установить приложение 1xCasino. Нажмите «Установить» и дождитесь завершения установки.","После успешной установки откройте приложение 1xCasino.","Открыв приложение, разрешите Push-уведомления — так вы получите больше бонусов, новости об акциях и оповещения по счёту.","Если язык приложения вам неудобен, перейдите в раздел «Menu».","Откройте настройки в правом верхнем углу. Там же можно гибко настроить приложение под себя.","Выберите нужный язык из доступных. Поздравляем — установка завершена, можно переходить к следующему шагу!"],
  "en": ["Download the APK using one of the available buttons on the Guideline page.","Allow the download of 1xCasinoAfrica.apk from a 1xCasino mirror site. Downloading from this site is completely safe.","Open the Downloads section on your phone and tap the downloaded 1xCasinoAfrica.apk file to start the installation.","If installation from Unknown sources is blocked, open Settings and allow installation for your browser.","This example shows Chrome, but allow installation for the browser you used to download 1xCasinoAfrica.apk.","Your phone will offer to install the 1xCasino app. Tap Install and wait for the installation to finish.","Once the installation is complete, open the 1xCasino app.","Once the app opens, allow Push notifications to get more bonuses, account alerts, and news about new promotions.","If the app's language isn't the one you need, go to the Menu section.","Open Settings in the top-right corner. There you can also fine-tune the app to suit your needs.","Choose your preferred language from the list. Congratulations — setup is complete, you can move to the next step!"],
  "fr": ["Téléchargez l'APK via l'un des boutons disponibles sur la page Guideline.","Autorisez le téléchargement de 1xCasinoAfrica.apk depuis un site miroir 1xCasino. Ce téléchargement est totalement sûr.","Ouvrez les « Téléchargements » de votre téléphone et appuyez sur le fichier 1xCasinoAfrica.apk pour lancer l'installation.","Si l'installation depuis « Sources inconnues » est bloquée, ouvrez les paramètres et autorisez-la pour votre navigateur.","Cet exemple montre Chrome ; autorisez l'installation pour le navigateur utilisé pour télécharger 1xCasinoAfrica.apk.","Votre téléphone proposera d'installer l'application 1xCasino. Appuyez sur « Installer » et attendez la fin.","Une fois l'installation terminée, ouvrez l'application 1xCasino.","À l'ouverture de l'app, autorisez les notifications Push pour plus de bonus, des alertes de compte et les promos.","Si la langue de l'application ne vous convient pas, allez dans la section « Menu ».","Ouvrez les paramètres en haut à droite. Vous pouvez aussi y adapter l'application à vos besoins.","Choisissez votre langue parmi celles proposées. Félicitations, l'installation est terminée, passez à l'étape suivante !"],
 },
 "login": {
  "ru": ["Нажмите LogIn в приложении и войдите, используя данные, которые указывали при регистрации.","Используйте форму входа по Email, ID, Username или по номеру телефона.","Если вы забыли данные для входа, воспользуйтесь функцией восстановления пароля."],
  "en": ["Tap LogIn in the app and sign in using the details you entered during registration.","Use the login form with your Email, ID, Username, or phone number.","If you've forgotten your login details, use the password recovery feature."],
  "fr": ["Appuyez sur LogIn dans l'application et connectez-vous avec les données saisies lors de l'inscription.","Utilisez le formulaire de connexion par Email, ID, Username ou numéro de téléphone.","Si vous avez oublié vos identifiants, utilisez la fonction de récupération du mot de passe."],
 },
 "profile": {
  "ru": ["Откройте профиль пользователя. Мы не передаём данные третьим лицам — они нужны для защиты вашего аккаунта и выигрышей.","Проверьте заполнение полей Username, Email, Phone, Name, Surname, Country, City.","Перейдите в раздел расширенных персональных данных.","Проверьте заполнение полей Patronymic, Date of Birth, Place of Birth.","Перейдите в раздел настроек.","Заполните Security settings, чтобы повысить безопасность вашего аккаунта.","Скопируйте ID вашего профиля — он понадобится для получения бонуса."],
  "en": ["Open your user profile. We don't share your data with third parties — it's needed to protect your account and winnings.","Check that Username, Email, Phone, Name, Surname, Country, and City are filled in.","Go to the extended personal data section.","Check that Patronymic, Date of Birth, and Place of Birth are filled in.","Go to the Settings section.","Complete the Security settings to improve your account's security.","Copy your profile ID — you'll need it to claim your bonus."],
  "fr": ["Ouvrez votre profil. Nous ne partageons pas vos données — elles servent à protéger votre compte et vos gains.","Vérifiez les champs Username, Email, Phone, Name, Surname, Country, City.","Accédez à la section des données personnelles avancées.","Vérifiez les champs Patronymic, Date of Birth, Place of Birth.","Accédez à la section des paramètres.","Renseignez les Security settings pour renforcer la sécurité de votre compte.","Copiez l'ID de votre profil — il vous servira à obtenir le bonus."],
 },
}
INSTALL_TXT = {
 "ru": {"formstep":"Отправь свой USER ID для получения бонуса","valerr":"Пожалуйста, введи корректный USER ID. Пример: 1569699313","scroll":"Листать вниз"},
 "en": {"formstep":"Send your USER ID to claim the bonus","valerr":"Please enter a valid USER ID. Example: 1569699313","scroll":"Scroll down"},
 "fr": {"formstep":"Envoie ton USER ID pour obtenir le bonus","valerr":"Veuillez saisir un USER ID valide. Exemple : 1569699313","scroll":"Faire défiler"},
}

# ============================================================ shared blocks
def slider_block(t, group, plat="", caps_key=None):
    lang = t["lang"]
    folder = "fr" if lang == "fr" else "en"   # RU по умолчанию на EN-скринах
    base = f"{plat}/" if plat else ""
    caps = SLIDES[caps_key or group][lang]
    figs = "\n".join(
        f'        <figure class="shot"><img src="/assets/shots/{base}{folder}/{group}_{i+1}.webp" alt="" loading="lazy" decoding="async"><figcaption class="shot__cap">{cap}</figcaption></figure>'
        for i, cap in enumerate(caps))
    return f'''    <div class="shots{' shots--ios' if plat=='ios' else ''}">
      <h3 class="shots__h">{t['a_slide_h']}</h3>
      <div class="shots__track">
{figs}
      </div>
    </div>'''

def block_reviews(t, cls="section"):
    lang = t["lang"]; lbl = REVIEW_LBL[lang]
    rfmt = lambda rt: f"{rt:g}".replace(".", ",")
    cards = "\n".join(
        f'        <article class="review">\n'
        f'          <div class="review__top"><img class="review__ava" src="/assets/reviews/a{n}.webp" alt="" width="52" height="52" loading="lazy" decoding="async"><div class="stars-rate" style="--r:{rt/5*100:.0f}%" role="img" aria-label="{rfmt(rt)} {lbl["of5"]}"></div></div>\n'
        f'          <p class="review__text">{txt}</p>\n'
        f'        </article>'
        for n, rt, txt in REVIEWS[lang])
    return f'''<section class="{cls}" id="reviews">
  <div class="wrap rich">
    <p class="eyebrow">{lbl['eye']}</p>
    <h2>{lbl['h2']}</h2>
    <div class="reviews">
      <div class="reviews__track">
{cards}
      </div>
    </div>
  </div>
</section>'''

def block_install(t, arrow, cls="section section--alt", checks_key="a_b5_check"):
    tx = INSTALL_TXT[t["lang"]]
    checks = "".join(
        f'        <li><label class="ckl__row{"" if i==0 else " is-locked"}"><input type="checkbox" class="ckl__cb"{"" if i==0 else " disabled"}><span class="ckl__box" aria-hidden="true"></span><span>{txt}</span></label></li>\n'
        for i, txt in enumerate(t[checks_key]))
    return f'''<section class="{cls}" id="install">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b5_eye']}</p>
    <h2>{t['a_b5_h2']}</h2>
    <div class="bar bar--draft" id="dbar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
      <div class="bar__mask" id="dmask"></div>
      <span class="bar__txt" id="dtxt">{t['a_prog']}</span>
    </div>
    <p>{t['a_b5_intro']}</p>
    <div class="install">
      <ul class="ckl" id="dckl">
{checks}      </ul>
      <div class="bform bform--draft is-locked" id="dform">
        <label class="form-chk"><input type="checkbox" class="ckl__cb" id="dformChk" disabled><span class="ckl__box" aria-hidden="true"></span><span>{tx['formstep']}</span></label>
        <p class="bform__t">{t['a_form_title']}</p>
        <div class="bform__row">
          <input type="text" id="duid" class="bform__in" inputmode="numeric" autocomplete="off" placeholder="{t['a_form_ph']}">
          <button type="button" class="btn btn--violet" id="dsend" disabled>{t['a_form_btn']}</button>
        </div>
        <p class="bform__lock" id="dlock">{t['a_form_locked']}</p>
        <p class="bform__msg" id="dmsg" hidden></p>
      </div>
      <a class="scroll-arrow" href="{arrow}" aria-label="{tx['scroll']}"><span class="scroll-arrow__chev"></span></a>
    </div>
  </div>
</section>'''

# ------------------------------------------------------------ pages
def page_app(t):
    bens = "\n".join(
        f'        <div class="gben"><span class="emo">{e}</span><span>{txt}</span></div>'
        for e, txt in t["h_bens"])
    return head(t, t["h_title"], t["h_desc"], "app/") + f"""<body id="top">
{header(t, "app/")}
<main class="gate">
  <div class="wrap">
    <div class="gate__zone">
      <img class="gate__img" src="/assets/casino_app_mainpage.webp" alt="1xCasino app" width="561" height="580" decoding="async">
      <h1>{t['h_h1']}</h1>
      <p>{t['h_lead']}</p>
      <div class="gate__btns">
        <a class="btn btn--lg" href="{'/android/' if t['lang']=='en' else '/'+t['lang']+'/android/'}">{ANDROID_ICON} {t['h_android']}</a>
        <a class="btn btn--lg btn--violet" href="{'/ios/' if t['lang']=='en' else '/'+t['lang']+'/ios/'}">{APPLE_ICON} {t['h_ios']}</a>
      </div>
      <div class="gate__bens">
{bens}
      </div>
    </div>
  </div>
</main>
{footer(t, "app/")}
{js_base()}
</body>
</html>
"""

def _app_page(t, page, plat="android"):
    ios = plat == "ios"
    lp = "ios_" if ios else ""
    title = t["i_title"] if ios else t["a_title"]
    desc = t["i_desc"] if ios else t["a_desc"]
    lead = t["i_lead"] if ios else t["a_lead"]
    cta = t["i_cta_hero"] if ios else t["a_cta_hero"]
    sticky_txt = t["i_cta_hero"] if ios else t["c_sticky_and"]
    checks_key = "i_b5_check" if ios else "a_b5_check"
    bens6 = "\n".join(
        f'        <div class="gben"><span class="emo">{e}</span><span>{txt}</span></div>'
        for e, txt in t["h_bens"])
    MAILLINK = '<a class="ilink" href="mailto:info@1xcasino-guide.com?subject=1xCasino%20Guide">info@1xcasino-guide.com</a>'
    b7_list = "\n".join(f'      <li>{i}</li>' for i in (t["i_b7_list"] if ios else t["a_b7_list"])).replace("info@1xcasino-guide.com", MAILLINK)
    faq = "\n".join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q, a in (t["i_b12"] if ios else t["a_b12"]))
    if ios:
        chips = (f'<span class="chip chip--green">{t["i_chip1"]}</span>\n'
                 f'            <span class="chip chip--sand">{t["i_chip2"]}</span>')
    else:
        chips = (f'<span class="chip chip--green">{t["a_chip1"]}</span>\n'
                 f'            <span class="chip chip--blue">{t["a_chip2"]}</span>\n'
                 f'            <span class="chip chip--sand">{t["a_chip3"]}</span>')
    b3 = "" if ios else f"""<section class="section">
  <div class="wrap">
    <p class="eyebrow">{t['a_b3_eye']}</p>
    <h2>{t['a_b3_h2']}</h2>
    <div class="gate__bens">
{bens6}
    </div>
  </div>
</section>

"""
    if ios:
        b4 = f"""<section class="section section--alt" id="b4">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b4_eye']}</p>
    <h2>{t['a_b4_h2']}</h2>
    <p>{t['i_b4_p1']}</p>
{slider_block(t, "install", "ios", "ios_install")}
  </div>
</section>"""
    else:
        b4 = f"""<section class="section section--alt" id="b4">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b4_eye']}</p>
    <h2>{t['a_b4_h2']}</h2>
    <p>{t['a_b4_p1']}</p>
    <p>{t['a_b4_p3b']}</p>
    <p>{t['a_b4_p4']}</p>
{tbl(t['a_b4_th1'], t['a_b4_th2'], t['a_b4_rows'])}
{slider_block(t, "install")}
  </div>
</section>"""
    login_slider = slider_block(t, "login", "ios") if ios else slider_block(t, "login")
    profile_slider = slider_block(t, "profile", "ios") if ios else slider_block(t, "profile")
    b8_p1 = t["i_b8_p1"] if ios else t["a_b8_p1"]
    b8_p2 = t["i_b8_p2"] if ios else t["a_b8_p2"]
    b8_rows = t["i_b8_rows"] if ios else t["a_b8_rows"]
    b13 = t["i_b13_h2"] if ios else t["a_b13_h2"]
    return head(t, title, desc, page) + f"""<body id="top" class="has-sticky">
{header(t, page)}
<section class="hero">
  <div class="wrap hero__grid">
    <div class="hero__text">
      <p class="eyebrow">{t['a_eyebrow']} <span data-geo="country">{t['a_geo_country']}</span></p>
      <h1>{t['a_h1']}</h1>
      <p class="hero__lead">{lead}</p>
      <div class="appcard">
        <img class="appcard__icon" src="/assets/app_icon.webp" alt="" width="58" height="58" decoding="async">
        <div>
          <strong class="appcard__name">{t['a_appname']}</strong>
          <div class="appcard__rating"><span class="stars" aria-hidden="true">★★★★★</span><span>·</span><span>{t['a_downloads']}</span></div>
          <div class="appcard__chips">
            {chips}
          </div>
        </div>
      </div>
      <div class="hero__cta"><a class="btn btn--lg" href="/go?b={lp}hero" rel="nofollow noopener">{cta}</a></div>
    </div>
    <div class="hero__media">
      <img class="hero__img" src="/assets/casino_app_mainpage.webp" alt="1xCasino app" width="561" height="580" decoding="async">
    </div>
  </div>
</section>

{b3}{block_reviews(t, "section section--alt")}

{block_install(t, "#b4", "section", checks_key)}

{b4}

<section class="section">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b7_eye']}</p>
    <h2>{t['a_b7_h2']}</h2>
    <ul class="bullets">
{b7_list}
    </ul>
{login_slider}
  </div>
</section>

<section class="section section--alt">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b8_eye']}</p>
    <h2>{t['a_b8_h2']}</h2>
    <p>{b8_p1}</p>
    <p>{b8_p2}</p>
{tbl(t['a_b8_th1'], t['a_b8_th2'], b8_rows)}
{profile_slider}
  </div>
</section>

<section class="section">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b6_eye']}</p>
    <h2>{t['a_b6_h2']}</h2>
    <p>{t['a_b6_p']}</p>
  </div>
</section>

<section class="section faq">
  <div class="wrap">
    <p class="eyebrow">{t['a_b12_eye']}</p>
    <h2>{t['a_b12_h2']}</h2>
{faq}
  </div>
</section>

<section class="final-cta">
  <div class="wrap">
    <h2>{b13}</h2>
    <a class="btn btn--lg" href="/go?b={lp}final" rel="nofollow noopener">{cta}</a>
  </div>
</section>

{footer(t, page)}

<div class="sticky-cta">
  <a class="btn btn--block btn--lg" href="/go?b={lp}sticky" rel="nofollow noopener">{sticky_txt}</a>
</div>

{js_android(t)}
</body>
</html>
"""


def page_android(t):
    return _app_page(t, "android/", "android")

OFFER = {
 "en": {
   "title": 'Don\'t miss your chance to grab <span class="hl">95 FS</span> in <span class="hl">Aviatrix2</span>!',
   "sub": "Your personal offer is limited!",
   "btn": "Claim my bonus",
 },
 "fr": {
   "title": 'Ne manque pas ta chance de récupérer <span class="hl">95 FS</span> sur <span class="hl">Aviatrix2</span> !',
   "sub": "Ton offre personnelle est limitée !",
   "btn": "Récupérer le bonus",
 },
 "ru": {
   "title": 'Не упусти свой шанс забрать <span class="hl">95 FS</span> в <span class="hl">Aviatrix2</span>!',
   "sub": "Твоё персональное предложение ограничено!",
   "btn": "Хочу забрать бонус",
 },
}

_OFFER_JS = """(function(){
  var box = document.getElementById('offerTimer');
  if(!box) return;
  var KEY = 'bonus_deadline_24h', DUR = 24*60*60*1000; // 24 hours from first launch
  function getCookie(n){ var m = document.cookie.match('(?:^|; )'+n+'=([^;]*)'); return m ? decodeURIComponent(m[1]) : null; }
  function setCookie(n,v,age){ document.cookie = n+'='+encodeURIComponent(v)+'; path=/; max-age='+age+'; SameSite=Lax'; }
  var dl = parseInt(getCookie(KEY), 10);
  if(!dl || isNaN(dl)){ dl = Date.now() + DUR; setCookie(KEY, dl, 60*60*24*30); } // deadline stored 30 days; reset only by clearing cookies
  var hEl = document.getElementById('tHours'), mEl = document.getElementById('tMins'), sEl = document.getElementById('tSecs');
  function pad(n){ return (n<10?'0':'')+n; }
  var iv;
  function tick(){
    var left = dl - Date.now(); if(left < 0) left = 0;
    var ts = Math.floor(left/1000);
    hEl.textContent = pad(Math.floor(ts/3600));
    mEl.textContent = pad(Math.floor((ts % 3600)/60));
    sEl.textContent = pad(ts % 60);
    if(left <= 0){ clearInterval(iv); box.classList.add('is-done'); }
  }
  tick(); iv = setInterval(tick, 1000);
})();
(function(){
  var cta = document.getElementById('offerCta'); if(!cta) return;
  var ua = navigator.userAgent || navigator.vendor || '';
  var isIOS = /iPad|iPhone|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  cta.setAttribute('href', isIOS ? ABASE+'ios/' : ABASE+'android/');
})();
(function(){
  var sub = document.getElementById('offerSub');
  if(!sub) return;
  var full = sub.textContent;
  if(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  function run(){
    sub.innerHTML = '<span class="sub-typed"></span><span class="sub-rest"></span>';
    var typedEl = sub.firstChild, restEl = sub.lastChild;
    restEl.textContent = full;
    sub.classList.add('is-typing');
    var i = 0;
    (function type(){
      i++;
      typedEl.textContent = full.slice(0, i);
      restEl.textContent = full.slice(i);
      if(i < full.length){ setTimeout(type, 42); }
      else {
        sub.classList.remove('is-typing');
        sub.classList.add('is-blink');
        sub.addEventListener('animationend', function(){ sub.classList.remove('is-blink'); }, {once:true});
      }
    })();
  }
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); run(); } });
    }, {threshold:0.6});
    io.observe(sub);
  } else { run(); }
})();"""

def offer_block(t):
    lang = t["lang"]
    o = OFFER[lang]
    base = {"en": "/", "fr": "/fr/", "ru": "/ru/"}[lang]
    return f'''<section class="section offer" id="offer">
  <div class="wrap">
    <div class="offer__card">
      <img class="offer__img" src="/assets/bonus.webp" alt="" width="360" height="212" loading="lazy" decoding="async">
      <div class="offer__body">
        <h2 class="offer__title">{o['title']}</h2>
        <p class="offer__sub" id="offerSub">{o['sub']}</p>
        <div class="offer__timer" id="offerTimer" aria-live="off" role="timer">
          <div class="tunit"><span class="tunit__val" id="tHours">24</span></div>
          <span class="tsep" aria-hidden="true">:</span>
          <div class="tunit"><span class="tunit__val" id="tMins">00</span></div>
          <span class="tsep" aria-hidden="true">:</span>
          <div class="tunit"><span class="tunit__val" id="tSecs">00</span></div>
        </div>
        <a class="btn btn--lg offer__cta" id="offerCta" href="{base}android/" rel="nofollow noopener">{o['btn']}</a>
      </div>
    </div>
  </div>
</section>
<script>
var ABASE = "{base}";
{_OFFER_JS}
</script>'''


def page_draft(t):
    cards_svg = ['<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>',
                 '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v6l4 2"/><circle cx="12" cy="12" r="9"/></svg>',
                 '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>']
    cards = "\n".join(
        f'      <div class="card rv">\n        <div class="card__ic">{svg}</div>\n        <h3>{h}</h3>\n        <p>{p}</p>\n      </div>'
        for svg, (h, p) in zip(cards_svg, t["a_b11"]))
    faq = "\n".join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q, a in t["a_b12"])
    head_html = head(t, "Draft \u2014 1xCasino sandbox", t["a_desc"], "draft/").replace('content="index, follow"', 'content="noindex, nofollow"')
    return head_html + f"""<body id="top">
{header(t, "draft/")}
{offer_block(t)}
<section class="section">
  <div class="wrap rich">
    <p class="eyebrow">DRAFT</p>
    <h2>\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a / \u043f\u0435\u0441\u043e\u0447\u043d\u0438\u0446\u0430</h2>
    <p style="color:var(--muted)">\u0421\u044e\u0434\u0430 \u043f\u0435\u0440\u0435\u043d\u0435\u0441\u0435\u043d\u044b \u0442\u0435\u0441\u0442\u043e\u0432\u044b\u0435 \u0431\u043b\u043e\u043a\u0438. \u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430 \u043e\u0442 \u0438\u043d\u0434\u0435\u043a\u0441\u0430\u0446\u0438\u0438 (noindex).</p>
  </div>
</section>

{block_install(t, "#reviews", "section section--alt")}

{block_reviews(t, "section")}

<section class="section section--alt">
  <div class="wrap">
    <p class="eyebrow">{t['a_b11_eye']}</p>
    <h2>{t['a_b11_h2']}</h2>
    <div class="cards">
{cards}
    </div>
    <div class="pay"><span>Orange</span><span>Airtel</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <p class="eyebrow">{t['a_b9_eye']}</p>
    <h2>{t['a_b9_h2']}</h2>
    <div class="promo rv">
      <p style="color:var(--muted)">{t['a_b9_p']}</p>
      <div class="promo__code">
        <span class="promo__value" id="promoValue">{PROMO}</span>
        <button class="btn btn--violet" id="copyPromo" data-code="{PROMO}" type="button"><span class="copy-label">{t['a_copy']}</span></button>
      </div>
      <a class="btn btn--lg" href="/go?b=bonus" rel="nofollow noopener">{t['a_cta_bonus']}</a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wheel-block">
    <p class="eyebrow">{t['a_w_eye']}</p>
    <h2>{t['a_w_h2']}</h2>
    <p style="color:var(--muted);max-width:520px;margin:0 auto">{t['a_w_p']}</p>
    <div class="wheel-wrap">
      <div class="wheel-ring" aria-hidden="true"></div>
      <div class="wheel" id="wheel">
        <div class="seg" style="transform:rotate(22.5deg)"><b>95 FS</b></div>
        <div class="seg" style="transform:rotate(67.5deg)"><b>20 FS</b></div>
        <div class="seg" style="transform:rotate(112.5deg)"><b>50 FS</b></div>
        <div class="seg" style="transform:rotate(157.5deg)"><b>30 FS</b></div>
        <div class="seg" style="transform:rotate(202.5deg)"><b>80 FS</b></div>
        <div class="seg" style="transform:rotate(247.5deg)"><b>40 FS</b></div>
        <div class="seg" style="transform:rotate(292.5deg)"><b>70 FS</b></div>
        <div class="seg" style="transform:rotate(337.5deg)"><b>60 FS</b></div>
      </div>
      <div class="wheel-hub">FS</div>
    </div>
    <p class="wheel-result" id="wheelResult" hidden></p>
    <p style="margin-top:18px"><button class="btn btn--violet btn--lg" id="spinBtn" type="button"><span class="spin-label">{t['a_w_spin']}</span></button></p>
    <p style="margin-top:14px"><a class="btn btn--lg" href="/go?b=wheel" rel="nofollow noopener">{t['a_cta_bonus']}</a></p>
  </div>
</section>

<section class="section faq">
  <div class="wrap">
    <p class="eyebrow">{t['a_b12_eye']}</p>
    <h2>{t['a_b12_h2']}</h2>
{faq}
  </div>
</section>

<section class="section">
  <div class="wrap rich">
    <p class="eyebrow">{t['a_b10_eye']}</p>
    <h2>{t['a_b10_h2']}</h2>
    <p>{t['a_b10_p1']}</p>
    <p>{t['a_b10_p2']}</p>
    <ul class="bullets">
      <li>{t['a_b10_b1']}</li>
      <li>{t['a_b10_b2']}</li>
    </ul>
{tbl(t['a_b10_th1'], t['a_b10_th2'], t['a_b10_rows'])}
    {img_ph(t)}
  </div>
</section>

{footer(t, "draft/")}
{js_android(t)}
</body>
</html>
"""

def page_ios(t):
    return _app_page(t, "ios/", "ios")

def page_home(t):
    return head(t, t["home_title"], t["home_desc"], "") + f"""<body id="top">
{header(t, "")}
<main class="gate">
  <div class="wrap">
    <div class="gate__zone">
      <img class="gate__img" src="/assets/casino_app_mainpage.webp" alt="1xCasino" width="561" height="580" decoding="async">
      <h1>{t['home_h1']}</h1>
      <p>{t['home_lead']}</p>
      <div class="gate__one">
        <div class="gben"><span class="emo">\U0001F5C2\uFE0F</span><span>{t['home_note']}</span></div>
      </div>
    </div>
  </div>
</main>
{footer(t, "")}
{js_base()}
</body>
</html>
"""


BLOCK_TXT = {
    "ru": {"title": "Доступ к сайту ограничен",
           "body": "Сайт недоступен для пользователей из вашего региона. Убедитесь, что VPN или прокси отключены, и повторите попытку.",
           "btn": "Повторить попытку"},
    "en": {"title": "Site access restricted",
           "body": "This site isn't available to users in your region. Make sure any VPN or proxy is turned off and try again.",
           "btn": "Try again"},
    "fr": {"title": "Accès au site restreint",
           "body": "Ce site n'est pas disponible pour les utilisateurs de votre région. Assurez-vous que tout VPN ou proxy est désactivé, puis réessayez.",
           "btn": "Réessayer"},
}

def page_block(t):
    b = BLOCK_TXT[t["lang"]]
    home = "/" if t["lang"] == "en" else f"/{t['lang']}/"
    head_html = head(t, b["title"], b["body"], "block/").replace('content="index, follow"', 'content="noindex, nofollow"')
    return head_html + f"""<body class="blockpage">
  <main class="blockpage__wrap">
    <img class="blockpage__img" src="/assets/restrict.webp" alt="" width="688" height="469" decoding="async">
    <img class="blockpage__logo" src="{LOGO}" alt="1xCasino" decoding="async">
    <h1 class="blockpage__h1">{b['title']}</h1>
    <p class="blockpage__p">{b['body']}</p>
    <a class="btn btn--lg" href="{home}">{b['btn']}</a>
  </main>
</body>
</html>
"""

ERR_TXT = {
    "ru": {"title": "УПС, ОШИБКА!", "sub": "ТАКОЙ СТРАНИЦЫ НЕ СУЩЕСТВУЕТ", "btn": "НА ГЛАВНУЮ"},
    "en": {"title": "UH OH, ERROR!", "sub": "THIS PAGE DOESN'T EXIST", "btn": "BACK TO HOME"},
    "fr": {"title": "OUPS, ERREUR\u00a0!", "sub": "CETTE PAGE N'EXISTE PAS", "btn": "RETOUR À L'ACCUEIL"},
}

REELS_404 = """          <div class="reel reel--1"><div class="reel__strip" style="--rest:-4736px;--start:-1496px"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></div></div>
          <div class="reel reel--2"><div class="reel__strip" style="--rest:-4304px;--start:-1064px"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></div></div>
          <div class="reel reel--3"><div class="reel__strip" style="--rest:-4736px;--start:-1496px"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></div></div>"""

def page_404(t):
    e = ERR_TXT[t["lang"]]
    home = "/" if t["lang"] == "en" else f"/{t['lang']}/"
    head_html = head(t, "404 — " + e["title"], e["sub"], "404/").replace('content="index, follow"', 'content="noindex, nofollow"')
    return head_html + f"""<body class="err404">
{header(t, "404/")}
  <main class="err404__main">
    <div class="slot-wrap">
    <div class="slot">
      <div class="slot__banner">{e['title']}</div>
      <div class="slot__body">
        <div class="slot__reels">
{REELS_404}
        </div>
      </div>
      <div class="slot__led"><span>{e['sub']}</span></div>
      <div class="slot__lever"><span class="slot__ball"></span></div>
    </div>
    <a class="btn btn--lg err404__btn" href="{home}">{e['btn']}</a>
    </div>
  </main>
{footer(t, "404/")}
</body>
</html>
"""

# ===== /app-benefits — преимущества приложения (RU) =====
ABN_CSS = """
.abn{--card:#22075E;--card2:#1A0450;--line:#3A2170;--ink:#F3EEFF;--mut:#BCAEE6;--gold:#7EAC2F;--good:#7EAC2F;--bad:#FF5A6A;--r:16px;max-width:760px;margin-inline:auto;color:var(--ink);line-height:1.45}
.abn h1{font-size:clamp(23px,6.2vw,34px);line-height:1.12;margin:2px 0 10px;font-weight:900;letter-spacing:-.01em;text-align:center}
.abn .sub{color:var(--mut);font-size:clamp(14px,3.9vw,16px);max-width:46ch;margin:0 auto;text-align:center}
.abn .switch{margin:22px 0 8px;background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:var(--r);padding:14px}
.abn .switch-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.abn .switch-top .lbl{font-size:12.5px;font-weight:800;letter-spacing:.01em;color:var(--mut)}
.abn .switch-top .val{font-size:13px;font-weight:800}
.abn[data-net="good"] .switch-top .val{color:var(--good)}
.abn[data-net="weak"] .switch-top .val{color:var(--bad)}
.abn .seg{position:relative;display:grid;grid-template-columns:1fr 1fr;background:#14043C;border:1px solid var(--line);border-radius:12px;padding:5px;user-select:none}
.abn .seg .thumb{position:absolute;top:5px;bottom:5px;left:5px;width:calc(50% - 5px);border-radius:9px;transition:transform .32s cubic-bezier(.6,.05,.15,1),background .32s;background:linear-gradient(180deg,#8DBE38,#5f8622)}
.abn[data-net="weak"] .seg .thumb{transform:translateX(100%);background:linear-gradient(180deg,#d13a49,#a2242f)}
.abn .seg button{position:relative;z-index:1;appearance:none;background:none;border:0;cursor:pointer;color:var(--mut);font:inherit;font-weight:800;font-size:14px;padding:11px 8px;border-radius:9px;display:flex;align-items:center;justify-content:center;gap:8px;transition:color .2s}
.abn[data-net="good"] .seg button[data-v="good"]{color:#fff}
.abn[data-net="weak"] .seg button[data-v="weak"]{color:#fff}
.abn .seg .dot{width:9px;height:9px;border-radius:50%;background:currentColor;box-shadow:0 0 0 4px rgba(255,255,255,.08)}
.abn .hint{margin:10px 2px 0;font-size:12.5px;color:var(--mut)}
.abn .hint b{color:var(--ink)}
.abn .grid{display:grid;grid-template-columns:1fr;gap:12px;margin-top:14px}
@media (min-width:600px){.abn .grid{grid-template-columns:1fr 1fr}}
.abn .card{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:var(--r);padding:14px;position:relative;overflow:hidden}
.abn .card h3{margin:0 0 2px;font-size:15px;font-weight:800;display:flex;align-items:center;gap:8px}
.abn .card .ic{font-size:18px;filter:saturate(1.2)}
.abn .card .cap{margin:0 0 12px;font-size:12.5px;color:var(--mut)}
.abn .full{grid-column:1 / -1}
.abn .load-bars{display:grid;gap:10px}
.abn .track{position:relative;height:36px;border-radius:10px;background:#14043C;border:1px solid var(--line);overflow:hidden}
.abn .fill{position:absolute;inset:0 auto 0 0;width:0;border-radius:9px}
.abn .fill.b{background:linear-gradient(90deg,#ff4d5e,#ff8a5a)}
.abn .fill.a{background:linear-gradient(90deg,#8DBE38,#37d6b6)}
.abn .track-label{position:absolute;left:13px;top:50%;transform:translateY(-50%);z-index:2;font-size:13px;font-weight:800;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.55);white-space:nowrap}
.abn .track-time{position:absolute;right:12px;top:50%;transform:translateY(-50%);z-index:2;font-size:12.5px;font-weight:800;color:#fff;font-variant-numeric:tabular-nums;text-shadow:0 1px 3px rgba(0,0,0,.55)}
.abn .load-actions{display:flex;justify-content:center;margin-top:14px}
.abn .replay{appearance:none;cursor:pointer;font:inherit;font-weight:800;font-size:13px;color:var(--gold);background:none;border:1px solid #4a5f24;border-radius:10px;padding:10px 18px;display:inline-flex;align-items:center;gap:7px}
.abn .replay:active{transform:translateY(1px)}
.abn .reels{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.abn .reel-box{border:1px solid var(--line);border-radius:12px;background:#14043C;padding:9px;text-align:center}
.abn .reel-box .who{font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;margin-bottom:6px}
.abn .reel-box.b .who{color:var(--bad)}
.abn .reel-box.a .who{color:var(--good)}
.abn .window{height:56px;overflow:hidden;border-radius:9px;border:1px solid var(--line);background:#0C0230;position:relative}
.abn .strip{font-size:30px}
.abn .strip span{display:block;height:56px;line-height:56px;text-align:center}
@keyframes abnSpin{to{transform:translateY(-336px)}}
.abn .reel-box.a .strip{animation:abnSpin 1.1s linear infinite}
.abn .reel-box.b .strip{animation:abnSpin 1.5s steps(4,end) infinite}
.abn[data-net="weak"] .reel-box.b .strip{animation-duration:2.2s;animation-timing-function:steps(3,end)}
.abn .fps{margin-top:6px;font-size:11px;color:var(--mut)}
.abn .fps b{font-variant-numeric:tabular-nums;font-size:14px}
.abn .reel-box.b .fps b{color:var(--bad)}
.abn .reel-box.a .fps b{color:var(--good)}
.abn .bars{display:grid;gap:10px;margin-bottom:12px}
.abn .bar-row{display:grid;grid-template-columns:70px 1fr auto;align-items:center;gap:10px;font-size:12px}
.abn .bar-row .who{font-weight:800}
.abn .bar-row.b .who{color:var(--bad)}
.abn .bar-row.a .who{color:var(--good)}
.abn .meter{height:12px;border-radius:7px;background:#14043C;border:1px solid var(--line);overflow:hidden}
.abn .meter i{display:block;height:100%;border-radius:6px;transition:width .6s cubic-bezier(.2,.7,.2,1)}
.abn .bar-row.b .meter i{background:linear-gradient(90deg,#ff4d5e,#ff8a5a)}
.abn .bar-row.a .meter i{background:linear-gradient(90deg,#8DBE38,#37d6b6)}
.abn .bar-row .num{font-weight:800;font-variant-numeric:tabular-nums;min-width:52px;text-align:right}
.abn .saved{display:flex;align-items:center;justify-content:space-between;gap:10px;background:#14043C;border:1px dashed #4A3480;border-radius:11px;padding:10px 12px}
.abn .saved .big{font-size:20px;font-weight:900;color:var(--good);font-variant-numeric:tabular-nums}
.abn .stepper{display:flex;align-items:center;gap:8px}
.abn .stepper button{width:30px;height:30px;border-radius:8px;border:1px solid var(--line);background:#2E1B55;color:var(--ink);font-size:18px;font-weight:800;cursor:pointer;line-height:1}
.abn .stepper b{min-width:16px;text-align:center;font-variant-numeric:tabular-nums}
.abn .acc{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media (max-width:360px){.abn .acc{grid-template-columns:1fr}}
.abn .panel{border:1px solid var(--line);border-radius:12px;padding:14px;background:#14043C;min-height:96px;display:flex;flex-direction:column;gap:8px;justify-content:center}
.abn .panel .who{font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.05em}
.abn .panel.b .who{color:var(--bad)}
.abn .panel.a .who{color:var(--good)}
.abn .state{display:flex;align-items:center;gap:9px;font-weight:800;font-size:14px}
.abn .state .led{width:11px;height:11px;border-radius:50%;flex:none}
.abn .led.g{background:var(--good);box-shadow:0 0 10px #7EAC2F88}
.abn .led.r{background:var(--bad);box-shadow:0 0 10px #ff5a6a88}
.abn .state small{display:block;font-weight:600;color:var(--mut);font-size:11.5px;margin-top:2px}
@keyframes abnFlick{0%,100%{opacity:1}45%{opacity:.35}55%{opacity:.9}}
.abn .panel.b .drop{display:none}
.abn[data-net="weak"] .panel.b .ok{display:none}
.abn[data-net="weak"] .panel.b .drop{display:flex;animation:abnFlick 1.4s infinite}
.abn .abn-cta-wrap{text-align:center;margin-top:24px}
@media (prefers-reduced-motion: reduce){.abn .strip{animation:none !important}.abn .fill{transition:none}}
"""

BEN = {
 "en": {
   "title": "1xCasino app benefits — faster, more stable, less data",
   "desc": "A visual comparison: the 1xCasino app vs the browser — loading, game stability, data savings and stable account access.",
   "h1": "1xCasino app benefits!",
   "sub": "Below you can clearly compare the advantages of using the app.",
   "lbl": "⏱️ Network comparison",
   "netGood": "Good · Wi-Fi", "netWeak": "Weak · 2G/3G",
   "segGood": "Good", "segWeak": "Weak · 2G/3G",
   "hintGood": 'The connection is good right now — the difference is still small. <b>Switch to “Weak” ↑</b>',
   "hintWeak": 'The connection dropped — <b>the browser starts to fall apart, the app holds up.</b>',
   "browser": "Browser", "app": "App",
   "loadH": "Loading",
   "loadCap": "The app opens faster — the interface is already inside, it doesn’t load every time.",
   "btnLoad": "↻ Run the loading",
   "stabH": "Stability in games",
   "stabCap": "In the app, slots spin smoothly. On a weak network the browser starts to lag.",
   "trafH": "Data savings",
   "trafCap": "Images and layout are already in the app — a session uses far fewer MB.",
   "appShort": "App", "browserShort": "Browser",
   "mbBrowser": "18 MB", "mbApp": "4 MB",
   "savedLabel": "Saved per month", "sessLabel": "sessions<br>per day",
   "accH": "Stable account access",
   "accCap": "The app keeps your session even when the connection jumps. In the browser on a weak network you get kicked out.",
   "stOk": "Online", "stOkSmall": "while the connection is stable",
   "stDrop": "Session expired", "stDropSmall": "Log in again · enter password",
   "stAppSmall": "PIN login · session saved",
   "cta": "📲 Download the app",
   "sec": "s", "mb": "MB", "gb": "GB",
 },
 "fr": {
   "title": "Avantages de l'application 1xCasino — plus rapide, plus stable, moins de données",
   "desc": "Comparaison visuelle : l'application 1xCasino face au navigateur — chargement, stabilité des jeux, économie de données et accès stable au compte.",
   "h1": "Les avantages de l'application 1xCasino !",
   "sub": "Ci-dessous, tu peux comparer clairement les avantages de l'application.",
   "lbl": "⏱️ Comparaison réseau",
   "netGood": "Bonne · Wi-Fi", "netWeak": "Faible · 2G/3G",
   "segGood": "Bonne", "segWeak": "Faible · 2G/3G",
   "hintGood": 'La connexion est bonne pour l\'instant — la différence est encore faible. <b>Passe sur « Faible » ↑</b>',
   "hintWeak": 'La connexion a chuté — <b>le navigateur commence à lâcher, l\'app tient bon.</b>',
   "browser": "Navigateur", "app": "Application",
   "loadH": "Chargement",
   "loadCap": "L'application s'ouvre plus vite — l'interface est déjà intégrée, elle ne se recharge pas à chaque fois.",
   "btnLoad": "↻ Lancer le chargement",
   "stabH": "Stabilité des jeux",
   "stabCap": "Dans l'app, les machines tournent sans à-coups. Sur réseau faible, le navigateur commence à ramer.",
   "trafH": "Économie de données",
   "trafCap": "Images et mise en page sont déjà dans l'app — une session consomme bien moins de Mo.",
   "appShort": "App", "browserShort": "Navig.",
   "mbBrowser": "18 Mo", "mbApp": "4 Mo",
   "savedLabel": "Économie par mois", "sessLabel": "sessions<br>par jour",
   "accH": "Accès stable au compte",
   "accCap": "L'app conserve ta session même quand la connexion saute. Dans le navigateur sur réseau faible, tu es déconnecté.",
   "stOk": "En ligne", "stOkSmall": "tant que la connexion est stable",
   "stDrop": "Session expirée", "stDropSmall": "Reconnecte-toi · saisis le mot de passe",
   "stAppSmall": "connexion par PIN · session conservée",
   "cta": "📲 Télécharger l'app",
   "sec": "s", "mb": "Mo", "gb": "Go",
 },
 "ru": {
   "title": "Преимущества приложения 1xCasino — быстрее, стабильнее, меньше трафика",
   "desc": "Наглядное сравнение: приложение 1xCasino против браузера — загрузка, стабильность игр, экономия трафика и стабильный доступ к аккаунту.",
   "h1": "Преимущества 1xCasino приложения!",
   "sub": "Ниже можно наглядно сравнить плюсы работы приложения.",
   "lbl": "⏱️ Сравнение сети",
   "netGood": "Хорошая · Wi-Fi", "netWeak": "Слабая · 2G/3G",
   "segGood": "Хорошая", "segWeak": "Слабая · 2G/3G",
   "hintGood": 'Сейчас связь хорошая — разница ещё небольшая. <b>Переключи на «Слабую» ↑</b>',
   "hintWeak": 'Связь просела — <b>браузер начинает сыпаться, приложение держится.</b>',
   "browser": "Браузер", "app": "Приложение",
   "loadH": "Загрузка",
   "loadCap": "Приложение открывается быстрее — интерфейс уже внутри, не грузится каждый раз.",
   "btnLoad": "↻ Запустить загрузку",
   "stabH": "Стабильность в играх",
   "stabCap": "В приложении слоты крутятся плавно. На слабой сети браузер начинает лагать.",
   "trafH": "Экономия трафика",
   "trafCap": "Картинки и разметка уже в приложении — за сессию уходит в разы меньше МБ.",
   "appShort": "Прилож.", "browserShort": "Браузер",
   "mbBrowser": "18 МБ", "mbApp": "4 МБ",
   "savedLabel": "Экономия в месяц", "sessLabel": "сессий<br>в день",
   "accH": "Стабильный доступ к аккаунту",
   "accCap": "Приложение держит сессию даже когда связь прыгает. В браузере на слабой сети тебя выкидывает.",
   "stOk": "В сети", "stOkSmall": "пока связь стабильна",
   "stDrop": "Сессия истекла", "stDropSmall": "Войдите снова · введите пароль",
   "stAppSmall": "вход по PIN · сессия сохранена",
   "cta": "📲 Скачать приложение",
   "sec": "с", "mb": "МБ", "gb": "ГБ",
 },
}

_ABN_JS_BODY = """(function(){
  var root = document.querySelector('.abn');
  if(!root) return;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var buttons = root.querySelectorAll('.seg button');
  var netVal = document.getElementById('netVal');
  var netHint = document.getElementById('netHint');
  buttons.forEach(function(b){ b.addEventListener('click', function(){ setNet(b.dataset.v); }); });
  function setNet(v){
    root.dataset.net = v;
    buttons.forEach(function(b){ b.setAttribute('aria-selected', b.dataset.v===v); });
    if(v==='weak'){ netVal.textContent = LB.netWeak; netHint.innerHTML = LB.hintWeak; }
    else { netVal.textContent = LB.netGood; netHint.innerHTML = LB.hintGood; }
    runLoad();
  }
  var fB=document.getElementById('fLoadB'), fA=document.getElementById('fLoadA');
  var tB=document.getElementById('tLoadB'), tA=document.getElementById('tLoadA');
  var loadTimer;
  function runLoad(){
    var weak = root.dataset.net==='weak';
    var dB = weak ? 6.4 : 2.6, dA = weak ? 1.4 : 0.8;
    clearInterval(loadTimer);
    fB.style.transition='none'; fA.style.transition='none';
    fB.style.width='0'; fA.style.width='0';
    tB.textContent='0.0'+LB.sec; tA.textContent='0.0'+LB.sec;
    void fB.offsetWidth;
    if(reduced){ fB.style.width='100%'; fA.style.width='100%'; tB.textContent=dB.toFixed(1)+LB.sec; tA.textContent=dA.toFixed(1)+LB.sec; return; }
    fA.style.transition='width '+dA+'s cubic-bezier(.2,.8,.2,1)'; fA.style.width='100%';
    fB.style.transition='width '+(dB*0.4)+'s linear'; fB.style.width='45%';
    setTimeout(function(){ fB.style.transition='width '+(dB*0.6)+'s linear'; fB.style.width='100%'; }, dB*0.4*1000 + 350);
    var start=performance.now(), doneB=false, doneA=false;
    loadTimer=setInterval(function(){
      var el=(performance.now()-start)/1000;
      if(!doneA){ if(el>=dA){tA.textContent=dA.toFixed(1)+LB.sec;doneA=true;} else tA.textContent=el.toFixed(1)+LB.sec; }
      if(!doneB){ if(el>=dB+0.35){tB.textContent=dB.toFixed(1)+LB.sec;doneB=true;} else tB.textContent=el.toFixed(1)+LB.sec; }
      if(doneA&&doneB) clearInterval(loadTimer);
    }, 60);
  }
  document.getElementById('btnLoad').addEventListener('click', runLoad);
  var fpsB=document.getElementById('fpsB'), fpsA=document.getElementById('fpsA');
  if(!reduced){
    setInterval(function(){
      var weak = root.dataset.net==='weak';
      var lo = weak?9:34, hi = weak?16:46;
      fpsB.textContent = (lo + Math.floor(Math.random()*(hi-lo+1)));
      fpsA.textContent = (58 + Math.floor(Math.random()*3));
    }, 220);
  }
  var perSession = 18-4, sess=3;
  var sessEl=document.getElementById('sess'), savedEl=document.getElementById('savedVal');
  function renderSaved(){
    sessEl.textContent=sess;
    var mb = perSession*sess*30;
    savedEl.textContent = mb>=1024 ? (mb/1024).toFixed(1)+' '+LB.gb : mb+' '+LB.mb;
  }
  document.getElementById('plus').addEventListener('click',function(){ if(sess<15){sess++;renderSaved();} });
  document.getElementById('minus').addEventListener('click',function(){ if(sess>1){sess--;renderSaved();} });
  renderSaved();
  runLoad();
  var iOS = /iPad|iPhone|iPod/.test(navigator.userAgent||navigator.vendor||'') || (navigator.platform==='MacIntel' && navigator.maxTouchPoints>1);
  Array.prototype.forEach.call(document.querySelectorAll('.abn-dl'), function(c){ c.setAttribute('href', iOS?BBASE+'ios/':BBASE+'android/'); });
})();"""

def page_benefits(t):
    lang = t["lang"]
    b = BEN[lang]
    base = {"en": "/", "fr": "/fr/", "ru": "/ru/"}[lang]
    lb = json.dumps({k: b[k] for k in ("netGood","netWeak","hintGood","hintWeak","sec","mb","gb")}, ensure_ascii=False)
    sess_aria = b['sessLabel'].replace('<br>', ' ')
    content = f'''      <h1>{b['h1']}</h1>
      <p class="sub">{b['sub']}</p>

      <div class="switch">
        <div class="switch-top">
          <span class="lbl">{b['lbl']}</span>
          <span class="val" id="netVal">{b['netGood']}</span>
        </div>
        <div class="seg" role="tablist" aria-label="{b['lbl']}">
          <span class="thumb" aria-hidden="true"></span>
          <button data-v="good" role="tab" aria-selected="true"><span class="dot"></span>{b['segGood']}</button>
          <button data-v="weak" role="tab" aria-selected="false"><span class="dot"></span>{b['segWeak']}</button>
        </div>
        <p class="hint" id="netHint">{b['hintGood']}</p>
      </div>

      <section class="grid">
        <div class="card" id="cardLoad">
          <h3><span class="ic">🏁</span>{b['loadH']}</h3>
          <p class="cap">{b['loadCap']}</p>
          <div class="load-bars">
            <div class="track"><i class="fill b" id="fLoadB"></i><span class="track-label">{b['browser']}</span><span class="track-time" id="tLoadB">0.0{b['sec']}</span></div>
            <div class="track"><i class="fill a" id="fLoadA"></i><span class="track-label">{b['app']}</span><span class="track-time" id="tLoadA">0.0{b['sec']}</span></div>
          </div>
          <div class="load-actions"><button class="replay" id="btnLoad">{b['btnLoad']}</button></div>
        </div>

        <div class="card">
          <h3><span class="ic">🎰</span>{b['stabH']}</h3>
          <p class="cap">{b['stabCap']}</p>
          <div class="reels">
            <div class="reel-box b">
              <div class="who">{b['browser']}</div>
              <div class="window"><div class="strip"><span>🍒</span><span>🔔</span><span>⭐</span><span>7️⃣</span><span>🍋</span><span>💎</span><span>🍒</span><span>🔔</span><span>⭐</span><span>7️⃣</span><span>🍋</span><span>💎</span></div></div>
              <div class="fps"><b id="fpsB">42</b> FPS</div>
            </div>
            <div class="reel-box a">
              <div class="who">{b['app']}</div>
              <div class="window"><div class="strip"><span>💎</span><span>7️⃣</span><span>⭐</span><span>🔔</span><span>🍒</span><span>🍋</span><span>💎</span><span>7️⃣</span><span>⭐</span><span>🔔</span><span>🍒</span><span>🍋</span></div></div>
              <div class="fps"><b id="fpsA">60</b> FPS</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3><span class="ic">📉</span>{b['trafH']}</h3>
          <p class="cap">{b['trafCap']}</p>
          <div class="bars">
            <div class="bar-row b"><span class="who">{b['browserShort']}</span><div class="meter"><i style="width:100%"></i></div><span class="num">{b['mbBrowser']}</span></div>
            <div class="bar-row a"><span class="who">{b['appShort']}</span><div class="meter"><i style="width:22%"></i></div><span class="num">{b['mbApp']}</span></div>
          </div>
          <div class="saved">
            <div>
              <div style="font-size:11px;color:var(--mut);letter-spacing:.05em;font-weight:800">{b['savedLabel']}</div>
              <div class="big" id="savedVal">1.3 {b['gb']}</div>
            </div>
            <div class="stepper" aria-label="{sess_aria}">
              <button id="minus" aria-label="−">−</button>
              <div style="text-align:center;font-size:11px;color:var(--mut)">{b['sessLabel']}<br><b id="sess">3</b></div>
              <button id="plus" aria-label="+">+</button>
            </div>
          </div>
        </div>
      </section>

      <div class="card full" style="margin-top:12px">
        <h3><span class="ic">🔐</span>{b['accH']}</h3>
        <p class="cap">{b['accCap']}</p>
        <div class="acc">
          <div class="panel b">
            <div class="who">{b['browser']}</div>
            <div class="state ok"><span class="led g"></span><div>{b['stOk']}<small>{b['stOkSmall']}</small></div></div>
            <div class="state drop"><span class="led r"></span><div>{b['stDrop']}<small>{b['stDropSmall']}</small></div></div>
          </div>
          <div class="panel a">
            <div class="who">{b['app']}</div>
            <div class="state"><span class="led g"></span><div>{b['stOk']}<small>{b['stAppSmall']}</small></div></div>
          </div>
        </div>
      </div>

      <div class="abn-cta-wrap"><a class="btn btn--lg abn-dl" href="{base}android/" rel="nofollow noopener">{b['cta']}</a></div>'''
    head_html = head(t, b['title'], b['desc'], "app-benefits/").replace("</head>", "<style>" + ABN_CSS + "</style>\n</head>")
    js = "<script>\nvar LB = " + lb + ";\nvar BBASE = " + json.dumps(base) + ";\n" + _ABN_JS_BODY + "\n</script>"
    return head_html + f'''<body id="top" class="has-sticky">
{header(t, "app-benefits/")}
<section class="section">
  <div class="wrap">
    <div class="abn" data-net="good">
{content}
    </div>
  </div>
</section>
<div class="sticky-cta">
  <a class="btn btn--block btn--lg abn-dl" href="{base}android/" rel="nofollow noopener">{b['cta']}</a>
</div>
{footer(t, "app-benefits/")}
{js}
</body>
</html>'''


def page_limit(t):
    lang = t["lang"]
    title = {"en": "Limited offer — 95 FS in Aviatrix2 | 1xCasino",
             "fr": "Offre limitée — 95 FS sur Aviatrix2 | 1xCasino",
             "ru": "Ограниченное предложение — 95 FS в Aviatrix2 | 1xCasino"}[lang]
    desc = {"en": "A personal limited-time offer: grab 95 FS in Aviatrix2. Download the 1xCasino app.",
            "fr": "Une offre personnelle à durée limitée : récupère 95 FS sur Aviatrix2. Télécharge l'application 1xCasino.",
            "ru": "Персональное ограниченное предложение: забери 95 FS в Aviatrix2. Скачай приложение 1xCasino."}[lang]
    return head(t, title, desc, "limit/") + f'''<body id="top">
{header(t, "limit/")}
{offer_block(t)}
{footer(t, "limit/")}
</body>
</html>'''

OUT = "/home/claude/site"
for lang in ("en", "fr", "ru"):
    t = L[lang]
    base = OUT if lang == "en" else os.path.join(OUT, lang)
    for sub, fn in (("", page_home), ("app", page_app), ("android", page_android), ("ios", page_ios), ("block", page_block), ("404", page_404), ("limit", page_limit), ("app-benefits", page_benefits)):
        d = os.path.join(base, sub)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(fn(t))
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    f.write(MANIFEST)
# /draft \u2014 \u043e\u0434\u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430-\u043f\u0435\u0441\u043e\u0447\u043d\u0438\u0446\u0430 (\u0431\u0435\u0437 \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u043e\u0432), \u043a\u043e\u043d\u0442\u0435\u043d\u0442 \u043d\u0430 RU
dd = os.path.join(OUT, "draft")
os.makedirs(dd, exist_ok=True)
with open(os.path.join(dd, "index.html"), "w", encoding="utf-8") as f:
    f.write(page_draft(L["ru"]))
print("done")
