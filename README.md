# Brute-force--PIN-Search

Educational project that simulates 4-digit PIN guessing strategies using real-world PIN frequency patterns and brute-force search. Built for cybersecurity learning, statistics, and PIN-security awareness. Everything runs locally — **no real devices, accounts, or services are targeted.**

**[Live demo →](https://naren0316.github.io/Brute-force--PIN-Search/)**
*(link goes live once GitHub Pages is enabled — see Deploying below)*

---

## What's in this repo

| File | What it is |
|---|---|
| `PIN-Probability-Sim.py` | The original Python simulation: builds priority groups from real PIN-frequency data, then runs a brute-force search in that order. |
| `index.html` / `style.css` / `script.js` | A browser front end for the same idea — the JS port mirrors `crack_pin()` group-for-group, attempt-for-attempt. |
| `.github/workflows/deploy.yml` | Auto-deploys the static front end to GitHub Pages on every push to `main`. |

## The front end

A dark "vault dossier"-themed site that turns the simulation into something you can watch happen:

- **Live simulator** — set any 4-digit target PIN and watch the real search order run in your browser: verified top-20 → extended common → repeated digits → sequential patterns → likely years → repeated pairs → full brute force.
- **Weak-PIN reference grid** — the 20 most common real-world PINs, and the 21 least common, side by side.
- **Stats view** — a log-scaled chart of how the 10,000-value space splits across passes, with a live breakdown of exactly how many attempts each pass took on your last run.
- Fully responsive, keyboard-navigable, and respects `prefers-reduced-motion`.

No build step, no dependencies — it's plain HTML/CSS/JS.

### Running it locally

```bash
git clone https://github.com/Naren0316/Brute-force--PIN-Search.git
cd Brute-force--PIN-Search
python3 -m http.server 8000
# open http://localhost:8000
```

Or just open `index.html` directly in a browser.

### Running the original Python simulation

```bash
python3 PIN-Probability-Sim.py
```

## Deploying (GitHub Pages)

This repo includes a workflow that deploys automatically — you only need to flip one setting:

1. Go to **Settings → Pages** in this repository.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Push to `main` (or re-run the *Deploy to GitHub Pages* workflow from the **Actions** tab).
4. Your site will be live at `https://<your-username>.github.io/Brute-force--PIN-Search/` within a minute or two.

No further configuration needed — `.github/workflows/deploy.yml` handles the build and publish.

## Future plans

This project started as a local simulation for educational purposes and is now growing into a small interactive teaching tool. Planned next steps:

- Simulating additional authentication mechanisms (lockout policies, rate limiting)
- Testing PIN strength against different attack strategies beyond the current pass order
- Expanding the stats view with historical run comparisons
- Continued development for cybersecurity education and defensive security research

## License

No license file yet — all rights reserved by default until one is added. If you intend for this to be reused or contributed to, consider adding an [MIT](https://choosealicense.com/licenses/mit/) or similar license.
