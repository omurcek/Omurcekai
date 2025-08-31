@echo off
REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required packages
pip install flask requests

REM Set environment variables for Flask
set FLASK_APP=app.py
set FLASK_ENV=development

REM Run Flask app
flask run

pause