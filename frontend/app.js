const API_BASE = '/api';

// State
let state = {
    topicId: null,
    sections: [],
    currentSectionIndex: 0,
    questions: [],
    currentQuestionIndex: 0,
    answers: {},
    selectedChoiceId: null,
    selectedChoiceIsCorrect: false,
    score: 0 // Local offline score tracking
};

// Screens
const screens = {
    intro: document.getElementById('screen-intro'),
    education: document.getElementById('screen-education'),
    quiz: document.getElementById('screen-quiz'),
    result: document.getElementById('screen-result')
};

function showScreen(screenName) {
    Object.values(screens).forEach(s => s.classList.add('hidden'));
    screens[screenName].classList.remove('hidden');
    // Basic re-trigger animation
    screens[screenName].style.animation = 'none';
    screens[screenName].offsetHeight; 
    screens[screenName].style.animation = ''; 
    screens[screenName].style.opacity = '1'; // Force opacity
}

// --- Network / Offline Helper ---
async function fetchWithCache(url, cacheKey) {
    try {
        const res = await fetch(url);
        const data = await res.json();
        localStorage.setItem(cacheKey, JSON.stringify(data));
        return data;
    } catch (err) {
        console.log(`Fetch failed for ${url}, trying offline cache...`);
        const cached = localStorage.getItem(cacheKey);
        if (cached) {
            return JSON.parse(cached);
        }
        throw err;
    }
}

// --- Init & Intro ---
async function init() {
    try {
        const topics = await fetchWithCache(`${API_BASE}/intro/`, 'api_intro');
        if (topics && topics.length > 0) {
            const topic = topics[0];
            state.topicId = topic.id;
            document.getElementById('intro-title').innerText = topic.title;
            document.getElementById('intro-desc').innerText = topic.description;
        } else {
            document.getElementById('intro-title').innerText = "Ma'lumot topilmadi";
        }
    } catch (error) {
        console.error("API error:", error);
        document.getElementById('intro-title').innerText = "Oflayn rejim (Ma'lumotlar yo'q)";
    }
}

// --- Education ---
async function startEducation() {
    showScreen('education');
    try {
        const data = await fetchWithCache(`${API_BASE}/topic/${state.topicId}/sections/`, `api_sections_${state.topicId}`);
        state.sections = data;
        state.currentSectionIndex = 0;
        renderSection();
    } catch (e) {
        console.error(e);
        document.getElementById('edu-title').innerText = "Oflayn xatolik";
        document.getElementById('edu-content').innerText = "Darsliklarni yuklash uchun internet kerak.";
    }
}

function renderSection() {
    const sec = state.sections[state.currentSectionIndex];
    if (!sec) return;

    const progress = ((state.currentSectionIndex + 1) / state.sections.length) * 100;
    document.getElementById('edu-progress').style.width = `${progress}%`;

    document.getElementById('edu-title').innerText = sec.title;
    document.getElementById('edu-content').innerText = sec.content;
    
    const mediaContainer = document.getElementById('edu-media');
    if (sec.media_url) {
        mediaContainer.innerHTML = `<img src="${sec.media_url}" alt="${sec.title}">`;
    } else {
        mediaContainer.innerHTML = '';
    }

    const btn = document.getElementById('btn-next-edu');
    if (state.currentSectionIndex === state.sections.length - 1) {
        btn.innerText = "Testni boshlash 📝";
    } else {
        btn.innerText = "Keyingisi ➡️";
    }
}

function nextEducation() {
    if (state.currentSectionIndex < state.sections.length - 1) {
        state.currentSectionIndex++;
        renderSection();
    } else {
        startQuiz();
    }
}

// --- Quiz ---
async function startQuiz() {
    showScreen('quiz');
    try {
        const data = await fetchWithCache(`${API_BASE}/topic/${state.topicId}/quiz/`, `api_quiz_${state.topicId}`);
        state.questions = data;
        state.currentQuestionIndex = 0;
        state.answers = {};
        state.score = 0;
        renderQuestion();
    } catch (e) {
        console.error(e);
    }
}

