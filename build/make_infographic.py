#!/usr/bin/env python3
"""
One-page "by the numbers" infographic — English plus the top 10 languages
by site priority (matches TRANSLATIONS.md / LANGS order: es, vi, zh, ru,
ko, tl, hi, bn, hy, am).

More visual than the fridge sheet on purpose: a big headline stat, a bar
comparison of where the money actually goes, then the same three-step method
everything else on this site teaches. Sources: FBI IC3 2025 Internet Crime
Report (ic3.gov) and FTC Protecting Older Consumers 2024-2025 (ftc.gov).

Font/wrap notes (same lessons as make_fridge_new_langs.py and
make_cards_new_langs.py — see BACKLOG.md): reportlab's base-14 fonts are
Latin-1 only, so non-Latin scripts need a real Unicode font registered
explicitly or they render as tofu boxes. And reportlab's word-wrap just
does `text.split()`, which doesn't work for Chinese (no spaces between
words) without a character-level fallback.

    python3 build/make_infographic.py
"""
import os, io
import qrcode
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "formats", "print")

INK = HexColor("#111111")
MUTED = HexColor("#4a4a4a")
PAPER = HexColor("#fffdf9")
ACCENT = HexColor("#123f7a")
BAND = HexColor("#f0ece4")

W, H = 612, 792
M = 42  # page margin

# --- Unicode font registration (see note above) -----------------------------

