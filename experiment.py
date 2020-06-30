import argparse
import multiprocessing

import random
from copy import deepcopy

from game import Game
from player import AggressiveLogicalPlayer, DefensiveLogicalPlayer


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
    if opt.verbose:
        print(f"Done with {i}")
    return type(game.winner()).__name__

# Parameter settings
parser = argparse.ArgumentParser()
parser.add_argument('--verbose', action='store_true', default=False,
                    help='Whether you want to  print every succeeded game')
parser.add_argument('--amount_of_players', type=int, default=4,
                    help='How many players(the user excluded) are in the game [Default: 4](Maximum 4)')
parser.add_argument('--amount_of_starting_tiles', type=int,
                    default=4, help='The amount of tiles every player starts with [Default: 4]')
parser.add_argument('--max_tile_number', type=int, default=8,
                    help='What is the highest number on a tile, if the total amount of tiles will be double this number')
parser.add_argument('--n', type=int, default=1000,
                    help='Amount of simulations')
opt = parser.parse_args()

n = opt.n
amount_of_players = opt.amount_of_players
amount_of_starting_tiles = opt.amount_of_starting_tiles
max_tile_number = opt.max_tile_number

players_classes = [AggressiveLogicalPlayer, AggressiveLogicalPlayer, DefensiveLogicalPlayer, DefensiveLogicalPlayer]


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

print('\nPARAMETERS:')
print(f"N={n}\nAmount of players={amount_of_players}\nAmount of starting tiles={amount_of_starting_tiles}")
print(f"max_tile_number={max_tile_number} ({max_tile_number * 2} tiles)\nPlayer classes={players_classes}")
print('\nRESULT:')
print(results_dict)
print()
