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