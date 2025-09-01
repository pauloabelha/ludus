export function drawEmptyBoard(container) {
  container.innerHTML = '';
  container.classList.add("grid");
  for (let i = 0; i < 9; i++) {
    const d = document.createElement('div');
    d.className = 'cell';
    d.dataset.idx = i;
    container.appendChild(d);
  }
}

export function applyMove(container, move, player) {
  const cell = container.querySelector(`.cell[data-idx="${move}"]`);
  if (cell && !cell.classList.contains("played")) {
    cell.textContent = player; // "X" ou "O"
    cell.classList.add('played', player === 'X' ? 'played-x' : 'played-o');
  }
}

/**
 * Destaca a linha vencedora com a cor do vencedor
 * @param {HTMLElement} container - tabuleiro
 * @param {number[]} line - índices das células vencedoras
 * @param {"X"|"O"} winner - vencedor da partida
 */
export function highlightWinningLine(container, line, winner) {
  line.forEach(idx => {
    const cell = container.querySelector(`.cell[data-idx="${idx}"]`);
    if (cell) {
      cell.classList.add("win", winner === "X" ? "win-x" : "win-o");
    }
  });
}
