/* ============================================
   DATA + SEARCH LOGIC
   Ported directly from PIN-Probability-Sim.py
   so the browser demo matches the real script
   pass-for-pass.
   ============================================ */
const VERIFIED_TOP_20 = [
  "1234", "1111", "0000", "1212", "7777",
  "1004", "2000", "4444", "2222", "6969",
  "9999", "3333", "5555", "6666", "1122",
  "1313", "8888", "4321", "2001", "1010",
];

const EXTENDED_COMMON = [
  "2580", "0007", "0070", "1984", "1999",
  "1919", "1972", "1122", "2020", "2021",
  "2323", "6789", "2468", "1357", "1230",
  "5201", "0101", "0808", "1231", "0704",
];

const LEAST_LIKELY = [
  "8557", "9047", "8438", "0439", "9539",
  "8196", "7063", "6093", "6827", "7394",
  "0859", "8957", "9480", "6793", "8398",
  "0738", "7637", "6835", "9629", "8093",
  "8068",
];

function buildPriorityGroups() {
  const groups = [];

  groups.push(["VERIFIED top 20 (real study data)", VERIFIED_TOP_20]);
  groups.push(["EXTENDED known-common (documented, unranked)", EXTENDED_COMMON]);
  groups.push(["Repeated digits", Array.from({ length: 10 }, (_, d) => String(d).repeat(4))]);

  const seqs = [];
  for (let start = 0; start < 7; start++) {
    let s = "";
    for (let i = 0; i < 4; i++) s += (start + i) % 10;
    seqs.push(s);
  }
  for (let start = 9; start > 2; start--) {
    let s = "";
    for (let i = 0; i < 4; i++) s += (((start - i) % 10) + 10) % 10;
    seqs.push(s);
  }
  groups.push(["Sequential patterns", seqs]);

  const years = [];
  for (let y = 1940; y <= 2015; y++) years.push(String(y));
  groups.push(["Likely years (1940-2015)", years]);

  const pairs = [];
  for (let a = 0; a < 10; a++) {
    for (let b = 0; b < 10; b++) {
      if (a !== b) pairs.push(`${a}${a}${b}${b}`);
    }
  }
  groups.push(["Repeated-pair patterns (XYXY)", pairs]);

  return groups;
}

function buildFullSearchSpace() {
  const all = new Array(10000);
  for (let i = 0; i < 10000; i++) all[i] = String(i).padStart(4, "0");
  return all;
}

/**
 * Generator mirroring crack_pin() in PIN-Probability-Sim.py.
 * Yields one attempt at a time: { pin, group, attempt, found }
 */
function* crackPinSteps(targetPin) {
  const tried = new Set();
  const groups = buildPriorityGroups();

  for (const [groupName, pins] of groups) {
    for (const pin of pins) {
      if (tried.has(pin)) continue;
      tried.add(pin);
      const found = pin === targetPin;
      yield { pin, group: groupName, attempt: tried.size, found, groupSize: pins.length };
      if (found) return;
    }
  }

  const full = buildFullSearchSpace();
  for (const pin of full) {
    if (tried.has(pin)) continue;
    tried.add(pin);
    const found = pin === targetPin;
    yield { pin, group: "Full brute-force", attempt: tried.size, found, groupSize: full.length };
    if (found) return;
  }
}

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
   WEAK PIN GRID + LEAST-LIKELY GRID
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

function renderSafePinGrid() {
  const grid = document.getElementById("safe-pin-grid");
  if (!grid) return;

  grid.innerHTML = LEAST_LIKELY.map((pin, idx) => {
    // inverted weighting: these are least likely, so bar reflects rarity (short = rare)
    const fillPct = Math.max(30 - idx * 1.1, 6);
    return `
      <div class="pin-chip">
        <span class="digits">${pin}</span>
        <div class="bar-track"><div class="bar-fill" style="width:${fillPct}%"></div></div>
        <span class="rank">bottom #${idx + 1}</span>
      </div>
    `;
  }).join("");
}

/* ============================================
   GROUP SIZE CHART
   ============================================ */
const FULL_BRUTE_LABEL = "Full brute-force";

function chartData() {
  const groups = buildPriorityGroups();
  const tried = new Set();
  const rows = [];

  for (const [name, pins] of groups) {
    let netNew = 0;
    for (const pin of pins) {
      if (!tried.has(pin)) {
        tried.add(pin);
        netNew++;
      }
    }
    rows.push([name, netNew]);
  }

  rows.push([FULL_BRUTE_LABEL, 10000 - tried.size]);
  return rows;
}

