#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Style-reference builder for future rehabilitation-information PDFs."""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTMLDIR = os.path.join(ROOT, "_html"); os.makedirs(HTMLDIR, exist_ok=True)
FONTS_CSS = "file://" + os.path.join(ROOT, "fonts", "fonts.local.css")
CSS = open(os.path.join(ROOT, "base.css"), encoding="utf-8").read()

IC = {
  "route": '<circle cx="6" cy="19" r="3"/><path d="M9 19h6.5a3.5 3.5 0 0 0 0-7H8.5a3.5 3.5 0 0 1 0-7H18"/><circle cx="18" cy="5" r="3"/>',
  "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8Z"/>',
  "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
  "check": '<path d="m9 11 3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
  "alert": '<path d="m21.7 18-9-16a1 1 0 0 0-1.7 0l-9 16a1 1 0 0 0 .9 1.5h18a1 1 0 0 0 .8-1.5Z"/><path d="M12 9v4M12 17h.01"/>',
  "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
  "calendar": '<path d="M8 2v4M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
}

def svg(name, size, stroke="currentColor"):
    return f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" stroke="{stroke}">{IC[name]}</svg>'

def E(text): return html.escape(text, quote=False)
def p(text, cls="par"): return f'<p class="{cls}">{text}</p>'
def b(text): return f'<strong>{E(text)}</strong>'
def pill(text): return f'<span class="pill">{E(text)}</span>'

def summary(text):
    return (f'<div class="summary"><div class="ico">{svg("zap",20,"hsl(199 89% 40%)")}</div>'
            f'<div class="sbody"><h2>בקצרה</h2><p>{text}</p></div></div>')

def context_note(text):
    return f'<div class="eligbar"><p>{text}</p></div>'

def acc(icon, title, *parts):
    head = f'<div class="acc-h"><span class="si">{svg(icon,20,"var(--primary-d)")}</span><h3>{E(title)}</h3></div>'
    return '<div class="acc">' + head + ''.join(parts) + '</div>'

def cond(n, title, inner):
    return f'<div class="cond"><div class="cond-h"><span class="ncirc">{n}</span><h4>{E(title)}</h4></div>{inner}</div>'

def callout(variant, html_text, icon=None):
    ic = icon or ("alert" if variant == "red" else "info")
    return f'<div class="callout {variant}"><span class="cico">{svg(ic,17)}</span><p>{html_text}</p></div>'

def twoup(items):
    cards = []
    for icon, title, desc in items:
        head = f'<div class="mh">{svg(icon,17)}<h5>{E(title)}</h5></div>' if icon else f'<h5>{E(title)}</h5>'
        cards.append(f'<div class="minicard">{head}<p>{desc}</p></div>')
    return '<div class="twoup">' + ''.join(cards) + '</div>'

def checks(items):
    lis = ''.join(f'<li>{svg("check",16)}<span>{item}</span></li>' for item in items)
    return f'<ul class="checks">{lis}</ul>'

def important(text):
    return (f'<div class="important"><div class="ico">{svg("alert",19,"hsl(38 92% 42%)")}</div>'
            f'<div><h3>חשוב לזכור</h3><p>{text}</p></div></div>')

def build():
    body = []
    body.append(summary("תבנית זו משמשת לשימור השפה העיצובית בלבד. את התוכן הסופי נחליף במידע שיימסר בהמשך."))
    body.append(context_note("כאן תופיע הערת הקשר קצרה למבוטח/ת: מהו השלב בתהליך, מה נדרש לדעת, ומה צפוי לקרות מול עובד/ת השיקום."))
    body.append(acc("users", "כותרת סקשן לדוגמה",
        p("פסקת פתיחה קצרה בסגנון המסמכים: פשוטה, ישירה ומלווה את המבוטח/ת צעד אחר צעד.", "lead"),
        cond("1", "שלב או אפשרות ראשונה", p("כאן יופיע הסבר ממוקד על אפשרות אחת בתהליך.") + callout("blue", "תיבת מידע רכה מתאימה להבהרות שאינן אזהרה.")),
        cond("2", "שלב או אפשרות שנייה", twoup([
            ("calendar", "אפשרות א׳", "הסבר קצר שמוצג בכרטיס משנה."),
            ("info", "אפשרות ב׳", "הסבר קצר שמוצג לצד האפשרות הראשונה."),
        ])),
        callout("amber", b("שים לב: ") + "כאן תופיע הערה חשובה אך לא חמורה.", "alert"),
        checks(["פריט בדיקה ראשון", "פריט בדיקה שני", "פריט בדיקה שלישי"])
    ))
    body.append(important("הטקסט כאן מיועד להדגמת רכיב 'חשוב לזכור'. במסמך אמיתי נחליף אותו במסר המרכזי לסיום."))
    body_html = '\n'.join(body)
    return f"""<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<title>תבנית עיצוב — מדריכי שיקום</title>
<style>@import url("{FONTS_CSS}");
{CSS}</style></head><body>
<div class="page">
  <div class="hero">
    <div class="circle c1"></div><div class="circle c2"></div>
    <div class="hero-row">
      <div class="hero-ico">{svg("route",30,"#fff")}</div>
      <div><h1>תבנית עיצוב למדריך שיקום</h1><p class="sub">בסיס לדסקטופ ולמובייל עבור תכנים חדשים</p></div>
    </div>
  </div>
  <div class="body">
{body_html}
  </div>
  <div class="foot">המידע הוא מסייע בלבד ואינו מחליף הנחיות רשמיות או ייעוץ פרטני. לאימות זכאות, תנאים וסכומים מעודכנים יש לפנות לעובד/ת השיקום המטפל/ת.
  <div class="brand">מדריכי שיקום · מידע למבוטחים</div></div>
</div></body></html>"""

if __name__ == '__main__':
    open(os.path.join(HTMLDIR, 'template-style-reference.html'), 'w', encoding='utf-8').write(build())
    print('built template-style-reference.html')
