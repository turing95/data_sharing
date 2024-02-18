## Automatic output.css update
run the following command to update output.css file:

```
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```
set files to watch in tailwind.config.js
```
module.exports = {
    content: [
        './templates/**/*.html',
        ...,
    ]
    ...
```

## _secret.py
 - secret.py to _secret.py and fill in the blanks

## postgresql
required to the app.
 - docker container with 5432:5432
 - set POSTGRES_PASSWORD to the same as in _secret.py


## ngrok
required for stripe
 - ```ngrok http http://localhost:8000```

## celery
required for async tasks
 - ```celery -A web_app worker -l INFO```
 - for windows use: ```celery -A web_app worker -l INFO --pool=solo```

## celery beat
required for scheduled async tasks
 - ```celery -A web_app beat -l INFO```

## redis
 - docker container with 6379:6379



## stripe
 - requires ngrok if you want to use webhooks
 - requires setting in django admin under model Api keys:
    - STRIPE_TEST_SECRET_KEY
 - run:  ```python manage.py djstripe_sync_models Price Product ```

## documentation
 - npm i docsify-cli -g
 - docsify serve docs
 - to test images locally use ngrok and expose local host url. add to allowed hosts the url from ngrok (it changes daily)