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

L["it"] = dict(brand="FIDATI, MA VERIFICA",
  tagline="Non serve sospettare di tutti. Basta aggiungere un passo.",
  steps_head="PRIMA DI INVIARE QUALSIASI SOMMA",
  steps=[("Cerchi il numero da solo.", "Non quello che le hanno dato. Quello sulla carta."),
         ("Chiami la persona da solo.", "Riagganci prima. Poi richiami."),
         ("Aspetti un giorno.", "Un problema vero sopravvive a una notte di sonno.")],
  signs_head="TRE SEGNALI CHE DEVONO FERMARLA",
  signs=["È arrivata a lei — non l'ha iniziata lei.",
         "Ha toccato le emozioni velocemente — paura o fretta.",
         "Vuole un trasferimento — denaro, un codice, o il computer."],
  never_head="MAI, NEMMENO UNA VOLTA",
  never=["Nessuna istituzione accetta carte regalo come pagamento.",
         "La sua banca non le chiederà mai di prelevare denaro.",
         "Non dica mai a nessuno un codice ricevuto via messaggio.",
         "Nessuno viene a casa sua per ritirare contanti o oro."],
  help_head="AIUTO GRATUITO — SENZA GIUDIZIO",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Lun–Ven"),
         ("877-908-3360", "AARP Fraud Watch  ·  Lun–Ven")],
  report="Segnali a: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Se è già successo: non è colpa sua, e non è troppo tardi.",
  foot="Libero da stampare, copiare e condividere.",
  url="https://trustbutverifyproject.org/it/")

L["el"] = dict(brand="ΕΜΠΙΣΤΕΥΣΟΥ, ΑΛΛΑ ΕΠΑΛΗΘΕΥΣΕ",
  tagline="Δεν χρειάζεται να υποψιάζεστε τον καθένα. Προσθέστε ένα βήμα.",
  steps_head="ΠΡΙΝ ΣΤΑΛΟΥΝ ΧΡΗΜΑΤΑ",
  steps=[("Βρείτε τον αριθμό μόνοι σας.", "Όχι αυτόν που σας έδωσαν. Αυτόν στην κάρτα σας."),
         ("Καλέστε το άτομο μόνοι σας.", "Κλείστε πρώτα. Μετά καλέστε."),
         ("Περιμένετε μία ημέρα.", "Ένα πραγματικό πρόβλημα επιβιώνει μια νύχτα ύπνου.")],
  signs_head="ΤΡΙΑ ΣΗΜΑΔΙΑ ΠΟΥ ΠΡΕΠΕΙ ΝΑ ΣΑΣ ΣΤΑΜΑΤΗΣΟΥΝ",
  signs=["Ήρθε σε εσάς — δεν το ξεκινήσατε εσείς.",
         "Άγγιξε γρήγορα τα συναισθήματά σας — φόβο ή βιασύνη.",
         "Θέλει μεταφορά — χρήματα, κωδικό, ή τον υπολογιστή σας."],
  never_head="ΠΟΤΕ, ΟΥΤΕ ΜΙΑ ΦΟΡΑ",
  never=["Κανένας νόμιμος οργανισμός δεν δέχεται δωροκάρτες.",
         "Η τράπεζά σας δεν θα ζητήσει ποτέ να βγάλετε χρήματα.",
         "Ποτέ μην πείτε σε κανέναν έναν κωδικό από μήνυμα.",
         "Κανείς δεν έρχεται στο σπίτι σας για μετρητά ή χρυσό."],
  help_head="ΔΩΡΕΑΝ ΒΟΗΘΕΙΑ — ΧΩΡΙΣ ΚΡΙΤΙΚΗ",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Δευ–Παρ"),
         ("877-908-3360", "AARP Fraud Watch  ·  Δευ–Παρ")],
  report="Αναφορά: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Αν έχει ήδη συμβεί: δεν φταίτε εσείς, και δεν είναι πολύ αργά.",
  foot="Ελεύθερο για εκτύπωση, αντιγραφή και διαμοιρασμό.",
  url="https://trustbutverifyproject.org/el/")

