export function drawEmptyBoard(container) {
  container.innerHTML = '';
  container.className = "sticks";
  for (let i = 0; i < 11; i++) {
    const d = document.createElement('div');
    d.className = 'stick';
    d.dataset.idx = i;
    d.textContent = '━';   // horizontal bar stick
    container.appendChild(d);
  }
}

export function applyMove(container, move, player) {
  const sticks = Array.from(container.querySelectorAll('.stick'));
  let toRemove = move;

  for (let i = 0; i < sticks.length && toRemove > 0; i++) {
    if (!sticks[i].classList.contains("removed")) {
      if (player === "X") {
        sticks[i].textContent = "❌";
        sticks[i].classList.add("removed-x");
      } else {
        sticks[i].textContent = "⭕";
        sticks[i].classList.add("removed-o");
      }
      sticks[i].classList.add("removed");
      toRemove--;
    }
  }
}
