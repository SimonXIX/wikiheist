# @name: __init__.py
# @version: 0.1
# @creation_date: 2022-02-02
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <simon.bowie.19@gmail.com>
# @purpose: Initialises the app and queries Wikidata
# @acknowledgements:

from flask import Flask, render_template
from flask_moment import Moment
import requests
import urllib.request, json

# initiate Moment for datetime functions
moment = Moment()

app = Flask(__name__)

moment.init_app(app)

@app.route('/')
def index():

    query = '''SELECT ?person ?personLabel ?personDescription ?image WHERE {
  { SELECT ?person ?image WHERE {
    ?person wdt:P31 wd:Q5;
      wdt:P27 wd:Q145;
      wdt:P569 ?birth;
      wdt:P18 ?image.
      FILTER NOT EXISTS { ?person wdt:P570 ?o. }
      FILTER(?birth >= "1922-01-01"^^xsd:dateTime)
   }
   ORDER BY (UUID())
   LIMIT 6}
   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
'''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    people = data['results']['bindings']

    query = '''SELECT ?art ?artLabel ?artDescription ?locationLabel ?image WHERE {
  { SELECT ?art ?image WHERE {
    ?art wdt:P31 wd:Q838948;
      wdt:P18 ?image;
   }
   ORDER BY (UUID())
   LIMIT 1  }
   SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
   OPTIONAL { ?art wdt:P276 ?location. }
}
'''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    art = data['results']['bindings']

    return render_template('index.html', people=people, art=art)
