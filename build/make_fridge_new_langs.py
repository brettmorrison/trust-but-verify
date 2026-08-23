#!/usr/bin/env python3
"""
Fridge sheets for the 10 newest languages, via reportlab (no WeasyPrint
needed). Matches the visual layout of the existing sheets: title, tagline,
three numbered steps, three signs, a bordered never-list, two hotlines, a
closing line. Text is the same translations already used on each language's
landing page in content/<lang>/index.md.

    python3 build/make_fridge_new_langs.py
"""
import os
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "formats", "print")

INK = HexColor("#111111")
MUTED = HexColor("#4a4a4a")
PAPER = HexColor("#fffdf9")
ACCENT = HexColor("#123f7a")

W, H = 612, 792
M = 40

L = {}

L["et"] = dict(brand="USALDA, AGA KONTROLLI",
  tagline="Teil pole vaja kõiki kahtlustada. Lisage lihtsalt üks samm.",
  steps_head="ENNE RAHA SAATMIST",
  steps=[("Otsige number ise üles.", "Mitte see, mille teile anti. See, mis on kaardil või väljavõttel."),
         ("Helistage inimesele ise.", "Pange kõigepealt toru hargile. Seejärel helistage."),
         ("Oodake üks päev.", "Tõeline probleem püsib üle ühe öö. Pettus ei püsi.")],
  signs_head="KOLM MÄRKI, MIS PEAKSID TEID PEATAMA",
  signs=["See tuli teie juurde — teie ei alustanud seda.",
         "See mõjutas kiiresti teie tundeid — hirmu või kiirustamist.",
         "See soovib ülekannet — raha, koodi või teie arvutit."],
  never_head="MITTE KUNAGI, MITTE KORDAGI",
  never=["Ükski asutus ei aktsepteeri kinkekaarte maksena.",
         "Teie pank ei palu teil kunagi kontolt raha välja võtta.",
         "Ärge öelge kellelegi koodi, mille saite tekstiga.",
         "Keegi ei tule teie koju sularaha ega kulda järele."],
  help_head="TASUTA ABI — ILMA HUKKAMÕISTUTA",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  E–R"),
         ("877-908-3360", "AARP Fraud Watch  ·  E–R")],
  report="Teatage: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Kui see on juba juhtunud: see pole teie süü ja pole veel liiga hilja.",
  foot="Tasuta kopeerida, printida ja jagada.",
  url="https://trustbutverifyproject.org/et/")

L["lv"] = dict(brand="UZTICIES, BET PĀRBAUDI",
  tagline="Jums nav jāaizdomājas par visiem. Vienkārši pievienojiet vienu soli.",
  steps_head="PIRMS JEBKĀDAS NAUDAS NOSŪTĮŠANAS",
  steps=[("Paši atrodiet numuru.", "Nevis to, ko jums iedeva. To, kas ir uz kartes vai izraksta."),
         ("Paši piezvaniet personai.", "Vispirms nolieciet klausuli. Tad piezvaniet."),
         ("Pagaidiet vienu dienu.", "Įsta problēma pārdzīvo vienu nakti miega. Krāpšana — nē.")],
  signs_head="TRĪS PAZĪMES, KURĀM JĀAPSTĀJAS",
  signs=["Tas atnāca pie jums — jūs to nesākāt.",
         "Tas ātri skāra jūsu jūtas — bailes vai steigu.",
         "Tas vēlas pārskaitījumu — naudu, kodu vai datoru."],
  never_head="NEKAD, NE REIZI",
  never=["Neviena iestāde nepieņem dāvanu kartes kā maksājumu.",
         "Jūsu banka nekad neprasa izņemt naudu no konta.",
         "Nekad nevienam nepasakiet kodu, ko saņēmāt īsziņā.",
         "Neviens nenāk mājās pēc skaidras naudas vai zelta."],
  help_head="BEZMAKSAS PALĪDZĪBA — BEZ NOSODĪJUMA",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  P–Pk"),
         ("877-908-3360", "AARP Fraud Watch  ·  P–Pk")],
  report="Ziņojiet: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Ja tas jau ir noticis: tā nav jūsu vaina, un vēl nav par vēlu.",
  foot="Brivi kopēt, printet un dalīties.",
  url="https://trustbutverifyproject.org/lv/")

