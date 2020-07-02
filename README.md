# LAMAS_davinci

## Installation instructions
1. git clone this repo
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip3 install -r requirements.txt`
5. `sudo apt install graphviz`

## Run instructions
For instruction to replicate the experiments use: `python3 experiment.py --help`

To play the game with 2 logical players and yourself use: `python run_simulation.py --add_human_player --amount_of_players 2 --max_tile_number 7`

To see the other options when using the GUI use `python run_simulation.py --help`

## File descriptions of all files in the repo
<ul>
  <li>
    <b>experiment.py</b>: This script can be used to simulated a series of games, for different experimental setups.
  </li>
  <li>
    <b>game.spy</b>: Contains the game class
  </li>
  <li>
    <b>kripke_plotter.py</b>: An assortment of functions to plot global and local kripke models using networkx and graphviz.
  </li>
  <li>
    <b>player.py</b>: Implements the Player class. Also the subclasses for human controlled and logical agent controlled players are implemented in this file. SO this is were the code for the different strategies is at.
  </li>
  <li>
    <b>possible_worlds.py</b>: This file contains the code the recursively generate all possible world given the game state.
  </li>
  <li>
    <b>run_simulation.py</b>: This file can be used to play the game with a GUI.
  </li>
  <li>
    <b>tile.py</b>: Implements the Tile class, which represents a white or black black with a number.
  </li>
  <li>
    <b>view.py</b>: All code related to the tkitner GUI is in this file.
  </li>
</ul>
