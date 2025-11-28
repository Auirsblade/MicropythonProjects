def scale_color(color, brightness):
    """Scale a color tuple by brightness percentage (0-100)"""
    return tuple(int(c * brightness / 100) for c in color)

def interpolate_color(color1, color2, factor):
    """Interpolate between two colors. Factor: 0.0 = color1, 1.0 = color2"""
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

class Color:
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    WARM_WHITE = (255, 180, 100)  # Warm white with orange tint
    COOL_WHITE = (200, 200, 255)
    GOLD = (255, 200, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    PINK = (255, 192, 203)
    TEAL = (0, 128, 128)
    AQUA = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    OFF = (0, 0, 0)

    @classmethod
    def all(cls):
        """Return list of all color values."""
        return [
            cls.GREEN, cls.RED, cls.BLUE, cls.YELLOW, cls.WHITE,
            cls.PURPLE, cls.ORANGE, cls.PINK, cls.TEAL, cls.AQUA, cls.MAGENTA
        ]