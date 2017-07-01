import datetime
import filecmp
import imagehash
import json
import os
import shutil
import urllib.request

from celery import Celery
from PIL import Image

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def process_photo(path):
    json_file = open(path, 'r+')
    photo = json.load(json_file)
    temp_file = download(photo['url_o'])
    photo['_dhash'] = str(calculate_hash(temp_file))
    store(path, photo, temp_file)
    json_file.seek(0)
    json.dump(photo, json_file)
    json_file.close()
    print("Done: %s" % path)


def download(url, retries = 0):
    path1, _ = urllib.request.urlretrieve(url)
    path2, _ = urllib.request.urlretrieve(url)

    if not filecmp.cmp(path1, path2):
        return download(url, retries + 1)

    return path1


def calculate_hash(path):
    return imagehash.dhash(Image.open(path))


def photo_path(photo_dir, photo):
    title = photo['title']
    if title in ['', '.']:
        title = photo['datetaken']

    title += ' - ' + photo['id']
    name, ext = os.path.splitext(photo['url_o'])
    if ext == "":
        if name.startswith("VID"):
            ext = 'mp4'
        else:
            print("***ERROR***: NoExtension: %s" % photo['id'])

    title += ext
    return os.path.join(photo_dir, title)


def store(json_file, photo, filepath):
    photo_dir = os.path.dirname(json_file).replace('json_files', 'image_files')
    os.makedirs(photo_dir, exist_ok=True)
    final_location = photo_path(photo_dir, photo)
    shutil.move(filepath, final_location)
    fix_timestamp(photo, final_location)


def fix_timestamp(photo, path):
    epoch = datetime.datetime.utcfromtimestamp(0)
    time_format = '%Y-%m-%d %H:%M:%S'
    date_taken = datetime.datetime.strptime(photo['datetaken'], time_format)
    seconds = (date_taken - epoch).total_seconds()
    os.utime(path, (seconds, seconds))
