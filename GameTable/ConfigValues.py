class ConfigStatus:
    """Configuration status constants."""
    NOT_IN_CONFIG = 0
    COLOR = 1
    TIMER = 2


# These buttons are RGB, but the LED controller uses GRB
class Color:
    """Color constants in RGB format (GRB conversion handled by LedController)."""
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    PINK = (255, 192, 203)
    TEAL = (0, 128, 128)
    AQUA = (0, 255, 255)
    MAGENTA = (255, 0, 255)

    @classmethod
    def all(cls):
        """Return list of all color values."""
        return [
            cls.GREEN, cls.RED, cls.BLUE, cls.YELLOW, cls.WHITE,
            cls.PURPLE, cls.ORANGE, cls.PINK, cls.TEAL, cls.AQUA, cls.MAGENTA
        ]


class Times:
    """Timer duration constants."""
    XS = 1
    SM = 2
    MD = 4
    LG = 8
    XL = 12

    @classmethod
    def all(cls):
        """Return list of all timer values."""
        return [cls.XS, cls.SM, cls.MD, cls.LG, cls.XL]