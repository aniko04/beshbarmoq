/* ===== MASHQ 3 — TOPISHMOQ ARENA ===== */

// ===== DATA =====
const professions = [
    { id: 1,  name: "Bichuvchi",        img: "/media/jobs/Picture1.png" },
    { id: 2,  name: "Shifokor",         img: "/media/jobs/Picture2.png" },
    { id: 3,  name: "Bog'bon",          img: "/media/jobs/Picture3.png" },
    { id: 4,  name: "Sartarosh",        img: "/media/jobs/Picture4.png" },
    { id: 5,  name: "O't o'chiruvchi",  img: "/media/jobs/Picture5.png" },
    { id: 6,  name: "Militsioner",      img: "/media/jobs/Picture6.png" },
    { id: 7,  name: "Quruvchi",         img: "/media/jobs/Picture7.png" },
    { id: 8,  name: "Sotuvchi",         img: "/media/jobs/Picture8.png" },
    { id: 9,  name: "Nonvoy",           img: "/media/jobs/Picture9.png" },
    { id: 10, name: "O'qituvchi",       img: "/media/jobs/Picture10.png" },
    { id: 11, name: "Uchuvchi",         img: "/media/jobs/Picture11.png" },
    { id: 12, name: "Tikuvchi",         img: "/media/jobs/Picture12.png" }
];

const riddles = [
    {
        id: 1,
        text: "Mato yoyib chiziq chizar,\nAndoza bilan yo'l belgilar,\nQaychi bilan bo'lak-bo'lak qilar,\nTikuvchiga ish tayyorlar.",
        answer: 1, profession: "Bichuvchi",
        hint: "'B' harfi bilan boshlanadi"
    },
    {
        id: 2,
        text: "Igna-ipni qo'lga olar,\nKesilgan matoni ulab borar,\nChokma-chok kiyim chiqarar,\nEgasi kiyib quvonar.",
        answer: 12, profession: "Tikuvchi",
        hint: "'T' harfi bilan boshlanadi"
    },
    {
        id: 3,
        text: "Oq kiyimda dardni tinglar,\nTomir tutib sabab izlar,\nDori yozib shifo tilar,\nBemor sog'ayib kulib chiqar.",
        answer: 2, profession: "Shifokor",
        hint: "'Sh' harfi bilan boshlanadi"
    },
    {
        id: 4,
        text: "Bahor kelsa urug' sevar,\nSuv sepib nihol o'stirar,\nYozda gullar, kuzda meva berar,\nHosilini yig'ib olar.",
        answer: 3, profession: "Bog'bon",
        hint: "'B' harfi bilan boshlanadi"
    },
    {
        id: 5,
        text: "Mijoz kelar o'rindiqqa,\nSochini yuvib taroqqa,\nQaychi bilan shakl berar,\nOynada chiroy ko'rinar.",
        answer: 4, profession: "Sartarosh",
        hint: "'S' harfi bilan boshlanadi"
    },
    {
        id: 6,
        text: "Qizil mashina shoshilar,\nTutun ichra yo'l topar,\nSuv sepib olovni yengar,\nOdamlarni asrab qolar.",
        answer: 5, profession: "O't o'chiruvchi",
        hint: "'O' harfi bilan boshlanadi"
    },
    {
        id: 7,
        text: "Yo'lda turib qo'l ko'tarar,\nMashinalarga yo'l solar,\nQoidani buzganni to'xtatar,\nTinchlik uchun xizmat qilar.",
        answer: 6, profession: "Militsioner",
        hint: "'M' harfi bilan boshlanadi"
    },
    {
        id: 8,
        text: "Poydevordan ish boshlanar,\nG'isht ustiga g'isht qo'yilar,\nTom yopilib uy bitar,\nYangi maskan qad ko'tarar.",
        answer: 7, profession: "Quruvchi",
        hint: "'Q' harfi bilan boshlanadi"
    },
    {
        id: 9,
        text: "Rastani toza tutar,\nXaridorni kulib kutar,\nMahsulotni o'lchab sotar,\nPulini olib rahmat aytar.",
        answer: 8, profession: "Sotuvchi",
        hint: "'S' harfi bilan boshlanadi"
    },
    {
        id: 10,
        text: "Tong saharda tandir yoqar,\nXamir qorib non yopar,\nIssiq hidi ko'chaga tarar,\nDasturxonga baraka solar.",
        answer: 9, profession: "Nonvoy",
        hint: "'N' harfi bilan boshlanadi"
    },
    {
        id: 11,
        text: "Qo'lida kitob-daftar,\nBolalarga saboq aytar,\nSavol berib fikr uyg'otar,\nBilim bilan yo'l ko'rsatar.",
        answer: 10, profession: "O'qituvchi",
        hint: "'O' harfi bilan boshlanadi"
    },
    {
        id: 12,
        text: "Temir qushni osmonga olar,\nBulutlar orasida yo'l topar,\nUzoq manzilga eltib borar,\nYo'lovchini sog' yetkazar.",
        answer: 11, profession: "Uchuvchi",
        hint: "'U' harfi bilan boshlanadi"
    }
];

