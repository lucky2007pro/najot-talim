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
    score: 0, // Local offline score tracking
    user: null, // User profile data
    token: localStorage.getItem('access_token') || null
};

let authMode = 'login'; // 'login' or 'register'

// --- Audio TTS ---
function playTTS(elementId) {
    const text = document.getElementById(elementId).innerText;
    if (!text) return;
    
    // Stop any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'uz-UZ'; // Try Uzbek
    // Fallback language handling could be added here
    window.speechSynthesis.speak(utterance);
}

// --- Auth Handling ---
function showAuthModal(mode) {
    authMode = mode;
    document.getElementById('auth-title').innerText = mode === 'login' ? 'Kirish' : "Ro'yxatdan o'tish";
    document.getElementById('auth-error').classList.add('hidden');
    document.getElementById('auth-modal').classList.remove('hidden');
    document.getElementById('auth-modal').classList.add('flex');
}

function closeAuthModal() {
    document.getElementById('auth-modal').classList.add('hidden');
    document.getElementById('auth-modal').classList.remove('flex');
}

async function handleAuth(e) {
    e.preventDefault();
    const username = document.getElementById('auth-username').value;
    const password = document.getElementById('auth-password').value;
    const errorEl = document.getElementById('auth-error');
    
    try {
        const endpoint = authMode === 'login' ? '/auth/login/' : '/auth/register/';
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        const data = await res.json();
        
        if (!res.ok) {
            throw new Error(data.error || data.detail || 'Xatolik yuz berdi');
        }
        
        // Save token
        const token = authMode === 'login' ? data.access : data.tokens.access;
        localStorage.setItem('access_token', token);
        state.token = token;
        
        closeAuthModal();
        await fetchProfile();
        
    } catch (err) {
        errorEl.innerText = err.message;
        errorEl.classList.remove('hidden');
    }
}

function logout() {
    localStorage.removeItem('access_token');
    state.token = null;
    state.user = null;
    updateAuthUI();
}

async function fetchProfile() {
    if (!state.token) return;
    try {
        const res = await fetch(`${API_BASE}/profile/`, {
            headers: { 'Authorization': `Bearer ${state.token}` }
        });
        if (res.ok) {
            const data = await res.json();
            state.user = data.user;
            updateAuthUI();
        } else {
            logout();
        }
    } catch (e) {
        console.log("Offline, profile not fetched");
    }
}

function updateAuthUI() {
    const authBtns = document.getElementById('auth-buttons');
    const profileHeader = document.getElementById('user-profile-header');
    
    if (state.user) {
        authBtns.classList.add('hidden');
        profileHeader.classList.remove('hidden');
        document.getElementById('header-username').innerText = state.user.username;
        document.getElementById('header-level').innerText = `Lvl ${state.user.profile.level}`;
        document.getElementById('header-xp').innerText = state.user.profile.xp;
    } else {
        authBtns.classList.remove('hidden');
        profileHeader.classList.add('hidden');
    }
}

// Screens - only grab elements that exist on this page
const screens = {};
['intro', 'education', 'quiz', 'result'].forEach(name => {
    const el = document.getElementById('screen-' + name);
    if (el) screens[name] = el;
});

function showScreen(screenName) {
    Object.values(screens).forEach(s => s.classList.add('hidden'));
    if (screens[screenName]) {
        screens[screenName].classList.remove('hidden');
        screens[screenName].style.animation = 'none';
        screens[screenName].offsetHeight; 
        screens[screenName].style.animation = ''; 
        screens[screenName].style.opacity = '1';
    }
}

