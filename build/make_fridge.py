#!/usr/bin/env python3
"""Generate the large-print one-page fridge sheet in five languages."""
import os, html, subprocess
try:
    from weasyprint import HTML as _WeasyHTML
except Exception:
    _WeasyHTML = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "formats", "print")
os.makedirs(OUT, exist_ok=True)

# --- language data ---------------------------------------------------------

L = {}

L["en"] = dict(
    font="DejaVu Sans",
    brand="TRUST BUT VERIFY",
    tagline="You can stay trusting, but add a pause.",
    steps_head="BEFORE ANY MONEY MOVES",
    steps=[("Look up the number yourself.",
            "Not the number they gave you. The one on your card or statement."),
           ("Call the person yourself.",
            "Hang up first. If it was real, they'll still be there."),
           ("Wait a day.",
            "Real problems survive a night's sleep. Scams don't.")],
    signs_head="THREE SIGNS TO STOP",
    signs=["It came to you — you didn't start it.",
           "It moved you fast — fear, worry, or a deadline.",
           "It wants a transfer — money, a code, or your computer."],
    never_head="NEVER, NOT ONCE, NOT EVER",
    never=["Nobody legitimate is paid in gift cards.",
           "Your bank will never ask you to move money out of your bank.",
           "Never read a text code out loud. Not to anyone.",
           "Nobody comes to your home to collect cash, gold, or valuables."],
    help_head="FREE HELP — NO JUDGMENT",
    helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Mon–Fri 10–6 ET"),
           ("877-908-3360", "AARP Fraud Watch  ·  Mon–Fri 8–8 ET")],
    report="Report at ic3.gov  ·  reportfraud.ftc.gov",
    code_head="Our family's code word:",
    footline="If it already happened: it is not your fault, and it is not too late.",
    foot="Free to copy, print, and share.",
)

L["es"] = dict(
    font="DejaVu Sans",
    brand="CONFÍA, PERO VERIFICA",
    tagline="Puede seguir confiando, solo añada una pausa.",
    steps_head="ANTES DE MOVER CUALQUIER DINERO",
    steps=[("Busque el número usted mismo.",
            "No el que le dieron. El de su tarjeta o su estado de cuenta."),
           ("Llame usted mismo a la persona.",
            "Cuelgue primero. Si era real, ahí seguirán."),
           ("Espere un día.",
            "Los problemas reales sobreviven a una noche de sueño. Las estafas no.")],
    signs_head="TRES SEÑALES PARA DETENERSE",
    signs=["Vino hacia usted — usted no lo empezó.",
           "Le movió rápido — miedo, preocupación o prisa.",
           "Quiere una transferencia — dinero, un código o su computadora."],
    never_head="NUNCA, NI UNA SOLA VEZ",
    never=["Nadie legítimo cobra en tarjetas de regalo.",
           "Su banco nunca le pedirá sacar el dinero de su banco.",
           "Nunca lea en voz alta un código recibido por mensaje.",
           "Nadie va a su casa a recoger efectivo, oro ni objetos de valor."],
    help_head="AYUDA GRATUITA — SIN JUICIOS",
    helps=[("833-372-8311", "Línea Nacional de Fraude · Lun–Vie 10–6 ET"),
           ("877-908-3360", "AARP Fraud Watch · Lun–Vie 8–8 ET · en español")],
    report="Reporte en ic3.gov  ·  reportfraud.ftc.gov",
    code_head="La palabra clave de nuestra familia:",
    footline="Si ya ocurrió: no es culpa suya, y no es demasiado tarde.",
    foot="Libre de copiar, imprimir y compartir.",
)

L["vi"] = dict(
    font="DejaVu Sans",
    brand="TIN TƯỞNG, NHƯNG PHẢI KIỂM CHỨNG",
    tagline="Quý vị vẫn có thể tin tưởng, chỉ cần thêm một khoảng dừng.",
    steps_head="TRƯỚC KHI CHUYỂN BẤT KỲ KHOẢN TIỀN NÀO",
    steps=[("Tự mình tra số điện thoại.",
            "Không dùng số họ đưa. Dùng số trên thẻ hoặc sao kê của quý vị."),
           ("Tự mình gọi cho người đó.",
            "Cúp máy trước đã. Nếu là thật, họ vẫn ở đó."),
           ("Chờ một ngày.",
            "Chuyện thật thì qua một đêm vẫn còn. Lừa đảo thì không.")],
    signs_head="BA DẤU HIỆU PHẢI DỪNG LẠI",
    signs=["Nó tìm đến quý vị — không phải quý vị bắt đầu.",
           "Nó khiến quý vị xúc động nhanh — sợ hãi, lo lắng, gấp gáp.",
           "Nó muốn một sự chuyển giao — tiền, mã số, hoặc máy tính."],
    never_head="TUYỆT ĐỐI KHÔNG BAO GIỜ",
    never=["Không người đàng hoàng nào được trả bằng thẻ quà tặng.",
           "Ngân hàng không bao giờ bảo quý vị rút tiền ra khỏi ngân hàng.",
           "Không bao giờ đọc to mã số nhận qua tin nhắn.",
           "Không ai đến nhà quý vị lấy tiền mặt, vàng hay tài sản."],
    help_head="TRỢ GIÚP MIỄN PHÍ — KHÔNG PHÁN XÉT",
    helps=[("833-372-8311", "Đường dây Quốc gia · T2–T6, 10–6 ET"),
           ("877-908-3360", "AARP Fraud Watch · T2–T6, 8–8 ET")],
    report="Báo cáo tại ic3.gov  ·  reportfraud.ftc.gov  ·  có thông dịch",
    code_head="Từ khóa bí mật của gia đình chúng ta:",
    footline="Nếu đã xảy ra rồi: đó không phải lỗi của quý vị, và chưa quá muộn.",
    foot="Tự do sao chép, in ấn và chia sẻ.",
)

L["ru"] = dict(
    font="DejaVu Sans",
    brand="ДОВЕРЯЙ, НО ПРОВЕРЯЙ",
    tagline="Можно продолжать доверять — просто добавьте паузу.",
    steps_head="ПРЕЖДЕ ЧЕМ УЙДУТ ЛЮБЫЕ ДЕНЬГИ",
    steps=[("Найдите номер сами.",
            "Не тот, что дали они. Тот, что на вашей карте или в выписке."),
           ("Позвоните человеку сами.",
            "Сначала положите трубку. Если всё настоящее — они на месте."),
           ("Подождите сутки.",
            "Настоящая беда переживёт ночь. Мошенничество — нет.")],
    signs_head="ТРИ ПРИЗНАКА — ОСТАНОВИТЕСЬ",
    signs=["Оно пришло к вам — вы это не начинали.",
           "Вас быстро задело — страх, тревога или спешка.",
           "От вас хотят передачи — денег, кода или доступа к компьютеру."],
    never_head="НИКОГДА, НИ ЕДИНОГО РАЗА",
    never=["Никому законному не платят подарочными картами.",
           "Банк никогда не попросит вывести деньги из банка.",
           "Никогда не называйте вслух код из сообщения.",
           "Никто не приезжает к вам домой за наличными, золотом или ценностями."],
    help_head="БЕСПЛАТНАЯ ПОМОЩЬ — БЕЗ ОСУЖДЕНИЯ",
    helps=[("833-372-8311", "Национальная линия · Пн–Пт 10–18 (вост. время)"),
           ("877-908-3360", "AARP Fraud Watch · Пн–Пт 8–20 (вост. время)")],
    report="Сообщить: ic3.gov  ·  reportfraud.ftc.gov  ·  есть переводчик",
    code_head="Кодовое слово нашей семьи:",
    footline="Если уже случилось: это не ваша вина, и ещё не поздно.",
    foot="Свободно копировать, печатать и распространять.",
)

