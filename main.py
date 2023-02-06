import argparse

import web_utils
from object_search import full_search
from config import GEOCODER_API_KEY


def init_parser():
    parser = argparse.ArgumentParser(
        description="find organization on map ")

    parser.add_argument('start_search_point')
    parser.add_argument('organization')
    args = parser.parse_args()
    return args


def main():
    args = init_parser()

    org_to_search = args.organization
    center = web_utils.get_ll_by_address(
        GEOCODER_API_KEY, args.start_search_point)
    full_search(center, org_to_search)


if __name__ == '__main__':
    main()