L["lt"] = dict(brand="PASITIKĖK, BET PATIKRINK",
  tagline="Jums nereikia įtarinėti visų. Tiesiog pridėkite vieną žingsnį.",
  steps_head="PRIEŠ IŠSIUNČIANT PINIGUS",
  steps=[("Patys susiraskite numerį.", "Ne tą, kurį jums davė. Tą, kuris yra ant kortelės ar išrašo."),
         ("Patys paskambinkite.", "Pirmiausia padėkite ragelį. Tada paskambinkite."),
         ("Palaukite vieną dieną.", "Tikra problema išgyvena nakties miegą. Sukčiavimas — ne.")],
  signs_head="TRYS POŽYMIAI, KURIE TURĖTŲ JŪS SUSTABDYTI",
  signs=["Tai atėjo pas jus — jūs to nepradėjote.",
         "Tai greitai paveikė jausmus — baimę ar skubą.",
         "Tai nori pervedimo — pinigų, kodo ar kompiuterio."],
  never_head="NIEKADA, NĖ KARTĀ",
  never=["Jokia įstaiga nepriima dovanų kortelių kaip mokėjimo.",
         "Bankas niekada neprašys išsiimti pinigų iš sąskaitos.",
         "Niekada nesakykite kodo, gauto SMS žinute.",
         "Niekas neatvyksta namo pasiimti grynųjų ar aukso."],
  help_head="NEMOKAMA PAGALBA — BE SMERKIMO",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Pr–Pn"),
         ("877-908-3360", "AARP Fraud Watch  ·  Pr–Pn")],
  report="Praneškite: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Jei tai jau atsitiko: tai ne jūsų kaltė, ir dar nėra vėlu.",
  foot="Laisvai kopijuoti, spausdinti ir dalintis.",
  url="https://trustbutverifyproject.org/lt/")

L["pl"] = None  # already exists from the earlier batch — skipped here

L["ht"] = dict(brand="FÈ KONFYANS, MEN VERIFYE",
  tagline="Ou pa bezwen sispèk tout moun. Jis ajoute yon sèl etap.",
  steps_head="ANVAN NENPÒT LAJAN SOTI",
  steps=[("Chèche nimewo a ou menm.", "Se pa nimewo yo te ba ou a. Se sa ki sou kat ou."),
         ("Rele moun nan ou menm.", "Rakwoche anvan. Apre sa rele."),
         ("Tann yon jou.", "Yon vrè pwoblèm ap siviv yon nwit somèy.")],
  signs_head="TWA SIY KI DWE FÈ OU SISPANN",
  signs=["Se yo ki rele ou — se pa ou ki te kòmanse.",
         "Yo touche santiman ou byen vit — laperèz oswa prese.",
         "Yo vle yon transfè — lajan, yon kòd, oswa òdinatè ou."],
  never_head="PA JANM, PA MENM YON FWA",
  never=["Pa gen enstitisyon serye ki aksepte kat kado kòm peman.",
         "Bank ou pap janm mande ou retire lajan nan kont ou.",
         "Pa janm bay pèsonn yon kòd ou resevwa nan tèks.",
         "Pèsonn pa vin lakay ou pou ranmase kach oswa lò."],
  help_head="ÈD GRATIS — SAN JIJMAN",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Lin–Van"),
         ("877-908-3360", "AARP Fraud Watch  ·  Lin–Van")],
  report="Rapòte nan: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Si sa deja rive: se pa fòt ou, e li poko twò ta.",
  foot="Gratis pou kopye, enprime, ak pataje.",
  url="https://trustbutverifyproject.org/ht/")

