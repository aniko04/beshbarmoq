"""«Texnologik diktantlar» topshiriqlari.

Manba: `malumotlar/topshiriqlar/Texnologik diktantlar (2).docx` — 4 variant,
har birida 4 ta topshiriq (jami 16). Har topshiriqda 1–4 raqami bilan
raqamlangan to'rtta rasm va to'rtta nom bor; o'quvchi har bir nomga mos
rasm raqamini qo'yadi.

To'rt variant sahifada TO'RT BOSQICH bo'lib chiqadi va ketma-ket yechiladi:
bosqich tekshirilgandan keyin keyingisi ochiladi (natijasi past bo'lsa ham —
o'quvchi tiqilib qolmasin). Har bosqichning o'z vaqti bor va natijasi
alohida saqlanadi (`Result.MASHQ_CHOICES` dagi `dikt1`…`dikt4`).

Rasmlar Word ichidan `static/img/diktant/v{variant}s{savol}_{raqam}.jpg`
ko'rinishida olingan. Rasmli testdagi qoidalar bu yerda ham amal qiladi:

  * Worddagi JPEG'lar — bayti o'zgarishsiz nusxa (qayta siqilmaydi);
  * PNG fotosuratlar — JPEG q92, klipart esa q97 va subsampling=0;
  * shaffof joylar oqqa yotqiziladi (aks holda brauzerda qora bo'lib chiqadi);
  * rasm HECH QACHON kattalashtirilmaydi — manbalar 150–700px, shuning uchun
    sahifada tabiiy o'lchamida turadi;
  * kengaytma hammasida bir xil (.jpg), nom esa faqat variant/savol/raqamga
    bog'liq — shunda rasmlar qayta yasalganda manzillar siljib ketmaydi.

Word ichida bir xil rasm bir necha variantda qayta ishlatilgan (masalan
"Qog'oz turlari" to'rttala variantda ham bor); ular har bir o'rin uchun
alohida faylga nusxalanadi, ya'ni 64 ta fayl.

JAVOB KALITI Wordning o'zida bor edi (har topshiriqdagi "nom | raqam"
jadvalining ikkinchi ustuni), shuning uchun taxmin qilishga hojat bo'lmadi.
Bitta joyda Wordning o'zi ziddiyatli: 1-variant 3-topshiriqda "Gazeta"
va "Yozuv qog'oz" javoblari almashib ketgan (1-rasm — daftar, 4-rasm —
gazeta), holbuki 3-variant 1-topshiriqda AYNAN SHU ikki rasm to'g'ri
belgilangan. Quyida tuzatilgan; mijoz e'tiroz bildirsa, o'sha ikki
raqamni qaytarish yetarli — boshqa hech narsaga tegmaydi.
"""

import random
from pathlib import Path

QATOR_BALL = 5           # har bir mos qator uchun ball
BOSQICH_DAQIQA = 5       # har bosqichga beriladigan vaqt
RASM_YOL = '/static/img/diktant/'
RASM_VERSIYA = 1         # rasm almashtirilganda oshiriladi (brauzer keshi uchun)
RASM_KATALOG = Path(__file__).resolve().parent.parent / 'static' / 'img' / 'diktant'

BOSQICH_NOMLARI = {
    1: "I bosqich",
    2: "II bosqich",
    3: "III bosqich",
    4: "IV bosqich",
}

