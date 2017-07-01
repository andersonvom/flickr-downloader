# Flickr-Downloader

This utility downloads all images from Flickr into your local hard
drive.

## Usage

Create your credentials file `credentials.json` (see example in
`credentials.sample.json` and install requirements:

    pip install -r requirements.txt
    sudo apt-get install rabbitmq-server

Download picture info from Flickr. The first time you run this command
you will be prompted to authorize access to your Flickr account:

    python save_json.py

Start your celery workers:

    for i in $(seq 4)
    do
      (celery -A tasks.save_photos worker --loglevel=warning --concurrency 8 -n worker${i}@%h &> worker-${i}.log) &
    done

Kick off image downloading:

    python save_photos.py

Wait a really long time (depending on the number of pictures you
have)...
