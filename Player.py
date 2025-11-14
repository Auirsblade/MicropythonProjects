import machine, neopixel, LedController, time, random

from ConfigValues import Color, Times, ConfigStatus

NUM_LEDS = 1
BRIGHTNESS = 1
INACTIVE_BRIGHTNESS = 0.05
DEBOUNCE_MS = 60
CONFIG_MS = 2000
SUB_CONFIG_MS = 1000

class Player:
    def __init__(self, player_number, button_pin_num, neopixel_pin_num):
        """
        Initialize a Player object.

        Args:
            player_number: Integer identifying the player (e.g., 1, 2, 3...)
            button_pin_num: GPIO pin number for the player's button
            neopixel_pin_num: GPIO pin number for the player's NeoPixel strip
        """
        # Player setup
        self.player_number = player_number
        self.button = machine.Pin(button_pin_num, machine.Pin.IN, machine.Pin.PULL_UP)
        self.neopixel = neopixel.NeoPixel(machine.Pin(neopixel_pin_num, machine.Pin.OUT), NUM_LEDS)

        # Player state
        self.is_active = True
        self.is_turn = False
        self.config_status = ConfigStatus.NOT_IN_CONFIG
        self.pending_color = None
        self.color = random.choice(Color.all())
        self.pending_timer = None
        self.appy_timer = None
        
        # Button timing state
        self.button_press_time = None
        self.button_release_time = None
        self.last_action_time = None

    def is_button_pressed(self):
        """Check if the button is currently pressed (active low)."""
        return self.button.value() == 0

    def record_button_press(self):
        """Record the time when button was pressed. Called from IRQ."""
        if self.button_press_time is None:
            self.button_press_time = time.ticks_ms()
            print(f"[IRQ] Player {self.player_number} button pressed at {self.button_press_time}")

    def record_button_release(self):
        """Record the time when button was released. Called from IRQ."""
        if self.button_press_time is not None:
            self.button_release_time = time.ticks_ms()
            print(f"[IRQ] Player {self.player_number} button released at {self.button_release_time}")

    def check_button_event(self, is_current_player):
        if self.button_release_time is None and not self.button_press_time is None:
            return False

        # Handle inactive player config cycling
        if self.button_press_time is None:
            if not self.is_active:
                return self._handle_inactive_config_timeout()
            return False

        # Validate button press duration
        duration = self._calculate_and_validate_duration()
        if duration is None:
            print(f"  -> Rejected: debounced")
            return False

        # Handle long press for activation toggle
        if duration > CONFIG_MS:
            print(f"  -> Accepted: long press for config toggle")
            self.toggle_activation()
            return self.return_action(False)

        # Handle current player turn action
        if is_current_player:
            print(f"  -> Accepted: not their turn (current: Player {self.player_number})")
            return self.return_action(True)

        # Handle configuration mode for inactive players
        if not self.is_active:
            print(f"  -> Accepted: inactive player config")
            return self._handle_config_button_press(duration)

        return self.return_action(False)

    def _handle_inactive_config_timeout(self):
        """Handle automatic config cycling when player is inactive and button not pressed."""
        if self._is_time_elapsed(SUB_CONFIG_MS):
            print(f"  -> Accepted: inactive config time trigger config: {self.config_status}")
            if self.config_status == ConfigStatus.COLOR:
                self.cycle_color()
            elif self.config_status == ConfigStatus.TIMER:
                self.cycle_timer()
            return self.return_action(False)
        return False

    def _calculate_and_validate_duration(self):
        """Calculate button press duration and validate it meets minimum threshold."""
        duration = time.ticks_diff(self.button_release_time, self.button_press_time)

        # Clear the button event timestamps
        self.button_press_time = None
        self.button_release_time = None

        print(f"[Process] Player {self.player_number} button: duration={duration}ms")

        # Check if duration meets minimum threshold
        if duration < DEBOUNCE_MS:
            print(f"  -> Rejected: too short ({duration}ms < {DEBOUNCE_MS}ms)")
            return None

        return duration

    def _handle_config_button_press(self, duration):
        """Handle button press during configuration mode for inactive players."""
        if self.config_status == ConfigStatus.NOT_IN_CONFIG:
            print(f"  -> changing to color config")
            self.config_status = ConfigStatus.COLOR
            self.pending_color = self.color
            return self.return_action(False)
        elif self.config_status == ConfigStatus.COLOR:
            if duration > SUB_CONFIG_MS:
                self.color = self.pending_color
            self.pending_color = None
            self.set_color((0, 0, 0), BRIGHTNESS)

            print(f"  -> changing to timer config")
            self.config_status = ConfigStatus.TIMER
            self.pending_timer = Times.XS
            return self.return_action(False)
        elif self.config_status == ConfigStatus.TIMER:
            if duration > SUB_CONFIG_MS:
                self.appy_timer = self.pending_timer
            self.pending_timer = None

            print(f"  -> changing to inactive config")
            self.config_status = ConfigStatus.NOT_IN_CONFIG
            return self.return_action(False)
        return None

    def _is_time_elapsed(self, threshold_ms):
        """Check if the specified time threshold has elapsed since last action."""
        time_since_last_action = time.ticks_diff(time.ticks_ms(), self.last_action_time)
        return time_since_last_action > threshold_ms

    def return_action(self, flag):
        self.last_action_time = time.ticks_ms()
        return flag

    def cycle_color(self):
        colors = Color.all()
        current_index = colors.index(self.pending_color)
        next_index = (current_index + 1) % len(colors)
        self.pending_color = colors[next_index]
        self.set_color(self.pending_color, BRIGHTNESS)

    def cycle_timer(self):
        times = Times.all()
        current_index = times.index(self.pending_timer)
        next_index = (current_index + 1) % len(times)
        self.pending_timer = times[next_index]

    def start_turn(self):
        self.is_turn = True
        self.set_color(self.color, BRIGHTNESS)

    def end_turn(self):
        self.is_turn = False
        self.set_color(self.color, INACTIVE_BRIGHTNESS)

    def toggle_activation(self):
        if self.is_active:
            self.is_active = False
            self.set_color((0, 0, 0), 0)
        else:
            self.is_active = True
            self.config_status = ConfigStatus.NOT_IN_CONFIG
            self.pending_timer = None
            self.appy_timer = None
            self.set_color(self.color, INACTIVE_BRIGHTNESS)

    def set_color(self, color, brightness: float = BRIGHTNESS):
        LedController.fill(self.neopixel, color, NUM_LEDS, brightness)


    def __repr__(self):
        return f"Player(number={self.player_number}, button_pin={self.button}, leds={len(self.neopixel)})"