L["pa"] = dict(brand="ਭਰੋਸਾ ਕਰੋ, ਪਰ ਪੁਸ਼ਟੀ ਕਰੋ",
  tagline="ਤੁਹਾਨੂੰ ਹਰ ਕਿਸੇ 'ਤੇ ਸ਼ੱਕ ਕਰਨ ਦੀ ਲੋੜ ਨਹੀਂ। ਬੱਸ ਇੱਕ ਕਦਮ ਜੋੜੋ।",
  steps_head="ਕੋਈ ਵੀ ਪੈਸਾ ਭੇਜਣ ਤੋਂ ਪਹਿਲਾਂ",
  steps=[("ਨੰਬਰ ਆਪ ਲੱਭੋ।", "ਉਹ ਨੰਬਰ ਨਹੀਂ ਜੋ ਦਿੱਤਾ ਗਿਆ। ਕਾਰਡ 'ਤੇ ਵਾਲਾ।"),
         ("ਵਿਅਕਤੀ ਨੂੰ ਆਪ ਕਾਲ ਕਰੋ।", "ਪਹਿਲਾਂ ਫ਼ੋਨ ਰੱਖੋ। ਫਿਰ ਕਾਲ ਕਰੋ।"),
         ("ਇੱਕ ਦਿਨ ਉਡੀਕ ਕਰੋ।", "ਅਸਲੀ ਮੁਸ਼ਕਲ ਇੱਕ ਰਾਤ ਦੀ ਨੀਂਦ ਤੋਂ ਬਚ ਜਾਂਦੀ ਹੈ।")],
  signs_head="ਤਿੰਨ ਸੰਕੇਤ ਜਿਨ੍ਹਾਂ ਨੂੰ ਰੋਕਣਾ ਚਾਹੀਦਾ ਹੈ",
  signs=["ਇਹ ਤੁਹਾਡੇ ਕੋਲ ਆਇਆ — ਤੁਸੀਂ ਸ਼ੁਰੂ ਨਹੀਂ ਕੀਤਾ।",
         "ਇਸ ਨੇ ਭਾਵਨਾਵਾਂ ਨੂੰ ਤੇਜ਼ੀ ਨਾਲ ਛੂਹਿਆ — ਡਰ ਜਾਂ ਕਾਹਲੀ।",
         "ਇਹ ਟ੍ਰਾਂਸਫਰ ਚਾਹੁੰਦਾ ਹੈ — ਪੈਸਾ, ਕੋਡ, ਜਾਂ ਕੰਪਿਊਟਰ।"],
  never_head="ਕਦੇ ਵੀ ਨਹੀਂ, ਇੱਕ ਵਾਰ ਵੀ ਨਹੀਂ",
  never=["ਕੋਈ ਵੀ ਸੰਸਥਾ ਗਿਫ਼ਟ ਕਾਰਡਾਂ ਨੂੰ ਭੁਗਤਾਨ ਵਜੋਂ ਸਵੀਕਾਰ ਨਹੀਂ ਕਰਦੀ।",
         "ਤੁਹਾਡਾ ਬੈਂਕ ਕਦੇ ਖਾਤੇ ਵਿੱਚੋਂ ਪੈਸੇ ਕਢਵਾਉਣ ਲਈ ਨਹੀਂ ਕਹੇਗਾ।",
         "ਟੈਕਸਟ ਰਾਹੀਂ ਮਿਲਿਆ ਕੋਡ ਕਦੇ ਕਿਸੇ ਨੂੰ ਨਾ ਦੱਸੋ।",
         "ਨਕਦੀ ਜਾਂ ਸੋਨਾ ਲੈਣ ਕੋਈ ਘਰ ਨਹੀਂ ਆਉਂਦਾ।"],
  help_head="ਮੁਫ਼ਤ ਮਦਦ — ਬਿਨਾਂ ਨਿਰਣੇ ਦੇ",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  ਸੋਮ–ਸ਼ੁੱਕਰ"),
         ("877-908-3360", "AARP Fraud Watch  ·  ਸੋਮ–ਸ਼ੁੱਕਰ")],
  report="ਰਿਪੋਰਟ ਕਰੋ: ic3.gov  ·  reportfraud.ftc.gov",
  footline="ਜੇ ਇਹ ਪਹਿਲਾਂ ਹੀ ਹੋ ਚੁੱਕਾ ਹੈ: ਇਹ ਤੁਹਾਡੀ ਗ਼ਲਤੀ ਨਹੀਂ ਹੈ।",
  foot="ਆਜ਼ਾਦੀ ਨਾਲ ਛਾਪੋ, ਕਾਪੀ ਕਰੋ ਅਤੇ ਸਾਂਝਾ ਕਰੋ।",
  url="https://trustbutverifyproject.org/pa/")

