# Prompt 02 — Visual DNA of the original video

**Where to paste:** Claude Code (Opus 5.5), started in the project root that
contains `source/AGI_Race_V1.mp4` and `source/AGI_Race.srt`.

---

You are a film analyst and FFmpeg engineer. Build a measured "Visual DNA" of
`source/AGI_Race_V1.mp4` that a later HyperFrames re-edit can be held to.
Do not edit or re-render the source. Do not design V2 yet.

1. **Technical profile** with ffprobe: duration, resolution, frame rate,
   codecs, audio layout.
2. **Rhythm:** detect hard cuts with FFmpeg scene detection. Report the cut
   count, shot count, mean and median shot length, the number of shots under
   1 s, and the fastest and slowest 10-second blocks. Include a table of
   every cut with its timestamp.
3. **Key frames:** extract candidate frames, review them yourself, and keep
   about 24 that best represent the story beats. Save them under
   `analysis/Episode1_Visual_DNA/` as `<ID>_t<seconds>_<what-it-shows>.jpg`.
4. **Per frame, nine fields:** story function, why it worked, composition,
   camera, lighting/colour, motion, text/subtitles, mobile (9:16) lesson,
   and what V2 should inherit vs. not copy.
5. **Ending:** measure frame-to-frame motion over the last 5 s. Is it a true
   freeze or a near-freeze? How long is any black?
6. **Colour:** approximate saturation range and the strongest accent.
7. **9:16 test:** make a contact sheet with the centre 9:16 crop marked.
   List every element the crop cuts.
8. **Naming:** record characters by role (Racer-A, Quartermaster, …), never
   by real name.

Write `analysis/Episode1_Visual_DNA.md` (profile, rhythm table, beat→frame
map, per-frame fields, inherit/don't-copy summary, exact commands) and
`analysis/Episode1_Visual_DNA_ContactSheet.jpg`.

Before finishing, re-check every claim against the frames and correct any
that overstate what is visible. Then stop and report. Commit nothing.
