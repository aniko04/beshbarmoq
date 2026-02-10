let draggedItem = null;

// ===== DESKTOP: Drag & Drop =====
document.addEventListener('dragstart', function (e) {
    if (!e.target.classList.contains('drag-item')) return;
    draggedItem = e.target;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
});

document.addEventListener('dragend', function (e) {
    if (!e.target.classList.contains('drag-item')) return;
    e.target.classList.remove('dragging');
    document.querySelectorAll('.drop-zone').forEach(z => z.classList.remove('drag-over'));
    draggedItem = null;
});

document.querySelectorAll('.drop-zone, #drag-area').forEach(zone => {
    zone.addEventListener('dragover', function (e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        if (zone.classList.contains('drop-zone')) {
            zone.classList.add('drag-over');
        }
    });

    zone.addEventListener('dragleave', function () {
        zone.classList.remove('drag-over');
    });

    zone.addEventListener('drop', function (e) {
        e.preventDefault();
        zone.classList.remove('drag-over');
        if (!draggedItem) return;

        draggedItem.classList.remove('correct-placed', 'wrong-placed');
        clearResult();

        if (zone.id === 'drag-area') {
            zone.appendChild(draggedItem);
        } else {
            const itemsContainer = zone.querySelector('.zone-items');
            itemsContainer.appendChild(draggedItem);
        }
    });
});

// ===== MOBILE: Touch Drag =====
let touchItem = null;
let touchClone = null;
let offsetX = 0;
let offsetY = 0;

document.addEventListener('touchstart', function (e) {
    const item = e.target.closest('.drag-item');
    if (!item) return;

    touchItem = item;
    const rect = item.getBoundingClientRect();
    const touch = e.touches[0];
    offsetX = touch.clientX - rect.left;
    offsetY = touch.clientY - rect.top;

    touchClone = item.cloneNode(true);
    touchClone.style.position = 'fixed';
    touchClone.style.width = rect.width + 'px';
    touchClone.style.zIndex = '9999';
    touchClone.style.pointerEvents = 'none';
    touchClone.style.opacity = '0.85';
    touchClone.style.left = (touch.clientX - offsetX) + 'px';
    touchClone.style.top = (touch.clientY - offsetY) + 'px';
    document.body.appendChild(touchClone);

    item.classList.add('dragging');
}, { passive: true });

document.addEventListener('touchmove', function (e) {
    if (!touchClone) return;
    e.preventDefault();
    const touch = e.touches[0];
    touchClone.style.left = (touch.clientX - offsetX) + 'px';
    touchClone.style.top = (touch.clientY - offsetY) + 'px';

    document.querySelectorAll('.drop-zone').forEach(z => {
        const rect = z.getBoundingClientRect();
        if (touch.clientX >= rect.left && touch.clientX <= rect.right &&
            touch.clientY >= rect.top && touch.clientY <= rect.bottom) {
            z.classList.add('drag-over');
        } else {
            z.classList.remove('drag-over');
        }
    });
}, { passive: false });

document.addEventListener('touchend', function (e) {
    if (!touchItem || !touchClone) return;

    const touch = e.changedTouches[0];
    touchClone.remove();
    touchItem.classList.remove('dragging');
    touchItem.classList.remove('correct-placed', 'wrong-placed');
    clearResult();

    let dropped = false;

    document.querySelectorAll('.drop-zone').forEach(zone => {
        zone.classList.remove('drag-over');
        const rect = zone.getBoundingClientRect();
        if (touch.clientX >= rect.left && touch.clientX <= rect.right &&
            touch.clientY >= rect.top && touch.clientY <= rect.bottom) {
            zone.querySelector('.zone-items').appendChild(touchItem);
            dropped = true;
        }
    });

    if (!dropped) {
        const dragArea = document.getElementById('drag-area');
        const rect = dragArea.getBoundingClientRect();
        if (touch.clientX >= rect.left && touch.clientX <= rect.right &&
            touch.clientY >= rect.top && touch.clientY <= rect.bottom) {
            dragArea.appendChild(touchItem);
        }
    }

    touchItem = null;
    touchClone = null;
}, { passive: true });

// ===== TEKSHIRISH =====
function checkAnswers2() {
    let allCorrect = true;
    let allPlaced = true;

    const allItems = document.querySelectorAll('.drag-item');

    allItems.forEach(item => {
        item.classList.remove('correct-placed', 'wrong-placed');

        const zone = item.closest('.drop-zone');
        if (!zone) {
            allPlaced = false;
            return;
        }

        const zoneName = zone.dataset.zone;
        const correct = item.dataset.correct;

        if (zoneName === correct) {
            item.classList.add('correct-placed');
        } else {
            item.classList.add('wrong-placed');
            allCorrect = false;
        }
    });

    const resultEl = document.getElementById('result');
    const retryBtn = document.getElementById('retry-btn');

    if (!allPlaced) {
        resultEl.textContent = "Barcha kartochkalarni joylashtiring!";
        resultEl.className = 'result-msg fail';
        retryBtn.style.display = 'none';
    } else if (allCorrect) {
        resultEl.textContent = "Barakalla! Barcha javoblar to'g'ri!";
        resultEl.className = 'result-msg success';
        retryBtn.style.display = 'none';
    } else {
        resultEl.textContent = "Noto'g'ri javoblar bor. Qaytadan urinib ko'ring!";
        resultEl.className = 'result-msg fail';
        retryBtn.style.display = 'inline-block';
    }
}

function resetQuiz2() {
    const dragArea = document.getElementById('drag-area');
    const allItems = document.querySelectorAll('.drag-item');

    allItems.forEach(item => {
        item.classList.remove('correct-placed', 'wrong-placed');
        dragArea.appendChild(item);
    });

    clearResult();
    document.getElementById('retry-btn').style.display = 'none';
}

function clearResult() {
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
}
