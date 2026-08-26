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

# Pilot audio narration, English only -- see build/make_audio.py. Bare
# slugs; "" (home) is handled as "home" in the player src, matching the
# audio filename make_audio.py actually writes.
AUDIO_PAGES = {
    "", "the-three-steps", "warning-signs", "about", "i-think-i-was-scammed",
    "scams/phantom-hacker", "scams/tech-support-popup", "scams/grandparent-scam",
    "scams/government-impersonation", "scams/romance-scam", "scams/job-scams",
    "scams/investment-and-crypto", "scams/medicare-scams", "scams/voice-cloning",
    "scams/delivery-toll-recall-texts", "scams/virtual-kidnapping", "scams/recovery-scam",
    "how-they-ask-to-be-paid", "for-family", "scams/sim-swap",
    "scams/charity-scams", "scams/lottery-sweepstakes", "scams/home-repair",
    "scams/phishing", "how-they-got-your-information", "for-facilities",
}

# Hero photos, keyed by bare slug, English pages only. Sourced from Wikimedia
# Commons under licenses that require attribution (CC BY / CC BY-SA) — the
# figcaption below is that attribution, not decorative text; don't remove it.
# See assets/photos/manifest.json for the full sourcing record, including
# topics deliberately left without a photo rather than forcing a bad fit.
PHOTOS = {
    "about": dict(file="about.jpg", alt="A grandparent watching a child play with a toy car",
                  author="Shixart1985",
                  url="https://commons.wikimedia.org/wiki/File:Grandparent_enjoys_coffee_while_watching_child_play_with_toy_car_during_sunset_at_the_park.jpg",
                  license="CC BY 2.0"),
    "warning-signs": dict(file="warning-signs.jpg", alt="A woman talking on the phone while writing in a notebook",
                           author="Shixart1985",
                           url="https://commons.wikimedia.org/wiki/File:Woman_talks_on_the_phone_while_writing_in_a_notebook.jpg",
                           license="CC BY 2.0"),
    "scams/grandparent-scam": dict(file="grandparent-scam.jpg", alt="A woman smiling while talking on a landline phone at home",
                                    author="Shixart1985",
                                    url="https://commons.wikimedia.org/wiki/File:Senior_woman_engaged_in_a_cheerful_conversation_on_a_landline_phone_at_her_home.jpg",
                                    license="CC BY 2.0"),
    "scams/virtual-kidnapping": dict(file="virtual-kidnapping.jpg", alt="A woman looking at her phone in a relaxed home setting",
                                      author="Shixart1985",
                                      url="https://commons.wikimedia.org/wiki/File:Woman_looking_at_phone_in_a_casual_setting_while_smiling_and_enjoying_the_moment_with_a_relaxed_atmosphere.jpg",
                                      license="CC BY 2.0"),
    "scams/romance-scam": dict(file="romance-scam.jpg", alt="Hands typing on a laptop keyboard",
                                author="Shixart1985",
                                url="https://commons.wikimedia.org/wiki/File:Woman_with_long_nails_typing_on_a_laptop_keyboard.jpg",
                                license="CC BY 2.0"),
    "scams/tech-support-popup": dict(file="tech-support-popup.jpg", alt="A laptop on a desk in a home workspace",
                                      author="Shixart1985",
                                      url="https://commons.wikimedia.org/wiki/File:Laptop_and_small_plant_on_a_desk_in_a_modern_workspace_during_daylight_hours.jpg",
                                      license="CC BY 2.0"),
    "scams/delivery-toll-recall-texts": dict(file="delivery-toll-recall-texts.jpg", alt="A delivery driver knocking on a door with packages",
                                              author="Meanwell Packaging",
                                              url="https://commons.wikimedia.org/wiki/File:A_Delivery_Driver_Knocking_on_a_Door_to_Deliver_Packages.jpg",
                                              license="CC BY 2.0"),
    "scams/phishing": dict(file="phishing.jpg", alt="Hands typing on a laptop keyboard",
                            author="Shixart1985",
                            url="https://commons.wikimedia.org/wiki/File:Hands_are_seen_typing_on_a_laptop_keyboard.jpg",
                            license="CC BY 2.0"),
    "scams/job-scams": dict(file="job-scams.jpg", alt="A laptop, coffee cup, and plant on a desk",
                             author="Shixart1985",
                             url="https://commons.wikimedia.org/wiki/File:Working_at_a_desk_with_a_laptop_coffee_cup_and_a_plant_on_a_white_surface.jpg",
                             license="CC BY 2.0"),
    "scams/investment-and-crypto": dict(file="investment-and-crypto.jpg", alt="A hand writing on a receipt next to a calculator",
                                         author="Dave Dugdale from Superior, USA",
                                         url="https://commons.wikimedia.org/wiki/File:Analyzing_Financial_Data_(5099605109).jpg",
                                         license="CC BY-SA 2.0"),
    "scams/voice-cloning": dict(file="voice-cloning.jpg", alt="A woman talking on the phone",
                                 author="Shixart1985",
                                 url="https://commons.wikimedia.org/wiki/File:Woman_talking_on_phone_in_a_modern_indoor_space_closeup.jpg",
                                 license="CC BY 2.0"),
    "scams/home-repair": dict(file="home-repair.jpg", alt="A man working on a car in a garage",
                               author="Shixart1985",
                               url="https://commons.wikimedia.org/wiki/File:Elderly_man_stands_in_garage_near_car_with_tools_showing_signs_of_work_done.jpg",
                               license="CC BY 2.0"),
    "scams/medicare-scams": dict(file="medicare-scams.jpg", alt="A stethoscope held in a hand",
                                  author="Shixart1985",
                                  url="https://commons.wikimedia.org/wiki/File:Close-up_of_a_stethoscope_chest_piece_in_a_womans_hand_with_a_blurry_background.jpg",
                                  license="CC BY 2.0"),
    "scams/sim-swap": dict(file="sim-swap.jpg", alt="A SIM card and tray next to a ruler",
                            author="BwDraco",
                            url="https://commons.wikimedia.org/wiki/File:Nano_SIM_card_and_tray.jpg",
                            license="CC BY-SA 3.0"),
    "scams/phantom-hacker": dict(file="phantom-hacker.jpg", alt="A woman holding a phone in each hand while sitting at a laptop",
                                  author="Shixart1985",
                                  url="https://commons.wikimedia.org/wiki/File:Frustrated_woman_holds_telephone_receiver_while_working_at_laptop.jpg",
                                  license="CC BY 2.0"),
}

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
    ("ht", "ht",         "Kreyòl Ayisyen"),
    ("pa", "pa",         "ਪੰਜਾਬੀ"),
    ("gu", "gu",         "ગુજરાતી"),
    ("so", "so",         "Af-Soomaali"),
    ("km", "km",         "ខ្មែរ"),
    ("hmn", "hmn",       "Hmoob"),
    ("ka", "ka",         "ქართული"),
    ("lt", "lt",         "Lietuvių"),
    ("lv", "lv",         "Latviešu"),
    ("et", "et",         "Eesti"),
    ("it", "it",         "Italiano"),
    ("el", "el",         "Ελληνικά"),
    ("he", "he",         "עברית"),
    ("hu", "hu",         "Magyar"),
    ("hr", "hr",         "Hrvatski"),
    ("sr", "sr",         "Српски"),
    ("ms", "ms",         "Bahasa Melayu"),
    ("sv", "sv",         "Svenska"),
    ("no", "no",         "Norsk"),
    ("da", "da",         "Dansk"),
    ("sw", "sw",         "Kiswahili"),
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
   navprivacy="Privacy", navterms="Terms", navblog="Blog",
   listen="Listen to this page:",
   railtitle="Find your way", s_romance="Someone I met online",
   s_tech="Fake tech support", s_bank="Bank / “phantom hacker”",
   s_gov="Government impersonation", s_grandparent="Grandchild in trouble",
   s_kidnap="Virtual kidnapping", s_signs="Three warning signs"),
 "es": dict(strap="Cuelgue. Busque el n\u00famero usted mismo. Espere un d\u00eda.",
   back="\u2190 Volver al inicio", read="Leer esto en:", help="Ayuda gratuita, sin juicios.",
   nocookie="Este sitio no usa cookies ni recopila datos personales \u2014 Cloudflare solo cuenta visitas an\u00f3nimas a la p\u00e1gina.",
   free="Libre de imprimir, copiar, traducir y compartir. No hace falta permiso.",
   langpage="Ayuda en su idioma", skip="Ir al contenido principal",
   navhome="Inicio", navscams="Tipos de estafas", navprint="Materiales para imprimir",
   navabout="Acerca de", navtalk="D\u00e9 esta charla", navhelp="Ayude a traducir",
   navprivacy="Privacidad", navterms="T\u00e9rminos", navblog="Blog",
   railtitle="Encuentre su camino", s_romance="Alguien que conoc\u00ed en l\u00ednea",
   s_tech="Soporte t\u00e9cnico falso", s_bank="Banco / \u201chacker fantasma\u201d",
   s_gov="Suplantaci\u00f3n del gobierno", s_grandparent="Nieto en problemas",
   s_kidnap="Secuestro virtual", s_signs="Tres se\u00f1ales de alerta"),
 "vi": dict(strap="C\u00fap m\u00e1y. T\u1ef1 m\u00ecnh tra s\u1ed1. Ch\u1edd m\u1ed9t ng\u00e0y.",
   back="\u2190 V\u1ec1 trang \u0111\u1ea7u", read="\u0110\u1ecdc b\u1eb1ng:", help="Tr\u1ee3 gi\u00fap mi\u1ec5n ph\u00ed, kh\u00f4ng ph\u00e1n x\u00e9t.",
   nocookie="Trang n\u00e0y kh\u00f4ng d\u00f9ng cookie v\u00e0 kh\u00f4ng thu th\u1eadp d\u1eef li\u1ec7u c\u00e1 nh\u00e2n \u2014 Cloudflare ch\u1ec9 \u0111\u1ebfm l\u01b0\u1ee3t xem trang \u1ea9n danh.",
   free="T\u1ef1 do in, sao ch\u00e9p, d\u1ecbch v\u00e0 chia s\u1ebb. Kh\u00f4ng c\u1ea7n xin ph\u00e9p.",
   langpage="Tr\u1ee3 gi\u00fap b\u1eb1ng ng\u00f4n ng\u1eef c\u1ee7a qu\u00fd v\u1ecb", skip="\u0110\u1ebfn n\u1ed9i dung ch\u00ednh",
   navhome="Trang ch\u1ee7", navscams="C\u00e1c lo\u1ea1i l\u1eeba \u0111\u1ea3o", navprint="T\u00e0i li\u1ec7u in",
   navabout="Gi\u1edbi thi\u1ec7u", navtalk="Tr\u00ecnh b\u00e0y bu\u1ed5i n\u00f3i chuy\u1ec7n n\u00e0y", navhelp="Gi\u00fap d\u1ecbch thu\u1eadt",
   navprivacy="Quy\u1ec1n ri\u00eang t\u01b0", navterms="\u0110i\u1ec1u kho\u1ea3n", navblog="Blog",
   railtitle="T\u00ecm h\u01b0\u1edbng \u0111i c\u1ee7a b\u1ea1n", s_romance="Ng\u01b0\u1eddi t\u00f4i quen qua m\u1ea1ng",
   s_tech="H\u1ed7 tr\u1ee3 k\u1ef9 thu\u1eadt gi\u1ea3 m\u1ea1o", s_bank="Ng\u00e2n h\u00e0ng / \u201ctin t\u1eb7c ma\u201d",
   s_gov="Gi\u1ea3 m\u1ea1o c\u01a1 quan ch\u00ednh ph\u1ee7", s_grandparent="Ch\u00e1u g\u1eb7p r\u1eafc r\u1ed1i",
   s_kidnap="B\u1eaft c\u00f3c gi\u1ea3", s_signs="Ba d\u1ea5u hi\u1ec7u c\u1ea3nh b\u00e1o"),
 "zh": dict(strap="\u6302\u65ad\u3002\u81ea\u5df1\u67e5\u53f7\u7801\u3002\u7b49\u4e00\u5929\u3002",
   back="\u2190 \u56de\u5230\u9996\u9875", read="\u5176\u4ed6\u8bed\u8a00\uff1a", help="\u514d\u8d39\u6c42\u52a9\uff0c\u4e0d\u4f1a\u6709\u4eba\u8bc4\u5224\u60a8\u3002",
   nocookie="\u672c\u7ad9\u4e0d\u4f7f\u7528 Cookie\uff0c\u4e5f\u4e0d\u6536\u96c6\u60a8\u7684\u4e2a\u4eba\u4fe1\u606f\u2014\u2014Cloudflare \u53ea\u7edf\u8ba1\u533f\u540d\u7684\u9875\u9762\u8bbf\u95ee\u91cf\u3002",
   free="\u6b22\u8fce\u81ea\u7531\u6253\u5370\u3001\u590d\u5236\u3001\u7ffb\u8bd1\u548c\u5206\u4eab\u3002\u65e0\u9700\u6388\u6743\u3002",
   langpage="\u7528\u60a8\u7684\u8bed\u8a00\u6c42\u52a9", skip="\u8df3\u5230\u4e3b\u8981\u5185\u5bb9",
   navhome="\u9996\u9875", navscams="\u8bc8\u9a97\u7c7b\u578b", navprint="\u5370\u5237\u6750\u6599",
   navabout="\u5173\u4e8e\u6211\u4eec", navtalk="\u505a\u8fd9\u4e2a\u8bb2\u5ea7", navhelp="\u5e2e\u52a9\u7ffb\u8bd1",
   navprivacy="\u9690\u79c1", navterms="\u6761\u6b3e", navblog="\u535a\u5ba2",
   railtitle="\u5feb\u901f\u5bfc\u822a", s_romance="\u7f51\u604b\u5bf9\u8c61",
   s_tech="\u865a\u5047\u6280\u672f\u652f\u6301", s_bank="\u94f6\u884c\uff0f\u201c\u5e7d\u7075\u9ed1\u5ba2\u201d",
   s_gov="\u5192\u5145\u653f\u5e9c\u673a\u6784", s_grandparent="\u5b59\u8f88\u9047\u5230\u9ebb\u70e6",
   s_kidnap="\u865a\u62df\u7ed1\u67b6", s_signs="\u4e09\u4e2a\u8b66\u793a\u4fe1\u53f7"),
 "ru": dict(strap="\u041f\u043e\u043b\u043e\u0436\u0438\u0442\u0435 \u0442\u0440\u0443\u0431\u043a\u0443. \u041d\u0430\u0439\u0434\u0438\u0442\u0435 \u043d\u043e\u043c\u0435\u0440 \u0441\u0430\u043c\u0438. \u041f\u043e\u0434\u043e\u0436\u0434\u0438\u0442\u0435 \u0441\u0443\u0442\u043a\u0438.",
   back="\u2190 \u041d\u0430 \u0433\u043b\u0430\u0432\u043d\u0443\u044e", read="\u0427\u0438\u0442\u0430\u0442\u044c \u043d\u0430:", help="\u0411\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u0430\u044f \u043f\u043e\u043c\u043e\u0449\u044c, \u0431\u0435\u0437 \u043e\u0441\u0443\u0436\u0434\u0435\u043d\u0438\u044f.",
   nocookie="\u042d\u0442\u043e\u0442 \u0441\u0430\u0439\u0442 \u043d\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442 cookie \u0438 \u043d\u0435 \u0441\u043e\u0431\u0438\u0440\u0430\u0435\u0442 \u043b\u0438\u0447\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435 \u2014 Cloudflare \u043f\u043e\u0434\u0441\u0447\u0438\u0442\u044b\u0432\u0430\u0435\u0442 \u0442\u043e\u043b\u044c\u043a\u043e \u0430\u043d\u043e\u043d\u0438\u043c\u043d\u044b\u0435 \u043f\u0440\u043e\u0441\u043c\u043e\u0442\u0440\u044b \u0441\u0442\u0440\u0430\u043d\u0438\u0446.",
   free="\u041c\u043e\u0436\u043d\u043e \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u043e \u043f\u0435\u0447\u0430\u0442\u0430\u0442\u044c, \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0438 \u0440\u0430\u0441\u043f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u044f\u0442\u044c. \u0420\u0430\u0437\u0440\u0435\u0448\u0435\u043d\u0438\u0435 \u043d\u0435 \u043d\u0443\u0436\u043d\u043e.",
   langpage="\u041f\u043e\u043c\u043e\u0449\u044c \u043d\u0430 \u0432\u0430\u0448\u0435\u043c \u044f\u0437\u044b\u043a\u0435", skip="\u041a \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u043c\u0443 \u0441\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u044e",
   navhome="\u0413\u043b\u0430\u0432\u043d\u0430\u044f", navscams="\u0412\u0438\u0434\u044b \u043c\u043e\u0448\u0435\u043d\u043d\u0438\u0447\u0435\u0441\u0442\u0432\u0430", navprint="\u041f\u0435\u0447\u0430\u0442\u043d\u044b\u0435 \u043c\u0430\u0442\u0435\u0440\u0438\u0430\u043b\u044b",
   navabout="\u041e \u0441\u0430\u0439\u0442\u0435", navtalk="\u041f\u0440\u043e\u0432\u0435\u0441\u0442\u0438 \u044d\u0442\u0443 \u0431\u0435\u0441\u0435\u0434\u0443", navhelp="\u041f\u043e\u043c\u043e\u0447\u044c \u0441 \u043f\u0435\u0440\u0435\u0432\u043e\u0434\u043e\u043c",
   navprivacy="\u041a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u043e\u0441\u0442\u044c", navterms="\u0423\u0441\u043b\u043e\u0432\u0438\u044f", navblog="\u0411\u043b\u043e\u0433",
   railtitle="\u0411\u044b\u0441\u0442\u0440\u044b\u0439 \u043f\u0435\u0440\u0435\u0445\u043e\u0434", s_romance="\u0427\u0435\u043b\u043e\u0432\u0435\u043a, \u0432\u0441\u0442\u0440\u0435\u0447\u0435\u043d\u043d\u044b\u0439 \u043e\u043d\u043b\u0430\u0439\u043d",
   s_tech="\u041f\u043e\u0434\u0434\u0435\u043b\u044c\u043d\u0430\u044f \u0442\u0435\u0445\u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0430", s_bank="\u0411\u0430\u043d\u043a / \u00ab\u0444\u0430\u043d\u0442\u043e\u043c\u043d\u044b\u0439 \u0445\u0430\u043a\u0435\u0440\u00bb",
   s_gov="\u041c\u043e\u0448\u0435\u043d\u043d\u0438\u043a\u0438 \u043e\u0442 \u0438\u043c\u0435\u043d\u0438 \u0433\u043e\u0441\u0443\u0434\u0430\u0440\u0441\u0442\u0432\u0430", s_grandparent="\u0412\u043d\u0443\u043a \u0432 \u0431\u0435\u0434\u0435",
   s_kidnap="\u0412\u0438\u0440\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u0445\u0438\u0449\u0435\u043d\u0438\u0435", s_signs="\u0422\u0440\u0438 \u0442\u0440\u0435\u0432\u043e\u0436\u043d\u044b\u0445 \u043f\u0440\u0438\u0437\u043d\u0430\u043a\u0430"),
}