# (variant, topshiriq nomeri, savol matni, [(nom, to'g'ri rasm raqami), ...])
# Matnlar Worddan o'zgartirilmasdan olingan (faqat ortiqcha bo'sh joylar tozalangan).
_XOM = [
    (1, 1, "Qogʻozdan turli usullarda kompozitsiyalar yasalgan. Ulardan mosini toping hamda raqamlang?", [
        ("Applikatsiya usulida yasalgan tasvir", 1),
        ("Geometrik shaklli applikatsiya tasviri", 2),
        ("Qogʻozni buklash orqali yasalgan tasvir", 3),
        ("Mozaika usulida yasalgan tasvir", 4),
    ]),
    (1, 2, "Qogʻozdan turli usullarda kompozitsiyalar mosini toping, hamda raqamlang.", [
        ("Applikatsiya usulida yasalgan tasvir", 4),
        ("Kvilling usulida yasalgan tasvir", 3),
        ("Pape-mashe usulida yasalgan tasvir", 1),
        ("Mozaika usulida yasalgan tasvir", 2),
    ]),
    (1, 3, "Qogʻoz turlaridan mosini toping, hamda raqamlang.", [
        ("Gazeta qogʻoz", 4),          # Worddagi kalit tuzatildi (yuqoridagi izohga qarang)
        ("Rangli karton qogʻoz", 2),
        ("Ajurli karton qogʻoz", 3),
        ("Yozuv qogʻoz", 1),           # Worddagi kalit tuzatildi
    ]),
    (1, 4, "Turli materiallardan applikatsiyalar mosini toping, hamda raqamlang.", [
        ("Toʻqish iplaridan bajarilgan applikatsiya kompozitsiya", 4),
        ("Barglardan bajarilgan applikatsiya kompozitsiya", 1),
        ("Biser va toshlardan bajarilgan applikatsiya kompozitsiya", 2),
        ("Rangli qogʻozdan applikatsiya kompozitsiyasi", 3),
    ]),
    (2, 1, "Qogʻoz turlaridan mosini toping, hamda raqamlang.", [
        ("Gazeta qogʻoz", 4),
        ("Rangli karton qogʻoz", 2),
        ("Ajurli karton qogʻoz", 3),
        ("Chizmachilik qogʻoz", 1),
    ]),
    (2, 2, "Turli materiallardan applikatsiyalar mosini toping, hamda raqamlang.", [
        ("Gazlama boʻlaklaridan bajarilgan applikatsiya kompozitsiya", 1),
        ("Barglardan bajarilgan applikatsiya kompozitsiya", 3),
        ("Urugʻlardan bajarilgan applikatsiya kompozitsiya", 4),
        ("Somondan bajarilgan applikatsiya kompozitsiyasi", 2),
    ]),
    (2, 3, "Qogʻozdan turli usullarda yasalgan kompozitsiyalar mosini toping hamda raqamlang.", [
        ("Applikatsiya usulida yasalgan tasvir", 4),
        ("Kvilling usulida yasalgan tasvir", 2),
        ("Pape-mashe usulida yasalgan tasvir", 1),
        ("Mozaika usulida yasalgan tasvir", 3),
    ]),
    (2, 4, "Robotlarning vazifasi toʻgʻri koʻrsatilgan raqamni belgilang?", [
        ("Avtomobil yigʻuvchi", 4),
        ("Dazmollovchi", 3),
        ("Ofisiant", 1),
        ("Oshpaz", 2),
    ]),
    (3, 1, "Qogʻoz turlaridan mosini toping, hamda raqamlang.", [
        ("Gazeta qogʻoz", 4),
        ("Qayta ishlangan qogʻoz", 2),
        ("Shagren naqshdor qogʻoz", 3),
        ("Yozuv qogʻoz", 1),
    ]),
    (3, 2, "Kasblarni mosini toping, hamda raqamlang.", [
        ("Oʻt ochiruvchi", 2),
        ("Styuardessa", 3),
        ("Fotosuratchi", 4),
        ("Sapyor", 1),
    ]),
    (3, 3, "Tabiiy materiallardan kompozitsiyalar nomini toping, hamda raqamlang?", [
        ("Qushlarning patlari", 4),
        ("Gʻuddalar", 2),
        ("Yongʻoqlar", 1),
        ("Makkajoʻxori", 3),
    ]),
    (3, 4, "Robotlarning vazifasi toʻgʻri koʻrsatilgan raqamni belgilang?", [
        ("Politsiya xodimi", 2),
        ("Idish yuvish mashinasi", 3),
        ("Askar", 4),
        ("Qadoqlovchi", 1),
    ]),
    (4, 1, "Qogʻoz turlaridan mosini toping, hamda raqamlang.", [
        ("Karton qogʻoz", 4),
        ("Rangli va jiloli qogʻoz", 2),
        ("Ajurli karton qogʻoz", 3),
        ("Chizmachilik qogʻoz", 1),
    ]),
    (4, 2, "Robotlarning vazifasi toʻgʻri koʻrsatilgan raqamni belgilang?", [
        ("Quruvchi", 3),
        ("Politsiya xodimi", 4),
        ("Ofisiant", 2),
        ("Payvandchi", 1),
    ]),
    (4, 3, "Turli materiallardan mozaika kompozitsiyalari nomini toping, hamda raqamlang?", [
        ("Plastilindan bajarilgan mozaika sanʼati", 4),
        ("Qalam qipiqlaridan bajarilgan mozaika", 2),
        ("Tugmalardan bajarilgan mozaika", 1),
        ("Qogʻoz turlaridan bajarilgan mozaika", 3),
    ]),
    (4, 4, "Ish anjomlari?", [
        ("Duradgorlik", 3),
        ("Tasviriy sanʼat", 4),
        ("Tabiiy materiallar bilan ishlash", 2),
        ("Gazlama bilan ishlashda", 1),
    ]),
]

