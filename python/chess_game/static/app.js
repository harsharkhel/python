/**
 * GrandMaster AI — Frontend Application
 *
 * Handles board rendering, user interaction, API communication,
 * clocks, sounds, and all game UI logic.
 */

// ══════════════════════════════════════════════════════════
// State
// ══════════════════════════════════════════════════════════

const STATE = {
    mode: 'pvai',
    difficulty: 3,
    time: 300,
    selectedSquare: null,
    legalMoves: [],
    gameState: null,       // last server state
    clockInterval: null,
    clockWhite: 300,
    clockBlack: 300,
    clockActive: 'white',
    clockRunning: false,
    unlimited: false,
    aiThinking: false,
    promotionPending: null, // { from, to }
};

// Piece Unicode symbols
const PIECES = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
};

const DIFF_DESCRIPTIONS = {
    1: 'Beginner • ~600 Elo',
    2: 'Easy • ~900 Elo',
    3: 'Medium • ~1200 Elo',
    4: 'Hard • ~1400 Elo',
    5: 'Expert • ~1600 Elo',
    6: 'Master • ~1800 Elo',
};

// ══════════════════════════════════════════════════════════
// Sound Engine (Web Audio API)
// ══════════════════════════════════════════════════════════

let audioCtx = null;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playTone(freq, durMs, vol = 0.15) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.value = freq;
    osc.type = 'sine';

    const now = audioCtx.currentTime;
    const dur = durMs / 1000;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(vol, now + Math.min(0.01, dur * 0.2));
    gain.gain.linearRampToValueAtTime(0, now + dur);

    osc.start(now);
    osc.stop(now + dur);
}

function playSound(name) {
    initAudio();
    switch (name) {
        case 'move':      playTone(600, 70);  break;
        case 'capture':   playTone(400, 110); break;
        case 'check':     playTone(800, 140); break;
        case 'castle':    playTone(500, 90);  break;
        case 'game_over': playTone(300, 280); break;
    }
}

// ══════════════════════════════════════════════════════════
// Screen Navigation
// ══════════════════════════════════════════════════════════

function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function showSpinner(on) {
    document.getElementById('spinner').classList.toggle('active', on);
}

// ══════════════════════════════════════════════════════════
// Menu Logic
// ══════════════════════════════════════════════════════════

function initMenu() {
    // Mode buttons
    document.querySelectorAll('#mode-group .menu-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#mode-group .menu-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            STATE.mode = btn.dataset.mode;
            // Show/hide difficulty
            document.getElementById('difficulty-section').style.display =
                STATE.mode === 'pvp' ? 'none' : '';
        });
    });

    // Difficulty buttons
    document.querySelectorAll('#diff-group .menu-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#diff-group .menu-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            STATE.difficulty = parseInt(btn.dataset.diff);
            document.getElementById('diff-desc').textContent =
                DIFF_DESCRIPTIONS[STATE.difficulty] || '';
        });
    });

    // Time control buttons
    document.querySelectorAll('#tc-group .menu-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('#tc-group .menu-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            STATE.time = btn.dataset.time === 'null' ? null : parseInt(btn.dataset.time);
        });
    });

    // Start
    document.getElementById('start-btn').addEventListener('click', startGame);

    // Stats
    document.getElementById('stats-link').addEventListener('click', () => {
        loadStats();
        showScreen('stats-screen');
    });

    // Stats back
    document.getElementById('stats-back-btn').addEventListener('click', () => {
        showScreen('menu-screen');
    });
}

// ══════════════════════════════════════════════════════════
// Game Start
// ══════════════════════════════════════════════════════════

