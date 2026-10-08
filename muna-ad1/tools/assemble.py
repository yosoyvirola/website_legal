"""Assemble AD1: trim each storyboard clip to its slot, concatenate, add the
white flash, lay the master audio and burn in reference-style captions.

usage: python3 tools/assemble.py [clips_dir] [output.mp4]
"""
import os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
TOTAL = 244.5
FLASH_AT, FLASH_LEN = 11.40, 0.13
SKIP_HEAD = 6 / FPS  # drop the first frames where a storyboard grid can flash

# (sheet, start, end) — locked to the reference cut points, see PRODUCTION_PLAN.md
SLOTS = [
    (1, 0.00, 10.67), (2, 10.67, 19.53), (3, 19.53, 28.87), (4, 28.87, 40.07),
    (5, 40.07, 54.23), (6, 54.23, 67.00), (7, 67.00, 76.10), (8, 76.10, 87.57),
    (9, 87.57, 92.57), (10, 92.57, 105.73), (11, 105.73, 118.73), (12, 118.73, 131.33),
    (13, 131.33, 145.13), (14, 145.13, 155.93), (15, 155.93, 168.27), (16, 168.27, 179.33),
    (17, 179.33, 191.93), (18, 191.93, 206.93), (19, 206.93, 216.07), (20, 216.07, 229.03),
    (21, 229.03, 237.27), (22, 237.27, 244.50),
]


def run(cmd):
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    clips = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "clips")
    output = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "out", "AD1_MUNA_final.mp4")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="ad1_")

    parts = []
    for sheet, s, e in SLOTS:
        src = os.path.join(clips, f"sheet{sheet:02d}.mp4")
        if not os.path.exists(src):
            sys.exit(f"missing {src}")
        need = e - s
        avail = duration(src) - SKIP_HEAD
        pad = max(0.0, need - avail)
        if pad > 0.3:
            print(f"warning: sheet{sheet:02d} is {pad:.2f}s short, holding last frame", file=sys.stderr)
        part = os.path.join(tmp, f"p{sheet:02d}.mp4")
        vf = (f"scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,fps={FPS},"
              f"tpad=stop_mode=clone:stop_duration={pad + 0.5:.3f},setsar=1")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{SKIP_HEAD:.3f}", "-i", src, "-t", f"{need:.3f}",
             "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", part])
        parts.append(part)

    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    video = os.path.join(tmp, "video.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", video])

    # captions + white flash + master audio
    rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(ROOT, "captions", "captions.tsv"), encoding="utf-8") if l.strip()]
    pngdir = os.path.join(ROOT, "captions", "png")
    if len(os.listdir(pngdir)) != len(rows):
        run([sys.executable, os.path.join(ROOT, "tools", "render_captions.py")])
    inputs = ["-i", video, "-i", os.path.join(ROOT, "audio", "ad1_master_audio.mp3")]
    filt = [f"[0:v]drawbox=x=0:y=0:w=iw:h=ih:color=white@1:t=fill:enable='between(t,{FLASH_AT},{FLASH_AT + FLASH_LEN})'[v0]"]
    for i, (s, e, _) in enumerate(rows):
        inputs += ["-i", os.path.join(pngdir, f"{i:03d}.png")]
        filt.append(f"[v{i}][{i + 2}:v]overlay=0:0:enable='between(t,{s},{float(e) - 0.001})'[v{i + 1}]")
    script = os.path.join(tmp, "filter.txt")
    with open(script, "w") as f:
        f.write(";\n".join(filt))
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex_script", script,
         "-map", f"[v{len(rows)}]", "-map", "1:a", "-t", f"{TOTAL}", "-r", str(FPS),
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", output])
    print(f"done: {output} ({duration(output):.2f}s)")


if __name__ == "__main__":
    main()
