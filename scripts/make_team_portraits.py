"""Create uniformly framed team portraits (4:5, 560x700) from the original photos.

Every portrait gets the same head size and the same headroom, so the Team grid looks
consistent whatever the shape of the original photo. Originals are never modified.

To add or replace a person: put the photo in static/images/, add an entry below with
  cx   = horizontal centre of the face (fraction of image width, 0-1)
  top  = top of the head or hair (fraction of image height)
  chin = bottom of the chin (fraction of image height)
and run:  python scripts/make_team_portraits.py
(Tip: if a face is small or the photo is low resolution, the result is upscaled and will look soft.
Use the highest-resolution original you have.)
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "static/images", ROOT / "static/images/team"
SIZE = (560, 700)          # 4:5
HEAD_FRACTION = 0.38       # head (hair top to chin) as a share of the portrait height
HEADROOM = 0.14            # space above the head as a share of the portrait height

# Photos taken very close (no room above the head): add this much white above, as a fraction of the photo height.
# The background becomes white anyway, so this only gives the head the same headroom as everyone else.
# cx / top / chin for these photos are measured on the PADDED image.
PAD_TOP = {"papie-medgar-mojaki.jpg": 0.25}

PEOPLE = {  # file: (cx, top, chin)
    "mampho.png": (0.43, 0.00, 0.345),
    "sean.jpg": (0.55, 0.10, 0.53),
    "papie-medgar-mojaki.jpg": (0.58, 0.21, 0.74),
    "koketso.jpeg": (0.56, 0.28, 0.53),
    "mzwakhe.jpg": (0.50, 0.14, 0.53),
    "athabile-ntlokwana.jpg": (0.49, 0.10, 0.46),
    "mercy.jpeg": (0.50, 0.05, 0.46),
    "sinalo.jpeg": (0.53, 0.14, 0.50),
    "patience.jpg": (0.545, 0.03, 0.27),
}


def open_source(name):
    im = Image.open(SRC / name).convert("RGB")
    pad = PAD_TOP.get(name)
    if pad:
        canvas = Image.new("RGB", (im.width, round(im.height * (1 + pad))), (255, 255, 255))
        canvas.paste(im, (0, canvas.height - im.height))
        im = canvas
    return im


def crop_box(w, h, cx, top, chin):
    head = (chin - top) * h
    ch = head / HEAD_FRACTION                 # ideal crop height
    ch = min(ch, h, w / 0.8)                  # cannot exceed the photo
    cw = ch * 0.8
    y = top * h - HEADROOM * ch
    x = cx * w - cw / 2
    y = max(0, min(y, h - ch)); x = max(0, min(x, w - cw))
    return round(x), round(y), round(x + cw), round(y + ch)


def main():
    """Frame and whiten every portrait (delegates to whiten_team_backgrounds.py so the result is always on white)."""
    import whiten_team_backgrounds as w
    OUT.mkdir(parents=True, exist_ok=True)
    for name in PEOPLE:
        print("done", w.make(name).name)


if __name__ == "__main__":
    main()