// ===== STATE =====
const State = {
    IDLE: 'IDLE',
    ROUND_INTRO: 'ROUND_INTRO',
    SPOTLIGHT_READY: 'SPOTLIGHT_READY',
    SPOTLIGHT_ACTIVE: 'SPOTLIGHT_ACTIVE',
    SELECTING: 'SELECTING',
    CONFIRMING: 'CONFIRMING',
    RESULT: 'RESULT',
    GAME_OVER: 'GAME_OVER',
    SUMMARY: 'SUMMARY'
};

const SPOTLIGHT_DURATION = 4500;
const SPOTLIGHT_RADIUS_FACTOR = 0.28;
const TYPEWRITER_SPEED = 25;
const RESULT_DELAY = 1600;
const CONFETTI_COUNT = 20;

let game = {
    state: State.IDLE,
    round: 0,
    score: 0,
    lives: 3,
    streak: 0,
    maxStreak: 0,
    correct: 0,
    wrong: 0,
    hintUsed: false,
    roundOrder: [],
    cardOrder: [],
    selectedCard: null,
    spotlightAnimId: null,
    spotlightStart: 0,
    typewriterTimer: null
};

// ===== DOM REFS =====
const $ = (id) => document.getElementById(id);

// ===== SCREEN MANAGEMENT =====
function showScreen(id) {
    document.querySelectorAll('.m3-screen').forEach(s => s.classList.remove('m3-active'));
    const screen = $(id);
    screen.classList.add('m3-active');
    screen.style.animation = 'none';
    screen.offsetHeight; // force reflow
    screen.style.animation = 'm3-screenIn 0.4s ease';
}

// ===== UTILITIES =====
function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

// ===== GAME INIT =====
function startGame() {
    game.state = State.IDLE;
    game.round = 0;
    game.score = 0;
    game.lives = 3;
    game.streak = 0;
    game.maxStreak = 0;
    game.correct = 0;
    game.wrong = 0;
    game.selectedCard = null;

    // Shuffle riddle order and card positions
    game.roundOrder = shuffle([...Array(12).keys()]);
    game.cardOrder = shuffle([...professions]);

    // Reset HUD
    resetHearts();
    updateHUD();

    // Build arena
    renderArena();

    showScreen('game-screen');

    // Start first round after short delay
    setTimeout(() => startRound(), 400);
}

function renderArena() {
    const grid = $('arena-grid');
    grid.innerHTML = '';

    game.cardOrder.forEach((prof, idx) => {
        const card = document.createElement('div');
        card.className = 'arena-card';
        card.dataset.id = prof.id;
        card.style.setProperty('--fog-opacity', '1');
        card.style.animationDelay = idx * 0.05 + 's';

        const img = document.createElement('img');
        img.src = prof.img;
        img.alt = 'Kasb';
        img.draggable = false;
        card.appendChild(img);

        card.addEventListener('click', () => onCardClick(prof.id));
        grid.appendChild(card);
    });
}

