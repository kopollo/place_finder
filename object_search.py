import os
import sys

import image_utils
import web_utils
from config import GEOSEARCH_API_KEY
import pygame

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

    with open('image.png', 'wb') as file:
        file.write(img_content)
    # image_utils.show_image(img_content)



def load_image(path, colorkey=None):
    if not os.path.isfile(path):
        print(f"Файл с изображением '{path}' не найден")
        sys.exit()
    image = pygame.image.load(path)
    return image


class DrawWithSprite(pygame.sprite.Sprite):
    def __init__(self, pos, size, image):
        super().__init__()
        width, height = size
        image = pygame.transform.scale(image, (width, height))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


def pygame_draw():

    pygame.init()
    screen_width, screen_height =600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    running = True
    image = load_image("image.png")
    fon = DrawWithSprite(
        (0, 0),
        (screen_width, screen_height), image
    )
    fon_group = pygame.sprite.GroupSingle(fon)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('blue'))
        fon_group.draw(screen)
        pygame.display.flip()
    pygame.quit()


def full_search(center, org_to_search):
    text = org_to_search
    center = center
    geosearch_json = web_utils.geosearch_request(
        apikey=GEOSEARCH_API_KEY,
        text=text,
        center=center,
    )
    show_pil_image(geosearch_json)
    pygame_draw()
