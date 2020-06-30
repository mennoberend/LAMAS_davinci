import multiprocessing
import random
from copy import deepcopy

from game import Game
from player import AggressiveLogicalPlayer, DefensiveLogicalPlayer, LogicalPlayer


def play_game(t):
    # because passing arguments is a bitch
    i, amount_of_players, amount_of_starting_tiles, max_tile_number, player_classes = t

    # Start the game from here
    player_classes = deepcopy(player_classes)
    random.shuffle(player_classes)

    game = Game(
        amount_of_players=amount_of_players,
        amount_of_starting_tiles=amount_of_starting_tiles,
        max_tile_number=max_tile_number,
        add_human_player=False,
        player_classes=player_classes
    )

    while not game.has_ended():
        game.play_round()

    print(f"Done with {i}")
    return type(game.winner()).__name__


# Parameter settings
n = 1000
amount_of_players = 4
amount_of_starting_tiles = 4
max_tile_number = 8

players_classes = [AggressiveLogicalPlayer, AggressiveLogicalPlayer, DefensiveLogicalPlayer, DefensiveLogicalPlayer]
# players_classes = [AggressiveLogicalPlayer, DefensiveLogicalPlayer]

# Multiprocessing part
pool = multiprocessing.Pool(processes=6)
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

print('\nPARAMETERS:')
print(f"N={n}\nAmount of players={amount_of_players}\nAmount of starting tiles={amount_of_starting_tiles}")
print(f"max_tile_number={max_tile_number} ({max_tile_number * 2} tiles)\nPlayer classes={players_classes}")
print('\nRESULT:')
print(results_dict)
