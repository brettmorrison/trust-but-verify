#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a landing page for every language that has a printed sheet but no full
translation yet. Content is pulled straight from make_fridge.py so the web page
and the printed sheet can never drift apart.

    python3 build/make_lang_pages.py
"""
import io, os, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "mf", os.path.join(ROOT, "build", "make_fridge.py"))
mf = importlib.util.module_from_spec(spec)
mf.__name__ = "mf_import_only"
src = io.open(spec.origin, encoding="utf-8").read()
src = src.split("# --- template ---")[0]          # data only, don't rebuild PDFs
exec(compile(src, spec.origin, "exec"), mf.__dict__)
L = mf.L
NOTICE = {}
for line in io.open(spec.origin, encoding="utf-8").read().splitlines():
    pass

# languages that already have a full hand-written translation
FULL = {"en", "es", "vi", "ru", "zh"}

# native-language labels + the strings this page needs beyond the sheet data
EXTRA = {
 "ja": dict(name="日本語", sheet="印刷用の1ページ資料（PDF）",
   nofull="このサイトの全ページはまだ日本語になっていません。下の1ページ資料には、"
          "最も大切なことがすべて入っています。",
   helphead="お手伝いいただけませんか",
   helpbody="この翻訳はAIによるもので、母語話者の確認をまだ受けていません。"
            "1〜2時間で結構です。不自然な言い回しや、見下した響きのある箇所を"
            "教えてください。",
   full="英語の全ページ"),
 "ko": dict(name="한국어", sheet="인쇄용 한 장 자료 (PDF)",
   nofull="이 사이트의 모든 페이지가 아직 한국어로 번역되지는 않았습니다. "
          "아래 한 장짜리 자료에 가장 중요한 내용이 모두 담겨 있습니다.",
   helphead="도와주시겠습니까",
   helpbody="이 번역은 AI가 한 것이며 원어민의 검토를 아직 받지 않았습니다. "
            "한두 시간이면 됩니다. 어색한 표현이나 무시하는 듯한 어조가 있으면 "
            "알려주십시오.",
   full="영어 전체 페이지"),
 "tl": dict(name="Tagalog", sheet="Isang pahinang babasahin (PDF)",
   nofull="Hindi pa naisasalin sa Tagalog ang lahat ng pahina ng site na ito. "
          "Nasa isang pahinang babasahin sa ibaba ang pinakamahalagang bahagi.",
   helphead="Matutulungan mo ba kami",
   helpbody="AI ang nagsalin nito at hindi pa ito nasusuri ng katutubong "
            "nagsasalita. Isa o dalawang oras lang. Sabihin mo lang kung alin ang "
            "hindi natural o parang minamaliit ang bumabasa.",
   full="Buong pahina sa Ingles"),
 "hi": dict(name="हिन्दी", sheet="छापने योग्य एक पन्ने की शीट (PDF)",
   nofull="इस साइट के सभी पन्ने अभी हिंदी में नहीं हैं। नीचे दी गई एक पन्ने की "
          "शीट में सबसे ज़रूरी बातें हैं।",
   helphead="क्या आप हमारी मदद करेंगे",
   helpbody="यह अनुवाद AI ने किया है और किसी मातृभाषी ने इसे जाँचा नहीं है। "
            "एक-दो घंटे चाहिए। बस बताइए कि कौन-सी बात अटपटी लगती है और कहाँ "
            "पढ़ने वाले को कमतर समझा जा रहा है।",
   full="अंग्रेज़ी में पूरे पन्ने"),
 "bn": dict(name="বাংলা", sheet="ছাপার উপযোগী এক পাতার শিট (PDF)",
   nofull="এই সাইটের সব পাতা এখনো বাংলায় হয়নি। নিচের এক পাতার শিটে সবচেয়ে "
          "জরুরি কথাগুলো আছে।",
   helphead="আপনি কি আমাদের সাহায্য করবেন",
   helpbody="এই অনুবাদ AI করেছে, কোনো মাতৃভাষী দেখেননি। এক-দুই ঘণ্টা লাগবে। "
            "শুধু বলুন কোন বাক্য কানে লাগে আর কোথায় পাঠককে ছোট করা হচ্ছে বলে "
            "মনে হয়।",
   full="ইংরেজিতে সম্পূর্ণ পাতা"),
 "hy": dict(name="Հայերեն", sheet="Տպելու համար մեկ էջ (PDF)",
   nofull="Այս կայքի բոլոր էջերը դեռ հայերեն չեն։ Ներքևի մեկ էջում ամենակարևորն է։",
   helphead="Կօգնե՞ք մեզ",
   helpbody="Այս թարգմանությունը կատարել է արհեստական բանականությունը, և կրողը "
            "դեռ չի ստուգել։ Մեկ-երկու ժամ է պետք։ Ասեք, թե որ նախադասությունն է "
            "անբնական հնչում և որտեղ է ընթերցողին վերևից նայում։",
   full="Ամբողջական էջերը անգլերեն"),
 "am": dict(name="አማርኛ", sheet="የሚታተም አንድ ገጽ (PDF)",
   nofull="የዚህ ድረ-ገጽ ሁሉም ገጾች ገና በአማርኛ አልተዘጋጁም። ከታች ባለው አንድ ገጽ ላይ በጣም "
          "አስፈላጊው ነገር ሁሉ አለ።",
   helphead="ሊረዱን ይችላሉ",
   helpbody="ይህ ትርጉም በAI የተሰራ ሲሆን በአፍ መፍቻ ተናጋሪ ገና አልተመረመረም። አንድ ወይም ሁለት "
            "ሰዓት ይበቃል። የትኛው ዓረፍተ ነገር እንደማይሰማ እና የት አንባቢውን እንደሚያሳንስ ይንገሩን።",
   full="ሙሉ ገጾች በእንግሊዝኛ"),
 "sq": dict(name="Shqip", sheet="Fletë një-faqesh për printim (PDF)",
   nofull="Jo të gjitha faqet e kësaj faqeje interneti janë ende në shqip. "
          "Fleta një-faqesh më poshtë përmban gjithçka më të rëndësishme.",
   helphead="A mund të na ndihmoni",
   helpbody="Ky përkthim është bërë nga AI dhe nuk është shqyrtuar ende nga një "
            "folës amtar. Mjaftojnë një ose dy orë. Na tregoni cila fjali tingëllon "
            "e panatyrshme dhe ku lexuesi trajtohet me epërsi.",
   full="Faqet e plota në anglisht"),
 "ar": dict(name="العربية", sheet="صفحة واحدة للطباعة (PDF)",
   nofull="لم تُترجم كل صفحات هذا الموقع إلى العربية بعد. الصفحة الواحدة أدناه "
          "تحتوي على أهم ما يلزم.",
   helphead="هل يمكنك مساعدتنا",
   helpbody="تُرجم هذا النص بالذكاء الاصطناعي ولم يراجعه ناطق بالعربية بعد. "
            "ساعة أو ساعتان تكفيان. أخبرنا أي جملة تبدو غير طبيعية وأين يبدو "
            "النص متعاليًا على القارئ.",
   full="الصفحات الكاملة بالإنجليزية"),
 "ur": dict(name="اردو", sheet="پرنٹ کرنے کے لیے ایک صفحہ (PDF)",
   nofull="اس سائٹ کے تمام صفحات ابھی اردو میں نہیں ہیں۔ نیچے دیے گئے ایک صفحے "
          "میں سب سے ضروری باتیں موجود ہیں۔",
   helphead="کیا آپ ہماری مدد کریں گے",
   helpbody="یہ ترجمہ مصنوعی ذہانت نے کیا ہے اور کسی مادری بولنے والے نے اسے "
            "نہیں دیکھا۔ ایک دو گھنٹے کافی ہیں۔ بس بتائیں کون سا جملہ اجنبی لگتا "
            "ہے اور کہاں قاری کو کمتر سمجھا جا رہا ہے۔",
   full="انگریزی میں مکمل صفحات"),
 "fa": dict(name="فارسی", sheet="یک صفحه برای چاپ (PDF)",
   nofull="همه صفحات این سایت هنوز به فارسی نیست. صفحه زیر مهم‌ترین نکات را دارد.",
   helphead="می‌توانید کمک کنید",
   helpbody="این متن با هوش مصنوعی ترجمه شده و هنوز هیچ فارسی‌زبانی آن را بازبینی "
            "نکرده است. یکی دو ساعت کافی است. بگویید کدام جمله غیرطبیعی است و کجا "
            "لحن از بالا به پایین است.",
   full="صفحات کامل به انگلیسی"),
 "ps": dict(name="پښتو", sheet="د چاپ لپاره یوه پاڼه (PDF)",
   nofull="د دې ویب پاڼې ټولې برخې لا په پښتو نه دي. لاندې یوه پاڼه کې ترټولو "
          "مهم شیان شته.",
   helphead="راسره مرسته کولی شئ",
   helpbody="دا ژباړه د مصنوعي ځیرکتیا په واسطه شوې او لا یې کوم مورنۍ ژبې "
            "ویونکي نه ده کتلې. یو دوه ساعته بس دي. راته ووایاست کومه جمله "
            "ناسمه ښکاري او چیرته لوستونکی سپک ګڼل کیږي.",
   full="په انګلیسي کې بشپړې پاڼې"),
}

OUTDIR = os.path.join(ROOT, "content")
CONTACT = "translations@trustbutverifyproject.org"

written = 0
for code, d in L.items():
    if code in FULL or code not in EXTRA:
        continue
    e = EXTRA[code]
    lines = []
    lines.append("---")
    lines.append("title: %s" % d["brand"])
    lines.append("slug: /%s/" % code)
    lines.append("description: %s" % d["tagline"])
    lines.append("lang: %s" % code)
    lines.append("status: UNVALIDATED AI TRANSLATION — not reviewed by a native "
                 "speaker; do not print or distribute")
    lines.append("validated_by: (none yet)")
    lines.append("---")
    lines.append("")
    lines.append("# %s" % d["brand"])
    lines.append("")
    lines.append("**%s**" % d["tagline"])
    lines.append("")
    lines.append("> %s" % d["interp"] if d.get("interp") else "")
    lines.append("")
    lines.append("## %s" % d["steps_head"])
    lines.append("")
    for i, (imp, sub) in enumerate(d["steps"], 1):
        lines.append("**%d. %s**" % (i, imp))
        lines.append("")
        lines.append(sub)
        lines.append("")
    lines.append("## %s" % d["signs_head"])
    lines.append("")
    for sgn in d["signs"]:
        lines.append("- %s" % sgn)
    lines.append("")
    lines.append("## %s" % d["never_head"])
    lines.append("")
    for nv in d["never"]:
        lines.append("- **%s**" % nv)
    lines.append("")
    lines.append("## %s" % d["help_head"])
    lines.append("")
    for tel, who in d["helps"]:
        lines.append("**%s** — %s" % (tel, who))
        lines.append("")
    if d.get("interp"):
        lines.append("%s" % d["interp"])
        lines.append("")
    lines.append(d["report"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## %s" % e["sheet"])
    lines.append("")
    lines.append(e["nofull"])
    lines.append("")
    lines.append("**[%s](/print/fridge-sheet-%s.pdf)**" % (e["sheet"], code))
    lines.append("")
    lines.append("[%s](/)" % e["full"])
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## %s" % e["helphead"])
    lines.append("")
    lines.append(e["helpbody"])
    lines.append("")
    lines.append("**%s**" % CONTACT)
    lines.append("")
    lines.append("*NOTICE — unvalidated AI translation, not reviewed by a native "
                 "speaker. Please do not print or distribute this yet. "
                 "%s speakers: we need one reader. It takes an hour.*" % e["name"])
    lines.append("")
    lines.append("**%s**" % d["footline"])
    lines.append("")

    path = os.path.join(OUTDIR, code)
    os.makedirs(path, exist_ok=True)
    fn = os.path.join(path, "index.md")
    io.open(fn, "w", encoding="utf-8").write("\n".join(lines))
    written += 1
    print("wrote", fn)

print("total:", written)
