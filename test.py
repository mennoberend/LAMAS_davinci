from game import Game


def main():
    human_player_in_the_game = False
    game = Game(
        amount_of_players=3,
        amount_of_starting_tiles=4,
        add_human_player=human_player_in_the_game
    )

    print(game.game_str())
    prompt = 'Press enter to continue to the next round(or type anything to exit)'
    user_input = input(prompt)

    while user_input == '':
        if human_player_in_the_game:
            print('\n' * 20)
        print(game.game_str())
        game.play_round()
        user_input = input(prompt)


if __name__ == "__main__":
    main()
