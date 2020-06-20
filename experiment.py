import multiprocessing
import random

from game import Game
from player import BalancedLogicalPlayerMaximizeSelf, LogicalPlayerMinimiseOthers, LogicalPlayer


def play_game(t):
    # because passing arguments is a bitch
    i, amount_of_players, amount_of_starting_tiles, max_tile_number, player_classes = t

    # Start the game from here
    player_classes = player_classes.copy()
    random.shuffle(player_classes)
    game = Game(
        amount_of_players=amount_of_players,
        amount_of_starting_tiles=amount_of_starting_tiles,
        max_tile_number=max_tile_number,
        add_human_player=False,
        player_classes=players_classes
    )

    while not game.has_ended():
        game.play_round()

    print(f"Done with {i}")
    return type(game.winner()).__name__


# Parameter settings
n = 20
amount_of_players = 4
amount_of_starting_tiles = 4
max_tile_number = 10
# players_classes = [BalancedLogicalPlayerMaximizeSelf, BalancedLogicalPlayerMaximizeSelf, LogicalPlayerMinimiseOthers,
#                    LogicalPlayerMinimiseOthers]
players_classes = [BalancedLogicalPlayerMaximizeSelf, BalancedLogicalPlayerMaximizeSelf, LogicalPlayer,
                   LogicalPlayer]


# Multiprocessing part
pool = multiprocessing.Pool(processes=None)
winners = pool.map(play_game, ((i, amount_of_players, amount_of_starting_tiles, max_tile_number, players_classes) for i in range(n)))
pool.close()
pool.join()



# Extract and print results
results_dict = {}
for winner in winners:
    if winner in results_dict:
        results_dict[winner] += 1
    else:
        results_dict[winner] = 1

print(f"N={n}\nAmount of players={amount_of_players}\nAmount of starting tiles={amount_of_starting_tiles}")
print(f"max_tile_number={max_tile_number} ({max_tile_number * 2} tiles)\nPlayer classes={players_classes}")
print(results_dict)
