import machine, neopixel, time

LED_PIN = 29          # LED strip data
NUM_LEDS = 214        # change to your strip length
DEFAULT_BRIGHTNESS = 0.05    # keep small while on USB only (e.g., 0.02–0.1)

np = neopixel.NeoPixel(machine.Pin(LED_PIN, machine.Pin.OUT), NUM_LEDS)

# LED Segments
N = 6

# Hardcoded LED index ranges for each player/segment
SEGMENTS = {
    1: range(178, 214),   # 35 LEDs
    2: range(0, 35),      # 35 LEDs
    3: range(35, 71),     # 36 LEDs
    4: range(71, 107),    # 36 LEDs
    5: range(107, 142),   # 36 LEDs
    6: range(142, 178),   # 36 LEDs
}

def scale(c, brightness):
    # c is (r,g,b) 0-255; apply software brightness
    return tuple(min(255, max(0, int(v * brightness))) for v in c)

def fill(pixels, color, length, brightness = DEFAULT_BRIGHTNESS):
    color = scale(color, brightness)
    for i in range(length):
        pixels[i] = (color[1], color[0], color[2])  # GRB order
    pixels.write()

def wheel(pos):
    if pos < 85:
        return pos * 3, 255 - pos * 3, 0
    if pos < 170:
        pos -= 85
        return 255 - pos * 3, 0, pos * 3
    pos -= 170
    return 0, pos * 3, 255 - pos * 3

def rainbow_frame(player, j, step=7):
    for i in SEGMENTS[player]:
        r, g, b = wheel((i * step + j) & 255)
        r, g, b = scale((r, g, b), DEFAULT_BRIGHTNESS)
        np[i] = (g, r, b)  # GRB
    np.write()

def reset():
    fill(np, (255, 255, 255), NUM_LEDS)

def test_sequence():
    for color in ((255,0,0), (0,255,0), (0,0,255), (255,255,255)):
        fill(np, color, NUM_LEDS)
        time.sleep(0.25)
    fill(np, (0,0,0), NUM_LEDS)