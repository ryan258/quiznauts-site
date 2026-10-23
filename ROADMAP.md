# Roadmap — Quiznauts Site

Local, single-user authoring site for the Quiznauts channel and brand marketing materials. Built with Hugo extended, vanilla Sass tokens, and Python standard-library automation.

---

## Implemented

| Area | Status / Notes |
| --- | --- |
| **Site architecture** | Hugo extended with LibSass; zero npm, node, or external framework dependencies. |
| **Design tokens** | `assets/scss/_tokens.scss` and `site.scss` exposing CSS custom properties for responsive typography, high-contrast text, 44px minimum controls, and reduced-motion preferences. |
| **Poster style** | Sibling player cut-paper space poster style: navy night sky (`#031522`), navy ink (`#071D2B`), cream paper (`#F3E6C8`), gold (`#EFB23F`), vermilion (`#DC4027`), and blue (`#2B5E9E`). |
| **Interactive mission** | `content/missions/first-contact.md` with `data/quick_mission.json` (3-question sample, sourced explanations, and a no-JavaScript reveal path). |
| **Collections & pages** | Field notes, about, links, site notes, media kit, 404, RSS feeds, and robots.txt. |
| **Brand library** | `static/brand/`: preserved v1.4 vector masters, PNGs, and lossless WebPs for Mr. Big mascot poses, badges, frames, and glyphs. |
| **Marketing exports** | `static/marketing/`: 14 platform exports (YouTube banner, thumbnail, open graph, Pinterest, avatar, etc.) across SVG, PNG, and lossless WebP; deterministic brand and social download kits. |
| **Local CLI (`qn`)** | `./qn` helper commands: `serve`, `build`, `check`, `browser`, `kit`, `images`, `art`, `backup`, `status`, `readiness`. |
| **Content contracts** | Verified mapping in `data/missions.json`, public host rules in `data/url_policy.json`, and source checks in `scripts/`. |
| **Hosting & CI/CD** | GitHub Pages deployment workflow (`.github/workflows/deploy.yml`) with automated Hugo extended build, contract checks, deterministic kit packaging, dynamic base URL configuration, and `.nojekyll` protection. |

---

## Verified

| Evidence scope | Recorded result | Open items |
| --- | --- | --- |
| **Contract tests** | 12 tests pass (`python3 -m unittest discover -s scripts -p test_contracts.py`) | Browser-specific interaction acceptance |
| **Local site check** | `./qn check` passes cleanly (12 pages, 310 local references, 14 marketing assets, 22 WebP images, 44 brand files, ZIP integrity pass) | Human visual/content sign-off |
| **Reflow repair** | Viewport reflow repairs recorded in `docs/reflow-repair.md` | Owner browser rerun via `./qn browser` |
| **Image optimization** | All 22 PNGs have lossless WebP companions matching hashes in `docs/image-optimization.json` | None |

---

## Next Actions & Proposed

- **GitHub Pages activation**: In GitHub repository settings (Settings → Pages), set Source to **GitHub Actions**. Pushing `main` or triggering `workflow_dispatch` will deploy automatically.
- **Browser review rerun**: Execute `./qn browser` using Playwright in the sibling environment to verify layout across 24 test cases.
- **External destinations**: Populate verified channel and social URLs in `data/properties.json` when established; empty values remain safely hidden from public links.
- **Dart Sass migration**: Migrate Sass pipeline before Hugo removes deprecated LibSass in future releases.
- **Custom domain (optional)**: Add CNAME or custom domain in GitHub Pages settings if moving away from default `ryan258.github.io/quiznauts-site/`.
