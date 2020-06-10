import networkx as nx
from nxpd import draw


def build_graph(possible_worlds):
    G = nx.MultiDiGraph()  # create empty graph
    for world in possible_worlds:  # msg is python email.Message.Message object
        G.add_node(world, shape='square', penwidth=0, fontname="helvetica italic")
        other_worlds = [other for other in possible_worlds if other != world]
        for other in other_worlds:
            if not G.has_edge(other, world):
                G.add_edge(world, other, color='red', dir='both')

    return G


def combinations_to_str(game_state, all_combinations):
    player_names = [f"p{i}" for i in range(len(game_state.player_tiles))]
    ret = []
    for c in all_combinations:
        start_idx = 0
        world_string = '"'
        for players_amount_of_tiles, name in zip(map(len, game_state.player_tiles), player_names):
            world_string += name + ': {'
            world_string += ' '.join(str(t) for t in c[start_idx:start_idx + players_amount_of_tiles])
            world_string += '}\l\n'
            start_idx += players_amount_of_tiles
        ret.append(world_string + '"')
    return ret


def plot_kripke_model(game_state, all_combinations):
    s = combinations_to_str(game_state, all_combinations)

    G = build_graph(s)
    G.graph['rankdir'] = 'LR'
    G.graph['dpi'] = 120
    G.graph['layout'] = 'circo'
    draw(G)
