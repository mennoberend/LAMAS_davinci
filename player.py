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
            view.canvas.draw_game(game)  # Doesn't work
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
        view.canvas.text.append(
            f"Player {self.name} guesses that tile {tile_idx + 1} of Player {chosen_player.name} is {guessed_tile}"
        )

        # Check if the guess was correct, if the drawn tile is added visible to the other players
        correct = chosen_player.handle_guess(tile_idx, guessed_tile)
        if not correct:
            if drawn_tile is not None:
                drawn_tile.become_visible()
                self.add_tile(drawn_tile)

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
        return GameState(player_tiles, max_tile_number=game.max_tile_number)

    def plot_local_kripke_model(self, game):
        game_state = self.get_local_game_state(game)
        # Calculate possible worlds
        all_possible_worlds = possible_worlds(game_state)
        # Plot the kripke model
        plot_local_kripke_model(game_state, all_possible_worlds, ['red', 'green', 'blue', 'purple'][self.name])


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

        # print('\n'.join(map(lambda t: str(list(map(str, t))), options_per_tile)))
        # print(flat_tile_idx)
        return chosen_player, tile_idx, guess