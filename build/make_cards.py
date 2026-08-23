#!/usr/bin/env python3
"""Wallet / by-the-phone cards. 8 per Letter page, cut on the hairlines."""
import os, html, subprocess, importlib.util

spec = importlib.util.spec_from_file_location("mf", "/home/claude/tbv/build/make_fridge.py")

OUT = "/home/claude/tbv/formats/print"
os.makedirs(OUT, exist_ok=True)

CARDS = {
 "en": dict(font="DejaVu Sans", brand="TRUST BUT VERIFY",
   lead="Before any money moves",
   steps=["Look up the number yourself.",
          "Call the person yourself.",
          "Wait a day."],
   line="You don't have to get suspicious of everybody. You add one step.",
   helps=[("833-372-8311", "Elder Fraud Hotline"),
          ("877-908-3360", "AARP Fraud Watch")],
   tail="Free help. No judgment."),

 "es": dict(font="DejaVu Sans", brand="CONFÍA, PERO VERIFICA",
   lead="Antes de mover cualquier dinero",
   steps=["Busque el número usted mismo.",
          "Llame usted mismo a la persona.",
          "Espere un día."],
   line="No hace falta desconfiar de todos. Solo añada un paso.",
   helps=[("833-372-8311", "Línea Nacional de Fraude"),
          ("877-908-3360", "AARP Fraud Watch")],
   tail="Ayuda gratuita. Sin juicios."),

 "vi": dict(font="DejaVu Sans", brand="TIN TƯỞNG, NHƯNG PHẢI KIỂM CHỨNG",
   lead="Trước khi chuyển bất kỳ khoản tiền nào",
   steps=["Tự mình tra số điện thoại.",
          "Tự mình gọi cho người đó.",
          "Chờ một ngày."],
   line="Không cần nghi ngờ mọi người. Chỉ cần thêm một bước.",
   helps=[("833-372-8311", "Đường dây Quốc gia"),
          ("877-908-3360", "AARP Fraud Watch")],
   tail="Miễn phí. Có thông dịch."),

 "ru": dict(font="DejaVu Sans", brand="ДОВЕРЯЙ, НО ПРОВЕРЯЙ",
   lead="Прежде чем уйдут любые деньги",
   steps=["Найдите номер сами.",
          "Позвоните человеку сами.",
          "Подождите сутки."],
   line="Не нужно подозревать всех. Нужен один шаг.",
   helps=[("833-372-8311", "Национальная линия"),
          ("877-908-3360", "AARP Fraud Watch")],
   tail="Бесплатно. Есть переводчик."),

 "zh": dict(font="Noto Sans CJK SC", brand="信任，但要核实",
   lead="在任何一笔钱转出去之前",
   steps=["自己去查电话号码。",
          "自己打电话给那个人。",
          "等一天。"],
   line="您不需要怀疑每一个人。只需多加一个步骤。",
   helps=[("833-372-8311", "全国老年人诈骗热线"),
          ("877-908-3360", "AARP 反诈热线")],
   tail="免费求助。提供翻译。"),
}

NOTICE = {'es': 'AVISO: traducción sin validar. No imprimir aún. ¿Habla español? Ayúdenos: translations@trustbutverifyproject.org', 'vi': 'LƯU Ý: bản dịch chưa kiểm chứng. Xin chưa in. Xin giúp chúng tôi: translations@trustbutverifyproject.org', 'ru': 'ВНИМАНИЕ: непроверенный перевод. Пока не печатайте. Помогите нам: translations@trustbutverifyproject.org', 'zh': '注意：翻译未经核校，请暂勿打印。请帮我们校对：translations@trustbutverifyproject.org'}


CARDS.update({
 "uk": dict(font="DejaVu Sans", brand="ДОВІРЯЙ, АЛЕ ПЕРЕВІРЯЙ",
   lead="Перш ніж підуть будь-які гроші",
   steps=["Знайдіть номер самі.","Зателефонуйте людині самі.","Зачекайте добу."],
   line="Не треба підозрювати всіх. Потрібен один крок.",
   helps=[("833-372-8311","Національна лінія"),("877-908-3360","AARP Fraud Watch")],
   tail="Безкоштовно. Є перекладач."),
 "fr": dict(font="DejaVu Sans", brand="FAITES CONFIANCE, MAIS VÉRIFIEZ",
   lead="Avant que le moindre argent ne parte",
   steps=["Cherchez le numéro vous-même.","Appelez la personne vous-même.","Attendez un jour."],
   line="Pas besoin de se méfier de tous. Ajoutez une étape.",
   helps=[("833-372-8311","Ligne nationale"),("877-908-3360","AARP Fraud Watch")],
   tail="Gratuit. Interprète disponible."),
 "de": dict(font="DejaVu Sans", brand="VERTRAUEN, ABER NACHPRÜFEN",
   lead="Bevor Geld fließt",
   steps=["Suchen Sie die Nummer selbst.","Rufen Sie die Person selbst an.","Warten Sie einen Tag."],
   line="Sie müssen nicht jedem misstrauen. Ein Schritt genügt.",
   helps=[("833-372-8311","Nationale Hotline"),("877-908-3360","AARP Fraud Watch")],
   tail="Kostenlos. Dolmetscher verfügbar."),
 "pt": dict(font="DejaVu Sans", brand="CONFIE, MAS VERIFIQUE",
   lead="Antes que qualquer dinheiro saia",
   steps=["Procure o número você mesmo.","Ligue você mesmo para a pessoa.","Espere um dia."],
   line="Não precisa desconfiar de todos. Acrescente um passo.",
   helps=[("833-372-8311","Linha Nacional"),("877-908-3360","AARP Fraud Watch")],
   tail="Gratuito. Há intérprete."),
 "pl": dict(font="DejaVu Sans", brand="UFAJ, ALE SPRAWDZAJ",
   lead="Zanim wyjdą jakiekolwiek pieniądze",
   steps=["Sam znajdź numer.","Sam zadzwoń do tej osoby.","Odczekaj dobę."],
   line="Nie musisz podejrzewać wszystkich. Dodaj jeden krok.",
   helps=[("833-372-8311","Infolinia krajowa"),("877-908-3360","AARP Fraud Watch")],
   tail="Bezpłatnie. Jest tłumacz."),
 "ro": dict(font="DejaVu Sans", brand="AI ÎNCREDERE, DAR VERIFICĂ",
   lead="Înainte să plece orice ban",
   steps=["Căutați singur numărul.","Sunați dumneavoastră persoana.","Așteptați o zi."],
   line="Nu trebuie să suspectezi pe toți. Adaugă un pas.",
   helps=[("833-372-8311","Linia Națională"),("877-908-3360","AARP Fraud Watch")],
   tail="Gratuit. Există interpret."),
 "id": dict(font="DejaVu Sans", brand="PERCAYA, TAPI PERIKSA",
   lead="Sebelum uang berpindah",
   steps=["Cari sendiri nomor teleponnya.","Telepon sendiri orangnya.","Tunggu satu hari."],
   line="Tak perlu mencurigai semua orang. Tambah satu langkah.",
   helps=[("833-372-8311","Saluran Nasional"),("877-908-3360","AARP Fraud Watch")],
   tail="Gratis. Tersedia juru bahasa."),
})

