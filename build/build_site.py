#!/usr/bin/env python3
"""
Trust But Verify — static site generator.

    python3 build/build_site.py

Reads content/**/*.md, writes site/. No build tooling, no framework,
no JavaScript, no cookies. Cloudflare's cookie-free Web Analytics is the only
thing that counts anything, and it only counts anonymous pageviews.
Upload site/ to Cloudflare Pages.
"""
import os, re, shutil, html, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
PRINT = os.path.join(ROOT, "formats", "print")
OUT = os.path.join(ROOT, "site")

SITE = "https://trustbutverifyproject.org"
CONTACT = "translations@trustbutverifyproject.org"

RTL = {"ar", "ur", "fa", "ps", "he"}

LANGS = [
    ("en", "English",    "English"),
    ("es", "es",         "Español"),
    ("vi", "vi",         "Tiếng Việt"),
    ("zh", "zh",         "中文"),
    ("ru", "ru",         "Русский"),
    ("ko", "ko",         "한국어"),
    ("tl", "tl",         "Tagalog"),
    ("hi", "hi",         "हिन्दी"),
    ("bn", "bn",         "বাংলা"),
    ("hy", "hy",         "Հայերեն"),
    ("am", "am",         "አማርኛ"),
    ("sq", "sq",         "Shqip"),
    ("ja", "ja",         "日本語"),
    ("ar", "ar",         "العربية"),
    ("ur", "ur",         "اردو"),
    ("fa", "fa",         "فارسی"),
    ("ps", "ps",         "پښتو"),
    ("de", "de",         "Deutsch"),
    ("fr", "fr",         "Français"),
    ("pt", "pt",         "Português"),
    ("pl", "pl",         "Polski"),
    ("ro", "ro",         "Română"),
    ("uk", "uk",         "Українська"),
    ("id", "id",         "Bahasa Indonesia"),
]


