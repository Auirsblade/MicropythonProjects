import time, neopixel, machine, random
from CommonUtils import LEDUtils
from CommonUtils.LEDUtils import Color

num_pixels = 150

pixels = neopixel.NeoPixel(machine.Pin(29, machine.Pin.OUT), num_pixels)

# Global brightness (0-100)
BRIGHTNESS = 75

pixels.fill(Color.OFF)
pixels.write()

def animate_on(color, delay=0.01):
    scaled_color = LEDUtils.scale_color(color, BRIGHTNESS)
    for i in range(num_pixels):
        pixels[i] = scaled_color
        pixels.write()
        time.sleep(delay)

def animate_off(delay=0.01):
    for i in range(num_pixels):
        pixels[i] = Color.OFF
        pixels.write()
        time.sleep(delay)


def twinkle(color, bg_color=Color.OFF, delay=0.5):
    """Randomly sparkles pixels with a specific color over a background."""
    bg_scaled = LEDUtils.scale_color(bg_color, BRIGHTNESS)
    pixels.fill(bg_scaled)

    # Pick a random pixel
    idx = random.randint(0, num_pixels - 1)
    pixels[idx] = LEDUtils.scale_color(color, BRIGHTNESS)
    pixels.write()
    time.sleep(delay)
    # Fade it back to background (optional, here we just set it back next loop usually,
    # but for a simple twinkle, resetting it immediately looks sparklier)
    pixels[idx] = bg_scaled


def cylon(color, delay=0.05, eye_size=3):
    """Moves a 'eye' of light back and forth."""
    scaled = LEDUtils.scale_color(color, BRIGHTNESS)
    off = Color.OFF

    # Forward
    for i in range(num_pixels - eye_size):
        pixels.fill(off)
        for j in range(eye_size):
            pixels[i + j] = scaled
        pixels.write()
        time.sleep(delay)

    # Backward
    for i in range(num_pixels - eye_size, 0, -1):
        pixels.fill(off)
        for j in range(eye_size):
            pixels[i + j] = scaled
        pixels.write()
        time.sleep(delay)


def rainbow_cycle(wait=0.01):
    """Draws a rainbow that uniformly distributes itself across all pixels."""

    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)

    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            color = wheel(pixel_index & 255)
            # Reorder for GRB if needed, though wheel returns RGB usually.
            # Assuming your Color class handles raw tuples well, but let's swap to GRB
            # if your strip needs it. Based on LEDUtils comments, it seems to expect GRB tuples.
            # Wheel is usually R, G, B. Let's swap to G, R, B to match typical WS2812.
            r, g, b = color

            # Apply brightness
            pixels[i] = LEDUtils.scale_color((g, r, b), BRIGHTNESS)

        pixels.write()
        time.sleep(wait)


def christmas_twinkle(delay=0.015):
    """Random sparkly effect with red and white twinkles"""
    colors = [Color.RED, Color.WHITE, Color.GOLD, Color.GREEN]

    # Light up 5-8 random pixels with random colors and store them
    lit_pixels = {}  # {index: color}
    pixels.fill(Color.OFF)

    for _ in range(random.randint(20, 50)):
        idx = random.randint(0, num_pixels - 1)
        color = random.choice(colors)
        lit_pixels[idx] = color
        pixels[idx] = LEDUtils.scale_color(color, BRIGHTNESS)

    # Fade in and out only the lit pixels
    for brightness in list(range(1, BRIGHTNESS + 1, 1)) + list(range(BRIGHTNESS, 0, -1)):
        for idx, color in lit_pixels.items():
            pixels[idx] = LEDUtils.scale_color(color, brightness)
        pixels.write()
        time.sleep(delay)


def christmas_pulse(delay=0.02):
    # Pulse red
    for brightness in list(range(5, BRIGHTNESS, 1)) + list(range(BRIGHTNESS, 5, -1)):
        pixels.fill(LEDUtils.scale_color(Color.RED, brightness))
        pixels.write()
        time.sleep(delay)

    # Quick transition from red to green (10 frames)
    for step in range(10):
        factor = step / 10.0
        interpolated = LEDUtils.interpolate_color(Color.RED, Color.GREEN, factor)
        pixels.fill(LEDUtils.scale_color(interpolated, 5))
        pixels.write()
        time.sleep(delay)

    # Pulse green
    for brightness in list(range(5, BRIGHTNESS, 1)) + list(range(BRIGHTNESS, 5, -1)):
        pixels.fill(LEDUtils.scale_color(Color.GREEN, brightness))
        pixels.write()
        time.sleep(delay)

    # Quick transition from green to red (10 frames)
    for step in range(10):
        factor = step / 10.0
        interpolated = LEDUtils.interpolate_color(Color.GREEN, Color.RED, factor)
        pixels.fill(LEDUtils.scale_color(interpolated, 5))
        pixels.write()
        time.sleep(delay)


