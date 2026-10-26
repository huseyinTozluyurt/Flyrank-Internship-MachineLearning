# Portfolio site

React + Vite + React Router (`HashRouter`) site with one page per notebook/module,
plus the capstone paper. It builds into `../docs/`, which GitHub Pages serves from
the `main` branch, so no Pages setting needs to change.

```bash
cd site
npm install
npm run dev        # local dev server
npm run build      # writes docs/index.html, docs/assets/ and docs/figures/
npm run preview    # serve the built docs/ folder
```

- Page content lives in `src/content/` (`analysis.js`, `ml.js`, `track.js`, `paper.html`).
- The build first runs `scripts/extract_figures.py` (Python 3, standard library only), which
  extracts the charts from the notebooks' saved outputs into `public/figures/<page>/`
  (git-ignored; the built copies live in `docs/figures/`). Charts that identify individual clients are deliberately
  not extracted.
- The build only replaces `docs/index.html`, `docs/assets/` and `docs/figures/`; the
  markdown docs, the PDF and `docs/img/` are left alone.
- `index.html` keeps the FlyRank data credit (https://flyrank.ai) in its static HTML
  because the CI smoke test checks the deployed page for it.