# Per-language interface strings. Falls back to English for anything missing.
UI = {
 "en": dict(strap="Hang up. Look up the number yourself. Wait a day.",
   back="\u2190 Back to the start", read="Read this in:",
   help="Free help, no judgment.", nocookie="This site sets no cookies and collects no personal data — Cloudflare counts anonymous pageviews only.",
   free="Free to print, copy, translate, and hand to a neighbour. No permission needed.",
   langpage="Help in your language", skip="Skip to the main content",
   navhome="Home", navscams="Scam types", navprint="Print materials",
   navabout="About", navtalk="Give this talk", navhelp="Help translate",
   railtitle="Find your way", s_romance="Someone I met online",
   s_tech="Fake tech support", s_bank="Bank / “phantom hacker”",
   s_gov="Government impersonation", s_grandparent="Grandchild in trouble",
   s_kidnap="Virtual kidnapping", s_signs="Three warning signs"),
 "es": dict(strap="Cuelgue. Busque el n\u00famero usted mismo. Espere un d\u00eda.",
   back="\u2190 Volver al inicio", read="Leer esto en:", help="Ayuda gratuita, sin juicios.",
   nocookie="Este sitio no usa cookies ni recopila datos personales \u2014 Cloudflare solo cuenta visitas an\u00f3nimas a la p\u00e1gina.",
   free="Libre de imprimir, copiar, traducir y compartir. No hace falta permiso.",
   langpage="Ayuda en su idioma", skip="Ir al contenido principal"),
 "vi": dict(strap="C\u00fap m\u00e1y. T\u1ef1 m\u00ecnh tra s\u1ed1. Ch\u1edd m\u1ed9t ng\u00e0y.",
   back="\u2190 V\u1ec1 trang \u0111\u1ea7u", read="\u0110\u1ecdc b\u1eb1ng:", help="Tr\u1ee3 gi\u00fap mi\u1ec5n ph\u00ed, kh\u00f4ng ph\u00e1n x\u00e9t.",
   nocookie="Trang n\u00e0y kh\u00f4ng d\u00f9ng cookie v\u00e0 kh\u00f4ng thu th\u1eadp d\u1eef li\u1ec7u c\u00e1 nh\u00e2n \u2014 Cloudflare ch\u1ec9 \u0111\u1ebfm l\u01b0\u1ee3t xem trang \u1ea9n danh.",
   free="T\u1ef1 do in, sao ch\u00e9p, d\u1ecbch v\u00e0 chia s\u1ebb. Kh\u00f4ng c\u1ea7n xin ph\u00e9p.",
   langpage="Tr\u1ee3 gi\u00fap b\u1eb1ng ng\u00f4n ng\u1eef c\u1ee7a qu\u00fd v\u1ecb", skip="\u0110\u1ebfn n\u1ed9i dung ch\u00ednh"),
 "zh": dict(strap="\u6302\u65ad\u3002\u81ea\u5df1\u67e5\u53f7\u7801\u3002\u7b49\u4e00\u5929\u3002",
   back="\u2190 \u56de\u5230\u9996\u9875", read="\u5176\u4ed6\u8bed\u8a00\uff1a", help="\u514d\u8d39\u6c42\u52a9\uff0c\u4e0d\u4f1a\u6709\u4eba\u8bc4\u5224\u60a8\u3002",
   nocookie="\u672c\u7ad9\u4e0d\u4f7f\u7528 Cookie\uff0c\u4e5f\u4e0d\u6536\u96c6\u60a8\u7684\u4e2a\u4eba\u4fe1\u606f\u2014\u2014Cloudflare \u53ea\u7edf\u8ba1\u533f\u540d\u7684\u9875\u9762\u8bbf\u95ee\u91cf\u3002",
   free="\u6b22\u8fce\u81ea\u7531\u6253\u5370\u3001\u590d\u5236\u3001\u7ffb\u8bd1\u548c\u5206\u4eab\u3002\u65e0\u9700\u6388\u6743\u3002",
   langpage="\u7528\u60a8\u7684\u8bed\u8a00\u6c42\u52a9", skip="\u8df3\u5230\u4e3b\u8981\u5185\u5bb9"),
 "ru": dict(strap="\u041f\u043e\u043b\u043e\u0436\u0438\u0442\u0435 \u0442\u0440\u0443\u0431\u043a\u0443. \u041d\u0430\u0439\u0434\u0438\u0442\u0435 \u043d\u043e\u043c\u0435\u0440 \u0441\u0430\u043c\u0438. \u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435 \u0441\u0443\u0442\u043a\u0438.",
   back="\u2190 \u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e", read="\u0427\u0438\u0442\u0430\u0442\u044c \u043d\u0430:", help="\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u0430\u044f \u043f\u043e\u043c\u043e\u0449\u044c, \u0431\u0435\u0437 \u043e\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u044f.",
   nocookie="\u042d\u0442\u043e\u0442 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 cookie \u0438 \u043d\u0435 \u0441\u043e\u0431\u0438\u0440\u0430\u0435\u0442 \u043b\u0438\u0447\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u2014 Cloudflare \u043f\u043e\u0434\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u043d\u043e\u043d\u0438\u043c\u043d\u044b\u0435 \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u044b \u0441\u0442\u0440\u0430\u043d\u0438\u0446.",
   free="\u041c\u043e\u0436\u043d\u043e \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e \u043f\u0435\u0447\u0430\u0442\u0430\u0442\u044c, \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0438 \u0440\u0430\u0441\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u044f\u0442\u044c. \u0420\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0435 \u043d\u0435 \u043d\u0443\u0436\u043d\u043e.",
   langpage="\u041f\u043e\u043c\u043e\u0449\u044c \u043d\u0430 \u0432\u0430\u0448\u0435\u043c \u044f\u0437\u044b\u043a\u0435", skip="\u041a \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u043c\u0443 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044e"),
}


UI["ko"] = dict(strap="전화를 끊으십시오. 번호를 직접 찾으십시오. 하루 기다리십시오.",
  back="← 처음으로", read="다른 언어로 읽기:", help="무료 도움, 나무라지 않습니다.",
  nocookie="이 사이트는 쿠키를 쓰지 않고 개인정보를 수집하지 않습니다 — Cloudflare는 익명 페이지뷰만 집계합니다.",
  free="자유롭게 인쇄, 복사, 번역, 공유하십시오. 허락은 필요 없습니다.",
  langpage="당신의 언어로 도움받기", skip="본문으로 건너뛰기")
