const words = [
    'Seamstress', 'Carpenter', 'Embroiderer', 'Chef cook',
    'Painter', 'Potter', 'Cobbler', 'Carpet weaver',
    'Baker', 'Weaver', 'Auto mechanic'
];

let shuffled = [];
let currentIndex = 0;
let solved = 0;

function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function init() {
    shuffled = shuffle(words);
    currentIndex = 0;
    solved = 0;
    updateProgress();
    showNextWord();
}

function showNextWord() {
    const wordEl = document.getElementById('drag-word');
    const center = document.getElementById('center-circle');

    if (currentIndex >= shuffled.length) {
        // Hammasi tugadi
        wordEl.textContent = '';
        wordEl.classList.remove('visible');
        center.classList.add('completed');
        document.getElementById('result').textContent = "Barakalla! Barcha hunarlar topildi!";
        document.getElementById('result').className = 'result-msg success';
        return;
    }

    wordEl.textContent = shuffled[currentIndex];
    wordEl.dataset.word = shuffled[currentIndex].toLowerCase();
    wordEl.classList.add('visible');
    wordEl.draggable = true;

    // Animatsiya
    wordEl.classList.remove('word-enter');
    void wordEl.offsetWidth;
    wordEl.classList.add('word-enter');
}

function updateProgress() {
    const total = words.length;
    document.getElementById('progress-text').textContent = solved + ' / ' + total;
    document.getElementById('progress-fill').style.width = (solved / total * 100) + '%';
}

// ===== DESKTOP DRAG & DROP =====
document.getElementById('drag-word').addEventListener('dragstart', function (e) {
    e.dataTransfer.setData('text/plain', this.dataset.word);
    e.dataTransfer.effectAllowed = 'move';
    this.classList.add('dragging');
});

document.getElementById('drag-word').addEventListener('dragend', function () {
    this.classList.remove('dragging');
});

document.querySelectorAll('.drop-target').forEach(target => {
    target.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        this.classList.add('drag-hover');
    });

    target.addEventListener('dragleave', function () {
        this.classList.remove('drag-hover');
    });

    target.addEventListener('drop', function (e) {
        e.preventDefault();
        this.classList.remove('drag-hover');
        const word = e.dataTransfer.getData('text/plain');
        handleDrop(this, word);
    });
});

// ===== MOBILE TOUCH =====
let touchEl = null;
let touchClone = null;
let tOffsetX = 0;
let tOffsetY = 0;

document.getElementById('drag-word').addEventListener('touchstart', function (e) {
    if (!this.classList.contains('visible')) return;
    touchEl = this;
    const rect = this.getBoundingClientRect();
    const touch = e.touches[0];
    tOffsetX = touch.clientX - rect.left;
    tOffsetY = touch.clientY - rect.top;

    touchClone = this.cloneNode(true);
    touchClone.style.position = 'fixed';
    touchClone.style.width = rect.width + 'px';
    touchClone.style.zIndex = '9999';
    touchClone.style.pointerEvents = 'none';
    touchClone.style.opacity = '0.9';
    touchClone.style.left = (touch.clientX - tOffsetX) + 'px';
    touchClone.style.top = (touch.clientY - tOffsetY) + 'px';
    document.body.appendChild(touchClone);
    this.classList.add('dragging');
}, { passive: true });

document.addEventListener('touchmove', function (e) {
    if (!touchClone) return;
    e.preventDefault();
    const touch = e.touches[0];
    touchClone.style.left = (touch.clientX - tOffsetX) + 'px';
    touchClone.style.top = (touch.clientY - tOffsetY) + 'px';

    document.querySelectorAll('.drop-target').forEach(t => {
        const r = t.getBoundingClientRect();
        if (touch.clientX >= r.left && touch.clientX <= r.right &&
            touch.clientY >= r.top && touch.clientY <= r.bottom) {
            t.classList.add('drag-hover');
        } else {
            t.classList.remove('drag-hover');
        }
    });
}, { passive: false });

document.addEventListener('touchend', function (e) {
    if (!touchEl || !touchClone) return;
    const touch = e.changedTouches[0];
    touchClone.remove();
    touchEl.classList.remove('dragging');

    const word = touchEl.dataset.word;

    document.querySelectorAll('.drop-target').forEach(target => {
        target.classList.remove('drag-hover');
        const r = target.getBoundingClientRect();
        if (touch.clientX >= r.left && touch.clientX <= r.right &&
            touch.clientY >= r.top && touch.clientY <= r.bottom) {
            handleDrop(target, word);
        }
    });

    touchEl = null;
    touchClone = null;
}, { passive: true });

// ===== DROP LOGIC =====
function handleDrop(target, word) {
    const answer = target.dataset.answer;

    if (target.classList.contains('matched')) return;

    if (word === answer) {
        // To'g'ri!
        target.classList.add('matched');

        // Rasm ustiga label qo'yish
        const label = document.createElement('div');
        label.className = 'matched-label';
        label.textContent = shuffled[currentIndex];
        target.appendChild(label);

        solved++;
        currentIndex++;
        updateProgress();

        setTimeout(() => showNextWord(), 400);
    } else {
        // Noto'g'ri — silkinish
        target.classList.add('wrong-shake');
        setTimeout(() => target.classList.remove('wrong-shake'), 500);
    }
}

// Boshlash
init();