async function startGame() {
    initAudio();
    showSpinner(true);

    try {
        const res = await fetch('/api/new', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                mode: STATE.mode,
                difficulty: STATE.difficulty,
                time: STATE.time,
            }),
        });
        const data = await res.json();
        STATE.gameState = data;
        STATE.selectedSquare = null;
        STATE.aiThinking = false;
        STATE.promotionPending = null;

        // Clock setup
        STATE.unlimited = data.unlimited;
        STATE.clockWhite = data.clock_white_raw;
        STATE.clockBlack = data.clock_black_raw;
        STATE.clockActive = 'white';
        STATE.clockRunning = false;

        // Update names
        if (STATE.mode !== 'pvp') {
            document.getElementById('clock-white-name').textContent = 'White (You)';
            document.getElementById('clock-black-name').textContent = 'Black (AI)';
        } else {
            document.getElementById('clock-white-name').textContent = 'White';
            document.getElementById('clock-black-name').textContent = 'Black';
        }

        // Show/hide eval bar & coach panel
        const evalBar = document.getElementById('eval-bar');
        const coachPanel = document.getElementById('coach-panel');
        if (STATE.mode === 'pvp') {
            evalBar.style.display = 'none';
            coachPanel.style.display = 'none';
        } else {
            evalBar.style.display = '';
            coachPanel.style.display = '';
        }

        initBoard();
        renderState(data);
        startClockInterval();
        showScreen('game-screen');

        // Hide game over overlay
        document.getElementById('game-over-overlay').classList.remove('active');
    } catch (e) {
        console.error('Failed to start game:', e);
    } finally {
        showSpinner(false);
    }
}

// ══════════════════════════════════════════════════════════
// Board Initialization & Rendering
// ══════════════════════════════════════════════════════════

function initBoard() {
    const board = document.getElementById('chessboard');
    board.innerHTML = '';

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const sq = document.createElement('div');
            const rank = 8 - row;
            const file = String.fromCharCode(97 + col); // a-h
            const sqName = file + rank;

            sq.className = 'square ' + ((row + col) % 2 === 0 ? 'light' : 'dark');
            sq.dataset.square = sqName;
            sq.addEventListener('click', () => onSquareClick(sqName));
            board.appendChild(sq);
        }
    }

    // Rank labels
    const rankLabels = document.getElementById('rank-labels');
    rankLabels.innerHTML = '';
    for (let i = 8; i >= 1; i--) {
        const lbl = document.createElement('div');
        lbl.className = 'rank-label';
        lbl.textContent = i;
        rankLabels.appendChild(lbl);
    }

    // File labels
    const fileLabels = document.getElementById('file-labels');
    fileLabels.innerHTML = '';
    for (const f of 'abcdefgh') {
        const lbl = document.createElement('div');
        lbl.className = 'file-label';
        lbl.textContent = f;
        fileLabels.appendChild(lbl);
    }
}

function parseFEN(fen) {
    // Returns { square_name: piece_char } from a FEN string
    const pieces = {};
    const parts = fen.split(' ');
    const rows = parts[0].split('/');

    for (let r = 0; r < 8; r++) {
        let col = 0;
        for (const ch of rows[r]) {
            if (ch >= '1' && ch <= '8') {
                col += parseInt(ch);
            } else {
                const file = String.fromCharCode(97 + col);
                const rank = 8 - r;
                pieces[file + rank] = ch;
                col++;
            }
        }
    }
    return pieces;
}

