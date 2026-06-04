#!/usr/bin/env python3
# =============================================================================
# pattern_map.py  -  Pear Pie walked-pattern map (demo visualiser)
# =============================================================================
# Runs full-screen on the hub Pi and projects the emergent movement pattern:
# which rooms lit up, in what order, how recently (the walked trail), and where
# you are dwelling. It reads pod_log.csv that hub_ble_logger.py writes, so the
# drawing process never competes with the BLE radio.
#
# HONEST SCOPE: this is a RELATIONAL map (which room, in what order, how recent),
# not a GPS position. The radars sense the human, not each other, so there is no
# true (x, y). Place the nodes yourself in ROOMS below to match your home.
#
# RUN:  python3 pattern_map.py            (windowed, for testing)
#       python3 pattern_map.py --full     (full-screen, for the projector)
# DEPS: pip install pygame
# CSV schema expected (from hub_ble_logger.py):
#   timestamp,pod_id,presence,unusual,sequence,rssi
# =============================================================================

import sys, time, csv, math, os

import pygame

# --- CONFIG -------------------------------------------------------------------
LOG_PATH = os.path.expanduser("~/Pear-Pie/Pear-Pie(HUB)/pod_log.csv")  # adjust if needed
FULLSCREEN = "--full" in sys.argv

# Map each POD_ID to a room name and a rough position (0..1 of the screen).
# Lay these out like your home. Position is for the picture, not measured.
ROOMS = {
    1: {"name": "Kitchen",     "pos": (0.22, 0.24)},
    2: {"name": "Hallway",     "pos": (0.50, 0.42)},
    3: {"name": "Living room", "pos": (0.22, 0.74)},
    4: {"name": "Bedroom",     "pos": (0.78, 0.24)},
    5: {"name": "Bathroom",    "pos": (0.80, 0.74)},
}

# --- BRAND PALETTE ------------------------------------------------------------
BG      = (20, 18, 22)        # #141216
MAGENTA = (233, 31, 236)      # #E91FEC
LIME    = (200, 240, 44)      # #C8F02C
CYAN    = (46, 196, 241)      # #2EC4F1
GOLD    = (255, 192, 0)       # #FFC000
CREAM   = (255, 248, 231)     # #FFF8E7
DIM     = (255, 248, 231)

PRESENT_SECS = 4      # how long after the last ping a room counts as "present"
TRAIL_SECS   = 45     # how long a room keeps a fading glow (the walked trail)
LINK_SECS    = 6      # transitions within this window draw a move line


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


