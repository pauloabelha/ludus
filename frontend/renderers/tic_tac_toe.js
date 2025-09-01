export function drawEmptyBoard(container) {
  container.innerHTML = '';
  container.className = "grid";
  for (let i = 0; i < 9; i++) {
    const d = document.createElement('div');
    d.className = 'cell';
    d.dataset.idx = i;
    container.appendChild(d);
  }
}

export function applyMove(container, move, player) {
  const cell = container.querySelector(`.cell[data-idx="${move}"]`);
  if (cell) {
    if (player === 'X') {
      cell.textContent = '❌';
      cell.classList.add('played', 'played-x');
    } else {
      cell.textContent = '⭕';
      cell.classList.add('played', 'played-o');
    }
  }
}

export function highlightWinningLine(line) {
  line.forEach(idx => {
    const cell = document.querySelector(`.cell[data-idx="${idx}"]`);
    if (cell) cell.classList.add("win");
  });
}