function renderState(state) {
    if (!state || !state.fen) return;

    STATE.gameState = state;
    const pieces = parseFEN(state.fen);

    // Clear all squares
    document.querySelectorAll('.square').forEach(sq => {
        sq.innerHTML = '';
        sq.classList.remove('selected', 'last-move', 'check');
    });

    // Place pieces
    for (const [sqName, pieceChar] of Object.entries(pieces)) {
        const sq = document.querySelector(`.square[data-square="${sqName}"]`);
        if (!sq) continue;

        const pieceEl = document.createElement('span');
        pieceEl.className = 'piece ' + (pieceChar === pieceChar.toUpperCase() ? 'white-piece' : 'black-piece');
        pieceEl.textContent = PIECES[pieceChar] || pieceChar;
        sq.appendChild(pieceEl);
    }

    // Last move highlight
    if (state.last_move) {
        const from = state.last_move.substring(0, 2);
        const to = state.last_move.substring(2, 4);
        const fromSq = document.querySelector(`.square[data-square="${from}"]`);
        const toSq = document.querySelector(`.square[data-square="${to}"]`);
        if (fromSq) fromSq.classList.add('last-move');
        if (toSq) toSq.classList.add('last-move');
    }

    // Check highlight
    if (state.check_square) {
        const checkSq = document.querySelector(`.square[data-square="${state.check_square}"]`);
        if (checkSq) checkSq.classList.add('check');
    }

    // Selected square + legal moves
    if (STATE.selectedSquare) {
        const selSq = document.querySelector(`.square[data-square="${STATE.selectedSquare}"]`);
        if (selSq) selSq.classList.add('selected');

        // Show legal move indicators
        const legalDests = state.legal_moves
            .filter(m => m.from === STATE.selectedSquare)
            .map(m => m.to);

        for (const dest of legalDests) {
            const destSq = document.querySelector(`.square[data-square="${dest}"]`);
            if (!destSq) continue;
            const hasPiece = pieces[dest];
            const indicator = document.createElement('div');
            indicator.className = hasPiece ? 'legal-capture' : 'legal-dot';
            destSq.appendChild(indicator);
        }
    }

    // Update clocks
    updateClockDisplay(state);

    // Update eval bar
    if (STATE.mode !== 'pvp') {
        updateEvalBar(state.current_eval, state.eval_formatted);
    }

    // Update coach panel
    if (STATE.mode !== 'pvp') {
        updateCoachPanel(state);
    }

    // Update move log
    updateMoveLog(state.move_log);

    // Game over check
    if (state.state === 'game_over') {
        STATE.clockRunning = false;
        showGameOver(state.result_text, state.reason_text);
        playSound('game_over');
    }
}

// ══════════════════════════════════════════════════════════
// Square Click Handler
// ══════════════════════════════════════════════════════════

function onSquareClick(sqName) {
    const state = STATE.gameState;
    if (!state || state.state !== 'playing') return;
    if (STATE.aiThinking) return;

    // Check if it's human's turn
    const isHumanTurn = STATE.mode === 'pvp' ||
        state.turn === state.player_color;
    if (!isHumanTurn) return;

    // If a piece is selected and this is a legal destination
    if (STATE.selectedSquare) {
        const legalDests = state.legal_moves
            .filter(m => m.from === STATE.selectedSquare)
            .map(m => m.to);

        if (legalDests.includes(sqName)) {
            // Check for promotion
            const promoMoves = state.legal_moves.filter(
                m => m.from === STATE.selectedSquare && m.to === sqName && m.promotion
            );

            if (promoMoves.length > 0) {
                // Show promotion dialog
                STATE.promotionPending = { from: STATE.selectedSquare, to: sqName };
                showPromotionDialog(state.turn === 'white');
                return;
            }

            // Normal move
            makeMove(STATE.selectedSquare, sqName);
            return;
        }
    }

    // Select a new piece (or deselect)
    const pieces = parseFEN(state.fen);
    const piece = pieces[sqName];

    if (piece) {
        const isWhitePiece = piece === piece.toUpperCase();
        const isCurrentTurn = (state.turn === 'white' && isWhitePiece) ||
                              (state.turn === 'black' && !isWhitePiece);

        if (isCurrentTurn) {
            STATE.selectedSquare = sqName;
            renderState(state);
            return;
        }
    }

    // Deselect
    STATE.selectedSquare = null;
    renderState(state);
}

// ══════════════════════════════════════════════════════════
// Make Move (API call)
// ══════════════════════════════════════════════════════════