RAQAMLAR = [1, 2, 3, 4]
BOSQICH_SONI = 4

_KESH = None


def _savol_id(variant, nomer):
    """Sahifa va JS uchun barqaror kalit: 'v1s3'."""
    return f'v{variant}s{nomer}'


def _rasm(variant, nomer, raqam):
    """Rasm manzili.

    Oxiridagi `?v=` — brauzer keshini yangilash uchun: fayl o'sha nom bilan
    almashtirilsa, `RASM_VERSIYA` ni oshiring, aks holda ba'zi brauzerlar
    eski rasmni ko'rsatib turaveradi.
    """
    return f'{RASM_YOL}v{variant}s{nomer}_{raqam}.jpg?v={RASM_VERSIYA}'


def _fayl_nomi(variant, nomer, raqam):
    return f'v{variant}s{nomer}_{raqam}.jpg'


def yetishmagan_rasmlar():
    """Diskda yo'q rasmlar ro'yxati — `manage.py check` shuni ogohlantiradi."""
    return [
        _fayl_nomi(v, n, r)
        for v, n, _, _ in _XOM
        for r in RAQAMLAR
        if not (RASM_KATALOG / _fayl_nomi(v, n, r)).exists()
    ]


def bosqichlar():
    """Shablon uchun tayyor ro'yxat (bir marta yig'ilib, keshlanadi)."""
    global _KESH
    if _KESH is not None:
        return _KESH

    guruh = {}
    for variant, nomer, matn, qatorlar in _XOM:
        guruh.setdefault(variant, []).append({
            'id': _savol_id(variant, nomer),
            'nomer': nomer,
            'savol': matn,
            'ball': len(qatorlar) * QATOR_BALL,
            'rasmlar': [
                {'raqam': r, 'rasm': _rasm(variant, nomer, r)}
                for r in RAQAMLAR
            ],
            'qatorlar': [
                {'nomer': i, 'yorliq': yorliq, 'javob': javob}
                for i, (yorliq, javob) in enumerate(qatorlar)
            ],
        })

    chiqish = []
    for variant in sorted(guruh):
        savollar = guruh[variant]
        qator = sum(len(s['qatorlar']) for s in savollar)
        chiqish.append({
            'raqam': variant,
            'nomi': BOSQICH_NOMLARI.get(variant, f'{variant}-bosqich'),
            'kalit': natija_kaliti(variant),
            'daqiqa': BOSQICH_DAQIQA,
            'savollar': savollar,
            'qator': qator,
            'ball': qator * QATOR_BALL,
        })
    _KESH = chiqish
    return chiqish


