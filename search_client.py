#!/usr/bin/env python
import requests

WIKIPEDIA_API_URL = 'http://no.wikipedia.org/w/api.php'
NRK_API_URL = 'http://v8.psapi.nrk.no/search/'
NRK_API_KEY = '7fed1e022ffa400dbcc34c5c88b97c84'
NRK_RADIO_URL_PREFIX = 'http://radio.nrk.no/'
NRK_TV_URL_PREFIX = 'http://tv.nrk.no/'


RADIUS = 10 * 1000
PAGE_LIMIT = 5


def extract_fields(hit):
    web_images = hit['hit']['image']['webImages']
    title = hit['hit']['title'] if hit['type'] == 'serie' else hit['hit']['episodeTitle']
    if hit['type'] == 'episode' and not title.startswith(hit['hit']['seriesTitle']):
        title = u'{}: {}'.format(hit['hit']['seriesTitle'], title)

    return {
        'id': hit['hit']['id'],
        'title': title,
        'url': '{}{}'.format(NRK_TV_URL_PREFIX, hit['hit']['url']),
        'image': web_images[0]['imageUrl'] if web_images else None
    }


def wikipedia_geo_search(latitude, longitude):
    params = {
        'action': 'query',
        'format': 'json',
        'gscoord': '{}|{}'.format(latitude, longitude),
        'gsradius': RADIUS,
        'list': 'geosearch',
        'gslimit': PAGE_LIMIT
    }

    r = requests.get(WIKIPEDIA_API_URL, params=params)
    return r.json()['query']


def wikipedia_id_lookup(wid):
    params = {
        'action': 'query',
        'format': 'json',
        'pageids': wid,
        'prop': 'info|extracts',
        'inprop': 'url',
        'explaintext': True,
        'exintro': True
    }
    r = requests.get(WIKIPEDIA_API_URL, params=params)
    return r.json()['query']['pages'][str(wid)]


def nrk_search(query):

    # Fetch from tv medium
    params = {
        'APIKey': '7fed1e022ffa400dbcc34c5c88b97c84',
        'q': query,
        'maxResultsPerPage': PAGE_LIMIT,
        'medium': 'tv',
        'includeHighLights': True,
    }

    r = requests.get(NRK_API_URL, params=params)
    tv_hits = [extract_fields(th) for th in r.json()['hits']]

    # Fetch from radio medium
    params['medium'] = 'radio'
    r = requests.get(NRK_API_URL, params=params)
    radio_hits = [extract_fields(rh) for rh in r.json()['hits']]

    hits = tv_hits + radio_hits
    return hits
