# Alvi Ibn Amzad Anil — Portfolio

A single-page, electronics-themed portfolio in a light theme. Pure HTML, CSS and vanilla
JavaScript — no frameworks, no build step, no npm install. Just open it and it runs.

## What's inside

```
alvi-portfolio/
├── index.html                     # all page content
├── assets/
│   ├── css/style.css              # theme, layout, animations
│   ├── js/main.js                 # canvas PCB background, scope, reveals, filters
│   ├── img/favicon.svg            # tab icon
│   └── files/
│       └── Alvi-Ibn-Amzad-Anil-CV.pdf
├── serve.py                       # optional local preview server
├── .nojekyll                      # tells GitHub Pages to serve files as-is
└── README.md
```

## Features

- Animated printed-circuit-board background drawn on `<canvas>` with signal pulses
  travelling along copper traces
- Hero "edge node" board with an IC illustration and a live oscilloscope readout
- Scroll progress bar, sticky navigation with scroll-spy, mobile drawer menu
- Reveal-on-scroll animations, animated counters, impact-factor meters
- Publication filtering by authorship position
- Subtle 3D tilt on project and skill cards
- Fully responsive; respects `prefers-reduced-motion`; prints cleanly

## Before you publish — fill in your links

Open `assets/js/main.js` and edit the `PROFILES` block at the very top:

```js
var PROFILES = {
  linkedin:     'https://www.linkedin.com/in/your-handle',
  researchgate: 'https://www.researchgate.net/profile/Your-Name',
  scholar:      'https://scholar.google.com/citations?user=XXXXXXX',
  github:       'https://github.com/your-username',
  certificate:  'https://drive.google.com/file/d/XXXX/view'
};
```

Any value left as `''` stays visible but inactive, and clicking it shows a reminder.

## Preview locally

Double-click `index.html`, or for a proper HTTP preview:

```bash
python serve.py
```

## Deploy to GitHub Pages

1. Create a **public** repository named `<your-username>.github.io`.
2. Upload the **contents** of this folder (not the folder itself) to the repo root, so
   that `index.html` sits at the top level.
3. Go to **Settings → Pages**, set **Source** to `Deploy from a branch`, branch `main`,
   folder `/ (root)`, and save.
4. Wait 1–2 minutes, then visit `https://<your-username>.github.io/`.

Full step-by-step instructions, including the command-line route, are in
`DEPLOY.md`.

## Editing the content

Everything is plain HTML — search `index.html` for the text you want to change.

| To change | Look for |
| --- | --- |
| Name, tagline, intro | `<section class="hero"` |
| Rotating job titles | `phrases` array in `assets/js/main.js` |
| Metrics row | `<section class="metrics"` |
| Experience / education | `<section ... id="experience"` |
| Projects | `<section ... id="projects"` |
| Publications | `<section ... id="publications"` |
| Skills | `<section ... id="skills"` |
| Contact & references | `<section ... id="contact"` |
| Colours | `:root` block at the top of `assets/css/style.css` |

To add a publication, copy an existing `<article class="pub ...">` block and change the
text, the `data-role` attribute (`first`, `second` or `co`) and the `--v` value on the
impact meter (impact factor ÷ 10 × 100%).
