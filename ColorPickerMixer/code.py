# RGB Color Picker/Mixer
#   https://github.com/gordykeene
# Hardware: 
#   NeoTrellis M4
#   https://learn.adafruit.com/adabox010/introduction
#   https://learn.adafruit.com/adafruit-neotrellis-m4?view=all
# Libraries:
#   adafruit-circuitpython-bundle-4.x-mpy-20181211.zip
#   https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest

import time
import adafruit_trellism4
 
brightness = [0,3,7,15,31,63,127,255]

trellis = adafruit_trellism4.TrellisM4Express(rotation = 90)

width = trellis.pixels.width
height = trellis.pixels.height

PULSE_SELECTION = False
# These are used for "pulsing"
PULSE_LOW = 8
PULSE_RANGE = 256 - 2 * PULSE_LOW
PULSE_PER_SECOND = .65
# These are used for "blinking"
BLINK_COLOR = (4, 3, 1)
next_blink = time.monotonic() 
blinker_state = False

Ri = height - 1
Gi = height - 1
Bi = height - 1

while True:
    stamp = time.monotonic()
    # print(stamp)

    # reset
    pixels = [[(brightness[(7 - x) * (y == 0)], brightness[(7 - x) * (y == 1)], brightness[(7 - x) * (y == 2)]) for x in range(8)] for y in range(8)]

    # Check for pressed buttons
    pressed = set(trellis.pressed_keys)
    # print(pressed)
    current_press = set()
    for down in pressed - current_press:
        # print("Pressed down", down)
        x = down[0]
        y = down[1]

        if (x == 0): Ri = y
        if (x == 1): Gi = y
        if (x == 2): Bi = y
        if (x == 3): 
            Ri = y
            Gi = y
            Bi = y
        current_press = pressed

    if (PULSE_SELECTION):
        # Pulse active "primary" colors
        ratio = stamp * PULSE_PER_SECOND - int(stamp * PULSE_PER_SECOND)
        pulse = int(2 * ratio * (PULSE_RANGE))
        if (pulse > PULSE_RANGE): pulse = (2 * PULSE_RANGE) - pulse
        pulse += PULSE_LOW
        # print(stamp, ratio, pulse) 
        pixels[0][Ri] = (pulse, 0, 0)
        pixels[1][Gi] = (0, pulse, 0)
        pixels[2][Bi] = (0, 0, pulse)
    else:
        if (stamp >= next_blink):
            blinker_state = not blinker_state
            next_blink += 0.5
        if (blinker_state):
            pixels[0][Ri] = BLINK_COLOR
            pixels[1][Gi] = BLINK_COLOR
            pixels[2][Bi] = BLINK_COLOR

    # Render resulting color
    resultingColor = (brightness[7 - Ri], brightness[7 - Gi], brightness[7 - Bi])
    for y in range(0, height):
        pixels[3][y] = resultingColor

    # Display it
    for x in range(width):
        for y in range(height):
            trellis.pixels[x, y] = pixels[x][y]
