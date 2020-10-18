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


```

Properties available are quite limited at this stage but each object stores the relevant page at ```.html``` and the JSON (if applicable) at ```.json```. It uses [Gazpacho](https://github.com/maxhumber/gazpacho) for html parsing with an instance of the ```Soup``` object availabe at ```.soup```.

## Notes

Experimental at this stage, scrape responsibly!

Originally forked from [python-espncricinfo](https://github.com/dwillis/python-espncricinfo/tree/master/espncricinfo) but largely re-written.
