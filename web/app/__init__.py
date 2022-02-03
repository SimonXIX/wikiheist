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

    query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?personLabel ?personDescription ?image WHERE {
  ?person wdt:P31 wd:Q5;
    wdt:P27 wd:Q145;
    wdt:P569 ?birth;
    wdt:P18 ?image.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  FILTER(NOT EXISTS { ?person (wdt:P570|wdt:P509|wdt:P20) ?o. })
  FILTER(EXISTS { ?person wdt:P18 ?o. })
  FILTER(?birth >= "1922-01-01"^^xsd:dateTime)
}
ORDER BY (UUID())
LIMIT 6
'''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    people = data['results']['bindings']

    query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?art ?artLabel ?artDescription ?locationLabel ?image WHERE {
  ?art wdt:P31 wd:Q838948.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL { ?art wdt:P276 ?location. }
  OPTIONAL { ?art wdt:P18 ?image. }
  FILTER(EXISTS { ?art wdt:P18 ?o. })
}
ORDER BY (UUID())
LIMIT 1
'''

    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    data = requests.get(url, params={'query': query, 'format': 'json'}).json()
    art = data['results']['bindings']

    return render_template('index.html', people=people, art=art)