async function makeMove(from, to, promotion = null) {
    STATE.selectedSquare = null;

    if (STATE.mode !== 'pvp') {
        STATE.aiThinking = true;
        updateCoachThinking(true);
    }

    showSpinner(true);

    try {
        const body = { from, to };
        if (promotion) body.promotion = promotion;

        const res = await fetch('/api/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body),
        });

        const data = await res.json();

        if (data.error) {
            console.error('Move error:', data.error);
            STATE.aiThinking = false;
            return;
        }

        // Play human move sound
        if (data.sound) playSound(data.sound);

        // Sync clocks from server
        if (data.state) {
            STATE.clockWhite = data.state.clock_white_raw;
            STATE.clockBlack = data.state.clock_black_raw;
            STATE.clockActive = data.state.clock_active;
            STATE.unlimited = data.state.unlimited;

            if (data.state.move_count >= 1) {
                STATE.clockRunning = true;
            }
        }

        // If AI moved, play its sound after a brief delay
        if (data.ai_sound) {
            setTimeout(() => playSound(data.ai_sound), 150);
        }

        STATE.aiThinking = false;
        renderState(data.state);

    } catch (e) {
        console.error('Move failed:', e);
        STATE.aiThinking = false;
    } finally {
        showSpinner(false);
        updateCoachThinking(false);
    }
}

// ══════════════════════════════════════════════════════════
// Promotion Dialog
// ══════════════════════════════════════════════════════════

function showPromotionDialog(isWhite) {
    const overlay = document.getElementById('promotion-overlay');
    const container = document.getElementById('promotion-pieces');
    container.innerHTML = '';

    const promoOptions = [
        { name: 'queen',  symbol: isWhite ? '♕' : '♛' },
        { name: 'rook',   symbol: isWhite ? '♖' : '♜' },
        { name: 'bishop', symbol: isWhite ? '♗' : '♝' },
        { name: 'knight', symbol: isWhite ? '♘' : '♞' },
    ];

    for (const opt of promoOptions) {
        const btn = document.createElement('div');
        btn.className = 'promotion-choice';
        btn.textContent = opt.symbol;
        btn.addEventListener('click', () => {
            overlay.classList.remove('active');
            const pending = STATE.promotionPending;
            STATE.promotionPending = null;
            makeMove(pending.from, pending.to, opt.name);
        });
        container.appendChild(btn);
    }

    overlay.classList.add('active');
}

// ══════════════════════════════════════════════════════════
// Eval Bar
// ══════════════════════════════════════════════════════════

function updateEvalBar(evalCp, evalFormatted) {
    // Sigmoid mapping
    const pct = 1.0 / (1.0 + Math.exp(-evalCp / 400.0));
    const whitePct = Math.max(2, Math.min(98, pct * 100));

    const bar = document.getElementById('eval-bar-white');
    bar.style.height = whitePct + '%';

    const label = document.getElementById('eval-bar-label');
    label.textContent = evalFormatted;

    // Position label at division line
    const topPct = 100 - whitePct;
    label.style.top = Math.max(2, Math.min(92, topPct)) + '%';

    // Color based on position
    if (pct > 0.5) {
        label.style.color = '#1e1e1e';
        label.style.background = 'rgba(220,220,220,0.7)';
    } else {
        label.style.color = '#ddd';
        label.style.background = 'rgba(50,50,68,0.7)';
    }
}

// ══════════════════════════════════════════════════════════
// Coach Panel
// ══════════════════════════════════════════════════════════

function updateCoachPanel(state) {
    const evalEl = document.getElementById('coach-eval');
    evalEl.textContent = state.eval_formatted;

    const content = document.getElementById('coach-content');
    let html = '';

    // Opening
    if (state.opening_info) {
        const [name, eco] = state.opening_info;
        html += `<div class="coach-opening">${name} (${eco})</div>`;
    }

    // Classification
    if (state.last_analysis) {
        const a = state.last_analysis;
        const color = `rgb(${a.color.join(',')})`;
        html += `<div class="coach-classification" style="color:${color}">`;
        html += `${a.symbol}  ${a.label}`;
        if (a.cp_loss > 0) {
            html += `<span class="coach-cp-loss">(-${a.cp_loss} cp)</span>`;
        }
        html += `</div>`;
    }

    // AI explanation (coaching mode)
    if (state.ai_explanation && STATE.mode === 'coaching') {
        html += `<div class="coach-explanation">${escapeHtml(state.ai_explanation)}</div>`;
    }

    // Tip
    if (state.coach_tip) {
        html += `<div class="coach-tip">${escapeHtml(state.coach_tip)}</div>`;
    }

    if (!html) {
        html = '<div class="coach-tip">Make your first move to begin!</div>';
    }

    content.innerHTML = html;
}

