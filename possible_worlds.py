from tile import Tile
import itertools


class GameState:
    def __init__(self, player_tiles, tiles_open_on_table):
        self.player_tiles = player_tiles
        self.flat_player_tiles = [t for p in player_tiles for t in p]

        # End of every player in the flat player tiles
        cumulative_length = 0
        self.end_of_player_idxs = []
        for player_length in list(map(len, player_tiles)):
            self.end_of_player_idxs.append(cumulative_length + player_length)
            cumulative_length += player_length

        self.tiles_open_on_table = tiles_open_on_table

    @property
    def known_tiles(self):
        return [Tile.from_string(t) for t in self.flat_player_tiles if '*' not in t] + \
               [Tile.from_string(t) for t in self.tiles_open_on_table]

    @property
    def unknown_tiles(self):
        return list(set(Tile.complete_set(6)) - set(self.known_tiles))

    def __str__(self):
        s = "players tiles:\n"
        for p in player_tiles:
            s += ' '.join(p) + '\n'
        s += 'on table:\n' + ' '.join(self.tiles_open_on_table)
        s += '\nknown tiles: ' + ' '.join(map(str, self.known_tiles))
        s += '\nunknown tiles: ' + ' '.join(map(str, self.unknown_tiles))
        return s


def permutation_adheres_to_game_rules(added_tile, previous_tile, game_state, idx):
    if game_state.flat_player_tiles[idx][0] != added_tile.color:  # Make sure the color matches what we see
        return False

    if idx not in game_state.end_of_player_idxs and previous_tile is not None:
        if previous_tile > added_tile:
            return False

    return True


def perms(arr, game_state, idx=0, previous_tile=None):
    # We reached the required length
    if idx == len(game_state.flat_player_tiles) - 1:
        if '*' in game_state.flat_player_tiles[idx]:
            return [[v] for v in arr
                    if permutation_adheres_to_game_rules(v, previous_tile, game_state, idx)]
        else:
            already_known_tile = Tile.from_string(game_state.flat_player_tiles[idx])
            if permutation_adheres_to_game_rules(already_known_tile, previous_tile, game_state, idx):
                return [[already_known_tile]]
            else:
                return []

    # The next tile is already known
    if '*' not in game_state.flat_player_tiles[idx]:
        already_known_tile = Tile.from_string(game_state.flat_player_tiles[idx])
        if permutation_adheres_to_game_rules(already_known_tile, previous_tile, game_state, idx):
            return [[already_known_tile] + p for p in perms(arr, game_state, idx + 1, already_known_tile)]
        else:  # If the known tile does not adhere to the game rules, something must be wrong in this permutation
            return []

    result = []
    for i, v in enumerate(arr):
        if permutation_adheres_to_game_rules(v, previous_tile, game_state, idx):
            result += [[v] + p for p in perms(arr[:i] + arr[i + 1:], game_state, idx + 1, v)]
    return result


def possible_worlds(game_state):
    # print(f"Our own blocks: {' '.join(map(str, own_tiles))}")
    print(f"Game state:\n{str(game_state)}")
    print(game_state.end_of_player_idxs)
    all_combinations = perms(game_state.unknown_tiles, game_state)

    print(f"There are {len(all_combinations)} possible worlds after using what we see from our opponents:")

    # for i, c in enumerate(all_combinations):
    #     print(f'World {i}')
    #     start_idx = 0
    #     for players_amount_of_tiles in map(len, game_state.player_tiles):
    #         print(' '.join(str(t) for t in c[start_idx:start_idx + players_amount_of_tiles]))
    #         start_idx += players_amount_of_tiles
    #     print()


if __name__ == "__main__":
    # own_tiles = list(map(lambda s: Tile.from_string(s), ['w1', 'b5', 'w5', 'w6']))
    # other_player_colors = [['b', 'b', 'w', 'w'], ['b', 'w', 'b', 'b']]
    player_tiles = [['w1', 'b5', 'w5', 'w6'], ['b*', 'b*', 'w*', 'w*'], ['b*', 'w*', 'b*', 'b*']]
    game_state = GameState(player_tiles, [])
    possible_worlds(game_state)


    # own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5', 'w6']))
    # other_player_colors = [['b', 'w', 'w', 'b'], ['w', 'b', 'w', 'w']]
    player_tiles = [['b1', 'b4', 'b5', 'w6'], ['b*', 'w*', 'w*', 'b*'], ['w*', 'b*', 'w*', 'w*']]
    game_state = GameState(player_tiles, [])
    possible_worlds(game_state)

    # own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5']))
    # other_player_colors = [['b', 'w', 'w'], ['w', 'b', 'w']]
    player_tiles = [['b1', 'b4', 'b5'], ['b*', 'w*', 'w*'], ['w*', 'b*', 'w*']]
    game_state = GameState(player_tiles, [])
    possible_worlds(game_state)

    # own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5', 'w6']))
    # other_player_colors = [['b', 'w', 'w', 'b']]
    player_tiles = [['b1', 'b4', 'b5', 'w6'], ['b*', 'w*', 'w*', 'b*']]
    game_state = GameState(player_tiles, [])
    possible_worlds(game_state)