UI["ja"] = dict(strap="電話を切る。番号は自分で調べる。一日待つ。",
  back="← 最初に戻る", read="他の言語で読む：", help="無料の相談。責めません。",
  nocookie="このサイトはクッキーを使わず、個人情報も収集しません。Cloudflareは匿名のページビューのみを集計します。",
  free="自由に印刷・複製・翻訳・共有してください。許可は不要です。",
  langpage="あなたの言語での相談先", skip="本文へ移動")
UI["hi"] = dict(strap="फ़ोन काटें। नंबर खुद ढूँढें। एक दिन रुकें।",
  back="← शुरुआत पर वापस", read="इन भाषाओं में पढ़ें:", help="मुफ़्त मदद, कोई ताना नहीं।",
  nocookie="यह साइट कुकी नहीं रखती और कोई व्यक्तिगत जानकारी नहीं जुटाती — Cloudflare केवल गुमनाम पेजव्यू गिनता है।",
  free="बेझिझक छापें, कॉपी करें, अनुवाद करें और बाँटें। अनुमति की ज़रूरत नहीं।",
  langpage="अपनी भाषा में मदद", skip="मुख्य सामग्री पर जाएँ")
UI["bn"] = dict(strap="ফোন রাখুন। নম্বর নিজে খুঁজুন। একদিন অপেক্ষা করুন।",
  back="← শুরুতে ফিরুন", read="অন্য ভাষায় পড়ুন:", help="বিনামূল্যে সহায়তা, কোনো দোষারোপ নেই।",
  nocookie="এই সাইট কুকি রাখে না এবং কোনো ব্যক্তিগত তথ্য সংগ্রহ করে না — Cloudflare শুধু বেনামী পেজভিউ গণনা করে।",
  free="স্বাধীনভাবে ছাপুন, কপি করুন, অনুবাদ করুন ও ভাগ করুন। অনুমতি লাগবে না।",
  langpage="আপনার ভাষায় সহায়তা", skip="মূল অংশে যান")
UI["tl"] = dict(strap="Ibaba ang telepono. Hanapin mo mismo ang numero. Maghintay ng isang araw.",
  back="← Balik sa simula", read="Basahin ito sa:", help="Libreng tulong, walang husga.",
  nocookie="Walang cookies ang site na ito at walang kinokolektang personal na impormasyon — binibilang lang ng Cloudflare ang anonymous na pageviews.",
  free="Malayang i-print, kopyahin, isalin, at ipamahagi. Hindi kailangan ng pahintulot.",
  langpage="Tulong sa iyong wika", skip="Tumalon sa pangunahing nilalaman")
UI["hy"] = dict(strap="Անջատեք։ Համարը ինքներդ գտեք։ Սպասեք մեկ օր։",
  back="← Վերադառնալ սկիզբ", read="Կարդալ նաև՝", help="Անվճար օգնություն, առանց դատելու։",
  nocookie="Այս կայքը cookie չի օգտագործում և ձեր անձնական տվյալները չի հավաքում։ Cloudflare-ը հաշվում է միայն անանուն դիտումների քանակը։",
  free="Ազատորեն տպեք, պատճենեք, թարգմանեք և տարածեք։ Թույլտվություն պետք չէ։",
  langpage="Օգնություն ձեր լեզվով", skip="Անցնել հիմնական բովանդակությանը")
UI["am"] = dict(strap="ስልኩን ይዝጉ። ቁጥሩን ራስዎ ይፈልጉ። አንድ ቀን ይጠብቁ።",
  back="← ወደ መጀመሪያው ተመለስ", read="በሌላ ቋንቋ ያንብቡ፦", help="ነጻ እርዳታ፣ ማንም አይወቅስዎትም።",
  nocookie="ይህ ድረ-ገጽ ኩኪ አይጠቀምም እና የግል መረጃዎን አይሰበስብም — Cloudflare ስም-አልባ የገጽ ጉብኝት ብዛት ብቻ ይቆጥራል።",
  free="በነጻነት ያትሙ፣ ይቅዱ፣ ይተርጉሙ እና ያካፍሉ። ፈቃድ አያስፈልግም።",
  langpage="በቋንቋዎ እርዳታ", skip="ወደ ዋናው ይዘት ዝለል")
