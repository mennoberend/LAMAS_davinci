import itertools

import matplotlib.pyplot as plt
import networkx as nx
from nxpd import draw


# unix mailbox recipe
# see https://docs.python.org/3/library/mailbox.html


def mbox_graph():
    G = nx.MultiDiGraph()  # create empty graph
    G.graph['rankdir'] = 'LR'
    G.graph['dpi'] = 120

    perms = [''.join(perm) + "\n123" for perm in itertools.permutations('abc')]
    print(perms)
    # parse each messages and build graph
    for i in perms:  # msg is python email.Message.Message object
        G.add_node(i, shape='square', pencolor='white', penwidth=0)
        to = [other for other in perms if other != i]
        for other in to:
            if not G.has_edge(other, i):
                G.add_edge(i, other, color='red', dir='both')

    return G


if __name__ == '__main__':

    G = mbox_graph()

    # print edges with message subject
    # for (u, v, d) in G.edges(data=True):
    #     print("From: %s To: %s Subject: %s" % (u, v, d['message']["Subject"]))

    pos = nx.spring_layout(G, iterations=10)

    edges = G.edges()
    colors = nx.get_edge_attributes(G, 'color').values()
    # nx.draw(G, pos, edges=edges, edge_color=colors, node_size=0, alpha=0.4, font_size=16, with_labels=True)
    draw(G)
    # nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    # nx.draw_networkx_edges(G, pos,
    #                        edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
    #                        width=1, alpha=0.5, edge_color='r')
    plt.show()