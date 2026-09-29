# gstack Tutorial #5 — AGI Race V2

**From YouTube analytics to a re-engineered Short: CSR-RAP agent × Claude Opus 5.5 × HyperFrames**

![Three layers, one loop: decide → build → render → measure](assets/fig_pipeline_en.png)

## What this tutorial does

It documents, end to end, how a published YouTube Short (58,736 views, 98
comments) was diagnosed with the CSR-RAP framework, measured with FFmpeg,
briefed to Claude Opus 5.5 in Claude Code, and rebuilt with HyperFrames into
two new versions: a 56.34 s 16:9 master and a separately directed 46.54 s
9:16 Short. It ends with the measurement plan that decides whether V2
actually beat V1.

This is **V2 of the existing AGI Race Short**. Episode 2 ("OpenAI vs.
Anthropic — Mission: Impossible Edition") is still in production and is not
taught here.

## At a glance

| | V1 (published) | V2 |
|---|---|---|
| Runtime | 62.49 s | 56.34 s master (16:9) · 46.54 s Short (9:16) |
| Hook complete | slower | 4.15 s |
| Characters | recognised by face | role tags (THE ACCELERATOR, THE LITIGATOR …) |
| 9:16 | centre crop, several failures | re-directed shot by shot |
| CSR-RAP score (design) | B = 0.602 | B = 0.770 (+27.9 %) |
| Comments per 1,000 views | 1.67 | target > 2.5, **not yet measured** |

Watch V2: [9:16 Short](https://youtube.com/shorts/mEztESwn7mI) · [16:9 master](https://youtu.be/6MnhRmSR_TA)

## Tutorial No. 5

| Read | Language |
|---|---|
| [TUTORIAL.md](TUTORIAL.md) | English |
| [TUTORIAL.zh.md](TUTORIAL.zh.md) | 中文 |

| Deliverable | English | 中文 |
|---|---|---|
| Executive memo (Word) | [gstack-tutorial-5_EN.docx](dist/gstack-tutorial-5_EN.docx) | [gstack-tutorial-5_ZH.docx](dist/gstack-tutorial-5_ZH.docx) |
| Slide deck (PowerPoint, 18 slides) | [gstack-tutorial-5_EN.pptx](dist/gstack-tutorial-5_EN.pptx) | [gstack-tutorial-5_ZH.pptx](dist/gstack-tutorial-5_ZH.pptx) |
| Slide deck (PDF, view in browser) | [gstack-tutorial-5_EN.pdf](dist/gstack-tutorial-5_EN.pdf) | [gstack-tutorial-5_ZH.pdf](dist/gstack-tutorial-5_ZH.pdf) |

No Office installed? Open the **PDF**. GitHub previews it directly in the browser.

## The gstack tutorial series

| # | Topic |
|---|---|
| [#2](https://github.com/mikelix/gstack-tutorial-2) | AI-agent end-to-end EDA flow on SkyWater SKY130, with verification gates |
| [#3](https://github.com/mikelix/gstack-tutorial-3) | English → Chinese video-captioning pipeline |
| [#4](https://github.com/mikelix/gstack-tutorial-4-tweet-screenshot-tool) | From AI planning to working production software (Tweet Screenshot) |
| **#5** | **This repo: AGI Race V2 with CSR-RAP × Opus 5.5 × HyperFrames** |

## Stack

| Tool | Role | Install |
|---|---|---|
| CSR-RAP agent (custom GPT) | Decides what to change: R × A × P scoring | — |
| Claude Code + Claude Opus 5.5 | Plans, writes and verifies the composition | Claude subscription |
| [gstack](https://github.com/garrytan/gstack) | Premise challenge, plan review, code review | ~1 minute, see TUTORIAL §1.2 |
| [HyperFrames](https://github.com/heygen-com/hyperframes) | Seek-safe HTML → MP4 rendering | Claude Code plugin, see TUTORIAL §1.3 |
| FFmpeg | Visual DNA measurement, render probing | `winget install --id Gyan.FFmpeg -e` |

## Run it yourself (Windows 11)

Check your toolchain first:

```powershell
powershell -ExecutionPolicy Bypass -File starter\scripts\check_prereqs.ps1
```

Then follow TUTORIAL Parts 1–9. The three prompts you paste are in
[`starter/prompts/`](starter/prompts/), and a project `CLAUDE.md` template is
in [`starter/CLAUDE.md.example`](starter/CLAUDE.md.example).

| Prompt | Paste into | Produces |
|---|---|---|
| [01_csr_rap_diagnosis.md](starter/prompts/01_csr_rap_diagnosis.md) | CSR-RAP agent | R/A/P scores and the change list |
| [02_visual_dna.md](starter/prompts/02_visual_dna.md) | Claude Code (Opus 5.5) | Measured Visual DNA of V1 |
| [03_opus55_v2_build.md](starter/prompts/03_opus55_v2_build.md) | Claude Code (Opus 5.5) + HyperFrames | V2 master, V2 Short, QA report |

## Repository layout

```text
README.md            this file
TUTORIAL.md          English tutorial
TUTORIAL.zh.md       Chinese tutorial
assets/              figures + annotated screenshots (EN and ZH)
dist/                Word memos, slide decks and PDFs (EN and ZH)
docs/SOURCES.md      every number, with its source
starter/prompts/     01 CSR-RAP diagnosis · 02 Visual DNA · 03 V2 build prompt
starter/scripts/     check_prereqs.ps1
starter/CLAUDE.md.example
_build/              generators: one bilingual source → figures, memos, decks
```

## Known limitations

- **No real V2 analytics yet.** Every V2 result here is a structural (design) score. The measured result will be added after the 72-hour analytics pull.
- The four setup screenshots are **illustrative mock-ups**. Replace them with your own captures before publishing a fork.
- The videos satirise real public figures. V2 uses role tags instead of names; review platform policy before each release.

## Reproducing the tutorial artifacts

```bash
pip install matplotlib pillow          # figures
python _build/make_figures.py          # → assets/*.png
node _build/build_deck.js              # → dist/*.pptx   (needs pptxgenjs)
node _build/build_doc.js               # → dist/*.docx   (needs docx)
python _build/verify.py                # number and EN/ZH parity checks
```

The PDFs are exported from the `.pptx` files in PowerPoint
(**File → Export → Create PDF/XPS**). Re-export them whenever the decks change.

Edit `_build/content.js` (memo and deck text) or the tutorials, never the
generated files in `dist/`.

## What's intentionally not in this repo

The V1 and V2 video files, the HyperFrames project source, and the full
V2 storyboard. The tutorial teaches the method; the YouTube uploads are the
public artifacts.

## License

MIT — see [LICENSE](LICENSE).
