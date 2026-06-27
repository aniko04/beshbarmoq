# O'quvchi mashqlari — qo'llanma

Bu hujjat o'quvchi (rol: `oquvchi`) uchun mashqlarni qanday qo'shish/tugatishni tushuntiradi.

## Loyiha tuzilishi (qisqacha)

- **Rollar:** `oquvchi` va `talaba` (`home/models.py` → `Profile`). Talaba/staff `/mNa…` (o'qituvchi sahifalari) ni, o'quvchi `/oNa…` ni ko'radi. Bosh sahifa kartasi rolga qarab havola beradi (`templates/index.html`).
- **1–5 mashqlar** — interaktiv o'yinlar (hamma uchun bir xil).
- **6–10 mashqlar** — har biri 3 bosqich: **video → test → krossvord**.
  - O'quvchi sahifalari: `templates/oquvchi/mNa.html` (video), `mNb.html` (test), `mNc.html` (krossvord).
  - URL: `/oNa`, `/oNb`, `/oNc` (masalan `/o8a`). View: `home/views.py` dagi `oquvchi_mNx`. Marshrut: `core/urls.py`.
  - Test va krossvord **shu HTML faylning ichida** (inline `<script>`), tashqi JS ishlatilmaydi.
- **Mavzu ranglari** (`<body class="t-...">`): 6=`t-blue`, 7=`t-rose`, 8=`t-indigo`, 9=`t-coral`, 10=`t-emerald`.

## ⚠️ Chala qolgan ish: 9-mashq (Kvilling)

9-mashq (Kvilling) o'quvchi uchun **hozircha faqat video**:
- `/o9a` (Video4) → `/o9a2` (Video5) → **bosh sahifaga** qaytadi.
- **Test (`/o9b`) va krossvord (`/o9c`) hali YO'Q** — chunki `namuna` papkasida Kvilling materiallari berilmagan edi.

Materiallar tayyor bo'lgach quyidagi 6 qadam bilan tugatiladi.

---

## Kvilling (9) test+krossvordini qo'shish — bosqichma-bosqich

### 0. Materiallarni `namuna` papkasiga qo'ying
Ikki fayl kerak (6/7/8/10 da bo'lgani kabi):
- **`...docx`** — 8–10 ta test savoli + krossvord savollari (har biriga "Javob: SO'Z").
- **`index...html`** — krossvord to'ri (jadval). Har katakda harf; `<span class="gor">N</span>` = **eniga** so'z raqami, `<span class="ver">N</span>` = **bo'yiga** so'z raqami.

### 1. Video oqimini ulang
`templates/oquvchi/m9a2.html` ichida redirectni bosh sahifadan testga o'zgartiring:
```js
window.location.href = '/';      // ESKI
window.location.href = '/o9b';   // YANGI
```

### 2. Testni yarating: `templates/oquvchi/m9b.html`
Eng oson yo'l — tayyor namunani nusxalash:
1. `templates/oquvchi/m8b.html` mazmunini `m9b.html` ga ko'chiring.
2. O'zgartiring:
   - `<body class="t-indigo">` → `<body class="t-coral">`
   - `<title>Mashq 8 - Test</title>` → `Mashq 9 - Test`
   - `0 / 8` (progress matni) → savol soniga moslang (masalan `0 / 8`).
   - `<a href="/o8c" ...>` (next-btn) → `/o9c`.
   - `const questions = [ ... ]` ni Word'dagi savollar bilan to'liq almashtiring.
   - `mashq: 'm8b'` (save-result) → `'m9b'`.
3. Savol formati:
   ```js
   { question: "Savol matni?", options: ["A","B","C","D"], correctAnswer: "to'g'ri variant" }
   ```
   `correctAnswer` `options` ichidagi matnga **aynan** teng bo'lsin.

### 3. Krossvordni yarating: `templates/oquvchi/m9c.html`
1. `templates/oquvchi/m8c.html` ni `m9c.html` ga nusxalang.
2. Sarlavha/rang/havolalar: `t-indigo`→`t-coral`, `Mashq 8`→`Mashq 9`, orqaga havola `/o8b`→`/o9b`.
3. To'r o'lchami (yuqorida JS + CSS): `var ROWS=.., COLS=..` va `grid-template-columns:repeat(COLS,38px)`, `grid-template-rows:repeat(ROWS,38px)` (ikki media-query'da ham).
4. Ma'lumotni `namuna/index...html` jadvalidan ko'chiring:
   - **`answers`** — har katak: `'qator-ustun':'HARF'`. `CH`, `SH`, `G'`, `O'` — bitta katak (digraf, avtomatik kichik shrift).
   - **`hRanges`** (eniga so'zlar) — `[qator, boshUstun, oxirUstun]`.
   - **`vRanges`** (bo'yiga so'zlar) — `[ustun, boshQator, oxirQator]`.
   - **`nums`** — raqam badge'lari: `'qator-ustun':[{n:'1',c:'#rang'}]`. Bitta katakda 2 raqam bo'lsa: `[{n:'2',c:'#..'},{n:'7',c:'#..',second:true}]`.
   - **`clues-h`** (Eniga) va **`clues-v`** (Bo'yiga) — savol matnlari (Word'dan).

### 4. View qo'shing: `home/views.py`
9-mashq bo'limiga:
```python
def oquvchi_m9b(request):
    return render(request, 'oquvchi/m9b.html')

def oquvchi_m9c(request):
    return render(request, 'oquvchi/m9c.html')
```

### 5. Marshrut qo'shing: `core/urls.py`
`o9a2` qatoridan keyin:
```python
path('o9b', views.oquvchi_m9b, name='oquvchi_m9b'),
path('o9c', views.oquvchi_m9c, name='oquvchi_m9c'),
```

### 6. Tekshiring
```bash
env/Scripts/python.exe manage.py check
```
So'ng `/o9a → /o9a2 → /o9b → /o9c` oqimini brauzerda sinab ko'ring.
> `index.html` ga tegmaysiz — 9-karta allaqachon `/o9a` ga ulangan.

---

## Foydali eslatmalar

- **To'r xatolari:** `namuna` jadvallarida ba'zan harf xato yoziladi (masalan `Z`↔`R`). Har doim **Word'dagi javobni** asosiy deb oling va kesishmalar (bir katakni baham ko'rgan ikki so'z) bir xil harf berishini tekshiring.
- **Izchillikni tekshirish:** `answers` dagi har katak kamida bitta `hRanges`/`vRanges` so'ziga tegishli bo'lishi, va har so'z katagi `answers` da bo'lishi shart (ortiqcha/yetishmaydigan katak bo'lmasin).
- **Natija saqlash:** test `'/api/save-result'` ga `mashq:'mNb'` kaliti bilan yuboradi (faqat tizimga kirgan foydalanuvchida saqlanadi). Yangi kalit kerak bo'lsa `home/models.py` → `Result.MASHQ_CHOICES` ga qo'shing.
- **`namuna/` papkasi** — faqat ishchi/manba fayllar; git'ga commit qilinmaydi.
