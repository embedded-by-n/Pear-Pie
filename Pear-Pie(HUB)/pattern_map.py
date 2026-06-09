#!/usr/bin/env python3
# =============================================================================
# pattern_map.py  -  Pear Pie walked-pattern map (demo visualiser)
# =============================================================================
# Shows: the walked trail + dwell, the learned "normal" per room, AND the
# second-order loop: the predicted next room, the per-pod parameters the hub
# is pushing, and a rolling log of second-order activity.
#
# READ-ONLY: it re-runs the hub's own model + rules to SHOW what the hub is
# deciding. It never pushes anything and never touches the pods.
# =============================================================================

import sys, time, csv, math, os, threading

import pygame

# --- optional ML overlay (degrades gracefully if libs/model missing) ---------
try:
    import model
    import rules
    import pod_registry
    _ML = True
except Exception as e:
    print("ML overlay off (%s). Map still runs." % e)
    _ML = False

# --- CONFIG -------------------------------------------------------------------
LOG_PATH = os.path.expanduser("~/Pear-Pie/Pear-Pie(HUB)/pod_log.csv")
FULLSCREEN = "--full" in sys.argv

ROOMS = {
    1: {"name": "Hallway",                  "pos": (0.22, 0.20)},
    2: {"name": "Kitchen (cooking)",        "pos": (0.50, 0.18)},
    3: {"name": "Kitchen island / walkway", "pos": (0.50, 0.46)},
    4: {"name": "Office",                   "pos": (0.78, 0.20)},
    5: {"name": "Lounge / couch",           "pos": (0.74, 0.74)},
    6: {"name": "Bedroom doorway",          "pos": (0.50, 0.64)},
    7: {"name": "Bathroom",                 "pos": (0.24, 0.80)},
    8: {"name": "Bedroom",                  "pos": (0.50, 0.86)},
}

# --- BRAND PALETTE ------------------------------------------------------------
BG      = (20, 18, 22)
MAGENTA = (233, 31, 236)
LIME    = (200, 240, 44)
CYAN    = (46, 196, 241)
GOLD    = (255, 192, 0)
CREAM   = (255, 248, 231)
DIM     = (255, 248, 231)

PRESENT_SECS = 4
TRAIL_SECS   = 45
LINK_SECS    = 6

HOUSE_CENTRE = (0.50, 0.55)
MAP_FRAC = 0.70

