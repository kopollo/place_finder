import json

import requests


def get_request(server: str, params: dict[str, str] = None):
    try:
        response = requests.get(server, params)
        if not response:
            print('Server is sad with status code', response.status_code)
            print(response.reason)
            return response
        return response
    except requests.RequestException as exc:
        print('Oh ship :(')
        print(exc)


def geocoder_request(apikey: str, geocode: str, format: str = 'json'):
    API_SERVER = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': apikey,
        'geocode': geocode,
        'format': format,
    }

    response = get_request(API_SERVER, params)
    json = response.json()
    return json["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]


def static_maps_request(address_ll, span, org_point, map_type: str = 'map'):
    API_SERVER = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'll': address_ll,
        'spn': ','.join(map(str, span)),
        'l': map_type,
        "pt": "{0},pm2dgl".format(org_point)
    }
    response = get_request(API_SERVER, params)
    print(response.url)
    return response.content


def geosearch_request(*, apikey, text, center,
                      lang: str = 'ru_RU', type_: str = 'biz'):
    API_SERVER = "https://search-maps.yandex.ru/v1/"
    map_params = {
        'apikey': apikey,
        'text': text,
        'lang': lang,
        'll': center,
        'type': type_,
    }
    response = get_request(API_SERVER, params=map_params)
    json = response.json()
    return json


def get_ll_by_address(key, address):
    coords = geocoder_request(key, address)['Point']['pos']
    return coords.replace(' ', ',')