L["gu"] = dict(brand="વિશ્વાસ કરો, પણ ચકાસો",
  tagline="તમારે દરેક પર શંકા કરવાની જરૂર નથી. ફક્ત એક પગલું ઉમેરો.",
  steps_head="કોઈપણ પૈસા મોકલતા પહેલાં",
  steps=[("નંબર જાતે શોધો.", "તેમણે આપેલો નહીં. કાર્ડ પર જે છે તે."),
         ("વ્યક્તિને જાતે ફોન કરો.", "પહેલા ફોન મૂકી દો. પછી કૉલ કરો."),
         ("એક દિવસ રાહ જુઓ.", "સાચી સમસ્યા એક રાતની ઊંઘ પછી પણ રહે છે.")],
  signs_head="ત્રણ સંકેતો જે તમને રોકવા જોઈએ",
  signs=["તે તમારી પાસે આવ્યું — તમે શરૂ નથી કર્યું.",
         "તેણે લાગણીઓને ઝડપથી સ્પર્શ કરી — ડર અથવા ઉતાવળ.",
         "તે ટ્રાન્સફર ઇચ્છે છે — પૈસા, કોડ, અથવા કમ્પ્યુટર."],
  never_head="ક્યારેય નહીં, એક વાર પણ નહીં",
  never=["કોઈપણ સંસ્થા ગિફ્ટ કાર્ડને ચુકવણી તરીકે સ્વીકારતી નથી.",
         "તમારી બેંક ક્યારેય ખાતામાંથી પૈસા ઉપાડવાનું નહીં કહે.",
         "ટેક્સ્ટ દ્વારા મળેલો કોડ ક્યારેય કોઈને ન કહો.",
         "રોકડ અથવા સોનું લેવા કોઈ ઘરે આવતું નથી."],
  help_head="મફત મદદ — કોઈ નિર્ણય નહીં",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  સોમ–શુક્ર"),
         ("877-908-3360", "AARP Fraud Watch  ·  સોમ–શુક્ર")],
  report="જાણ કરો: ic3.gov  ·  reportfraud.ftc.gov",
  footline="જો આ પહેલેથી જ બની ચૂક્યું છે: આ તમારો વાંક નથી.",
  foot="મુક્તપણે છાપો, નકલ કરો અને શેર કરો.",
  url="https://trustbutverifyproject.org/gu/")

L["so"] = dict(brand="ISKA KALSOONOW, LAAKIIN XAQIIJI",
  tagline="Uma baahnid inaad ka shakiso qof kasta. Kaliya ku dar hal tallaabo.",
  steps_head="KA HOR INTA AAN LACAG LA DIRIN",
  steps=[("Nambarka naftaada raadi.", "Ma aha nambarka ay ku siiyeen. Ee ku qoran kaadhkaaga."),
         ("Naftaada u wac qofka.", "Marka hore xir taleefanka. Dabadeed wac."),
         ("Sug hal maalin.", "Dhibaato dhab ah waxay ka badbaadaa hal habeen oo hurdo ah.")],
  signs_head="SADDEX CALAAMADOOD OO LAGU JOOJIYO",
  signs=["Adigaa loo yeeray — mana bilaabin.",
         "Dareenkaaga si degdeg ah bay u taabteen — cabsi ama degdeg.",
         "Waxay rabaan wareejin — lacag, kood, ama kombiyuutarkaaga."],
  never_head="WALIGEED, XITAA HAL MAR",
  never=["Ma jiro machad sharci ah oo aqbala kaararka hadiyadda.",
         "Bangigaagu marnaba kuma weydiisan doono inaad lacag ka bixiso.",
         "Weligaa ha u sheegin qof kood aad ku heshay fariin qoraal ah.",
         "Ninna kuma iman doono guriga si uu u qaado lacag ama dahab."],
  help_head="CAAWIMAAD BILAASH AH — XUKUN LA'AAN",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Isniin–Jimce"),
         ("877-908-3360", "AARP Fraud Watch  ·  Isniin–Jimce")],
  report="Ka warbixi: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Haddii ay hore u dhacday: ma ihid kii qaladka lahaa.",
  foot="Bilaash u daabac, u koobiyee, oo u wadaag.",
  url="https://trustbutverifyproject.org/so/")

