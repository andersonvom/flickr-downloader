import time

from flickr_downloader.flickr_client import FlickrClient
from tasks.tasks import download


def main():
    client = FlickrClient()
    for info in client.walk_photos():
        download.delay(**info)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(120)