SYS = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(SYS, "Arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(SYS, "Arial Bold.ttf")))
pdfmetrics.registerFont(TTFont("ArialUnicode", os.path.join(SYS, "Arial Unicode.ttf")))
pdfmetrics.registerFont(TTFont("KefaIII", os.path.join(SYS, "KefaIII.ttf")))

# Arial/Arial-Bold cover Latin-1 plus Cyrillic (ru). Everything else needs
# Arial Unicode (no separate bold weight -- both roles reuse the regular
# face) or, for Amharic, KefaIII.
FONTS = {
    "zh": ("ArialUnicode", "ArialUnicode"),
    "ko": ("ArialUnicode", "ArialUnicode"),
    "hi": ("ArialUnicode", "ArialUnicode"),
    "bn": ("ArialUnicode", "ArialUnicode"),
    "hy": ("ArialUnicode", "ArialUnicode"),
    "am": ("KefaIII", "KefaIII"),
}


def fonts_for(lang):
    return FONTS.get(lang, ("Arial", "Arial-Bold"))


def _units_for(text):
    # Fall back to character-level wrapping for scripts that don't use
    # spaces between words (Chinese) -- word-splitting alone would treat
    # a whole sentence as a single unbreakable "word".
    space_ratio = text.count(" ") / max(1, len(text))
    if space_ratio > 0.03:
        return text.split(), " "
    return list(text), ""


def wrap(c, text, x, y, font, size, max_w, leading, color=INK, align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    units, sep = _units_for(text)
    line = ""
    for u in units:
        test = (line + sep + u) if line else u
        if stringWidth(test, font, size) > max_w and line:
            _draw_line(c, line, x, y, font, size, max_w, align)
            y -= leading
            line = u
        else:
            line = test
    if line:
        _draw_line(c, line, x, y, font, size, max_w, align)
        y -= leading
    return y


def _draw_line(c, line, x, y, font, size, max_w, align):
    if align == "center":
        c.drawCentredString(x + max_w / 2, y, line)
    else:
        c.drawString(x, y, line)


def qr_image(url, suffix):
    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#123f7a", back_color="#fffdf9")
    path = os.path.join(OUT_DIR, "infographic-%s.pdf.qr.png" % suffix)
    img.save(path)
    return path


def bar(c, x, y, w, h, frac, label, amount, font, color=ACCENT):
    c.setFillColor(BAND)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(color)
    c.rect(x, y, w * frac, h, fill=1, stroke=0)
    c.setFont(font, 10)
    c.setFillColor(INK)
    c.drawString(x, y + h + 5, label)
    c.setFont(font, 11)
    c.drawRightString(x + w, y + h + 5, amount)


# --- English (base) content, same shape as CONTENT[lang] below --------------

EN = dict(
    strap="Elder fraud, by the numbers — and the one habit that stops most of it",
    headline="$7.7 BILLION",
    headline_sub="lost by Americans 60+ to fraud in 2025 — a 59% jump in one year",
    headline_detail="201,266 complaints filed. Average loss per victim: $38,500. FBI IC3, 2025.",
    bars_header="WHERE THE MONEY ACTUALLY GOES",
    bars=[
        ("Investment fraud (crypto, fake trading platforms)", "$3.52B"),
        ("Recovery scams — stealing from people already scammed once", "$540M"),
        ("Tech support scams (FTC, 2024)", "$159M"),
        ("Grandparent / distress scams, voice cloning", "$5M+"),
    ],
    bars_footnote="Bar length shows relative size, not to scale below ~1%. FBI IC3 2025 Elder Fraud data; FTC 2024-2025 for tech support.",
    rising_header="WHAT'S GROWING FASTEST",
    rising=[
        ("Phishing / spoofing texts and emails, age 60+", "up over 100%"),
        ("Government impersonation calls", "nearly doubled"),
        ("Romance scams targeting older adults", "up 30%"),
        ("Scams referencing or using AI voice cloning", "3,100+ complaints, $352M+ lost"),
    ],
    method_header="THE ONE HABIT THAT STOPS MOST OF THIS",
    steps=[
        ("1", "Look up the number yourself.", "Not the one they gave you."),
        ("2", "Call the person yourself.", "Hang up first. If it was real, they'll still be there."),
        ("3", "Wait a day.", "Real problems survive a night's sleep. Scams don't."),
    ],
    footer_header="FREE HELP — NO JUDGMENT",
    hotline1_label="National Elder Fraud Hotline",
    hotline2_label="AARP Fraud Watch",
    report_line="Report at ic3.gov and reportfraud.ftc.gov  ·  Sources: FBI IC3 2025 Internet Crime Report, FTC Protecting Older Consumers 2024-2025",
)

# --- Translated content, top 10 languages by site priority ------------------
# All unvalidated AI translations awaiting a native speaker's review, same
# as every other non-English page on this site. Numbers/currency stay as
# Western digits throughout, matching the fridge-sheet convention.

CONTENT = {"en": EN}

CONTENT["es"] = dict(
    strap="El fraude a personas mayores, en números — y el único hábito que detiene la mayoría",
    headline="$7.7 MIL MILLONES",
    headline_sub="perdidos por estadounidenses de 60+ años por fraude en 2025 — un aumento del 59% en un año",
    headline_detail="201,266 denuncias presentadas. Pérdida promedio por víctima: $38,500. FBI IC3, 2025.",
    bars_header="A DÓNDE VA REALMENTE EL DINERO",
    bars=[
        ("Fraude de inversión (cripto, plataformas falsas)", "$3.52B"),
        ("Estafas de recuperación — roban a quienes ya fueron estafados", "$540M"),
        ("Estafas de soporte técnico (FTC, 2024)", "$159M"),
        ("Estafa del nieto / voz clonada por IA", "$5M+"),
    ],
    bars_footnote="El largo de la barra muestra el tamaño relativo, no a escala por debajo de ~1%. Datos de fraude a mayores del FBI IC3 2025; FTC 2024-2025 para soporte técnico.",
    rising_header="LO QUE MÁS ESTÁ CRECIENDO",
    rising=[
        ("Mensajes y correos de phishing, 60+ años", "más del 100%"),
        ("Llamadas de suplantación del gobierno", "casi el doble"),
        ("Estafas románticas dirigidas a mayores", "30% más"),
        ("Estafas con voz clonada por IA", "3,100+ denuncias, $352M+ perdidos"),
    ],
    method_header="EL ÚNICO HÁBITO QUE DETIENE LA MAYORÍA",
    steps=[
        ("1", "Busque el número usted mismo.", "No el que le dieron."),
        ("2", "Llame usted mismo a la persona.", "Cuelgue primero. Si era real, seguirán ahí."),
        ("3", "Espere un día.", "Los problemas reales sobreviven una noche. Las estafas no."),
    ],
    footer_header="AYUDA GRATIS — SIN JUICIOS",
    hotline1_label="Línea Nacional de Fraude a Mayores",
    hotline2_label="AARP Fraud Watch",
    report_line="Reporte en ic3.gov y reportfraud.ftc.gov  ·  Fuentes: Informe FBI IC3 2025, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["vi"] = dict(
    strap="Lừa đảo người cao tuổi, bằng con số — và thói quen duy nhất ngăn chặn phần lớn",
    headline="7,7 TỶ ĐÔ LA",
    headline_sub="người Mỹ trên 60 tuổi mất vì lừa đảo năm 2025 — tăng 59% trong một năm",
    headline_detail="201.266 đơn khiếu nại. Thiệt hại trung bình mỗi nạn nhân: $38,500. FBI IC3, 2025.",
    bars_header="TIỀN THỰC SỰ ĐI ĐÂU",
    bars=[
        ("Lừa đảo đầu tư (tiền mã hóa, sàn giao dịch giả)", "$3.52B"),
        ("Lừa đảo 'thu hồi tiền' — nhắm vào người đã bị lừa", "$540M"),
        ("Lừa đảo hỗ trợ kỹ thuật (FTC, 2024)", "$159M"),
        ("Lừa đảo cháu nội / giọng nói giả bằng AI", "$5M+"),
    ],
    bars_footnote="Độ dài thanh thể hiện quy mô tương đối, không theo tỷ lệ dưới ~1%. Dữ liệu FBI IC3 2025; FTC 2024-2025 cho hỗ trợ kỹ thuật.",
    rising_header="TĂNG NHANH NHẤT",
    rising=[
        ("Tin nhắn / email lừa đảo, tuổi 60+", "tăng hơn 100%"),
        ("Cuộc gọi giả danh chính phủ", "gần gấp đôi"),
        ("Lừa đảo tình cảm nhắm vào người cao tuổi", "tăng 30%"),
        ("Lừa đảo dùng giọng nói giả bằng AI", "hơn 3.100 đơn, mất hơn $352M"),
    ],
    method_header="THÓI QUEN DUY NHẤT NGĂN CHẶN PHẦN LỚN",
    steps=[
        ("1", "Tự mình tra số điện thoại.", "Không phải số họ đưa cho bạn."),
        ("2", "Tự mình gọi cho người đó.", "Cúp máy trước. Nếu là thật, họ vẫn còn đó."),
        ("3", "Chờ một ngày.", "Vấn đề thật sẽ còn đó sau một đêm. Lừa đảo thì không."),
    ],
    footer_header="TRỢ GIÚP MIỄN PHÍ — KHÔNG PHÁN XÉT",
    hotline1_label="Đường dây Quốc gia về Lừa đảo Người cao tuổi",
    hotline2_label="AARP Fraud Watch",
    report_line="Báo cáo tại ic3.gov và reportfraud.ftc.gov  ·  Nguồn: Báo cáo FBI IC3 2025, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["zh"] = dict(
    strap="老年人诈骗数据一览——以及能阻止大多数骗局的一个习惯",
    headline="77亿美元",
    headline_sub="2025年60岁以上美国人因诈骗损失的金额——比上一年增加59%",
    headline_detail="共提交201,266起投诉。每位受害者平均损失:$38,500。数据来源:FBI IC3,2025年。",
    bars_header="钱究竟去了哪里",
    bars=[
        ("投资诈骗(加密货币、虚假交易平台)", "$3.52B"),
        ("'追回资金'诈骗——专门针对已被骗过的人", "$540M"),
        ("技术支持诈骗(FTC,2024年)", "$159M"),
        ("冒充孙辈 / AI克隆声音诈骗", "$5M+"),
    ],
    bars_footnote="条形长度表示相对大小,低于约1%时不按比例显示。数据来源:FBI IC3 2025年老年人诈骗数据;技术支持部分为FTC 2024-2025年数据。",
    rising_header="增长最快的诈骗类型",
    rising=[
        ("针对60岁以上人群的钓鱼短信/邮件", "增长超过100%"),
        ("冒充政府机构来电", "增长近一倍"),
        ("针对老年人的网络婚恋诈骗", "增长30%"),
        ("使用AI克隆声音的诈骗", "3,100+起投诉,损失超$352M"),
    ],
    method_header="能阻止大多数骗局的一个习惯",
    steps=[
        ("1", "自己查号码。", "不是对方给你的号码。"),
        ("2", "自己打电话给本人。", "先挂断电话,再拨打。如果是真的,他们还会在。"),
        ("3", "等一天。", "真正的问题经得起一晚的等待,骗局经不起。"),
    ],
    footer_header="免费帮助——绝不评判",
    hotline1_label="全国老年人诈骗热线",
    hotline2_label="AARP诈骗监察热线",
    report_line="在ic3.gov和reportfraud.ftc.gov举报  ·  数据来源:FBI IC3 2025年互联网犯罪报告,FTC 2024-2025年保护老年消费者报告",
)

CONTENT["ru"] = dict(
    strap="Мошенничество против пожилых людей в цифрах — и единственная привычка, которая останавливает большинство случаев",
    headline="$7,7 МИЛЛИАРДА",
    headline_sub="потеряли американцы старше 60 лет из-за мошенничества в 2025 году — рост на 59% за год",
    headline_detail="201 266 поданных жалоб. Средний убыток на жертву: $38 500. FBI IC3, 2025.",
    bars_header="КУДА НА САМОМ ДЕЛЕ УХОДЯТ ДЕНЬГИ",
    bars=[
        ("Инвестиционное мошенничество (крипто, фальшивые платформы)", "$3.52B"),
        ("Мошенничество «возврата денег» — обман уже обманутых", "$540M"),
        ("Мошенничество тех. поддержки (FTC, 2024)", "$159M"),
        ("Обман «внук в беде» / клонированный ИИ-голос", "$5M+"),
    ],
    bars_footnote="Длина полосы показывает относительный размер, не в масштабе ниже ~1%. Данные FBI IC3 2025 по мошенничеству против пожилых; FTC 2024-2025 по тех. поддержке.",
    rising_header="ЧТО РАСТЁТ БЫСТРЕЕ ВСЕГО",
    rising=[
        ("Фишинговые сообщения и письма, возраст 60+", "рост более 100%"),
        ("Звонки с имитацией госорганов", "почти удвоение"),
        ("Романтическое мошенничество против пожилых", "рост на 30%"),
        ("Мошенничество с использованием ИИ-клонирования голоса", "3 100+ жалоб, потеряно $352M+"),
    ],
    method_header="ЕДИНСТВЕННАЯ ПРИВЫЧКА, КОТОРАЯ ОСТАНАВЛИВАЕТ БОЛЬШИНСТВО СЛУЧАЕВ",
    steps=[
        ("1", "Найдите номер сами.", "Не тот, что вам дали."),
        ("2", "Позвоните человеку сами.", "Сначала положите трубку. Если это правда, они всё ещё будут на месте."),
        ("3", "Подождите сутки.", "Настоящие проблемы переживут ночь. Мошенничество — нет."),
    ],
    footer_header="БЕСПЛАТНАЯ ПОМОЩЬ — БЕЗ ОСУЖДЕНИЯ",
    hotline1_label="Национальная горячая линия по мошенничеству против пожилых",
    hotline2_label="AARP Fraud Watch",
    report_line="Сообщите на ic3.gov и reportfraud.ftc.gov  ·  Источники: отчёт FBI IC3 2025, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["ko"] = dict(
    strap="숫자로 보는 노인 사기 — 그리고 대부분을 막아주는 단 하나의 습관",
    headline="77억 달러",
    headline_sub="2025년 60세 이상 미국인이 사기로 잃은 금액 — 전년 대비 59% 증가",
    headline_detail="201,266건 신고 접수. 피해자 1인당 평균 손실액: $38,500. FBI IC3, 2025년.",
    bars_header="돈이 실제로 어디로 가는가",
    bars=[
        ("투자 사기 (암호화폐, 가짜 거래 플랫폼)", "$3.52B"),
        ("'돈 되찾아 주기' 사기 — 이미 사기당한 사람을 다시 노림", "$540M"),
        ("기술지원 사기 (FTC, 2024년)", "$159M"),
        ("손주 사칭 / AI 음성 복제 사기", "$5M+"),
    ],
    bars_footnote="막대 길이는 상대적 크기를 나타내며, 약 1% 미만은 비례하지 않습니다. FBI IC3 2025 노인 사기 데이터; 기술지원 부분은 FTC 2024-2025년 자료.",
    rising_header="가장 빠르게 증가하는 유형",
    rising=[
        ("60세 이상 대상 피싱 문자/이메일", "100% 이상 증가"),
        ("정부 사칭 전화", "거의 두 배 증가"),
        ("노인 대상 로맨스 스캠", "30% 증가"),
        ("AI 음성 복제를 이용한 사기", "3,100건 이상 신고, $352M 이상 손실"),
    ],
    method_header="대부분을 막아주는 단 하나의 습관",
    steps=[
        ("1", "번호를 직접 찾아보세요.", "상대방이 알려준 번호가 아닙니다."),
        ("2", "본인이 직접 전화하세요.", "먼저 전화를 끊으세요. 진짜라면 다시 걸어도 그대로 있을 것입니다."),
        ("3", "하루를 기다리세요.", "진짜 문제는 하룻밤을 견딥니다. 사기는 그렇지 않습니다."),
    ],
    footer_header="무료 도움 — 비난하지 않습니다",
    hotline1_label="전국 노인 사기 신고 전화",
    hotline2_label="AARP 사기 감시",
    report_line="ic3.gov와 reportfraud.ftc.gov에 신고하세요  ·  출처: FBI IC3 2025 인터넷 범죄 보고서, FTC 2024-2025 Protecting Older Consumers",
)

CONTENT["tl"] = dict(
    strap="Pandaraya sa mga nakatatanda, sa mga numero — at ang isang gawi na pumipigil sa karamihan nito",
    headline="$7.7 BILYON",
    headline_sub="nawala sa mga Amerikanong 60+ dahil sa scam noong 2025 — 59% na pagtaas sa loob ng isang taon",
    headline_detail="201,266 na reklamong isinampa. Karaniwang nawala bawat biktima: $38,500. FBI IC3, 2025.",
    bars_header="SAAN TALAGA NAPUPUNTA ANG PERA",
    bars=[
        ("Investment scam (crypto, pekeng trading platform)", "$3.52B"),
        ("Recovery scam — muling niloloko ang mga na-scam na", "$540M"),
        ("Tech support scam (FTC, 2024)", "$159M"),
        ("Apo scam / ginayang boses gamit ang AI", "$5M+"),
    ],
    bars_footnote="Ipinapakita ng haba ng bar ang relatibong laki, hindi eksakto sa sukat kung mas mababa sa ~1%. Datos ng FBI IC3 2025 para sa elder fraud; FTC 2024-2025 para sa tech support.",
    rising_header="PINAKAMABILIS LUMALAKI",
    rising=[
        ("Phishing na text at email, edad 60+", "tumaas nang higit 100%"),
        ("Mga tawag na nagpapanggap na gobyerno", "halos doble"),
        ("Romance scam na tumatarget sa mga nakatatanda", "tumaas 30%"),
        ("Scam gamit ang AI voice cloning", "3,100+ reklamo, $352M+ nawala"),
    ],
    method_header="ANG ISANG GAWI NA PUMIPIGIL SA KARAMIHAN NITO",
    steps=[
        ("1", "Hanapin mo mismo ang numero.", "Hindi yung binigay nila sa iyo."),
        ("2", "Tawagan mo mismo ang tao.", "Ibaba muna. Kung totoo, nandiyan pa rin sila."),
        ("3", "Maghintay ng isang araw.", "Ang totoong problema ay nabubuhay sa magdamag. Ang scam, hindi."),
    ],
    footer_header="LIBRENG TULONG — WALANG PANGHUHUSGA",
    hotline1_label="National Elder Fraud Hotline",
    hotline2_label="AARP Fraud Watch",
    report_line="Mag-report sa ic3.gov at reportfraud.ftc.gov  ·  Pinagmulan: FBI IC3 2025 Report, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["hi"] = dict(
    strap="बुज़ुर्गों के साथ धोखाधड़ी, आंकड़ों में — और वह एक आदत जो ज़्यादातर मामलों को रोक देती है",
    headline="$7.7 अरब",
    headline_sub="2025 में 60+ उम्र के अमेरिकियों ने धोखाधड़ी में गंवाए — एक साल में 59% की बढ़ोतरी",
    headline_detail="201,266 शिकायतें दर्ज। हर पीड़ित का औसत नुकसान: $38,500। FBI IC3, 2025।",
    bars_header="पैसा असल में कहाँ जाता है",
    bars=[
        ("निवेश धोखाधड़ी (क्रिप्टो, नकली ट्रेडिंग प्लेटफ़ॉर्म)", "$3.52B"),
        ("'पैसा वापस दिलाने' का धोखा — पहले ठगे गए लोगों को फिर ठगना", "$540M"),
        ("टेक सपोर्ट धोखाधड़ी (FTC, 2024)", "$159M"),
        ("पोते-पोती का बहाना / AI से नकली आवाज़", "$5M+"),
    ],
    bars_footnote="बार की लंबाई सापेक्ष आकार दिखाती है, ~1% से कम में सटीक अनुपात में नहीं। FBI IC3 2025 का डेटा; टेक सपोर्ट के लिए FTC 2024-2025।",
    rising_header="सबसे तेज़ी से बढ़ रहा है",
    rising=[
        ("फ़िशिंग टेक्स्ट और ईमेल, उम्र 60+", "100% से ज़्यादा बढ़ोतरी"),
        ("सरकार बनकर की गई कॉलें", "लगभग दोगुना"),
        ("बुज़ुर्गों को निशाना बनाने वाले रोमांस स्कैम", "30% बढ़ोतरी"),
        ("AI आवाज़ क्लोनिंग का उपयोग करने वाले स्कैम", "3,100+ शिकायतें, $352M+ का नुकसान"),
    ],
    method_header="वह एक आदत जो ज़्यादातर मामलों को रोक देती है",
    steps=[
        ("1", "नंबर खुद ढूंढें।", "वह नहीं जो उन्होंने आपको दिया।"),
        ("2", "व्यक्ति को खुद कॉल करें।", "पहले फ़ोन रखें। अगर सच होगा, तो वे अभी भी वहीं होंगे।"),
        ("3", "एक दिन रुकें।", "असली समस्याएं एक रात में खत्म नहीं होतीं। धोखाधड़ी नहीं टिकती।"),
    ],
    footer_header="मुफ़्त मदद — कोई जजमेंट नहीं",
    hotline1_label="नेशनल एल्डर फ्रॉड हॉटलाइन",
    hotline2_label="AARP फ्रॉड वॉच",
    report_line="ic3.gov और reportfraud.ftc.gov पर रिपोर्ट करें  ·  स्रोत: FBI IC3 2025 रिपोर्ट, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["bn"] = dict(
    strap="সংখ্যায় প্রবীণ প্রতারণা — এবং একটি অভ্যাস যা বেশিরভাগ ঠেকিয়ে দেয়",
    headline="$7.7 বিলিয়ন",
    headline_sub="2025 সালে জালিয়াতির কারণে 60+ বয়সী আমেরিকানরা এই পরিমাণ হারিয়েছেন — এক বছরে 59% বৃদ্ধি",
    headline_detail="201,266 টি অভিযোগ দাখিল হয়েছে। প্রতি ভুক্তভোগীর গড় ক্ষতি: $38,500। FBI IC3, 2025।",
    bars_header="টাকা আসলে কোথায় যাচ্ছে",
    bars=[
        ("বিনিয়োগ জালিয়াতি (ক্রিপ্টো, ভুয়া ট্রেডিং প্ল্যাটফর্ম)", "$3.52B"),
        ("'টাকা ফেরত' জালিয়াতি — আগে প্রতারিত হওয়া মানুষদের আবার ঠকানো", "$540M"),
        ("টেক সাপোর্ট জালিয়াতি (FTC, 2024)", "$159M"),
        ("নাতি-নাতনির ছল / AI দিয়ে নকল কণ্ঠস্বর", "$5M+"),
    ],
    bars_footnote="বারের দৈর্ঘ্য আপেক্ষিক আকার দেখায়, ~1% এর নিচে সঠিক অনুপাতে নয়। FBI IC3 2025 তথ্য; টেক সাপোর্টের জন্য FTC 2024-2025।",
    rising_header="সবচেয়ে দ্রুত বাড়ছে",
    rising=[
        ("ফিশিং টেক্সট ও ইমেইল, বয়স 60+", "100% এর বেশি বৃদ্ধি"),
        ("সরকার সেজে করা কল", "প্রায় দ্বিগুণ"),
        ("প্রবীণদের লক্ষ্য করে রোমান্স স্ক্যাম", "30% বৃদ্ধি"),
        ("AI কণ্ঠস্বর নকল করা স্ক্যাম", "3,100+ অভিযোগ, $352M+ ক্ষতি"),
    ],
    method_header="একটি অভ্যাস যা বেশিরভাগ ঠেকিয়ে দেয়",
    steps=[
        ("1", "নিজে নম্বর খুঁজুন।", "তারা যেটা দিয়েছে সেটা নয়।"),
        ("2", "নিজে ব্যক্তিকে কল করুন।", "আগে ফোন রাখুন। সত্যি হলে, তারা তখনও থাকবে।"),
        ("3", "একদিন অপেক্ষা করুন।", "আসল সমস্যা এক রাত টিকে থাকে। প্রতারণা টেকে না।"),
    ],
    footer_header="বিনামূল্যে সাহায্য — কোনো বিচার নেই",
    hotline1_label="ন্যাশনাল এল্ডার ফ্রড হটলাইন",
    hotline2_label="AARP ফ্রড ওয়াচ",
    report_line="ic3.gov এবং reportfraud.ftc.gov-এ রিপোর্ট করুন  ·  সূত্র: FBI IC3 2025 রিপোর্ট, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["hy"] = dict(
    strap="Տարեցների նկատմամբ խարդախությունը թվերով — և մեկ սովորությունը, որը կանգնեցնում է դեպքերի մեծ մասը",
    headline="$7.7 ՄԻԼԻԱՐԴ",
    headline_sub="կորցրել են 60+ տարեկան ամերիկացիները խարդախության հետևանքով 2025-ին — 59% աճ մեկ տարվա ընթացքում",
    headline_detail="201,266 բողոք է ներկայացվել։ Միջին կորուստը մեկ զոհի հաշվով՝ $38,500։ FBI IC3, 2025։",
    bars_header="ՈՒՐ Է ԻՐԱԿԱՆՈՒՄ ԳՆՈՒՄ ԴՐԱՄԸ",
    bars=[
        ("Ներդրումային խարդախություն (կրիպտո, կեղծ առևտրային հարթակներ)", "$3.52B"),
        ("«Դրամի վերադարձի» խարդախություն — կրկին խաբում են արդեն խաբվածներին", "$540M"),
        ("Տեխնիկական աջակցության խարդախություն (FTC, 2024)", "$159M"),
        ("Թոռան մասին սուտ / AI-ով կեղծված ձայն", "$5M+"),
    ],
    bars_footnote="Գծի երկարությունը ցույց է տալիս հարաբերական չափը, ոչ ճշգրիտ մասշտաբով ~1%-ից ցածր դեպքում։ FBI IC3 2025 տվյալներ; FTC 2024-2025՝ տեխնիկական աջակցության համար։",
    rising_header="ԱՄԵՆԱԱՐԱԳ ԱՃՈՂԸ",
    rising=[
        ("Ֆիշինգ հաղորդագրություններ և նամակներ, 60+ տարիք", "աճ՝ ավելի քան 100%"),
        ("Կառավարությանը նմանակող զանգեր", "գրեթե կրկնապատկվել է"),
        ("Տարեցներին ուղղված սիրավեպի խարդախություններ", "աճ՝ 30%"),
        ("AI ձայնային կլոնավորում օգտագործող խարդախություններ", "3,100+ բողոք, $352M+ կորուստ"),
    ],
    method_header="ՄԵԿ ՍՈՎՈՐՈՒԹՅՈՒՆ, ՈՐԸ ԿԱՆԳՆԵՑՆՈՒՄ Է ԴԵՊՔԵՐԻ ՄԵԾ ՄԱՍԸ",
    steps=[
        ("1", "Ինքներդ գտեք համարը։", "Ոչ այն, որ ձեզ տվեցին։"),
        ("2", "Ինքներդ զանգահարեք մարդուն։", "Նախ փակեք հեռախոսը։ Եթե իրական է, նրանք դեռ այնտեղ կլինեն։"),
        ("3", "Սպասեք մեկ օր։", "Իրական խնդիրները դիմանում են գիշերվան։ Խարդախությունը՝ ոչ։"),
    ],
    footer_header="ԱՆՎՃԱՐ ՕԳՆՈՒԹՅՈՒՆ — ԱՌԱՆՑ ԴԱՏԱՊԱՐՏՄԱՆ",
    hotline1_label="Տարեցների խարդախության ազգային թեժ գիծ",
    hotline2_label="AARP Fraud Watch",
    report_line="Հայտնեք ic3.gov և reportfraud.ftc.gov կայքերում  ·  Աղբյուրներ՝ FBI IC3 2025 զեկույց, FTC Protecting Older Consumers 2024-2025",
)

CONTENT["am"] = dict(
    strap="የአዛውንት ማጭበርበር በቁጥር — እና አብዛኛውን የሚያስቆም አንድ ልማድ",
    headline="$7.7 ቢሊዮን",
    headline_sub="በ2025 60+ ዕድሜ ያላቸው አሜሪካውያን በማጭበርበር ያጡት — በአንድ ዓመት ውስጥ በ59% ጭማሪ",
    headline_detail="201,266 ቅሬታዎች ቀርበዋል። በአንድ ተጎጂ አማካይ ኪሳራ፦ $38,500። FBI IC3, 2025።",
    bars_header="ገንዘቡ በእውነት የት ይሄዳል",
    bars=[
        ("የኢንቨስትመንት ማጭበርበር (ክሪፕቶ፣ የሐሰት የንግድ መድረኮች)", "$3.52B"),
        ("'ገንዘብ መልስ' ማጭበርበር — ቀድሞ የተጭበረበሩትን እንደገና ማጭበርበር", "$540M"),
        ("የቴክኒክ ድጋፍ ማጭበርበር (FTC, 2024)", "$159M"),
        ("የልጅ ልጅ ማጭበርበር / በ AI የተቀዳ ድምፅ", "$5M+"),
    ],
    bars_footnote="የመስመሩ ርዝመት አንጻራዊ መጠንን ያሳያል፣ ከ~1% በታች በትክክለኛ መጠን አይደለም። FBI IC3 2025 መረጃ፤ ለቴክኒክ ድጋፍ FTC 2024-2025።",
    rising_header="በፍጥነት እያደገ ያለው",
    rising=[
        ("የማስመሰያ መልእክቶች እና ኢሜይሎች፣ ዕድሜ 60+", "ከ100% በላይ ጭማሪ"),
        ("የመንግስት አስመሳይ ጥሪዎች", "በእጥፍ ገደማ"),
        ("አዛውንቶችን ኢላማ ያደረገ የፍቅር ማጭበርበር", "በ30% ጭማሪ"),
        ("AI የድምፅ ግልባጭ የሚጠቀም ማጭበርበር", "3,100+ ቅሬታዎች፣ $352M+ ኪሳራ"),
    ],
    method_header="አብዛኛውን የሚያስቆም አንድ ልማድ",
    steps=[
        ("1", "ቁጥሩን በራስዎ ይፈልጉ።", "እነሱ የሰጡዎትን አይደለም።"),
        ("2", "ሰውዬውን በራስዎ ይደውሉ።", "መጀመሪያ ስልኩን ይዝጉ። እውነት ከሆነ፣ አሁንም እዚያ ይሆናሉ።"),
        ("3", "አንድ ቀን ይጠብቁ።", "እውነተኛ ችግሮች ሌሊቱን ያልፋሉ። ማጭበርበር ግን አያልፍም።"),
    ],
    footer_header="ነጻ እርዳታ — ያለ ፍርድ",
    hotline1_label="ብሔራዊ የአዛውንት ማጭበርበር ስልክ መስመር",
    hotline2_label="AARP Fraud Watch",
    report_line="በ ic3.gov እና reportfraud.ftc.gov ሪፖርት ያድርጉ  ·  ምንጮች፦ FBI IC3 2025 ሪፖርት፣ FTC Protecting Older Consumers 2024-2025",
)


def draw(lang):
    d = CONTENT[lang]
    FR, FB = fonts_for(lang)
    out = os.path.join(OUT_DIR, "infographic-%s.pdf" % lang)
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # header
    y = H - M
    c.setFillColor(ACCENT)
    c.setLineWidth(2)
    # magnifying glass + checkmark, matching the site logo:
    # "look it up yourself" (glass), "it checks out" (check)
    sx, sy, sr = M + 8, y - 20, 7
    c.setLineWidth(2.3)
    c.circle(sx, sy, sr, fill=0, stroke=1)
    p = c.beginPath()
    p.moveTo(sx - 2.5, sy + 0)
    p.lineTo(sx - 0.8, sy - 1.7)
    p.lineTo(sx + 2.3, sy + 2.2)
    c.drawPath(p, fill=0, stroke=1)
    c.line(sx + sr * 0.72, sy - sr * 0.72, sx + sr * 1.55, sy - sr * 1.55)
    c.setFont(FB, 22)
    c.setFillColor(INK)
    c.drawString(M + 28, y - 26, "TRUST BUT VERIFY")
    y -= 44
    c.setStrokeColor(INK)
    c.setLineWidth(3)
    c.line(M, y, W - M, y)
    y -= 8
    y = wrap(c, d["strap"], M, y - 10, FR, 10, W - 2 * M, 13, color=MUTED)
    y -= 20

    # headline stat
    # NOTE: the page's total content used to run past the bottom margin --
    # "FREE HELP" and everything below it landed at negative y and never
    # rendered. That bug predates the per-language content (it was already
    # true for the single, hardcoded English version). Fixed by trimming
    # gaps throughout, not just here -- see BACKLOG.md.
    c.setFont(FB, 46)
    c.setFillColor(ACCENT)
    y2 = wrap(c, d["headline"], M, y - 40, FB, 46, W - 2 * M, 46, color=ACCENT)
    y = y2 + 46 - 20
    y = wrap(c, d["headline_sub"], M, y, FB, 13, W - 2 * M, 16, color=INK)
    y -= 2
    y = wrap(c, d["headline_detail"], M, y, FR, 9, W - 2 * M, 12, color=MUTED)
    y -= 14

    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.line(M, y, W - M, y)
    y -= 16

    # bar chart
    c.setFont(FB, 13)
    c.setFillColor(INK)
    y = wrap(c, d["bars_header"], M, y, FB, 13, W - 2 * M, 16)
    y -= 5
    bw = W - 2 * M
    bh = 16
    fracs = [1.00, 0.153, 0.100, 0.0014]
    for (label, amount), frac in zip(d["bars"], fracs):
        bar(c, M, y - bh, bw, bh, frac, label, amount, FB)
        y -= bh + 22
    c.setFont(FR, 8)
    c.setFillColor(MUTED)
    y = wrap(c, d["bars_footnote"], M, y, FR, 8, W - 2 * M, 11, color=MUTED)
    y -= 6

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 16

    # what's rising
    c.setFont(FB, 13)
    c.setFillColor(INK)
    y = wrap(c, d["rising_header"], M, y, FB, 13, W - 2 * M, 16)
    y -= 5
    for label, stat in d["rising"]:
        c.setFont(FR, 10.5)
        c.setFillColor(INK)
        stat_w = stringWidth(stat, FB, 10.5) + 8
        yy = wrap(c, "•  " + label, M + 12, y, FR, 10.5, W - 2 * M - stat_w, 13)
        c.setFont(FB, 10.5)
        c.setFillColor(ACCENT)
        c.drawRightString(W - M, y, stat)
        y = min(yy, y - 14)
    y -= 4

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 16

    # the method
    c.setFont(FB, 13)
    c.setFillColor(INK)
    y = wrap(c, d["method_header"], M, y, FB, 13, W - 2 * M, 16)
    y -= 6
    # Reserve the bottom-right corner for the QR code (drawn later, at
    # roughly x=[508,570] y=[38,100]) -- see BACKLOG.md, this overlapped
    # step 3's text before the fix.
    qr_reserve = 90
    step_w = (W - 2 * M - 24 - qr_reserve) / 3
    step_y = y
    max_drop = 0
    for i, (num, head, sub) in enumerate(d["steps"]):
        x = M + i * (step_w + 12)
        c.setFont(FB, 26)
        c.setFillColor(ACCENT)
        c.drawString(x, step_y, num)
        c.setFont(FB, 10.5)
        c.setFillColor(INK)
        yy = wrap(c, head, x, step_y - 20, FB, 10.5, step_w, 13)
        yy = wrap(c, sub, x, yy - 2, FR, 8.5, step_w, 11, color=MUTED)
        max_drop = max(max_drop, step_y - yy)
    y = step_y - max_drop - 14

    c.setStrokeColor(INK)
    c.line(M, y, W - M, y)
    y -= 18

    # footer: hotlines + QR
    c.setFont(FB, 10)
    c.setFillColor(INK)
    y = wrap(c, d["footer_header"], M, y, FB, 10, W - 2 * M, 13)
    y -= 2
    c.setFont(FB, 13)
    c.drawString(M, y, "833-372-8311")
    c.setFont(FR, 8.5)
    c.setFillColor(MUTED)
    wrap(c, d["hotline1_label"], M + 92, y + 1, FR, 8.5, W - M - (M + 92), 11, color=MUTED)
    y -= 16
    c.setFont(FB, 13)
    c.setFillColor(INK)
    c.drawString(M, y, "877-908-3360")
    c.setFont(FR, 8.5)
    c.setFillColor(MUTED)
    c.drawString(M + 92, y + 1, d["hotline2_label"])
    y -= 16
    c.setFont(FR, 8.5)
    wrap(c, d["report_line"], M, y, FR, 8.5, W - 2 * M - 90, 11, color=MUTED)

    site_url = "https://trustbutverifyproject.org" if lang == "en" else \
        "https://trustbutverifyproject.org/%s/" % lang
    qr_path = qr_image(site_url, lang)
    qr_size = 62
    c.drawImage(qr_path, W - M - qr_size, M - 4, width=qr_size, height=qr_size,
                preserveAspectRatio=True, mask="auto")
    c.setFont("Arial", 7)
    c.setFillColor(MUTED)
    url_display = site_url.replace("https://", "")
    c.drawRightString(W - M, M - 12, url_display)

    c.showPage()
    c.save()
    os.remove(qr_path)
    print("wrote", out)


if __name__ == "__main__":
    for lang in CONTENT:
        draw(lang)
