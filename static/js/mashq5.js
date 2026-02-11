// Ish qurollari — har bir qurol qaysi kasbga tegishli
const tools = [
    { id: 4,  img: 'Picture4.png',  profession: 'tikuvchi'  }, // Qaychi
    { id: 5,  img: 'Picture5.png',  profession: 'oshpaz'    }, // Qozon
    { id: 6,  img: 'Picture6.png',  profession: 'tikuvchi'  }, // O'lchov lentasi
    { id: 7,  img: 'Picture7.png',  profession: 'tikuvchi'  }, // Ip va igna
    { id: 8,  img: 'Picture8.png',  profession: 'oshpaz'    }, // Aralash idish
    { id: 9,  img: 'Picture9.png',  profession: 'tikuvchi'  }, // Angishvona
    { id: 10, img: 'Picture10.png', profession: 'oshpaz'    }, // Taxtacha
    { id: 11, img: 'Picture11.png', profession: 'duradgor'  }, // Kleshe
    { id: 12, img: 'Picture12.png', profession: 'duradgor'  }, // Drel
    { id: 13, img: 'Picture13.png', profession: 'oshpaz'    }, // Uqalagich
    { id: 14, img: 'Picture14.png', profession: 'duradgor'  }, // Arra
    { id: 15, img: 'Picture15.png', profession: 'tikuvchi'  }, // Dazmol
    { id: 16, img: 'Picture16.png', profession: 'tikuvchi'  }, // Ignayostiqcha
    { id: 17, img: 'Picture17.png', profession: 'oshpaz'    }, // Skovoroda
    { id: 18, img: 'Picture18.png', profession: 'duradgor'  }, // Ploskogubsi
    { id: 19, img: 'Picture19.png', profession: 'duradgor'  }, // Bolg'a
];

const TOTAL = tools.length;

function shuffle(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function updateProgress() {
    const placed = TOTAL - document.querySelectorAll('#tools-pool .tool-item').length;
    document.getElementById('progress-text').textContent = placed + ' / ' + TOTAL;
    document.getElementById('progress-fill').style.width = (placed / TOTAL * 100) + '%';
}

// Tool element yaratish (pool va slot larda ishlatiladi)
function createToolEl(tool) {
    const div = document.createElement('div');
    div.className = 'tool-item';
    div.draggable = true;
    div.dataset.id = tool.id;
    div.dataset.profession = tool.profession;
    div.dataset.img = tool.img;

    const img = document.createElement('img');
    img.src = 'media/ishqurollari/ishqurollari/' + tool.img;
    img.alt = 'Tool ' + tool.id;
    div.appendChild(img);

    div.addEventListener('dragstart', onDragStart);
    div.addEventListener('dragend', onDragEnd);
    div.addEventListener('touchstart', onTouchStart, { passive: true });

    return div;
}

function init() {
    // Natijalarni tozalash
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
    document.getElementById('retry-btn').style.display = 'none';
    document.getElementById('check-btn').style.display = '';

    // Slotlarni tozalash
    document.querySelectorAll('.tool-slots').forEach(s => s.innerHTML = '');
    document.querySelectorAll('.profession-group').forEach(g => {
        g.classList.remove('completed', 'wrong-shake', 'group-correct', 'group-wrong');
    });

    // Pool ni to'ldirish
    const pool = document.getElementById('tools-pool');
    pool.innerHTML = '';
    shuffle(tools).forEach(tool => {
        pool.appendChild(createToolEl(tool));
    });

    updateProgress();

    // Drop zone: kasblar
    document.querySelectorAll('.profession-group').forEach(group => {
        group.addEventListener('dragover', onDragOver);
        group.addEventListener('dragleave', onDragLeave);
        group.addEventListener('drop', onDrop);
    });

    // Drop zone: pool (qaytarish uchun)
    pool.addEventListener('dragover', onDragOver);
    pool.addEventListener('dragleave', onDragLeave);
    pool.addEventListener('drop', onDropPool);
}

// ===== DESKTOP DRAG & DROP =====
let draggedEl = null;

function onDragStart(e) {
    draggedEl = this;
    e.dataTransfer.setData('text/plain', this.dataset.id);
    e.dataTransfer.effectAllowed = 'move';
    this.classList.add('dragging');
}

function onDragEnd() {
    this.classList.remove('dragging');
    draggedEl = null;
}

function onDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    // Eng yaqin profession-group yoki pool ni topish
    const group = this.closest('.profession-group') || this.closest('.tools-pool');
    if (group) group.classList.add('drag-hover');
}