UI["ko"] = dict(strap="전화를 끊으십시오. 번호를 직접 찾으십시오. 하루 기다리십시오.",
  back="← 처음으로", read="다른 언어로 읽기:", help="무료 도움, 나무라지 않습니다.",
  nocookie="이 사이트는 쿠키를 쓰지 않고 개인정보를 수집하지 않습니다 — Cloudflare는 익명 페이지뷰만 집계합니다.",
  free="자유롭게 인쇄, 복사, 번역, 공유하십시오. 허락은 필요 없습니다.",
  langpage="당신의 언어로 도움받기", skip="본문으로 건너뛰기",
  navhome="홈", navscams="사기 유형", navprint="인쇄 자료",
  navabout="소개", navtalk="이 강연 진행하기", navhelp="번역 돕기",
  navprivacy="개인정보 보호", navterms="이용 약관", navblog="블로그",
  railtitle="빠른 이동", s_romance="온라인에서 만난 사람",
  s_tech="가짜 기술 지원", s_bank="은행 / “유령 해커”",
  s_gov="정부 사칭", s_grandparent="손주가 곤경에 처했다는 전화",
  s_kidnap="가상 납치", s_signs="세 가지 경고 신호")
UI["ja"] = dict(strap="電話を切る。番号は自分で調べる。一日待つ。",
  back="← 最初に戻る", read="他の言語で読む：", help="無料の相談。責めません。",
  nocookie="このサイトはクッキーを使わず、個人情報も収集しません。Cloudflareは匿名のページビューのみを集計します。",
  free="自由に印刷・複製・翻訳・共有してください。許可は不要です。",
  langpage="あなたの言語での相談先", skip="本文へ移動",
  navhome="ホーム", navscams="詐欺の種類", navprint="印刷用資料",
  navabout="このサイトについて", navtalk="この講演を行う", navhelp="翻訳に協力する",
  navprivacy="プライバシー", navterms="利用規約", navblog="ブログ",
  railtitle="サイト内ナビ", s_romance="ネットで知り合った相手",
  s_tech="偽のテクニカルサポート", s_bank="銀行／「幽霊ハッカー」",
  s_gov="政府機関のなりすまし", s_grandparent="孫がトラブルに",
  s_kidnap="バーチャル誘拐", s_signs="3つの警告サイン")
UI["hi"] = dict(strap="फ़ोन काटें। नंबर खुद ढूँढें। एक दिन रुकें।",
  back="← शुरुआत पर वापस", read="इन भाषाओं में पढ़ें:", help="मुफ़्त मदद, कोई ताना नहीं।",
  nocookie="यह साइट कुकी नहीं रखती और कोई व्यक्तिगत जानकारी नहीं जुटाती — Cloudflare केवल गुमनाम पेजव्यू गिनता है।",
  free="बेझिझक छापें, कॉपी करें, अनुवाद करें और बाँटें। अनुमति की ज़रूरत नहीं।",
  langpage="अपनी भाषा में मदद", skip="मुख्य सामग्री पर जाएँ",
  navhome="होम", navscams="धोखाधड़ी के प्रकार", navprint="प्रिंट सामग्री",
  navabout="हमारे बारे में", navtalk="यह वार्ता दें", navhelp="अनुवाद में मदद करें",
  navprivacy="गोपनीयता", navterms="शर्तें", navblog="ब्लॉग",
  railtitle="जल्दी पहुँचें", s_romance="ऑनलाइन मिला कोई व्यक्ति",
  s_tech="नकली तकनीकी सहायता", s_bank="बैंक / “भूत हैकर”",
  s_gov="सरकार का रूप धरना", s_grandparent="पोता-पोती मुसीबत में",
  s_kidnap="वर्चुअल अपहरण", s_signs="तीन चेतावनी संकेत")
