# Pear Pie - Time Timer tool pod (OFFICE) - MicroPython, Waveshare 1.8" ST7735S
from machine import Pin, SPI
import framebuf, time, math

# ---------- SETTINGS ----------
DURATION_MIN = 25
WIDTH, HEIGHT = 128, 160        # portrait (native)
RADIUS = 58
# colours are byte-swapped for the SPI order (Waveshare convention)
def rgb(r, g, b):
    c = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return ((c << 8) | (c >> 8)) & 0xFFFF
TIMER = rgb(0x2E, 0xC4, 0xF1)   # cyan disk. red = rgb(0xE0,0x30,0x30)
FACE  = rgb(0xFF, 0xFF, 0xFF)   # empty part
RING  = rgb(0x14, 0x12, 0x16)   # outline
BG    = rgb(0xFF, 0xFF, 0xFF)
MADCTL = 0xC0                   # if red/blue look swapped, use 0xC8

# ---------- PINS (all right side) ----------
spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))
CS  = Pin(17, Pin.OUT)
DC  = Pin(20, Pin.OUT)
RST = Pin(21, Pin.OUT)
BL  = Pin(22, Pin.OUT)
BTN = Pin(26, Pin.IN, Pin.PULL_UP)

# ---------- ST7735S DRIVER ----------
class LCD(framebuf.FrameBuffer):
    def __init__(self):
        self.buf = bytearray(WIDTH * HEIGHT * 2)
        super().__init__(self.buf, WIDTH, HEIGHT, framebuf.RGB565)
        BL.value(1)
        self._init()
    def _cmd(self, c):
        DC.value(0); CS.value(0); spi.write(bytearray([c])); CS.value(1)
    def _data(self, d):
        DC.value(1); CS.value(0); spi.write(bytearray([d])); CS.value(1)
    def _init(self):
        RST.value(1); time.sleep_ms(5); RST.value(0); time.sleep_ms(20)
        RST.value(1); time.sleep_ms(150)
        for c in (0x01,): self._cmd(c)
        time.sleep_ms(150)
        self._cmd(0x11); time.sleep_ms(255)            # sleep out
        self._cmd(0xB1); [self._data(x) for x in (0x01,0x2C,0x2D)]
        self._cmd(0xB2); [self._data(x) for x in (0x01,0x2C,0x2D)]
        self._cmd(0xB3); [self._data(x) for x in (0x01,0x2C,0x2D,0x01,0x2C,0x2D)]
        self._cmd(0xB4); self._data(0x07)
        self._cmd(0xC0); [self._data(x) for x in (0xA2,0x02,0x84)]
        self._cmd(0xC1); self._data(0xC5)
        self._cmd(0xC2); [self._data(x) for x in (0x0A,0x00)]
        self._cmd(0xC3); [self._data(x) for x in (0x8A,0x2A)]
        self._cmd(0xC4); [self._data(x) for x in (0x8A,0xEE)]
        self._cmd(0xC5); self._data(0x0E)
        self._cmd(0x20)                                # inversion off
        self._cmd(0x36); self._data(MADCTL)            # orientation/colour order
        self._cmd(0x3A); self._data(0x05)              # 16-bit colour
        self._cmd(0x13); time.sleep_ms(10)
        self._cmd(0x29); time.sleep_ms(100)            # display on
    def show(self):
        self._cmd(0x2A); [self._data(x) for x in (0x00,0x00,0x00,WIDTH-1)]
        self._cmd(0x2B); [self._data(x) for x in (0x00,0x00,0x00,HEIGHT-1)]
        self._cmd(0x2C)
        DC.value(1); CS.value(0); spi.write(self.buf); CS.value(1)

lcd = LCD()
CX, CY = WIDTH // 2, HEIGHT // 2

# ---------- DRAW THE SHRINKING DISK ----------
def draw_disk(fraction):
    lcd.fill(BG)
    sweep = fraction * 2 * math.pi
    r2, rin2 = RADIUS * RADIUS, (RADIUS - 2) * (RADIUS - 2)
    for dy in range(-RADIUS, RADIUS + 1):
        yy = CY + dy
        for dx in range(-RADIUS, RADIUS + 1):
            d2 = dx * dx + dy * dy
            if d2 > r2:
                continue
            if d2 >= rin2:
                lcd.pixel(CX + dx, yy, RING)
            else:
                a = math.atan2(dx, -dy)
                if a < 0:
                    a += 2 * math.pi
                lcd.pixel(CX + dx, yy, TIMER if a <= sweep else FACE)
    lcd.show()

# ---------- RUN ----------
total = DURATION_MIN * 60
start = time.ticks_ms()
last_min = -1
draw_disk(1.0)

while True:
    if not BTN.value():                # restart
        start = time.ticks_ms()
        last_min = -1
        time.sleep_ms(200)
    elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000
    remaining = max(0, total - elapsed)
    mins = math.ceil(remaining / 60)
    if mins != last_min:               # only redraw when the minute changes
        draw_disk(remaining / total)
        last_min = mins
    time.sleep_ms(200)
