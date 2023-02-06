import image_utils
import web_utils
from config import GEOSEARCH_API_KEY


def get_span(geosearch_json):
    bounds = geosearch_json['properties']['ResponseMetaData'][
        'SearchResponse']['boundedBy']
    span_lon = (bounds[1][0] - bounds[0][0]) / 10
    span_lat = (bounds[1][1] - bounds[0][1]) / 10
    span = (span_lon, span_lat)
    return span


def show_pil_image(geosearch_json):
    organization = geosearch_json["features"][0]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    span = get_span(geosearch_json)
    img_content = web_utils.static_maps_request(
        address_ll=org_point,
        span=span,
        org_point=org_point,
    )
    image_utils.show_image(img_content)


def full_search(center, org_to_search):
    text = org_to_search
    center = center
    geosearch_json = web_utils.geosearch_request(
        apikey=GEOSEARCH_API_KEY,
        text=text,
        center=center,
    )
    show_pil_image(geosearch_json)
