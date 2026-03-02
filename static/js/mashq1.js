const correctAnswers = ['badiiy', 'geometrik-shaklli', 'mazmunli', 'geometrik-predmetli', 'dekorativ'];

function toggle(btn) {
    btn.classList.toggle('checked');
    btn.textContent = btn.classList.contains('checked') ? '✓' : '';

    // Oldingi natijani tozalash
    btn.classList.remove('correct', 'wrong');
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
}

function checkAnswers() {
    const allBtns = document.querySelectorAll('.checkbox-btn');
    let allCorrect = true;

    allBtns.forEach(btn => {
        const answer = btn.dataset.answer;
        const isChecked = btn.classList.contains('checked');
        const isCorrect = correctAnswers.includes(answer);

        btn.classList.remove('correct', 'wrong');

        if (isChecked && isCorrect) {
            btn.classList.add('correct');
        } else if (isChecked && !isCorrect) {
            btn.classList.add('wrong');
            allCorrect = false;
        } else if (!isChecked && isCorrect) {
            allCorrect = false;
        }
    });

    const resultEl = document.getElementById('result');
    const retryBtn = document.getElementById('retry-btn');
    if (allCorrect) {
        resultEl.textContent = "Barakalla! Barcha javoblar to'g'ri!";
        resultEl.className = 'result-msg success';
        retryBtn.style.display = 'none';
    } else {
        resultEl.textContent = "Noto'g'ri javoblar bor. Qaytadan urinib ko'ring!";
        resultEl.className = 'result-msg fail';
        retryBtn.style.display = 'inline-block';
    }

    // Natijani serverga yuborish
    fetch('/api/save-result', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({mashq: 'm1', score: allCorrect ? 1 : 0, total: 1, is_passed: allCorrect})
    }).catch(() => {});
}

function resetQuiz() {
    const allBtns = document.querySelectorAll('.checkbox-btn');
    allBtns.forEach(btn => {
        btn.classList.remove('checked', 'correct', 'wrong');
        btn.textContent = '';
    });
    document.getElementById('result').textContent = '';
    document.getElementById('result').className = 'result-msg';
    document.getElementById('retry-btn').style.display = 'none';
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