class PatternMap:
    def __init__(self):
        pygame.init()
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        self.screen = pygame.display.set_mode((1280, 800), flags)
        pygame.display.set_caption("Pear Pie - walked pattern map")
        self.W, self.H = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.font   = pygame.font.SysFont("Trebuchet MS", 22)
        self.fontbig = pygame.font.SysFont("Trebuchet MS", 40)
        self.fontsm = pygame.font.SysFont("Courier New", 18)
        self.last_seen = {pid: -1e9 for pid in ROOMS}   # last time present
        self.dwell     = {pid: 0 for pid in ROOMS}       # accumulated activity
        self.order     = []                              # recent (pid, time) sequence
        self.cur = None
        self.prev = None
        self.last_move = ""
        self._last_size = 0
        self._last_mtime = 0
        self.sweep = 0.0

    # --- read new rows from the CSV without re-reading the whole file --------
    def poll_log(self):
        try:
            mtime = os.path.getmtime(LOG_PATH)
            if mtime == self._last_mtime:
                return
            self._last_mtime = mtime
            with open(LOG_PATH, newline="") as f:
                rows = list(csv.reader(f))
        except (FileNotFoundError, OSError):
            return
        now = time.time()
        for row in rows[-200:]:                  # only the tail matters
            if len(row) < 6:
                continue
            try:
                ts = float(row[0]); pid = int(row[1]); present = int(row[2])
            except ValueError:
                continue
            if pid not in ROOMS or present != 1:
                continue
            # treat a fresh present-ping as activity in that room
            if ts > self.last_seen[pid]:
                if now - self.last_seen[pid] > PRESENT_SECS and pid != self.cur:
                    self.prev = self.cur
                    self.cur = pid
                    if self.prev is not None:
                        self.last_move = "%s  to  %s" % (ROOMS[self.prev]["name"], ROOMS[pid]["name"])
                    self.order.append((pid, now))
                    self.order = self.order[-12:]
                self.last_seen[pid] = now
                self.dwell[pid] += 1

    def node_xy(self, pid):
        px, py = ROOMS[pid]["pos"]
        return int(px * self.W), int(py * self.H * 0.92 + self.H * 0.04)

    def draw(self):
        now = time.time()
        self.screen.fill(BG)
        cx, cy = self.W // 2, int(self.H * 0.5)

        # radar rings + sweep
        for i in range(1, 6):
            pygame.draw.circle(self.screen, (40, 38, 44), (cx, cy), i * int(self.H * 0.11), 1)
        self.sweep += 0.012
        ex = cx + math.cos(self.sweep) * self.W
        ey = cy + math.sin(self.sweep) * self.W
        sweep_surf = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.line(sweep_surf, (46, 196, 241, 60), (cx, cy), (ex, ey), 36)
        self.screen.blit(sweep_surf, (0, 0))

        # walked-trail move lines (recent transitions)
        for k in range(1, len(self.order)):
            pid_a, ta = self.order[k]
            pid_b, tb = self.order[k - 1]
            age = now - ta
            if age < TRAIL_SECS and (ta - tb) < LINK_SECS:
                a = self.node_xy(pid_b); b = self.node_xy(pid_a)
                alpha = max(0, int(180 * (1 - age / TRAIL_SECS)))
                ls = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                pygame.draw.line(ls, (233, 31, 236, alpha), a, b, 4)
                self.screen.blit(ls, (0, 0))

        # nodes
        for pid in ROOMS:
            x, y = self.node_xy(pid)
            age = now - self.last_seen[pid]
            present = age < PRESENT_SECS
            glow = max(0.0, 1 - age / TRAIL_SECS) if age < TRAIL_SECS else 0.0
            r = 16 + min(self.dwell[pid], 40) * 0.7

            if glow > 0:
                gs = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                col = (233, 31, 236) if present else (46, 196, 241)
                pygame.draw.circle(gs, col + (int(60 * glow),), (x, y), int(r + 30 * glow))
                self.screen.blit(gs, (0, 0))

            if present:
                core = MAGENTA if math.sin(now * 4) > 0 else LIME
            elif glow > 0:
                core = lerp(BG, CYAN, glow)
            else:
                core = (70, 68, 64)
            pygame.draw.circle(self.screen, core, (x, y), int(r))
            pygame.draw.circle(self.screen, BG, (x, y), int(r * 0.45))

            label = self.font.render(ROOMS[pid]["name"], True, CREAM if present else (150, 146, 138))
            self.screen.blit(label, (x - label.get_width() // 2, y + int(r) + 8))

        # info panel
        panel_x = int(self.W * 0.04)
        cur_name = ROOMS[self.cur]["name"] if self.cur else "waiting for presence"
        hot = max(self.dwell, key=lambda k: self.dwell[k]) if any(self.dwell.values()) else None
        hot_name = ROOMS[hot]["name"] if hot else "-"
        self.screen.blit(self.fontsm.render("NOW IN", True, CYAN), (panel_x, self.H - 150))
        self.screen.blit(self.fontbig.render(cur_name, True, CREAM), (panel_x, self.H - 130))
        self.screen.blit(self.fontsm.render("LAST MOVE   " + self.last_move, True, (150, 146, 138)), (panel_x, self.H - 78))
        self.screen.blit(self.fontsm.render("MOST ACTIVE   " + hot_name, True, (150, 146, 138)), (panel_x, self.H - 54))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
            self.poll_log()
            self.draw()
            self.clock.tick(30)
        pygame.quit()


if __name__ == "__main__":
    PatternMap().run()