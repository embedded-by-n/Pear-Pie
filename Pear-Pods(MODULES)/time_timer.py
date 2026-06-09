# =============================================================================
# main.py  (OFFICE POD WITH TIME TIMER USE THIS AS MAIN.PY)  -  living light + learning Time Timer (fully local)
# =============================================================================
import time
import led
import gossip
import config
import sensors
import rule_listener
from baseline import AdaptiveBaseline

from machine import Pin, SPI, ADC
import framebuf, math
try:
    import json
except ImportError:
    import ujson as json

# ---------- TIMER CONFIG ----------
T_W, T_H = 128, 160
T_RADIUS = 58
T_FACE_MIN = 60          # whole disk = 60 minutes (real Time Timer face)
T_MAX_MINUTES = 60
T_MIN_MINUTES = 1
T_CONFIRM_SECS = 3       # 3-2-1 before it starts
T_RESET_AFTER = 60       # gone this many seconds -> abandon + reset
T_BREAK_MIN = 10         # pomodoro break length
AVG_ALPHA = 0.3          # how strongly recent choices pull the learned average
DATA_FILE = "/timer_data.json"
T_REDRAW_SECS = 60       # redraw the shrinking pie at most this often

def _rgb(r, g, b):
    c = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return ((c << 8) | (c >> 8)) & 0xFFFF
T_RED   = _rgb(0xE0, 0x30, 0x30)   # study pie (classic red)
T_BREAK = _rgb(0x2E, 0xC4, 0xF1)   # break pie (cyan)
T_FACE  = _rgb(0xFF, 0xFF, 0xFF)
T_RING  = _rgb(0x14, 0x12, 0x16)
T_BG    = _rgb(0xFF, 0xFF, 0xFF)
T_TEXT  = _rgb(0x14, 0x12, 0x16)
T_MADCTL = 0xC0                    # red/blue swapped? use 0xC8

_spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0, sck=Pin(6), mosi=Pin(7))
_CS  = Pin(5, Pin.OUT); _DC = Pin(4, Pin.OUT)
_RST = Pin(3, Pin.OUT);  _BL = Pin(2, Pin.OUT)
_POT = ADC(Pin(26))

class _LCD(framebuf.FrameBuffer):
    def __init__(self):
        self.buf = bytearray(T_W * T_H * 2)
        super().__init__(self.buf, T_W, T_H, framebuf.RGB565)
        _BL.value(1); self._init()
    def _c(self, c):
        _DC.value(0); _CS.value(0); _spi.write(bytearray([c])); _CS.value(1)
    def _d(self, d):
        _DC.value(1); _CS.value(0); _spi.write(bytearray([d])); _CS.value(1)
    def _init(self):
        _RST.value(1); time.sleep_ms(5); _RST.value(0); time.sleep_ms(20)
        _RST.value(1); time.sleep_ms(150)
        self._c(0x01); time.sleep_ms(150)
        self._c(0x11); time.sleep_ms(255)
        self._c(0xB1); [self._d(x) for x in (0x01,0x2C,0x2D)]
        self._c(0xB2); [self._d(x) for x in (0x01,0x2C,0x2D)]
        self._c(0xB3); [self._d(x) for x in (0x01,0x2C,0x2D,0x01,0x2C,0x2D)]
        self._c(0xB4); self._d(0x07)
        self._c(0xC0); [self._d(x) for x in (0xA2,0x02,0x84)]
        self._c(0xC1); self._d(0xC5)
        self._c(0xC2); [self._d(x) for x in (0x0A,0x00)]
        self._c(0xC3); [self._d(x) for x in (0x8A,0x2A)]
        self._c(0xC4); [self._d(x) for x in (0x8A,0xEE)]
        self._c(0xC5); self._d(0x0E)
        self._c(0x20)
        self._c(0x36); self._d(T_MADCTL)
        self._c(0x3A); self._d(0x05)
        self._c(0x13); time.sleep_ms(10)
        self._c(0x29); time.sleep_ms(100)
    def show(self):
        self._c(0x2A); [self._d(x) for x in (0x00,0x00,0x00,T_W-1)]
        self._c(0x2B); [self._d(x) for x in (0x00,0x00,0x00,T_H-1)]
        self._c(0x2C)
        _DC.value(1); _CS.value(0); _spi.write(self.buf); _CS.value(1)