def aralashtirilgan(rnd=None):
    """`bosqichlar()` ning har sahifa ochilishida qayta aralashtirilgan nusxasi.

    Worddan olingan tartibda javoblar ko'zga tashlanadigan darajada bir xil
    edi (masalan qog'oz turlari topshiriqlarining hammasida 4-2-3-1, birinchi
    topshiriqda esa to'g'ridan-to'g'ri 1-2-3-4), ya'ni o'quvchi rasmga
    qaramasdan ham topib olardi. Shuning uchun har topshiriqda IKKI narsa
    aralashadi:

      1. rasmlarning raqamlari — qaysi rasm 1, qaysisi 4 bo'lishi;
      2. nom qatorlarining tartibi.

    Javob kaliti shu yerda birga hisoblanadi (`javob_kaliti()` ga aynan shu
    ro'yxat berilishi shart), aks holda sahifadagi kalit boshqa tartibda
    bo'lib, hamma javob xato chiqadi.

    `_KESH` dagi asl ma'lumot o'zgarmaydi — har savol uchun yangi ro'yxat
    yasaladi, matn va rasm manzillari esa o'sha-o'sha.
    """
    rnd = rnd or random.Random()
    chiqish = []
    for bosqich in bosqichlar():
        savollar = []
        for savol in bosqich['savollar']:
            # tartib[k-1] = k-o'rinda turadigan rasmning ASL raqami
            tartib = list(RAQAMLAR)
            rnd.shuffle(tartib)
            yangi_raqam = {asl: yangi for yangi, asl in enumerate(tartib, 1)}

            rasmlar = [
                {'raqam': yangi, 'rasm': savol['rasmlar'][asl - 1]['rasm']}
                for yangi, asl in enumerate(tartib, 1)
            ]

            qatorlar = list(savol['qatorlar'])
            # 24 ta joylashuvdan 2 tasi — 1-2-3-4 va 4-3-2-1 — tasodif bo'lsa
            # ham "aralashtirilmagan" bo'lib ko'rinadi, shuning uchun ular
            # qaytadan tashlanadi (urinish soni cheklangan, sikl qotib
            # qolmaydi; qator soni 2 dan kam bo'lsa shart baribir bajarilmaydi).
            for _ in range(20):
                rnd.shuffle(qatorlar)
                javoblar = [yangi_raqam[q['javob']] for q in qatorlar]
                if javoblar != sorted(javoblar) and javoblar != sorted(javoblar, reverse=True):
                    break

            qatorlar = [
                {'nomer': i, 'yorliq': q['yorliq'], 'javob': yangi_raqam[q['javob']]}
                for i, q in enumerate(qatorlar)
            ]

            savollar.append(dict(savol, rasmlar=rasmlar, qatorlar=qatorlar))
        chiqish.append(dict(bosqich, savollar=savollar))
    return chiqish


def javob_kaliti(manba=None):
    """{savol id: [to'g'ri raqamlar]} — sahifadagi JS shu bilan tekshiradi.

    `manba` — `aralashtirilgan()` qaytargan ro'yxat. Berilmasa asl (aralashmagan)
    tartib olinadi; sahifa ALBATTA o'zi ko'rsatayotgan ro'yxatni uzatishi kerak.
    """
    if manba is None:
        manba = bosqichlar()
    return {
        savol['id']: [q['javob'] for q in savol['qatorlar']]
        for bosqich in manba
        for savol in bosqich['savollar']
    }


def natija_kaliti(variant):
    """`Result.mashq` uchun kalit: 1-bosqich → 'dikt1'."""
    return f'dikt{variant}'


def bosqich_ball():
    """Bitta bosqichning to'liq bali (hamma bosqichda bir xil)."""
    return bosqichlar()[0]['ball']


def jami_ball():
    return sum(len(q) for _, _, _, q in _XOM) * QATOR_BALL


def jami_qator():
    return sum(len(q) for _, _, _, q in _XOM)