// ===== ROUND MANAGEMENT =====
function startRound() {
    const riddleIdx = game.roundOrder[game.round];
    const riddle = riddles[riddleIdx];

    game.state = State.ROUND_INTRO;
    game.hintUsed = false;
    game.selectedCard = null;

    // Reset card states
    document.querySelectorAll('.arena-card').forEach(card => {
        card.classList.remove('selected', 'correct-reveal', 'wrong-reveal', 'not-clickable');
        card.style.setProperty('--fog-opacity', '1');
    });

    // Hide confirm button
    $('confirm-btn').classList.add('m3-hidden');

    // Reset hint
    $('hint-area').classList.add('m3-hidden');
    $('hint-btn').disabled = false;

    // Hide discover button
    $('discover-btn').classList.add('m3-hidden');

    // Update badge
    $('riddle-badge').textContent = '#' + (game.round + 1);

    // Update HUD
    updateHUD();

    // Clear riddle text and start typewriter
    $('riddle-text').textContent = '';
    typeWriter($('riddle-text'), riddle.text, TYPEWRITER_SPEED, () => {
        // Typewriter done — show discover button
        game.state = State.SPOTLIGHT_READY;
        $('discover-btn').classList.remove('m3-hidden');
    });
}

// ===== TYPEWRITER EFFECT =====
function typeWriter(el, text, speed, callback) {
    clearInterval(game.typewriterTimer);
    el.innerHTML = '';
    let i = 0;
    const cursor = document.createElement('span');
    cursor.className = 'm3-cursor';
    el.appendChild(cursor);

    game.typewriterTimer = setInterval(() => {
        if (i < text.length) {
            const char = text[i] === '\n' ? document.createElement('br') : document.createTextNode(text[i]);
            el.insertBefore(char, cursor);
            i++;
        } else {
            clearInterval(game.typewriterTimer);
            // Remove cursor after a brief pause
            setTimeout(() => cursor.remove(), 500);
            if (callback) callback();
        }
    }, speed);
}

// ===== SPOTLIGHT =====
function startSpotlight() {
    if (game.state !== State.SPOTLIGHT_READY) return;

    game.state = State.SPOTLIGHT_ACTIVE;
    $('discover-btn').classList.add('m3-hidden');

    const grid = $('arena-grid');
    grid.classList.add('spotlighting');

    const glow = $('spotlight-glow');
    glow.classList.remove('m3-hidden');

    game.spotlightStart = 0;
    game.spotlightAnimId = requestAnimationFrame(spotlightLoop);
}

function getCardCenters() {
    const arena = $('arena');
    const arenaRect = arena.getBoundingClientRect();
    const cards = document.querySelectorAll('.arena-card');
    return Array.from(cards).map(card => {
        const rect = card.getBoundingClientRect();
        return {
            x: rect.left + rect.width / 2 - arenaRect.left,
            y: rect.top + rect.height / 2 - arenaRect.top,
            el: card
        };
    });
}

function getSpotlightWaypoints(centers) {
    // 4x3 grid — cards are in DOM order: row 0 (0-3), row 1 (4-7), row 2 (8-11)
    // Zigzag: row 0 L→R, row 1 R→L, row 2 L→R
    if (centers.length < 12) return centers;

    // Determine grid layout (could be 4x3 or 3x4 on mobile)
    const cols = getGridCols();
    const rows = Math.ceil(centers.length / cols);
    const waypoints = [];

    for (let r = 0; r < rows; r++) {
        const rowCards = [];
        for (let c = 0; c < cols && r * cols + c < centers.length; c++) {
            rowCards.push(centers[r * cols + c]);
        }
        // Even rows L→R, odd rows R→L
        if (r % 2 === 1) rowCards.reverse();
        waypoints.push(...rowCards);
    }

    return waypoints;
}

function getGridCols() {
    const w = window.innerWidth;
    if (w <= 600) return 3;
    return 4;
}

