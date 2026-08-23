#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arabic fridge sheet + wallet card.

wkhtmltopdf clips right-to-left text (old WebKit bidi), so Arabic is rendered
through LibreOffice instead, which handles Arabic shaping and bidi correctly.
Layout is table-based because LibreOffice's HTML importer ignores flexbox.
"""
import os, html, subprocess, shutil

OUT = "/home/claude/tbv/formats/print"
TMP = "/tmp/ar_build"
os.makedirs(OUT, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

D = dict(
  brand="ثق، ولكن تحقق",
  tagline="لست مضطراً للشك في كل الناس. أضف خطوة واحدة.",
  steps_head="قبل أن تنتقل أي أموال",
  steps=[("ابحث عن الرقم بنفسك.", "ليس الرقم الذي أعطوك إياه. الرقم على بطاقتك أو كشف حسابك."),
         ("اتصل بالشخص بنفسك.", "أغلق الخط أولاً. إن كان الأمر حقيقياً، فسيظلون موجودين."),
         ("انتظر يوماً واحداً.", "المشكلة الحقيقية تحتمل ليلة نوم. الاحتيال لا يحتمل.")],
  signs_head="ثلاث علامات للتوقف",
  signs=["جاءتك أنت — لست أنت من بدأ.",
         "حرّكتك بسرعة — خوف أو قلق أو موعد نهائي.",
         "تريد نقلاً — مالاً أو رمزاً أو حاسوبك."],
  never_head="أبداً، ولا مرة واحدة",
  never=["لا أحد مشروع يُدفع له ببطاقات الهدايا.",
         "بنكك لن يطلب منك أبداً إخراج أموالك من بنكك.",
         "لا تقرأ رمز الرسالة بصوت عالٍ لأي أحد أبداً.",
         "لا أحد يأتي إلى بيتك ليأخذ نقداً أو ذهباً أو أشياء ثمينة."],
  help_head="مساعدة مجانية — بلا أحكام مسبقة",
  helps=[("833-372-8311", "الخط الوطني · الاثنين–الجمعة ١٠–٦ بتوقيت الشرق"),
         ("877-908-3360", "AARP Fraud Watch · الاثنين–الجمعة ٨–٨ بتوقيت الشرق")],
  report="للإبلاغ: ic3.gov · reportfraud.ftc.gov · تتوفر ترجمة فورية",
  footline="إذا وقع الأمر فعلاً: ليس ذنبك، ولم يفت الأوان.",
  foot="حر النسخ والطباعة والمشاركة.",
  notice_head="تنبيه: ترجمة غير مُدقَّقة — لا تطبعها بعد",
  notice_body="تُرجمت بالذكاء الاصطناعي ولم يراجعها متحدث أصلي. هل تتحدث العربية؟ "
              "ساعدنا: translations@trustbutverifyproject.org",
  notice_en="UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. "
            "Do not distribute. Arabic speakers: please help us check it.",
)

F = "DejaVu Sans"
e = html.escape


def row(cells):
    return "<tr>" + "".join(cells) + "</tr>"


def build_sheet():
    steps = ""
    for i, (imp, sub) in enumerate(D["steps"], 1):
        steps += (
          '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
          f'<td width="88%" align="right" style="padding:1pt 0 0 0">'
          f'<span style="font-size:13pt;font-weight:bold">{e(imp)}</span><br/>'
          f'<span style="font-size:9pt">{e(sub)}</span></td>'
          f'<td width="12%" align="left" valign="top" style="padding:3pt 0">'
          f'<span style="font-size:19pt;font-weight:bold">{i}</span></td>'
          '</tr></table>')

    signs = "".join(
        f'<p style="font-size:10pt;margin:0;padding:0 0" align="right">'
        f'{e(x)} &#9632;</p>' for x in D["signs"])

    never = "".join(
        f'<p style="font-size:9.5pt;font-weight:bold;margin:0;padding:0 0" '
        f'align="right">{e(x)} &#10005;</p>' for x in D["never"])

    helps = row([
        f'<td width="50%" align="right" style="padding:2pt 0">'
        f'<span style="font-size:17pt;font-weight:bold">{e(t)}</span><br/>'
        f'<span style="font-size:10pt">{e(w)}</span></td>'
        for t, w in D["helps"]])

    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
 @page {{ margin: 0.28in 0.45in 0.15in 0.45in; }}
 body {{ font-family:"{F}"; color:#000; }}
 p, td, span {{ font-family:"{F}"; }}
 .hr {{ border-top:3pt solid #000; font-size:1pt; line-height:1pt; }}
 .hair {{ border-top:1pt solid #000; font-size:1pt; line-height:1pt; }}
 .zone {{ font-size:10pt; font-weight:bold; }}
</style></head>
<body dir="rtl">
<p align="right" style="font-size:22pt;font-weight:bold;margin:0">{e(D['brand'])}</p>
<p align="right" style="font-size:12pt;margin:0;padding-top:2pt">{e(D['tagline'])}</p>
<table width="100%" cellpadding="4" cellspacing="0" border="2" bordercolor="#000000">
<tr><td align="right" bgcolor="#EEEEEE">
<p align="right" style="font-size:10pt;font-weight:bold;margin:0">{e(D['notice_head'])}</p>
<p align="right" style="font-size:8.5pt;margin:0;padding-top:1pt">{e(D['notice_body'])}</p>
<p align="left" style="font-size:6.5pt;margin:0;padding-top:1pt" dir="ltr">{e(D['notice_en'])}</p>
</td></tr></table>
<hr size="4" color="#000000" noshade="noshade"/>
<p align="right" class="zone" style="margin:0;padding:2pt 0">{e(D['steps_head'])}</p>
{steps}
<hr size="1" color="#000000" noshade="noshade"/>
<p align="right" class="zone" style="margin:0;padding:2pt 0">{e(D['signs_head'])}</p>
{signs}
<hr size="1" color="#000000" noshade="noshade"/>
<table width="100%" cellpadding="3" cellspacing="0" border="3" bordercolor="#000000">
<tr><td align="right">
<p align="right" class="zone" style="margin:0;padding-bottom:4pt">{e(D['never_head'])}</p>
{never}
</td></tr></table>
<hr size="1" color="#000000" noshade="noshade"/>
<p align="right" class="zone" style="margin:0;padding:2pt 0">{e(D['help_head'])}</p>
<table width="100%" cellpadding="0" cellspacing="0">{helps}</table>
<p align="right" style="font-size:11pt;margin:0;padding-top:3pt">{e(D['report'])}</p>
<p align="right" style="font-size:8pt;margin:0;padding-top:2pt">{e(D['foot'])}</p>
<p align="right" style="font-size:11.5pt;font-weight:bold;margin:0;padding-top:2pt">{e(D['footline'])}</p>
</body></html>"""

    src = f"{TMP}/fridge-sheet-ar.html"
    open(src, "w", encoding="utf-8").write(doc)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    src, "--outdir", TMP],
                   check=True, capture_output=True)
    shutil.move(f"{TMP}/fridge-sheet-ar.pdf", f"{OUT}/fridge-sheet-ar.pdf")
    print("built ar sheet")


