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
4. migrate: ```python manage.py migrate```
5. create superuser: ```python manage.py createsuperuser```
6. run server: ```python manage.py runserver``` or via debugger
7. add to djstripe api key the following:
    - key name: STRIPE_TEST_SECRET_KEY (there si a bug you may need to update and add the name again after creating the key)
    - secret: take it from somewhere
8. run: ```python manage.py djstripe_sync_models```
9. install and run ngrok (not in venv): ```ngrok http http://localhost:8000```
10. add to djstripe webhook the following:
     - Base url: url from ngrok found under "forwarding" in the terminal 
     - Version: 2023-10-16
11. add the ngrok url without https to the ALLOWED_HOSTS in settings.py
12. run celery
13. access app at localhost:8000

# Windows and vs code venv activation
Giulio: 
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
..\venvs\data_share_venv\Scripts\activate 
``` 

# useful scripts
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
..\venvs\data_share_venv\Scripts\activate 
npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
..\venvs\data_share_venv\Scripts\activate 
celery -A web_app worker -l INFO
```
```
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
..\venvs\data_share_venv\Scripts\activate 
celery -A web_app worker -l INFO --pool=solo
```