function onDragLeave() {
    const group = this.closest('.profession-group') || this.closest('.tools-pool');
    if (group) group.classList.remove('drag-hover');
}

function onDrop(e) {
    e.preventDefault();
    const group = this.closest('.profession-group');
    if (group) {
        group.classList.remove('drag-hover');
        const toolId = parseInt(e.dataTransfer.getData('text/plain'));
        placeTool(group, toolId);
    }
}

function onDropPool(e) {
    e.preventDefault();
    const pool = document.getElementById('tools-pool');
    pool.classList.remove('drag-hover');
    const toolId = parseInt(e.dataTransfer.getData('text/plain'));
    returnToPool(toolId);
}

// ===== MOBILE TOUCH =====
let touchEl = null;
let touchClone = null;
let tOffsetX = 0;
let tOffsetY = 0;

function onTouchStart(e) {
    touchEl = this;
    const rect = this.getBoundingClientRect();
    const touch = e.touches[0];
    tOffsetX = touch.clientX - rect.left;
    tOffsetY = touch.clientY - rect.top;

    touchClone = this.cloneNode(true);
    touchClone.style.position = 'fixed';
    touchClone.style.width = rect.width + 'px';
    touchClone.style.height = rect.height + 'px';
    touchClone.style.zIndex = '9999';
    touchClone.style.pointerEvents = 'none';
    touchClone.style.opacity = '0.85';
    touchClone.style.left = (touch.clientX - tOffsetX) + 'px';
    touchClone.style.top = (touch.clientY - tOffsetY) + 'px';
    document.body.appendChild(touchClone);
    this.classList.add('dragging');
}

document.addEventListener('touchmove', function (e) {
    if (!touchClone) return;
    e.preventDefault();
    const touch = e.touches[0];
    touchClone.style.left = (touch.clientX - tOffsetX) + 'px';
    touchClone.style.top = (touch.clientY - tOffsetY) + 'px';

    // Hover effekti
    document.querySelectorAll('.profession-group').forEach(g => {
        const r = g.getBoundingClientRect();
        if (touch.clientX >= r.left && touch.clientX <= r.right &&
            touch.clientY >= r.top && touch.clientY <= r.bottom) {
            g.classList.add('drag-hover');
        } else {
            g.classList.remove('drag-hover');
        }
    });

    const poolRect = document.getElementById('tools-pool').getBoundingClientRect();
    if (touch.clientX >= poolRect.left && touch.clientX <= poolRect.right &&
        touch.clientY >= poolRect.top && touch.clientY <= poolRect.bottom) {
        document.getElementById('tools-pool').classList.add('drag-hover');
    } else {
        document.getElementById('tools-pool').classList.remove('drag-hover');
    }
}, { passive: false });