function spotlightLoop(timestamp) {
    if (!game.spotlightStart) game.spotlightStart = timestamp;

    const elapsed = timestamp - game.spotlightStart;
    const progress = Math.min(elapsed / SPOTLIGHT_DURATION, 1);

    const centers = getCardCenters();
    const waypoints = getSpotlightWaypoints(centers);

    if (waypoints.length < 2) {
        onSpotlightComplete();
        return;
    }

    const totalSegments = waypoints.length - 1;
    const segmentFloat = progress * totalSegments;
    const segmentIndex = Math.min(Math.floor(segmentFloat), totalSegments - 1);
    const segmentT = segmentFloat - segmentIndex;

    // Smooth easing for segment transition
    const easedT = segmentT;

    const a = waypoints[segmentIndex];
    const b = waypoints[Math.min(segmentIndex + 1, waypoints.length - 1)];

    const spotX = a.x + (b.x - a.x) * easedT;
    const spotY = a.y + (b.y - a.y) * easedT;

    // Position glow
    const glow = $('spotlight-glow');
    glow.style.left = spotX + 'px';
    glow.style.top = spotY + 'px';

    // Update fog on all cards
    const arena = $('arena');
    const arenaRect = arena.getBoundingClientRect();
    const radius = Math.min(arenaRect.width, arenaRect.height) * SPOTLIGHT_RADIUS_FACTOR;

    centers.forEach(c => {
        const dist = Math.hypot(c.x - spotX, c.y - spotY);
        const fog = dist < radius ? 0 : dist < radius * 1.5 ? (dist - radius) / (radius * 0.5) : 1;
        c.el.style.setProperty('--fog-opacity', Math.min(1, Math.max(0, fog)));
    });

    if (progress < 1) {
        game.spotlightAnimId = requestAnimationFrame(spotlightLoop);
    } else {
        onSpotlightComplete();
    }
}

function onSpotlightComplete() {
    game.state = State.SELECTING;

    const grid = $('arena-grid');
    grid.classList.remove('spotlighting');

    // Remove fog completely — images fully visible
    document.querySelectorAll('.arena-card').forEach(card => {
        card.style.setProperty('--fog-opacity', '0');
    });

    // Hide glow
    $('spotlight-glow').classList.add('m3-hidden');
}

// ===== CARD INTERACTION =====
function onCardClick(profId) {
    if (game.state === State.SELECTING) {
        // Select the card
        game.selectedCard = profId;
        game.state = State.CONFIRMING;

        document.querySelectorAll('.arena-card').forEach(c => c.classList.remove('selected'));
        const card = document.querySelector(`.arena-card[data-id="${profId}"]`);
        if (card) card.classList.add('selected');

        $('confirm-btn').classList.remove('m3-hidden');

    } else if (game.state === State.CONFIRMING) {
        // Change selection
        document.querySelectorAll('.arena-card').forEach(c => c.classList.remove('selected'));

        if (game.selectedCard === profId) {
            // Deselect
            game.selectedCard = null;
            game.state = State.SELECTING;
            $('confirm-btn').classList.add('m3-hidden');
        } else {
            game.selectedCard = profId;
            const card = document.querySelector(`.arena-card[data-id="${profId}"]`);
            if (card) card.classList.add('selected');
        }
    }
}

function confirmSelection() {
    if (game.state !== State.CONFIRMING || game.selectedCard === null) return;

    game.state = State.RESULT;
    $('confirm-btn').classList.add('m3-hidden');

    const riddleIdx = game.roundOrder[game.round];
    const riddle = riddles[riddleIdx];
    const isCorrect = game.selectedCard === riddle.answer;

    // Make all cards non-clickable during result
    document.querySelectorAll('.arena-card').forEach(c => c.classList.add('not-clickable'));

    if (isCorrect) {
        handleCorrect(riddle);
    } else {
        handleWrong(riddle);
    }
}

function handleCorrect(riddle) {
    game.correct++;
    game.streak++;
    game.maxStreak = Math.max(game.maxStreak, game.streak);

    const multiplier = Math.min(game.streak, 5);
    const points = 100 * multiplier;
    game.score += points;

    // Visual feedback
    const card = document.querySelector(`.arena-card[data-id="${riddle.answer}"]`);
    if (card) {
        card.classList.remove('selected');
        card.classList.add('correct-reveal');
        confetti(card);
    }

    scorePop(points);
    updateHUD();

    // Next round after delay
    setTimeout(() => advanceRound(), RESULT_DELAY);
}

function handleWrong(riddle) {
    game.wrong++;
    game.streak = 0;
    game.lives--;

    // Shake the wrong card
    const wrongCard = document.querySelector(`.arena-card[data-id="${game.selectedCard}"]`);
    if (wrongCard) {
        wrongCard.classList.remove('selected');
        wrongCard.classList.add('wrong-reveal');
    }

    // Reveal correct card
    const correctCard = document.querySelector(`.arena-card[data-id="${riddle.answer}"]`);
    if (correctCard) {
        correctCard.classList.add('correct-reveal');
    }

    // Lose heart
    loseHeart();
    updateHUD();

    // Next round after delay
    setTimeout(() => advanceRound(), RESULT_DELAY);
}

