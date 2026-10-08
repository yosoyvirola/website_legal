# MUNA VitalDrops · AD1 "Arruiné su boda" (BATCH37 remake)

- `PRODUCTION_PLAN.md`: reference analysis, cast (new Mexican hero, before/after), 22 storyboard sheets locked to the reference timing, and the image and video prompts.
- `audio/ad1_master_audio.mp3`: the reference audio track (same audio, as the brief asks).
- `captions/`: corrected captions in the reference style (TSV, SRT, PNG overlays).
- `reference/`: contact sheets of the reference's 76 shots and `ref_shots.tsv` with the cut times.
- `tools/assemble.py`: put `clips/sheet01.mp4` … `sheet22.mp4` in place, then run `python3 tools/assemble.py`. It writes `out/AD1_MUNA_final.mp4` (720x1280, 30 fps, 244.5 s) with audio, captions and the white flash.

The assembly pipeline was tested end to end with stand-in clips. The output was frame-accurate against the reference.