L["zh"] = dict(
    font="Noto Sans CJK SC",
    brand="信任，但要核实",
    tagline="您依然可以信任别人，只需多加一个停顿。",
    steps_head="在任何一笔钱转出去之前",
    steps=[("自己去查电话号码。",
            "不要用他们给的号码。用您卡片背面或账单上的号码。"),
           ("自己打电话给那个人。",
            "先挂断。如果是真的，对方还在那里。"),
           ("等一天。",
            "真事经得起睡一觉。骗局经不起。")],
    signs_head="三个信号，请停下",
    signs=["它是找上门来的——不是您先发起的。",
           "它让您瞬间情绪起伏——恐惧、担心或紧迫。",
           "它要的是一次转移——钱、验证码，或您的电脑。"],
    never_head="绝对不会，一次也不会",
    never=["没有任何正当机构收礼品卡。",
           "银行绝不会要求您把钱转出您的银行。",
           "绝不要把短信验证码念给任何人听。",
           "没有人会上门收取现金、金条或贵重物品。"],
    help_head="免费求助——不会有人评判您",
    helps=[("833-372-8311", "全国老年人诈骗热线 · 周一至周五 美东 10–6"),
           ("877-908-3360", "AARP 反诈热线 · 周一至周五 美东 8–8")],
    report="报案：ic3.gov  ·  reportfraud.ftc.gov  ·  提供翻译服务",
    code_head="我们家的暗号：",
    footline="如果已经发生了：这不是您的错，也还不算晚。",
    foot="欢迎自由复制、打印和分享。",
)


NOTICE = {
 "ur": ("اطلاع: غیر تصدیق شدہ مشینی ترجمہ — ابھی پرنٹ نہ کریں",
        "یہ مصنوعی ذہانت کا ترجمہ ہے، کسی مادری بولنے والے نے نہیں دیکھا۔ اردو جانتے ہیں؟ مدد کریں: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Urdu speakers: please help us check it."),
 "hi": ("सूचना: अप्रमाणित मशीनी अनुवाद — अभी प्रिंट न करें",
        "यह AI अनुवाद है, किसी मातृभाषी ने जाँचा नहीं है। हिंदी जानते हैं? मदद कीजिए: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Hindi speakers: please help us check it."),
 "fa": ("توجه: ترجمه ماشینی راستی‌آزمایی‌نشده — فعلاً چاپ نکنید",
        "این متن با هوش مصنوعی ترجمه شده و هیچ فارسی‌زبانی آن را بازبینی نکرده است. کمک کنید: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Farsi speakers: please help us check it."),
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
 "ps": ("پام: ناتصدیق شوې ماشیني ژباړه — لا یې مه چاپوئ",
        "دا د AI ژباړه ده او کوم مورنۍ ژبې ویونکي نه ده کتلې. مرسته وکړئ: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. Pashto speakers: please help us check it."),
 "ja": ("注意：未検証の機械翻訳 — まだ印刷しないでください",
        "AIによる翻訳で、母語話者の確認をまだ受けていません。日本語を話せる方、"
        "確認にご協力ください： translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Japanese speakers: please help us check it."),
 "ko": ("주의: 검증되지 않은 기계 번역 — 아직 인쇄하지 마십시오",
        "AI가 번역했으며 원어민의 검토를 아직 받지 않았습니다. 한국어를 하시는 분, "
        "검토를 도와주십시오: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Korean speakers: please help us check it."),
 "tl": ("PAUNAWA: HINDI PA NASUSURING AI TRANSLATION — HUWAG PA I-PRINT",
        "Isinalin ng AI at hindi pa nasusuri ng katutubong nagsasalita. Marunong ka ba? "
        "Tulungan mo kami: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Tagalog speakers: please help us check it."),
 "ar": ("تنبيه: ترجمة آلية غير مراجَعة — يُرجى عدم الطباعة بعد",
        "تُرجم هذا النص بالذكاء الاصطناعي ولم يراجعه ناطق بالعربية. هل تتحدث العربية؟ "
        "ساعدنا: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Arabic speakers: please help us check it."),
 "es": ("AVISO: TRADUCCIÓN SIN VALIDAR — NO IMPRIMIR AÚN",
        "Traducido por inteligencia artificial. Todavía no lo ha revisado un hablante nativo. "
        "¿Habla español? Ayúdenos a corregirlo: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Spanish speakers: please help us check it."),
 "vi": ("LƯU Ý: BẢN DỊCH CHƯA KIỂM CHỨNG — XIN CHƯA IN",
        "Do trí tuệ nhân tạo dịch. Chưa được người bản ngữ duyệt lại. "
        "Quý vị nói tiếng Việt? Xin giúp chúng tôi: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Vietnamese speakers: please help us check it."),
 "ru": ("ВНИМАНИЕ: НЕПРОВЕРЕННЫЙ ПЕРЕВОД — ПОКА НЕ ПЕЧАТАЙТЕ",
        "Переведено искусственным интеллектом. Не проверено носителем языка. "
        "Говорите по-русски? Помогите нам: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Russian speakers: please help us check it."),
 "zh": ("注意：翻译未经核校 —— 请暂勿打印",
        "由人工智能翻译，尚未经母语者审阅。您会说中文吗？请帮我们校对："
        "translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Chinese speakers: please help us check it."),
}


L["uk"] = dict(font="DejaVu Sans", brand="ДОВІРЯЙ, АЛЕ ПЕРЕВІРЯЙ",
  tagline="Можна й далі довіряти — просто додайте паузу.",
  steps_head="ПЕРШ НІЖ ПІДУТЬ БУДЬ-ЯКІ ГРОШІ",
  steps=[("Знайдіть номер самі.","Не той, що дали вони. Той, що на вашій картці або у виписці."),
         ("Зателефонуйте людині самі.","Спершу покладіть слухавку. Якщо все справжнє — вони на місці."),
         ("Зачекайте добу.","Справжня біда переживе ніч. Шахрайство — ні.")],
  signs_head="ТРИ ОЗНАКИ — ЗУПИНІТЬСЯ",
  signs=["Воно прийшло до вас — ви цього не починали.",
         "Вас швидко зачепило — страх, тривога або поспіх.",
         "Від вас хочуть передачі — грошей, коду або доступу до комп'ютера."],
  never_head="НІКОЛИ, ЖОДНОГО РАЗУ",
  never=["Нікому законному не платять подарунковими картками.",
         "Банк ніколи не попросить вивести гроші з банку.",
         "Ніколи не називайте вголос код із повідомлення.",
         "Ніхто не приїжджає додому по готівку, золото чи цінності."],
  help_head="БЕЗКОШТОВНА ДОПОМОГА — БЕЗ ОСУДУ",
  helps=[("833-372-8311","Національна лінія · Пн–Пт 10–18 ET"),
         ("877-908-3360","AARP Fraud Watch · Пн–Пт 8–20 ET")],
  report="Повідомити: ic3.gov · reportfraud.ftc.gov · є перекладач",
  code_head="Кодове слово нашої родини:",
  footline="Якщо вже сталося: це не ваша провина, і ще не пізно.",
  foot="Вільно копіювати, друкувати й поширювати.")

L["fr"] = dict(font="DejaVu Sans", brand="FAITES CONFIANCE, MAIS VÉRIFIEZ",
  tagline="Vous pouvez rester confiant, ajoutez juste une pause.",
  steps_head="AVANT QUE LE MOINDRE ARGENT NE PARTE",
  steps=[("Cherchez le numéro vous-même.","Pas celui qu'ils ont donné. Celui de votre carte ou de votre relevé."),
         ("Appelez la personne vous-même.","Raccrochez d'abord. Si c'était vrai, ils seront toujours là."),
         ("Attendez un jour.","Un vrai problème survit à une nuit de sommeil. Pas une arnaque.")],
  signs_head="TROIS SIGNES POUR S'ARRÊTER",
  signs=["C'est venu vers vous — vous n'avez rien commencé.",
         "Cela vous a touché vite — peur, inquiétude ou délai.",
         "On veut un transfert — argent, code ou votre ordinateur."],
  never_head="JAMAIS, PAS UNE SEULE FOIS",
  never=["Personne de légitime n'est payé en cartes-cadeaux.",
         "Votre banque ne demandera jamais de sortir l'argent de votre banque.",
         "Ne lisez jamais un code reçu par SMS à voix haute.",
         "Personne ne vient chez vous chercher espèces, or ou objets de valeur."],
  help_head="AIDE GRATUITE — SANS JUGEMENT",
  helps=[("833-372-8311","Ligne nationale · Lun–Ven 10h–18h ET"),
         ("877-908-3360","AARP Fraud Watch · Lun–Ven 8h–20h ET")],
  report="Signalez : ic3.gov · reportfraud.ftc.gov · interprète disponible",
  code_head="Le mot de code de notre famille :",
  footline="Si c'est déjà arrivé : ce n'est pas votre faute, et il n'est pas trop tard.",
  foot="Libre de copier, imprimer et partager.")

