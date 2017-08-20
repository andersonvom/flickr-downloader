#!/usr/bin/env bash
set -e

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

for i in $(seq 2)
do
  (celery -A tasks.save_json worker --loglevel=warning --concurrency 8 -n worker${i}@%h &> worker-${i}.log) &
done

python start.py &
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT
tail -f worker*.log