def build_card():
    one = (
      f'<p align="right" style="font-size:11pt;font-weight:bold;margin:0">{e(D["brand"])}</p>'
      f'<p align="right" style="font-size:7.5pt;font-weight:bold;margin:0;padding-top:2pt">'
      f'{e(D["steps_head"])}</p>'
      + "".join(f'<p align="right" style="font-size:10pt;font-weight:bold;margin:0;'
                f'padding:0 0">{e(imp)} .{i}</p>'
                for i, (imp, _) in enumerate(D["steps"], 1))
      + f'<p align="right" style="font-size:7pt;margin:0;padding-top:2pt">'
        f'{e(D["tagline"])}</p>'
      + '<table width="100%" cellpadding="0" cellspacing="0"><tr>'
      + "".join(f'<td width="50%" align="right">'
                f'<span style="font-size:10.5pt;font-weight:bold">{e(t)}</span><br/>'
                f'<span style="font-size:6pt">{e(w)}</span></td>'
                for t, w in D["helps"])
      + '</tr></table>'
      + f'<p align="right" style="font-size:5.5pt;font-weight:bold;margin:0;'
        f'padding-top:2pt">{e(D["notice_head"])} · translations@trustbutverifyproject.org</p>')

    cells = "".join(
        f'<tr><td width="50%" style="border:1pt dashed #999;padding:7pt">{one}</td>'
        f'<td width="50%" style="border:1pt dashed #999;padding:7pt">{one}</td></tr>'
        for _ in range(3))

    doc = (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
           f'<style>@page{{margin:0.35in 0.4in 0.3in 0.4in}}body,td,p,span{{font-family:"{F}";color:#000}}</style></head>'
           f'<body dir="rtl"><table width="100%" cellpadding="0" cellspacing="0">'
           f'{cells}</table></body></html>')

    src = f"{TMP}/wallet-card-ar.html"
    open(src, "w", encoding="utf-8").write(doc)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                    src, "--outdir", TMP],
                   check=True, capture_output=True)
    shutil.move(f"{TMP}/wallet-card-ar.pdf", f"{OUT}/wallet-card-ar.pdf")
    print("built ar card")


build_sheet()
build_card()