L["he"] = dict(brand="תבטח, אבל תוודא",
  tagline="אתה לא צריך לחשוד בכולם. פשוט תוסיף שלב אחד.",
  steps_head="לפני שכסף כלשהו יוצא",
  steps=[("חפש את המספר בעצמך.", "לא את המספר שנתנו לך. את זה שעל הכרטיס."),
         ("תתקשר בעצמך.", "תנתק קודם. אחר כך תתקשר."),
         ("חכה יום אחד.", "בעיה אמיתית שורדת לילה של שינה.")],
  signs_head="שלושה סימנים שצריכים לעצור אותך",
  signs=["זה הגיע אליך — אתה לא התחלת.",
         "זה נגע ברגשות שלך מהר — פחד או חיפזון.",
         "זה רוצה העברה — כסף, קוד, או המחשב שלך."],
  never_head="אף פעם, אפילו לא פעם אחת",
  never=["אף מוסד לגיטימי לא מקבל כרטיסי מתנה כתשלום.",
         "הבנק שלך לעולם לא יבקש למשוך כסף מהחשבון.",
         "לעולם אל תגיד קוד שקיבלת בהודעת טקסט.",
         "אף אחד לא בא לביתך לאסוף מזומן או זהב."],
  help_head="עזרה חינם — בלי שיפוט",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  שני–שישי"),
         ("877-908-3360", "AARP Fraud Watch  ·  שני–שישי")],
  report="דווח ב: ic3.gov  ·  reportfraud.ftc.gov",
  footline="אם זה כבר קרה: זו לא אשמתך, ועדיין לא מאוחר מדי.",
  foot="חופשי להעתקה, הדפסה ושיתוף.",
  url="https://trustbutverifyproject.org/he/")

L["hu"] = dict(brand="BÍZZ, DE ELLENŐRIZZ",
  tagline="Nem kell mindenkit gyanúsítania. Csak adjon hozzá egy lépést.",
  steps_head="MIELŐTT BÁRMILYEN PÉNZ ELMENNE",
  steps=[("Keresse meg maga a számot.", "Ne azt, amit adtak. Ami a kártyáján van."),
         ("Hívja fel maga a személyt.", "Először tegye le. Aztán hívja."),
         ("Várjon egy napot.", "Egy valódi probléma túlél egy éjszakai alvást.")],
  signs_head="HÁROM JEL, AMI MEG KELL HOGY ÁLLÍTSA",
  signs=["Önhöz érkezett — nem ön kezdeményezte.",
         "Gyorsan megérintette érzelmeit — félelmet vagy sietséget.",
         "Átutalást akar — pénzt, kódot, vagy a számítógépét."],
  never_head="SOHA, EGYSZER SEM",
  never=["Egyetlen intézmény sem fogad el ajándékkártyát fizetségként.",
         "A bankja soha nem kéri, hogy vegyen ki pénzt.",
         "Soha ne mondjon el kódot szöveges üzenetből.",
         "Senki nem jön el önhöz készpénzért vagy aranyért."],
  help_head="INGYENES SEGÍTSÉG — ÍTÉLKEZÉS NÉLKÜL",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  H–P"),
         ("877-908-3360", "AARP Fraud Watch  ·  H–P")],
  report="Jelentse: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Ha ez már megtörtént: nem az ön hibája, és még nem késő.",
  foot="Szabadon másolható, nyomtatható és megosztható.",
  url="https://trustbutverifyproject.org/hu/")

L["hr"] = dict(brand="VJERUJ, ALI PROVJERI",
  tagline="Ne morate sumnjati u svakoga. Samo dodajte jedan korak.",
  steps_head="PRIJE NEGO ŠTO BILO KOJI NOVAC ODE",
  steps=[("Sami pronađite broj.", "Ne onaj koji su vam dali. Onaj na kartici."),
         ("Sami nazovite osobu.", "Prvo prekinite poziv. Zatim nazovite."),
         ("Pričekajte jedan dan.", "Pravi problem preživi jednu noć sna.")],
  signs_head="TRI ZNAKA KOJA BI TREBALA ZAUSTAVITI VAS",
  signs=["Došlo je vama — vi to niste započeli.",
         "Brzo je dotaklo vaše osjećaje — strah ili žurbu.",
         "Želi transfer — novac, kod, ili vaše računalo."],
  never_head="NIKADA, NI JEDNOM",
  never=["Nijedna institucija ne prihvaća poklon kartice kao plaćanje.",
         "Vaša banka nikada neće tražiti da podignete novac.",
         "Nikada nikome ne recite kod iz tekstualne poruke.",
         "Nitko ne dolazi vama kući po gotovinu ili zlato."],
  help_head="BESPLATNA POMOĆ — BEZ OSUĐIVANJA",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Pon–Pet"),
         ("877-908-3360", "AARP Fraud Watch  ·  Pon–Pet")],
  report="Prijavite na: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Ako se to već dogodilo: to nije vaša krivnja, i još nije prekasno.",
  foot="Slobodno za ispis, kopiranje i dijeljenje.",
  url="https://trustbutverifyproject.org/hr/")

