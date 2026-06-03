# UART_TEST.py

from machine import UART, Pin
import time

uart = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13),
            bits=8, parity=None, stop=1, timeout=50)

print("dumping raw radar bytes for 10 seconds, stand in front...")
end = time.ticks_add(time.ticks_ms(), 10000)
while time.ticks_diff(end, time.ticks_ms()) > 0:
    n = uart.any()
    if n:
        data = uart.read(n)
        print(data)
    time.sleep_ms(100)
print("done")
