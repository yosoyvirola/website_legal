# Starting AD1 in Claude Desktop

Paste the prompt below into a **new chat in the Code tab** of Claude Desktop, with this repo's `muna-ad1/` folder open. Atlas Cloud must be connected first (playbook tab 2).

```
We're producing MUNA AD1 "Arruiné su boda". Everything is already planned in this folder:
- PRODUCTION_PLAN.md: cast, 22 storyboard sheets locked to the reference timing, and the prompts
- audio/ad1_master_audio.mp3: final audio (do not change it)
- captions/: corrected captions (do not change them)
- tools/assemble.py: builds the final video from clips/sheet01.mp4 … sheet22.mp4

Steps (show me each result and wait for my OK before moving on):
1. Check the Atlas Cloud balance.
2. Generate the 5 character sheets (Valeria BEFORE, Valeria AFTER, Daniela slim, Daniela curvy, Tía) with the image tool, using prompt 4.1. Attach the MUNA bottle photo wherever the product appears.
3. Generate storyboard Sheet 01 (prompt 4.2) and animate it in Atlas with Seedance 2.0 Mini, 720p, 9:16, 11 s (prompt 4.3). It's the test.
4. Once I approve it, produce sheets 02–22 the same way and save them as clips/sheetNN.mp4.
5. Run: python3 tools/assemble.py, then do the QC in section 6 of the plan.
Rules: Muna branding only (never Amua), 3D Pixar-style look like the reference, the hero has Mexican features and a flat → pear-shaped transformation.
```

Requirements on the computer: Node.js 18+ (for Atlas), Python 3 with Pillow (`pip install pillow`) and ffmpeg (Mac: `brew install ffmpeg`; Windows: `winget install ffmpeg`).