L["sr"] = dict(brand="ВЕРУЈ, АЛИ ПРОВЕРИ",
  tagline="Не морате да сумњате у свакога. Само додајте један корак.",
  steps_head="ПРЕ НЕГО ШТО БИЛО КАКАВ НОВАЦ ОДЕ",
  steps=[("Сами пронађите број.", "Не онај који су вам дали. Онај на картици."),
         ("Сами позовите особу.", "Прво прекините позив. Затим позовите."),
         ("Сачекајте један дан.", "Прави проблем преживи једну ноћ сна.")],
  signs_head="ТРИ ЗНАКА КОЈА ТРЕБА ДА ВАС ЗАУСТАВЕ",
  signs=["Дошло је вама — ви то нисте започели.",
         "Брзо је додирнуло ваша осећања — страх или журбу.",
         "Жели трансфер — новац, код, или ваш рачунар."],
  never_head="НИКАДА, НИ ЈЕДНОМ",
  never=["Ниједна институција не прихвата поклон картице као плаћање.",
         "Ваша банка никада неће тражити да подигнете новац.",
         "Никада никоме не реците код из текстуалне поруке.",
         "Нико не долази вама кући по готовину или злато."],
  help_head="БЕСПЛАТНА ПОМОЋ — БЕЗ ОСУЂИВАЊА",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Пон–Пет"),
         ("877-908-3360", "AARP Fraud Watch  ·  Пон–Пет")],
  report="Пријавите на: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Ако се то већ догодило: то није ваша кривица, и још није прекасно.",
  foot="Слободно за штампу, копирање и дељење.",
  url="https://trustbutverifyproject.org/sr/")

L["ms"] = dict(brand="PERCAYA, TETAPI SAHKAN",
  tagline="Anda tidak perlu mengesyaki semua orang. Cuma tambah satu langkah.",
  steps_head="SEBELUM MANA-MANA WANG DIHANTAR",
  steps=[("Cari sendiri nombor itu.", "Bukan nombor yang diberikan. Yang ada pada kad."),
         ("Telefon sendiri orang itu.", "Letak telefon dahulu. Kemudian telefon semula."),
         ("Tunggu satu hari.", "Masalah sebenar bertahan selepas semalaman tidur.")],
  signs_head="TIGA TANDA YANG PATUT MENGHENTIKAN ANDA",
  signs=["Ia datang kepada anda — anda tidak memulakannya.",
         "Ia menyentuh perasaan anda dengan cepat — ketakutan atau tergesa-gesa.",
         "Ia mahukan pemindahan — wang, kod, atau komputer anda."],
  never_head="JANGAN SESEKALI, WALAUPUN SEKALI",
  never=["Tiada institusi sah menerima kad hadiah sebagai bayaran.",
         "Bank anda tidak akan meminta anda mengeluarkan wang.",
         "Jangan sesekali beritahu sesiapa kod daripada SMS.",
         "Tiada sesiapa datang ke rumah anda untuk wang tunai atau emas."],
  help_head="BANTUAN PERCUMA — TANPA PENGHAKIMAN",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Isn–Jum"),
         ("877-908-3360", "AARP Fraud Watch  ·  Isn–Jum")],
  report="Laporkan di: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Jika ini sudah berlaku: ini bukan salah anda, dan belum terlambat.",
  foot="Bebas untuk cetak, salin dan kongsi.",
  url="https://trustbutverifyproject.org/ms/")

L["sv"] = dict(brand="LITA PÅ, MEN KONTROLLERA",
  tagline="Du behöver inte misstänka alla. Lägg bara till ett steg.",
  steps_head="INNAN NÅGRA PENGAR SKICKAS",
  steps=[("Slå upp numret själv.", "Inte numret de gav dig. Det på ditt kort."),
         ("Ring personen själv.", "Lägg på först. Ring sedan."),
         ("Vänta en dag.", "Ett riktigt problem överlever en natts sömn.")],
  signs_head="TRE TECKEN SOM BORDE STOPPA DIG",
  signs=["Det kom till dig — du startade det inte.",
         "Det rörde dina känslor snabbt — rädsla eller brådska.",
         "Det vill ha en överföring — pengar, kod, eller din dator."],
  never_head="ALDRIG, INTE EN ENDA GÅNG",
  never=["Ingen institution accepterar presentkort som betalning.",
         "Din bank kommer aldrig be dig ta ut pengar.",
         "Berätta aldrig en kod du fått via sms.",
         "Ingen kommer hem till dig för kontanter eller guld."],
  help_head="GRATIS HJÄLP — UTAN ATT DÖMA",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Mån–Fre"),
         ("877-908-3360", "AARP Fraud Watch  ·  Mån–Fre")],
  report="Rapportera: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Om det redan har hänt: det är inte ditt fel, och det är inte för sent.",
  foot="Fritt att kopiera, skriva ut och dela.",
  url="https://trustbutverifyproject.org/sv/")