L["km"] = dict(brand="ជឿទុកចិត្ត ប៉ុន្តែផ្ទៀងផ្ទាត់",
  tagline="អ្នកមិនចាំបាច់សង្ស័យអ្នកគ្រប់គ្នាទេ។ គ្រាន់តែបន្ថែមជំហានមួយ។",
  steps_head="មុននឹងលុយណាមួយចេញ",
  steps=[("ស្វែងរកលេខដោយខ្លួនឯង។", "មិនមែនលេខដែលពួកគេឲ្យទេ។ លេខនៅលើកាត។"),
         ("ទូរស័ព្ទដោយខ្លួនឯង។", "ដាក់ទូរស័ព្ទចុះជាមុនសិន។ បន្ទាប់មកទូរស័ព្ទ។"),
         ("រង់ចាំមួយថ្ងៃ។", "បញ្ហាពិតអាចរស់រានពីមួយយប់នៃការគេង។")],
  signs_head="សញ្ញាបីយ៉ាងដែលគួរបញ្ឈប់អ្នក",
  signs=["វាមកដល់អ្នក — អ្នកមិនបានចាប់ផ្តើមទេ។",
         "វារំជើបអារម្មណ៍អ្នកយ៉ាងលឿន — ការភ័យខ្លាចឬការប្រញាប់។",
         "វាចង់បានការផ្ទេរ — លុយ កូដ ឬកុំព្យូទ័រ។"],
  never_head="មិនដែលឡើយ សូម្បីតែម្តង",
  never=["គ្មានស្ថាប័នស្របច្បាប់ណាទទួលកាតអំណោយជាការទូទាត់ទេ។",
         "ធនាគាររបស់អ្នកនឹងមិនដែលសុំឲ្យអ្នកដកលុយចេញពីគណនីទេ។",
         "កុំប្រាប់អ្នកណាម្នាក់ពីកូដដែលអ្នកបានទទួលតាមសារជាដាច់ខាត។",
         "គ្មាននរណាម្នាក់មកផ្ទះអ្នកដើម្បីយកលុយសុទ្ធឬមាសទេ។"],
  help_head="ជំនួយឥតគិតថ្លៃ — គ្មានការវិនិច្ឆ័យ",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  ច័ន្ទ–សុក្រ"),
         ("877-908-3360", "AARP Fraud Watch  ·  ច័ន្ទ–សុក្រ")],
  report="រាយការណ៍នៅ៖ ic3.gov  ·  reportfraud.ftc.gov",
  footline="ប្រសិនបើវាបានកើតឡើងរួចហើយ៖ វាមិនមែនជាកំហុសរបស់អ្នកទេ។",
  foot="សេរីភាពក្នុងការបោះពុម្ព ចម្លង និងចែករំលែក។",
  url="https://trustbutverifyproject.org/km/")

