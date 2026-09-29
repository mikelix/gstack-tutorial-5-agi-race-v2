# Prompt 03 — Build V2 with HyperFrames (Claude Code, Opus 5.5)

**Where to paste:** Claude Code with the HyperFrames plugin and gstack
installed, started in the project root (see TUTORIAL.md §1.4).

**Note:** this is a reusable template that encodes the V2 specification
described in the tutorial. Adjust the change and keep lists to your own
CSR-RAP diagnosis and Visual DNA.

---

## Role and goal

You are a senior YouTube Shorts editor and a HyperFrames engineer. Re-engineer
the published video `source/AGI_Race_V1.mp4` into **V2**: a 16:9 master and a
separately directed 9:16 Short. This is a **re-edit**. Generate no new
photoreal footage. Every change must be traceable to the inputs below.

## Inputs (read all of them before planning)

1. `source/AGI_Race_V1.mp4`, `source/AGI_Race.srt`
2. `analysis/Episode1_Visual_DNA.md` and its frames: the measured benchmark
3. `playbook/HyperFrames_Shot_Playbook.md`: overrides any rule below if they conflict
4. `briefs/CSR-RAP_V1_diagnosis.md`: why V1 converted views but not comments

## Change list (from CSR-RAP)

1. **Cold open:** open on the strongest punchline, before the title
   (V1 line: "Taste my lawsuit, non-profit boy!"; use the clearest delivery).
2. **Title slam** directly after it. The hook (spectacle + punchline +
   premise) must be complete by about 4 s.
3. **Roll call with role tags**, not names: THE GPU DEALER, THE LITIGATOR,
   THE ACCELERATOR, THE SAFETY GUY, THE OPEN-SOURCE GUY, THE LATE ENTRANT.
4. **Delete any line that is not clearly intelligible.** Do not caption what
   the picture already says.
5. **English captions** designed for mobile: centre third horizontally,
   about 60 % frame height in 9:16.
6. **9:16 is a separate composition:** a per-shot horizontal offset, a pan
   for group shots, the title restacked to three lines, a series header in
   the top bar, the bottom and right edges kept clear for platform UI, and a
   fully re-laid-out final card.
7. **Ending:** keep the unresolved jump, then end-card
   *TO BE CONTINUED → EPISODE 2 → SUBSCRIBE*, with a hold of about 2.5 s.
8. **Short edit:** target about 45–47 s. Cut by choice, not evenly: prefer
   removing roll-call repetition, the Patron block and GPU-montage shots. Keep
   hook → rivals → gags → safety counterforce → late entrant → cliff.
9. **Master:** target about 56 s.

## Keep list (from Visual DNA)

- Fast grammar (V1 median shot 1.08 s) and the fastest cutting just before the climax.
- The "slow down" counterforce as the biggest close-up, as the last beat before the climax.
- Near-freeze (≈1.5 s) → black as the ending shape, placed before the end-card.
- The muted grade; do not add saturation.

## Hard rules (Shot Playbook)

1. Route through `/hyperframes` first; this multi-scene job is `/general-video`.
2. Run `npx hyperframes doctor` and read the timeline before designing.
3. Search the catalog before building any named element; reuse where possible.
4. **Seek-safe:** every visual and audio state must be correct if the renderer
   jumps directly to any time. No wall-clock logic, no Web Audio graphs, no
   conflicting second `fromTo`.
5. Holds longer than about 4 s get one monotonic micro-motion (e.g. scale 1 → 1.008), never a loop.
6. One shared token and typography system feeds both compositions.
7. Verification chain for **each** composition:
   `lint` → `check` → `snapshot` (contact sheet) → `render` → `ffprobe`.
   Open every contact sheet yourself and describe what you see.

## Outputs

- `agi-race-v2/` HyperFrames project (CLI version pinned in `package.json`)
- `outputs/v2/AGI_Race_V2_master_16x9.mp4`
- `outputs/v2/AGI_Race_V2_short_9x16.mp4`
- `outputs/v2/V2_Storyboard.md`: every shot with source timecode, V2
  in/out, role tag, caption, and 9:16 offset/pan
- `outputs/v2/V2_QA.md`: gate results, ffprobe output, durations, shot
  counts, and every deviation from this brief with its reason
- Contact sheets for both versions

## Stop conditions

- Stop after both renders and the QA report. **Do not upload anything.**
- If a rule here conflicts with the Playbook, follow the Playbook and log it.
- Any staging change that moves a face or key element away from the
  Visual DNA must be listed for human sign-off, not silently applied.
- Report numbers only from the rendered files. Do not estimate.
