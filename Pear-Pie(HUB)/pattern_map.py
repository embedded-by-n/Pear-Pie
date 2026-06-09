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
    1: {"name": "Hallway",                  "pos": (0.15, 0.12)},
    2: {"name": "Kitchen (cooking)",        "pos": (0.50, 0.12)},
    3: {"name": "Kitchen island / walkway", "pos": (0.50, 0.45)},
    4: {"name": "Office",                   "pos": (0.85, 0.12)},
    5: {"name": "Lounge / couch",           "pos": (0.82, 0.72)},
    6: {"name": "Bedroom doorway",          "pos": (0.55, 0.66)},
    7: {"name": "Bathroom",                 "pos": (0.15, 0.88)},
    8: {"name": "Bedroom",                  "pos": (0.50, 0.88)},
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
        # --- learning stats (the "what it has learned" panel) ----------------
        # occupancy rate per room = the learned sense of "normal" for that space.
        # unusual flag = the pod's AdaptiveBaseline said "present when usually empty".
        self.total       = {pid: 0 for pid in ROOMS}   # readings seen for this pod
        self.present_n   = {pid: 0 for pid in ROOMS}   # how many were "present"
        self.unusual_last = {pid: 0 for pid in ROOMS}  # latest unusual flag (0/1)
        self.unusual_n   = {pid: 0 for pid in ROOMS}   # times flagged unusual
        self.obs_total   = 0                           # total readings logged
        self._rows_done  = 0                           # rows already counted

    # --- read NEW rows from the CSV and update movement + learning stats -----
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
        # only the rows we have not counted yet (so stats don't double-count)
        new_rows = rows[self._rows_done:]
        self._rows_done = len(rows)
        for row in new_rows:
            if len(row) < 6:
                continue
            try:
                ts = float(row[0]); pid = int(row[1])
                present = int(row[2]); unusual = int(row[3])
            except (ValueError, IndexError):
                continue
            if pid not in ROOMS:
                continue
            # --- learning stats: every reading counts toward "normal" --------
            self.total[pid]   += 1
            self.obs_total    += 1
            if present == 1:
                self.present_n[pid] += 1
            self.unusual_last[pid] = unusual
            if unusual == 1:
                self.unusual_n[pid] += 1
            # --- movement: only a present-ping lights/traces a room ----------
            if present == 1 and ts > self.last_seen[pid]:
                if now - self.last_seen[pid] > PRESENT_SECS and pid != self.cur:
                    self.prev = self.cur
                    self.cur = pid
                    if self.prev is not None:
                        self.last_move = "%s  to  %s" % (ROOMS[self.prev]["name"], ROOMS[pid]["name"])
                    self.order.append((pid, now))
                    self.order = self.order[-12:]
                self.last_seen[pid] = now
                self.dwell[pid] += 1

    def occupancy(self, pid):
        """The learned 'normal' for a room: fraction of readings it was occupied."""
        return (self.present_n[pid] / self.total[pid]) if self.total[pid] else 0.0

    def node_xy(self, pid):
        px, py = ROOMS[pid]["pos"]
        # keep nodes in the left ~70% so they don't hide behind the right panel
        return int(px * self.W * 0.70), int(py * self.H * 0.92 + self.H * 0.04)

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

        self.draw_learning_panel()
        pygame.display.flip()

    # --- the "what Pear Pie has learned" panel -------------------------------
    def draw_learning_panel(self):
        # a translucent panel down the right edge
        pw = int(self.W * 0.28)
        px = self.W - pw
        panel = pygame.Surface((pw, self.H), pygame.SRCALPHA)
        panel.fill((30, 28, 34, 180))
        self.screen.blit(panel, (px, 0))

        x = px + 22
        self.screen.blit(self.fontsm.render("WHAT PEAR PIE HAS LEARNED", True, GOLD), (x, 24))
        self.screen.blit(self.fontsm.render("%d readings observed" % self.obs_total, True, (150, 146, 138)), (x, 50))

        # per-room: learned occupancy ("normal") as a bar + live unusual flag
        bar_w = pw - 64
        y = 92
        row_h = (self.H - 140) / max(len(ROOMS), 1)
        for pid in ROOMS:
            occ = self.occupancy(pid)
            name = ROOMS[pid]["name"]
            flagged = self.unusual_last[pid] == 1

            # room name (lights gold if currently flagged unusual)
            self.screen.blit(self.fontsm.render(name, True, GOLD if flagged else CREAM), (x, int(y)))

            # learned-normal bar (how often this space is usually occupied)
            by = int(y) + 24
            pygame.draw.rect(self.screen, (60, 58, 64), (x, by, bar_w, 10), border_radius=4)
            pygame.draw.rect(self.screen, CYAN, (x, by, int(bar_w * occ), 10), border_radius=4)
            self.screen.blit(self.fontsm.render("normal occupancy %d%%" % round(occ * 100), True, (150, 146, 138)), (x, by + 14))

            # live "unusual" tag from the pod's baseline
            if flagged:
                tag = self.fontsm.render("UNUSUAL", True, MAGENTA)
                self.screen.blit(tag, (px + pw - tag.get_width() - 22, int(y)))

            y += row_h

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
