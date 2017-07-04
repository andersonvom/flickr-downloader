import json
import os

from .flickr_client import FlickrClient
from .error_handler import handle


BASE_DIR = 'json_files'
MAX_RETIES = 5


class JsonDownloader(object):
    def __init__(self):
        print('Starting flickr')
        self.client = FlickrClient()
        print('Initialized')

    def start(self):
        for info in self.client.walk_photos():
            handle(process_json, **info)


def process_json(set_info, photo):
    set_title = set_info['title']['_content']
    photo_title = photo['title']
    url = photo['url_o']

    dir_path = os.path.join(BASE_DIR, set_title)
    file_path = get_json_name(dir_path, photo)
    os.makedirs(dir_path, exist_ok=True)

    local_photo, local_fp = load_existing_json(path)
    local_photo.update(photo)

    json.dump(local_photo, local_fp)
    local_fp.close()
    print('Saved: %s - %s' % (set_title, file_path))


def load_existing_json(path):
    if os.path.isfile(path):
        local_fp = open(path, 'r+')
        local_photo = json.load(local_fp)
        local_fp.seek(0)
    else:
        local_fp = open(path, 'w')
        local_photo = {}

    return local_photo, local_fp


def get_json_name(dir_path, photo):
    return os.path.join(dir_path, photo['id']) + '.json'
