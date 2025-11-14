from Player import Player

NUM_PLAYERS = 6

# Initialize all buttons
BUTTONS_BY_PLAYER = {}
for i in range(NUM_PLAYERS):
    BUTTONS_BY_PLAYER[i + 1] = Player(i + 1, i + 9, i + 2)


def apply_button_events(current_player):
    # Check all player buttons for release events
    for player_num, player in BUTTONS_BY_PLAYER.items():
        process_next_turn = player.check_button_event(player_num == current_player)

        if not process_next_turn:
            continue

        nxt = try_advance_to_player(current_player + 1)
        BUTTONS_BY_PLAYER[current_player].end_turn()
        BUTTONS_BY_PLAYER[nxt].start_turn()
        # Valid button press! Advance to next player
        return nxt
    return None

def try_advance_to_player(target):
    if target > NUM_PLAYERS:
        return try_advance_to_player(1)
    if BUTTONS_BY_PLAYER[target].is_active:
        return target
    return try_advance_to_player(target + 1)


def init_all():
    for button in BUTTONS_BY_PLAYER.values():
        button.end_turn()