function advanceRound() {
    game.round++;

    if (game.lives <= 0 || game.round >= 12) {
        showSummary();
    } else {
        startRound();
    }
}

// ===== HINT =====
function useHint() {
    if (game.hintUsed) return;
    if (game.state !== State.SPOTLIGHT_READY && game.state !== State.SELECTING && game.state !== State.CONFIRMING) return;

    game.hintUsed = true;
    game.score = Math.max(0, game.score - 30);

    const riddleIdx = game.roundOrder[game.round];
    const riddle = riddles[riddleIdx];

    $('hint-area').textContent = 'Ishora: ' + riddle.hint;
    $('hint-area').classList.remove('m3-hidden');
    $('hint-btn').disabled = true;

    updateHUD();
}

// ===== HUD =====
function updateHUD() {
    $('round-text').textContent = 'Raund ' + (game.round + 1) + ' / 12';
    $('progress-fill').style.width = ((game.round + 1) / 12 * 100) + '%';
    $('score-display').textContent = game.score;

    // Streak badge
    const streakBadge = $('streak-badge');
    if (game.streak >= 2) {
        streakBadge.textContent = '\uD83D\uDD25 x' + game.streak;
        streakBadge.classList.remove('m3-hidden');
    } else {
        streakBadge.classList.add('m3-hidden');
    }
}

function resetHearts() {
    document.querySelectorAll('.m3-heart').forEach(h => {
        h.classList.add('active');
        h.classList.remove('lost');
    });
}

function loseHeart() {
    const hearts = document.querySelectorAll('.m3-heart.active');
    if (hearts.length > 0) {
        const last = hearts[hearts.length - 1];
        last.classList.remove('active');
        last.classList.add('lost');
    }
}

// ===== EFFECTS =====
function confetti(sourceEl) {
    const rect = sourceEl.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const colors = ['#ff1744', '#00c853', '#2979ff', '#ffd600', '#ea4c89', '#8338ec', '#00bcd4'];

    for (let i = 0; i < CONFETTI_COUNT; i++) {
        const particle = document.createElement('div');
        particle.className = 'm3-confetti';
        particle.style.left = cx + 'px';
        particle.style.top = cy + 'px';
        particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        particle.style.width = (4 + Math.random() * 6) + 'px';
        particle.style.height = (4 + Math.random() * 6) + 'px';
        particle.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        particle.style.setProperty('--dx', (Math.random() - 0.5) * 240 + 'px');
        particle.style.setProperty('--dy', (Math.random() - 0.7) * 200 + 'px');
        particle.style.setProperty('--rot', Math.floor(Math.random() * 1080) + 'deg');
        document.body.appendChild(particle);
        particle.addEventListener('animationend', () => particle.remove());
    }
}

function scorePop(amount) {
    const scoreEl = $('score-display');
    const rect = scoreEl.getBoundingClientRect();
    const pop = document.createElement('span');
    pop.className = 'm3-score-pop';
    pop.textContent = '+' + amount;
    pop.style.left = (rect.left + rect.width / 2) + 'px';
    pop.style.top = rect.top + 'px';
    document.body.appendChild(pop);
    pop.addEventListener('animationend', () => pop.remove());
}

// ===== SUMMARY =====
function showSummary() {
    game.state = State.SUMMARY;

    // Stats
    $('stat-correct').textContent = game.correct;
    $('stat-wrong').textContent = game.wrong;

    showScreen('summary-screen');

    // Natijani serverga yuborish
    var total3 = game.correct + game.wrong;
    fetch('/api/save-result', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({mashq: 'm3', score: game.correct, total: total3, is_passed: game.correct > game.wrong})
    }).catch(() => {});
}

// ===== EVENT LISTENERS =====
$('start-btn').addEventListener('click', startGame);
$('discover-btn').addEventListener('click', startSpotlight);
$('confirm-btn').addEventListener('click', confirmSelection);
$('hint-btn').addEventListener('click', useHint);
$('replay-btn').addEventListener('click', startGame);

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}