UI["sq"] = dict(strap="Mbylleni telefonin. Gjejeni vetë numrin. Prisni një ditë.",
  back="← Kthehu në fillim", read="Lexoni këtë në:", help="Ndihmë falas, pa gjykim.",
  nocookie="Kjo faqe nuk përdor cookies dhe nuk mbledh të dhëna personale — Cloudflare numëron vetëm shikime anonime të faqes.",
  free="I lirë për ta printuar, kopjuar, përkthyer dhe shpërndarë. Pa leje.",
  langpage="Ndihmë në gjuhën tuaj", skip="Kalo te përmbajtja kryesore")
UI["ar"] = dict(strap="أغلق الخط. ابحث عن الرقم بنفسك. انتظر يومًا.",
  back="← العودة إلى البداية", read="اقرأ هذا بلغة أخرى:", help="مساعدة مجانية، بلا أحكام.",
  nocookie="هذا الموقع لا يستخدم ملفات تعريف الارتباط ولا يجمع أي بيانات شخصية — تحسب Cloudflare فقط عدد الزيارات المجهولة للصفحة.",
  free="يمكنك الطباعة والنسخ والترجمة والمشاركة بحرية. لا حاجة لإذن.",
  langpage="مساعدة بلغتك", skip="انتقل إلى المحتوى الرئيسي")
UI["ur"] = dict(strap="فون بند کریں۔ نمبر خود تلاش کریں۔ ایک دن انتظار کریں۔",
  back="← شروع پر واپس", read="اسے اس زبان میں پڑھیں:", help="مفت مدد، کوئی ملامت نہیں۔",
  nocookie="یہ سائٹ کوکیز استعمال نہیں کرتی اور کوئی ذاتی معلومات جمع نہیں کرتی — Cloudflare صرف گمنام پیج ویوز شمار کرتا ہے۔",
  free="آزادانہ چھاپیں، نقل کریں، ترجمہ کریں اور تقسیم کریں۔ اجازت کی ضرورت نہیں۔",
  langpage="اپنی زبان میں مدد", skip="مرکزی مواد پر جائیں")
UI["fa"] = dict(strap="تلفن را قطع کنید. شماره را خودتان پیدا کنید. یک روز صبر کنید.",
  back="← بازگشت به آغاز", read="این را به زبان دیگر بخوانید:", help="کمک رایگان، بدون سرزنش.",
  nocookie="این سایت از کوکی استفاده نمی‌کند و هیچ اطلاعات شخصی جمع نمی‌کند — Cloudflare فقط بازدیدهای ناشناس صفحه را می‌شمارد.",
  free="آزادانه چاپ، کپی، ترجمه و منتشر کنید. نیازی به اجازه نیست.",
  langpage="کمک به زبان شما", skip="رفتن به محتوای اصلی")
UI["ps"] = dict(strap="ټیلیفون بند کړئ. شمېره پخپله ولټوئ. یوه ورځ صبر وکړئ.",
  back="← بېرته پیل ته", read="دا په بله ژبه ولولئ:", help="وړیا مرسته، هېڅ ملامتیا نشته.",
  nocookie="دا ویب پاڼه کوکیز نه کاروي او ستاسو شخصي معلومات نه راټولوي — Cloudflare یوازې ناپیژندل شوي د پاڼې لیدنې شمېري.",
  free="په آزادۍ سره یې چاپ، کاپي، ژباړه او شریکول کولی شئ. اجازې ته اړتیا نشته.",
  langpage="ستاسو په ژبه مرسته", skip="اصلي منځپانګې ته ورشئ")

# ---------------------------------------------------------------- front matter

def split_front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            raw = text[3:end].strip()
            body = text[end + 4:].lstrip("\n")
            for line in raw.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            return meta, body
    return meta, text


def slug_to_path(slug):
    """/questions/foo -> questions/foo/index.html ; / -> index.html"""
    s = (slug or "/").strip("/")
    return "index.html" if not s else os.path.join(s, "index.html")


def depth_prefix(outpath):
    d = outpath.count(os.sep)
    return "../" * d if d else "./"

# ---------------------------------------------------------------------- layout

MARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M12 2.5 19.5 5.5V11C19.5 16 16 19.8 12 21.5 '
        '8 19.8 4.5 16 4.5 11V5.5Z"/><path d="M8.2 11.6 10.8 14.2 15.8 9"/></svg>')