function renderGroupChart(matchGroup) {
  const el = document.getElementById("group-chart");
  if (!el) return;

  const data = chartData();
  const maxLog = Math.log10(Math.max(...data.map(([, n]) => n)) + 1);

  el.innerHTML = data.map(([name, count]) => {
    const pct = Math.max((Math.log10(count + 1) / maxLog) * 100, 3);
    const isMatch = name === matchGroup;
    return `
      <div class="chart-row${isMatch ? " is-match" : ""}">
        <span class="chart-row-label">${name}</span>
        <div class="chart-row-track"><div class="chart-row-fill" style="width:${pct.toFixed(1)}%"></div></div>
        <span class="chart-row-value">${count.toLocaleString()}</span>
      </div>
    `;
  }).join("");
}

function renderStatsNote(groupCounts, matchGroup, matchAttempt) {
  const note = document.getElementById("stats-note");
  const title = document.getElementById("stats-note-title");
  const table = document.getElementById("stats-note-table");
  if (!note) return;

  title.textContent = `This run: ${matchAttempt} total attempts across ${Object.keys(groupCounts).length} pass${Object.keys(groupCounts).length > 1 ? "es" : ""}`;
  table.innerHTML = Object.entries(groupCounts).map(([name, count]) => `
    <div class="stats-note-cell${name === matchGroup ? " is-match" : ""}">
      <span class="label">${name}</span>
      <span class="value">${count} attempt${count === 1 ? "" : "s"}</span>
    </div>
  `).join("");

  note.hidden = false;
}

/* ============================================
   HERO DIAL
   Idles through the verified top-20 until the
   live simulator starts, then mirrors real
   attempts in real time.
   ============================================ */
let dialIdleTimer = null;

function startDialIdleAnimation() {
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
  const sequence = [...VERIFIED_TOP_20, "1948"];
  let i = 0;

  dialIdleTimer = setInterval(() => {
    digitsEl.textContent = sequence[i % sequence.length];
    attempt += Math.floor(Math.random() * 40) + 5;
    countEl.textContent = String(attempt).padStart(6, "0");
    i++;
  }, 900);
}

function updateDialReadout(pin, attempt) {
  const digitsEl = document.getElementById("dial-digits");
  const countEl = document.getElementById("dial-count");
  if (digitsEl) digitsEl.textContent = pin;
  if (countEl) countEl.textContent = String(attempt).padStart(6, "0");
}

/* ============================================
   LIVE SIMULATOR
   ============================================ */
const sim = {
  running: false,
  gen: null,
  targetPin: "1948",
  startTime: 0,
  lastGroup: null,
  lastGroupWasBruteForce: false,
  groupCounts: {},
};

function simEls() {
  return {
    input: document.getElementById("target-pin"),
    randomizeBtn: document.getElementById("randomize-pin"),
    startBtn: document.getElementById("start-sim"),
    resetBtn: document.getElementById("reset-sim"),
    currentPin: document.getElementById("sim-current-pin"),
    attemptCount: document.getElementById("sim-attempt-count"),
    elapsed: document.getElementById("sim-elapsed"),
    log: document.getElementById("sim-log"),
    result: document.getElementById("sim-result"),
    resultHeadline: document.getElementById("sim-result-headline"),
    resultDetail: document.getElementById("sim-result-detail"),
  };
}

function appendLog(html) {
  const { log } = simEls();
  if (!log) return;
  log.innerHTML += (log.innerHTML ? "\n" : "") + html;
  log.scrollTop = log.scrollHeight;
}

function validPin(value) {
  return /^[0-9]{4}$/.test(value);
}

function resetSimUI() {
  const els = simEls();
  els.currentPin.textContent = "····";
  els.attemptCount.textContent = "0";
  els.elapsed.textContent = "0.00s";
  els.log.textContent = 'Set a target PIN and press "Start search".';
  els.result.hidden = true;
  els.startBtn.disabled = false;
  els.startBtn.textContent = "Start search";
  els.resetBtn.disabled = true;
  els.input.disabled = false;
}

function handleStep(step) {
  const els = simEls();
  els.currentPin.textContent = step.pin;
  els.attemptCount.textContent = String(step.attempt);
  els.elapsed.textContent = ((performance.now() - sim.startTime) / 1000).toFixed(2) + "s";
  updateDialReadout(step.pin, step.attempt);

  sim.groupCounts[step.group] = (sim.groupCounts[step.group] || 0) + 1;

  if (step.group !== sim.lastGroup) {
    appendLog(`<span class="log-group">↳ Trying: ${step.group} (${step.groupSize} candidates)</span>`);
    sim.lastGroup = step.group;
  }

  const isBruteForce = step.group === "Full brute-force";
  const shouldLog = isBruteForce
    ? step.attempt % 500 === 0
    : (step.attempt % 10 === 0 || step.attempt <= 5);

  if (shouldLog && !step.found) {
    appendLog(`   attempt ${String(step.attempt).padStart(5, " ")} | tried ${step.pin} | ${els.elapsed.textContent}`);
  }

  sim.lastGroupWasBruteForce = isBruteForce;
}

