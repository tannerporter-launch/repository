# The Mind Game — v3 (web build)

Self-contained HTML build of the first-person psychological simulation. This is
the shippable, linkable demo (the Godot 4 port under `../mind-game-godot/` is the
larger engine-port effort).

## Live link

Deployed to GitHub Pages by `.github/workflows/deploy-pages.yml` on every push to
`main` that touches `web/`. Once enabled, it serves at:

    https://tannerporter-launch.github.io/repository/

## Contents

- `index.html` — the entire game (single file, ~64 KB).

## Runtime dependencies (loaded from CDN at play time)

- [three.js r128](https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js)
- Google Fonts: Space Mono, EB Garamond

No build step, no bundler, no local assets — open `index.html` in any modern
browser (or visit the live link) and it runs.
