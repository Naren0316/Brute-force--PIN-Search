/* ============================================
   DATA — mirrors PIN-Probability-Sim.py
   (real-world verified top-20 leaked PIN frequency)
   ============================================ */
const VERIFIED_TOP_20 = [
  "1234", "1111", "0000", "1212", "7777",
  "1004", "2000", "4444", "2222", "6969",
  "9999", "3333", "5555", "6666", "1122",
  "1313", "8888", "4321", "2001", "1010",
];

/* ============================================
   DRAW DIAL TICKS
   ============================================ */
function drawDialTicks() {
  const group = document.querySelector(".dial-ticks");
  if (!group) return;
  const cx = 170, cy = 170, rOuter = 150, rInner = 138;
  const ticks = 40;
  for (let i = 0; i < ticks; i++) {
    const angle = (i / ticks) * Math.PI * 2;
    const x1 = cx + rInner * Math.cos(angle);
    const y1 = cy + rInner * Math.sin(angle);
    const x2 = cx + rOuter * Math.cos(angle);
    const y2 = cy + rOuter * Math.sin(angle);
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x1.toFixed(1));
    line.setAttribute("y1", y1.toFixed(1));
    line.setAttribute("x2", x2.toFixed(1));
    line.setAttribute("y2", y2.toFixed(1));
    group.appendChild(line);
  }
}

/* ============================================
   HERO DIAL — idle cycling animation
   Purely decorative today; Day 2 wires this to
   the real ported search logic.
   ============================================ */
function startDialAnimation() {
  const digitsEl = document.getElementById("dial-digits");
  const countEl = document.getElementById("dial-count");
  if (!digitsEl || !countEl) return;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduceMotion) {
    digitsEl.textContent = "1948";
    countEl.textContent = "004821";
    return;
  }

  let attempt = 0;
  const sequence = [...VERIFIED_TOP_20, "1948"]; // 1948 = SECRET_PIN in the sim, landed on last
  let i = 0;

  setInterval(() => {
    digitsEl.textContent = sequence[i % sequence.length];
    attempt += Math.floor(Math.random() * 40) + 5;
    countEl.textContent = String(attempt).padStart(6, "0");
    i++;
  }, 900);
}

/* ============================================
   WEAK PIN GRID
   ============================================ */
function renderPinGrid() {
  const grid = document.getElementById("pin-grid");
  if (!grid) return;

  grid.innerHTML = VERIFIED_TOP_20.map((pin, idx) => {
    const rank = idx + 1;
    const fillPct = Math.max(100 - idx * 4.5, 8); // purely visual weighting, rank-based
    return `
      <div class="pin-chip">
        <span class="digits">${pin}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${fillPct}%"></div></div>
        <span class="rank">rank #${rank}</span>
      </div>
    `;
  }).join("");
}

/* ============================================
   DEMO BUTTON — placeholder for Day 2
   ============================================ */
function wireDemoButton() {
  const btn = document.getElementById("try-demo");
  if (!btn) return;
  btn.addEventListener("click", () => {
    btn.textContent = "Live simulator lands Day 2 →";
    btn.disabled = true;
    setTimeout(() => {
      document.querySelector("#how").scrollIntoView({ behavior: "smooth" });
    }, 500);
  });
}

/* ============================================
   INIT
   ============================================ */
document.addEventListener("DOMContentLoaded", () => {
  drawDialTicks();
  startDialAnimation();
  renderPinGrid();
  wireDemoButton();
});
