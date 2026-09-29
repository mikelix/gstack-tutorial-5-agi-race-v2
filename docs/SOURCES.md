# SOURCES — every number in this tutorial, and where it came from

Rule for contributors: a number that is not in this file does not go into the
tutorial, the memo, the deck or a figure. If you add one, add its source here first.

## V1 (published Short: "Elon Musk vs. OpenAI: The AGI Race (Mad Max Edition)")

| Fact | Value | Source |
|---|---|---|
| Views | 58,736 | YouTube Studio, as reported by the channel owner to the CSR-RAP agent (2026-09-28) |
| Comments | 98 | same |
| Comment Conversion Index (CCI) | 98 / 58,736 × 1000 = 1.67 | computed |
| Runtime | 62.49 s | `Episode1_Visual_DNA.md` (FFmpeg-measured) |
| Hard cuts / shots | 46 / 47 | same |
| Mean / median shot | 1.34 s / 1.08 s | same |
| Shots under 1 s | 20 of 46 | same |
| Fastest block | ≈50–60 s, mean shot 0.95 s | same |
| Ending | motion drops at 60.1 s, ≈1.5 s near-freeze, then 0.84 s black | same |
| Late-entrant beat | 54.45 s (frame C05) | same |
| 9:16 centre crop | cuts title, wide ensemble, final freeze and every subtitle; close-ups survive | same |
| CSR-RAP V1 | R 88, A 90, P 76 → B = 0.602 | CSR-RAP agent, first analysis |

## Production system milestones

| Fact | Value | Source |
|---|---|---|
| Text-to-video route, home PC | Entry gate FAIL: no reference images, nothing generated | Opus 5.5 report, 2026-09-28 11:49 |
| First HyperFrames short | 6 s, 1920×1080, 30 fps, 5 audio tracks, 15.6 s render | HyperFrames Shot Playbook |
| Pinned HyperFrames CLI | 0.8.79 | project `package.json`, per CSR-RAP review |
| C24 Hero Pilot v2 | 6.000 s, 24 fps, H.264 + stereo AAC; lint 0 errors; check contrast 13/13 | Opus 5.5 QA report, 2026-09-28 14:37 |
| C24 seek test | jump to 2.4/3.4/4.5/5.3 s shows 03/02/01/01 | same |
| C24 black cut | starts frame 139 (5.792 s), holds 0.21 s | same |
| C24 determinism | second render: 61/144 frames identical, 83 differ at ≥50 dB PSNR | same |
| C24 CSR-RAP | R 0.82, A 0.75, P 0.93, B 0.572 | same |

## V2 (two YouTube uploads)

| Fact | Value | Source |
|---|---|---|
| URLs | youtube.com/shorts/mEztESwn7mI (9:16), youtu.be/6MnhRmSR_TA (16:9) | channel owner |
| Master runtime | 56.34 s (−9.8 % vs V1) | V2 storyboard |
| Short runtime | 46.54 s (−25.5 % vs V1) | V2 storyboard |
| Shots | 43 master / 35 Short | V2 storyboard |
| Cold open / title slam / roll call | 0–2.55 s / 2.55–4.15 s / 4.15–8.53 s | V2 storyboard |
| Hook share of Short | 4.15 / 46.54 = 8.9 % | computed |
| Cliff + CTA segment | 8.6 s = 15.3 % of master, 18.5 % of Short | V2 storyboard / computed |
| End-card hold | ≈2.5 s = 5.37 % of Short | CSR-RAP V2 analysis |
| Cut from Short | some roll-call shots, the whole Patron block, part of the GPU montage | V2 storyboard |
| Role tags | THE GPU DEALER, THE LITIGATOR, THE ACCELERATOR, THE SAFETY GUY, THE OPEN-SOURCE GUY, THE LATE ENTRANT | V2 storyboard |
| CSR-RAP V2 | R 92, A 89, P 94 → B = 0.770 (+27.9 % structural vs 0.602) | CSR-RAP V2 analysis |
| Strongest coupling | R × P = 0.865 | computed |
| Real V2 analytics | **not yet collected** | — |

## External tools (checked 2026-09-29)

| Tool | Install | Source |
|---|---|---|
| gstack | `git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`; needs Claude Code, Git, Bun ≥1.0, Node.js (Windows) | github.com/garrytan/gstack README |
| HyperFrames | `claude plugin marketplace add heygen-com/hyperframes` then `claude plugin install hyperframes@hyperframes`; CLI `npx hyperframes init/preview/lint/check/snapshot/render/doctor`; needs Node.js ≥22 and FFmpeg | github.com/heygen-com/hyperframes README |