L["de"] = dict(font="DejaVu Sans", brand="VERTRAUEN, ABER NACHPRÜFEN",
  tagline="Sie können weiterhin vertrauen, fügen Sie nur eine Pause hinzu.",
  steps_head="BEVOR GELD FLIESST",
  steps=[("Suchen Sie die Nummer selbst.","Nicht die, die man Ihnen gab. Die auf Ihrer Karte oder Ihrem Auszug."),
         ("Rufen Sie die Person selbst an.","Erst auflegen. War es echt, sind sie noch da."),
         ("Warten Sie einen Tag.","Echte Probleme überstehen eine Nacht. Betrug nicht.")],
  signs_head="DREI ANZEICHEN ZUM ANHALTEN",
  signs=["Es kam zu Ihnen — Sie haben nichts angefangen.",
         "Es hat Sie schnell erwischt — Angst, Sorge oder eine Frist.",
         "Man will eine Übertragung — Geld, einen Code oder Ihren Computer."],
  never_head="NIEMALS, KEIN EINZIGES MAL",
  never=["Niemand Seriöses wird mit Geschenkkarten bezahlt.",
         "Ihre Bank bittet Sie nie, Geld von Ihrer Bank wegzuschaffen.",
         "Lesen Sie nie einen SMS-Code laut vor. Niemandem.",
         "Niemand kommt zu Ihnen nach Hause für Bargeld, Gold oder Wertsachen."],
  help_head="KOSTENLOSE HILFE — OHNE VORWÜRFE",
  helps=[("833-372-8311","Nationale Hotline · Mo–Fr 10–18 Uhr ET"),
         ("877-908-3360","AARP Fraud Watch · Mo–Fr 8–20 Uhr ET")],
  report="Melden: ic3.gov · reportfraud.ftc.gov · Dolmetscher verfügbar",
  code_head="Das Codewort unserer Familie:",
  footline="Wenn es schon passiert ist: Es ist nicht Ihre Schuld, und es ist nicht zu spät.",
  foot="Frei zu kopieren, drucken und weiterzugeben.")

L["pt"] = dict(font="DejaVu Sans", brand="CONFIE, MAS VERIFIQUE",
  tagline="Você pode continuar confiando, só acrescente uma pausa.",
  steps_head="ANTES QUE QUALQUER DINHEIRO SAIA",
  steps=[("Procure o número você mesmo.","Não o que lhe deram. O do seu cartão ou do seu extrato."),
         ("Ligue você mesmo para a pessoa.","Desligue primeiro. Se era verdade, eles continuarão lá."),
         ("Espere um dia.","Problemas reais sobrevivem a uma noite de sono. Golpes não.")],
  signs_head="TRÊS SINAIS PARA PARAR",
  signs=["Veio até você — não foi você que começou.",
         "Mexeu com você rápido — medo, preocupação ou prazo.",
         "Quer uma transferência — dinheiro, um código ou seu computador."],
  never_head="NUNCA, NEM UMA VEZ",
  never=["Ninguém legítimo recebe em cartões-presente.",
         "Seu banco nunca pedirá que tire o dinheiro do seu banco.",
         "Nunca leia em voz alta um código recebido por mensagem.",
         "Ninguém vai à sua casa buscar dinheiro, ouro ou objetos de valor."],
  help_head="AJUDA GRATUITA — SEM JULGAMENTO",
  helps=[("833-372-8311","Linha Nacional · Seg–Sex 10h–18h ET"),
         ("877-908-3360","AARP Fraud Watch · Seg–Sex 8h–20h ET")],
  report="Denuncie: ic3.gov · reportfraud.ftc.gov · há intérprete",
  code_head="A palavra-código da nossa família:",
  footline="Se já aconteceu: a culpa não é sua, e não é tarde demais.",
  foot="Livre para copiar, imprimir e compartilhar.")

L["pl"] = dict(font="DejaVu Sans", brand="UFAJ, ALE SPRAWDZAJ",
  tagline="Możesz nadal ufać, wystarczy dodać przerwę.",
  steps_head="ZANIM WYJDĄ JAKIEKOLWIEK PIENIĄDZE",
  steps=[("Sam znajdź numer.","Nie ten, który podali. Ten z Twojej karty lub wyciągu."),
         ("Sam zadzwoń do tej osoby.","Najpierw odłóż słuchawkę. Jeśli to prawda, nadal tam będą."),
         ("Odczekaj dobę.","Prawdziwe kłopoty przetrwają noc. Oszustwa nie.")],
  signs_head="TRZY SYGNAŁY, BY SIĘ ZATRZYMAĆ",
  signs=["Przyszło do Ciebie — to nie Ty zacząłeś.",
         "Szybko Cię poruszyło — strach, niepokój albo termin.",
         "Chcą przekazania — pieniędzy, kodu albo Twojego komputera."],
  never_head="NIGDY, ANI RAZU",
  never=["Nikt uczciwy nie przyjmuje kart podarunkowych.",
         "Bank nigdy nie poprosi o wyprowadzenie pieniędzy z banku.",
         "Nigdy nie czytaj na głos kodu z SMS-a. Nikomu.",
         "Nikt nie przyjeżdża do domu po gotówkę, złoto ani kosztowności."],
  help_head="BEZPŁATNA POMOC — BEZ OCENIANIA",
  helps=[("833-372-8311","Infolinia krajowa · Pon–Pt 10–18 ET"),
         ("877-908-3360","AARP Fraud Watch · Pon–Pt 8–20 ET")],
  report="Zgłoś: ic3.gov · reportfraud.ftc.gov · jest tłumacz",
  code_head="Hasło naszej rodziny:",
  footline="Jeśli już się stało: to nie Twoja wina i nie jest za późno.",
  foot="Można swobodnie kopiować, drukować i rozpowszechniać.")

L["ro"] = dict(font="DejaVu Sans", brand="AI ÎNCREDERE, DAR VERIFICĂ",
  tagline="Puteți avea în continuare încredere, doar adăugați o pauză.",
  steps_head="ÎNAINTE SĂ PLECE ORICE BAN",
  steps=[("Căutați singur numărul.","Nu cel dat de ei. Cel de pe cardul sau extrasul dumneavoastră."),
         ("Sunați dumneavoastră persoana.","Închideți mai întâi. Dacă era real, tot acolo vor fi."),
         ("Așteptați o zi.","Problemele reale supraviețuiesc unei nopți. Escrocheriile nu.")],
  signs_head="TREI SEMNE SĂ VĂ OPRIȚI",
  signs=["A venit la dumneavoastră — nu dumneavoastră ați început.",
         "V-a mișcat repede — frică, îngrijorare sau un termen limită.",
         "Vor un transfer — bani, un cod sau calculatorul dumneavoastră."],
  never_head="NICIODATĂ, NICI O SINGURĂ DATĂ",
  never=["Nimeni serios nu este plătit cu carduri cadou.",
         "Banca nu vă va cere niciodată să scoateți banii din bancă.",
         "Nu citiți niciodată cu voce tare un cod primit prin mesaj.",
         "Nimeni nu vine acasă la dumneavoastră după bani, aur sau valori."],
  help_head="AJUTOR GRATUIT — FĂRĂ JUDECĂȚI",
  helps=[("833-372-8311","Linia Națională · Lun–Vin 10–18 ET"),
         ("877-908-3360","AARP Fraud Watch · Lun–Vin 8–20 ET")],
  report="Raportați: ic3.gov · reportfraud.ftc.gov · există interpret",
  code_head="Cuvântul de cod al familiei noastre:",
  footline="Dacă s-a întâmplat deja: nu e vina dumneavoastră și nu e prea târziu.",
  foot="Liber de copiat, tipărit și distribuit.")

