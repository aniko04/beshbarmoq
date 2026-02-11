// Test savollari — har bir savolda correctAnswer to'g'ri javob matni
const questions = [
    {
        question: "Applikatsiya qanday so'zdan olingan?",
        options: ["Lotincha", "Inglizcha", "Arabcha", "Yunoncha"],
        correctAnswer: "Lotincha"
    },
    {
        question: "Applikatsiya qanday manoni anglatadi?",
        options: ["Qirqib yopishtirish", "Joylashtirish", "Bo'yash", "Chizish"],
        correctAnswer: "Qirqib yopishtirish"
    },
    {
        question: "Applikatsiya mashg'uloti bolalarda qanday ahamiyatga ega?",
        options: [
            "Bolalarni o'stiradi",
            "Ruhan chiniqtiradi",
            "O'yinga qiziqtiradi",
            "Har tomonlama o'sishda katta ahamiyatga ega"
        ],
        correctAnswer: "Har tomonlama o'sishda katta ahamiyatga ega"
    },
    {
        question: "Applikatsiya necha guruhga bo'linadi?",
        options: ["4 ta", "5 ta", "3 ta", "2 ta"],
        correctAnswer: "5 ta"
    },
    {
        question: "Applikatsiya qanday paydo bo'lgan?",
        options: [
            "Applikatsiya 2500 yil muqadam ko'chmanchi xalqlarda paydo bo'lgan va kiyim bosh turar joylar bezatilgan",
            "Applikatsiya 2000 yil muqadam paydo bo'lgan va kiyim bosh bezatilgan",
            "Applikatsiya turar joylar bezatilgan qachon paydo bo'lgani noma'lum",
            "Applikatsiya 2000 yil muqadam paydo bo'lib, narsalar bezatishda ishlatiladi"
        ],
        correctAnswer: "Applikatsiya 2500 yil muqadam ko'chmanchi xalqlarda paydo bo'lgan va kiyim bosh turar joylar bezatilgan"
    }
];

const TOTAL = questions.length;
let selected = {}; // { questionIndex: selectedOptionText }
let checked = false;

function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function updateProgress() {
    const answered = Object.keys(selected).length;
    document.getElementById('progress-text').textContent = answered + ' / ' + TOTAL;
    document.getElementById('progress-fill').style.width = (answered / TOTAL * 100) + '%';
}

function renderQuestions() {
    const container = document.getElementById('test-questions');
    container.innerHTML = '';

    questions.forEach((q, qIndex) => {
        const qDiv = document.createElement('div');
        qDiv.className = 'test-question';
        qDiv.dataset.index = qIndex;

        const title = document.createElement('div');
        title.className = 'question-title';
        title.textContent = (qIndex + 1) + '. ' + q.question;
        qDiv.appendChild(title);

        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'question-options';

        // Variantlarni aralashtirish
        const shuffled = shuffle(q.options);
        const letters = ['A', 'B', 'C', 'D'];

        shuffled.forEach((opt, oIndex) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.dataset.question = qIndex;
            btn.dataset.value = opt;

            const letter = document.createElement('span');
            letter.className = 'option-letter';
            letter.textContent = letters[oIndex];

            const text = document.createElement('span');
            text.className = 'option-text';
            text.textContent = opt;

            btn.appendChild(letter);
            btn.appendChild(text);

            btn.addEventListener('click', function () {
                if (checked) return;
                selectOption(qIndex, opt);
            });

            optionsDiv.appendChild(btn);
        });

        qDiv.appendChild(optionsDiv);
        container.appendChild(qDiv);
    });
}

function selectOption(qIndex, value) {
    selected[qIndex] = value;

    // Buttonlarni yangilash
    const btns = document.querySelectorAll('.option-btn[data-question="' + qIndex + '"]');
    btns.forEach(btn => {
        if (btn.dataset.value === value) {
            btn.classList.add('selected');
        } else {
            btn.classList.remove('selected');
        }
    });

    updateProgress();
}

function checkAnswers() {
    // Hamma savol javoblangami?
    if (Object.keys(selected).length < TOTAL) {
        const qoldi = TOTAL - Object.keys(selected).length;
        document.getElementById('result').textContent =
            'Avval barcha savollarga javob bering! (' + qoldi + ' ta qoldi)';
        document.getElementById('result').className = 'result-msg fail';
        return;
    }

    checked = true;
    let correct = 0;

    questions.forEach((q, qIndex) => {
        const btns = document.querySelectorAll('.option-btn[data-question="' + qIndex + '"]');
        const userAnswer = selected[qIndex];

        btns.forEach(btn => {
            btn.classList.add('disabled');

            if (btn.dataset.value === q.correctAnswer) {
                btn.classList.add('correct');
            }

            if (btn.dataset.value === userAnswer && userAnswer !== q.correctAnswer) {
                btn.classList.add('wrong');
            }
        });

        if (userAnswer === q.correctAnswer) {
            correct++;
        }
    });

    if (correct === TOTAL) {
        document.getElementById('result').textContent =
            "Barakalla! Barcha javoblar to'g'ri! (" + correct + '/' + TOTAL + ')';
        document.getElementById('result').className = 'result-msg success';
    } else {
        document.getElementById('result').textContent =
            correct + ' / ' + TOTAL + " ta to'g'ri.";
        document.getElementById('result').className = 'result-msg fail';
    }

    document.getElementById('check-btn').style.display = 'none';
    document.getElementById('retry-btn').style.display = 'inline-block';
    document.getElementById('next-btn').style.display = 'inline-block';
}

function retry() {
    selected = {};
    checked = false;
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
    document.getElementById('check-btn').style.display = 'inline-block';
    document.getElementById('retry-btn').style.display = 'none';
    document.getElementById('next-btn').style.display = 'none';
    renderQuestions();
    updateProgress();
}

// Boshlash
document.getElementById('retry-btn').style.display = 'none';
document.getElementById('next-btn').style.display = 'none';
renderQuestions();
updateProgress();
