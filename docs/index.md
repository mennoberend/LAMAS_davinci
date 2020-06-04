---
layout: default
---
# Introduction

In this project, we will analyse the game **Da Vinci Code**. Da Vinci Code is a game in which players each get a secret code and have to guess the code of the other players. However, by guessing something of another player, you can also give information about your own code. Therefore, the players have to think carefully not only about what they know about the other players' codes, but also about what they know about what the other players know about their codes, and about what the other players know about what they know about the other players' codes, and that is where epistemic logic comes in.

# Game Explanation

The game consists of twelve black and twelve white blocks each with a number from 0 to 11 on it (each number occurring once on a black and once on a white block), and one black and one white block with a '-' on it. From the back side, the thirteen white and thirteen black blocks are indistinguishable, it is only visible whether they are black or white. 


At the start of the game, each player takes a certain number of blocks (usually four or five, depending on the number of players), and places them on the table such that the player himself can see the numbers but the other players cannot. These blocks form this player's code. The blocks have to be put in ascending order according to the numbers on them, where the '-' can be placed at any place, and in case of equal numbers the black blocks come before the white blocks. Then in each turn the player whose turn it is takes one block from stack, looks what it is and then can guess one block of one other player's code, e.g. "Is this white block a 1?". The other player must answer truthfully. If the guess was incorrect, the other player says "no'' (he doesn't have to tell what was the actual number on the block), and the player on turn has to reveal the block that he has just taken from the stack and put it at the correct place open in his code. His turn is then over and the next player may take a block from stack and guess a block from another player. If the guess was correct, the other player has to reveal the concerning block and lay it open at the correct place in his code (i.e. the place where it was already standing). The player on turn may - if he wants - guess another block of a player (which can be the same player or another), the same procedure repeats until a wrong guess is made, which ends the turn. He can also choose to not make another guess and add the block he drew to his code in the correct place.


When the total code of a player is revealed, he is out and cannot guess the codes of the other players anymore. The game ends when the codes of all but one players are revealed, the remaining player is the winner.