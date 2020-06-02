from LAMAS_davinci.game import Game


def main():
    human_player_in_the_game = True
    game = Game(amount_of_players=1, add_human_player=human_player_in_the_game)

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
