#! /bin/zsh

# celery -A config worker --loglevel=INFO


# start celery worker indirectly via watchmedo
watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A config worker  --concurrency=1 --loglevel=INFO
