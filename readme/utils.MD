## translations
to create/regenerate a language file after adding new string in the project run the following command:
```
python manage.py makemessages --locale=it
```
to compile the language file run the following command:
```
python manage.py compilemessages --locale=it
```
modify locale parameter to change language
```
--locale=en
```

to test images locally use ngrok and expose local host url. add to allowed hosts the url from ngrok (it changes daily)