_lcd = _LCD()
_CX, _CY = T_W // 2, T_H // 2

def _draw(a_lo, a_hi, fill, big=None, word=None):
    _lcd.fill(T_BG)
    r2, rin2 = T_RADIUS*T_RADIUS, (T_RADIUS-2)*(T_RADIUS-2)
    for dy in range(-T_RADIUS, T_RADIUS+1):
        yy = _CY + dy
        for dx in range(-T_RADIUS, T_RADIUS+1):
            d2 = dx*dx + dy*dy
            if d2 > r2: continue
            if d2 >= rin2:
                _lcd.pixel(_CX+dx, yy, T_RING)
            else:
                a = math.atan2(dx, -dy)
                if a < 0: a += 2*math.pi
                _lcd.pixel(_CX+dx, yy, fill if (a_lo <= a <= a_hi) else T_FACE)
    if big is not None:
        s = str(big); _lcd.text(s, _CX - len(s)*4, _CY - 4, T_TEXT)
    if word is not None:
        _lcd.text(word, _CX - len(word)*4, _CY + 12, T_TEXT)
    _lcd.show()

def _ang(minutes):
    return (minutes / T_FACE_MIN) * 2 * math.pi

def _pot_minutes():
    raw = _POT.read_u16()
    span = T_MAX_MINUTES - T_MIN_MINUTES
    return T_MIN_MINUTES + round(raw / 65535 * span)

# ---------- PERSISTENT LEARNING ----------
def _load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except Exception:
        return {"avg": 25.0, "completed": 0, "abandoned": 0, "good_breaks": 0}

def _save(d):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(d, f)
    except Exception as e:
        print("save failed:", e)

_data = _load()

def _learn_duration(mins):
    _data["avg"] = AVG_ALPHA * mins + (1 - AVG_ALPHA) * _data["avg"]
    _save(_data)

# ---------- STATE MACHINE ----------
IDLE, SETTING, CONFIRM, RUNNING, PAUSED, ENDED, BREAK, RETURN_DUE = range(8)
_mode = IDLE
_setmin = -999
_still_ms = time.ticks_ms()
_confirm_start = 0
_total = 0
_run_start = 0
_pause_start = 0
_locked_pot = _pot_minutes()
_prev_present = 0
_last_key = None
_last_redraw = time.ticks_ms()

def _ang_total():
    return (_total / 60) * 2 * math.pi if _total else 0

def _go_idle():
    global _mode, _locked_pot, _last_key
    _mode = IDLE; _locked_pot = _pot_minutes(); _last_key = None
    _draw(0, 0, T_RED, word="ready")

def _start_running(mins):
    global _mode, _total, _run_start, _locked_pot, _last_key, _last_redraw
    _total = mins * 60; _run_start = time.ticks_ms()
    _locked_pot = _pot_minutes(); _mode = RUNNING
    _last_key = None; _last_redraw = time.ticks_ms()

