import filecmp
import os
import urllib.request

from .flickr_client import FlickrClient


class Downloader(object):
    BASE_DIR = 'downloaded_files'
    MAX_RETIES = 5

    def __init__(self):
        self.client = FlickrClient()

    def start(self):
        for info in self.client.walk_photos():
            self.download(**info)

    def download(self, set_info, photo):
        set_title = set_info['title']['_content']
        photo_title = photo['title']
        photo_url = photo['url_o']
        self.save_photo(set_title, photo_title, photo_url)

    def save_photo(self, set_title, photo_title, url):
        dir_path = os.path.join(self.BASE_DIR, set_title)
        file_path = os.path.join(dir_path, photo_title)
        os.makedirs(dir_path, exist_ok=True)
        print('Saving: %s - %s - %s' % (set_title, photo_title, file_path))
        self.check_download(url, file_path)

    def check_download(self, url, file_path, retry=0):
        if retry == self.MAX_RETIES:
            print('*** ERROR ***: %s - %s' % (file_path, url))

        copy_file = file_path + '-copy'
        urllib.request.urlretrieve(url, file_path)
        urllib.request.urlretrieve(url, copy_file)

        if not filecmp.cmp(file_path, copy_file):
            self.check_download(url, file_path, retry + 1)
        else:
            os.remove(copy_file)
