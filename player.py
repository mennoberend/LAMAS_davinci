import random
import time
from math import exp
from tkinter import simpledialog

import numpy as np

from kripke_plotter import plot_local_kripke_model
from possible_worlds import GameState, possible_worlds
from tile import Tile


def exponential_random_choice(a):
    sample_chances = np.array([exp(-idx) for idx in range(len(a))])
    sample_chances /= sum(sample_chances)
    return np.random.choice(a, p=sample_chances)


class Player:
    def __init__(self, starting_tiles, name):
        self.tiles = sorted(starting_tiles)
        self.name = name
        self.impossible_tiles = None
        self.impossible_worlds = []

    def game_str(self):
        return f"Player {self.name}: {' '.join(t.game_str() for t in self.tiles)}"

    def play_round(self, game, view=None):
        drawn_tile = game.take_tile_from_table()

        # Make first guess
        if not self.guess_wrapper(game, drawn_tile, is_optional=False, view=view):
            return

        # Optionally make more guesses
        while True:
            if game.has_ended():
                return
            if view:
                view.canvas.draw_game(game)
                time.sleep(.5)
            if not self.guess_wrapper(game, drawn_tile, is_optional=True, view=view):
                return

    def guess_wrapper(self, game, drawn_tile, is_optional=False, view=None):
        # Make the guess
        chosen_player, tile_idx, guessed_tile = self.make_guess(game, drawn_tile, is_optional=is_optional, view=view)

        # If it was a optional guess, the agent can skip and he will get an extra tile
        if is_optional and chosen_player is None:
            if drawn_tile is not None:
                self.add_tile(drawn_tile)
            return False

        # Print the guess
        if view:
            view.canvas.text.append(
                f"Player {self.name} guesses that tile {tile_idx + 1} of Player {chosen_player.name} is {guessed_tile}"
            )

        # Check if the guess was correct, if the drawn tile is added visible to the other players
        correct = chosen_player.handle_guess(tile_idx, guessed_tile)
        if not correct:
            if drawn_tile is not None:
                drawn_tile.become_visible()
                self.add_tile(drawn_tile)

        # Update the players knowledge
        for player in game.players:
            player.add_knowledge(guessing_player=self, chosen_player=chosen_player, tile_idx=tile_idx,
                                 guessed_tile=guessed_tile, correct=correct, game=game)

        return correct

    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        raise NotImplementedError("Please implement this function in a child class")

    def all_known_tiles(self, game):
        ret = []
        for player in game.players:
            for tile in player.tiles:
                if tile.visible:
                    ret.append(tile)
        return set(ret)

    def handle_guess(self, tile_idx, guess):
        correct = self.tiles[tile_idx] == guess
        if correct:
            self.tiles[tile_idx].become_visible()
        return correct

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"Player {self.name}"

    def add_tile(self, tile):
        self.tiles.append(tile)
        self.tiles.sort()

    def get_local_game_state(self, game):
        # Build the game state
        player_tiles = []
        for player in game.players:
            if player.name == self.name:
                player_tiles.append([str(t) for t in player.tiles])
            else:
                player_tiles.append([t.game_str() for t in player.tiles])


        return GameState(player_tiles, self.impossible_tiles, max_tile_number=game.max_tile_number)

    def plot_local_kripke_model(self, game):
        game_state = self.get_local_game_state(game)
        # Calculate possible worlds
        all_possible_worlds = possible_worlds(game_state)

        # Determine extra relations
        color_group_pairs = []
        for color, player in zip(['red', 'green', 'blue', 'purple'], [p for p in game.players]):
            if player.name == self.name:
                continue
            color_group_pairs.append((color, self.groups_for_player(game, game.players[player.name], game_state,
                                                                    all_possible_worlds)))

        # Plot the kripke model
        real_world = [str(t) for player in game.players for t in player.tiles]
        plot_local_kripke_model(game_state, all_possible_worlds, real_world=real_world, player_idx=self.name,
                                color_group_pairs=color_group_pairs)

    def groups_for_player(self, game, player, game_state, all_possible_worlds):
        player_idx = game.players.index(player)
        player_tile_idxs = game_state.flat_idxs_of_player(player_idx)
        player_start_idx, player_end_idx = player_tile_idxs[0], player_tile_idxs[-1]

        groups = {}
        for world in all_possible_worlds:
            guessing_players_hand = ''.join(map(str, world[player_start_idx:player_end_idx]))
            if guessing_players_hand in groups:
                groups[guessing_players_hand].append(world)
            else:
                groups[guessing_players_hand] = [world]
        groups = list(groups.values())
        return groups

    def add_knowledge(self, guessing_player, chosen_player, tile_idx, guessed_tile, correct, game):
        # Setup the arrays to store the knowledge in
        game_state = self.get_local_game_state(game)
        amount_of_player_tiles = len(game_state.flat_player_tiles)
        if self.impossible_tiles is None or amount_of_player_tiles != len(self.impossible_tiles):
            self.impossible_tiles = [[] for _ in range(amount_of_player_tiles)]

        # Calculate some idxs belonging to relevant tiles
        guessing_player_idx = game.players.index(guessing_player)
        chosen_player_idx = game.players.index(chosen_player)
        guessing_player_tile_idxs = game_state.flat_idxs_of_player(guessing_player_idx)
        guessed_tile_flat_idx = game_state.player_and_tile_idx_to_flat_idx(chosen_player_idx, tile_idx)

        if correct:
            return

        # Guessing player can never have the guessed_tile
        for flat_idx in guessing_player_tile_idxs:
            self.impossible_tiles[flat_idx].append(guessed_tile)

        # The tile that was guessed cant be the guessed tile, since the guess was wrong
        self.impossible_tiles[guessed_tile_flat_idx].append(guessed_tile)

        # HARD PART

        # calculate possible worlds
        all_possible_worlds = possible_worlds(game_state)

        # Group worlds were the guessing agents hand is that same.
        groups = self.groups_for_player(game, guessing_player, game_state, all_possible_worlds)

        # if the guessed tile is not in the group we remove all worlds in the group
        for group in groups:
            # The guessed tile is not considered to be possible at the guessed location by the guessing agent
            if not any(world[guessed_tile_flat_idx] == guessed_tile for world in group):
                self.impossible_worlds.extend(map(lambda w: ''.join(map(str, w)), group))




