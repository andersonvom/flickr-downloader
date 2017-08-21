from celery import Celery
from celery import chain

from flickr_downloader.processors import json_processor
from flickr_downloader.processors import photo_processor

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
def download(set_info, photo):
    chain(
        process_json.s(set_info, photo) |
        process_photo.s()
    ).delay()


@app.task(autoretry_for=(Exception,), retry_backoff=True)
def process_json(set_info, photo):
    return json_processor.process_json(set_info, photo)


@app.task(autoretry_for=(Exception,), retry_backoff=True)
def process_photo(json_path):
    return photo_processor.process_photo(json_path)
