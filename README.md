# pycricinfo

A lightweight Python scraper for Cricinfo. Provides a number of classes that provide low level scraping of some of the pages on Cricinfo.

## Installation

It can be installed via pip from its git repo.

```sh
pip install git+https://github.com/scrambldchannel/pycricinfo.git

```

## Usage

Several objects are available and can be used to get information from Cricinfo based on id.

```python
from pycricinfo import Match, Player

m = Match(1216509)
m.description

'Indian Premier League, 34th Match: Delhi Capitals v Chennai Super Kings at Sharjah, Oct 17, 2020'

p = Player()
p.name

'Dean Jones'

p.player_stats['batting']

{'Tests': {'matches': '52', 'innings': '89', 'not out': '11', 'runs': '3631', 'hs': '216', 'average': '46.55', 'sr': '7427', 'balls': '48.88', '100s': '11', '50s': '14', '6s': '361', 'catches': '10', 'stumpings': '34'}, 'ODIs': {'matches': '164', 'innings': '161', 'not out': '25', 'runs': '6068', 'hs': '145', 'average': '44.61', 'sr': '8362', 'balls': '72.56', '100s': '7', '50s': '46', '6s': '', 'catches': '', 'stumpings': '54'}, 'First-class': {'matches': '245', 'innings': '415', 'not out': '45', 'runs': '19188', 'hs': '324*', 'average': '51.85', 'sr': '', 'balls': '', '100s': '55', '50s': '88', '6s': '', 'catches': '', 'stumpings': '185'}, 'List A': {'matches': '285', 'innings': '276', 'not out': '43', 'runs': '10936', 'hs': '145', 'average': '46.93', 'sr': '', 'balls': '', '100s': '19', '50s': '72', '6s': '', 'catches': '', 'stumpings': '115'}}

```

Properties available are quite limited at this stage but each object stores the relevant page at ```.html``` and the JSON (if applicable) at ```.json```. It uses [Gazpacho](https://github.com/maxhumber/gazpacho) for html parsing with an instance of the ```Soup``` object availabe at ```.soup```.

## Notes

Experimental at this stage, scrape responsibly!

Originally forked from [python-espncricinfo](https://github.com/dwillis/python-espncricinfo/tree/master/espncricinfo) but largely re-written.