def _timer_tick(present):
    global _mode, _setmin, _still_ms, _confirm_start, _total, _run_start
    global _pause_start, _locked_pot, _prev_present, _last_key, _last_redraw
    now = time.ticks_ms(); pot = _pot_minutes()

    if _mode in (IDLE, RUNNING, ENDED, BREAK, RETURN_DUE) and abs(pot - _locked_pot) >= 2:
        _mode = SETTING; _setmin = -999; _still_ms = now

    if _mode == IDLE:
        if present == 1 and _prev_present == 0:
            _start_running(max(1, round(_data["avg"])))

    elif _mode == SETTING:
        if pot != _setmin:
            _setmin = pot; _still_ms = now
            _draw(0, _ang(pot), T_RED, big=pot)
        elif time.ticks_diff(now, _still_ms) / 1000 >= 1:
            _mode = CONFIRM; _confirm_start = now; _last_key = None

    elif _mode == CONFIRM:
        left = T_CONFIRM_SECS - int(time.ticks_diff(now, _confirm_start) / 1000)
        if left <= 0:
            _learn_duration(_setmin); _start_running(_setmin)
        elif left != _last_key:
            _draw(0, _ang(_setmin), T_RED, big=left, word="start"); _last_key = left

    elif _mode == RUNNING:
        if present == 0:
            _mode = PAUSED; _pause_start = now
            consumed = 1 - (max(0, _total - time.ticks_diff(now, _run_start)/1000) / _total) if _total else 0
            _draw(consumed*_ang_total(), _ang_total(), T_RED, word="paused")
        else:
            remaining = max(0, _total - time.ticks_diff(now, _run_start) / 1000)
            if remaining <= 0:
                _data["completed"] += 1; _save(_data)
                _mode = ENDED; _draw(0, 0, T_RED, word="done")
            else:
                key = int(remaining / T_REDRAW_SECS)
                if key != _last_key or time.ticks_diff(now, _last_redraw)/1000 >= T_REDRAW_SECS:
                    consumed = 1 - (remaining / _total)
                    _draw(consumed*_ang_total(), _ang_total(), T_RED)
                    _last_key = key; _last_redraw = now

    elif _mode == PAUSED:
        if present == 1:
            _run_start = time.ticks_add(_run_start, time.ticks_diff(now, _pause_start))
            _mode = RUNNING; _last_key = None
        elif time.ticks_diff(now, _pause_start) / 1000 >= T_RESET_AFTER:
            _data["abandoned"] += 1; _save(_data); _go_idle()

    elif _mode == ENDED:
        _total = T_BREAK_MIN * 60; _run_start = now
        _mode = BREAK; _last_key = None; _last_redraw = now

    elif _mode == BREAK:
        remaining = max(0, _total - time.ticks_diff(now, _run_start) / 1000)
        if remaining <= 0:
            _mode = RETURN_DUE; _draw(0, 0, T_BREAK, word="back?")
        else:
            key = int(remaining / T_REDRAW_SECS)
            if key != _last_key:
                consumed = 1 - (remaining / _total)
                _draw(consumed*_ang(T_BREAK_MIN), _ang(T_BREAK_MIN), T_BREAK, word="break")
                _last_key = key

    elif _mode == RETURN_DUE:
        if present == 1:
            _data["good_breaks"] += 1; _save(_data); _go_idle()

    _prev_present = present

_go_idle()

# =============================================================================
sensors.begin()
led.clear()
learner = AdaptiveBaseline(config.ALPHA)
rule_listener.start(learner)
DEBOUNCE = 3
_raw_prev = 0
_stable_count = 0
present = 0
last_seen = None
prev_present = 0
swept = False
start_ms = time.ticks_ms()
while True:
    raw = sensors.read_presence()
    dist = sensors.last_distance_cm
    now = time.ticks_ms()
    phase = time.ticks_diff(now, start_ms) / 1000.0
    if raw == _raw_prev:
        if _stable_count < DEBOUNCE:
            _stable_count += 1
    else:
        _stable_count = 0
    _raw_prev = raw
    if _stable_count >= DEBOUNCE:
        present = raw
    in_proximity = led.set_proximity(dist)
    if not in_proximity:
        if present == 1:
            if prev_present == 0 and not swept:
                print("ARRIVAL  (distance:", dist, "cm)")
                led.arrival_sweep()
                swept = True
            led.set_purple(phase)
            last_seen = now
        elif last_seen is not None:
            elapsed = time.ticks_diff(now, last_seen) / 1000.0
            if elapsed >= config.FADE_SECONDS:
                led.clear()
                last_seen = None
                swept = False
            else:
                led.set_decay(1.0 - (elapsed / config.FADE_SECONDS))
        else:
            led.clear()
            swept = False
    if present == 1:
        last_seen = now
    threshold = rule_listener.get_threshold()
    learner.update(present)
    unusual = 1 if learner.is_unusual(present, threshold) else 0
    prev_present = present
    gossip.broadcast(config.POD_ID, present, unusual)
    _timer_tick(present)
    time.sleep_ms(120)