L["no"] = dict(brand="STOL PÅ, MEN KONTROLLER",
  tagline="Du trenger ikke mistenke alle. Bare legg til ett steg.",
  steps_head="FØR NOEN PENGER SENDES",
  steps=[("Slå opp nummeret selv.", "Ikke nummeret de ga deg. Det på kortet ditt."),
         ("Ring personen selv.", "Legg på først. Ring så tilbake."),
         ("Vent en dag.", "Et ekte problem overlever en natts søvn.")],
  signs_head="TRE TEGN SOM BØR STOPPE DEG",
  signs=["Det kom til deg — du startet det ikke.",
         "Det rørte følelsene dine raskt — frykt eller hastverk.",
         "Det vil ha en overføring — penger, kode, eller datamaskinen din."],
  never_head="ALDRI, IKKE EN ENESTE GANG",
  never=["Ingen institusjon godtar gavekort som betaling.",
         "Banken din vil aldri be deg ta ut penger.",
         "Fortell aldri noen en kode du fikk på SMS.",
         "Ingen kommer hjem til deg for kontanter eller gull."],
  help_head="GRATIS HJELP — UTEN FORDØMMELSE",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Man–Fre"),
         ("877-908-3360", "AARP Fraud Watch  ·  Man–Fre")],
  report="Rapporter: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Hvis dette allerede har skjedd: det er ikke din skyld, ikke for sent.",
  foot="Fritt å kopiere, skrive ut og dele.",
  url="https://trustbutverifyproject.org/no/")

L["da"] = dict(brand="STOL PÅ, MEN KONTROLLER",
  tagline="Du behøver ikke mistænke alle. Tilføj bare ét trin.",
  steps_head="FØR NOGEN PENGE SENDES",
  steps=[("Find selv nummeret.", "Ikke det nummer de gav dig. Det på kortet."),
         ("Ring selv til personen.", "Læg først på. Ring så tilbage."),
         ("Vent en dag.", "Et rigtigt problem overlever en nats søvn.")],
  signs_head="TRE TEGN, DER BØR STOPPE DIG",
  signs=["Det kom til dig — du startede det ikke.",
         "Det rørte hurtigt dine følelser — frygt eller hastværk.",
         "Det vil have en overførsel — penge, kode, eller din computer."],
  never_head="ALDRIG, IKKE ÉN GANG",
  never=["Ingen institution accepterer gavekort som betaling.",
         "Din bank vil aldrig bede dig hæve penge fra kontoen.",
         "Fortæl aldrig nogen en kode fra en sms.",
         "Ingen kommer hjem til dig for kontanter eller guld."],
  help_head="GRATIS HJÆLP — UDEN FORDØMMELSE",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Man–Fre"),
         ("877-908-3360", "AARP Fraud Watch  ·  Man–Fre")],
  report="Anmeld: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Hvis dette allerede er sket: det er ikke din skyld, ikke for sent.",
  foot="Frit at kopiere, udskrive og dele.",
  url="https://trustbutverifyproject.org/da/")

L["sw"] = dict(brand="AMINI, LAKINI THIBITISHA",
  tagline="Huhitaji kushuku kila mtu. Ongeza tu hatua moja.",
  steps_head="KABLA YA FEDHA YOYOTE KUTUMWA",
  steps=[("Tafuta nambari mwenyewe.", "Si nambari waliyokupa. Ile iliyo kwenye kadi."),
         ("Mpigie mtu simu mwenyewe.", "Kata simu kwanza. Kisha piga tena."),
         ("Subiri siku moja.", "Tatizo la kweli huvumilia usiku mmoja wa kulala.")],
  signs_head="ISHARA TATU ZINAZOPASWA KUKUSIMAMISHA",
  signs=["Ilikujia — hukuianzisha wewe.",
         "Iligusa hisia zako haraka — hofu au haraka.",
         "Inataka uhamishaji — fedha, msimbo, au kompyuta."],
  never_head="KAMWE, HATA MARA MOJA",
  never=["Hakuna taasisi halali inayokubali kadi za zawadi.",
         "Benki yako haitawahi kukuomba kutoa fedha.",
         "Kamwe usimwambie mtu msimbo wa ujumbe wa maandishi.",
         "Hakuna anayekuja nyumbani kwako kwa fedha au dhahabu."],
  help_head="MSAADA WA BURE — BILA KUHUKUMU",
  helps=[("833-372-8311", "National Elder Fraud Hotline  ·  Jumatatu–Ijumaa"),
         ("877-908-3360", "AARP Fraud Watch  ·  Jumatatu–Ijumaa")],
  report="Ripoti: ic3.gov  ·  reportfraud.ftc.gov",
  footline="Ikiwa hili tayari limetokea: si kosa lako, na bado haijachelewa.",
  foot="Huru kunakili, kuchapisha na kushiriki.",
  url="https://trustbutverifyproject.org/sw/")


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