CSS = """
:root{
  --ink:#111;--paper:#fffdf9;--rule:#111;--muted:#4a4a4a;
  --accent:#123f7a;--band:#f0ece4;
  --measure:34rem;
}
*{box-sizing:border-box;margin:0;padding:0}
html{font-size:125%;-webkit-text-size-adjust:100%}
html,body{max-width:100%}
body{
  background:var(--paper);color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  font-size:1.05rem;line-height:1.6;
  padding:0 1.25rem 4rem;
}
.skip{position:absolute;left:-9999px}
.skip:focus{position:static;display:inline-block;padding:.6rem;background:#ff0;color:#000}
a{color:var(--accent);text-underline-offset:3px}
a:focus-visible,button:focus-visible{outline:4px solid #0b57d0;outline-offset:2px}

.shell{max-width:var(--measure);margin:0 auto;overflow-wrap:break-word;word-break:break-word}

header.site{border-bottom:5px solid var(--rule);padding:1.1rem 0 .9rem;margin-bottom:1.6rem}
header.site .top{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:.6rem}
header.site a.brand{
  display:inline-flex;align-items:center;gap:.5rem;
  font-weight:800;font-size:1.15rem;letter-spacing:.06em;
  text-transform:uppercase;color:var(--ink);text-decoration:none;line-height:1.2}
header.site a.brand svg{flex:none;width:1.7rem;height:1.7rem;color:var(--accent)}
header.site p.strap{font-size:.95rem;color:var(--muted);margin-top:.55rem}

nav.sitenav{display:flex;flex-wrap:wrap;gap:1.1rem 1.4rem;margin-top:.85rem;
  font-size:1rem;font-weight:700}
nav.sitenav a{text-decoration:none;color:var(--ink)}
nav.sitenav a:hover{color:var(--accent)}

details.langswitch{position:relative}
details.langswitch summary{list-style:none;cursor:pointer;font-weight:700;
  font-size:.95rem;padding:.5rem .8rem;border:2px solid var(--rule);
  border-radius:.3rem;white-space:nowrap;user-select:none}
details.langswitch summary::-webkit-details-marker{display:none}
details.langswitch summary::after{content:" \\25be";font-weight:400}
details.langswitch[open] summary::after{content:" \\25b4"}
details.langswitch .panel{margin-top:.6rem;background:var(--band);
  border:2px solid var(--rule);border-radius:.4rem;padding:.9rem 1rem}
details.langswitch .panel a,details.langswitch .panel strong{display:block;
  padding:.32rem 0;font-size:.98rem}
@media (min-width:32rem){
  details.langswitch .panel{columns:2;column-gap:1.4rem}
}

h1{font-size:2.1rem;line-height:1.14;font-weight:800;margin:.2rem 0 1rem;letter-spacing:-.01em}
h2{font-size:1.45rem;line-height:1.22;font-weight:800;margin:2.4rem 0 .7rem;
   padding-top:1.1rem;border-top:2px solid var(--rule)}
h3{font-size:1.15rem;font-weight:800;margin:1.7rem 0 .5rem}
h4{font-size:1.03rem;font-weight:800;margin:1.3rem 0 .4rem}
p,li{font-size:1.05rem}
p{margin:0 0 1rem}
ul,ol{margin:0 0 1.15rem 1.35rem}
li{margin:.42rem 0}
strong{font-weight:800}
hr{border:0;border-top:2px solid var(--rule);margin:2.2rem 0}
hr + h2{border-top:0;padding-top:0;margin-top:0}
h1 + h2{border-top:0;padding-top:0}

blockquote{
  border:3px solid var(--rule);background:var(--band);
  padding:1rem 1.1rem;margin:1.5rem 0}
blockquote > :last-child{margin-bottom:0}
blockquote h3{margin-top:0}

table{border-collapse:collapse;width:100%;margin:1.3rem 0;font-size:.98rem}
th,td{border:1px solid #bbb;padding:.55rem .6rem;text-align:left;vertical-align:top}
th{background:var(--band);font-weight:800}

code{background:var(--band);padding:.05em .3em;font-size:.95em}

.tel{white-space:nowrap;font-weight:800}

footer.site{margin-top:2.6rem;padding-top:1rem;border-top:5px solid var(--rule);
  font-size:.92rem;color:var(--muted)}
footer.site a{color:var(--accent)}
footer.site p{margin-bottom:.5rem;font-size:.92rem}
footer.site nav.sitenav{margin-bottom:1rem;font-size:.92rem;font-weight:700}

.cards{display:grid;grid-template-columns:1fr;gap:.85rem;margin:1.3rem 0 1.6rem}
@media (min-width:32rem){.cards{grid-template-columns:1fr 1fr}}
a.card{display:block;border:3px solid var(--rule);border-radius:.4rem;
  padding:1rem 1.1rem;text-decoration:none;color:var(--ink);background:var(--band);
  font-weight:800;font-size:1.06rem;line-height:1.35;min-height:3.4rem}
a.card:hover,a.card:focus-visible{border-color:var(--accent);background:#fff}
a.card span{display:block;font-weight:400;font-size:.88rem;color:var(--muted);
  margin-top:.3rem}

/* wide-screen nav rail: pure bonus for viewers with room, single column
   reading experience is unaffected below this breakpoint */
aside.rail{display:none}
@media (min-width:68rem){
  body{padding-left:15.5rem}
  aside.rail{display:block;position:fixed;left:2rem;top:2.2rem;width:12.5rem;
    font-size:.92rem;line-height:1.7}
  aside.rail .label{font-weight:800;text-transform:uppercase;letter-spacing:.05em;
    font-size:.75rem;color:var(--muted);margin-bottom:.5rem}
  aside.rail a{display:block;color:var(--ink);text-decoration:none;padding:.15rem 0}
  aside.rail a:hover{color:var(--accent)}
  aside.rail hr{margin:.9rem 0;border-top:1px solid #ccc}
}
.shell[dir="rtl"] aside.rail{left:auto;right:2rem}
@media (min-width:68rem){.shell[dir="rtl"]{padding-left:0}body:has(.shell[dir="rtl"]){padding-left:1.25rem;padding-right:15.5rem}}

.crumb{font-size:.92rem;margin-bottom:.6rem}
.crumb a{color:var(--muted)}

.shell[dir="rtl"]{direction:rtl;text-align:right}
.shell[dir="rtl"] ul,.shell[dir="rtl"] ol{margin:0 1.35rem 1.15rem 0}

@media print{
  body{background:#fff;padding:0!important}
  header.site,footer.site,.crumb,aside.rail{display:none}
  a{color:#000;text-decoration:none}
}
@media (max-width:26rem){ html{font-size:118%} h1{font-size:1.8rem} }
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="stylesheet" href="{pre}style.css">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<div class="shell"{dirattr}>
<aside class="rail">
  <div class="label">{railtitle}</div>
  <a href="{pre}">{navhome}</a>
  <a href="{pre}#scam-types">{navscams}</a>
  <a href="{pre}printables/">{navprint}</a>
  <a href="{pre}about/">{navabout}</a>
  <hr>
  <a href="{pre}scams/romance-scam/">{s_romance}</a>
  <a href="{pre}scams/tech-support-popup/">{s_tech}</a>
  <a href="{pre}scams/phantom-hacker/">{s_bank}</a>
  <a href="{pre}scams/government-impersonation/">{s_gov}</a>
  <a href="{pre}scams/grandparent-scam/">{s_grandparent}</a>
  <a href="{pre}scams/virtual-kidnapping/">{s_kidnap}</a>
  <a href="{pre}warning-signs/">{s_signs}</a>
</aside>
<header class="site">
  <div class="top">
    <a class="brand" href="{pre}">{mark}Trust But Verify</a>
    <details class="langswitch">
      <summary>{langbtn}</summary>
      <div class="panel">
{langs}
      </div>
    </details>
  </div>
  <p class="strap">{strap}</p>
  <nav class="sitenav" aria-label="Site">
    <a href="{pre}">{navhome}</a>
    <a href="{pre}#scam-types">{navscams}</a>
    <a href="{pre}printables/">{navprint}</a>
    <a href="{pre}about/">{navabout}</a>
  </nav>
</header>
{crumb}
<main id="main">
{body}
</main>
<footer class="site">
  <nav class="sitenav" aria-label="Site">
    <a href="{pre}">{navhome}</a>
    <a href="{pre}about/">{navabout}</a>
    <a href="{pre}give-this-talk/">{navtalk}</a>
    <a href="{pre}help-translate/">{navhelp}</a>
  </nav>
  <p><strong>{helpline}</strong>
     National Elder Fraud Hotline
     <a class="tel" href="tel:+18333728311">833-372-8311</a> ·
     AARP Fraud Watch
     <a class="tel" href="tel:+18779083360">877-908-3360</a></p>
  <p>Report at <a href="https://reportfraud.ftc.gov">reportfraud.ftc.gov</a>
     and <a href="https://www.ic3.gov">ic3.gov</a>.
     <a href="{pre}resources-by-language/">{langpage}</a>.</p>
  <p>{free}</p>
  <p>{nocookie}</p>
</footer>
</div>
</body>
</html>
"""