class SimpleRandomPlayer(Player):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        if is_optional:
            return None, None, None
        possible_tiles = list(set(Tile.complete_set(max_number=game.max_tile_number)) - self.all_known_tiles(game) - {drawn_tile})

        # Try to get the player with the most invisible tiles
        chosen_player = sorted([p for p in game.players if p.name != self.name],
                               key=lambda p: len([t for t in p.tiles if not t.visible]),
                               reverse=True)[0]

        # Either choose high or low tile according to invisible tiles of the chosen player
        half_tiles_idx = len(chosen_player.tiles) // 2

        if len([t for t in chosen_player.tiles[:half_tiles_idx] if not t.visible]) > \
                len([t for t in chosen_player.tiles[half_tiles_idx:] if not t.visible]):
            # Choose a low possible tile
            tile_idx, chosen_tile = sorted(list(enumerate(chosen_player.tiles)), key=lambda p: (p[1].visible, p[0]))[0]
            guess = exponential_random_choice(sorted([t for t in possible_tiles if t.color == chosen_tile.color]))
        else:
            # Choose a high possible tile
            tile_idx, chosen_tile = sorted(list(enumerate(chosen_player.tiles)), key=lambda p: (p[1].visible, -p[0]))[0]
            guess = exponential_random_choice(
                sorted([t for t in possible_tiles if t.color == chosen_tile.color], reverse=True)
            )

        return chosen_player, tile_idx, guess


