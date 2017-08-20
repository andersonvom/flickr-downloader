import time

from flickr2photos.flickr_client import FlickrClient
from tasks.save_json import process_json


def main():
    client = FlickrClient()
    for info in client.walk_photos():
        process_json.delay(**info)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(120)
