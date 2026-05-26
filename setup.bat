@echo off
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install flask requests
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
pause
