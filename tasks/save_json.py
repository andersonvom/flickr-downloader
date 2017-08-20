import json
import os
from celery import Celery

from tasks.save_photos import process_photo

app = Celery('tasks', broker='pyamqp://guest@localhost//')
BASE_DIR = 'json_files'


@app.task
def process_json(set_info, photo):
    set_title = set_info['title']['_content']
    photo_title = photo['title']
    url = photo['url_o']

    dir_path = os.path.join(BASE_DIR, set_title)
    json_path = get_json_name(dir_path, photo)
    os.makedirs(dir_path, exist_ok=True)

    local_photo, local_fp = load_existing_json(json_path)
    local_photo.update(photo)

    json.dump(local_photo, local_fp)
    local_fp.close()
    print('Saved: %s - %s' % (set_title, json_path))
    process_photo.delay(json_path)


def load_existing_json(json_path):
    if os.path.isfile(json_path):
        local_fp = open(json_path, 'r+')
        local_photo = json.load(local_fp)
        local_fp.seek(0)
    else:
        local_fp = open(json_path, 'w')
        local_photo = {}

    return local_photo, local_fp


def get_json_name(dir_path, photo):
    return os.path.join(dir_path, photo['id']) + '.json'
