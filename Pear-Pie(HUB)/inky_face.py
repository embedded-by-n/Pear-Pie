#!/usr/bin/env python3
# =============================================================================
# inky_face.py  -  Pear Pie calm e-ink face (Inky Impression, 7-colour)
# =============================================================================
# The Inky is the CALM, undemanding face of Pear Pie. It is NOT the live map
# (e-ink can't animate). It quietly redraws a still summary every 10 minutes:
# where you are now, today's rhythm, and what the system has learned. No
# buttons, no interaction - it just sits there and updates itself. That is the
# point: an ignorable, no-demand companion.
#
# Reads the same pod_log.csv the hub logger writes. Runs forever; refreshes
# every REFRESH_MINUTES. Start it once and leave it.
#
# RUN (on the hub Pi, venv active):
#   nohup python inky_face.py &
# DEPS: the Inky library (already installed) + Pillow (comes with it).
# =============================================================================

import time, csv, os
from datetime import datetime

from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont

# --- CONFIG -------------------------------------------------------------------
LOG_PATH = os.path.expanduser("~/Pear-Pie/Pear-Pie(HUB)/pod_log.csv")
REFRESH_MINUTES = 10
PRESENT_SECS = 60          # "now in" = a present-ping within the last minute

ROOMS = {
    1: "Hallway",
    2: "Kitchen (cooking)",
    3: "Kitchen island / walkway",
    4: "Office",
    5: "Lounge / couch",
    6: "Bedroom doorway",
    7: "Bathroom",
    8: "Bedroom",
}

# --- PALETTE (Inky inks: blue, yellow, orange, black only - no red/green) -----
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
BLUE   = (0, 0, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)

# roles
HEADER_COL = ORANGE       # "Pear Pie" title
ACCENT_COL = BLUE         # "now in", occupancy bars
LEARN_COL  = ORANGE       # "what it has learned" label
TEXT_COL   = BLACK


def load_font(size):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def read_stats():
    """Read the whole log once and compute: current room, per-room occupancy,
    most-active room, total observations. Returns a dict."""
    total = {pid: 0 for pid in ROOMS}
    present_n = {pid: 0 for pid in ROOMS}
    last_present_ts = {pid: 0.0 for pid in ROOMS}
    obs = 0
    try:
        with open(LOG_PATH, newline="") as f:
            for row in csv.reader(f):
                if len(row) < 4:
                    continue
                try:
                    ts = float(row[0]); pid = int(row[1]); present = int(row[2])
                except ValueError:
                    continue
                if pid not in ROOMS:
                    continue
                total[pid] += 1
                obs += 1
                if present == 1:
                    present_n[pid] += 1
                    if ts > last_present_ts[pid]:
                        last_present_ts[pid] = ts
    except (FileNotFoundError, OSError):
        pass

    now = time.time()
    # most recently present room within the present window = "now in"
    cur = None
    newest = 0.0
    for pid in ROOMS:
        if last_present_ts[pid] > newest and (now - last_present_ts[pid]) < PRESENT_SECS:
            newest = last_present_ts[pid]; cur = pid
    occ = {pid: (present_n[pid] / total[pid] if total[pid] else 0.0) for pid in ROOMS}
    hot = max(occ, key=lambda k: occ[k]) if any(occ.values()) else None
    return {"cur": cur, "occ": occ, "hot": hot, "obs": obs}


def render(inky, stats):
    img = Image.new("P", (inky.WIDTH, inky.HEIGHT))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, inky.WIDTH, inky.HEIGHT), fill=WHITE)

    f_title = load_font(34)
    f_big   = load_font(40)
    f_lbl   = load_font(18)
    f_row   = load_font(20)

    pad = 16
    # header
    d.text((pad, pad), "Pear Pie", font=f_title, fill=HEADER_COL)
    d.text((inky.WIDTH - 150, pad + 8),
           datetime.now().strftime("%H:%M"), font=f_lbl, fill=TEXT_COL)
    d.line((pad, pad + 46, inky.WIDTH - pad, pad + 46), fill=TEXT_COL, width=2)

    # "now in"
    y = pad + 58
    d.text((pad, y), "now in", font=f_lbl, fill=ACCENT_COL)
    cur_name = ROOMS[stats["cur"]] if stats["cur"] else "settled / away"
    d.text((pad, y + 20), cur_name, font=f_big, fill=TEXT_COL)

    # learned occupancy bars
    y += 86
    d.text((pad, y), "what it has learned (normal occupancy)", font=f_lbl, fill=LEARN_COL)
    y += 28
    bar_x = pad + 200
    bar_w = inky.WIDTH - bar_x - pad
    row_h = 30
    for pid in ROOMS:
        occ = stats["occ"][pid]
        d.text((pad, y), ROOMS[pid][:18], font=f_row, fill=TEXT_COL)
        d.rectangle((bar_x, y + 4, bar_x + bar_w, y + 18), outline=TEXT_COL)
        fillw = int(bar_w * occ)
        if fillw > 0:
            d.rectangle((bar_x, y + 4, bar_x + fillw, y + 18), fill=ACCENT_COL)
        d.text((bar_x + bar_w - 44, y), "%d%%" % round(occ * 100), font=f_lbl, fill=TEXT_COL)
        y += row_h

    # footer
    d.text((pad, inky.HEIGHT - 28),
           "%d readings learned   updates every %d min" % (stats["obs"], REFRESH_MINUTES),
           font=f_lbl, fill=TEXT_COL)

    inky.set_image(img)
    inky.show()


def main():
    inky = auto()
    print("Pear Pie e-ink face running. Updates every", REFRESH_MINUTES, "min. Ctrl+C to stop.")
    while True:
        try:
            stats = read_stats()
            render(inky, stats)
            print("refreshed at", datetime.now().strftime("%H:%M"), "obs:", stats["obs"])
        except Exception as e:
            print("refresh error:", e)
        time.sleep(REFRESH_MINUTES * 60)


if __name__ == "__main__":
    main()
