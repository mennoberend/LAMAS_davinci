import networkx as nx
from nxpd import draw


def build_graph(possible_worlds, G=None, color='red'):
    G = G or nx.MultiDiGraph()  # create empty graph

    if len(possible_worlds) > 25:
        print("To many worlds unable to make plot:(")
        return G

    for world in possible_worlds:  # msg is python email.Message.Message object
        G.add_node(world, shape='square', penwidth=0, fontname="helvetica italic")
        other_worlds = [other for other in possible_worlds if other != world]
        for other in other_worlds:
            if G.has_edge(other, world):
                existing_edges = G.get_edge_data(other, world)
                if any([edge_data['color'] == color for edge_data in existing_edges.values()]):
                    continue
            G.add_edge(world, other, color=color, dir='both')

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


def draw_graph(G, layout='circo'):
    G.graph['rankdir'] = 'LR'
    G.graph['dpi'] = 120
    G.graph['layout'] = layout
    if layout not in {'circo', 'dot'}:
        G.graph['ranksep'] = 3
        G.graph['nodesep'] = 2.5
    draw(G)


def plot_local_kripke_model(game_state, all_combinations, color='red'):
    s = combinations_to_str(game_state, all_combinations)
    G = build_graph(s, color=color)
    draw_graph(G)


def plot_global_kripke_model(state_combination_pairs):
    colors = ['red', 'green', 'blue', 'purple']
    G = nx.MultiDiGraph()
    for (game_state, all_combinations), color in zip(state_combination_pairs, colors):
        s = combinations_to_str(game_state, all_combinations)
        G = build_graph(s, G, color=color)
    draw_graph(G, layout='sfdp')  # dot or sfdp are the best options
