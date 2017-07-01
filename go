#!/usr/bin/env bash

killall celery

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

python save_json.py

for i in $(seq 4)
do
  (celery -A tasks.save_photos worker --loglevel=warning --concurrency 8 -n worker${i}@%h &> worker-${i}.log) &
done

python save_photos.py