L["id"] = dict(font="DejaVu Sans", brand="PERCAYA, TAPI PERIKSA",
  tagline="Anda tetap bisa percaya, cukup tambahkan jeda.",
  steps_head="SEBELUM UANG BERPINDAH",
  steps=[("Cari sendiri nomor teleponnya.","Bukan nomor yang mereka beri. Nomor di kartu atau rekening koran Anda."),
         ("Telepon sendiri orangnya.","Tutup dulu teleponnya. Kalau benar, mereka masih di sana."),
         ("Tunggu satu hari.","Masalah sungguhan tahan semalam. Penipuan tidak.")],
  signs_head="TIGA TANDA UNTUK BERHENTI",
  signs=["Ia datang kepada Anda — bukan Anda yang memulai.",
         "Ia menggerakkan Anda cepat — takut, cemas, atau tenggat waktu.",
         "Ia ingin pemindahan — uang, kode, atau komputer Anda."],
  never_head="TIDAK PERNAH, SEKALI PUN TIDAK",
  never=["Tidak ada pihak sah yang dibayar dengan kartu hadiah.",
         "Bank tidak akan pernah meminta Anda memindahkan uang keluar dari bank.",
         "Jangan pernah membacakan kode SMS kepada siapa pun.",
         "Tidak ada yang datang ke rumah mengambil uang tunai, emas, atau barang berharga."],
  help_head="BANTUAN GRATIS — TANPA MENGHAKIMI",
  helps=[("833-372-8311","Saluran Nasional · Sen–Jum 10–18 ET"),
         ("877-908-3360","AARP Fraud Watch · Sen–Jum 8–20 ET")],
  report="Laporkan: ic3.gov · reportfraud.ftc.gov · tersedia juru bahasa",
  code_head="Kata kode keluarga kita:",
  footline="Kalau sudah terjadi: ini bukan salah Anda, dan belum terlambat.",
  foot="Bebas disalin, dicetak, dan dibagikan.")



