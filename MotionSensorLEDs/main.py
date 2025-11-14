import time, neopixel, machine

pir = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)

num_pixels = 92

pixels = neopixel.NeoPixel(machine.Pin(1, machine.Pin.OUT), num_pixels)

# Define colors at full brightness
WARM_WHITE = (255, 180, 100)  # Warm white with orange tint
OFF = (0, 0, 0)

# Global brightness (0-100)
BRIGHTNESS = 75

def scale_color(color, brightness=BRIGHTNESS):
    """Scale a color tuple by brightness percentage (0-100)"""
    return tuple(int(c * brightness / 100) for c in color)

pixels.fill(OFF)
pixels.write()

motionDetected = False
detectionCountdown = 0

COOLDOWN_SECONDS = 3  # how long to ignore new motion after turning off
cooldown_remaining = 0

def animate_on(color, delay=0.01):
    scaled_color = scale_color(color)
    for i in range(num_pixels):
        pixels[i] = scaled_color
        pixels.write()
        time.sleep(delay)

def animate_off(delay=0.01):
    for i in range(num_pixels):
        pixels[i] = OFF
        pixels.write()
        time.sleep(delay)

print("Starting motion detection...")

while True:
    pir_state = pir.value()

    # Decrement countdowns
    if detectionCountdown > 0:
        detectionCountdown -= 1
    if cooldown_remaining > 0:
        cooldown_remaining -= 1

    # If motion is currently detected (lights on)
    if motionDetected:
        if pir_state == 1:
            # Still seeing motion: keep extending the "on" time
            detectionCountdown = 10
        elif detectionCountdown <= 0:
            # No motion for a while: turn off and start cooldown
            print("motion no longer detected")
            motionDetected = False
            animate_off(delay=0.01)
            cooldown_remaining = COOLDOWN_SECONDS

    # If motion is currently NOT detected (lights off)
    else:
        # Only allow new motion if cooldown is over
        if pir_state == 1 and cooldown_remaining <= 0:
            print("motion detected")
            motionDetected = True
            detectionCountdown = 10
            animate_on(WARM_WHITE, delay=0.01)

    time.sleep(1)