NOTICE.update({
 "uk":"УВАГА: неперевірений переклад. Поки не друкуйте. Допоможіть нам: translations@trustbutverifyproject.org",
 "fr":"AVIS : traduction non validée. Ne pas imprimer. Aidez-nous : translations@trustbutverifyproject.org",
 "de":"HINWEIS: ungeprüfte Übersetzung. Noch nicht drucken. Helfen Sie uns: translations@trustbutverifyproject.org",
 "pt":"AVISO: tradução não validada. Não imprimir ainda. Ajude-nos: translations@trustbutverifyproject.org",
 "pl":"UWAGA: tłumaczenie niezweryfikowane. Nie drukuj. Pomóż nam: translations@trustbutverifyproject.org",
 "ro":"ATENȚIE: traducere neverificată. Nu tipăriți încă. Ajutați-ne: translations@trustbutverifyproject.org",
 "id":"PERHATIAN: terjemahan belum diperiksa. Jangan dicetak dulu. Bantu kami: translations@trustbutverifyproject.org",
})

TPL = """<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<style>
 * {{ box-sizing:border-box; margin:0; padding:0; }}
 body {{ font-family:"{font}","DejaVu Sans",sans-serif; color:#000; }}
 table {{ border-collapse:collapse; width:100%; }}
 td {{ width:50%; height:2.42in; border:0.5pt dashed #999; padding:13pt 15pt;
       vertical-align:top; }}
 .brand {{ font-size:{bs}pt; font-weight:700; letter-spacing:1px; line-height:1.05; }}
 .lead {{ font-size:10pt; font-weight:700; letter-spacing:0.8px;
          border-top:2pt solid #000; margin-top:4pt; padding-top:5pt; }}
 ol {{ margin:5pt 0 0 17pt; }}
 li {{ font-size:14pt; font-weight:700; line-height:1.24; padding:1pt 0; }}
 .line {{ font-size:10pt; line-height:1.25; margin-top:4pt; }}
 .helps {{ display:flex; gap:9pt; border-top:1pt solid #000; margin-top:5pt;
           padding-top:4pt; }}
 .h {{ flex:1; }}
 .tel {{ font-size:15pt; font-weight:700; letter-spacing:-0.3px; }}
 .who {{ font-size:9pt; line-height:1.2; }}
 .note {{ font-size:7pt; line-height:1.2; margin-top:3pt;
         border-top:0.75pt solid #000; padding-top:3pt; font-weight:700; }}
 .tail {{ font-size:9pt; margin-top:3pt; }}
</style></head><body><table>{rows}</table></body></html>"""


def card(d, e, code):
    steps = "".join(f"<li>{e(s)}</li>" for s in d["steps"])
    helps = "".join(f'<div class="h"><div class="tel">{e(t)}</div>'
                    f'<div class="who">{e(w)}</div></div>' for t, w in d["helps"])
    return (f'<div class="brand">{e(d["brand"])}</div>'
            f'<div class="lead">{e(d["lead"])}</div>'
            f'<ol>{steps}</ol>'
            f'<div class="line">{e(d["line"])}</div>'
            f'<div class="helps">{helps}</div>'
            f'<div class="tail">{e(d["tail"])}</div>'
            + (f'<div class="note">{e(NOTICE[code])}</div>' if code in NOTICE else ''))


for code, d in CARDS.items():
    e = html.escape
    one = card(d, e, code)
    rows = "".join("<tr><td>" + one + "</td><td>" + one + "</td></tr>"
                   for _ in range(4))
    n = len(d["brand"])
    bs = 15.5 if n <= 20 else (12 if n <= 28 else 10)
    out = TPL.format(lang=code, font=d["font"], bs=bs, rows=rows)
    h = f"{OUT}/wallet-card-{code}.html"
    open(h, "w", encoding="utf-8").write(out)
    subprocess.run(["wkhtmltopdf", "--quiet", "--page-size", "Letter",
                    "-T", "13mm", "-B", "13mm", "-L", "13mm", "-R", "13mm",
                    h, f"{OUT}/wallet-card-{code}.pdf"], check=True)
    print("card", code)
