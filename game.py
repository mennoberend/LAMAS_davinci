import random

from kripke_plotter import plot_global_kripke_model
from player import SimpleRandomPlayer, HumanControlledPlayer, Player
from possible_worlds import possible_worlds
from tile import Tile


class Game:
    def __init__(self, amount_of_players=3, amount_of_starting_tiles=4, max_tile_number=7,
                 player_classes=SimpleRandomPlayer, add_human_player=False):
        if not isinstance(player_classes, list):
            player_classes = [player_classes] * amount_of_players

        self.max_tile_number = max_tile_number
        self.unplayed_tiles = Tile.complete_set(max_number=max_tile_number)

        # random.seed(9)
        random.shuffle(self.unplayed_tiles)

        self.players = []
        for name, player_class in zip(list(range(amount_of_players)), player_classes):
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
        if not self.has_ended():
            self.players[self.current_player_idx].play_round(self, view=view)
            self.next_player()

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
        # If the players tiles are all visible skip that player
        while all(t.visible for t in self.players[self.current_player_idx].tiles):
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def take_tile_from_table(self):
        return None
        # return self.unplayed_tiles.pop() if self.unplayed_tiles else None

    def plot_complete_kripke_model(self):
        state_combinations_pairs = []

        for player in self.players:
            game_state = player.get_local_game_state(self)
            # Calculate possible worlds
            all_possible_worlds = possible_worlds(game_state)

            color_group_pairs = []
            # Get hypothetical relations
            for color, other_player in zip(['red', 'green', 'blue', 'purple'], [p for p in self.players]):
                if other_player.name == player.name:
                    continue
                color_group_pairs.append((color, player.groups_for_player(self,
                                                                          self.players[other_player.name], game_state,
                                                                          all_possible_worlds)))
            state_combinations_pairs.append((game_state, all_possible_worlds, color_group_pairs))


        # Plot the kripke model
        real_world = [str(t) for player in self.players for t in player.tiles]
        plot_global_kripke_model(state_combinations_pairs, real_world=real_world)

    def winner(self):
        for player in self.players:
            if all([all([t.visible for t in p.tiles]) for p in self.players if p.name != player.name]):
                return player
        return None

    def has_ended(self):
        return self.winner() is not None
