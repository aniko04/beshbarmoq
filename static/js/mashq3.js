const riddles = {
    1: {
        text: "Matoni o'lchaydi ip bilan, igna,\nYaratar libosni go'zal did bilan.\nHar chokida mehnat, har ipda san'at,\nKiyim tikish — unga eng buyuk baxt.",
        answers: ["tikuvchi"]
    },
    2: {
        text: "Oq xalat kiygan, dardni biladi,\nBemorga davo topib, dilni tinch qiladi.\nYurak, qon bosim, nafasni tinglar,\nHayotni asrash — kasbining timsoli shular.",
        answers: ["shifokor", "vrach", "doktor"]
    },
    3: {
        text: "Bahorda ekadi, kuzda teradi,\nHar bir ko'chatni mehr bilan seradi.\nGul ochsa bog'ida, yuzida kulgu,\nMehnat hosili — bu hayot tuhfasi, to'g'ri so'zu!",
        answers: ["bog'bon"]
    },
    4: {
        text: "Qo'lida qaychi, mashinka jarang,\nSochlar par-par uchadi har dam.\nChiroyli qiyofa — uning san'ati,\nGo'zallikka eltadi har bir harakati.",
        answers: ["sartarosh"]
    },
    5: {
        text: "Qizil mashinada yugurar tez,\nYong'in o'chirar, cho'chimas hech kez.\nSuv purkar, olovdan asraydi jon,\nQahramon u — xalq uchun mehribon.",
        answers: ["o't o'chiruvchi", "ot ochiruvchi", "o't ochiruvchi"]
    },
    6: {
        text: "Yo'llarda turadi, tartibni qo'yar,\nXavfsizlik — yurakda, jasorat so'yar.\nAdolat posboni, xalq uchun sodiq,\nQonun — qalqoni, yuragi pok.",
        answers: ["militsioner", "politsiyachi", "politsiya"]
    },
    7: {
        text: "Qo'lida molga, qum bilan g'isht,\nTika oladi devor, uy-u ko'prik.\nShaharlar chiroyli, uylar mustahkam,\nMehnati bilan bo'lur xalq tinch va xurram.",
        answers: ["quruvchi", "qurilishchi"]
    },
    8: {
        text: "Do'kon ichra tartib, tozalik bor,\nXaridorni kutar xursand yuzlar.\nO'lchab, sanab, hurmat bilan so'zlar,\nSavdo qilmoq — uning faxrli so'zi, har bor.",
        answers: ["sotuvchi", "savdogar"]
    },
    9: {
        text: "Tongda uyg'onib yoqar tandir,\nXamir qoradi, qo'llari chaqqon bir.\nIssiq non hidi — mehrning belgisi,\nHar bir non — halol mehnat mevasi.",
        answers: ["nonvoy", "novvoy"]
    },
    10: {
        text: "Qo'lida daftar, bilim — yuragida,\nBolalar uchun quyosh har tongida.\nSabru bardosh bilan yo'l ko'rsatadi,\nKelajak bunyodkorini tarbiyalaydi.",
        answers: ["o'qituvchi", "oqituvchi", "muallim"]
    },
    11: {
        text: "Bulutlar orasida yo'l topadi,\nOsmon kengligida parvoz qiladi.\nYerga boqib, osmonda yuradi,\nXavfsiz manzil — niyati, orzusi shudi.",
        answers: ["uchuvchi", "pilot"]
    },
    12: {
        text: "Qirqadi, o'lchaydi, naqshlar soladi,\nMatodan mo''jiza yaratib oladi.\nTo'y libosi, ko'rpa, choyshab — hammasi udan,\nHar chokida mehnat, har ipda san'at.",
        answers: ["tikuvchi"]
    }
};

// Har bir kartochkani bosganda modal ochiladi
document.querySelectorAll('.job-card').forEach(card => {
    card.addEventListener('click', function () {
        const num = this.dataset.num;
        openRiddle(num);
    });
});

function openRiddle(num) {
    const riddle = riddles[num];
    if (!riddle) return;

    // Kartochkalarni tanlash
    document.querySelectorAll('.job-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`.job-card[data-num="${num}"]`).classList.add('selected');

    const modal = document.getElementById('riddle-modal');
    document.getElementById('riddle-num').textContent = num;
    document.getElementById('riddle-text').textContent = riddle.text;
    document.getElementById('riddle-input').value = '';
    document.getElementById('riddle-result').textContent = '';
    document.getElementById('riddle-result').className = 'riddle-result';
    modal.dataset.current = num;
    modal.classList.add('active');
    document.getElementById('riddle-input').focus();
}

function closeRiddle() {
    const modal = document.getElementById('riddle-modal');
    modal.classList.remove('active');
    document.querySelectorAll('.job-card').forEach(c => c.classList.remove('selected'));
}

function checkRiddle() {
    const modal = document.getElementById('riddle-modal');
    const num = modal.dataset.current;
    const riddle = riddles[num];
    const input = document.getElementById('riddle-input').value.trim().toLowerCase();
    const resultEl = document.getElementById('riddle-result');

    if (!input) {
        resultEl.textContent = "Javobni kiriting!";
        resultEl.className = 'riddle-result wrong';
        return;
    }

    const isCorrect = riddle.answers.some(a => a === input);

    if (isCorrect) {
        resultEl.textContent = "Barakalla! Javob to'g'ri!";
        resultEl.className = 'riddle-result correct';
        // Kartochkani solved qilish
        document.querySelector(`.job-card[data-num="${num}"]`).classList.add('solved');
    } else {
        resultEl.textContent = "Noto'g'ri! Qaytadan urinib ko'ring.";
        resultEl.className = 'riddle-result wrong';
    }
}

// Enter tugmasini bosganda tekshirish
document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && document.getElementById('riddle-modal').classList.contains('active')) {
        checkRiddle();
    }
    if (e.key === 'Escape') {
        closeRiddle();
    }
});

// Modal tashqarisini bosganda yopish
document.getElementById('riddle-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        closeRiddle();
    }
});