L["hmn"] = dict(brand="NTSEEG, TAB SIS XYUAS KOM POM TSEEB",
  tagline="Koj tsis tas yuav xav txhaus txog txhua tus neeg. Tsuas ntxiv ib kauj ruam.",
  steps_head="UA NTEJ YUAV XA NYIAJ TWG",
  steps=[("Nrhiav tus xov tooj koj tus kheej.", "Tsis yog tus lej lawv muab. Yog tus nyob ntawm koj daim card."),
         ("Hu tus neeg ntawd koj tus kheej.", "Tso tus xov tooj tso ua ntej. Ces mam li hu rov qab."),
         ("Tos ib hnub.", "Teeb meem tseeb yuav dhau ib hmo tsaug zog.")],
  signs_head="PEB YAM CIM UAS YUAV TSUM UA RAU KOJ NRES",
  signs=["Nws tuaj cuag koj — koj tsis yog tus pib.",
         "Nws tsim koj lub siab ceev ceev — kev ntshai los sis kev maj.",
         "Nws xav tau kev hloov — nyiaj, tus lej code, los sis lub computer."],
  never_head="YEEJ TSIS MUAJ, TXAWM YOG IB ZAUG LOS TSIS MUAJ",
  never=["Tsis muaj koom haum twg yuav txais daim gift card ua kev them nyiaj.",
         "Koj lub tsev txhab nyiaj yeej yuav tsis hais kom koj rho nyiaj tawm.",
         "Tsis txhob qhia leej twg paub tus lej code uas koj tau txais los ntawm xov xwm.",
         "Tsis muaj leej twg tuaj koj lub tsev los coj nyiaj ntsuab los sis kub."],
  help_head="KEV PAB DAWB — TSIS MUAJ KEV TXIAV TXIM",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Hli–Tim"),
         ("877-908-3360", "AARP Fraud Watch  ·  Hli–Tim")],
  report="Qhia rau: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Yog tias qhov no twb tshwm sim lawm: qhov no tsis yog koj lub txim.",
  foot="Thaij luam tawm, luam, thiab qhia dawb.",
  url="https://trustbutverifyproject.org/hmn/")

L["ka"] = dict(brand="ენდე, მაგრამ გადაამოწმე",
  tagline="არ არის საჭირო ყველას ეჭვის თვალით შეხედო. უბრალოდ დაამატე ერთი ნაბიჯი.",
  steps_head="სანამ რაიმე ფული გაიგზავნება",
  steps=[("ნომერი თავად მოძებნე.", "არა ის, რომელიც მოგცეს. ის, რომელიც ბარათზეა."),
         ("პირს თავად დაურეკე.", "ჯერ ჩაკეტე ზარი. შემდეგ დარეკე."),
         ("დაელოდე ერთ დღეს.", "ნამდვილი პრობლემა გაუძლებს ერთ ღამეს ძილს.")],
  signs_head="სამი ნიშანი, რომელმაც უნდა გაჩერო",
  signs=["ის შენთან მოვიდა — შენ არ დაგიწყია.",
         "სწრაფად შეგარყია გრძნობები — შიში ან ჩქარობა.",
         "სურს გადარიცხვა — ფული, კოდი, ან კომპიუტერი."],
  never_head="არასდროს, არც ერთხელ",
  never=["არცერთი დაწესებულება არ იღებს სასაჩუქრე ბარათებს გადახდის სახით.",
         "ბანკი არასდროს გთხოვს ანგარიშიდან ფულის გატანას.",
         "არასდროს გაუმხილო არავის ტექსტით მიღებული კოდი.",
         "არავინ მოდის სახლში ნაღდი ფულის ან ოქროს წასაღებად."],
  help_head="უფასო დახმარება — განსჯის გარეშე",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  ორშ–პარ"),
         ("877-908-3360", "AARP Fraud Watch  ·  ორშ–პარ")],
  report="აცნობე: ic3.gov  ·  reportfraud.ftc.gov",
  footline="ეს შენი ბრალი არ არის, და ჯერ არ არის გვიან.",
  foot="თავისუფლად დაბეჭდე, გადაიღე და გაავრცელე.",
  url="https://trustbutverifyproject.org/ka/")