SECONDORDER_EVERY = 30   # seconds between read-only model/rules recomputes


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
        self.fonttiny = pygame.font.SysFont("Courier New", 14)
        self.last_seen = {pid: -1e9 for pid in ROOMS}
        self.dwell     = {pid: 0 for pid in ROOMS}
        self.order     = []
        self.cur = None
        self.prev = None
        self.last_move = ""
        self._last_mtime = 0
        self.sweep = 0.0
        self.total       = {pid: 0 for pid in ROOMS}
        self.present_n   = {pid: 0 for pid in ROOMS}
        self.unusual_last = {pid: 0 for pid in ROOMS}
        self.unusual_n   = {pid: 0 for pid in ROOMS}
        self.obs_total   = 0
        self._rows_done  = 0
        # --- second-order overlay state (filled by the background worker) ----
        self.params = {}            # pod_id -> {"alpha":, "threshold":}
        self.param_flash = {}       # pod_id -> time a param last changed
        self.predicted_pid = None   # pod the model predicts you'll go to next
        self.predicted_name = None
        self.events = []            # rolling (time, text) second-order log
        if _ML:
            t = threading.Thread(target=self._secondorder_worker, daemon=True)
            t.start()

    # --- background: re-run the hub's model + rules (read-only) --------------
    def _secondorder_worker(self):
        while True:
            try:
                updates = rules.compute_updates()
                now = time.time()
                for pid, vals in updates.items():
                    old = self.params.get(pid)
                    if old and (old["threshold"] != vals["threshold"]
                                or old["alpha"] != vals["alpha"]):
                        self.param_flash[pid] = now
                        self.events.append((now, "pod %d retuned  thr %.2f"
                                            % (pid, vals["threshold"])))
                self.params = updates
                # prediction from the current room's space
                if self.cur is not None:
                    from_space = pod_registry.get_space(self.cur)
                    lt = time.localtime()
                    pred = model.predict_next_space(lt.tm_hour, lt.tm_wday, from_space)
                    if pred:
                        pid = pod_registry.get_pod_for_space(pred)
                        if pid != self.predicted_pid:
                            self.events.append((now, "predicts next: %s" % pred))
                        self.predicted_pid = pid
                        self.predicted_name = pred
                self.events = self.events[-6:]
            except Exception as e:
                self.events.append((time.time(), "2nd-order skipped"))
                self.events = self.events[-6:]
            time.sleep(SECONDORDER_EVERY)

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
            self.total[pid]   += 1
            self.obs_total    += 1
            if present == 1:
                self.present_n[pid] += 1
            self.unusual_last[pid] = unusual
            if unusual == 1:
                self.unusual_n[pid] += 1
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
        return (self.present_n[pid] / self.total[pid]) if self.total[pid] else 0.0

    def map_xy(self, px, py):
        return int(px * self.W * MAP_FRAC), int(py * self.H * 0.92 + self.H * 0.04)

    def node_xy(self, pid):
        px, py = ROOMS[pid]["pos"]
        return self.map_xy(px, py)

    def draw(self):
        now = time.time()
        self.screen.fill(BG)
        cx, cy = self.map_xy(*HOUSE_CENTRE)

        map_right = int(self.W * MAP_FRAC)
        max_r = min(cx, cy, map_right - cx, self.H - cy) - 16
        max_r = max(max_r, 60)

        for i in range(1, 6):
            pygame.draw.circle(self.screen, (40, 38, 44), (cx, cy), int(max_r * i / 5), 1)
        self.sweep += 0.012
        ex = cx + math.cos(self.sweep) * max_r
        ey = cy + math.sin(self.sweep) * max_r
        sweep_surf = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        pygame.draw.line(sweep_surf, (46, 196, 241, 60), (cx, cy), (ex, ey), 36)
        self.screen.blit(sweep_surf, (0, 0))

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

        for pid in ROOMS:
            x, y = self.node_xy(pid)
            age = now - self.last_seen[pid]
            present = age < PRESENT_SECS
            glow = max(0.0, 1 - age / TRAIL_SECS) if age < TRAIL_SECS else 0.0
            r = 16 + min(self.dwell[pid], 40) * 0.7

            # --- predicted-next room: pulsing gold ring -----------------------
            if pid == self.predicted_pid and not present:
                pulse = 0.5 + 0.5 * math.sin(now * 3)
                ps = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                pygame.draw.circle(ps, GOLD + (int(120 * pulse),), (x, y),
                                   int(r + 14 + 8 * pulse), 3)
                self.screen.blit(ps, (0, 0))

            # --- param-update flash: brief gold halo --------------------------
            if pid in self.param_flash and now - self.param_flash[pid] < 2.0:
                fa = int(160 * (1 - (now - self.param_flash[pid]) / 2.0))
                fs = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
                pygame.draw.circle(fs, GOLD + (fa,), (x, y), int(r + 26))
                self.screen.blit(fs, (0, 0))

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

            # --- per-pod pushed parameters readout ----------------------------
            if pid in self.params:
                p = self.params[pid]
                txt = "thr %.2f  a %.3f" % (p["threshold"], p["alpha"])
                col = GOLD if (pid in self.param_flash and now - self.param_flash[pid] < 2.0) else (140, 136, 128)
                pr = self.fonttiny.render(txt, True, col)
                self.screen.blit(pr, (x - pr.get_width() // 2, y + int(r) + 30))

        panel_x = int(self.W * 0.04)
        cur_name = ROOMS[self.cur]["name"] if self.cur else "waiting for presence"
        hot = max(self.dwell, key=lambda k: self.dwell[k]) if any(self.dwell.values()) else None
        hot_name = ROOMS[hot]["name"] if hot else "-"
        self.screen.blit(self.fontsm.render("NOW IN", True, CYAN), (panel_x, self.H - 150))
        self.screen.blit(self.fontbig.render(cur_name, True, CREAM), (panel_x, self.H - 130))
        self.screen.blit(self.fontsm.render("LAST MOVE   " + self.last_move, True, (150, 146, 138)), (panel_x, self.H - 78))
        self.screen.blit(self.fontsm.render("MOST ACTIVE   " + hot_name, True, (150, 146, 138)), (panel_x, self.H - 54))
        if self.predicted_name:
            self.screen.blit(self.fontsm.render("PREDICTS NEXT   " + self.predicted_name, True, GOLD), (panel_x, self.H - 30))

        self.draw_learning_panel()
        pygame.display.flip()

    def draw_learning_panel(self):
        pw = int(self.W * 0.28)
        px = self.W - pw
        panel = pygame.Surface((pw, self.H), pygame.SRCALPHA)
        panel.fill((30, 28, 34, 180))
        self.screen.blit(panel, (px, 0))

        x = px + 22
        self.screen.blit(self.fontsm.render("WHAT PEAR PIE HAS LEARNED", True, GOLD), (x, 24))
        self.screen.blit(self.fontsm.render("%d readings observed" % self.obs_total, True, (150, 146, 138)), (x, 50))

        bar_w = pw - 64
        y = 88
        # leave room at the bottom for the second-order activity log
        log_h = 150
        row_h = (self.H - 120 - log_h) / max(len(ROOMS), 1)
        for pid in ROOMS:
            occ = self.occupancy(pid)
            name = ROOMS[pid]["name"]
            flagged = self.unusual_last[pid] == 1

            self.screen.blit(self.fontsm.render(name, True, GOLD if flagged else CREAM), (x, int(y)))
            by = int(y) + 22
            pygame.draw.rect(self.screen, (60, 58, 64), (x, by, bar_w, 9), border_radius=4)
            pygame.draw.rect(self.screen, CYAN, (x, by, int(bar_w * occ), 9), border_radius=4)
            self.screen.blit(self.fonttiny.render("normal %d%%" % round(occ * 100), True, (150, 146, 138)), (x, by + 12))

            if flagged:
                tag = self.fonttiny.render("UNUSUAL", True, MAGENTA)
                self.screen.blit(tag, (px + pw - tag.get_width() - 22, int(y)))
            y += row_h

        # --- second-order activity log -------------------------------------
        ly = self.H - log_h
        pygame.draw.line(self.screen, (60, 58, 64), (x, ly - 8), (px + pw - 22, ly - 8))
        self.screen.blit(self.fontsm.render("SECOND-ORDER ACTIVITY", True, GOLD), (x, ly))
        if not _ML:
            self.screen.blit(self.fonttiny.render("overlay off (model not loaded)", True, (150, 146, 138)), (x, ly + 24))
        ey = ly + 26
        for ts, txt in reversed(self.events):
            stamp = time.strftime("%H:%M", time.localtime(ts))
            self.screen.blit(self.fonttiny.render("%s  %s" % (stamp, txt), True, (180, 176, 168)), (x, ey))
            ey += 18

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