// --- Network / Offline Helper ---
async function fetchWithCache(url, cacheKey) {
    const headers = {};
    if (state.token) {
        headers['Authorization'] = `Bearer ${state.token}`;
    }
    try {
        const res = await fetch(url, { headers });
        if (!res.ok) throw new Error('Server error: ' + res.status);
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
    await fetchProfile(); // Auth setup
    
    try {
        const topics = await fetchWithCache(`${API_BASE}/intro/`, 'api_intro');
        if (topics && topics.length > 0) {
            const topic = topics[0];
            state.topicId = topic.id;
            const titleEl = document.getElementById('intro-title');
            const descEl = document.getElementById('intro-desc');
            if (titleEl) titleEl.innerText = topic.title;
            if (descEl) descEl.innerText = topic.description;
        } else {
            const titleEl = document.getElementById('intro-title');
            if (titleEl) titleEl.innerText = "Ma'lumot topilmadi";
        }
    } catch (error) {
        console.error("API error:", error);
        const titleEl = document.getElementById('intro-title');
        if (titleEl) titleEl.innerText = "Oflayn rejim (Ma'lumotlar yo'q)";
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
        const titleEl = document.getElementById('edu-title');
        const contentEl = document.getElementById('edu-content');
        if (titleEl) titleEl.innerText = "Oflayn xatolik";
        if (contentEl) contentEl.innerText = "Darsliklarni yuklash uchun internet kerak.";
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
        // Har doim yangi tasodifiy savollar olish uchun cache'dan foydalanmaymiz
        // Eski cache'ni tozalaymiz
        localStorage.removeItem(`api_quiz_${state.topicId}`);
        
        const headers = {};
        if (state.token) {
            headers['Authorization'] = `Bearer ${state.token}`;
        }
        
        const res = await fetch(`${API_BASE}/topic/${state.topicId}/quiz/`, { headers });
        if (!res.ok) throw new Error('Server error: ' + res.status);
        const data = await res.json();
        
        // Offline uchun cache'ga saqlaymiz
        localStorage.setItem(`api_quiz_${state.topicId}`, JSON.stringify(data));
        
        state.questions = data;
        state.currentQuestionIndex = 0;
        state.answers = {};
        state.score = 0;
        renderQuestion();
    } catch (e) {
        console.error(e);
        // Offline bo'lsa, cache'dan foydalanishga harakat qilamiz
        const cached = localStorage.getItem(`api_quiz_${state.topicId}`);
        if (cached) {
            const data = JSON.parse(cached);
            state.questions = data;
            state.currentQuestionIndex = 0;
            state.answers = {};
            state.score = 0;
            renderQuestion();
        } else {
            document.getElementById('quiz-question').innerText = "Savollarni yuklashda xatolik.";
        }
    }
}

function renderQuestion() {
    if (!state.questions || state.questions.length === 0) {
        document.getElementById('quiz-question').innerText = "Kechirasiz, savollar topilmadi. (Baza bo'sh yoki yangilanmagan)";
        document.getElementById('btn-next-quiz').style.display = 'none';
        return;
    }
    const q = state.questions[state.currentQuestionIndex];
    if (!q) return;

    state.selectedChoiceId = null;
    state.selectedChoiceIsCorrect = false;
    document.getElementById('btn-next-quiz').disabled = true;
    document.getElementById('btn-next-quiz').style.display = ''; // Re-show button

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
        nextBtn.innerText = "Keyingi savol ➡️";
    }
}

function selectChoice(choiceId, isCorrect, element) {
    if (document.getElementById('btn-next-quiz').disabled === false) return;

    state.selectedChoiceId = choiceId;
    state.selectedChoiceIsCorrect = isCorrect;
    
    // Disable other choices
    document.querySelectorAll('.choice-btn').forEach(b => {
        b.onclick = null;
        b.style.opacity = '0.5';
    });
    
    element.style.opacity = '1';

    // Interactive Reaction
    if (isCorrect) {
        element.classList.add('correct');
        state.score++;
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
            username: state.user ? state.user.username : "Yosh Fazogir",
            answers: state.answers,
            total_questions: total_questions
        };

        const headers = { 'Content-Type': 'application/json' };
        if (state.token) {
            headers['Authorization'] = `Bearer ${state.token}`;
        }

        const res = await fetch(`${API_BASE}/topic/${state.topicId}/quiz/submit/`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        showScreen('result');
        
        if (data.earned_xp) {
            data.message += `\nSiz ${data.earned_xp} XP yig'dingiz! 🌟`;
        }
        
        document.getElementById('score-display').innerText = `${data.score} / ${data.max_score}`;
        document.getElementById('result-message').innerText = data.message;
        
        if (state.token) {
            await fetchProfile(); // Update XP in header
        }
        
        if (data.score === data.max_score && data.max_score > 0) {
            triggerVictoryConfetti();
        }

    } catch (e) {
        console.log("Offline mode: calculating local score.");
        showScreen('result');
        document.getElementById('score-display').innerText = `${state.score} / ${total_questions}`;
        
        const percentage = (state.score / total_questions) * 100;
        if (percentage === 100) {
            finalMessage = "Ajoyib!";
            triggerVictoryConfetti();
        }
        else if (percentage >= 60) finalMessage = "Yaxshi natija!";
        else finalMessage = "Yana o'qib chiqish kerak!";
        
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

// Note: init() is called by enterApp() in index.html
// Do NOT auto-call init() here as it conflicts with the landing page
