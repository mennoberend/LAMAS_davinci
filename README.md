# LAMAS_davinci

## Installation instructions
1. git clone this repo
2. `python3 -m venv venv`
3. `source venv/bin/activate`
4. `pip3 install -r requirements.txt`
5. `sudo apt install graphviz`



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
