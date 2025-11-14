# Python
import machine, time, LedController
import ButtonController

N = len(ButtonController.BUTTONS_BY_PLAYER)

# State managed in main loop
current_player = 1
pending_next_segment = None

def _button_irq(pin):
    # Minimal ISR: track press/release events
    for player in ButtonController.BUTTONS_BY_PLAYER.values():
        if player.button is pin:
            if player.is_button_pressed():
                player.record_button_press()
            else:
                player.record_button_release()
            break

def main():
    global current_player, pending_next_segment

    # Set up IRQ for each player's button
    for player_num, player in ButtonController.BUTTONS_BY_PLAYER.items():
        try:
            player.button.irq(trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING, handler=_button_irq)
            print(f"IRQ set up for Player {player_num} on pin {player.button}")
        except AttributeError:
            player.button.irq(trigger=getattr(machine.Pin, "IRQ_FALLING", 0) | getattr(machine.Pin, "IRQ_RISING", 0), handler=_button_irq)
            print(f"IRQ set up (fallback) for Player {player_num} on pin {player.button}")

    LedController.test_sequence()
    ButtonController.init_all()
    LedController.reset()
    ButtonController.BUTTONS_BY_PLAYER[current_player].start_turn()
    j = 0
    print(f"Game ready! {N} players. Current player: {current_player}")

    while True:
        # Process button events between frames
        pending_next_segment = ButtonController.apply_button_events(current_player)
        if pending_next_segment is not None:
            # Clear current LEDs fully before switching to avoid leftovers
            LedController.reset()
            current_player = pending_next_segment
            pending_next_segment = None
            # small pause to ensure clear is latched on the strip
            time.sleep(0.005)

        LedController.rainbow_frame(current_player, j, step=7)
        j = (j + 1) & 255
        time.sleep(0.02)

# Run
main()