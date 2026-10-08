# Captions — AD1 MUNA

- `captions.tsv`: start, end, text (seconds). The timing is copied from the reference ad's own captions, so it matches `audio/ad1_master_audio.mp3`.
- `captions.srt`: the same captions for CapCut or Premiere.
- `png/`: 720x1280 transparent overlays in the reference style (white rounded box, purple #7A00F8 Poppins Medium 38px, centred at y≈957). Rebuild them with `python3 tools/render_captions.py`.

The text follows the client's script, not the reference's auto-captions. The reference had misheard words that would look like mistakes to the client: "pitos estrujanos" → **fitoestrógenos**, "del estruje no la hormona" → **del estrógeno, la hormona**, "Botero" → **gotero**, "boda de mi hermano" → **hermana**, "1 000 noches de bodas" → **mi noche de bodas**, "desvalanciarlo" → **desbalancearlo**, "llévate" → **te llevas**, and others.

⚠ Listen once to these windows: the reference showed no caption or only part of the line here, so the split of the words was estimated.
| Time | Line |
|---|---|
| 38.2–40.0 | "cada reto de sentadillas dándolo todo." Check that "dándolo todo" is actually spoken. |
| 79.0–82.5 | "…en absoluto". Dijo / que las mujeres en Brasil" |
| 109.6–117.2 | "Por generaciones… han usado fitoestrógenos: raíz de maca, fenogreco, ashwagandha, para despertar esa señal…" |
| 125.9–127.5 | no caption (product insert, as in the reference) |
| 230.0–230.7 | "así que" |
