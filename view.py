import sys
import tkinter as tk

from game import Game
from player import HumanControlledPlayer, LogicalPlayer, LogicalPlayerMaximizeSelf


class ExtendedCanvas(tk.Canvas):

    def __init__(self, player_width, player_height, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.player_width = player_width
        self.player_height = player_height

        self.table_height = 3 * player_height
        self.table_width = int(0.75 * player_width)

        self.tile_height = int(self.player_height * .8)
        self.tile_width = self.player_width // 9
        self.tile_spacing = self.tile_width // 4

        self.text = ["Press space to continue to the next turn.", "Press escape to leave the game."]

    def draw_button(self, location, text, action, color):
        button1 = tk.Button(self, text=text, command=action, anchor=tk.W)
        button1.configure(width=15, activebackground=color, relief=tk.FLAT)  # "#33B5E5"
        self.create_window(location[0], location[1], anchor=tk.NW, window=button1)

    def draw_rectangle(self, x, y, width, height, *args, **kwargs):
        self.create_rectangle(x, y, x + width, y + height, *args, **kwargs)

    def draw_tile(self, tile, location, force_visible=False):
        color = "black" if tile.color == 'b' else "white"
        self.draw_rectangle(location[0], location[1], self.tile_width, self.tile_height, fill=color)
        border_color = "yellow" if tile.visible else "darkgrey"
        self.draw_rectangle(location[0], location[1], self.tile_width, self.tile_height, outline=border_color)

        if tile.visible or force_visible:
            text_color = "white" if tile.color == 'b' else "black"
            self.create_text(location[0] + self.tile_width // 2, location[1] + self.tile_height // 2, fill=text_color,
                             font="Times 20 italic bold", text=str(tile.number))

    def draw_player(self, player, location, game, color):
        self.draw_rectangle(location[0], location[1], self.player_width, self.player_height, fill="gray")
        human_player_text = " (You)" if isinstance(player, HumanControlledPlayer) else ""
        self.create_text(location[0] + self.player_width // 2, location[1] + int(self.player_height * 1.5),
                         fill=color, font="Times 20 bold", text=f"Player {player.name}{human_player_text}")

        tile_x = location[0] + self.tile_spacing
        tile_y = location[1] + self.player_height // 10

        for idx, tile in enumerate(player.tiles):
            self.draw_tile(tile, (tile_x, tile_y), force_visible=isinstance(player, HumanControlledPlayer))
            self.create_text(tile_x + self.tile_width // 2, tile_y + int(self.tile_height * 1.3),
                             fill="black", font=f"Times 7", text=str(idx + 1))
            tile_x += self.tile_spacing + self.tile_width

        self.draw_button((location[0], location[1] - 35), "Local Kripke Model",
                         lambda: player.plot_local_kripke_model(game), color)

    def draw_table(self, game):
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()
        table_x = canvas_width // 2 - self.table_width // 2
        table_y = canvas_height // 2 - self.table_height // 2
        self.draw_rectangle(table_x, table_y, self.table_width, self.table_height, fill="brown")

        # Unplayed tiles
        tile_x = table_x + self.table_width // 2 - self.tile_width // 2
        tile_y = table_y + self.table_height // 2 - self.tile_height // 2
        for tile in game.unplayed_tiles:
            self.draw_tile(tile, (tile_x, tile_y))
            tile_x += self.tile_width // 3

    def draw_text_screen(self, loc, size):
        self.draw_rectangle(loc[0], loc[1], size[0], size[1], fill="white")
        self.draw_rectangle(loc[0], loc[1], size[0], size[1], outline="darkgray")
        font_size = 14
        line_spacing = font_size // 2
        amount_of_visible_lines = size[1] // (font_size + line_spacing)
        line_x = loc[0] + 5
        line_y = loc[1] + size[1] - (5 + font_size)
        for line in reversed(self.text[-amount_of_visible_lines:]):
            self.create_text(line_x, line_y, fill="black", font=f"Times {font_size}", text=line, anchor='nw')
            line_y -= line_spacing + font_size

    def draw_game(self, game, drawn_tile=None):
        self.delete("all")  # Clean the screen
        canvas_width, canvas_height = self.winfo_width(), self.winfo_height()

        # Players
        player_locations = [
            (canvas_width // 2 - self.player_width // 2, self.player_height),
            (50, canvas_height // 2 - self.player_height // 2),
            (canvas_width - (self.player_width + 50), canvas_height // 2 - self.player_height // 2),
            (canvas_width // 2 - self.player_width // 4, canvas_height - (50 + self.player_height))
        ]
        player_colors = ['red', 'green', 'blue', 'purple']
        for player, loc, color in zip(game.players, player_locations, player_colors):
            self.draw_player(player, loc, game, color)

        # Table
        self.draw_table(game)

        # Optional tile that was just drawn
        if drawn_tile:
            loc = (canvas_width - 100, 100)
            self.draw_tile(drawn_tile, loc, force_visible=True)
            self.create_text(loc[0], loc[1] + int(self.tile_height * 1.5), fill="darkblue",
                             font="Times 20 italic bold", text="Your drawn tile")

        self.draw_text_screen((25, canvas_height - 200), (350, 175))

        self.draw_button((10, 10), "Global Kripke Model", lambda: game.plot_complete_kripke_model(), 'white')
        self.update()


class View:
    def __init__(self, game, window_width=1080, window_height=720):
        self.window_width = window_width
        self.window_height = window_height
        self.game = game
        self.master = tk.Tk()
        self.master.title("Da Vinci Code")
        self.master.bind('<Escape>', lambda _: self.close())
        self.master.bind('<space>', lambda _: self.next_round())
        self.canvas = ExtendedCanvas(master=self.master, width=window_width, height=window_height, player_width=350,
                                     player_height=75)
        self.canvas.pack()

        self.canvas.create_line(0, 0, 200, 100)

        self.master.update()

        self.canvas.text.append(f"It is Player {self.game.current_player_idx}'s turn!")
        self.canvas.draw_game(game)

        tk.mainloop()

    def next_round(self):
        self.game.play_round(view=self)
        if self.game.has_ended():
            self.canvas.text.append(f"{self.game.winner()} has won the game!")
        else:
            self.canvas.text.append(f"It is Player {self.game.current_player_idx}'s turn!")
        self.canvas.draw_game(self.game)

    def close(self):
        self.master.withdraw()
        sys.exit()


if __name__ == "__main__":
    game = Game(
        amount_of_players=3,
        amount_of_starting_tiles=4,
        max_tile_number=7,
        add_human_player=False,
        player_class=LogicalPlayerMaximizeSelf
    )

    v = View(game)
