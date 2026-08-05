"""«Rasmli test» savollari.

Manba: `malumotlar/topshiriqlar/Rasmli test.docx` (2–4-sinf o'quvchilari uchun,
20 daqiqa, 15 topshiriq, jami 165 ball).

Rasmlar o'sha Word ichidan `static/img/rasmli-test/sNN{a,b,s}.jpg` ko'rinishida
olingan. Worddagi rasmlarning hammasi kichkina (180–320px), shuning uchun ular
kattalashtirilmaydi — sahifada tabiiy o'lchamida ko'rsatiladi.

  * Worddagi JPEG'lar — bayti o'zgarishsiz nusxa (qayta siqilmaydi);
  * PNG fotosuratlar — JPEG q92;
  * klipart va anjomlar panjarasi — JPEG q97, rang siqilishisiz (subsampling=0),
    shunda tekis fonda JPEG shovqini ko'rinmaydi;
  * shaffof joylar oqqa qo'yiladi (aks holda brauzerda qora bo'lib chiqadi);
  * 13-topshiriqda bitta variantda bir nechta anjom bor — ular bitta oq
    varaqqa panjara qilib joylangan.

Kengaytma ATAYLAB hammasida bir xil (.jpg): avval klipartlar .png edi va
rasmlar qayta yasalganda manzillar o'zgarib, ishlab turgan serverda 404
chiqardi. Endi manzil faqat savol raqami va harfga bog'liq.

Har bir javob qatori 5 ball: 33 qator × 5 = 165 ball — Worddagi
"(5 - ball)" / "(15 - ball)" yozuvlari bilan bir xil.

Javob kaliti Wordda yo'q edi — rasmlarga qarab tuzilgan. O'zgartirish kerak
bo'lsa, faqat shu fayldagi harflarni tahrirlash yetarli.
"""

from pathlib import Path

QATOR_BALL = 5
DAQIQA = 20
RASM_YOL = '/static/img/rasmli-test/'
RASM_VERSIYA = 4   # rasm fayllari almashtirilganda oshiriladi (kesh yangilanishi uchun)
RASM_KATALOG = Path(__file__).resolve().parent.parent / 'static' / 'img' / 'rasmli-test'

# (raqam, savol matni, [(qator yorlig'i, to'g'ri harf), ...])
# Yorliq bo'sh bo'lsa — savolning o'zi yagona javobli.
_XOM = [
    (1, "Kvilling usulida yasalgan tasvirni toping", [
        ('', 'b')]),
    (2, "Applikatsiya usulida yasalgan tasvirni toping", [
        ('', 'a')]),
    (3, "Mozaika usulida yasalgan tasvirni toping", [
        ('', 's')]),
    (4, "Origami usulida yasalgan tasvirni toping", [
        ('', 'b')]),
    (5, "Papye-mashe usulida yasalgan tasvirni toping", [
        ('', 's')]),
    (6, "Kasblarga mos rasmni toping", [
        ('Baliqchi', 's'), ('Quruvchi', 'a'), ('Haydovchi', 'b')]),
    (7, "Kasblarga mos rasmni toping", [
        ('Duradgor', 's'), ('Doktor', 'a'), ('Metallurg', 'b')]),
    (8, "Kasblarga mos rasmni toping", [
        ('Bank xodimi', 'b'), ('Uchuvchi', 's'), ('Haydovchi', 'a')]),
    (9, "Kasblarga mos rasmni toping", [
        ('Modelyer', 's'), ('Veterinar', 'b'), ("Qo'g'irchoqboz", 'a')]),
    (10, "Kasblarga mos rasmni toping", [
        ('Konstruktor', 's'), ('Florist', 'a'), ('Tikuvchi', 'b')]),
    (11, "Kasblarga mos rasmni toping", [
        ('Styuardessa', 'a'), ('Bichiqchi', 'b'), ('Fazogir', 's')]),
    (12, "Bu ish anjomlaridan qaysi kasb egalari foydalanadi?", [
        ('Tikuvchi ish anjomlari', 'a'), ('Rassom ish anjomlari', 's'),
        ('Duradgor ish anjomlari', 'b')]),
    (13, "Qaysi javobda faqat tikuvchilik ish anjomlari tasvirlangan?", [
        ('', 'b')]),
    (14, "Qog'oz turlari to'g'ri ko'rsatilgan javobni belgilang", [
        ("Daftar qog'oz", 's'), ("Rangli qog'oz", 'a'), ("Karton qog'oz", 'b')]),
    (15, "Qog'oz turlari to'g'ri ko'rsatilgan javobni belgilang", [
        ("Chizmachilik qog'oz", 's'), ("Gazeta qog'oz", 'a'), ("Yaltiroq qog'oz", 'b')]),
]

HARFLAR = [('a', 'A'), ('b', 'B'), ('s', 'S')]

_KESH = None


def _rasm(raqam, kalit):
    """Variant rasmining manzili.

    Oxiridagi `?v=` — brauzer keshini yangilash uchun. Rasm fayli
    almashtirilsa (nomi o'sha qolgani holda) shu raqamni oshiring,
    aks holda ba'zi brauzerlar eski nusxani ko'rsatib turaveradi.
    """
    return f'{RASM_YOL}s{raqam:02d}{kalit}.jpg?v={RASM_VERSIYA}'


def yetishmagan_rasmlar():
    """Diskda yo'q rasmlar ro'yxati — `manage.py check` shuni ogohlantiradi."""
    return [
        f's{raqam:02d}{k}.jpg'
        for raqam, _, _ in _XOM
        for k, _ in HARFLAR
        if not (RASM_KATALOG / f's{raqam:02d}{k}.jpg').exists()
    ]


def savollar():
    """Shablon uchun tayyor ro'yxat (bir marta yig'ilib, keshlanadi)."""
    global _KESH
    if _KESH is not None:
        return _KESH
    chiqish = []
    for raqam, matn, qatorlar in _XOM:
        chiqish.append({
            'raqam': raqam,
            'savol': matn,
            'ball': len(qatorlar) * QATOR_BALL,
            'moslash': len(qatorlar) > 1,
            'variantlar': [
                {'kalit': k, 'harf': h, 'rasm': _rasm(raqam, k)}
                for k, h in HARFLAR
            ],
            'qatorlar': [
                {'nomer': i, 'yorliq': yorliq, 'javob': javob}
                for i, (yorliq, javob) in enumerate(qatorlar)
            ],
        })
    _KESH = chiqish
    return chiqish


def javob_kaliti():
    """{savol raqami: [to'g'ri harflar]} — sahifadagi JS shu bilan tekshiradi."""
    return {str(raqam): [j for _, j in qatorlar] for raqam, _, qatorlar in _XOM}


def jami_ball():
    return sum(len(q) for _, _, q in _XOM) * QATOR_BALL


def jami_qator():
    return sum(len(q) for _, _, q in _XOM)
