class Tile:
    def __init__(self, color, number):
        assert color == 'b' or color == 'w'
        self.color = color
        self.number = number
        self.visible = False

    def become_visible(self):
        self.visible = True

    @staticmethod
    def complete_set():
        max_number = 6
        return [Tile('b', i) for i in range(1, max_number + 1)] + [Tile('w', i) for i in range(1, max_number + 1)]

    def game_str(self):
        return f"{self.color}{self.number if self.visible else '*'}"

    @staticmethod
    def from_string(s):
        return Tile(s[:1], int(s[1:]))

    def __lt__(self, other):
        if self.number == other.number:
            return self.color == 'b'
        return self.number < other.number

    def __str__(self):
        return f"{self.color}{self.number}"

    def __eq__(self, other):
        return self.color == other.color and self.number == other.number

    def __hash__(self):
        return hash((self.color, self.number))