UI["bn"] = dict(strap="ফোন রাখুন। নম্বর নিজে খুঁজুন। একদিন অপেক্ষা করুন।",
  back="← শুরুতে ফিরুন", read="অন্য ভাষায় পড়ুন:", help="বিনামূল্যে সহায়তা, কোনো দোষারোপ নেই।",
  nocookie="এই সাইট কুকি রাখে না এবং কোনো ব্যক্তিগত তথ্য সংগ্রহ করে না — Cloudflare শুধু বেনামী পেজভিউ গণনা করে।",
  free="স্বাধীনভাবে ছাপুন, কপি করুন, অনুবাদ করুন ও ভাগ করুন। অনুমতি লাগবে না।",
  langpage="আপনার ভাষায় সহায়তা", skip="মূল অংশে যান",
  navhome="হোম", navscams="প্রতারণার ধরন", navprint="প্রিন্ট সামগ্রী",
  navabout="আমাদের সম্পর্কে", navtalk="এই আলোচনা দিন", navhelp="অনুবাদে সাহায্য করুন",
  navprivacy="গোপনীয়তা", navterms="শর্তাবলী", navblog="ব্লগ",
  railtitle="দ্রুত যান", s_romance="অনলাইনে পরিচিত কেউ",
  s_tech="ভুয়া প্রযুক্তি সহায়তা", s_bank="ব্যাংক / “ভুতুড়ে হ্যাকার”",
  s_gov="সরকারি ছদ্মবেশ", s_grandparent="নাতি-নাতনি বিপদে",
  s_kidnap="ভার্চুয়াল অপহরণ", s_signs="তিনটি সতর্কতা চিহ্ন")
UI["tl"] = dict(strap="Ibaba ang telepono. Hanapin mo mismo ang numero. Maghintay ng isang araw.",
  back="← Balik sa simula", read="Basahin ito sa:", help="Libreng tulong, walang husga.",
  nocookie="Walang cookies ang site na ito at walang kinokolektang personal na impormasyon — binibilang lang ng Cloudflare ang anonymous na pageviews.",
  free="Malayang i-print, kopyahin, isalin, at ipamahagi. Hindi kailangan ng pahintulot.",
  langpage="Tulong sa iyong wika", skip="Tumalon sa pangunahing nilalaman",
  navhome="Home", navscams="Uri ng scam", navprint="Mga materyal na maipi-print",
  navabout="Tungkol sa amin", navtalk="Magbigay ng talk na ito", navhelp="Tumulong magsalin",
  navprivacy="Privacy", navterms="Mga Tuntunin", navblog="Blog",
  railtitle="Mabilisang sanggunian", s_romance="Taong nakilala online",
  s_tech="Peke na tech support", s_bank="Bangko / “multong hacker”",
  s_gov="Pagpapanggap bilang gobyerno", s_grandparent="Apo raw nasa gulo",
  s_kidnap="Virtual na pagdukot", s_signs="Tatlong babala")
UI["hy"] = dict(strap="Անջատեք։ Համարը ինքներդ գտեք։ Սպասեք մեկ օր։",
  back="← Վերադառնալ սկիզբ", read="Կարդալ նաև՝", help="Անվճար օգնություն, առանց դատելու։",
  nocookie="Այս կայքը cookie չի օգտագործում և ձեր անձնական տվյալները չի հավաքում։ Cloudflare-ը հաշվում է միայն անանուն դիտումների քանակը։",
  free="Ազատորեն տպեք, պատճենեք, թարգմանեք և տարածեք։ Թույլտվություն պետք չէ։",
  langpage="Օգնություն ձեր լեզվով", skip="Անցնել հիմնական բովանդակությանը",
  navhome="Գլխավոր", navscams="Խարդախության տեսակներ", navprint="Տպագիր նյութեր",
  navabout="Մեր մասին", navtalk="Կայացրեք այս զրույցը", navhelp="Օգնեք թարգմանել",
  navprivacy="Գաղտնիություն", navterms="Պայմաններ", navblog="Բլոգ",
  railtitle="Արագ նավարկություն", s_romance="Ինտերնետով ծանոթացած մեկը",
  s_tech="Կեղծ տեխնիկական աջակցություն", s_bank="Բանկ / «ուրվական հաքեր»",
  s_gov="Կառավարության քողարկում", s_grandparent="Թոռը՝ դժվարության մեջ",
  s_kidnap="Վիրտուալ առևանգում", s_signs="Երեք նախազգուշական նշան")
UI["am"] = dict(strap="ስልኩን ይዝጉ። ቁጥሩን ራስዎ ይፈልጉ። አንድ ቀን ይጠብቁ።",
  back="← ወደ መጀመሪያው ተመለስ", read="በሌላ ቋንቋ ያንብቡ፦", help="ነጻ እርዳታ፣ ማንም አይወቅስዎትም።",
  nocookie="ይህ ድረ-ገጽ ኩኪ አይጠቀምም እና የግል መረጃዎን አይሰበስብም — Cloudflare ስም-አልባ የገጽ ጉብኝት ብዛት ብቻ ይቆጥራል።",
  free="በነጻነት ያትሙ፣ ይቅዱ፣ ይተርጉሙ እና ያካፍሉ። ፈቃድ አያስፈልግም።",
  langpage="በቋንቋዎ እርዳታ", skip="ወደ ዋናው ይዘት ዝለል",
  navhome="መነሻ", navscams="የማጭበርበሪያ ዓይነቶች", navprint="የህትመት ቁሳቁሶች",
  navabout="ስለ እኛ", navtalk="ይህን ንግግር ስጡ", navhelp="ትርጉም ያግዙ",
  navprivacy="ግላዊነት", navterms="ውሎች", navblog="ብሎግ",
  railtitle="ፈጣን አሰሳ", s_romance="በኢንተርኔት ያገኙት ሰው",
  s_tech="ሐሰተኛ ቴክኒካል ድጋፍ", s_bank="ባንክ / «መንፈስ ጠላፊ»",
  s_gov="የመንግስት ማስመሰል", s_grandparent="የልጅ ልጅ ችግር ላይ ነው",
  s_kidnap="ምናባዊ አፈና", s_signs="ሦስት ማስጠንቀቂያ ምልክቶች")
UI["sq"] = dict(strap="Mbylleni telefonin. Gjejeni vetë numrin. Prisni një ditë.",
  back="← Kthehu në fillim", read="Lexoni këtë në:", help="Ndihmë falas, pa gjykim.",
  nocookie="Kjo faqe nuk përdor cookies dhe nuk mbledh të dhëna personale — Cloudflare numëron vetëm shikime anonime të faqes.",
  free="I lirë për ta printuar, kopjuar, përkthyer dhe shpërndarë. Pa leje.",
  langpage="Ndihmë në gjuhën tuaj", skip="Kalo te përmbajtja kryesore",
  navhome="Kreu", navscams="Llojet e mashtrimeve", navprint="Materiale për printim",
  navabout="Rreth nesh", navtalk="Mbani këtë bisedë", navhelp="Ndihmoni të përkthejmë",
  navprivacy="Privatësia", navterms="Kushtet", navblog="Blog",
  railtitle="Gjeni rrugën", s_romance="Dikush që takova online",
  s_tech="Mbështetje teknike e rreme", s_bank="Banka / “haker fantazmë”",
  s_gov="Imitim i qeverisë", s_grandparent="Nipi/mbesa në telashe",
  s_kidnap="Rrëmbim virtual", s_signs="Tre shenja paralajmëruese")
UI["ar"] = dict(strap="أغلق الخط. ابحث عن الرقم بنفسك. انتظر يومًا.",
  back="← العودة إلى البداية", read="اقرأ هذا بلغة أخرى:", help="مساعدة مجانية، بلا أحكام.",
  nocookie="هذا الموقع لا يستخدم ملفات تعريف الارتباط ولا يجمع أي بيانات شخصية — تحسب Cloudflare فقط عدد الزيارات المجهولة للصفحة.",
  free="يمكنك الطباعة والنسخ والترجمة والمشاركة بحرية. لا حاجة لإذن.",
  langpage="مساعدة بلغتك", skip="انتقل إلى المحتوى الرئيسي",
  navhome="الرئيسية", navscams="أنواع الاحتيال", navprint="مواد للطباعة",
  navabout="نبذة عنا", navtalk="قدّم هذه المحاضرة", navhelp="ساعد في الترجمة",
  navprivacy="الخصوصية", navterms="الشروط", navblog="المدونة",
  railtitle="تصفح سريع", s_romance="شخص تعرفت عليه عبر الإنترنت",
  s_tech="دعم فني وهمي", s_bank="البنك / «القرصان الشبح»",
  s_gov="انتحال صفة جهة حكومية", s_grandparent="حفيد في ورطة",
  s_kidnap="اختطاف وهمي", s_signs="ثلاث علامات تحذيرية")
UI["ur"] = dict(strap="فون بند کریں۔ نمبر خود تلاش کریں۔ ایک دن انتظار کریں۔",
  back="← شروع پر واپس", read="اسے اس زبان میں پڑھیں:", help="مفت مدد، کوئی ملامت نہیں۔",
  nocookie="یہ سائٹ کوکیز استعمال نہیں کرتی اور کوئی ذاتی معلومات جمع نہیں کرتی — Cloudflare صرف گمنام پیج ویوز شمار کرتا ہے۔",
  free="آزادانہ چھاپیں، نقل کریں، ترجمہ کریں اور تقسیم کریں۔ اجازت کی ضرورت نہیں۔",
  langpage="اپنی زبان میں مدد", skip="مرکزی مواد پر جائیں",
  navhome="ہوم", navscams="فراڈ کی اقسام", navprint="پرنٹ میٹریل",
  navabout="ہمارے بارے میں", navtalk="یہ گفتگو پیش کریں", navhelp="ترجمے میں مدد کریں",
  navprivacy="رازداری", navterms="شرائط", navblog="بلاگ",
  railtitle="فوری رسائی", s_romance="آن لائن ملنے والا کوئی شخص",
  s_tech="جعلی تکنیکی مدد", s_bank="بینک / “غائب ہیکر”",
  s_gov="حکومت کا جعلی روپ", s_grandparent="پوتا/پوتی مصیبت میں",
  s_kidnap="ورچوئل اغوا", s_signs="تین وارننگ نشانیاں")
UI["fa"] = dict(strap="تلفن را قطع کنید. شماره را خودتان پیدا کنید. یک روز صبر کنید.",
  back="← بازگشت به آغاز", read="این را به زبان دیگر بخوانید:", help="کمک رایگان، بدون سرزنش.",
  nocookie="این سایت از کوکی استفاده نمی‌کند و هیچ اطلاعات شخصی جمع نمی‌کند — Cloudflare فقط بازدیدهای ناشناس صفحه را می‌شمارد.",
  free="آزادانه چاپ، کپی، ترجمه و منتشر کنید. نیازی به اجازه نیست.",
  langpage="کمک به زبان شما", skip="رفتن به محتوای اصلی",
  navhome="خانه", navscams="انواع کلاهبرداری", navprint="مطالب چاپی",
  navabout="درباره ما", navtalk="این سخنرانی را ارائه دهید", navhelp="در ترجمه کمک کنید",
  navprivacy="حریم خصوصی", navterms="شرایط", navblog="وبلاگ",
  railtitle="دسترسی سریع", s_romance="فردی که آنلاین آشنا شدید",
  s_tech="پشتیبانی فنی جعلی", s_bank="بانک / «هکر شبح»",
  s_gov="جعل هویت دولتی", s_grandparent="نوه در دردسر",
  s_kidnap="آدم‌ربایی مجازی", s_signs="سه نشانه هشدار")
