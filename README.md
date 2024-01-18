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
required for sending email
 - ```celery -A web_app worker -l INFO```



## redis
 - docker container with 6379:6379



## stripe
 - requires ngrok
 - requires setting in django amin under model Api keys:
    - STRIPE_TEST_SECRET_KEY
 - run: python manage.py djstripe_sync_models

## documentation
 - npm i docsify-cli -g
 - docsify serve docs

## per giulio
1. clone repo
2. install requirements in venv
3. install docker and create postgresql container and redis container (run them)
3. migrate: ```python manage.py migrate```
4. create superuser: ```python manage.py createsuperuser```
5. run server: ```python manage.py runserver``` or via debugger
1. add to djstripe api key the following:
    - key name: STRIPE_TEST_SECRET_KEY (there si a bug you may need to update and add the name again after creating the key)
    - secret: take it from somewhere
1. run: ```python manage.py djstripe_sync_models```
1. install and run ngrok (not in venv): ```ngrok http http://localhost:8000```
1. add to djstripe webhook the following:
    - Base url: url from ngrok found under "forwarding" in the terminal 
    - Version: 2023-10-16
1. run celery
1. access app at http://127.0.0.1:8000 