class HumanControlledPlayer(Player):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        if view:
            view.canvas.draw_game(game, drawn_tile=drawn_tile)

        # Choose a player
        prompt = "\nOf which player you want to guess a tile?" + ("\nType -1 to not guess" if is_optional else "")
        player_name = int(self.save_prompt(prompt,
                                           list({str(p.name) for p in game.players} - {str(self.name)}) + ['-1'],
                                           view.master))
        if is_optional and player_name == -1:
            return None, None, None
        chosen_player = [p for p in game.players if p.name == player_name][0]

        # Choose a tile idx
        prompt = "\nWhat is the idx of the tile? (Starting at 1)"
        tile_idx = int(self.save_prompt(prompt, [str(idx + 1) for idx in range(len(chosen_player.tiles))], view.master)) - 1

        # Choose the tile
        prompt = "\nWhat tile do you think the player has. (Enter as b1 or w6)"
        guess = Tile.from_string(self.save_prompt(prompt, [str(t) for t in Tile.complete_set(game.max_tile_number)], view.master))

        return chosen_player, tile_idx, guess

    @staticmethod
    def save_prompt(prompt, allowed_responses=None, application_window=None):
        if application_window is None:
            ret = input(prompt)
        else:
            ret = simpledialog.askstring("Input", prompt, parent=application_window)

        while allowed_responses and ret not in allowed_responses:
            if application_window is None:
                print('Your response is not allowed, please retry...')
                ret = input(prompt)
            else:
                ret = simpledialog.askstring("Input",
                                             'Your response is not allowed, please retry...\n' + prompt,
                                             parent=application_window)
        return ret


class LogicalPlayer(Player):
    def kripke_options_per_tile(self, game_state, all_possible_worlds):
        options_per_tile = [[] for _ in all_possible_worlds[0]]

        known_tiles = [True if '*' not in t else False for t in game_state.flat_player_tiles]

        for world in all_possible_worlds:
            for tile_idx, is_known in zip(range(len(world)), known_tiles):
                if not is_known:
                    options_per_tile[tile_idx].append(world[tile_idx])

        return options_per_tile

    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        game_state = self.get_local_game_state(game)
        all_possible_worlds = possible_worlds(game_state)

        if is_optional and len(all_possible_worlds) > 1:
            return None, None, None

        options_per_tile = self.kripke_options_per_tile(game_state, all_possible_worlds)
        # Get the tile with the most options
        flat_tile_idx = np.argmax([len(np.unique(tile)) for tile in options_per_tile])

        # Randomly choose a tile from from the option, options that are true in more world therefore have a higher
        # chance of being picked
        guess = random.choice(options_per_tile[flat_tile_idx])
        player_idx, tile_idx = game_state.flat_idx_to_player_and_tile_idx(flat_tile_idx)
        chosen_player = game.players[player_idx]

        return chosen_player, tile_idx, guess


class LogicalPlayerMinimiseOthers(LogicalPlayer):

    def all_groups_for_all_player(self, game, game_state, all_possible_worlds):
        groups = []
        for player in [p for p in game.players if p.name != self.name]:
            groups.extend(self.groups_for_player(game, player, game_state, all_possible_worlds))
        return groups

    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        game_state = self.get_local_game_state(game)
        all_possible_worlds = possible_worlds(game_state)

        if is_optional and len(all_possible_worlds) > 1:
            return None, None, None

        options_per_tile = self.kripke_options_per_tile(game_state, all_possible_worlds)
        unique_options_per_tile = [np.unique(tile) for tile in options_per_tile]

        groups_of_possible_worlds_for_different_players = self.all_groups_for_all_player(game, game_state,
                                                                                        all_possible_worlds)

        best_flat_tile_idx, best_option = None, None
        highest_avg_group_size_after_guess = 0
        # Try out all possible options for this agent
        for flat_tile_idx, tile in enumerate(unique_options_per_tile):
            for option in tile:
                # Suppose the guess is right, we calculate the new group sizes for the other players
                filtered_groups = [[1 for w in group if w[flat_tile_idx] == option] for group in groups_of_possible_worlds_for_different_players]
                grp_size_after_guess = np.average(list(map(len, filtered_groups)))

                # And take the guess that keeps the avg group size the highest
                if grp_size_after_guess >= highest_avg_group_size_after_guess:
                    best_flat_tile_idx = flat_tile_idx
                    best_option = option
                    highest_avg_group_size_after_guess = grp_size_after_guess

        player_idx, tile_idx = game_state.flat_idx_to_player_and_tile_idx(best_flat_tile_idx)
        return game.players[player_idx], tile_idx, best_option

