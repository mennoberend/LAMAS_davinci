import sys
import tkinter as tk

from game import Game
from player import HumanControlledPlayer


class ExtendedCanvas(tk.Canvas):

    def __init__(self, player_width, player_height, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player_width = player_width
        self.player_height = player_height

        self.table_height = 2 * player_height
        self.table_width = player_width

        self.tile_height = int(self.player_height * .8)
        self.tile_width = self.player_width // 7
        self.tile_spacing = self.tile_width // 4

    def draw_rectangle(self, x, y, width, height, *args, **kwargs):
        self.create_rectangle(x, y, x + width, y+height, *args, **kwargs)

    def draw_tile(self, tile, location, force_visible=False):
        color = "black" if tile.color == 'b' else "white"
        self.draw_rectangle(location[0], location[1], self.tile_width, self.tile_height, fill=color)
        border_color = "yellow" if tile.visible else "darkgrey"
        self.draw_rectangle(location[0], location[1], self.tile_width, self.tile_height, outline=border_color)

        if tile.visible or force_visible:
            text_color = "white" if tile.color == 'b' else "black"
            self.create_text(location[0] + self.tile_width // 2, location[1] + self.tile_height // 2, fill=text_color,
                             font="Times 20 italic bold", text=str(tile.number))

    def draw_player(self, player, location):
        self.draw_rectangle(location[0], location[1], self.player_width, self.player_height, fill="gray")
        human_player_text = " (You)" if isinstance(player, HumanControlledPlayer) else ""
        self.create_text(location[0] + self.player_width // 2, location[1] + int(self.player_height * 1.5),
                         fill="darkblue", font="Times 20 italic bold", text=f"Player {player.name}{human_player_text}")

        tile_x = location[0] + self.tile_spacing
        tile_y = location[1] + self.player_height // 10

        for tile in player.tiles:
            self.draw_tile(tile, (tile_x, tile_y), force_visible=isinstance(player, HumanControlledPlayer))
            tile_x += self.tile_spacing + self.tile_width

    def draw_table(self, game):
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        table_x = canvas_width // 2 - self.table_width // 2
        table_y = canvas_height // 2 - self.table_height // 2
        self.draw_rectangle(table_x, table_y, self.table_width, self.table_height, fill="brown")

        # Played tiles
        tile_x = table_x + self.tile_spacing
        tile_y = table_y + self.table_height // 20
        for tile in game.tiles_open_on_table:
            self.draw_tile(tile, (tile_x, tile_y))
            tile_x += self.tile_spacing + self.tile_width

        # Unplayed tiles
        tile_x = table_x + int(self.table_width * 0.6)
        tile_y = table_y + self.table_height // 20 + self.table_height // 2
        for tile in game.unplayed_tiles:
            self.draw_tile(tile, (tile_x, tile_y))
            tile_x += self.tile_width // 3

    def draw_game(self, game, drawn_tile=None):
        self.delete("all")
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()

        player_locations = [
            (canvas_width // 2 - self.player_width // 2, self.player_height),
            (50, canvas_height // 2 - self.player_height // 2),
            (canvas_width - (self.player_width + 50), canvas_height // 2 - self.player_height // 2),
            (canvas_width // 2 - self.player_width // 2, canvas_height - (50 + self.player_height))
        ]

        self.draw_table(game)

        for player, loc in zip(game.players, player_locations):
            self.draw_player(player, loc)

        if drawn_tile:
            loc = (canvas_width - 100, 100)
            self.draw_tile(drawn_tile, loc, force_visible=True)
            self.create_text(loc[0], loc[1] + int(self.tile_height * 1.5), fill="darkblue",
                             font="Times 20 italic bold", text="Your drawn tile")


class View:

    def __init__(self, game, window_width=1080, window_height=720):
        self.window_width = window_width
        self.window_height = window_height
        self.game = game
        self.master = tk.Tk()
        self.master.bind('<Escape>', lambda _: self.close())
        self.master.bind('<space>', lambda _: self.next_round())
        self.canvas = ExtendedCanvas(master=self.master, width=window_width, height=window_height, player_width=250,
                                     player_height=75)
        self.canvas.pack()

        self.canvas.create_line(0, 0, 200, 100)

        self.master.update()
        self.canvas.draw_game(game)

        tk.mainloop()

    def next_round(self):
        game.play_round(view=self)
        print(game.game_str())
        self.canvas.draw_game(self.game)

    def close(self):
        self.master.withdraw()
        sys.exit()


if __name__ == "__main__":
    game = Game(
        amount_of_players=2,
        amount_of_starting_tiles=3,
        add_human_player=True
    )

    v = View(game)