UI["ps"] = dict(strap="ټیلیفون بند کړئ. شمېره پخپله ولټوئ. یوه ورځ صبر وکړئ.",
  back="← بېرته پیل ته", read="دا په بله ژبه ولولئ:", help="وړیا مرسته، هېڅ ملامتیا نشته.",
  nocookie="دا ویب پاڼه کوکیز نه کاروي او ستاسو شخصي معلومات نه راټولوي — Cloudflare یوازې ناپیژندل شوي د پاڼې لیدنې شمېري.",
  free="په آزادۍ سره یې چاپ، کاپي، ژباړه او شریکول کولی شئ. اجازې ته اړتیا نشته.",
  langpage="ستاسو په ژبه مرسته", skip="اصلي منځپانګې ته ورشئ",
  navhome="کور", navscams="د درغلۍ ډولونه", navprint="د چاپ توکي",
  navabout="زموږ په اړه", navtalk="دا خبرې اترې وړاندې کړئ", navhelp="په ژباړه کې مرسته وکړئ",
  navprivacy="محرمیت", navterms="شرایط", navblog="بلاگ",
  railtitle="ګړندی لاره موندنه", s_romance="هغه کس چې آنلاین سره پیژندل شوی",
  s_tech="جعلي تخنیکي مرسته", s_bank="بانک / «روح هکر»",
  s_gov="د حکومت جعل", s_grandparent="لمسی/لمسۍ په ستونزه کې",
  s_kidnap="مجازی زورول", s_signs="درې خبرداری نښې")

UI["de"] = dict(strap="Auflegen. Die Nummer selbst nachschlagen. Einen Tag warten.",
  back="← Zurück zum Anfang", read="Auf anderen Sprachen lesen:", help="Kostenlose Hilfe, ohne Urteil.",
  nocookie="Diese Website setzt keine Cookies und sammelt keine persönlichen Daten – Cloudflare zählt nur anonyme Seitenaufrufe.",
  free="Frei zum Drucken, Kopieren, Übersetzen und Weitergeben. Keine Erlaubnis nötig.",
  langpage="Hilfe in Ihrer Sprache", skip="Zum Hauptinhalt springen",
  navhome="Startseite", navscams="Betrugsarten", navprint="Druckmaterialien",
  navabout="Über uns", navtalk="Diesen Vortrag halten", navhelp="Beim Übersetzen helfen",
  navprivacy="Datenschutz", navterms="Nutzungsbedingungen", navblog="Blog",
  railtitle="Schnellzugriff", s_romance="Jemand, den ich online kennengelernt habe",
  s_tech="Falscher technischer Support", s_bank="Bank / „Phantom-Hacker“",
  s_gov="Vorgetäuschte Behörde", s_grandparent="Enkelkind in Schwierigkeiten",
  s_kidnap="Virtuelle Entführung", s_signs="Drei Warnzeichen")
UI["fr"] = dict(strap="Raccrochez. Cherchez le numéro vous-même. Attendez un jour.",
  back="← Retour au début", read="Lire dans une autre langue :", help="Aide gratuite, sans jugement.",
  nocookie="Ce site ne dépose aucun cookie et ne collecte aucune donnée personnelle — Cloudflare compte uniquement des visites anonymes.",
  free="Libre à imprimer, copier, traduire et partager. Aucune autorisation nécessaire.",
  langpage="Aide dans votre langue", skip="Aller au contenu principal",
  navhome="Accueil", navscams="Types d'arnaques", navprint="Documents à imprimer",
  navabout="À propos", navtalk="Donner cette présentation", navhelp="Aider à traduire",
  navprivacy="Confidentialité", navterms="Conditions", navblog="Blog",
  railtitle="Accès rapide", s_romance="Une personne rencontrée en ligne",
  s_tech="Faux support technique", s_bank="Banque / « pirate fantôme »",
  s_gov="Usurpation d'un organisme gouvernemental", s_grandparent="Petit-enfant en difficulté",
  s_kidnap="Enlèvement virtuel", s_signs="Trois signes d'alerte")
UI["pt"] = dict(strap="Desligue. Procure o número você mesmo. Espere um dia.",
  back="← Voltar ao início", read="Ler em outro idioma:", help="Ajuda gratuita, sem julgamento.",
  nocookie="Este site não usa cookies nem coleta dados pessoais — o Cloudflare conta apenas visualizações anônimas de página.",
  free="Livre para imprimir, copiar, traduzir e compartilhar. Não é preciso permissão.",
  langpage="Ajuda no seu idioma", skip="Ir para o conteúdo principal",
  navhome="Início", navscams="Tipos de golpe", navprint="Materiais para impressão",
  navabout="Sobre", navtalk="Dê esta palestra", navhelp="Ajude a traduzir",
  navprivacy="Privacidade", navterms="Termos", navblog="Blog",
  railtitle="Acesso rápido", s_romance="Alguém que conheci on-line",
  s_tech="Suporte técnico falso", s_bank="Banco / “hacker fantasma”",
  s_gov="Falsa autoridade governamental", s_grandparent="Neto em apuros",
  s_kidnap="Sequestro virtual", s_signs="Três sinais de alerta")
UI["pl"] = dict(strap="Rozłącz się. Sam sprawdź numer. Poczekaj dzień.",
  back="← Powrót do początku", read="Czytaj w innym języku:", help="Bezpłatna pomoc, bez oceniania.",
  nocookie="Ta strona nie używa plików cookie i nie zbiera danych osobowych — Cloudflare liczy tylko anonimowe wyświetlenia stron.",
  free="Można swobodnie drukować, kopiować, tłumaczyć i udostępniać. Zgoda nie jest potrzebna.",
  langpage="Pomoc w Twoim języku", skip="Przejdź do głównej treści",
  navhome="Strona główna", navscams="Rodzaje oszustw", navprint="Materiały do druku",
  navabout="O nas", navtalk="Wygłoś tę prelekcję", navhelp="Pomóż w tłumaczeniu",
  navprivacy="Prywatność", navterms="Warunki", navblog="Blog",
  railtitle="Szybka nawigacja", s_romance="Osoba poznana w internecie",
  s_tech="Fałszywe wsparcie techniczne", s_bank="Bank / „hacker widmo”",
  s_gov="Podszywanie się pod urząd", s_grandparent="Wnuk w tarapatach",
  s_kidnap="Wirtualne porwanie", s_signs="Trzy sygnały ostrzegawcze")
UI["ro"] = dict(strap="Închideți. Căutați numărul singur. Așteptați o zi.",
  back="← Înapoi la început", read="Citiți în altă limbă:", help="Ajutor gratuit, fără judecată.",
  nocookie="Acest site nu folosește cookie-uri și nu colectează date personale — Cloudflare numără doar vizualizări anonime de pagină.",
  free="Liber de tipărit, copiat, tradus și distribuit. Nu e nevoie de permisiune.",
  langpage="Ajutor în limba dumneavoastră", skip="Sari la conținutul principal",
  navhome="Acasă", navscams="Tipuri de escrocherii", navprint="Materiale de tipărit",
  navabout="Despre noi", navtalk="Susțineți această prezentare", navhelp="Ajutați la traducere",
  navprivacy="Confidențialitate", navterms="Termeni", navblog="Blog",
  railtitle="Navigare rapidă", s_romance="Cineva cunoscut online",
  s_tech="Suport tehnic fals", s_bank="Bancă / „hacker fantomă”",
  s_gov="Impersonarea unei instituții publice", s_grandparent="Nepot aflat în necaz",
  s_kidnap="Răpire virtuală", s_signs="Trei semne de avertizare")
UI["uk"] = dict(strap="Покладіть слухавку. Знайдіть номер самостійно. Зачекайте день.",
  back="← Повернутися на початок", read="Читати іншою мовою:", help="Безкоштовна допомога, без осуду.",
  nocookie="Цей сайт не використовує файли cookie і не збирає особисті дані — Cloudflare рахує лише анонімні перегляди сторінок.",
  free="Можна вільно друкувати, копіювати, перекладати та передавати іншим. Дозвіл не потрібен.",
  langpage="Допомога вашою мовою", skip="Перейти до основного вмісту",
  navhome="Головна", navscams="Види шахрайства", navprint="Друковані матеріали",
  navabout="Про нас", navtalk="Провести цю бесіду", navhelp="Допомогти з перекладом",
  navprivacy="Конфіденційність", navterms="Умови", navblog="Блог",
  railtitle="Швидка навігація", s_romance="Людина, зустрінута онлайн",
  s_tech="Фальшива технічна підтримка", s_bank="Банк / «хакер-привид»",
  s_gov="Видавання себе за державну установу", s_grandparent="Онук у біді",
  s_kidnap="Віртуальне викрадення", s_signs="Три тривожні ознаки")
UI["id"] = dict(strap="Tutup telepon. Cari sendiri nomornya. Tunggu satu hari.",
  back="← Kembali ke awal", read="Baca dalam bahasa lain:", help="Bantuan gratis, tanpa menghakimi.",
  nocookie="Situs ini tidak memasang cookie dan tidak mengumpulkan data pribadi — Cloudflare hanya menghitung kunjungan halaman anonim.",
  free="Bebas dicetak, disalin, diterjemahkan, dan dibagikan. Tidak perlu izin.",
  langpage="Bantuan dalam bahasa Anda", skip="Langsung ke konten utama",
  navhome="Beranda", navscams="Jenis penipuan", navprint="Materi cetak",
  navabout="Tentang kami", navtalk="Bawakan ceramah ini", navhelp="Bantu menerjemahkan",
  navprivacy="Privasi", navterms="Ketentuan", navblog="Blog",
  railtitle="Navigasi cepat", s_romance="Orang yang ditemui secara online",
  s_tech="Dukungan teknis palsu", s_bank="Bank / “peretas hantu”",
  s_gov="Penyamaran sebagai pemerintah", s_grandparent="Cucu dalam masalah",
  s_kidnap="Penculikan virtual", s_signs="Tiga tanda peringatan")
UI["ht"] = dict(strap="Rakwoche. Chèche nimewo a ou menm. Tann yon jou.",
  back="← Retounen nan kòmansman", read="Li sa nan yon lòt lang:", help="Èd gratis, san jijman.",
  nocookie="Sit sa a pa mete okenn cookie e li pa kolekte okenn done pèsonèl — Cloudflare sèlman konte vizit paj anonim.",
  free="Ou lib pou enprime, kopye, tradui, epi pataje. Pa bezwen pèmisyon.",
  langpage="Èd nan lang ou", skip="Ale dirèkteman nan kontni prensipal la",
  navhome="Akèy", navscams="Kalite eskrokri", navprint="Materyèl pou enprime",
  navabout="Konsènan nou", navtalk="Bay prezantasyon sa a", navhelp="Ede tradui",
  navprivacy="Konfidansyalite", navterms="Kondisyon", navblog="Blòg",
  railtitle="Navigasyon rapid", s_romance="Yon moun mwen rankontre sou entènèt",
  s_tech="Fo sipò teknik", s_bank="Bank / “ajan pirat fantom”",
  s_gov="Moun k ap fè tankou gouvènman", s_grandparent="Pitit pitit nan tras",
  s_kidnap="Kidnapin vityèl", s_signs="Twa siy avètisman")