function renderQuestion() {
    const q = state.questions[state.currentQuestionIndex];
    if (!q) return;

    state.selectedChoiceId = null;
    state.selectedChoiceIsCorrect = false;
    document.getElementById('btn-next-quiz').disabled = true;

    const progress = ((state.currentQuestionIndex + 1) / state.questions.length) * 100;
    document.getElementById('quiz-progress').style.width = `${progress}%`;

    document.getElementById('quiz-question').innerText = q.text;
    
    const choicesDiv = document.getElementById('quiz-choices');
    choicesDiv.innerHTML = '';
    
    q.choices.forEach(choice => {
        const btn = document.createElement('div');
        btn.className = 'choice-btn';
        btn.innerText = choice.text;
        btn.onclick = () => selectChoice(choice.id, choice.is_correct, btn);
        choicesDiv.appendChild(btn);
    });

    const nextBtn = document.getElementById('btn-next-quiz');
    if (state.currentQuestionIndex === state.questions.length - 1) {
        nextBtn.innerText = "Natijani ko'rish 🏆";
    } else {
        nextBtn.innerText = "Javobni tasdiqlash ✅";
    }
}

function selectChoice(choiceId, isCorrect, element) {
    if (document.getElementById('btn-next-quiz').disabled === false) return; // Allready answered this question

    state.selectedChoiceId = choiceId;
    state.selectedChoiceIsCorrect = isCorrect;
    
    // Disable other choices
    document.querySelectorAll('.choice-btn').forEach(b => {
        b.onclick = null; // Remove listener so they can't click again
        b.style.opacity = '0.5';
    });
    
    element.style.opacity = '1';

    // Interactive Reaction
    if (isCorrect) {
        element.classList.add('correct');
        state.score++; // local tally
        if (typeof confetti === 'function') {
            confetti({
                particleCount: 100,
                spread: 70,
                origin: { y: 0.6 }
            });
        }
    } else {
        element.classList.add('wrong');
        element.classList.add('shake');
        // Optionally show which one was correct
        const allBtns = document.querySelectorAll('.choice-btn');
        state.questions[state.currentQuestionIndex].choices.forEach((c, idx) => {
            if (c.is_correct) {
                allBtns[idx].classList.add('correct');
            }
        });
    }
    
    document.getElementById('btn-next-quiz').disabled = false;
}

function nextQuiz() {
    const qId = state.questions[state.currentQuestionIndex].id;
    state.answers[qId] = state.selectedChoiceId;

    if (state.currentQuestionIndex < state.questions.length - 1) {
        state.currentQuestionIndex++;
        renderQuestion();
    } else {
        submitQuiz();
    }
}

// --- Result ---
async function submitQuiz() {
    const total_questions = state.questions.length;
    let finalMessage = "";

    try {
        const payload = {
            username: "Yosh Fazogir",
            answers: state.answers,
            total_questions: total_questions
        };

        const res = await fetch(`${API_BASE}/topic/${state.topicId}/quiz/submit/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        showScreen('result');
        document.getElementById('score-display').innerText = `${data.score} / ${data.max_score}`;
        document.getElementById('result-message').innerText = data.message;
        
        if (data.score === data.max_score && data.max_score > 0) {
            triggerVictoryConfetti();
        }

    } catch (e) {
        console.log("Offline mode: calculating local score.");
        // OFFLINE Fallback
        showScreen('result');
        document.getElementById('score-display').innerText = `${state.score} / ${total_questions}`;
        
        const percentage = (state.score / total_questions) * 100;
        if (percentage === 100) {
            finalMessage = "Ajoyib! (Oflayn hisoblandi)";
            triggerVictoryConfetti();
        }
        else if (percentage >= 60) finalMessage = "Yaxshi natija! (Oflayn hisoblandi)";
        else finalMessage = "Yana o'qib chiqish kerak! (Oflayn hisoblandi)";
        
        document.getElementById('result-message').innerText = finalMessage;
    }
}

function triggerVictoryConfetti() {
    if (typeof confetti === 'function') {
        var duration = 3 * 1000;
        var end = Date.now() + duration;

        (function frame() {
            confetti({
                particleCount: 5,
                angle: 60,
                spread: 55,
                origin: { x: 0 },
                colors: ['#00D2D3', '#facc15']
            });
            confetti({
                particleCount: 5,
                angle: 120,
                spread: 55,
                origin: { x: 1 },
                colors: ['#00D2D3', '#facc15']
            });

            if (Date.now() < end) {
                requestAnimationFrame(frame);
            }
        }());
    }
}

function restart() {
    if (typeof restartApp === "function") {
        restartApp();
    } else {
        showScreen('intro');
    }
}

// Start app
window.onload = init;
