import networkx as nx
from nxpd import draw


def edge_already_exists(G, w1, w2, color):
    if G.has_edge(w1, w2):
        existing_edges = G.get_edge_data(w1, w2)
        if any([edge_data['color'] == color for edge_data in existing_edges.values()]):
            return True
    elif G.has_edge(w2, w1):
        existing_edges = G.get_edge_data(w2, w1)
        if any([edge_data['color'] == color for edge_data in existing_edges.values()]):
            return True
    return False


def build_graph(possible_worlds, G=None, color='red'):
    G = G or nx.MultiDiGraph()  # create empty graph

    if len(possible_worlds) > 25:
        print(f"There are {len(possible_worlds)} worlds in the Kripke model, which is to big to plot.")
        return G

    for world in possible_worlds:  # msg is python email.Message.Message object
        G.add_node(world, shape='square', penwidth=0, fontname="helvetica italic")
        other_worlds = [other for other in possible_worlds if other != world]
        for other in other_worlds:
            if not edge_already_exists(G, other, world, color):
                G.add_edge(world, other, color=color, dir='both')

    return G


def world_to_str(w, game_state):
    player_names = [f"p{i}" for i in range(len(game_state.player_tiles))]
    start_idx = 0
    world_string = '"'
    for players_amount_of_tiles, name in zip(map(len, game_state.player_tiles), player_names):
        world_string += name + ': {'
        world_string += ' '.join(str(t) for t in w[start_idx:start_idx + players_amount_of_tiles])
        world_string += '}\l\n'
        start_idx += players_amount_of_tiles
    return world_string + '"'


def combinations_to_str(game_state, all_combinations):
    return [world_to_str(w, game_state) for w in all_combinations]


def draw_graph(G, layout='circo'):
    G.graph['rankdir'] = 'LR'
    G.graph['dpi'] = 120
    G.graph['layout'] = layout
    if layout not in {'circo', 'dot'}:
        G.graph['ranksep'] = 3
        G.graph['nodesep'] = 2.5
    draw(G)


def add_hypothetical_relations_to_graph(G, game_state, color_group_pairs):
    for color, groups in color_group_pairs:
        for group in groups:
            group = combinations_to_str(game_state, group)
            for w in group:
                other_w = [other for other in group if w != other]
                for other in other_w:
                    if not edge_already_exists(G, other, w, color):
                        G.add_edge(w, other, color=color, dir='both')


def plot_local_kripke_model(game_state, all_combinations, player_idx, real_world=None, colors=None,
                            color_group_pairs=None):
    colors = colors or ['red', 'green', 'blue', 'purple']
    s = combinations_to_str(game_state, all_combinations)
    G = build_graph(s, color=colors[player_idx])
    if real_world and len(s) <= 25:
        real_world_string = world_to_str(real_world, game_state)
        G.add_node(real_world_string, shape='square', penwidth=2, fontname="helvetica italic")

    # Add relations for the other players
    if color_group_pairs and len(s) <= 25:  # when there is more than 25 worlds nothing gets plotted
        add_hypothetical_relations_to_graph(G, game_state, color_group_pairs)
    draw_graph(G)


def plot_global_kripke_model(state_combination_pairs, real_world=None, color_group_pairs=None):
    colors = ['red', 'green', 'blue', 'purple']
    G = nx.MultiDiGraph()
    for (game_state, all_combinations, color_group_pairs), color in zip(state_combination_pairs, colors):
        s = combinations_to_str(game_state, all_combinations)
        G = build_graph(s, G, color=color)

        # Add relations for the other players
        if color_group_pairs and len(s) <= 25:  # when there is more than 25 worlds nothing gets plotted
            add_hypothetical_relations_to_graph(G, game_state, color_group_pairs)

    if real_world:
        real_world_string = world_to_str(real_world, state_combination_pairs[0][0])
        G.add_node(real_world_string, shape='square', penwidth=2, fontname="helvetica italic")

    draw_graph(G, layout='sfdp')  # dot or sfdp are the best options