UI["pa"] = dict(strap="ਫ਼ੋਨ ਰੱਖੋ। ਨੰਬਰ ਖੁਦ ਲੱਭੋ। ਇੱਕ ਦਿਨ ਉਡੀਕ ਕਰੋ।",
  back="← ਸ਼ੁਰੂਆਤ ਵੱਲ ਵਾਪਸ", read="ਇਸ ਨੂੰ ਹੋਰ ਭਾਸ਼ਾ ਵਿੱਚ ਪੜ੍ਹੋ:", help="ਮੁਫ਼ਤ ਮਦਦ, ਬਿਨਾਂ ਕਿਸੇ ਨਿਰਣੇ ਦੇ।",
  nocookie="ਇਹ ਸਾਈਟ ਕੋਈ ਕੂਕੀ ਨਹੀਂ ਰੱਖਦੀ ਅਤੇ ਕੋਈ ਨਿੱਜੀ ਜਾਣਕਾਰੀ ਇਕੱਠੀ ਨਹੀਂ ਕਰਦੀ — Cloudflare ਸਿਰਫ਼ ਗੁਮਨਾਮ ਪੇਜ ਵਿਊ ਗਿਣਦਾ ਹੈ।",
  free="ਖੁੱਲ੍ਹ ਕੇ ਛਾਪੋ, ਕਾਪੀ ਕਰੋ, ਅਨੁਵਾਦ ਕਰੋ ਅਤੇ ਸਾਂਝਾ ਕਰੋ। ਇਜਾਜ਼ਤ ਦੀ ਲੋੜ ਨਹੀਂ।",
  langpage="ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਵਿੱਚ ਮਦਦ", skip="ਮੁੱਖ ਸਮੱਗਰੀ 'ਤੇ ਜਾਓ",
  navhome="ਹੋਮ", navscams="ਧੋਖਾਧੜੀ ਦੀਆਂ ਕਿਸਮਾਂ", navprint="ਛਪਾਈ ਸਮੱਗਰੀ",
  navabout="ਸਾਡੇ ਬਾਰੇ", navtalk="ਇਹ ਗੱਲਬਾਤ ਦਿਓ", navhelp="ਅਨੁਵਾਦ ਵਿੱਚ ਮਦਦ ਕਰੋ",
  navprivacy="ਪਰਦੇਦਾਰੀ", navterms="ਸ਼ਰਤਾਂ", navblog="ਬਲੌਗ",
  railtitle="ਤੁਰੰਤ ਨੇਵੀਗੇਸ਼ਨ", s_romance="ਆਨਲਾਈਨ ਮਿਲਿਆ ਕੋਈ ਵਿਅਕਤੀ",
  s_tech="ਨਕਲੀ ਤਕਨੀਕੀ ਸਹਾਇਤਾ", s_bank="ਬੈਂਕ / “ਭੂਤ ਹੈਕਰ”",
  s_gov="ਸਰਕਾਰ ਦਾ ਢੌਂਗ", s_grandparent="ਪੋਤਾ-ਪੋਤੀ ਮੁਸੀਬਤ ਵਿੱਚ",
  s_kidnap="ਵਰਚੁਅਲ ਅਗਵਾ", s_signs="ਤਿੰਨ ਚੇਤਾਵਨੀ ਸੰਕੇਤ")
UI["gu"] = dict(strap="ફોન મૂકી દો. નંબર જાતે શોધો. એક દિવસ રાહ જુઓ.",
  back="← શરૂઆતમાં પાછા", read="આ બીજી ભાષામાં વાંચો:", help="મફત મદદ, કોઈ ટીકા નહીં.",
  nocookie="આ સાઇટ કોઈ કૂકી સેટ કરતી નથી અને કોઈ અંગત માહિતી એકત્ર કરતી નથી — Cloudflare ફક્ત અનામી પેજવ્યુ ગણે છે.",
  free="મુક્તપણે છાપો, નકલ કરો, અનુવાદ કરો અને શેર કરો. પરવાનગીની જરૂર નથી.",
  langpage="તમારી ભાષામાં મદદ", skip="મુખ્ય સામગ્રી પર જાઓ",
  navhome="હોમ", navscams="છેતરપિંડીના પ્રકારો", navprint="પ્રિન્ટ સામગ્રી",
  navabout="અમારા વિશે", navtalk="આ વાત આપો", navhelp="અનુવાદમાં મદદ કરો",
  navprivacy="ગોપનીયતા", navterms="શરતો", navblog="બ્લોગ",
  railtitle="ઝડપી માર્ગદર્શન", s_romance="ઓનલાઇન મળેલ કોઈ વ્યક્તિ",
  s_tech="નકલી ટેક સપોર્ટ", s_bank="બેંક / “ભૂત હેકર”",
  s_gov="સરકારનો ઢોંગ", s_grandparent="પૌત્ર-પૌત્રી મુશ્કેલીમાં",
  s_kidnap="વર્ચ્યુઅલ અપહરણ", s_signs="ત્રણ ચેતવણી ચિહ્નો")
UI["so"] = dict(strap="Xidh taleefanka. Naambarka adigu raadi. Maalin sug.",
  back="← Ku laabo bilowga", read="Ku akhri luqad kale:", help="Caawimaad bilaash ah, aan xukun lahayn.",
  nocookie="Boggan ma dejiyo cookies-na, mana ururiyo xog shakhsi ah — Cloudflare wuxuu tirinayaa oo keliya booqasho aan la aqoonsan.",
  free="Xor u ah in la daabaco, la koobiyeeyo, la tarjumo, oo la wadaago. Ma loo baahna ogolaansho.",
  langpage="Caawimaad luqaddaada", skip="U gudub qaybta ugu muhiimsan",
  navhome="Bogga hore", navscams="Noocyada khiyaanada", navprint="Waraaqaha daabacan",
  navabout="Nagu saabsan", navtalk="Bixi hadalkan", navhelp="Ka caawi tarjumaadda",
  navprivacy="Asturnaanta", navterms="Shuruudaha", navblog="Blog-ga",
  railtitle="Wax degdeg ah u gaar", s_romance="Qof aan online kula kulmay",
  s_tech="Taageero farsamo oo been ah", s_bank="Bank / “hacker-ka ekaanta”",
  s_gov="Iska dhigid dowlad", s_grandparent="Awoowe/Ayeeyo dhibaato ku jira",
  s_kidnap="Afduub aan dhab ahayn", s_signs="Saddex calaamadood oo digniin ah")
UI["km"] = dict(strap="ដាក់ទូរស័ព្ទចុះ។ ស្វែងរកលេខដោយខ្លួនឯង។ រង់ចាំមួយថ្ងៃ។",
  back="← ត្រឡប់ទៅដើម", read="អានជាភាសាផ្សេង៖", help="ជំនួយឥតគិតថ្លៃ គ្មានការវិនិច្ឆ័យ។",
  nocookie="គេហទំព័រនេះមិនប្រើខូគី ហើយមិនប្រមូលទិន្នន័យផ្ទាល់ខ្លួនឡើយ — Cloudflare រាប់តែចំនួនអ្នកចូលមើលអនាមិកប៉ុណ្ណោះ។",
  free="សេរីក្នុងការបោះពុម្ព ថតចម្លង បកប្រែ និងចែករំលែក។ មិនចាំបាច់សុំការអនុញ្ញាតទេ។",
  langpage="ជំនួយជាភាសារបស់អ្នក", skip="រំលងទៅមាតិកាចម្បង",
  navhome="ទំព័រដើម", navscams="ប្រភេទឧបាយកល", navprint="ឯកសារបោះពុម្ព",
  navabout="អំពីយើង", navtalk="ធ្វើការនិយាយនេះ", navhelp="ជួយបកប្រែ",
  navprivacy="ឯកជនភាព", navterms="លក្ខខណ្ឌ", navblog="ប្លុក",
  railtitle="រុករកលឿន", s_romance="អ្នកដែលបានស្គាល់តាមអនឡាញ",
  s_tech="ជំនួយបច្ចេកទេសក្លែងក្លាយ", s_bank="ធនាគារ / “ហេគឃ័រខ្មោច”",
  s_gov="ក្លែងបន្លំជាអាជ្ញាធររដ្ឋ", s_grandparent="ចៅជួបបញ្ហា",
  s_kidnap="ការចាប់ជំរិតតាមប្រព័ន្ធអនឡាញ", s_signs="សញ្ញាព្រមានបី")
UI["hmn"] = dict(strap="Tso tais xov tooj. Tus kheej mus tshawb tus najnpawb. Tos ib hnub.",
  back="← Rov qab mus rau qhov pib", read="Nyeem qhov no ua lwm hom lus:", help="Pab dawb, tsis txiav txim.",
  nocookie="Lub vev xaib no tsis siv cookies thiab tsis sau tej ntaub ntawv ntiag tug — Cloudflare tsuas suav tus naj npawb neeg saib nkaus xwb, tsis paub yog leej twg.",
  free="Muaj cai luam tawm, luam theej duab, txhais lus, thiab qhia rau lwm tus. Tsis tas yuav tau kev tso cai.",
  langpage="Kev pab hauv koj hom lus", skip="Hla mus rau cov ntsiab lus tseem ceeb",
  navhome="Tsev", navscams="Hom kev dag ntxias", navprint="Cov ntaub ntawv luam tawm",
  navabout="Txog peb", navtalk="Muab zaj lus qhia no", navhelp="Pab txhais lus",
  navprivacy="Kev ceev ntiag tug", navterms="Cov cai", navblog="Blog",
  railtitle="Nrhiav sai", s_romance="Ib tug neeg uas ntsib hauv online",
  s_tech="Kev pab txuas ntxiv cuav", s_bank="Tuam txhab nyiaj / “dab hacker”",
  s_gov="Ua txuj yog tsoomfwv", s_grandparent="Xeeb ntxwv raug teeb meem",
  s_kidnap="Kev txeeb neeg cuav", s_signs="Peb lub cim ceeb toom")
UI["ka"] = dict(strap="დადეთ ყურმილი. თავად მოძებნეთ ნომერი. დაელოდეთ ერთ დღეს.",
  back="← დაბრუნება დასაწყისში", read="წაიკითხეთ სხვა ენაზე:", help="უფასო დახმარება, განსჯის გარეშე.",
  nocookie="ეს საიტი არ იყენებს cookie-ებს და არ აგროვებს პირად მონაცემებს — Cloudflare მხოლოდ ანონიმურ ნახვებს ითვლის.",
  free="თავისუფლად დაბეჭდეთ, დააკოპირეთ, თარგმნეთ და გაუზიარეთ. ნებართვა არ არის საჭირო.",
  langpage="დახმარება თქვენს ენაზე", skip="გადადით მთავარ კონტენტზე",
  navhome="მთავარი", navscams="თაღლითობის სახეები", navprint="საბეჭდი მასალები",
  navabout="ჩვენ შესახებ", navtalk="ჩაატარეთ ეს საუბარი", navhelp="დაეხმარეთ თარგმანს",
  navprivacy="კონფიდენციალურობა", navterms="პირობები", navblog="ბლოგი",
  railtitle="სწრაფი ნავიგაცია", s_romance="ინტერნეტში გაცნობილი ადამიანი",
  s_tech="ყალბი ტექნიკური მხარდაჭერა", s_bank="ბანკი / „მოჩვენება ჰაკერი“",
  s_gov="სახელმწიფო უწყების იმიტაცია", s_grandparent="შვილიშვილი გასაჭირშია",
  s_kidnap="ვირტუალური გატაცება", s_signs="სამი გამაფრთხილებელი ნიშანი")
UI["lt"] = dict(strap="Padėkite ragelį. Numerį susiraskite patys. Palaukite dieną.",
  back="← Atgal į pradžią", read="Skaityti kita kalba:", help="Nemokama pagalba, be jokio vertinimo.",
  nocookie="Ši svetainė nenaudoja slapukų ir nerenka jokių asmens duomenų — „Cloudflare“ skaičiuoja tik anoniminius apsilankymus.",
  free="Galima laisvai spausdinti, kopijuoti, versti ir dalintis. Leidimo nereikia.",
  langpage="Pagalba jūsų kalba", skip="Pereiti prie pagrindinio turinio",
  navhome="Pradžia", navscams="Sukčiavimo rūšys", navprint="Spausdinami leidiniai",
  navabout="Apie mus", navtalk="Praveskite šį pokalbį", navhelp="Padėkite versti",
  navprivacy="Privatumas", navterms="Sąlygos", navblog="Tinklaraštis",
  railtitle="Greita naršymas", s_romance="Internete sutiktas žmogus",
  s_tech="Netikra techninė pagalba", s_bank="Bankas / „vaiduoklis įsilaužėlis“",
  s_gov="Apsimetimas valstybine įstaiga", s_grandparent="Anūkas bėdoje",
  s_kidnap="Virtualus pagrobimas", s_signs="Trys įspėjamieji ženklai")
