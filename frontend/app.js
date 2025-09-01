// ===============================
//  Arena Frontend Orchestrator (Universal)
// ===============================
//
// Handles:
//  - Dynamic loading of games & bots
//  - Per-game renderers & CSS
//  - Move animation
//  - Winner highlight + flash
//  - Colorblind-friendly Tic Tac Toe
//  - Horizontal sticks for Eleven Sticks
//  - Leaderboard refresh
//  - i18n support
// ===============================

import { renderers } from './renderers/index.js';

// ---------- DOM references ----------
const gameSelect   = document.getElementById('gameSelect');
const bot0Select   = document.getElementById('bot0Select');
const bot1Select   = document.getElementById('bot1Select');
const playBtn      = document.getElementById('playBtn');
const boardEl      = document.getElementById('board');
const statusEl     = document.getElementById('status');
const lbTableBody  = document.querySelector('#leaderboardTable tbody');
const langSelect   = document.getElementById('langSelect'); 
const backupBtn    = document.getElementById("backupBtn");

// ---------- State ----------
let botsCache = {};
let currentGame = null;

// ---------- Animation ----------
const MOVE_DELAY = 1000; // ms
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

// =======================================================
//  i18n
// =======================================================
async function initI18n(lang = "en") {
  const res = await fetch(`/static/i18n/${lang}.json`);
  const resources = await res.json();

  await i18next.init({
    lng: lang,
    resources: { [lang]: { translation: resources } },
    interpolation: { escapeValue: false }
  });

  refreshUITexts();
}

function t(key, opts = {}) {
  return i18next.t(key, opts);
}

function refreshUITexts() {
  document.querySelector("header h1").textContent = t("title");
  document.querySelector("header .subtitle").textContent = t("subtitle");
  playBtn.textContent = t("play");
  document.querySelector(".leaderboard h2").textContent = t("leaderboard");

  const ths = document.querySelectorAll("#leaderboardTable thead th");
  if (ths.length >= 5) {
    ths[0].textContent = t("bot");
    ths[1].textContent = t("games");
    ths[2].textContent = t("wins");
    ths[3].textContent = t("draws");
    ths[4].textContent = t("losses");
  }
}

// =======================================================
//  Helpers
// =======================================================
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(await res.text());
  return await res.json();
}

// Load per-game CSS
function setGameStyle(gameCode) {
  const link = document.getElementById("game-style");
  if (link) link.href = `/static/renderers/${gameCode}.css`;
}

// Trigger winner flash animation
function triggerWinnerFlash() {
  statusEl.classList.remove('winnerFlash');
  void statusEl.offsetWidth; // force reflow
  statusEl.classList.add('winnerFlash');
}

// =======================================================
//  Rendering helpers
// =======================================================
function drawEmptyBoard() {
  boardEl.innerHTML = '';
  boardEl.className = ''; // reset all previous classes

  const r = renderers[currentGame];
  if (r && r.drawEmptyBoard) r.drawEmptyBoard(boardEl);
  else boardEl.textContent = `(no renderer for ${currentGame})`;
}

function applyMove(move, player) {
  const r = renderers[currentGame];
  if (r && r.applyMove) r.applyMove(boardEl, move, player);
}

function highlightWinningLine(line) {
  const r = renderers[currentGame];
  if (r && r.highlightWinningLine) r.highlightWinningLine(boardEl, line);
}



// =======================================================
//  Games & Bots
// =======================================================
async function loadGamesAndBots() {
  const games = await fetchJSON('/games');
  gameSelect.innerHTML = '';
  for (const g of games) {
    const opt = document.createElement('option');
    opt.value = g.code;
    opt.textContent = `${g.name} — ${g.description}`;
    gameSelect.appendChild(opt);
  }

  // ✅ força Tic Tac Toe como padrão se existir
  if (games.some(g => g.code === "tic_tac_toe")) {
    gameSelect.value = "tic_tac_toe";
    currentGame = "tic_tac_toe";
  } else {
    currentGame = gameSelect.value;
  }

  setGameStyle(currentGame);
  await loadBots();
}

async function loadBots() {
  const game = gameSelect.value;
  const bots = await fetchJSON(`/bots?game=${encodeURIComponent(game)}`);
  botsCache = {};
  for (const b of bots) botsCache[b.id] = b;

  for (const sel of [bot0Select, bot1Select]) {
    sel.innerHTML = '';
    for (const b of bots) {
      const opt = document.createElement('option');
      opt.value = b.id;
      opt.textContent = b.name;
      sel.appendChild(opt);
    }
  }
}

// =======================================================
//  Leaderboard
// =======================================================
async function refreshLeaderboard() {
  const game = gameSelect.value;
  const lb = await fetchJSON(`/leaderboard?game=${encodeURIComponent(game)}`);
  const rows = Object.entries(lb).map(([bot, stats]) => ({ bot, ...stats }));
  rows.sort((a,b) => b.wins - a.wins || a.losses - b.losses);

  lbTableBody.innerHTML = '';
  for (const r of rows) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${r.bot}</td>
      <td>${r.games}</td>
      <td>${r.wins}</td>
      <td>${r.draws}</td>
      <td>${r.losses}</td>
    `;
    lbTableBody.appendChild(tr);
  }
}

// =======================================================
//  Match Flow
// =======================================================
async function playMatch() {
  currentGame = gameSelect.value;
  setGameStyle(currentGame);

  statusEl.textContent = t("playing");
  statusEl.classList.remove('winnerFlash');
  drawEmptyBoard();

  const bot0 = bot0Select.value;
  const bot1 = bot1Select.value;

  const result = await fetchJSON(
    `/play?game=${encodeURIComponent(currentGame)}&bot0=${encodeURIComponent(bot0)}&bot1=${encodeURIComponent(bot1)}`
  );

  for (const step of result.moves) {
    applyMove(step.move, step.player);
    await sleep(MOVE_DELAY);
  }

  if (result.winner === 'draw') {
    statusEl.textContent = t("draw");
  } else {
    if (result.winning_line?.length) highlightWinningLine(result.winning_line);

    const winnerId = result.winner === "X" ? bot0 : bot1;
    const winnerMeta = botsCache[winnerId];
    if (winnerMeta) {
      statusEl.innerHTML = `<div><strong>${t("winner", {
        name: winnerMeta.name,
        piece: result.winner,
        desc: winnerMeta.description
      })}</strong></div>`;
    }

    // Winner flash animation
    triggerWinnerFlash();
  }

  await refreshLeaderboard();
}

// =======================================================
//  Event Handlers
// =======================================================
gameSelect.addEventListener('change', async () => {
  currentGame = gameSelect.value;
  setGameStyle(currentGame);
  await loadBots();
  await refreshLeaderboard();
  drawEmptyBoard();
});

playBtn.addEventListener('click', playMatch);

langSelect.addEventListener('change', async (e) => await initI18n(e.target.value));

backupBtn.addEventListener("click", () => window.location.href = "/backup");

// =======================================================
//  Init
// =======================================================
(async () => {
  await loadGamesAndBots();
  setGameStyle(currentGame);
  await refreshLeaderboard();
  await initI18n("en");
  drawEmptyBoard();
})();
