# RGB Color Binary Picker/Mixer
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
 
brightness = [1,2,4,8,16,32,64,128]

trellis = adafruit_trellism4.TrellisM4Express(rotation = 90)

width = trellis.pixels.width
height = trellis.pixels.height

BLINK_COLOR = (0, 0, 0)
next_blink = time.monotonic() 
blinker_state = False

R = 0
G = 0
B = 0
isPressed = False

while True:
    stamp = time.monotonic()
    # print(stamp)

    # reset
    pixels = [[(brightness[(7 - x) * (y == 0)], brightness[(7 - x) * (y == 1)], brightness[(7 - x) * (y == 2)]) for x in range(8)] for y in range(8)]

    # Check for pressed buttons
    pressed = set(trellis.pressed_keys)
    print(pressed)
    current_press = set()
    if (isPressed == False): 
        for down in pressed - current_press:
            isPressed = True
            # print("Pressed down", down)
            x = down[0]
            y = down[1]

            if (x == 0):
                R = R - brightness[7 - y] if R & brightness[7 - y] else R + brightness[7 - y]
            elif (x == 1):
                G = G - brightness[7 - y] if G & brightness[7 - y] else G + brightness[7 - y]
            elif (x == 2):
                B = B - brightness[7 - y] if B & brightness[7 - y] else B + brightness[7 - y]
            elif (y == 0): 
                R = 255
                G = 255
                B = 255
            elif (y == 7): 
                R = 0
                G = 0
                B = 0
            current_press = pressed
    elif (len(pressed) == 0):
        isPressed = False
    
    if (stamp >= next_blink):
        blinker_state = not blinker_state
        next_blink += 0.5
    if (blinker_state):
        for y in range(8):
            pixels[0][y] = BLINK_COLOR if R & brightness[7 - y] else pixels[0][y]
            pixels[1][y] = BLINK_COLOR if G & brightness[7 - y] else pixels[1][y]
            pixels[2][y] = BLINK_COLOR if B & brightness[7 - y] else pixels[2][y]

    # Render resulting color
    # print (R, G, B)
    # resultingColor = (brightness[7 - Ri], brightness[7 - Gi], brightness[7 - Bi])
    for y in range(0, height):
        pixels[3][y] = (R, G, B)

    # Display it
    for x in range(width):
        for y in range(height):
            trellis.pixels[x, y] = pixels[x][y]
