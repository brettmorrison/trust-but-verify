#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The unvalidated-translation notice. One source of truth, print and web.

Every non-English page on this site was translated by a machine and read by
nobody. The sentence saying so is the most important sentence on the page,
because a reader who cannot check it has no other way to know.

It used to live in three places that could not see each other: a NOTICE dict
in build/make_fridge.py that went onto the printed fridge sheets in 23
languages, a hand-written blockquote at the top of 98 translated markdown
files, and a hand-written English paragraph at the foot of 40 landing pages.
The result was that 23 languages had a notice a reader could read on paper
and an English one on the web, and a language could gain a printed notice
without ever gaining a web one. This module is that single source: both
build/make_fridge.py and build/build_site.py read it, so a language can no
longer have one and not the other.

Each entry is (headline, body, english_line):

    headline      in the reader's language, the line that must be seen first
    body          in the reader's language, including how to help
    english_line  the same warning in English, shown underneath, so an
                  English-reading relative sitting with the reader sees it too

For the 21 languages with no translated notice yet, notice_for() builds an
English one carrying that language's own name from the switcher, so a reader
can at least tell the warning is about the page in front of them. That is
strictly better than today, where those readers get an English notice with no
language name at all, at 93% of the way down the page. It is not the finished
state: the finished state is a translated notice in all 45, added here as
each language's fridge sheet is regenerated.
"""
import html

# The 23 languages whose notice has been translated and is already printed on
# the fridge sheets handed to people. Moved here verbatim from
# build/make_fridge.py -- not retranslated, not reworded.
NOTICE = {
 "es": ("AVISO: TRADUCCIÓN SIN VALIDAR — NO IMPRIMIR AÚN",
        "Traducido por inteligencia artificial. Todavía no lo ha revisado un hablante nativo. ¿Habla español? Ayúdenos a corregirlo: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Spanish speakers: please help us check it."),
 "vi": ("LƯU Ý: BẢN DỊCH CHƯA KIỂM CHỨNG — XIN CHƯA IN",
        "Do trí tuệ nhân tạo dịch. Chưa được người bản ngữ duyệt lại. Quý vị nói tiếng Việt? Xin giúp chúng tôi: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Vietnamese speakers: please help us check it."),
 "zh": ("注意：翻译未经核校 —— 请暂勿打印",
        "由人工智能翻译，尚未经母语者审阅。您会说中文吗？请帮我们校对：translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Chinese speakers: please help us check it."),
 "ru": ("ВНИМАНИЕ: НЕПРОВЕРЕННЫЙ ПЕРЕВОД — ПОКА НЕ ПЕЧАТАЙТЕ",
        "Переведено искусственным интеллектом. Не проверено носителем языка. Говорите по-русски? Помогите нам: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Russian speakers: please help us check it."),
 "ko": ("주의: 검증되지 않은 기계 번역 — 아직 인쇄하지 마십시오",
        "AI가 번역했으며 원어민의 검토를 아직 받지 않았습니다. 한국어를 하시는 분, 검토를 도와주십시오: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Korean speakers: please help us check it."),
 "tl": ("PAUNAWA: HINDI PA NASUSURING AI TRANSLATION — HUWAG PA I-PRINT",
        "Isinalin ng AI at hindi pa nasusuri ng katutubong nagsasalita. Marunong ka ba? Tulungan mo kami: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Tagalog speakers: please help us check it."),
 "hi": ("सूचना: अप्रमाणित मशीनी अनुवाद — अभी प्रिंट न करें",
        "यह AI अनुवाद है, किसी मातृभाषी ने जाँचा नहीं है। हिंदी जानते हैं? मदद कीजिए: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Hindi speakers: please help us check it."),
 "bn": ("বিজ্ঞপ্তি: যাচাই-না-করা যান্ত্রিক অনুবাদ — এখনই ছাপবেন না",
        "এটি AI অনুবাদ, কোনো মাতৃভাষী দেখেননি। বাংলা জানেন? সাহায্য করুন: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Bengali speakers: please help us check it."),
 "hy": ("ՈՒՇԱԴՐՈՒԹՅՈՒՆ՝ չստուգված մեքենայական թարգմանություն — դեռ մի՛ տպեք",
        "Սա AI թարգմանություն է, կրող չի ստուգել։ Օգնե՛ք մեզ՝ translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Armenian speakers: please help us check it."),
 "am": ("ማስታወሻ፦ ያልተረጋገጠ የማሽን ትርጉም — ገና አያትሙ",
        "ይህ በAI የተተረጎመ ሲሆን በአፍ መፍቻ ተናጋሪ አልተመረመረም። ይርዱን፦ translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Amharic speakers: please help us check it."),
 "sq": ("NJOFTIM: PËRKTHIM AI I PAVERIFIKUAR — MOS E PRINTONI ENDE",
        "Përkthyer nga AI dhe i pashqyrtuar nga folës amtar. Na ndihmoni: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Albanian speakers: please help us check it."),
 "ja": ("注意：未検証の機械翻訳 — まだ印刷しないでください",
        "AIによる翻訳で、母語話者の確認をまだ受けていません。日本語を話せる方、確認にご協力ください： translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Japanese speakers: please help us check it."),
 "ar": ("تنبيه: ترجمة آلية غير مراجَعة — يُرجى عدم الطباعة بعد",
        "تُرجم هذا النص بالذكاء الاصطناعي ولم يراجعه ناطق بالعربية. هل تتحدث العربية؟ ساعدنا: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Arabic speakers: please help us check it."),
 "ur": ("اطلاع: غیر تصدیق شدہ مشینی ترجمہ — ابھی پرنٹ نہ کریں",
        "یہ مصنوعی ذہانت کا ترجمہ ہے، کسی مادری بولنے والے نے نہیں دیکھا۔ اردو جانتے ہیں؟ مدد کریں: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Urdu speakers: please help us check it."),
 "fa": ("توجه: ترجمه ماشینی راستی‌آزمایی‌نشده — فعلاً چاپ نکنید",
        "این متن با هوش مصنوعی ترجمه شده و هیچ فارسی‌زبانی آن را بازبینی نکرده است. کمک کنید: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Farsi speakers: please help us check it."),
 "ps": ("پام: ناتصدیق شوې ماشیني ژباړه — لا یې مه چاپوئ",
        "دا د AI ژباړه ده او کوم مورنۍ ژبې ویونکي نه ده کتلې. مرسته وکړئ: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Pashto speakers: please help us check it."),
 "de": ("HINWEIS: UNGEPRÜFTE ÜBERSETZUNG — NOCH NICHT DRUCKEN",
        "Von künstlicher Intelligenz übersetzt. Nicht muttersprachlich geprüft. Sprechen Sie Deutsch? Helfen Sie uns: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. German speakers: please help us check it."),
 "fr": ("AVIS : TRADUCTION NON VALIDÉE — NE PAS IMPRIMER",
        "Traduit par intelligence artificielle. Non relu par un locuteur natif. Vous parlez français ? Aidez-nous : translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. French speakers: please help us check it."),
 "pt": ("AVISO: TRADUÇÃO NÃO VALIDADA — NÃO IMPRIMIR AINDA",
        "Traduzido por inteligência artificial. Não revisado por falante nativo. Você fala português? Ajude-nos: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Portuguese speakers: please help us check it."),
 "pl": ("UWAGA: TŁUMACZENIE NIEZWERYFIKOWANE — NIE DRUKUJ",
        "Przetłumaczone przez sztuczną inteligencję. Niesprawdzone przez native speakera. Mówisz po polsku? Pomóż nam: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Polish speakers: please help us check it."),
 "ro": ("ATENȚIE: TRADUCERE NEVERIFICATĂ — NU TIPĂRIȚI ÎNCĂ",
        "Tradus de inteligență artificială. Neverificat de un vorbitor nativ. Vorbiți românește? Ajutați-ne: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Romanian speakers: please help us check it."),
 "uk": ("УВАГА: НЕПЕРЕВІРЕНИЙ ПЕРЕКЛАД — ПОКИ НЕ ДРУКУЙТЕ",
        "Перекладено штучним інтелектом. Не перевірено носієм мови. Розмовляєте українською? Допоможіть нам: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Ukrainian speakers: please help us check it."),
 "id": ("PERHATIAN: TERJEMAHAN BELUM DIPERIKSA — JANGAN DICETAK DULU",
        "Diterjemahkan oleh kecerdasan buatan. Belum diperiksa penutur asli. Anda berbahasa Indonesia? Bantu kami: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Indonesian speakers: please help us check it."),
}


# Every language the site is published in, with its English name. Used to say
# "Khmer speakers: ..." in the fallback notice and to keep this module's own
# coverage check honest.
ENGLISH_NAME = {
    "en": "English",
    "es": "Spanish",
    "vi": "Vietnamese",
    "zh": "Chinese",
    "ru": "Russian",
    "ko": "Korean",
    "tl": "Tagalog",
    "hi": "Hindi",
    "bn": "Bengali",
    "hy": "Armenian",
    "am": "Amharic",
    "sq": "Albanian",
    "ja": "Japanese",
    "ar": "Arabic",
    "ur": "Urdu",
    "fa": "Farsi",
    "ps": "Pashto",
    "de": "German",
    "fr": "French",
    "pt": "Portuguese",
    "pl": "Polish",
    "ro": "Romanian",
    "uk": "Ukrainian",
    "id": "Indonesian",
    "ht": "Haitian Creole",
    "pa": "Punjabi",
    "gu": "Gujarati",
    "so": "Somali",
    "km": "Khmer",
    "hmn": "Hmong",
    "ka": "Georgian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "et": "Estonian",
    "it": "Italian",
    "el": "Greek",
    "he": "Hebrew",
    "hu": "Hungarian",
    "hr": "Croatian",
    "sr": "Serbian",
    "ms": "Malay",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "sw": "Swahili",
}


def notice_for(lang):
    """(headline, body, english_line, translated) for one language.

    Everything here is plain text. `english_line` is empty for a language
    with no translated notice, because in that case the headline and body
    are already the English ones and repeating them helps nobody.
    """
    if lang in NOTICE:
        head, body, english = NOTICE[lang]
        return head, body, english, True

    name = ENGLISH_NAME.get(lang, lang)
    head = "NOTICE: unvalidated AI translation"
    body = ("Translated by AI. No native speaker has checked this page yet. "
            "Please do not print or distribute it. %s speakers: one or two "
            "hours of your time would fix that, and we would be grateful. "
            "Write to translations@trustbutverifyproject.org" % name)
    return head, body, "", False


def notice_html(lang, language_name):
    """The block the web build puts immediately under the <h1>.

    `language_name` is the language's own name as the site's switcher shows
    it -- Khmer arrives as the Khmer word for Khmer. For a language with no
    translated notice it is shown beside the English headline, marked up in
    that language, so a reader can see the warning is about the page in
    front of them even when they cannot read the sentence.

    The lang attributes are per paragraph rather than on the block, because
    a screen reader should not read an English sentence in a Khmer voice or
    a Korean one in an English voice. That is the whole audience for this
    notice: people reading in a language the page was not written in.
    """
    head, body, english, translated = notice_for(lang)
    tag = lang if translated else "en"
    out = ['<aside class="notice" data-notice="unvalidated" role="note">']
    if translated:
        out.append('<p class="notice-head" lang="%s"><strong>%s</strong></p>'
                   % (tag, html.escape(head)))
    else:
        out.append('<p class="notice-head" lang="en"><strong>%s (<span lang="%s">%s</span>)'
                   '</strong></p>' % (html.escape(head), lang, html.escape(language_name)))
    out.append('<p lang="%s">%s</p>' % (tag, html.escape(body)))
    if english:
        out.append('<p class="notice-en" lang="en" dir="ltr">%s</p>' % html.escape(english))
    out.append("</aside>")
    return "".join(out)

