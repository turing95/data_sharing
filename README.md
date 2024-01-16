ngrok
 - ```ngrok http http://localhost:8000```

celery
 - ```celery -A web_app worker -l INFO```

_secret.py
 - secret.py to _secret.py and fill in the blanks

redis
 - docker container with 6379:6379
postgresql
 - docker container with 5432:5432
 - set POSTGRES_PASSWORD to the same as in _secret.py

 stripe
 - requires ngrok
 - requires setting in django amin under model Api keys:
    - STRIPE_TEST_SECRET_KEY
    - STRIPE_LIVE_SECRET_KEY
 - run: python manage.py djstripe_sync_models

documentation
 - npm i docsify-cli -g
 - docsify serve docs