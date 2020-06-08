from math import exp
from tkinter import simpledialog

import numpy as np

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
        chosen_player, tile_idx, guessed_tile = self.make_guess(game, drawn_tile, is_optional=False,
                                                                view=view)
        correct = chosen_player.handle_guess(tile_idx, guessed_tile)
        if not correct:
            if drawn_tile is not None:
                game.put_open_on_table(drawn_tile)
            return

        # Optionally make more guesses
        while True:
            chosen_player, tile_idx, guessed_tile = self.make_guess(game, drawn_tile, is_optional=True,
                                                                    view=view)
            if chosen_player is None:
                break
            correct = chosen_player.handle_guess(tile_idx, guessed_tile)
            if not correct:
                if drawn_tile is not None:
                    game.put_open_on_table(drawn_tile)
                return

        if drawn_tile is not None:
            self.tiles.append(drawn_tile)
            self.tiles.sort()

    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        raise NotImplementedError("Please implement this function in a child class")

    def all_known_tiles(self, game):
        return set(self.tiles + game.tiles_open_on_table)

    def handle_guess(self, tile_idx, guess):
        correct = self.tiles[tile_idx] == guess
        if correct:
            self.tiles[tile_idx].become_visible()
        return correct

    def __eq__(self, other):
        return self.name == other.name


class SimpleRandomPlayer(Player):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        if is_optional:
            return None, None, None
        possible_tiles = list(set(Tile.complete_set()) - self.all_known_tiles(game) - {drawn_tile})

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

        print(f"\n***Player {self.name} guesses that tile {tile_idx + 1} of Player {chosen_player.name} is {guess}***\n")
        return chosen_player, tile_idx, guess


class HumanControlledPlayer(Player):
    def make_guess(self, game, drawn_tile, is_optional=False, view=None):
        print(f"\nYour tiles are: {' '.join(map(str, self.tiles))}")
        print(f"You just drew {drawn_tile}.")
        if view:
            view.canvas.draw_game(game, drawn_tile=drawn_tile)

        # Choose a player
        prompt = "\nOf which player you want to guess a tile?" + (" Type -1 to not guess" if is_optional else "")
        player_name = int(self.save_prompt(prompt,
                                           list({str(p.name) for p in game.players} - {str(self.name)}) + ['-1'],
                                           view.master))
        if is_optional and player_name == -1:
            return None, None, None
        chosen_player = [p for p in game.players if p.name == player_name][0]

        # Choose a tile idx
        prompt = "\nWhat is the idx of the tile? (Starting at 0)"
        tile_idx = int(self.save_prompt(prompt, [str(idx) for idx in range(len(chosen_player.tiles))], view.master))

        # Choose the tile
        prompt = "\nWhat tile do you think the player has. (Enter as b1 or w6)"
        guess = Tile.from_string(self.save_prompt(prompt, [str(t) for t in Tile.complete_set()], view.master))
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