UI["lv"] = dict(strap="Nolieciet klausuli. Pats atrodiet numuru. Pagaidiet dienu.",
  back="← Atpakaļ uz sākumu", read="Lasīt citā valodā:", help="Bezmaksas palīdzība, bez nosodījuma.",
  nocookie="Šī vietne neizmanto sīkfailus un nevāc personas datus — Cloudflare skaita tikai anonīmus lapas apmeklējumus.",
  free="Brīvi drukājiet, kopējiet, tulkojiet un dalieties. Atļauja nav vajadzīga.",
  langpage="Palīdzība jūsu valodā", skip="Pāriet uz galveno saturu",
  navhome="Sākums", navscams="Krāpšanas veidi", navprint="Drukājamie materiāli",
  navabout="Par mums", navtalk="Novadiet šo lekciju", navhelp="Palīdziet tulkot",
  navprivacy="Privātums", navterms="Noteikumi", navblog="Emuārs",
  railtitle="Ātrā navigācija", s_romance="Kāds, ko iepazinu tiešsaistē",
  s_tech="Viltus tehniskais atbalsts", s_bank="Banka / „spoku hakeris”",
  s_gov="Izlikšanās par valsts iestādi", s_grandparent="Mazbērns nepatikšanās",
  s_kidnap="Virtuāla nolaupīšana", s_signs="Trīs brīdinājuma pazīmes")
UI["et"] = dict(strap="Pange toru hargile. Otsige number ise üles. Oodake üks päev.",
  back="← Tagasi algusesse", read="Loe teises keeles:", help="Tasuta abi, ilma hukka mõistmata.",
  nocookie="See sait ei kasuta küpsiseid ega kogu isikuandmeid — Cloudflare loeb ainult anonüümseid lehevaatamisi.",
  free="Vabalt trükitav, kopeeritav, tõlgitav ja teistega jagatav. Luba pole vaja.",
  langpage="Abi teie keeles", skip="Liigu põhisisu juurde",
  navhome="Avaleht", navscams="Pettuste liigid", navprint="Trükimaterjalid",
  navabout="Meist", navtalk="Pidage seda vestlust", navhelp="Aidake tõlkida",
  navprivacy="Privaatsus", navterms="Tingimused", navblog="Blogi",
  railtitle="Kiirvalik", s_romance="Keegi, kellega tutvusin internetis",
  s_tech="Võlts tehniline tugi", s_bank="Pank / „fantoomhäkker”",
  s_gov="Riigiasutuse teesklemine", s_grandparent="Lapselaps hädas",
  s_kidnap="Virtuaalne inimrööv", s_signs="Kolm hoiatusmärki")
UI["it"] = dict(strap="Riagganciate. Cercate voi stessi il numero. Aspettate un giorno.",
  back="← Torna all'inizio", read="Leggi in un'altra lingua:", help="Aiuto gratuito, senza giudizio.",
  nocookie="Questo sito non utilizza cookie e non raccoglie dati personali — Cloudflare conta solo visualizzazioni di pagina anonime.",
  free="Libero da stampare, copiare, tradurre e condividere. Non serve alcun permesso.",
  langpage="Aiuto nella tua lingua", skip="Vai al contenuto principale",
  navhome="Home", navscams="Tipi di truffa", navprint="Materiali stampabili",
  navabout="Chi siamo", navtalk="Tieni questa presentazione", navhelp="Aiuta a tradurre",
  navprivacy="Privacy", navterms="Termini", navblog="Blog",
  railtitle="Accesso rapido", s_romance="Qualcuno conosciuto online",
  s_tech="Falso supporto tecnico", s_bank="Banca / “hacker fantasma”",
  s_gov="Finto ente governativo", s_grandparent="Nipote nei guai",
  s_kidnap="Sequestro virtuale", s_signs="Tre segnali d'allarme")
UI["el"] = dict(strap="Κλείστε το τηλέφωνο. Βρείτε μόνοι σας τον αριθμό. Περιμένετε μία μέρα.",
  back="← Επιστροφή στην αρχή", read="Διαβάστε σε άλλη γλώσσα:", help="Δωρεάν βοήθεια, χωρίς κριτική.",
  nocookie="Αυτός ο ιστότοπος δεν χρησιμοποιεί cookies και δεν συλλέγει προσωπικά δεδομένα — το Cloudflare μετρά μόνο ανώνυμες προβολές σελίδας.",
  free="Ελεύθερο για εκτύπωση, αντιγραφή, μετάφραση και διάδοση. Δεν χρειάζεται άδεια.",
  langpage="Βοήθεια στη γλώσσα σας", skip="Μετάβαση στο κύριο περιεχόμενο",
  navhome="Αρχική", navscams="Τύποι απάτης", navprint="Έντυπο υλικό",
  navabout="Σχετικά", navtalk="Παρουσιάστε αυτή την ομιλία", navhelp="Βοηθήστε στη μετάφραση",
  navprivacy="Απόρρητο", navterms="Όροι", navblog="Ιστολόγιο",
  railtitle="Γρήγορη πλοήγηση", s_romance="Κάποιος που γνώρισα online",
  s_tech="Ψεύτικη τεχνική υποστήριξη", s_bank="Τράπεζα / «φάντασμα χάκερ»",
  s_gov="Υποδυόμενος κρατική υπηρεσία", s_grandparent="Εγγόνι σε μπελά",
  s_kidnap="Εικονική απαγωγή", s_signs="Τρία προειδοποιητικά σημάδια")
UI["he"] = dict(strap="נתקו את השיחה. חפשו את המספר בעצמכם. חכו יום אחד.",
  back="← חזרה להתחלה", read="קראו בשפה אחרת:", help="עזרה חינמית, בלי שיפוטיות.",
  nocookie="האתר הזה לא משתמש בעוגיות ולא אוסף מידע אישי — Cloudflare סופרת רק צפיות אנונימיות בדפים.",
  free="מותר להדפיס, להעתיק, לתרגם ולהעביר הלאה בחופשיות. אין צורך באישור.",
  langpage="עזרה בשפה שלכם", skip="דלגו לתוכן הראשי",
  navhome="בית", navscams="סוגי הונאות", navprint="חומרים להדפסה",
  navabout="אודות", navtalk="תנו את ההרצאה הזו", navhelp="עזרו בתרגום",
  navprivacy="פרטיות", navterms="תנאים", navblog="בלוג",
  railtitle="ניווט מהיר", s_romance="מישהו שהכרתי באינטרנט",
  s_tech="תמיכה טכנית מזויפת", s_bank="בנק / “האקר רוח רפאים”",
  s_gov="התחזות לרשות ממשלתית", s_grandparent="נכד בצרה",
  s_kidnap="חטיפה וירטואלית", s_signs="שלושה סימני אזהרה")
UI["hu"] = dict(strap="Tegye le a telefont. Nézze meg saját maga a számot. Várjon egy napot.",
  back="← Vissza a kezdéshez", read="Olvassa más nyelven:", help="Ingyenes segítség, ítélkezés nélkül.",
  nocookie="Ez az oldal nem használ sütiket és nem gyűjt személyes adatokat — a Cloudflare csak névtelen oldalmegtekintéseket számol.",
  free="Szabadon nyomtatható, másolható, fordítható és megosztható. Nincs szükség engedélyre.",
  langpage="Segítség az Ön nyelvén", skip="Ugrás a fő tartalomra",
  navhome="Kezdőlap", navscams="Csalástípusok", navprint="Nyomtatható anyagok",
  navabout="Rólunk", navtalk="Tartsa meg ezt az előadást", navhelp="Segítsen a fordításban",
  navprivacy="Adatvédelem", navterms="Feltételek", navblog="Blog",
  railtitle="Gyors navigáció", s_romance="Valaki, akit online ismertem meg",
  s_tech="Hamis műszaki támogatás", s_bank="Bank / „szellemhacker”",
  s_gov="Kormányzati szerv megszemélyesítése", s_grandparent="Unoka bajban",
  s_kidnap="Virtuális emberrablás", s_signs="Három figyelmeztető jel")
UI["hr"] = dict(strap="Spustite slušalicu. Sami provjerite broj. Pričekajte jedan dan.",
  back="← Natrag na početak", read="Pročitajte na drugom jeziku:", help="Besplatna pomoć, bez osuđivanja.",
  nocookie="Ova stranica ne postavlja kolačiće i ne prikuplja osobne podatke — Cloudflare broji samo anonimne posjete stranici.",
  free="Slobodno ispišite, kopirajte, prevedite i podijelite. Dopuštenje nije potrebno.",
  langpage="Pomoć na vašem jeziku", skip="Idi na glavni sadržaj",
  navhome="Početna", navscams="Vrste prijevara", navprint="Materijali za ispis",
  navabout="O nama", navtalk="Održite ovo predavanje", navhelp="Pomozite s prijevodom",
  navprivacy="Privatnost", navterms="Uvjeti", navblog="Blog",
  railtitle="Brza navigacija", s_romance="Netko koga sam upoznao/la online",
  s_tech="Lažna tehnička podrška", s_bank="Banka / „hakerska sablast”",
  s_gov="Lažno predstavljanje državne institucije", s_grandparent="Unuk u nevolji",
  s_kidnap="Virtualna otmica", s_signs="Tri znaka upozorenja")
UI["sr"] = dict(strap="Спустите слушалицу. Сами проверите број. Сачекајте један дан.",
  back="← Назад на почетак", read="Прочитајте на другом језику:", help="Бесплатна помоћ, без осуђивања.",
  nocookie="Овај сајт не поставља колачиће и не прикупља личне податке — Cloudflare броји само анонимне посете страници.",
  free="Слободно штампајте, копирајте, преводите и делите. Дозвола није потребна.",
  langpage="Помоћ на вашем језику", skip="Иди на главни садржај",
  navhome="Почетна", navscams="Врсте превара", navprint="Материјали за штампу",
  navabout="О нама", navtalk="Одржите ово предавање", navhelp="Помозите у превођењу",
  navprivacy="Приватност", navterms="Услови", navblog="Блог",
  railtitle="Брза навигација", s_romance="Неко ко упознат онлајн",
  s_tech="Лажна техничка подршка", s_bank="Банка / „хакер-дух”",
  s_gov="Лажно представљање државне институције", s_grandparent="Унук у невољи",
  s_kidnap="Виртуелна отмица", s_signs="Три знака упозорења")
UI["ms"] = dict(strap="Letak telefon. Cari sendiri nombor itu. Tunggu sehari.",
  back="← Kembali ke permulaan", read="Baca dalam bahasa lain:", help="Bantuan percuma, tanpa menghakimi.",
  nocookie="Laman ini tidak menetapkan kuki dan tidak mengumpul data peribadi — Cloudflare hanya mengira paparan halaman tanpa nama.",
  free="Bebas untuk dicetak, disalin, diterjemah, dan dikongsi. Tiada keizinan diperlukan.",
  langpage="Bantuan dalam bahasa anda", skip="Langkau ke kandungan utama",
  navhome="Laman utama", navscams="Jenis penipuan", navprint="Bahan cetak",
  navabout="Tentang kami", navtalk="Sampaikan ceramah ini", navhelp="Bantu terjemah",
  navprivacy="Privasi", navterms="Terma", navblog="Blog",
  railtitle="Navigasi pantas", s_romance="Seseorang yang ditemui secara dalam talian",
  s_tech="Sokongan teknikal palsu", s_bank="Bank / “penggodam hantu”",
  s_gov="Penyamaran kerajaan", s_grandparent="Cucu dalam masalah",
  s_kidnap="Penculikan maya", s_signs="Tiga tanda amaran")