def wrap(c, text, x, y, font, size, max_w, leading, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if stringWidth(test, font, size) > max_w and line:
            c.drawString(x, y, line)
            y -= leading
            line = word
        else:
            line = test
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


def draw(lang, d):
    import qrcode
    path = os.path.join(OUT, "fridge-sheet-%s.pdf" % lang)
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    y = H - M
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(INK)
    y = wrap(c, d["brand"], M, y - 26, "Helvetica-Bold", 26, W - 2 * M, 30)
    c.setFont("Helvetica", 11)
    c.setFillColor(MUTED)
    y = wrap(c, d["tagline"], M, y, "Helvetica", 11, W - 2 * M, 15)
    y -= 4
    c.setStrokeColor(INK); c.setLineWidth(2)
    c.line(M, y, W - M, y); y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    c.drawString(M, y, d["steps_head"]); y -= 22
    for i, (head, sub) in enumerate(d["steps"], 1):
        c.setFont("Helvetica-Bold", 22)
        c.setFillColor(ACCENT)
        c.drawString(M, y - 16, str(i))
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(INK)
        yy = wrap(c, head, M + 30, y - 8, "Helvetica-Bold", 13, W - 2 * M - 30, 16)
        yy = wrap(c, sub, M + 30, yy, "Helvetica", 9.5, W - 2 * M - 30, 12, color=MUTED)
        y = yy - 6
    y -= 6
    c.line(M, y, W - M, y); y -= 18

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    c.drawString(M, y, d["signs_head"]); y -= 16
    c.setFont("Helvetica", 10)
    for s in d["signs"]:
        y = wrap(c, "▪  " + s, M, y, "Helvetica", 10, W - 2 * M, 14)
    y -= 6

    box_top = y
    c.setFont("Helvetica-Bold", 10)
    box_y = y - 18
    lines_needed = sum(1 for _ in d["never"]) * 2 + 1
    box_h = 24 + lines_needed * 12
    c.setStrokeColor(INK); c.setLineWidth(2)
    c.rect(M, box_top - box_h, W - 2 * M, box_h, fill=0, stroke=1)
    ny = box_top - 16
    c.setFillColor(INK)
    c.drawString(M + 10, ny, d["never_head"]); ny -= 16
    c.setFont("Helvetica", 9.5)
    for n in d["never"]:
        ny = wrap(c, "×  " + n, M + 10, ny, "Helvetica", 9.5, W - 2 * M - 20, 12)
    y = box_top - box_h - 16

    c.line(M, y, W - M, y); y -= 20
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    c.drawString(M, y, d["help_head"]); y -= 18
    for phone, label in d["helps"]:
        c.setFont("Helvetica-Bold", 15)
        c.drawString(M, y, phone)
        c.setFont("Helvetica", 8.5)
        c.setFillColor(MUTED)
        c.drawString(M + 105, y + 1, label)
        c.setFillColor(INK)
        y -= 16
    c.setFont("Helvetica", 9)
    c.setFillColor(MUTED)
    y = wrap(c, d["report"], M, y, "Helvetica", 9, W - 2 * M, 12)
    y -= 4
    c.line(M, y, W - M, y); y -= 16

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(INK)
    y = wrap(c, d["footline"], M, y, "Helvetica-Bold", 10, W - 2 * M - 80, 13)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(MUTED)
    c.drawString(M, y, d["foot"])

    qr = qrcode.QRCode(border=1, box_size=10)
    qr.add_data(d["url"]); qr.make(fit=True)
    img = qr.make_image(fill_color="#123f7a", back_color="#fffdf9")
    qr_path = path + ".qr.png"
    img.save(qr_path)
    qsize = 62
    c.drawImage(qr_path, W - M - qsize, M - 6, width=qsize, height=qsize,
                preserveAspectRatio=True, mask="auto")
    c.setFont("Helvetica", 6.5)
    c.setFillColor(MUTED)
    c.drawRightString(W - M, M - 14, d["url"].replace("https://", ""))

    c.showPage()
    c.save()
    os.remove(qr_path)
    print("wrote", path)


if __name__ == "__main__":
    for lang, d in L.items():
        if d is None:
            continue
        draw(lang, d)
