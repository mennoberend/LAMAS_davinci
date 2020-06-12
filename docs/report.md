Introduction {#introduction .unnumbered}
============

In this project, we will analyse the game 'Da Vinci Code'. Da Vinci Code
is a game in which players each get a secret code and have to guess the
code of the other players. However, by guessing something of another
player, you can also give information about your own code. Therefore,
the players have to think carefully not only about what they know about
the other players' codes, but also about what they know about what the
other players know about their codes, and about what the other players
know about what they know about the other players' codes, and that is
where epistemic logic comes in.

Game explanation {#game-explanation .unnumbered}
----------------

The game consists of twelve black and twelve white blocks each with a
number from 0 to 11 on it (each number occurring once on a black and
once on a white block), and one black and one white block with a '-' on
it. From the back side, the thirteen white and thirteen black blocks are
indistinguishable, it is only visible whether they are black or white.\
At the start of the game, each player takes a certain number of blocks
(usually four or five, depending on the number of players), and places
them on the table such that the player himself can see the numbers but
the other players cannot. These blocks form this player's code. The
blocks have to be put in ascending order according to the numbers on
them, where the '-' can be placed at any place, and in case of equal
numbers the black blocks come before the white blocks. Then in each turn
the player whose turn it is takes one block from stack, looks what it is
and then can guess one block of one other player's code, e.g. "Is this
white block a 1?\". The other player must answer truthfully. If the
guess was incorrect, the other player says "no" (he doesn't have to tell
what was the actual number on the block), and the player on turn has to
reveal the block that he has just taken from the stack and put it at the
correct place open in his code. His turn is then over and the next
player may take a block from stack and guess a block from another
player. If the guess was correct, the other player has to reveal the
concerning block and lay it open at the correct place in his code (i.e.
the place where it was already standing). The player on turn may - if he
wants - guess another block of a player (which can be the same player or
another), the same procedure repeats until a wrong guess is made, which
ends the turn. He can also choose to not make another guess and add the
block he drew to his code in the correct place.\
When the total code of a player is revealed, he is out and cannot guess
the codes of the other players anymore. The game ends when the codes of
all but one players are revealed, the remaining player is the winner.

Example with higher order knowledge {#example-with-higher-order-knowledge .unnumbered}
-----------------------------------

We will give an example to show where higher order knowledge might be
needed in the game. Suppose that in a certain state of the game player
$a$ has the code \[5,6,8,11\], and player $b$ has the code \[4,9,10,-\],
all in black blocks (to make in an easy example). From player $a$, the 5
and the 8 are revealed and from player $b$, the 4, the 10 and the '-'
are revealed, so the visible codes are \[5,?,8,?\] for player $a$ and
\[4,?,10,-\] for player $b$. It is $b$'s turn. Player $b$ can guess the
hidden block of player $a$ between the 5 and the 8, he has 50 % chance
of guessing correct because it can be either a 6 or a 7. However, if
player $b$ does guess this block and guesses it wrong, all players know
that he didn't know whether it was a 6 or 7, so they all know that
player $b$ does not have the 6 or the 7 himself (for if he would have
one of them, he would know the number on the block of player $a$). Then
they can deduce that the hidden block of player $b$ himself must be a 9,
because except for 6 and 7 the only numbers between 4 and 10 are 5 and
8, which already lay open in player $a$'s code. Hence, if player $b$
guesses that the hidden block of player $a$ is a 7, he has by doing so
given away his own code and can in the next turn of any player be out.

Models {#models .unnumbered}
======

Let $A$ be the set of players, with $|A|=m$ and $N$ the number of blocks
each player has at the beginning of the game. We will use the system
$S_{5(m)}$ to form a Kripke model of a simplified version of the game.
In this simplified version, there are only 12 blocks, namely the blocks
1-6 of both colors, there are 3 players, so $m=3$ and each player has 4
blocks so $N=4$. We also assume that players do not ask for numbers that
are in their own code or of which they for some other reason know that
cannot be correct (i.e. they will only make guesses that *can* be true).
A Kripke model $M$ is defined as $M=(S,\pi, R_1, ..., R_m)$ with

1.  $S$ a non-empty set of states,

2.  $\pi : S\rightarrow (P\rightarrow \{t,f\})$ a truth assignment for
    each propositional atom in each state,

3.  $R_i \subseteq S\times S$ $(i=1, ..., m)$ a set of accessibility
    relations.

Let us denote the white blocks as $W=\{w1, ..., w6\}$ and the black
blocks as $B=\{b1, ..., b6\}$.\

Initial model {#initial-model .unnumbered}
-------------

We can formalise the game as a Kripke model $M=(S,\pi, R_a, R_b, R_c)$.
We will start by creating a model of the beginning of the game. The
states are defined as
$S = (\langle a_1, a_2, a_3, a_4 \rangle, \langle b_1, b_2, b_3, b_4 \rangle, \langle c_1, c_2, c_3, c_4 \rangle) | a_1, ..., c_4 \in B\cup W, a_1 \not = ... \not = c_4, a_1 \prec ...\prec a_4, b_1\prec...\prec b_4, c_1\prec...\prec c_4$,
where $x_1, ..., x_4$ represent the four blocks of player $x$ and
$p\prec q$ is defined as 'the number on $p$ is lower than the number on
$q$ or (the numbers on $p$ and $q$ are equal and $p$ is black and $q$ is
white)'.\
If the players had no information at all about who had which blocks,
there would be an accessibility relation between each pair of states:
$$R_x = \{(s,t)\in S\times S\}$$ However, the players do have some
information and hence we can add some restrictions on the accessibility
relations. Since each player knows his own blocks but not those of the
other players, the accessibility relations $R_x$ of player $x$ are
restricted to pairs of states for which their own blocks are the same:
$$R_x = \{(s,t)\in S\times S | \langle x_{1s}, ... x_{4s} \rangle = \langle x_{1t}, ..., x_{4t}\rangle \}$$,
where $x_{is}$ represents the $i$th block of player $x$ in state $s$.\
Furthermore, each player can see the colour of the blocks of the other
player, so in all accessible states the colour of all blocks are the
same as in the current state:
$$R_x = \{(s,t)\in S\times S | \langle x_{1s}, ... x_{4s} \rangle = \langle x_{1t}, ..., x_{4t}\rangle \}, y_{is} \in W \Leftrightarrow y_{it} \in W \textrm{ for all } y\in A$$

Taking turns {#taking-turns .unnumbered}
------------

When it is player $a$'s turn, he will guess a block of another player.
There are two possibilities, either he can guess right or guess wrong.
When he guesses right, the block is revealed to everyone, so the value
of that block becomes common knowledge. In the accessibility relations
$R_i$ of all agents, the relations to states with a different value for
that block will be removed. If he guesses wrong, everyone knows that
that block does not have that value, so the relations to states with
that value will be removed from every player's accessibility relations.\
Because we assumed that players only make guesses that can be true, the
guess can also give the other players some information about the player
in turn. All states in which the current player has a block with the
number and colour of his guess will be removed from the accessibility
relations of the other player, and possibly other deductions can be
made.

Example 1 {#example-1 .unnumbered}
---------

In this section we will illustrate the model defined above by an
example. Assume that player $a$ has the blocks \[$b1, b4, b5, w6$\],
player $b$ has \[$b2, w2, w4, b6$\], and player $c$ has
\[$w1, b3, w3, w5$\]. Because the number of possible states is quite
large, we only look from the point of view of player $a$. Player $a$
only sees his own blocks and the colour of the blocks of the other
players. He can deduce right from the start that the white 1 should be
the first block of player $c$ (because if it would be at a different
position, there would be another block in front of it, which could only
be the black 1 due to the ordering of the numbers, but he has the black
1 himself). In the same way, he can deduce that the black 6 is the last
block of player $b$, because the only number that can follow the black 6
is the white 6, which he has himself. Therefore, considering the
ordering of the blocks, there are only six possible states from the
point of view of player $a$. The model with the possible states and
accessibility relations for player $a$ is shown in Figure
[\[fig:model1\]](#fig:model1){reference-type="ref"
reference="fig:model1"}. The real state is the state at the top.
Reflexive arrows have been left out of the picture, but are there for
every state.

Now suppose that player $b$ starts and asks whether the third block of
player $c$ is a 3. Player $c$ has to answer truthfully that this is
indeed the case. Now, all models without a 3 on this place can be
removed. The resulting model is shown in Figure
[\[fig:model2\]](#fig:model2){reference-type="ref"
reference="fig:model2"}.

Not all actions of other players give information to all other players.
Suppose that now it is player $c$'s turn, and he asks whether the first
block of player $b$ is a 2. Player $b$ will answer affirmatively, but
for player $a$, this is of no interest because he already knew that this
block was a 2. After this turn, for player $a$ the model is still as
shown in Figure [\[fig:model2\]](#fig:model2){reference-type="ref"
reference="fig:model2"}.\
Now when it is player $a$'s turn, he only has to discriminate between
the two states shown in Figure
[\[fig:model2\]](#fig:model2){reference-type="ref"
reference="fig:model2"}, so by for example asking whether the last block
of player $c$ is a 5, he will be able to deduce which of the two states
is the real state.

Example 2 {#example-2 .unnumbered}
---------

In order to show a model with accessibility relations for all agents, we
take an even more simplified example. Suppose that only the numbers 1,
2, and 3 are in the game for both colours, so every player has only 2
blocks. Suppose that player $a$ has two black blocks, player $b$ has one
white and one black block, and player $c$ has two white blocks. This is
common knowledge, because everyone can see the colour of the blocks of
every player, and knows that the others can see this as well, and knows
that the others know that everyone knows, et cetera. Now the Kripke
model representing the start of the game is as shown in Figure
[\[fig:model3\]](#fig:model3){reference-type="ref"
reference="fig:model3"}. The accessibility relations for player $a,b,$
and $c$ are shown in red, magenta, and cyan respectively. As can be seen
in the model, player $b$ only has reflexive accessibility relations,
because there are no two states in which the blocks of player $b$ are
the same. This shows that player $b$ immediately knows everything. On
the other hand, for players $a$ and $c$, there are some states that are
indistinguishable from each other.

Example 3 {#example-3 .unnumbered}
---------

(Example from introduction) In this third example, we will show the way
higher order knowledge can play a role in the game. Suppose that only
all black blocks are in the game, and they are divided such that player
$a$ has \[5,6,8,11\], player $b$ has \[4,9,10,-\], and player $c$ has
\[0,1,2,3\]. The 7 is not yet in the game. The 5, 8, 4, 10 and - are
revealed already. We look from the perspective of player $c$. For him,
there are six possible states. In Figure
[\[fig:model4\]](#fig:model4){reference-type="ref"
reference="fig:model4"} the Kripke model is shown. The accessibility
relations for agent $c$ have not been drawn, but are there between every
pair of worlds. Also, the reflexive relations are left out, but are
there for every world for every agent. The bold numbers denote the
numbers that are revealed and therefore are common knowledge among all
agents. Now suppose it is the turn of agent $b$. He cannot discriminate
between the real state (the top left state), and the top right state
where agent $a$ has a 7 instead of a 6. Therefore, he asks player $a$
whether his second block is a 7, to which player $a$ must give a
negative answer. To player $c$, this gives different types of
information. Suppose that $a_7$ is the proposition referring to the fact
that the second block of player $a$ is a 7. Of course, now player $c$
knows that $a$ does not have the 7: $K_c \neg a_7$. But also he knows
that player $b$ did not know: $K_c \neg K_b \neg a_7$. He can therefore
cancel out the worlds in which this is not true from his possible
worlds. $(M,w_3)\models a_7$, $(M,w_4)\models a_7$, and
$(M,w_5)\models a_7$, and $(M,w_1)\models K_b \neg a_7$ (in all worlds
$s$ with $(w_1,s)\in R_b, (M,s)\models \neg a_7$: these worlds are
exactly $w_1$ and $w_2$), and in the same way
$(M,w_2)\models K_b \neg a_7$. Hence, the only remaining world for $c$
is $w_0$.

Action model {#action-model .unnumbered}
------------

We can also describe the situation as an action model. The only 'real'
action that can be taken in the game is the action of asking a block
from another player, but we discriminate between a right guess and a
wrong guess. Because every action that is taken and every answer are
public, the relations in the action model are equal for all agents. The
precondition for the action 'right guess' (`rg`) is that the guessed
number is indeed there, while the precondition for the action 'wrong
guess' (`wg`) is that the guessed number is not on that block and that
the person who asks does not know this. Let us denote the proposition
that block $x_i$ (i.e. the $i$th block of player $x$) has number $p$ as
'$xi_p$'.We can therefore define an action model for the game as a
structure $\langle E, \sim, \textrm{pre}\rangle$ with

-   $E = \{ \texttt{rg}(xi_p), \texttt{wg}(xi_p)|x\in A, i\in N, p\in W\cup B\}$

-   $\sim = \{(e,e)|e\in E\}$

-   pre(`rg`($xi_p$)) = $xi_p$,\
    pre(`wg(xi_p)`)=$\neg xi_p \wedge \neg K_a \neg xi_p$ with $a$ the
    agent that performs the action

When we combine the model from Example 3 with the action of guessing
that the second block of $a$ is a 7, we get the action model shown in
Figure [\[fig:actionmodel1\]](#fig:actionmodel1){reference-type="ref"
reference="fig:actionmodel1"}.

[\[fig:actionmodel1\]]{#fig:actionmodel1 label="fig:actionmodel1"}

Simulation {#simulation .unnumbered}
==========

To supplement our research and visualise the theory of mind of different
agents, we could build a simulation of a simple scenario where agents
play against each other and model their knowledge states. This
simulation features a GUI in which the current game state can be viewed
(which blocks belong to which player). This GUI features two distinct
modes, mode 1 is where we can view a game played by logical agents and
see all of their blocks. In mode 2 you can try your luck against the
agents yourself and therefore only view your own and blocks visible for
all players.

In both modes it is possible to view the worlds a agent considers
possible after every turn. We aim to represent the agents view of the
world similar to Figure
[\[fig:model4\]](#fig:model4){reference-type="ref"
reference="fig:model4"}. This view only shows the worlds the agent
considers possible, but also shows relations for other agents. Therefore
it will give insight in the logic used by said agent to make its in-game
decisions.

When a player takes an action {#when-a-player-takes-an-action .unnumbered}
-----------------------------

*Hoeft misschien niet in het verslag, maar kan helpen om de simulatie te
maken.*\
When it is a player's turn and he takes a block from the stack, the
information on that block is added to his knowledge, i.e. it is as if
this block is already in his code. At the end of his turn, all the
worlds are updated such that he has added this block to his code.\
\
When some player takes the action $\texttt{rg}(xi_p)$, i.e. guessing
correctly that the $i$th block of player $x$ is number $p$, then that
block is revealed, so all the worlds where that block has a different
value are removed (for all players, because the action is public). The
same happens when a player has made a wrong guess and has to reveal the
block that he took at the beginning of his turn at the correct place in
his code.\
*Eerst alle models updaten/toevoegen zodat deze speler daar een extra
block heeft en dan degenen die niet kunnen weer weghalen, of alleen de
models toevoegen waar hij dit specifieke blokje heeft? (en degenen die
daardoor niet meer kunnen weghalen)*\
When player $a$ takes the action $\texttt{wg}(xi_p)$, i.e. guessing
incorrectly that the $i$th block of player $x$ is number $p$, everyone
knows that that block does not have number $p$ so all the worlds where
the value of the block *is* $p$ are removed. Furthermore, all players
know that player $a$ did not know that that block was not $p$, so for
every player, all relations to worlds in which that player knows that
$K_a xi_p$ are removed. This may be different per player, e.g. player
$c$ might know that player $a$ knows something in a certain world, while
player $b$ does not know that player $a$ knows this.\
*Je had toch de general models uitgerekend door de individuele models
uit te rekenen en die dan samen te voegen? Dat zou hier dan weer mooi
uitkomen: in het individuele model van elke speler weet je wat die
speler weet over wat anderen weten (zoals in Figure 4 bijvoorbeeld: de
relaties die daar voor a en b zijn, zijn wat c weet over wat a en b
weten omdat het uit het perspectief van c gemaakt is).*\
For every player, the relations to worlds where player $a$, according to
their knowledge, did not know that $xi_p$ are removed (the worlds
themselves are not removed because they might still be accessible for
other players). Hence the relations to worlds $s$ where for all $t$ with
$(s,t)\in R_a, (M,t)\models \neg xi_p$ are removed.\
*(In een wereld waar alle relaties van a naar werelden gaan waar $xi_p$
niet waar is, weet a dat $xi_p$ niet waar is, en zou hij dus nooit
$xi_p$ raden.)*\
\
