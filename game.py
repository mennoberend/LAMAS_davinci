import random

from kripke_plotter import plot_global_kripke_model
from player import SimpleRandomPlayer, HumanControlledPlayer
from possible_worlds import possible_worlds
from tile import Tile


class Game:
    def __init__(self, amount_of_players=3, amount_of_starting_tiles=4, max_tile_number=7,
                 player_class=SimpleRandomPlayer, add_human_player=False):
        self.max_tile_number = max_tile_number
        self.unplayed_tiles = Tile.complete_set(max_number=max_tile_number)
        random.shuffle(self.unplayed_tiles)

        self.players = []
        for name in range(amount_of_players):
            p = player_class(self.unplayed_tiles[:amount_of_starting_tiles], name)
            self.unplayed_tiles = self.unplayed_tiles[amount_of_starting_tiles:]
            self.players.append(p)

        if add_human_player:
            self.players.append(HumanControlledPlayer(self.unplayed_tiles[:amount_of_starting_tiles], len(self.players)))
            self.unplayed_tiles = self.unplayed_tiles[amount_of_starting_tiles:]

        self.current_player_idx = 0

    def game_str(self):
        return 'GAME STATE:\n' + \
               '\n'.join(p.game_str() for p in self.players) + \
               '\n'

    def play_round(self, view=None):
        self.players[self.current_player_idx].play_round(self, view=view)
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def take_tile_from_table(self):
        return self.unplayed_tiles.pop() if self.unplayed_tiles else None

    def plot_complete_kripke_model(self):
        state_combinations_pairs = []
        for player in self.players:
            game_state = player.get_local_game_state(self)
            # Calculate possible worlds
            all_possible_worlds = possible_worlds(game_state)
            state_combinations_pairs.append((game_state, all_possible_worlds))
        # Plot the kripke model
        plot_global_kripke_model(state_combinations_pairs)
