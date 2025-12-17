const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 게임 설정
const GAME_WIDTH = 600;
const GAME_HEIGHT = 800;
canvas.width = GAME_WIDTH;
canvas.height = GAME_HEIGHT;

// DOM 요소
const timeDisplay = document.getElementById('time-display');
const scoreBoard = document.getElementById('score-board');
const startScreen = document.getElementById('start-screen');
const difficultyScreen = document.getElementById('difficulty-screen');
const gameOverScreen = document.getElementById('game-over-screen');
const finalScoreDisplay = document.getElementById('final-score');

const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');
const diffBtns = document.querySelectorAll('.diff-btn');

// 게임 상태
let gameState = 'menu'; // 'menu', 'difficulty_select', 'playing', 'gameover'
let score = 0;
let startTime = 0;
let difficultyLevel = 1;

// 난이도 설정값
const DIFFICULTY_SETTINGS = {
    easy: { baseSpeed: 3, interval: 30, speedMult: 0.5, name: 'Easy' },
    normal: { baseSpeed: 5, interval: 20, speedMult: 1.0, name: 'Normal' },
    hard: { baseSpeed: 7, interval: 15, speedMult: 1.5, name: 'Hard' },
    hell: { baseSpeed: 10, interval: 5, speedMult: 2.0, name: 'HELL' }
};
let currentDifficulty = DIFFICULTY_SETTINGS.normal;

// 입력 상태
const keys = { ArrowLeft: false, ArrowRight: false };

// ... Player 클래스와 Poop 클래스는 동일하지만, 생성자에서 난이도 값을 참조하도록 일부 수정 필요 ...

class Player {
    constructor() {
        this.width = 30;
        this.height = 50;
        this.x = GAME_WIDTH / 2 - this.width / 2;
        this.y = GAME_HEIGHT - this.height - 10;
        this.vx = 0;
        this.speed = 0.5;
        this.friction = 0.85;
        this.maxSpeed = 8;
        this.color = 'black';
        this.state = 'normal';
    }

    update() {
        if (this.state === 'dead') return;
        if (keys.ArrowLeft) this.vx -= this.speed;
        if (keys.ArrowRight) this.vx += this.speed;
        if (this.vx > this.maxSpeed) this.vx = this.maxSpeed;
        if (this.vx < -this.maxSpeed) this.vx = -this.maxSpeed;
        this.vx *= this.friction;
        this.x += this.vx;
        if (this.x < 0) { this.x = 0; this.vx = 0; }
        if (this.x + this.width > GAME_WIDTH) { this.x = GAME_WIDTH - this.width; this.vx = 0; }
    }

    draw() {
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.lineCap = 'round';
        const cx = this.x + this.width / 2;
        const cy = this.y + this.height / 2;

        if (this.state === 'dead') {
            ctx.beginPath();
            ctx.arc(cx - 15, cy + 15, 8, 0, Math.PI * 2);
            ctx.moveTo(cx - 8, cy + 15); ctx.lineTo(cx + 10, cy + 15);
            ctx.stroke();
            return;
        }

        ctx.beginPath();
        ctx.arc(cx, this.y + 8, 8, 0, Math.PI * 2); // 머리
        ctx.moveTo(cx, this.y + 16); ctx.lineTo(cx, this.y + 35); // 몸통

        const armOffset = this.vx * 1.5;
        ctx.moveTo(cx, this.y + 20); ctx.lineTo(cx - 10 - armOffset, this.y + 30);
        ctx.moveTo(cx, this.y + 20); ctx.lineTo(cx + 10 - armOffset, this.y + 30);

        const legOffset = Math.sin(Date.now() / 50) * Math.abs(this.vx) * 1.5;
        ctx.moveTo(cx, this.y + 35); ctx.lineTo(cx - 8 + legOffset, this.y + 50);
        ctx.moveTo(cx, this.y + 35); ctx.lineTo(cx + 8 - legOffset, this.y + 50);
        ctx.stroke();
    }
}

class Poop {
    constructor() {
        this.size = Math.random() < 0.1 ? 30 : (Math.random() < 0.3 ? 24 : 15);
        this.x = Math.random() * (GAME_WIDTH - this.size);
        this.y = -this.size;

        // 난이도별 속도 적용
        const base = currentDifficulty.baseSpeed;
        // 크기에 따른 속도 차이 + 난이도 레벨(시간 경과)에 따른 가속
        let speed = (Math.random() * (base / 2) + base) * (30 / this.size) * 0.6;
        speed += (difficultyLevel * currentDifficulty.speedMult);

        this.speed = speed;
        this.color = '#8B4513';
    }