NOTICE.update({
 "uk": ("УВАГА: НЕПЕРЕВІРЕНИЙ ПЕРЕКЛАД — ПОКИ НЕ ДРУКУЙТЕ",
        "Перекладено штучним інтелектом. Не перевірено носієм мови. Розмовляєте українською? "
        "Допоможіть нам: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Ukrainian speakers: please help us check it."),
 "fr": ("AVIS : TRADUCTION NON VALIDÉE — NE PAS IMPRIMER",
        "Traduit par intelligence artificielle. Non relu par un locuteur natif. Vous parlez français ? "
        "Aidez-nous : translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "French speakers: please help us check it."),
 "de": ("HINWEIS: UNGEPRÜFTE ÜBERSETZUNG — NOCH NICHT DRUCKEN",
        "Von künstlicher Intelligenz übersetzt. Nicht muttersprachlich geprüft. Sprechen Sie Deutsch? "
        "Helfen Sie uns: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "German speakers: please help us check it."),
 "pt": ("AVISO: TRADUÇÃO NÃO VALIDADA — NÃO IMPRIMIR AINDA",
        "Traduzido por inteligência artificial. Não revisado por falante nativo. Você fala português? "
        "Ajude-nos: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Portuguese speakers: please help us check it."),
 "pl": ("UWAGA: TŁUMACZENIE NIEZWERYFIKOWANE — NIE DRUKUJ",
        "Przetłumaczone przez sztuczną inteligencję. Niesprawdzone przez native speakera. Mówisz po polsku? "
        "Pomóż nam: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Polish speakers: please help us check it."),
 "ro": ("ATENȚIE: TRADUCERE NEVERIFICATĂ — NU TIPĂRIȚI ÎNCĂ",
        "Tradus de inteligență artificială. Neverificat de un vorbitor nativ. Vorbiți românește? "
        "Ajutați-ne: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Romanian speakers: please help us check it."),
 "id": ("PERHATIAN: TERJEMAHAN BELUM DIPERIKSA — JANGAN DICETAK DULU",
        "Diterjemahkan oleh kecerdasan buatan. Belum diperiksa penutur asli. Anda berbahasa Indonesia? "
        "Bantu kami: translations@trustbutverifyproject.org",
        "UNVALIDATED AI TRANSLATION — not reviewed by a native speaker. Do not distribute. "
        "Indonesian speakers: please help us check it."),
})


L["ja"] = dict(
    font="Noto Sans CJK JP",
    brand="信頼せよ、されど確認せよ",
    tagline="信頼したままで大丈夫です。ひと呼吸置くだけです。",
    steps_head="お金を動かす前に",
    steps=[("電話番号は自分で調べる。",
            "相手が教えた番号は使わない。カードの裏面か明細書の番号を使う。"),
           ("相手には自分からかけ直す。",
            "まず電話を切る。本当なら、相手はそこにいます。"),
           ("一日待つ。",
            "本物の問題は一晩眠っても消えません。詐欺は消えます。")],
    signs_head="立ち止まるべき三つの合図",
    signs=["向こうから来た — 自分から始めたことではない。",
           "気持ちが一気に動いた — 恐れ、心配、締め切り。",
           "何かを渡せと言う — お金、暗証番号、またはパソコン。"],
    never_head="絶対にありません",
    never=["まともな相手がギフトカードで支払いを受けることはありません。",
           "銀行が「お金を銀行の外に移せ」と言うことは絶対にありません。",
           "ショートメールの認証番号を口に出して伝えてはいけません。",
           "現金・金・貴重品を自宅まで受け取りに来る機関はありません。"],
    help_head="無料の相談窓口 — 責めません",
    helps=[("833-372-8311", "高齢者詐欺ホットライン · 月〜金 東部時間10〜18時"),
           ("877-908-3360", "AARP詐欺相談 · 月〜金 東部時間8〜20時")],
    report="通報先： ic3.gov  ·  reportfraud.ftc.gov  ·  通訳あり",
    code_head="私たち家族の合言葉：",
    footline="すでに起きてしまった場合：あなたのせいではありません。まだ間に合います。",
    foot="自由に複製・印刷・共有してください。",
)

L["ko"] = dict(
    font="Noto Sans CJK KR",
    brand="믿되, 확인하십시오",
    tagline="계속 믿으셔도 됩니다. 잠깐 멈추는 것만 더하면 됩니다.",
    steps_head="돈이 움직이기 전에",
    steps=[("전화번호를 직접 찾으십시오.",
            "그들이 준 번호 말고, 카드 뒷면이나 명세서에 있는 번호로."),
           ("그 사람에게 직접 전화하십시오.",
            "먼저 끊으십시오. 진짜라면 그대로 있습니다."),
           ("하루 기다리십시오.",
            "진짜 문제는 하룻밤 자도 남아 있습니다. 사기는 사라집니다.")],
    signs_head="멈춰야 할 세 가지 신호",
    signs=["먼저 연락이 왔다 — 내가 시작한 일이 아니다.",
           "감정이 빠르게 흔들렸다 — 두려움, 걱정, 마감 시한.",
           "무언가를 넘기라고 한다 — 돈, 인증번호, 또는 컴퓨터."],
    never_head="절대로, 단 한 번도",
    never=["정상적인 곳은 기프트카드로 결제받지 않습니다.",
           "은행이 돈을 은행 밖으로 옮기라고 하는 일은 없습니다.",
           "문자로 받은 인증번호를 누구에게도 말하지 마십시오.",
           "현금·금·귀중품을 집으로 받으러 오는 기관은 없습니다."],
    help_head="무료 도움 — 나무라지 않습니다",
    helps=[("833-372-8311", "전국 노인 사기 상담전화 · 월–금 동부시간 10–18시"),
           ("877-908-3360", "AARP 사기 상담 · 월–금 동부시간 8–20시")],
    report="신고: ic3.gov  ·  reportfraud.ftc.gov  ·  통역 제공",
    code_head="우리 가족의 암호:",
    footline="이미 당하셨다면: 당신 잘못이 아니며, 아직 늦지 않았습니다.",
    foot="자유롭게 복사·인쇄·공유하십시오.",
)

L["tl"] = dict(
    font="DejaVu Sans",
    brand="MAGTIWALA, PERO TIYAKIN",
    tagline="Puwede kang magtiwala pa rin, magdagdag ka lang ng paghinto.",
    steps_head="BAGO GUMALAW ANG KAHIT ANONG PERA",
    steps=[("Hanapin mo mismo ang numero.",
            "Hindi ang numerong ibinigay nila. Ang nasa likod ng card o sa statement mo."),
           ("Ikaw mismo ang tumawag sa tao.",
            "Ibaba mo muna. Kung totoo, naroon pa rin sila."),
           ("Maghintay ng isang araw.",
            "Ang totoong problema ay kayang hintayin ang isang gabi. Ang scam, hindi.")],
    signs_head="TATLONG SENYALES PARA HUMINTO",
    signs=["Sila ang lumapit — hindi ikaw ang nagsimula.",
           "Mabilis kang naapektuhan — takot, alala, o deadline.",
           "May hinihinging ilipat — pera, code, o ang computer mo."],
    never_head="KAILANMAN, KAHIT MINSAN",
    never=["Walang lehitimong tao o kompanya ang binabayaran sa gift card.",
           "Hindi kailanman hihilingin ng bangko na ilabas mo ang pera sa bangko.",
           "Huwag basahin nang malakas ang code na natanggap sa text.",
           "Walang pumupunta sa bahay mo para kumuha ng pera o alahas."],
    help_head="LIBRENG TULONG — WALANG HUSGA",
    helps=[("833-372-8311", "National Elder Fraud Hotline · Lun–Biy 10–6 ET"),
           ("877-908-3360", "AARP Fraud Watch · Lun–Biy 8–8 ET")],
    report="Mag-report sa ic3.gov  ·  reportfraud.ftc.gov  ·  may interpreter",
    code_head="Ang code word ng aming pamilya:",
    footline="Kung nangyari na: hindi mo ito kasalanan, at hindi pa huli ang lahat.",
    foot="Malayang kopyahin, i-print, at ibahagi.",
)

L["ar"] = dict(
    font="DejaVu Sans",
    rtl=True,
    brand="ثق ولكن تحقق",
    tagline="يمكنك أن تبقى واثقًا، فقط أضف وقفة.",
    steps_head="قبل تحويل أي مبلغ",
    steps=[("ابحث عن الرقم بنفسك.",
            "ليس الرقم الذي أعطوك إياه. بل الرقم على ظهر بطاقتك أو في كشف حسابك."),
           ("اتصل بالشخص بنفسك.",
            "أغلق الخط أولًا. إن كان الأمر حقيقيًا فسيظلون هناك."),
           ("انتظر يومًا واحدًا.",
            "المشكلة الحقيقية تصمد ليلة كاملة. أما الاحتيال فلا.")],
    signs_head="ثلاث علامات توجب التوقف",
    signs=["هم من بدأوا الاتصال — لست أنت.",
           "حرّكك الأمر بسرعة — خوف أو قلق أو موعد نهائي.",
           "يطلبون تحويل شيء — مالًا أو رمزًا أو دخولًا إلى حاسوبك."],
    never_head="لا يحدث هذا أبدًا",
    never=["لا أحد شرعي يُدفع له ببطاقات الهدايا.",
           "لن يطلب منك مصرفك أبدًا نقل أموالك خارج المصرف.",
           "لا تقرأ رمز التحقق بصوت عالٍ لأي شخص كان.",
           "لا توجد جهة ترسل من يأتي إلى بيتك ليأخذ نقودًا أو ذهبًا."],
    help_head="مساعدة مجانية — بلا أحكام",
    helps=[("833-372-8311", "الخط الوطني لاحتيال كبار السن · الاثنين–الجمعة"),
           ("877-908-3360", "AARP Fraud Watch · الاثنين–الجمعة")],
    report="للإبلاغ: ic3.gov  ·  reportfraud.ftc.gov  ·  تتوفر ترجمة",
    code_head="كلمة السر الخاصة بعائلتنا:",
    footline="إن كان قد حدث بالفعل: ليس ذنبك، ولم يفت الأوان.",
    foot="يمكنك النسخ والطباعة والمشاركة بحرية.",
)



L["ur"] = dict(font="Noto Naskh Arabic", rtl=True,
  brand="اعتبار کریں، مگر تصدیق کریں",
  tagline="آپ اعتبار جاری رکھ سکتے ہیں، بس ایک توقف شامل کریں۔",
  steps_head="کوئی بھی رقم بھیجنے سے پہلے",
  steps=[("نمبر خود تلاش کریں۔","وہ نمبر نہیں جو انہوں نے دیا۔ اپنے کارڈ کی پشت یا اپنے اسٹیٹمنٹ کا نمبر۔"),
         ("خود اُس شخص کو فون کریں۔","پہلے فون بند کریں۔ اگر بات سچی ہے تو وہ وہیں ہوں گے۔"),
         ("ایک دن انتظار کریں۔","اصل مسئلہ ایک رات کی نیند برداشت کر لیتا ہے۔ فراڈ نہیں کرتا۔")],
  signs_head="رکنے کی تین علامتیں",
  signs=["رابطہ اُن کی طرف سے آیا — آپ نے شروع نہیں کیا۔",
         "آپ فوراً جذباتی ہو گئے — خوف، فکر یا جلدی۔",
         "وہ کچھ منتقل کرانا چاہتے ہیں — پیسے، کوڈ یا آپ کا کمپیوٹر۔"],
  never_head="کبھی نہیں، ایک بار بھی نہیں",
  never=["کوئی جائز ادارہ گفٹ کارڈ میں ادائیگی نہیں لیتا۔",
         "آپ کا بینک کبھی نہیں کہے گا کہ رقم بینک سے باہر منتقل کریں۔",
         "پیغام میں آیا کوڈ کبھی کسی کو مت بتائیں۔",
         "کوئی ادارہ نقدی یا سونا لینے آپ کے گھر نہیں آتا۔"],
  help_head="مفت مدد — کوئی ملامت نہیں",
  helps=[("833-372-8311","قومی ہیلپ لائن · پیر تا جمعہ"),
         ("877-908-3360","AARP فراڈ واچ · پیر تا جمعہ")],
  interp='فون اٹھنے پر انگریزی میں کہیں: "Urdu, please"',
  report="اطلاع دیں: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="ہمارے خاندان کا کوڈ ورڈ:",
  footline="اگر یہ ہو چکا ہے: یہ آپ کی غلطی نہیں، اور ابھی دیر نہیں ہوئی۔",
  foot="آزادانہ نقل، پرنٹ اور تقسیم کریں۔")

L["hi"] = dict(font="Noto Sans Devanagari",
  brand="भरोसा करें, पर जाँच लें",
  tagline="आप भरोसा करना जारी रख सकते हैं, बस एक ठहराव जोड़ें।",
  steps_head="कोई भी पैसा भेजने से पहले",
  steps=[("नंबर खुद ढूँढें।","वह नंबर नहीं जो उन्होंने दिया। अपने कार्ड के पीछे या स्टेटमेंट का नंबर।"),
         ("उस व्यक्ति को खुद फ़ोन करें।","पहले फ़ोन काटें। अगर बात सच है तो वे वहीं मिलेंगे।"),
         ("एक दिन रुकें।","असली समस्या एक रात की नींद झेल लेती है। ठगी नहीं झेलती।")],
  signs_head="रुकने के तीन संकेत",
  signs=["संपर्क उनकी ओर से आया — आपने शुरू नहीं किया।",
         "आप तुरंत घबरा गए — डर, चिंता या जल्दबाज़ी।",
         "वे कुछ भिजवाना चाहते हैं — पैसा, कोड, या आपका कंप्यूटर।"],
  never_head="कभी नहीं, एक बार भी नहीं",
  never=["कोई भी सही संस्था गिफ़्ट कार्ड में भुगतान नहीं लेती।",
         "आपका बैंक कभी नहीं कहेगा कि पैसा बैंक से बाहर भेजें।",
         "मैसेज में आया कोड कभी किसी को न बताएँ।",
         "कोई संस्था नकद या सोना लेने आपके घर नहीं आती।"],
  help_head="मुफ़्त मदद — कोई ताना नहीं",
  helps=[("833-372-8311","राष्ट्रीय हेल्पलाइन · सोम–शुक्र"),
         ("877-908-3360","AARP फ़्रॉड वॉच · सोम–शुक्र")],
  interp='फ़ोन उठने पर अंग्रेज़ी में कहें: "Hindi, please"',
  report="शिकायत करें: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="हमारे परिवार का कोड शब्द:",
  footline="अगर हो चुका है: यह आपकी गलती नहीं, और अभी देर नहीं हुई।",
  foot="स्वतंत्र रूप से कॉपी, प्रिंट और साझा करें।")

L["fa"] = dict(font="Noto Naskh Arabic", rtl=True,
  brand="اعتماد کن، اما راستی‌آزمایی کن",
  tagline="می‌توانید همچنان اعتماد کنید، فقط یک مکث اضافه کنید.",
  steps_head="پیش از انتقال هر مبلغی",
  steps=[("شماره را خودتان پیدا کنید.","نه شماره‌ای که آن‌ها داده‌اند. شماره پشت کارت یا روی صورت‌حساب شما."),
         ("خودتان با آن شخص تماس بگیرید.","اول قطع کنید. اگر واقعی باشد، همان‌جا هستند."),
         ("یک روز صبر کنید.","مشکل واقعی یک شب خواب را تاب می‌آورد. کلاهبرداری نه.")],
  signs_head="سه نشانه برای توقف",
  signs=["آن‌ها تماس گرفتند — شما شروع نکردید.",
         "به سرعت احساساتی شدید — ترس، نگرانی یا عجله.",
         "چیزی می‌خواهند منتقل شود — پول، یک کد، یا رایانه شما."],
  never_head="هرگز، حتی یک بار",
  never=["هیچ نهاد معتبری با کارت هدیه پول نمی‌گیرد.",
         "بانک شما هرگز نمی‌خواهد پول را از بانک بیرون ببرید.",
         "کد پیامکی را هرگز برای کسی نخوانید.",
         "هیچ نهادی برای گرفتن پول یا طلا به خانه شما نمی‌آید."],
  help_head="کمک رایگان — بدون سرزنش",
  helps=[("833-372-8311","خط ملی سالمندان · دوشنبه تا جمعه"),
         ("877-908-3360","AARP Fraud Watch · دوشنبه تا جمعه")],
  interp='وقتی پاسخ دادند، به انگلیسی بگویید: "Farsi, please"',
  report="گزارش: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="رمز خانوادگی ما:",
  footline="اگر رخ داده: تقصیر شما نیست و هنوز دیر نشده است.",
  foot="آزادانه کپی، چاپ و منتشر کنید.")

L["bn"] = dict(font="Noto Sans Bengali",
  brand="বিশ্বাস করুন, তবে যাচাই করুন",
  tagline="আপনি বিশ্বাস করা চালিয়ে যেতে পারেন, শুধু একটু বিরতি যোগ করুন।",
  steps_head="কোনো টাকা পাঠানোর আগে",
  steps=[("নম্বরটি নিজে খুঁজে নিন।","তারা যে নম্বর দিয়েছে সেটি নয়। আপনার কার্ডের পিছনের বা স্টেটমেন্টের নম্বর।"),
         ("নিজে সেই ব্যক্তিকে ফোন করুন।","আগে ফোন রাখুন। সত্যি হলে তাঁরা সেখানেই থাকবেন।"),
         ("একদিন অপেক্ষা করুন।","আসল সমস্যা এক রাত ঘুমিয়েও টিকে থাকে। প্রতারণা টেকে না।")],
  signs_head="থামার তিনটি সংকেত",
  signs=["যোগাযোগ ওদের দিক থেকে এসেছে — আপনি শুরু করেননি।",
         "আপনি দ্রুত আবেগাপ্লুত হয়েছেন — ভয়, দুশ্চিন্তা বা তাড়াহুড়ো।",
         "ওরা কিছু হস্তান্তর চায় — টাকা, কোড, বা আপনার কম্পিউটার।"],
  never_head="কখনোই নয়, একবারও নয়",
  never=["কোনো বৈধ প্রতিষ্ঠান গিফট কার্ডে টাকা নেয় না।",
         "আপনার ব্যাংক কখনো টাকা ব্যাংকের বাইরে সরাতে বলবে না।",
         "মেসেজে আসা কোড কাউকে বলবেন না।",
         "কোনো সংস্থা নগদ বা সোনা নিতে আপনার বাড়িতে আসে না।"],
  help_head="বিনামূল্যে সহায়তা — কোনো দোষারোপ নেই",
  helps=[("833-372-8311","জাতীয় হেল্পলাইন · সোম–শুক্র"),
         ("877-908-3360","AARP Fraud Watch · সোম–শুক্র")],
  interp='ফোন ধরলে ইংরেজিতে বলুন: "Bengali, please"',
  report="রিপোর্ট: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="আমাদের পরিবারের কোড শব্দ:",
  footline="যদি ঘটেই থাকে: এটি আপনার দোষ নয়, এবং এখনও দেরি হয়নি।",
  foot="স্বাধীনভাবে কপি, প্রিন্ট ও শেয়ার করুন।")

L["hy"] = dict(font="Noto Sans Armenian",
  brand="ՎՍՏԱՀԻՐ, ԲԱՅՑ ՍՏՈՒԳԻՐ",
  tagline="Կարող եք շարունակել վստահել, պարզապես ավելացրե՛ք դադար։",
  steps_head="ՆԱԽՔԱՆ ՈՐԵՎԷ ԳՈՒՄԱՐ ՓՈԽԱՆՑԵԼԸ",
  steps=[("Համարը ինքնե՛րդ գտեք։","Ոչ թե նրանց տված համարը։ Ձեր քարտի հետևի կամ քաղվածքի համարը։"),
         ("Ինքնե՛րդ զանգահարեք այդ մարդուն։","Նախ անջատե՛ք։ Եթե իսկական է, նրանք տեղում կլինեն։"),
         ("Սպասե՛ք մեկ օր։","Իսկական խնդիրը գիշերը կդիմանա։ Խարդախությունը՝ ոչ։")],
  signs_head="ԿԱՆԳ ԱՌՆԵԼՈՒ ԵՐԵՔ ՆՇԱՆ",
  signs=["Կապը եկավ նրանցից — դուք չեք սկսել։",
         "Ձեզ արագ ազդեց — վախ, անհանգստություն կամ շտապողականություն։",
         "Ուզում են փոխանցում — գումար, ծածկագիր կամ ձեր համակարգիչը։"],
  never_head="ԵՐԲԵՔ, ՈՉ ՄԻ ԱՆԳԱՄ",
  never=["Ոչ մի օրինական կազմակերպություն նվեր-քարտով վճար չի ընդունում։",
         "Ձեր բանկը երբեք չի խնդրի գումարը հանել բանկից։",
         "Երբեք ձայնով մի՛ ասեք հաղորդագրությամբ ստացած ծածկագիրը։",
         "Ոչ ոք ձեր տուն չի գալիս կանխիկ, ոսկի կամ արժեքներ վերցնելու։"],
  help_head="ԱՆՎՃԱՐ ՕԳՆՈՒԹՅՈՒՆ — ԱՌԱՆՑ ԴԱՏԵԼՈՒ",
  helps=[("833-372-8311","Ազգային թեժ գիծ · Երկ–Ուրբ"),
         ("877-908-3360","AARP Fraud Watch · Երկ–Ուրբ")],
  interp='Երբ պատասխանեն, անգլերեն ասեք՝ "Armenian, please"',
  report="Հաղորդել՝ ic3.gov  ·  reportfraud.ftc.gov",
  code_head="Մեր ընտանիքի գաղտնի բառը՝",
  footline="Եթե արդեն պատահել է՝ ձեր մեղքը չէ, և դեռ ուշ չէ։",
  foot="Ազատորեն պատճենեք, տպեք և տարածեք։")

L["am"] = dict(font="Noto Sans Ethiopic",
  brand="እመኑ፣ ግን አረጋግጡ",
  tagline="እምነትዎን መቀጠል ይችላሉ፣ አንድ ማቆሚያ ብቻ ይጨምሩ።",
  steps_head="ማንኛውም ገንዘብ ከመላኩ በፊት",
  steps=[("ስልክ ቁጥሩን ራስዎ ይፈልጉ።","እነሱ የሰጡትን ቁጥር አይደለም። በካርድዎ ጀርባ ወይም በመግለጫዎ ላይ ያለውን።"),
         ("ራስዎ ወደ ሰውዬው ይደውሉ።","መጀመሪያ ስልኩን ይዝጉ። እውነት ከሆነ እዚያው ይኖራሉ።"),
         ("አንድ ቀን ይጠብቁ።","እውነተኛ ችግር አንድ ሌሊት እንቅልፍ ይቋቋማል። ማጭበርበር አይችልም።")],
  signs_head="ማቆም ያለብዎት ሦስት ምልክቶች",
  signs=["እነሱ ናቸው የደወሉት — እርስዎ አልጀመሩም።",
         "በፍጥነት ስሜትዎን ነካ — ፍርሃት፣ ጭንቀት ወይም ችኮላ።",
         "ማስተላለፍ ይፈልጋሉ — ገንዘብ፣ ኮድ ወይም ኮምፒውተርዎን።"],
  never_head="በፍጹም፣ አንድ ጊዜም ቢሆን",
  never=["ማንኛውም ሕጋዊ ተቋም በስጦታ ካርድ ክፍያ አይቀበልም።",
         "ባንክዎ ገንዘብዎን ከባንክ እንዲያወጡ በፍጹም አይጠይቅም።",
         "በመልእክት የደረሰዎትን ኮድ ለማንም አይናገሩ።",
         "ጥሬ ገንዘብ ወይም ወርቅ ለመውሰድ ወደ ቤትዎ የሚመጣ ተቋም የለም።"],
  help_head="ነጻ እርዳታ — ማንም አይወቅስዎትም",
  helps=[("833-372-8311","ብሔራዊ የስልክ መስመር · ሰኞ–ዓርብ"),
         ("877-908-3360","AARP Fraud Watch · ሰኞ–ዓርብ")],
  interp='ሲነሱልዎት በእንግሊዝኛ ይበሉ፦ "Amharic, please"',
  report="ሪፖርት ያድርጉ፦ ic3.gov  ·  reportfraud.ftc.gov",
  code_head="የቤተሰባችን ሚስጥር ቃል፦",
  footline="አስቀድሞ ከተከሰተ፦ የእርስዎ ጥፋት አይደለም፣ እና ገና አልረፈደም።",
  foot="በነጻነት ይቅዱ፣ ያትሙ እና ያካፍሉ።")

L["sq"] = dict(font="DejaVu Sans",
  brand="BESO, POR VERIFIKO",
  tagline="Mund të vazhdoni të besoni, thjesht shtoni një pauzë.",
  steps_head="PARA SE TË LËVIZË ÇDO PARA",
  steps=[("Gjejeni vetë numrin.","Jo numrin që ju dhanë ata. Atë në pjesën e pasme të kartës ose në pasqyrën tuaj."),
         ("Telefonojini vetë personit.","Mbyllni telefonin fillimisht. Nëse ishte e vërtetë, ata do të jenë ende aty."),
         ("Prisni një ditë.","Problemi i vërtetë e mbijeton një natë gjumë. Mashtrimi jo.")],
  signs_head="TRI SHENJA PËR TË NDALUAR",
  signs=["Erdhi tek ju — nuk e nisët ju.",
         "Ju preku shpejt — frikë, shqetësim ose afat.",
         "Kërkon një transferim — para, një kod, ose kompjuterin tuaj."],
  never_head="KURRË, ASNJË HERË TË VETME",
  never=["Askush i ligjshëm nuk paguhet me karta dhuratë.",
         "Banka juaj nuk do t'ju kërkojë kurrë t'i nxirrni paratë nga banka.",
         "Mos e lexoni kurrë me zë kodin që ju erdhi me mesazh.",
         "Askush nuk vjen në shtëpinë tuaj për të marrë para, ar ose sende me vlerë."],
  help_head="NDIHMË FALAS — PA GJYKIM",
  helps=[("833-372-8311","Linja Kombëtare · Hën–Pre 10–6 ET"),
         ("877-908-3360","AARP Fraud Watch · Hën–Pre 8–8 ET")],
  interp='Kur t\'ju përgjigjen, thoni në anglisht: "Albanian, please"',
  report="Raportoni: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="Fjalëkalimi i familjes sonë:",
  footline="Nëse ka ndodhur tashmë: nuk është faji juaj dhe nuk është vonë.",
  foot="I lirë për ta kopjuar, printuar dhe shpërndarë.")

L["ps"] = dict(font="Noto Naskh Arabic", rtl=True,
  brand="باور وکړه، خو تصدیق یې کړه",
  tagline="تاسو کولی شئ لا هم باور وکړئ، یوازې یو درنګ ورزیات کړئ.",
  steps_head="د هرې پیسې لېږلو دمخه",
  steps=[("شمېره پخپله ولټوئ.","هغه شمېره نه چې هغوی درکړې. د خپل کارت شا یا د خپل حساب پاڼې شمېره."),
         ("پخپله هغه کس ته زنګ ووهئ.","لومړی ټیلیفون بند کړئ. که ریښتیا وي، هغوی به هلته وي."),
         ("یوه ورځ صبر وکړئ.","ریښتینې ستونزه د یوې شپې خوب زغمي. درغلي یې نه زغمي.")],
  signs_head="د درېدو درې نښې",
  signs=["اړیکه د هغوی له خوا راغله — تاسو یې پیل نه و کړی.",
         "ژر مو احساسات ولړزېدل — وېره، اندېښنه یا بیړه.",
         "د لېږد غوښتنه کوي — پیسې، کوډ، یا ستاسو کمپیوټر."],
  never_head="هېڅکله، حتی یو ځل هم",
  never=["هېڅ قانوني اداره د ډالۍ کارت له لارې پیسې نه اخلي.",
         "ستاسو بانک به هېڅکله ونه وایي چې پیسې له بانکه بهر کړئ.",
         "په پیغام کې راغلی کوډ هېڅ چا ته مه وایاست.",
         "هېڅ اداره ستاسو کور ته د نغدو پیسو یا سرو زرو اخیستلو لپاره نه راځي."],
  help_head="وړیا مرسته — هېڅ ملامتیا نشته",
  helps=[("833-372-8311","ملي کرښه · دوشنبه تر جمعې"),
         ("877-908-3360","AARP Fraud Watch · دوشنبه تر جمعې")],
  interp='کله چې ځواب درکړي، په انګلیسي کې ووایاست: "Pashto, please"',
  report="راپور: ic3.gov  ·  reportfraud.ftc.gov",
  code_head="زموږ د کورنۍ کوډ ټکی:",
  footline="که مخکې پېښ شوی وي: ستاسو ګناه نه ده، او لا ناوخته نه دي.",
  foot="په آزادۍ سره یې کاپي، چاپ او شریک کړئ.")


# --- template --------------------------------------------------------------

TPL = """<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="utf-8">
<title>{brand}</title>
<style>
  @page {{ size: Letter; margin: 10mm 13mm 7mm 13mm; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 100%; }}
  .wrap {{ width: 100%; max-width: 100%; }}
  body {{
    font-family: "{font}", "DejaVu Sans", sans-serif;
    color: #000; background: #fff;
    -webkit-font-smoothing: antialiased;
  }}

  /* masthead */
  .brand {{ font-size: {brandsize}pt; font-weight: 700; letter-spacing: {track}; line-height: 1.02; }}
  .tagline {{ font-size: 17pt; margin-top: 1pt; line-height: 1.15; }}
  .rule {{ border-top: 5pt solid #000; margin: 4pt 0 0 0; }}
  .hair {{ border-top: 1.5pt solid #000; margin: {hair}pt 0; }}

  /* zone labels sit on the rule, like a form */
  .zone {{ font-size: 13pt; font-weight: 700; letter-spacing: 2.2px;
           padding-top: 3pt; padding-bottom: 4pt; }}

  /* THE SIGNATURE: three steps, huge, readable across a kitchen */
  .step {{ display: flex; align-items: flex-start; gap: 19pt; padding: {steppad}pt 0; }}
  .num  {{ font-size: {numsz}pt; font-weight: 700; line-height: 0.85;
           width: 57pt; flex: none; }}
  .imp  {{ font-size: {impsize}pt; font-weight: 700; line-height: 1.04; }}
  .sub  {{ font-size: 15pt; line-height: 1.18; margin-top: 2pt; }}

  ul {{ list-style: none; }}
  li {{ font-size: {li}pt; line-height: 1.18; padding: {lipad}pt 0 {lipad}pt 26pt;
        position: relative; }}
  li:before {{ content: "\\25A0"; position: absolute; left: 0; font-size: 12pt; top: 5pt; }}

  .never {{ border: 4pt solid #000; padding: 6pt 14pt 7pt; margin-top: 1pt; }}
  .never .zone {{ padding-top: 0; padding-bottom: 5pt; }}
  .never li {{ font-weight: 700; font-size: {nli}pt; }}
  .never li:before {{ content: "\\2715"; font-size: 14pt; top: 3pt; }}

  .helpgrid {{ display: flex; gap: 28pt; padding-top: 1pt; }}
  .help {{ flex: 1; }}
  .tel {{ font-size: 33pt; font-weight: 700; letter-spacing: -0.5px; line-height: 1.0; }}
  .who {{ font-size: 13pt; line-height: 1.1; margin-top: 1pt; }}
  .report {{ font-size: 12.5pt; margin-top: 1pt; }}
  .interp {{ font-size: 13.5pt; font-weight: 700; margin-top: 4pt;
             border-top: 1.5pt solid #000; padding-top: 4pt; }}

  .spacer {{ height: 0; }}
  .codeline {{ display: flex; align-items: baseline; gap: 8pt;
               padding-top: 0; white-space: nowrap; }}
  .code-label {{ font-size: 10pt; font-weight: 700; }}
  .code-blank {{ flex: 1 1 auto; min-width: 40pt;
                 border-bottom: 1.3pt solid #000; height: 1pt; margin-bottom: -1pt; }}
  .footline {{ font-size: 14pt; font-weight: 700; line-height: 1.05;
               border-top: 3pt solid #000; padding-top: 2pt; }}
  .foot {{ font-size: 12pt; margin-top: 1pt; }}
  .notice {{ border: 2.5pt solid #000; padding: 3.5pt 9pt 4.5pt; margin-top: 2.5pt;
             background: #f0f0f0; }}
  .notice .nt {{ font-size: 11pt; font-weight: 700; line-height: 1.2; }}
  .notice .nb {{ font-size: 9.5pt; line-height: 1.2; margin-top: 2pt; }}
  .notice .ne {{ font-size: 7.3pt; line-height: 1.12; margin-top: 2pt; }}
{nastaliq_css}
</style></head><body><div class="wrap">

  <div class="brand">{brand}</div>
  <div class="tagline">{tagline}</div>
  <div class="rule"></div>

  <div class="zone">{steps_head}</div>
  {steps_html}

  <div class="hair"></div>
  <div class="zone" style="padding-top:0">{signs_head}</div>
  <ul>{signs_html}</ul>

  <div class="hair"></div>
  <div class="never">
    <div class="zone">{never_head}</div>
    <ul>{never_html}</ul>
  </div>

  <div class="hair"></div>
  <div class="zone" style="padding-top:0;padding-bottom:2pt">{help_head}</div>
  <div class="helpgrid">{help_html}</div>
  {interp_html}
  <div class="report">{report}</div>

  <div class="codeline"><span class="code-label">{code_head}</span><span class="code-blank"></span></div>

  <div class="spacer"></div>
  <div class="footline">{footline}</div>
  <div class="foot">{foot}</div>
  {notice_html}

</div></body></html>"""


def build(code, d):
    e = html.escape
    steps_html = "".join(
        f'<div class="step"><div class="num">{i+1}</div>'
        f'<div><div class="imp">{e(imp)}</div>'
        f'<div class="sub">{e(sub)}</div></div></div>'
        for i, (imp, sub) in enumerate(d["steps"]))
    signs_html = "".join(f"<li>{e(s)}</li>" for s in d["signs"])
    never_html = "".join(f"<li>{e(s)}</li>" for s in d["never"])
    help_html = "".join(
        f'<div class="help"><div class="tel">{e(t)}</div>'
        f'<div class="who">{e(w)}</div></div>' for t, w in d["helps"])

    # brand line has to fit on one line at Letter width
    n = len(d["brand"])
    brandsize = 46 if n <= 20 else (36 if n <= 28 else 29)
    impsize = 28 if code != "zh" else 29
    if code in NOTICE:
        impsize -= 5
    track = "1.5px" if code != "zh" else "2px"

    if code in NOTICE:
        nt, nb, ne = NOTICE[code]
        notice_html = (f'<div class="notice"><div class="nt">{e(nt)}</div>'
                       f'<div class="nb">{e(nb)}</div>'
                       f'<div class="ne">{e(ne)}</div></div>')
    else:
        notice_html = ""

    nastaliq = d.get("font","").startswith("Noto Nastaliq")
    tight = code in NOTICE
    spacer  = 1 if tight else 2
    steppad = 0.35 if tight else 2
    hair    = 2.3 if tight else 5
    li      = 13.0 if tight else 17
    lipad   = 0.6 if tight else 2
    nli     = 11.6 if tight else 15
    numsz   = 50 if tight else 60
    if nastaliq:
        impsize = 15
        spacer, steppad, hair = 0, 0, 4
        li, lipad, nli, numsz = 10.5, 0, 10, 34

    rtl = d.get("rtl", False)
    interp_html = (f'<div class="interp">{e(d["interp"])}</div>'
                   if d.get("interp") else "")

    nq = ""
    if rtl:
        impsize = round(impsize * 0.72)
        numsz   = round(numsz * 0.70)
        li      = round(li * 0.74, 1)
        nli     = round(nli * 0.74, 1)
        nq += ("\n  .brand { white-space: normal; word-spacing: .02em; }"
               "\n  .tagline { font-size: 12pt !important; }"
               "\n  .zone { font-size: 9.5pt !important; }"
               "\n  .sub { font-size: 10.5pt !important; }"
               "\n  .tel { font-size: 24pt !important; }"
               "\n  .who { font-size: 9.5pt !important; }"
               "\n  .interp { font-size: 10.5pt !important; }"
               "\n  .report { font-size: 10.5pt !important; }"
               "\n  .footline { font-size: 12pt !important; }"
               "\n  .notice .nt { font-size: 9.5pt !important; }"
               "\n  .notice .nb { font-size: 8.5pt !important; }"
               "\n  .notice .ne { font-size: 7pt !important; }"
               "\n  .foot { font-size: 8.5pt !important; }"
               "\n  .step { padding-top: 5pt !important; padding-bottom: 9pt !important; }"
               "\n  .sub { padding-bottom: 2pt; }"
               "\n  .hair { margin: 8pt 0 !important; }"
               "\n  .notice { margin-top: 6pt !important; }")
    if nastaliq:
        nq = ("\n  .brand {{ line-height: 2.05 !important; padding-bottom: 4pt; }}"
              "\n  .tagline {{ line-height: 2.1 !important; }}"
              "\n  .imp {{ line-height: 2.0 !important; }}"
              "\n  .sub {{ line-height: 2.0 !important; }}"
              "\n  li {{ line-height: 2.0 !important; padding-top: 4pt; padding-bottom: 4pt; }}"
              "\n  .zone {{ line-height: 1.9 !important; }}"
              "\n  .who {{ line-height: 2.0 !important; }}"
              "\n  .interp {{ line-height: 2.0 !important; }}"
              "\n  .footline {{ line-height: 2.0 !important; }}"
              "\n  .notice .nt {{ line-height: 2.0 !important; }}"
              "\n  .notice .nb {{ line-height: 2.0 !important; }}"
              "\n  .foot {{ line-height: 2.0 !important; }}").replace("{{","{").replace("}}","}")

    if rtl:
        brandsize = min(brandsize, 16)
        track = "0"
        nq = nq + (
          "\n  .brand, .tagline, .zone, .imp, .sub, li, .who, .interp,"
          "\n  .report, .footline, .foot, .notice .nt, .notice .nb, .code-label {"
          "\n    direction: rtl; text-align: right; letter-spacing: 0 !important; }"
          "\n  li { padding-left: 0 !important; padding-right: 26pt !important; }"
          "\n  li:before { left: auto !important; right: 0 !important; }"
          "\n  .step { flex-direction: row-reverse; }"
          "\n  .step > div:last-child { flex: 1 1 auto; min-width: 0; }"
          "\n  .num { text-align: left; margin-left: 16pt; }"
          "\n  .helpgrid { flex-direction: row-reverse; }"
          "\n  .tel { text-align: right; direction: ltr; }"
          "\n  .codeline { flex-direction: row-reverse; }"
        )

    out = TPL.format(lang=code, nastaliq_css=nq, brandsize=brandsize, spacer=spacer,
                     dir=("rtl" if rtl else "ltr"), dirn=("rtl" if rtl else "ltr"),
                     interp_html=interp_html,
                     steppad=steppad, hair=hair, li=li, lipad=lipad,
                     nli=nli, numsz=numsz, impsize=impsize, track=track,
                     steps_html=steps_html, signs_html=signs_html,
                     never_html=never_html, help_html=help_html,
                     brand=e(d["brand"]), tagline=e(d["tagline"]),
                     steps_head=e(d["steps_head"]), signs_head=e(d["signs_head"]),
                     never_head=e(d["never_head"]), help_head=e(d["help_head"]),
                     report=e(d["report"]), code_head=e(d["code_head"]), footline=e(d["footline"]),
                     foot=e(d["foot"]), font=d["font"], notice_html=notice_html)

    hpath = f"{OUT}/fridge-sheet-{code}.html"
    with open(hpath, "w", encoding="utf-8") as f:
        f.write(out)
    ppath = f"{OUT}/fridge-sheet-{code}.pdf"
    if _WeasyHTML is not None:
        _WeasyHTML(filename=hpath).write_pdf(ppath)
        print("built", code, "(weasyprint)")
        return
    subprocess.run(["wkhtmltopdf", "--quiet", "--enable-local-file-access",
                    "--page-size", "Letter",
                    "-T", "10mm", "-B", "7mm", "-L", "13mm", "-R", "13mm",
                    hpath, ppath], check=True)
    print("built", code)


for code, d in L.items():
    build(code, d)