UI["sv"] = dict(strap="Lägg på. Slå upp numret själv. Vänta en dag.",
  back="← Tillbaka till start", read="Läs på ett annat språk:", help="Gratis hjälp, utan att döma.",
  nocookie="Den här webbplatsen sätter inga kakor och samlar inte in några personuppgifter — Cloudflare räknar bara anonyma sidvisningar.",
  free="Fritt att skriva ut, kopiera, översätta och dela vidare. Inget tillstånd behövs.",
  langpage="Hjälp på ditt språk", skip="Hoppa till huvudinnehållet",
  navhome="Hem", navscams="Bedrägerityper", navprint="Utskriftsmaterial",
  navabout="Om oss", navtalk="Håll den här presentationen", navhelp="Hjälp till att översätta",
  navprivacy="Integritet", navterms="Villkor", navblog="Blogg",
  railtitle="Snabbnavigering", s_romance="Någon jag träffade online",
  s_tech="Falsk teknisk support", s_bank="Bank / ”spökhackare”",
  s_gov="Utger sig för att vara en myndighet", s_grandparent="Barnbarn i knipa",
  s_kidnap="Virtuell kidnappning", s_signs="Tre varningstecken")
UI["no"] = dict(strap="Legg på. Slå opp nummeret selv. Vent en dag.",
  back="← Tilbake til start", read="Les på et annet språk:", help="Gratis hjelp, uten å dømme.",
  nocookie="Dette nettstedet setter ingen informasjonskapsler og samler ikke inn personopplysninger — Cloudflare teller kun anonyme sidevisninger.",
  free="Fritt å skrive ut, kopiere, oversette og dele videre. Ingen tillatelse nødvendig.",
  langpage="Hjelp på ditt språk", skip="Hopp til hovedinnholdet",
  navhome="Hjem", navscams="Typer svindel", navprint="Utskriftsmateriell",
  navabout="Om oss", navtalk="Hold dette foredraget", navhelp="Hjelp til å oversette",
  navprivacy="Personvern", navterms="Vilkår", navblog="Blogg",
  railtitle="Hurtignavigasjon", s_romance="Noen jeg møtte på nettet",
  s_tech="Falsk teknisk støtte", s_bank="Bank / «spøkelseshacker»",
  s_gov="Utgir seg for å være myndighet", s_grandparent="Barnebarn i trøbbel",
  s_kidnap="Virtuell kidnapping", s_signs="Tre varselstegn")
UI["da"] = dict(strap="Læg på. Slå selv nummeret op. Vent en dag.",
  back="← Tilbage til start", read="Læs på et andet sprog:", help="Gratis hjælp, uden at dømme.",
  nocookie="Denne hjemmeside sætter ingen cookies og indsamler ingen personoplysninger — Cloudflare tæller kun anonyme sidevisninger.",
  free="Frit at printe, kopiere, oversætte og dele videre. Ingen tilladelse nødvendig.",
  langpage="Hjælp på dit sprog", skip="Spring til hovedindholdet",
  navhome="Hjem", navscams="Typer af svindel", navprint="Udskriftsmaterialer",
  navabout="Om os", navtalk="Hold dette oplæg", navhelp="Hjælp med at oversætte",
  navprivacy="Privatliv", navterms="Vilkår", navblog="Blog",
  railtitle="Hurtig navigation", s_romance="Nogen jeg mødte online",
  s_tech="Falsk teknisk support", s_bank="Bank / “spøgelseshacker”",
  s_gov="Udgiver sig for at være en myndighed", s_grandparent="Barnebarn i knibe",
  s_kidnap="Virtuel kidnapning", s_signs="Tre advarselstegn")
UI["sw"] = dict(strap="Kata simu. Tafuta nambari mwenyewe. Subiri siku moja.",
  back="← Rudi mwanzo", read="Soma kwa lugha nyingine:", help="Msaada wa bure, bila kuhukumu.",
  nocookie="Tovuti hii haiweki vidakuzi na haikusanyi taarifa binafsi — Cloudflare inahesabu tu watazamaji wa ukurasa wasiojulikana.",
  free="Huru kuchapisha, kunakili, kutafsiri, na kushiriki. Hakuna ruhusa inayohitajika.",
  langpage="Msaada kwa lugha yako", skip="Ruka hadi maudhui makuu",
  navhome="Nyumbani", navscams="Aina za ulaghai", navprint="Nyenzo za kuchapisha",
  navabout="Kutuhusu", navtalk="Toa mhadhara huu", navhelp="Saidia kutafsiri",
  navprivacy="Faragha", navterms="Masharti", navblog="Blogu",
  railtitle="Urambazaji wa haraka", s_romance="Mtu niliyekutana naye mtandaoni",
  s_tech="Msaada bandia wa kiufundi", s_bank="Benki / “hacker mzuka”",
  s_gov="Kujifanya ni serikali", s_grandparent="Mjukuu kwenye matatizo",
  s_kidnap="Utekaji wa kimtandao", s_signs="Ishara tatu za onyo")

# ---------------------------------------------------------------- front matter

def _unquote(v):
    """YAML-ish scalar: strip one layer of matching quotes and unescape \" inside.

    The front matter is parsed by hand rather than with a YAML library, so a
    title written as "\"There's a problem\"" arrived with its wrapping quotes
    still attached and rendered them into <title>. Titles that deliberately
    contain quotation marks need the wrapper; this removes it.
    """
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
        v = v[1:-1]
        if v and '\\' in v:
            v = v.replace('\\"', '"').replace("\\'", "'")
    return v


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
                    meta[k.strip()] = _unquote(v.strip())
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

# A magnifying glass with a checkmark inside — not a shield-and-checkmark,
# which reads as borrowed from antivirus/security-badge branding (McAfee,
# Norton, generic "verified" seals). This ties to the site's own two ideas
# instead: look it up yourself (the glass), then it checks out (the check).
MARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><circle cx="10" cy="10" r="6.75"/>'
        '<path d="M7.5 10 9.2 11.7 12.3 7.8"/>'
        '<path d="M15.1 15.1 20.5 20.5"/></svg>')

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

