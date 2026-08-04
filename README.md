# Bryant Quest — Major Advisor 🎓🎮

An interactive Flask web application that helps prospective Bryant University students explore majors with real career data, job growth projections, and AI-readiness assessments — in two wildly different visual themes.

## Dual-Theme UI

A toggle in the top-right corner lets users switch between two complete visual experiences. The choice persists across sessions via `localStorage`.

### 🎓 Professor Mode
A polished, professional dark interface using DM Sans and Fraunces serif typefaces, smooth gradients, rounded cards, and a refined data-visualization aesthetic.

### 🎮 Gamer Mode
A full 1980s NES arcade experience — Press Start 2P pixel font, CRT scanline overlay, twinkling starfield, floating clouds, coin-spinning animations, pipe-green career blocks, and brick-pattern ground straight from World 1-1. Labels transform: "College" → "WORLD", "Compare" → "⚔ BATTLE!", salary becomes "GOLD", empty results show "GAME OVER".

## Features

- **31 Bryant University majors** across three colleges, each mapped to real career paths
- **BLS salary data** — entry-level, median, and top-end salaries for every career
- **10-year job growth projections** from the Bureau of Labor Statistics (2023–2033)
- **AI impact scores** (0–100) with detailed qualitative analysis per career
- **Career breadth scores** (0–100) per major — how widely grads spread across occupations, with "where grads land" summaries
- **Grad-school flags** — 🎓 badges on careers needing education beyond a bachelor's, plus a "Bachelor's-Ready Only" filter
- **Three view modes** — expandable card grid, sortable data table, and two interactive charts: Salary vs. AI Impact (per career) and a Breadth vs. AI Exposure quadrant map (per major, with a labeled "Danger Zone" for focused + exposed majors)
- **Compare mode** — side-by-side analysis of up to 4 majors
- **Combine mode** — merge any 2 majors (double major / major + minor) into one profile: union of career paths, best-case AI resilience, bachelor's-reachable count, and combined breadth via a disclosed heuristic
- **Payback estimates** — simulated years to repay 100% debt-financed tuition at the 6.39% federal rate, paying 20% of a salary that starts at entry level and grows 5%/year; adjustable net-cost slider (defaults to Bryant's published average net price), "50+" when interest outruns payments
- **Shareable URLs** — filters, view, selections, and your cost setting are encoded in the address bar, so any state can be sent as a link
- **Filtering & sorting** — by college, salary, growth rate, AI resilience, career breadth, education level, and free-text search
- **Fully responsive** — works on desktop, tablet, and mobile

## Quick Start

```bash
# 1. Install Flask
pip install flask

# 2. Run the app
python app.py

# 3. Open in your browser
http://localhost:5001
```

No database, no build tools, no external APIs needed. All data is embedded in `app.py`.

## Project Structure

```
bryant-major-advisor/
├── app.py              # Flask backend — data, API routes (/api/majors, /api/compare, /api/stats)
├── templates/
│   └── index.html      # Single-page frontend with dual-theme engine
└── README.md
```

## API Endpoints

| Endpoint | Params | Description |
|----------|--------|-------------|
| `GET /api/majors` | `college`, `sort`, `ai_impact`, `education` | Filtered/sorted list of all majors with career data. `education=bachelors` keeps only careers reachable without a graduate degree |
| `GET /api/compare` | `ids` (repeated) | Side-by-side data for up to 4 majors |
| `GET /api/combine` | `ids` (exactly 2) | Merged profile for a pair of majors: deduped career union, best-case AI resilience, combined breadth |
| `GET /api/stats` | — | Aggregate stats: counts, averages, and all career data for the scatter chart |

## Data Sources

| Data | Source |
|------|--------|
| Programs | [Bryant University Undergraduate Programs](https://www.bryant.edu/undergraduate/academics/undergraduate-programs) |
| Salaries | [BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/) (May 2024 estimates) |
| Growth | BLS Employment Projections, 2023–2033 |
| AI Impact | Qualitative assessments based on industry research |

## Customization

All major and career data lives in the `MAJORS_DATA` list in `app.py`. To add or modify a major:

1. Add a new dict to `MAJORS_DATA` following the existing schema
2. Include BLS occupation codes, salary ranges (entry/median/top), growth rates, and employment numbers
3. Write an AI impact analysis and assign a score from 0 (AI-proof) to 100 (highly exposed)
4. The frontend picks it up automatically — no template changes needed

## Disclaimer

AI impact scores are qualitative estimates meant to spark discussion, not definitive predictions. Students should always combine this data with personal interests, strengths, and career goals. Salary figures are national medians and will vary by region, employer, and experience level.