    update() {
        this.y += this.speed;
    }

    draw() {
        ctx.fillStyle = this.color;
        const radius = this.size / 2;

        ctx.beginPath(); ctx.ellipse(this.x, this.y + radius * 0.5, radius, radius * 0.6, 0, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.ellipse(this.x, this.y, radius * 0.8, radius * 0.5, 0, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.ellipse(this.x, this.y - radius * 0.4, radius * 0.5, radius * 0.4, 0, 0, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.moveTo(this.x - radius * 0.4, this.y - radius * 0.4); ctx.quadraticCurveTo(this.x, this.y - radius * 1.5, this.x + radius * 0.4, this.y - radius * 0.4); ctx.fill();

        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath(); ctx.ellipse(this.x - radius * 0.3, this.y, radius * 0.2, radius * 0.1, -0.5, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = this.color;
    }
}

let player = new Player();
let poops = [];
let poopTimer = 0;
let poopInterval = 20;

// 화면 전환 함수
function showScreen(screenName) {
    startScreen.classList.add('hidden');
    difficultyScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    scoreBoard.classList.add('hidden');

    if (screenName === 'start') startScreen.classList.remove('hidden');
    else if (screenName === 'difficulty') difficultyScreen.classList.remove('hidden');
    else if (screenName === 'gameover') gameOverScreen.classList.remove('hidden');
    else if (screenName === 'playing') scoreBoard.classList.remove('hidden');
}

function startGame(difficulty) {
    currentDifficulty = DIFFICULTY_SETTINGS[difficulty];

    player = new Player();
    poops = [];
    score = 0;
    difficultyLevel = 1;
    poopInterval = currentDifficulty.interval;

    gameState = 'playing';
    startTime = Date.now();

    showScreen('playing');
    animate();
}

// 이벤트 리스너
startBtn.addEventListener('click', () => {
    gameState = 'difficulty_select';
    showScreen('difficulty');
});

diffBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const diff = btn.dataset.diff;
        startGame(diff);
    });
});

restartBtn.addEventListener('click', () => {
    // 처음으로 돌아가기 (다시하기 아님)
    gameState = 'menu';
    showScreen('start');
});

function handleInput() {
    window.addEventListener('keydown', e => { if (keys.hasOwnProperty(e.code)) keys[e.code] = true; });
    window.addEventListener('keyup', e => { if (keys.hasOwnProperty(e.code)) keys[e.code] = false; });
}

function checkCollision(rect1, circle1) {
    const hitBoxX = rect1.x + 5;
    const hitBoxY = rect1.y + 5;
    const hitBoxW = rect1.width - 10;
    const hitBoxH = rect1.height - 5;
    const circleX = circle1.x;
    const circleY = circle1.y;
    const radius = circle1.size / 2;
    const closestX = Math.max(hitBoxX, Math.min(circleX, hitBoxX + hitBoxW));
    const closestY = Math.max(hitBoxY, Math.min(circleY, hitBoxY + hitBoxH));
    const distanceX = circleX - closestX;
    const distanceY = circleY - closestY;
    return (distanceX * distanceX) + (distanceY * distanceY) < (radius * radius);
}

function gameOver() {
    gameState = 'gameover';
    player.state = 'dead';
    finalScoreDisplay.textContent = score.toFixed(2);
    showScreen('gameover');
}

function animate() {
    if (gameState === 'menu' || gameState === 'difficulty_select') return; // 메뉴에서는 루프 정지

    if (gameState === 'gameover') {
        player.draw();
        return;
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const currentTime = Date.now();
    score = (currentTime - startTime) / 1000;
    timeDisplay.textContent = score.toFixed(2);

    // 난이도 자동 증가 (시간 경과에 따라)
    difficultyLevel = 1 + Math.floor(score / 5);

    // 생성 간격 조절
    let currentInterval = currentDifficulty.interval - (difficultyLevel * (currentDifficulty.name === 'HELL' ? 1 : 2));
    if (currentInterval < 3) currentInterval = 3;

    poopTimer++;
    if (poopTimer > currentInterval) {
        poops.push(new Poop());
        poopTimer = 0;
    }

    player.update();
    player.draw();

    for (let i = 0; i < poops.length; i++) {
        poops[i].update();
        poops[i].draw();

        if (poops[i].y > GAME_HEIGHT + 50) {
            poops.splice(i, 1);
            i--;
            continue;
        }

        if (checkCollision(player, poops[i])) {
            gameOver();
        }
    }

    requestAnimationFrame(animate);
}

// 초기화
handleInput();
showScreen('start'); // 시작 시 메뉴 화면 표시
