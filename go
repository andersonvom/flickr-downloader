#!/usr/bin/env bash

set -e

killall celery 2> /dev/null || true

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

python save_json.py

for i in $(seq 2)
do
  (celery -A tasks.save_photos worker --loglevel=warning --concurrency 8 -n worker${i}@%h &> worker-${i}.log) &
done

python save_photos.py

tail -f worker*.log
