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