.table-scroll{overflow-x:auto;margin:1.3rem 0;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;min-width:26rem;margin:0;font-size:.98rem}
th,td{border:1px solid #bbb;padding:.55rem .6rem;text-align:left;vertical-align:top}
th{background:var(--band);font-weight:800;white-space:nowrap}
td a{white-space:nowrap}

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

.steps{margin:1.5rem 0;list-style:none;padding:0}
.steps .step-item{display:flex;gap:1.2rem;padding:1.15rem 0;border-top:2px solid var(--rule)}
.steps .step-item:first-child{border-top:none;padding-top:0}
.steps .step-num{flex:none;width:2.7rem;font-size:2.6rem;font-weight:800;
  line-height:.9;color:var(--accent);font-variant-numeric:tabular-nums}
.steps .step-body{flex:1 1 auto;min-width:0}
.steps .step-head{font-weight:800;font-size:1.14rem;line-height:1.35;margin:0}
.steps .step-desc{margin:.3rem 0 0;color:var(--muted)}
@media (max-width:26rem){
  .steps .step-item{gap:.8rem}
  .steps .step-num{width:2.1rem;font-size:2rem}
}

.audio-player{margin:1.1rem 0 1.6rem;padding:.9rem 1rem;border:2px solid var(--rule);
  border-radius:.4rem;background:var(--band)}
.audio-player strong{display:block;margin-bottom:.5rem}
.audio-player audio{width:100%;display:block}

figure.hero-photo{margin:1.1rem 0 1.6rem}
figure.hero-photo img{width:100%;aspect-ratio:16/9;object-fit:cover;
  border-radius:.4rem;display:block;background:var(--band)}
figure.hero-photo figcaption{font-size:.78rem;color:var(--muted);margin-top:.4rem}
figure.hero-photo figcaption a{color:var(--muted)}

.post-poster{max-width:280px;width:100%;float:right;margin:0 0 1rem 1.5rem;
  border:1px solid var(--rule)}
@media (max-width:520px){
  .post-poster{float:none;max-width:320px;margin:0 auto 1.2rem;display:block}
}

.eng-phrase{unicode-bidi:isolate;white-space:nowrap}

.feedback-form label{font-weight:700}
.feedback-form .hp{position:absolute;left:-9999px}
.feedback-form textarea,.feedback-form input[type=email]{
  border:3px solid var(--rule);border-radius:.3rem;margin-top:.4rem;
  background:var(--paper);color:var(--ink);width:100%;max-width:32rem;
  font:inherit;padding:.6rem;box-sizing:border-box}
.feedback-form textarea:focus,.feedback-form input[type=email]:focus{
  outline:none;border-color:var(--accent)}
.feedback-form button{
  font:inherit;font-weight:800;border:3px solid var(--rule);border-radius:.4rem;
  background:var(--accent);color:#fff;padding:.7rem 1.6rem;cursor:pointer}
.feedback-form button:hover,.feedback-form button:focus-visible{border-color:var(--ink)}

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
{hreflang}<meta name="robots" content="index,follow">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogimage}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{ogimage}">
<link rel="stylesheet" href="{pre}style.css">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<div class="shell"{dirattr}>
<aside class="rail" aria-label="{railtitle}">
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
  <nav class="sitenav" aria-label="Primary">
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
  <nav class="sitenav" aria-label="Footer">
    <a href="{pre}">{navhome}</a>
    <a href="{pre}about/">{navabout}</a>
    <a href="{pre}give-this-talk/">{navtalk}</a>
    <a href="{pre}blog/">{navblog}</a>
    <a href="{pre}help-translate/">{navhelp}</a>
    <a href="{pre}privacy/">{navprivacy}</a>
    <a href="{pre}terms/">{navterms}</a>
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
    body_html = re.sub(r'href="(/(?!/)[^"#]*)"', repl, body_html)

    def repl_src(m):
        return 'src="%s%s"' % (pre, m.group(1).lstrip("/"))
    return re.sub(r'src="(/(?!/)[^"]*)"', repl_src, body_html)


def phone_wrap(s):
    return re.sub(r"\b(8\d{2}-\d{3}-\d{4})\b",
                  lambda m: '<a class="tel" href="tel:+1%s">%s</a>' % (m.group(1).replace("-",""), m.group(1)), s)


def wrap_tables(s):
    # Wide tables (3+ real-content columns) don't fit 375px no matter how
    # the column widths are tuned -- forcing it just breaks words mid-
    # character ("reportfraud.ftc.gov" -> "reportf/raud.ft/c.gov"). A
    # horizontal-scroll container is the standard fix: the table keeps its
    # natural width and the page itself never scrolls sideways.
    return re.sub(r"(<table>.*?</table>)",
                  r'<div class="table-scroll">\1</div>', s, flags=re.S)


_STEP_RE = re.compile(r'<p><strong>(\d{1,2})\.\s*(.*?)</strong>\s*(.*?)</p>', re.S)


def numbered_steps(s):
    # The site's most-repeated content pattern -- "**1. Do this.** Because
    # why." -- is authored as plain markdown everywhere (the three steps,
    # warning-sign lists, every scam page's numbered advice). It's already
    # given real visual weight in the printed materials (giant numerals on
    # the fridge sheet and talk deck) but rendered as a bare bold sentence
    # on the site itself. Convert it to a numbered badge + heading +
    # description here, once, so every page using the pattern gets it --
    # not just home.md -- with no change needed to any content file.
    # <ol> + a real heading per step: screen-reader users get "list, 3
    # items" plus each step in the page's heading list, not just visual
    # weight. The big numeral is aria-hidden since the <li>'s own list
    # position already conveys the number -- otherwise it's announced twice.
    def item(m):
        num, head, desc = m.group(1), m.group(2).strip(), m.group(3).strip()
        desc_html = ('<p class="step-desc">%s</p>' % desc) if desc else ""
        return ('<li class="step-item"><div class="step-num" aria-hidden="true">%s</div>'
                '<div class="step-body"><h3 class="step-head">%s</h3>%s'
                '</div></li>') % (num, head, desc_html)

    s = _STEP_RE.sub(item, s)
    # Wrap runs of 2+ consecutive step-items (nothing but whitespace between
    # them) in a shared <ol>, so the border-top rules between items don't
    # also draw around an unrelated single "**1.**"-style bold sentence.
    return re.sub(r'(?:<li class="step-item">.*?</div></li>\s*){2,}',
                  lambda m: '<ol class="steps">' + m.group(0) + '</ol>',
                  s, flags=re.S)


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
            # slug_to_path() below only strips leading/trailing "/" -- a
            # "../" segment in frontmatter would otherwise let a build
            # write outside OUT entirely. Every real slug in this repo is
            # already lowercase letters/digits/-/_//,  so this is a strict
            # allowlist, not a guess at what to block.
            if not re.match(r'^/?[a-z0-9/_-]*$', slug):
                raise ValueError("Unsafe slug %r in %s" % (slug, src))
            pages.append((src, meta, body, lang, slug))

    # blog index: any content/en/blog/*.md other than blog.md itself.
    # Sorted newest first by the `date:` frontmatter field (ISO, so a
    # plain string sort works). Individual posts render like any other
    # page via the main loop below — nothing special-cased for those.
    def _blog_date_label(iso):
        try:
            return datetime.date.fromisoformat(iso).strftime("%B %-d, %Y")
        except ValueError:
            return iso

    blog_posts = sorted(
        (m for _src, m, _b, l, s in pages
         if l == "en" and s.strip("/").startswith("blog/")),
        key=lambda m: m.get("date", ""), reverse=True,
    )

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
        body_html = wrap_tables(body_html)
        body_html = numbered_steps(body_html)

        if lang == "en" and slug.strip("/") in PHOTOS:
            p = PHOTOS[slug.strip("/")]
            figure = (
                '<figure class="hero-photo">'
                '<img src="%sphotos/%s" alt="%s" fetchpriority="high">'
                '<figcaption>Photo: <a href="%s">%s</a> / Wikimedia Commons, %s</figcaption>'
                '</figure>'
            ) % (pre, p["file"], html.escape(p["alt"]), p["url"],
                 html.escape(p["author"]), p["license"])
            body_html = re.sub(r'(</h1>)', r'\1' + figure, body_html, count=1)

        if lang == "en" and slug.strip("/") in AUDIO_PAGES:
            audio_slug = (slug.strip("/") or "home").replace("/", "_")
            player = (
                '<p class="audio-player"><strong>%s</strong> '
                '<audio controls preload="none" src="%saudio/%s.mp3" '
                'aria-label="%s">'
                'Your browser doesn\'t support audio playback. '
                '<a href="%saudio/%s.mp3">Download the MP3</a> instead.'
                '</audio></p>'
            ) % (html.escape(ui(lang, "listen")), pre, audio_slug,
                 html.escape("Spoken version of: " + meta.get("title", "this page")),
                 pre, audio_slug)
            body_html = re.sub(r'(</h1>(?:\s*<figure class="hero-photo">.*?</figure>)?)',
                                r'\1' + player, body_html, count=1, flags=re.S)

        if lang == "en" and slug.strip("/") == "blog":
            if blog_posts:
                cards = "".join(
                    '<a class="card" href="%s%s/">%s<span>%s — %s</span></a>' % (
                        pre, m.get("slug", "").strip("/"),
                        html.escape(m.get("title", "")),
                        _blog_date_label(m.get("date", "")),
                        html.escape(m.get("description", "")),
                    )
                    for m in blog_posts
                )
                listing = '<div class="cards">' + cards + '</div>'
            else:
                listing = '<p><em>No posts yet — check back soon.</em></p>'
            body_html = re.sub(r'(</h1>)', r'\1' + listing, body_html, count=1)

        title = meta.get("title", "Trust But Verify")
        if slug.strip("/") not in ("", lang):
            title = "%s — Trust But Verify" % title

        # QAPage structured data for the questions/ pages — microdata, not a
        # <script type="application/ld+json"> block, because the site's own
        # CSP is default-src 'none' with no script-src exception, so a
        # <script> tag (any type, JSON-LD included) would just be dropped by
        # the browser. Microdata is plain HTML attributes: nothing to block.
        if re.match(r"^questions/", slug.strip("/") + "/"):
            body_html = (
                '<div itemscope itemtype="https://schema.org/QAPage">'
                '<div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">'
                '<meta itemprop="name" content="%s">'
                '<div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">'
                '<div itemprop="text">' % html.escape(meta.get("title", ""))
                + body_html + '</div></div></div></div>'
            )

        canonical = SITE + "/" + (outrel[:-len("index.html")]).replace(os.sep, "/")
        crumb = ("" if outrel == "index.html"
                 else '<p class="crumb"><a href="%s">← Back to the start</a></p>' % pre)
        og_rel = slug.strip("/") or "index"
        ogimage = SITE + "/og/" + og_rel.replace("/", "_") + ".png"

        # hreflang: only the 45 language landing pages are true translations
        # of each other. Deep content (scams/, questions/, talk/) exists in
        # English only, so pointing hreflang at it would misclaim a
        # translation that doesn't exist.
        hreflang = ""
        slug_bare = slug.strip("/")
        if slug_bare == "" or slug_bare == lang:
            tags = []
            for code, _short, _native in LANGS:
                href = SITE + "/" if code == "en" else "%s/%s/" % (SITE, code)
                tags.append('<link rel="alternate" hreflang="%s" href="%s">' % (code, href))
            tags.append('<link rel="alternate" hreflang="x-default" href="%s/">' % SITE)
            hreflang = "\n".join(tags) + "\n"

        page = PAGE.format(
            lang=lang,
            hreflang=hreflang,
            mark=MARK,
            dirattr=' dir="rtl"' if lang in RTL else "",
            title=html.escape(title),
            desc=html.escape(meta.get("description", "")),
            canonical=canonical,
            ogimage=ogimage,
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
            navprivacy=html.escape(ui(lang, "navprivacy")),
            navterms=html.escape(ui(lang, "navterms")),
            navblog=html.escape(ui(lang, "navblog")),
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
               '<circle cx="10" cy="10" r="7" fill="none" stroke="#123f7a" '
               'stroke-width="2.6"/>'
               '<path fill="none" stroke="#123f7a" stroke-width="2.6" '
               'stroke-linecap="round" stroke-linejoin="round" '
               'd="M7.5 10 9.2 11.7 12.3 7.8"/>'
               '<path fill="none" stroke="#123f7a" stroke-width="2.6" '
               'stroke-linecap="round" d="M15.1 15.1 20.5 20.5"/></svg>')
    open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8").write(favicon)

    # printables
    dest = os.path.join(OUT, "print")
    os.makedirs(dest, exist_ok=True)
    for fn in sorted(os.listdir(PRINT)):
        # .docx intentionally excluded: an editable file carrying the site's
        # branding is a tampering/impersonation risk. PDFs only.
        if fn.endswith(".pdf"):
            shutil.copy(os.path.join(PRINT, fn), os.path.join(dest, fn))

    # the talk deck — not editable-branded like the handout, a slide deck
    # being edited and re-shared doesn't carry the same impersonation risk
    talk_dir = os.path.join(ROOT, "formats", "talk")
    if os.path.isdir(talk_dir):
        for fn in sorted(os.listdir(talk_dir)):
            if fn.endswith(".pptx"):
                shutil.copy(os.path.join(talk_dir, fn), os.path.join(dest, fn))

    # social share cards (og:image) — committed, not built in CI; see
    # build/make_share_cards.py for why
    og_src = os.path.join(ROOT, "formats", "og")
    if os.path.isdir(og_src):
        og_dest = os.path.join(OUT, "og")
        os.makedirs(og_dest, exist_ok=True)
        for fn in sorted(os.listdir(og_src)):
            if fn.endswith(".png"):
                shutil.copy(os.path.join(og_src, fn), os.path.join(og_dest, fn))

    # hero photos (see PHOTOS above) -- committed under assets/photos/web/,
    # not regenerated in CI, same reasoning as og/ and print/
    photos_src = os.path.join(ROOT, "assets", "photos", "web")
    if os.path.isdir(photos_src):
        photos_dest = os.path.join(OUT, "photos")
        os.makedirs(photos_dest, exist_ok=True)
        for fn in sorted(os.listdir(photos_src)):
            if fn.endswith(".jpg"):
                shutil.copy(os.path.join(photos_src, fn), os.path.join(photos_dest, fn))

    # blog post images -- not sourced from Wikimedia Commons like the hero
    # photos above (a movie poster, used for editorial identification, not
    # covered by this site's CC BY-NC license), kept in a separate directory
    # so that distinction is obvious rather than mixed into photos/manifest.json
    blog_assets_src = os.path.join(ROOT, "assets", "blog")
    if os.path.isdir(blog_assets_src):
        blog_assets_dest = os.path.join(OUT, "blog-assets")
        os.makedirs(blog_assets_dest, exist_ok=True)
        for fn in sorted(os.listdir(blog_assets_src)):
            if fn.endswith(".jpg"):
                shutil.copy(os.path.join(blog_assets_src, fn), os.path.join(blog_assets_dest, fn))

    # pilot audio narration -- see build/make_audio.py and AUDIO_PAGES above
    audio_src = os.path.join(ROOT, "assets", "audio")
    if os.path.isdir(audio_src):
        audio_dest = os.path.join(OUT, "audio")
        os.makedirs(audio_dest, exist_ok=True)
        for fn in sorted(os.listdir(audio_src)):
            if fn.endswith(".mp3"):
                shutil.copy(os.path.join(audio_src, fn), os.path.join(audio_dest, fn))

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
        # media-src is required for the <audio> narration players. Without it
        # media falls back to default-src 'none' and every player is blocked
        # in every browser -- silently, apart from a console warning.
        "  Content-Security-Policy: default-src 'none'; style-src 'self'; img-src 'self'; "
        "media-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'\n"
        "  Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
        "\n/print/*\n  Cache-Control: public, max-age=86400\n"
        # The one page on the site with a <form>: same policy as everywhere
        # else, except form-action allows same-origin so the feedback form
        # can actually submit to /api/feedback.
        "\n/feedback/*\n"
        "  Content-Security-Policy: default-src 'none'; style-src 'self'; img-src 'self'; "
        "media-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'\n")

    # 404
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        PAGE.format(lang="en", dirattr="", mark=MARK, title="Page not found — Trust But Verify",
                    desc="That page isn't here.", canonical=SITE + "/404.html",
                    ogimage=SITE + "/og/index.png", pre="/", hreflang="",
                    crumb="",
                    body="<h1>That page isn't here.</h1>"
                         "<p>Nothing is wrong and you haven't broken anything. "
                         "The link may be old or mistyped.</p>"
                         "<p><a href=\"/\">Start from the beginning</a>, or if something "
                         "is happening right now and you need a person: "
                         "<strong>833-372-8311</strong>.</p>",
                    langs=lang_nav("/", "en"), langbtn="\U0001F310 " + lang_label("en"),
                    skip=UI["en"]["skip"], strap=UI["en"]["strap"],
                    helpline=UI["en"]["help"], langpage=UI["en"]["langpage"],
                    free=UI["en"]["free"], nocookie=UI["en"]["nocookie"],
                    railtitle=UI["en"]["railtitle"], navhome=UI["en"]["navhome"],
                    navscams=UI["en"]["navscams"], navprint=UI["en"]["navprint"],
                    navabout=UI["en"]["navabout"], navtalk=UI["en"]["navtalk"],
                    navhelp=UI["en"]["navhelp"], navprivacy=UI["en"]["navprivacy"],
                    navterms=UI["en"]["navterms"], navblog=UI["en"]["navblog"],
                    s_romance=UI["en"]["s_romance"],
                    s_tech=UI["en"]["s_tech"], s_bank=UI["en"]["s_bank"],
                    s_gov=UI["en"]["s_gov"], s_grandparent=UI["en"]["s_grandparent"],
                    s_kidnap=UI["en"]["s_kidnap"], s_signs=UI["en"]["s_signs"]))

    print("pages: %d" % written)
    print("output: %s" % OUT)


if __name__ == "__main__":
    build()
