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
    <b>character_augmentation/imagemorph_setup.sh</b>: A setup script to clone Imagemorph.c and to compile it
  </li>
  <li>
    <b>character_augmentation/split_characters.sh</b>: A simple script to split character images into two disjoint sets
  </li>
  <li>
    <b>character_augmentation/augmentation.sh</b>: A script to augment character images with 4 random transformations
  </li>
</ul>
