from tile import Tile
import itertools


def permutation_adheres_to_game_rules(added_tile, previous_tile, other_player_colors, observation_string, idx):
    if observation_string[idx] != added_tile.color:  # Make sure the color matches what we see
        return False
    not_sorted_idxs = map(len, other_player_colors)
    if idx not in not_sorted_idxs and previous_tile is not None:
        if previous_tile > added_tile:
            return False
    return True


def perms(arr, other_player_colors, idx=0, previous_tile=None):
    observation_string = ''.join(''.join(p) for p in other_player_colors)
    # if len(arr) == 1:  # Base case 1, if we made all possible permutation with the supplied tiles
    #     if permutation_adheres_to_game_rules(v, previous_tile, other_player_colors, observation_string, idx):
    #         return [arr]
    if idx == len(observation_string) - 1:  # Base case, we are on the required length
        return [[v] for v in arr
                if permutation_adheres_to_game_rules(v, previous_tile, other_player_colors, observation_string, idx)]
    result = []
    for i, v in enumerate(arr):
        if permutation_adheres_to_game_rules(v, previous_tile, other_player_colors, observation_string, idx):
            result += [[v] + p for p in perms(arr[:i] + arr[i + 1:], other_player_colors, idx + 1, v)]
    return result


def sort_combination(combination, other_player_colors):
    sorted_combination = []
    for sort_group_size in map(len, other_player_colors):
        sorted_combination.extend(sorted(combination[:sort_group_size]))
        combination = combination[sort_group_size:]

    return sorted_combination


def possible_worlds(own_tiles, other_player_colors):
    print(f"Our own blocks: {' '.join(map(str, own_tiles))}")
    print(f"Opponent colors: {', '.join(''.join(p) for p in other_player_colors)}\n")
    unknown_tiles = list(set(Tile.complete_set(6)) - set(own_tiles))
    # all_combinations = list(itertools.permutations(unknown_tiles, sum(map(len, other_player_colors))))
    all_combinations = perms(unknown_tiles, other_player_colors)
    print(f"There are {len(all_combinations)} possible worlds without regarding any game rules.")

    # Remove duplicate worlds
    all_combinations = [sort_combination(combination, other_player_colors) for combination in all_combinations]
    all_combinations.sort()
    all_combinations = list(c for c, _ in itertools.groupby(all_combinations))
    print(f"There are {len(all_combinations)} possible worlds when removing duplicates through sorting.")

    # Remove worlds that dont match with the black and white we can see
    observation_string = ''.join(''.join(p) for p in other_player_colors)
    all_combinations = [c for c in all_combinations if ''.join(t.color for t in c) == observation_string]

    print(f"There are {len(all_combinations)} possible worlds after using what we see from our opponents:")
    # for i, c in enumerate(all_combinations):
    #     print(f'World {i}')
    #     start_idx = 0
    #     for players_amount_of_tiles in map(len, other_player_colors):
    #         print(' '.join(str(t) for t in c[start_idx:start_idx + players_amount_of_tiles]))
    #         start_idx += players_amount_of_tiles
    #     print()


if __name__ == "__main__":
    own_tiles = list(map(lambda s: Tile.from_string(s), ['w1', 'b5', 'w5', 'w6']))
    other_player_colors = [['b', 'b', 'w', 'w'], ['b', 'w', 'b', 'b']]
    possible_worlds(own_tiles, other_player_colors)

    own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5', 'w6']))
    other_player_colors = [['b', 'w', 'w', 'b'], ['w', 'b', 'w', 'w']]
    possible_worlds(own_tiles, other_player_colors)

    own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5']))
    other_player_colors = [['b', 'w', 'w'], ['w', 'b', 'w']]
    possible_worlds(own_tiles, other_player_colors)

    own_tiles = list(map(lambda s: Tile.from_string(s), ['b1', 'b4', 'b5', 'w6']))
    other_player_colors = [['b', 'w', 'w', 'b']]
    possible_worlds(own_tiles, other_player_colors)