# ---------------------------------------------------------------------- render

md = markdown.Markdown(extensions=["tables", "attr_list", "sane_lists"])


def fix_links(body_html, pre):
    """Rewrite absolute site links (/foo) to relative dir URLs."""
    def repl(m):
        href = m.group(1)
        if href == "/":
            return 'href="%s"' % pre
        if "." in os.path.basename(href):
            return 'href="%s%s"' % (pre, href.lstrip("/"))
        return 'href="%s%s/"' % (pre, href.strip("/"))
    return re.sub(r'href="(/(?!/)[^"#]*)"', repl, body_html)


def phone_wrap(s):
    return re.sub(r"\b(8\d{2}-\d{3}-\d{4})\b",
                  lambda m: '<a class="tel" href="tel:+1%s">%s</a>' % (m.group(1).replace("-",""), m.group(1)), s)


def ui(lang, key):
    d = UI.get(lang) or {}
    if key in d:
        return d[key]
    return UI["en"][key]


def lang_label(code):
    for c, _short, label in LANGS:
        if c == code:
            return label
    return code


def lang_nav(pre, current):
    parts = ['<strong>%s</strong>' % html.escape(ui(current, "read"))]
    for code, _short, label in LANGS:
        href = pre if code == "en" else "%s%s/" % (pre, code)
        if code == current:
            parts.append("<strong>%s</strong>" % html.escape(label))
        else:
            parts.append('<a href="%s" lang="%s">%s</a>' % (href, code, html.escape(label)))
    return "\n".join(parts)


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    pages = []
    for dirpath, _dirs, files in os.walk(CONTENT):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            src = os.path.join(dirpath, fn)
            raw = open(src, encoding="utf-8").read()
            meta, body = split_front_matter(raw)
            lang = meta.get("lang", "en")
            slug = meta.get("slug") or "/" + os.path.relpath(src, CONTENT)[:-3]
            pages.append((src, meta, body, lang, slug))

    written = 0
    for src, meta, body, lang, slug in pages:
        outrel = slug_to_path(slug)
        outabs = os.path.join(OUT, outrel)
        os.makedirs(os.path.dirname(outabs), exist_ok=True)
        pre = depth_prefix(outrel)

        md.reset()
        body_html = md.convert(body)
        body_html = fix_links(body_html, pre)
        body_html = phone_wrap(body_html)

        title = meta.get("title", "Trust But Verify")
        if slug.strip("/") not in ("", lang):
            title = "%s — Trust But Verify" % title

        canonical = SITE + "/" + (outrel[:-len("index.html")]).replace(os.sep, "/")
        crumb = ("" if outrel == "index.html"
                 else '<p class="crumb"><a href="%s">← Back to the start</a></p>' % pre)

        page = PAGE.format(
            lang=lang,
            mark=MARK,
            dirattr=' dir="rtl"' if lang in RTL else "",
            title=html.escape(title),
            desc=html.escape(meta.get("description", "")),
            canonical=canonical,
            pre=pre,
            crumb=crumb,
            body=body_html,
            langs=lang_nav(pre, lang),
            langbtn=html.escape("\U0001F310 " + lang_label(lang)),
            skip=html.escape(ui(lang, "skip")),
            strap=html.escape(ui(lang, "strap")),
            helpline=html.escape(ui(lang, "help")),
            langpage=html.escape(ui(lang, "langpage")),
            free=html.escape(ui(lang, "free")),
            nocookie=html.escape(ui(lang, "nocookie")),
            railtitle=html.escape(ui(lang, "railtitle")),
            navhome=html.escape(ui(lang, "navhome")),
            navscams=html.escape(ui(lang, "navscams")),
            navprint=html.escape(ui(lang, "navprint")),
            navabout=html.escape(ui(lang, "navabout")),
            navtalk=html.escape(ui(lang, "navtalk")),
            navhelp=html.escape(ui(lang, "navhelp")),
            s_romance=html.escape(ui(lang, "s_romance")),
            s_tech=html.escape(ui(lang, "s_tech")),
            s_bank=html.escape(ui(lang, "s_bank")),
            s_gov=html.escape(ui(lang, "s_gov")),
            s_grandparent=html.escape(ui(lang, "s_grandparent")),
            s_kidnap=html.escape(ui(lang, "s_kidnap")),
            s_signs=html.escape(ui(lang, "s_signs")),
        )
        open(outabs, "w", encoding="utf-8").write(page)
        written += 1

    # stylesheet
    open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(CSS)

    # favicon: same mark, filled solid so it reads at 16px
    favicon = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
               '<path fill="#123f7a" d="M12 2.5 19.5 5.5V11C19.5 16 16 19.8 12 21.5 '
               '8 19.8 4.5 16 4.5 11V5.5Z"/>'
               '<path fill="none" stroke="#fffdf9" stroke-width="2.4" '
               'stroke-linecap="round" stroke-linejoin="round" '
               'd="M8.2 11.6 10.8 14.2 15.8 9"/></svg>')
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(favicon)

    # printables
    dest = os.path.join(OUT, "print")
    os.makedirs(dest, exist_ok=True)
    for fn in sorted(os.listdir(PRINT)):
        if fn.endswith(".pdf") or fn.endswith(".docx"):
            shutil.copy(os.path.join(PRINT, fn), os.path.join(dest, fn))

    # robots + sitemap
    open(os.path.join(OUT, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)

    today = datetime.date.today().isoformat()
    urls = []
    for _src, _meta, _b, _lang, slug in pages:
        loc = SITE + "/" + slug_to_path(slug)[:-len("index.html")].replace(os.sep, "/")
        urls.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, today))
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n</urlset>\n")

    # security + caching headers (Cloudflare Pages reads _headers)
    open(os.path.join(OUT, "_headers"), "w").write(
        "/*\n"
        "  X-Frame-Options: DENY\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: no-referrer\n"
        "  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()\n"
        "  Content-Security-Policy: default-src 'none'; style-src 'self'; img-src 'self'; "
        "base-uri 'none'; form-action 'none'; frame-ancestors 'none'\n"
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
        "\n/print/*\n  Cache-Control: public, max-age=86400\n")

    # 404
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        PAGE.format(lang="en", dirattr="", mark=MARK, title="Page not found — Trust But Verify",
                    desc="That page isn't here.", canonical=SITE + "/404.html", pre="./",
                    crumb="",
                    body="<h1>That page isn't here.</h1>"
                         "<p>Nothing is wrong and you haven't broken anything. "
                         "The link may be old or mistyped.</p>"
                         "<p><a href=\"/\">Start from the beginning</a>, or if something "
                         "is happening right now and you need a person: "
                         "<strong>833-372-8311</strong>.</p>",
                    langs=lang_nav("./", "en"), langbtn="\U0001F310 " + lang_label("en"),
                    skip=UI["en"]["skip"], strap=UI["en"]["strap"],
                    helpline=UI["en"]["help"], langpage=UI["en"]["langpage"],
                    free=UI["en"]["free"], nocookie=UI["en"]["nocookie"],
                    railtitle=UI["en"]["railtitle"], navhome=UI["en"]["navhome"],
                    navscams=UI["en"]["navscams"], navprint=UI["en"]["navprint"],
                    navabout=UI["en"]["navabout"], navtalk=UI["en"]["navtalk"],
                    navhelp=UI["en"]["navhelp"], s_romance=UI["en"]["s_romance"],
                    s_tech=UI["en"]["s_tech"], s_bank=UI["en"]["s_bank"],
                    s_gov=UI["en"]["s_gov"], s_grandparent=UI["en"]["s_grandparent"],
                    s_kidnap=UI["en"]["s_kidnap"], s_signs=UI["en"]["s_signs"]))

    print("pages: %d" % written)
    print("output: %s" % OUT)


if __name__ == "__main__":
    build()