document.addEventListener('touchend', function (e) {
    if (!touchEl || !touchClone) return;
    const touch = e.changedTouches[0];
    touchClone.remove();
    touchEl.classList.remove('dragging');

    const toolId = parseInt(touchEl.dataset.id);
    let dropped = false;

    // Kasbga tushirdimi?
    document.querySelectorAll('.profession-group').forEach(group => {
        group.classList.remove('drag-hover');
        const r = group.getBoundingClientRect();
        if (touch.clientX >= r.left && touch.clientX <= r.right &&
            touch.clientY >= r.top && touch.clientY <= r.bottom) {
            placeTool(group, toolId);
            dropped = true;
        }
    });

    // Poolga qaytardimi?
    if (!dropped) {
        const poolRect = document.getElementById('tools-pool').getBoundingClientRect();
        document.getElementById('tools-pool').classList.remove('drag-hover');
        if (touch.clientX >= poolRect.left && touch.clientX <= poolRect.right &&
            touch.clientY >= poolRect.top && touch.clientY <= poolRect.bottom) {
            returnToPool(toolId);
        }
    }

    touchEl = null;
    touchClone = null;
}, { passive: true });

// ===== JOYLASHTIRISH LOGIKASI =====
function placeTool(professionGroup, toolId) {
    const tool = tools.find(t => t.id === toolId);
    if (!tool) return;

    // Eski joydan olib tashlash (pool yoki boshqa slot)
    const existing = document.querySelector('.tool-item[data-id="' + toolId + '"]');
    if (!existing) return;

    // Tekshirish natijalarini tozalash
    clearResults();

    existing.remove();

    // Kasb slotiga qo'shish
    const slots = professionGroup.querySelector('.tool-slots');
    slots.appendChild(createToolEl(tool));

    updateProgress();
}

function returnToPool(toolId) {
    const tool = tools.find(t => t.id === toolId);
    if (!tool) return;

    const existing = document.querySelector('.tool-item[data-id="' + toolId + '"]');
    if (!existing) return;

    // Allaqachon poolda bo'lsa, hech narsa qilmaslik
    if (existing.closest('#tools-pool')) return;

    // Tekshirish natijalarini tozalash
    clearResults();

    existing.remove();

    const pool = document.getElementById('tools-pool');
    pool.appendChild(createToolEl(tool));

    updateProgress();
}

// ===== TEKSHIRISH =====
function checkAnswers() {
    const poolItems = document.querySelectorAll('#tools-pool .tool-item');
    if (poolItems.length > 0) {
        document.getElementById('result').textContent =
            "Avval barcha qurollarni kasblarga joylashtiring! (" + poolItems.length + " ta qoldi)";
        document.getElementById('result').className = 'result-msg fail';
        return;
    }

    let correct = 0;

    document.querySelectorAll('.profession-group').forEach(group => {
        const profession = group.dataset.profession;
        const toolEls = group.querySelectorAll('.tool-slots .tool-item');

        toolEls.forEach(el => {
            const toolProfession = el.dataset.profession;
            if (toolProfession === profession) {
                el.classList.add('tool-correct');
                correct++;
            } else {
                el.classList.add('tool-wrong');
            }
        });

        // Kasb guruhini belgilash
        const allCorrect = Array.from(toolEls).every(el => el.dataset.profession === profession);
        const expectedCount = tools.filter(t => t.profession === profession).length;
        if (allCorrect && toolEls.length === expectedCount) {
            group.classList.add('group-correct');
        }
    });

    if (correct === TOTAL) {
        document.getElementById('result').textContent = "Barakalla! Barcha ish qurollari to'g'ri joylashtirildi!";
        document.getElementById('result').className = 'result-msg success';
    } else {
        document.getElementById('result').textContent =
            correct + ' / ' + TOTAL + " ta to'g'ri. Xatolarni tuzating va qayta tekshiring!";
        document.getElementById('result').className = 'result-msg fail';
    }

    document.getElementById('retry-btn').style.display = '';
}

function clearResults() {
    document.querySelectorAll('.tool-correct').forEach(el => el.classList.remove('tool-correct'));
    document.querySelectorAll('.tool-wrong').forEach(el => el.classList.remove('tool-wrong'));
    document.querySelectorAll('.group-correct').forEach(el => el.classList.remove('group-correct'));
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
}

function retry() {
    init();
}

// Boshlash
init();
