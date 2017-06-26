# news-api
A Python API to search News in websites. This simple code was written in Python for training purposes

## Introduction

With this API you can:
	- See the list of registered websites
	- Register News websites
	- List the latest News in a specific Website
	- Search in all websites for News containing a keyword

## List

`localhost:5000/` or `localhost:5000/sites` or `localhost:5000/list`

This will list all registered websites

Result:

```json
{
  "sites": [
    "globo.com",
    "nytimes.com",
    "veja.abril.com.br"
  ]
}
```


## List

`localhost:5000/globo.com?limit=10` 

This will list the news from `globo.com`. The limit argument is optional, and the default is `limit=5`

Result:

```json
[
  "'Nada nos destruirá', diz Temer às vésperas de decisão de Janot",
  "Em condenação de Palocci, Moro cita Lula 75 vezes",
  "Marqueteiros do PT cumprirão pena em casa",
  "Temer engaveta proposta de usar FGTS em seguro",
  "Avião com droga partiu de área da família de Maggi"
]
```

## Search

`localhost:5000/search/Lula?limit=5` 

This will search all the websites registered for News that contain the word `Lula`.
The limit argument is optional, and the default is `limit=5`

Result:

```json
{
  "found": {
    "globo.com": [
      "Em condenação de Palocci, Moro cita Lula 75 vezes"
    ],
    "nytimes.com": [
      
    ],
    "veja.abril.com.br": [
      "Lula é citado 68 vezes na sentença que condenou Palocci",
      "Datafolha: Lula lidera; Bolsonaro e Marina empatam em segundo"
    ]
  }
}
```

## Setup

To run this script, you'll need [Python 3.x](https://www.python.org/downloads/) installed and [pip](https://pip.pypa.io/en/stable/installing/) to get the packages

Then you must get the extensions [Flask-restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/installation.html), [requests](http://docs.python-requests.org/en/master/user/install/) and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup)

To get then you can simply open a terminal and type:
`pip install flask-restful`
`pip install requests`
`pip install beautifulsoup4`

## Running

To run the program, `clone` the repository or download `news_finder_api.py`

Open a terminal and go to the folder that contains `news_finder_api.py` 

Type `python news_finder_api.py` and it will run the service under http://127.0.0.1:5000/