class LogicalPlayerMaximizeSelf(LogicalPlayer):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        game_state = self.get_local_game_state(game)
        all_possible_worlds = possible_worlds(game_state)

        if is_optional and len(all_possible_worlds) > 1:
            return None, None, None

        options_per_tile = self.kripke_options_per_tile(game_state, all_possible_worlds)
        unique_options_per_tile = [np.unique(tile) for tile in options_per_tile]

        best_flat_tile_idx, best_option = None, None
        minimum_amount_of_worlds = len(all_possible_worlds)
        # Try out all possible options for this agent
        for flat_tile_idx, tile in enumerate(unique_options_per_tile):
            for option in tile:
                # Suppose the guess is right, we calculate new amount of possible worlds
                new_amount_of_possible_worlds = sum(1 for w in all_possible_worlds if w[flat_tile_idx] == option)

                # Suppose the guess is wrong
                new_amount_of_possible_worlds = (len(all_possible_worlds) - new_amount_of_possible_worlds + new_amount_of_possible_worlds) / 2

                # And take the guess that lowers the possible amount of worlds the most
                if new_amount_of_possible_worlds <= minimum_amount_of_worlds:
                    best_flat_tile_idx = flat_tile_idx
                    best_option = option
                    minimum_amount_of_worlds = new_amount_of_possible_worlds

        # print(f"Possible worlds go from {len(all_possible_worlds)} to {minimum_amount_of_worlds}")

        player_idx, tile_idx = game_state.flat_idx_to_player_and_tile_idx(best_flat_tile_idx)
        return game.players[player_idx], tile_idx, best_option

class BalancedLogicalPlayerMaximizeSelf(LogicalPlayer):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        game_state = self.get_local_game_state(game)
        all_possible_worlds = possible_worlds(game_state)

        if is_optional and len(all_possible_worlds) > 1:
            return None, None, None

        options_per_tile = self.kripke_options_per_tile(game_state, all_possible_worlds)
        unique_options_per_tile = [np.unique(tile) for tile in options_per_tile]

        best_flat_tile_idx, best_option = None, None
        minimum_amount_of_worlds = len(all_possible_worlds)
        # Try out all possible options for this agent
        for flat_tile_idx, tile in enumerate(unique_options_per_tile):
            for option in tile:
                
                # Possible worlds left if guess is right:
                new_amount_of_possible_worlds_if_right = sum(1 for w in all_possible_worlds if w[flat_tile_idx] == option)

                # Possible worlds left if guess is wrong:
                new_amount_of_possible_worlds_if_wrong = len(all_possible_worlds) - new_amount_of_possible_worlds_if_right

                # Chance the guess is right: 
                chance_right = new_amount_of_possible_worlds_if_right/(new_amount_of_possible_worlds_if_right+new_amount_of_possible_worlds_if_wrong)

                # Weighted average:
                new_amount_of_possible_worlds = chance_right * new_amount_of_possible_worlds_if_right + (1-chance_right) * new_amount_of_possible_worlds_if_wrong

                # And take the guess that lowers the possible amount of worlds the most
                if new_amount_of_possible_worlds <= minimum_amount_of_worlds:
                    best_flat_tile_idx = flat_tile_idx
                    best_option = option
                    minimum_amount_of_worlds = new_amount_of_possible_worlds

        # print(f"Possible worlds go from {len(all_possible_worlds)} to {minimum_amount_of_worlds}")

        player_idx, tile_idx = game_state.flat_idx_to_player_and_tile_idx(best_flat_tile_idx)
        return game.players[player_idx], tile_idx, best_option