function updateCoachThinking(isThinking) {
    if (STATE.mode === 'pvp') return;
    if (isThinking) {
        const content = document.getElementById('coach-content');
        content.innerHTML = '<div class="ai-thinking">AI thinking<span class="dots"></span></div>';
    }
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ══════════════════════════════════════════════════════════
// Move Log
// ══════════════════════════════════════════════════════════

function updateMoveLog(moves) {
    const list = document.getElementById('move-log-list');
    list.innerHTML = '';

    const totalPairs = Math.ceil(moves.length / 2);

    for (let i = 0; i < totalPairs; i++) {
        const row = document.createElement('div');
        row.className = 'move-row';

        const num = document.createElement('span');
        num.className = 'move-num';
        num.textContent = (i + 1) + '.';
        row.appendChild(num);

        const whiteSan = moves[i * 2] || '';
        const blackSan = moves[i * 2 + 1] || '';

        const whiteEl = document.createElement('span');
        whiteEl.className = 'move-white' + (i * 2 === moves.length - 1 ? ' latest' : '');
        whiteEl.textContent = whiteSan;
        row.appendChild(whiteEl);

        const blackEl = document.createElement('span');
        blackEl.className = 'move-black' + (i * 2 + 1 === moves.length - 1 ? ' latest' : '');
        blackEl.textContent = blackSan;
        row.appendChild(blackEl);

        list.appendChild(row);
    }

    // Auto-scroll
    list.scrollTop = list.scrollHeight;
}

// ══════════════════════════════════════════════════════════
// Clocks
// ══════════════════════════════════════════════════════════

function startClockInterval() {
    if (STATE.clockInterval) clearInterval(STATE.clockInterval);
    STATE.clockInterval = setInterval(tickClock, 100);
}

function tickClock() {
    if (!STATE.clockRunning || STATE.unlimited) return;
    if (STATE.gameState && STATE.gameState.state !== 'playing') return;

    const dt = 0.1;
    if (STATE.clockActive === 'white') {
        STATE.clockWhite = Math.max(0, STATE.clockWhite - dt);
    } else {
        STATE.clockBlack = Math.max(0, STATE.clockBlack - dt);
    }

    updateClockElements();

    // Check flag
    if (STATE.clockWhite <= 0 || STATE.clockBlack <= 0) {
        STATE.clockRunning = false;
        // Server will handle the actual game end on next state fetch
        refreshState();
    }
}

function updateClockDisplay(state) {
    if (!state) return;

    // Active states
    const whiteClockEl = document.getElementById('clock-white');
    const blackClockEl = document.getElementById('clock-black');
    whiteClockEl.classList.toggle('active', state.clock_active === 'white' && state.state === 'playing');
    blackClockEl.classList.toggle('active', state.clock_active === 'black' && state.state === 'playing');

    updateClockElements();
}

function updateClockElements() {
    const whiteTimeEl = document.getElementById('clock-white-time');
    const blackTimeEl = document.getElementById('clock-black-time');

    if (STATE.unlimited) {
        whiteTimeEl.textContent = '∞';
        blackTimeEl.textContent = '∞';
        whiteTimeEl.classList.remove('low-time');
        blackTimeEl.classList.remove('low-time');
        return;
    }

    whiteTimeEl.textContent = formatTime(STATE.clockWhite);
    blackTimeEl.textContent = formatTime(STATE.clockBlack);

    whiteTimeEl.classList.toggle('low-time', STATE.clockWhite <= 30);
    blackTimeEl.classList.toggle('low-time', STATE.clockBlack <= 30);
}

function formatTime(secs) {
    if (secs === null || secs === undefined) return '∞';
    const t = Math.max(0, secs);
    const mins = Math.floor(t / 60);
    const s = Math.floor(t % 60);
    if (t < 10) {
        const tenths = Math.floor((t % 1) * 10);
        return `${mins}:${String(s).padStart(2, '0')}.${tenths}`;
    }
    return `${mins}:${String(s).padStart(2, '0')}`;
}

// ══════════════════════════════════════════════════════════
// Game Over
// ══════════════════════════════════════════════════════════

function showGameOver(result, reason) {
    document.getElementById('go-result').textContent = result;
    document.getElementById('go-reason').textContent = reason;
    document.getElementById('game-over-overlay').classList.add('active');
}

// ══════════════════════════════════════════════════════════
// Refresh State (for clock-flag detection)
// ══════════════════════════════════════════════════════════

async function refreshState() {
    try {
        const res = await fetch('/api/state');
        const data = await res.json();
        if (data.fen) renderState(data);
    } catch (e) {
        console.error('State refresh failed:', e);
    }
}

// ══════════════════════════════════════════════════════════
// Game Buttons
// ══════════════════════════════════════════════════════════

function initGameButtons() {
    document.getElementById('resign-btn').addEventListener('click', async () => {
        if (!STATE.gameState || STATE.gameState.state !== 'playing') return;
        if (!confirm('Are you sure you want to resign?')) return;

        try {
            const res = await fetch('/api/resign', { method: 'POST' });
            const data = await res.json();
            renderState(data);
        } catch (e) {
            console.error('Resign failed:', e);
        }
    });

    document.getElementById('new-game-btn').addEventListener('click', () => {
        document.getElementById('game-over-overlay').classList.remove('active');
        startGame();
    });

    document.getElementById('menu-btn').addEventListener('click', () => {
        if (STATE.clockInterval) clearInterval(STATE.clockInterval);
        document.getElementById('game-over-overlay').classList.remove('active');
        showScreen('menu-screen');
    });

    // Game over dialog buttons
    document.getElementById('go-new-game').addEventListener('click', () => {
        document.getElementById('game-over-overlay').classList.remove('active');
        startGame();
    });

    document.getElementById('go-menu').addEventListener('click', () => {
        if (STATE.clockInterval) clearInterval(STATE.clockInterval);
        document.getElementById('game-over-overlay').classList.remove('active');
        showScreen('menu-screen');
    });
}

// ══════════════════════════════════════════════════════════
// Stats Screen
// ══════════════════════════════════════════════════════════

async function loadStats() {
    try {
        const res = await fetch('/api/profile');
        const data = await res.json();

        const grid = document.getElementById('stats-grid');
        grid.innerHTML = `
            <div class="stat-card">
                <div class="stat-label">Games Played</div>
                <div class="stat-value">${data.games_played}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Record</div>
                <div class="stat-value">${data.wins}W / ${data.losses}L / ${data.draws}D</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Win Rate</div>
                <div class="stat-value accent">${data.win_rate.toFixed(1)}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Accuracy</div>
                <div class="stat-value success">${data.accuracy.toFixed(1)}%</div>
            </div>
        `;

        const quality = document.getElementById('stats-quality');
        quality.innerHTML = `
            <span class="quality-item quality-great">Great: ${data.great_moves}</span>
            <span class="quality-item quality-mistake">Mistakes: ${data.mistakes}</span>
            <span class="quality-item quality-blunder">Blunders: ${data.blunders}</span>
        `;

        const openings = document.getElementById('stats-openings');
        const favs = data.favorite_openings || {};
        const sorted = Object.entries(favs).sort((a, b) => b[1] - a[1]).slice(0, 5);

        if (sorted.length) {
            let html = '<div class="stats-openings-title">Top Openings</div>';
            sorted.forEach(([name, count], i) => {
                html += `<div class="opening-item">${i + 1}. ${name} (${count} games)</div>`;
            });
            openings.innerHTML = html;
        } else {
            openings.innerHTML = '';
        }
    } catch (e) {
        console.error('Failed to load stats:', e);
    }
}

// ══════════════════════════════════════════════════════════
// Initialize
// ══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    initMenu();
    initGameButtons();
});