function finishSim(found, step) {
  sim.running = false;
  clearInterval(dialIdleTimer);
  const els = simEls();
  const elapsedSec = (performance.now() - sim.startTime) / 1000;

  els.startBtn.disabled = false;
  els.startBtn.textContent = "Start search";
  els.resetBtn.disabled = false;
  els.input.disabled = true;

  if (found && step) {
    appendLog(`<span class="log-found">PIN cracked: ${step.pin} — in "${step.group}" — ${step.attempt} attempts — ${elapsedSec.toFixed(4)}s</span>`);
    els.result.hidden = false;
    els.resultHeadline.textContent = `Cracked in ${step.attempt} attempts (${elapsedSec.toFixed(2)}s)`;
    let detail = `Found via "${step.group}" — this pattern group is tried before a full brute force.`;
    const leastIdx = LEAST_LIKELY.indexOf(step.pin);
    if (leastIdx !== -1) {
      detail += ` Note: ${step.pin} is also one of the verified least-common real-world PINs (bottom ${leastIdx + 1}).`;
    }
    els.resultDetail.textContent = detail;
    renderGroupChart(step.group);
    renderStatsNote(sim.groupCounts, step.group, step.attempt);
  } else {
    appendLog("PIN not found.");
    els.result.hidden = false;
    els.resultHeadline.textContent = "PIN not found";
    els.resultDetail.textContent = "The full 0000–9999 space was exhausted without a match — this shouldn't happen for a valid 4-digit target.";
  }
}

function driveSimFrame() {
  if (!sim.running) return;
  const batchSize = sim.lastGroupWasBruteForce ? 60 : 1;

  for (let i = 0; i < batchSize; i++) {
    const { value, done } = sim.gen.next();
    if (done || !value) {
      finishSim(false);
      return;
    }
    handleStep(value);
    if (value.found) {
      finishSim(true, value);
      return;
    }
  }
  requestAnimationFrame(driveSimFrame);
}

function startSim() {
  const els = simEls();
  const target = els.input.value.trim();
  if (!validPin(target)) {
    els.input.focus();
    els.input.style.borderColor = "var(--danger)";
    setTimeout(() => (els.input.style.borderColor = ""), 900);
    return;
  }

  clearInterval(dialIdleTimer);

  sim.running = true;
  sim.targetPin = target;
  sim.gen = crackPinSteps(target);
  sim.startTime = performance.now();
  sim.lastGroup = null;
  sim.lastGroupWasBruteForce = false;
  sim.groupCounts = {};

  els.log.textContent = "";
  els.result.hidden = true;
  els.startBtn.disabled = true;
  els.startBtn.textContent = "Searching…";
  els.resetBtn.disabled = true;
  els.input.disabled = true;

  renderGroupChart();
  document.getElementById("stats-note").hidden = true;

  requestAnimationFrame(driveSimFrame);
}

function wireSimulator() {
  const els = simEls();
  if (!els.startBtn) return;

  els.startBtn.addEventListener("click", startSim);

  els.randomizeBtn.addEventListener("click", () => {
    const rand = String(Math.floor(Math.random() * 10000)).padStart(4, "0");
    els.input.value = rand;
  });

  els.resetBtn.addEventListener("click", () => {
    sim.running = false;
    resetSimUI();
    startDialIdleAnimation();
    renderGroupChart();
    document.getElementById("stats-note").hidden = true;
  });

  els.input.addEventListener("input", () => {
    els.input.value = els.input.value.replace(/[^0-9]/g, "").slice(0, 4);
  });
}

/* ============================================
   HERO CTA — scrolls to simulator and runs it
   ============================================ */
function wireHeroButton() {
  const btn = document.getElementById("try-demo");
  if (!btn) return;
  btn.addEventListener("click", () => {
    document.querySelector("#simulator").scrollIntoView({ behavior: "smooth", block: "start" });
    setTimeout(() => {
      if (!sim.running) startSim();
    }, 400);
  });
}

/* ============================================
   INIT
   ============================================ */
document.addEventListener("DOMContentLoaded", () => {
  drawDialTicks();
  startDialIdleAnimation();
  renderPinGrid();
  renderSafePinGrid();
  renderGroupChart();
  wireSimulator();
  wireHeroButton();
});