def candy_cane_stripes(delay=0.02):
    """Red and white stripes that smoothly transition as they animate across the strip"""
    stripe_width = 5

    # Use more frames for smoother animation (multiply offset by sub-pixels)
    for offset in range(stripe_width * 2 * 100):  # 100x more frames for smoothness
        pixels.fill(Color.OFF)
        for i in range(num_pixels):
            # Calculate which stripe this pixel is in, with fractional precision
            stripe_pos = (i + offset / 10.0) // stripe_width
            stripe_phase = (i + offset / 10.0) % stripe_width

            # Determine base color for this stripe (alternating red/white)
            if int(stripe_pos) % 2 == 0:
                base_color = Color.RED
                next_color = Color.WHITE
            else:
                base_color = Color.WHITE
                next_color = Color.RED

            # Smoothly transition within each stripe (0.0 to 1.0)
            transition_factor = stripe_phase / stripe_width
            interpolated = LEDUtils.interpolate_color(base_color, next_color, transition_factor)

            pixels[i] = LEDUtils.scale_color(interpolated, BRIGHTNESS)

        pixels.write()
        time.sleep(delay)


def christmas_chase(delay=0.01):
    """Random sparkly chase effect with smooth color transitions"""
    colors = [Color.RED, Color.WHITE, Color.GOLD, Color.GREEN]
    chase_length = 5

    # Use more frames for smoother animation
    for offset in range(num_pixels * 10):  # 10x more frames for smoothness
        pixels.fill(Color.OFF)

        # Calculate position with fractional precision
        pos = offset / 10.0
        color_idx = int(pos) % len(colors)

        # Get current color and next color for smooth transitions
        current_color = colors[color_idx]
        next_color = colors[(color_idx + 1) % len(colors)]

        # Calculate transition factor between colors
        color_transition = (pos % 1.0)

        # Draw the chase with fade effect
        for j in range(chase_length):
            idx = (int(pos) + j) % num_pixels

            # Fade effect: closer to front is brighter
            fade_brightness = BRIGHTNESS - (j * (BRIGHTNESS / chase_length))

            # Interpolate between colors as we move through the strip
            interpolated = LEDUtils.interpolate_color(current_color, next_color, color_transition)
            pixels[idx] = LEDUtils.scale_color(interpolated, max(fade_brightness, 0))

        pixels.write()
        time.sleep(delay)


def festive_sparkle(delay=0.15):
    """Bright random sparkles that appear and fade"""
    # Randomly light up pixels and let them fade
    for _ in range(10):
        pixels.fill(Color.OFF)
        num_sparkles = random.randint(3, 8)

        for _ in range(num_sparkles):
            idx = random.randint(0, num_pixels - 1)
            color = random.choice([Color.RED, Color.GREEN, Color.WHITE, Color.GOLD])
            pixels[idx] = LEDUtils.scale_color(color, BRIGHTNESS)

        pixels.write()
        time.sleep(delay)


def christmas_rainbow(delay=0.02):
    """Rainbow fade through Christmas colors with random LED assignments"""
    colors = [Color.RED, Color.GREEN, Color.WHITE, Color.GOLD]

    # Generate random color assignment for each pixel (stays same during color transitions)
    pixel_colors = [random.randint(0, len(colors) - 1) for _ in range(num_pixels)]

    # Cycle through color transitions
    for transition in range(len(colors) * 10):  # Multiple cycles
        # Hold on the true color longer (30 frames at current color)
        for hold_step in range(30):
            for i in range(num_pixels):
                color_idx = pixel_colors[i]
                current_color = colors[color_idx]
                pixels[i] = LEDUtils.scale_color(current_color, BRIGHTNESS)

            pixels.write()
            time.sleep(delay)

        # Quick fade through 8 steps per transition (faster)
        for step in range(8):
            factor = step / 8.0

            for i in range(num_pixels):
                # Get this pixel's assigned color index
                color_idx = pixel_colors[i]
                current_color = colors[color_idx]
                next_color = colors[(color_idx + 1) % len(colors)]

                # Interpolate between current and next color
                interpolated = LEDUtils.interpolate_color(current_color, next_color, factor)
                pixels[i] = LEDUtils.scale_color(interpolated, BRIGHTNESS)

            pixels.write()
            time.sleep(delay)

        # Rotate the color assignments for the next cycle
        pixel_colors = [(c + 1) % len(colors) for c in pixel_colors]


def icicle_shimmer(delay=0.08):
    for _ in range(20):
        pixels.fill(LEDUtils.scale_color(Color.AQUA, BRIGHTNESS * .30))

        # Add bright sparkles
        for _ in range(random.randint(3, 6)):
            idx = random.randint(0, num_pixels - 1)
            pixels[idx] = LEDUtils.scale_color(Color.WHITE, BRIGHTNESS)

        pixels.write()
        time.sleep(delay)

while True:
    # animate_on(Color.WARM_WHITE)
    # animate_off()

    # Example usage:
    animations = [
        christmas_chase,
        christmas_twinkle,
        christmas_pulse,
        candy_cane_stripes,
        christmas_rainbow,
        icicle_shimmer]

    for animation in animations:
        for _ in range(10):
            animation()