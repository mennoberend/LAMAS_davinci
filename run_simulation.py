import argparse

from game import Game
from player import DefensiveLogicalPlayer, AggressiveLogicalPlayer
from view import View

parser = argparse.ArgumentParser()

parser.add_argument('--add_human_player', action='store_true',
                    help='Whether you want to  [Default: False]')

parser.add_argument('--amount_of_players', type=int, default=4,
                    help='How many players(the user excluded) are in the game [Default: 4](Maximum 4)')
parser.add_argument('--amount_of_starting_tiles', type=int,
                    default=4, help='The amount of tiles every player starts with [Default: 4]')
parser.add_argument('--max_tile_number', type=int, default=8,
                    help='What is the highest number on a tile, if the total amount of tiles will be double this number')
parser.add_argument('--strategy', default='mixed', help="Pick the opponents strategy, either defensive, aggressive or "
                                                        "mixed")

opt = parser.parse_args()

if opt.strategy == 'mixed':
    player_classes = [DefensiveLogicalPlayer, AggressiveLogicalPlayer, DefensiveLogicalPlayer, AggressiveLogicalPlayer]
elif opt.strategy == 'aggressive':
    player_classes = [AggressiveLogicalPlayer] * 4
else:
    player_classes = [DefensiveLogicalPlayer] * 4

game = Game(
    amount_of_players=opt.amount_of_players,
    amount_of_starting_tiles=opt.amount_of_starting_tiles,
    max_tile_number=opt.max_tile_number,
    add_human_player=opt.add_human_player,
    player_classes=player_classes
)

v = View(game)
