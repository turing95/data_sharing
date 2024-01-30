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