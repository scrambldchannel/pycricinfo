# pycricinfo

[![scraper: gazpacho](https://img.shields.io/badge/scraper-gazpacho-C6422C)](https://github.com/maxhumber/gazpacho)


A lightweight Python scraper for Cricinfo. Provides a number of classes that provide low level scraping of some of the pages on Cricinfo.

## Installation

It can be installed via pip from its git repo.

```sh
pip install git+https://github.com/scrambldchannel/pycricinfo.git

```

## Usage

Several objects are available and can be used to get information from Cricinfo based on id.

Matches:

```python
from pycricinfo import Match, Player

m = Match(1216509)
m.name

'Indian Premier League, 34th Match: Delhi Capitals v Chennai Super Kings at Sharjah, Oct 17, 2020'

m.date

datetime.datetime(2020, 10, 17, 18, 0)

m.teams

[{'id': 4344,
  'name': 'Delhi Capitals',
  'players': [{'id': '1070168', 'name': 'Prithvi Shaw'},
   {'id': '28235', 'name': 'Shikhar Dhawan'},
   {'id': '277916', 'name': 'Ajinkya Rahane'},
   {'id': '642519', 'name': 'Shreyas Iyer'},
   {'id': '325012', 'name': 'Marcus Stoinis'},
   {'id': '326434', 'name': 'Alex Carey'},
   {'id': '554691', 'name': 'Axar Patel'},
   {'id': '26421', 'name': 'Ravichandran Ashwin'},
   {'id': '822553', 'name': 'Tushar Deshpande'},
   {'id': '550215', 'name': 'Kagiso Rabada'},
   {'id': '481979', 'name': 'Anrich Nortje'}]},
 {'id': 4343,
  'name': 'Chennai Super Kings',
  'players': [{'id': '662973', 'name': 'Sam Curran'},
   {'id': '44828', 'name': 'Faf du Plessis'},
   {'id': '8180', 'name': 'Shane Watson'},
   {'id': '33141', 'name': 'Ambati Rayudu'},
   {'id': '28081', 'name': 'MS Dhoni'},
   {'id': '234675', 'name': 'Ravindra Jadeja'},
   {'id': '290716', 'name': 'Kedar Jadhav'},
   {'id': '51439', 'name': 'Dwayne Bravo'},
   {'id': '447261', 'name': 'Deepak Chahar'},
   {'id': '475281', 'name': 'Shardul Thakur'},
   {'id': '30288', 'name': 'Karn Sharma'}]}]

m.match_stats

{'all_innings': [{'batting_team_id': 4343,
   'bowling_team_id': 4344,
   'balls_limit': 120,
   'balls': 120,
   'over_limit': 20.0,
   'overs': 20.0,
   'batting': [{'id': 662973,
     'name': 'Sam Curran',
     'captain': False,
     'runs': 0,
     'balls': 3,
     'minutes': 0,
     'fours': 0,
     'sixes': 0,
     'sr': 0.0,
     'fow': {'runs': 0, 'wickets': 1, 'overs': 0.3}},
    {'id': 44828,
     'name': 'Faf du Plessis',
     'captain': False,
     'runs': 58,
     'balls': 47,
     'minutes': 0,
     'fours': 6,
     'sixes': 2,
     'sr': 123.4,
     'fow': {'runs': 109, 'wickets': 3, 'overs': 14.4}},

     # .......
```

Players:

```python
p = Player(6044)
p.name

'Dean Jones'

p.player_stats['batting']['Tests']

{'matches': 52,
 'innings': 89,
 'not outs': 11,
 'runs': 3631,
 'highest inns score': '216',
 'average': 46.55,
 'balls': 7427,
 'sr': 48.88,
 '100s': 11,
 '50s': 14,
 'fours': 361,
 'sixes': 10,
 'catches': 34,
 'stumpings': 0}
```

Properties available are quite limited at this stage but each object stores the relevant page at ```.html``` and the JSON (if applicable) at ```.json```. It uses [Gazpacho](https://github.com/maxhumber/gazpacho) for html parsing with an instance of the ```Soup``` object availabe at ```.soup```.

There are also methods for saving the data locally for later use:

```python
p = Player(253802)
p.name

'Virat Kohli'

p.to_file("253802.html")
p2 = Player.from_file("253802.html")

p2.name

'Virat Kohli'
```




## Notes

Experimental at this stage, scrape responsibly!

Originally forked from [python-espncricinfo](https://github.com/dwillis/python-espncricinfo/tree/master/espncricinfo) but largely re-written.
