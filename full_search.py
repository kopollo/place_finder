#!/usr/bin/python3

import os
import sys

import requests

import image_utils
import web_utils

os.environ['GEOSEARCH_API_KEY'] = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
os.environ['GEOCODER_API_KEY'] = '40d1649f-0493-4b70-98ba-98533de7710b'

GEOSEARCH_API_KEY = os.environ.get('GEOSEARCH_API_KEY', '#trash')
GEOCODER_API_KEY = os.environ.get('GEOCODER_API_KEY', '#trash')


def main():
    text = ' '.join(sys.argv[1:])
    geosearch_json = web_utils.geosearch_request(
        apikey=GEOSEARCH_API_KEY,
        text=text,
        lon=37.588392,  # argparse argument
        lat=55.734036,  # argparse argument
    )

    bounds = geosearch_json['properties']['ResponseMetaData']['SearchResponse']['boundedBy']
    span_lon = bounds[1][0] - bounds[0][0]
    span_lat = bounds[1][1] - bounds[0][1]
    span = (span_lon, span_lat)
    center_lon = bounds[0][0] + span_lon / 2
    center_lat = bounds[0][1] + span_lat / 2

    img_content = web_utils.static_maps_request(lon=center_lon, lat=center_lat, span=span)
    image_utils.show_image(img_content)


if __name__ == '__main__':
    main()
