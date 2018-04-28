import datetime
import filecmp
import imagehash
import json
import os
import shutil
import urllib.request

from PIL import Image

from flickr_downloader.processors import json_processor

BASE_DIR = 'image_files'


def process_photo(json_path):
    try:
        json_file = open(json_path, 'r+')
        photo = json.load(json_file)
        if '_dhash' in photo:
            if os.environ.get('DEBUG') != None:
                print('Skipped: %s (already exists)' % json_path)
            return

        temp_file = download(photo['url_o'])
        photo['_dhash'] = str(calculate_hash(temp_file, photo))
        store(json_path, photo, temp_file)
        json_file.seek(0)
        json.dump(photo, json_file)
        json_file.close()
        print("Done: %s" % json_path)
    except Exception as e:
        print('ERROR: %s \n %s' % (e, photo))
        raise


def download(url, retries = 0):
    path1, _ = urllib.request.urlretrieve(url)
    path2, _ = urllib.request.urlretrieve(url)

    if not filecmp.cmp(path1, path2):
        return download(url, retries + 1)

    return path1


def calculate_hash(path, photo):
    if photo['media'] == 'photo':
        return imagehash.dhash(Image.open(path))
    else:
        return 'NoHash-NotAPhoto'


def photo_path(photo_dir, photo):
    ext = photo['originalformat']
    if photo['media'] == 'video':
        ext = 'mp4'

    title = photo['title']
    if title in ['', '.']:
        title = photo['datetaken']

    title += ' - ' + photo['id'] + ext
    return os.path.join(photo_dir, sanitize_title(title))


def sanitize_title(title):
    return title.replace('/', '-')


def store(json_file, photo, filepath):
    photo_dir = os.path.dirname(json_file).replace(json_processor.BASE_DIR, BASE_DIR)
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
