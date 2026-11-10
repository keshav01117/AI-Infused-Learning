@echo off
REM Setup for Windows.  Run from this folder:   setup.bat

echo ==^> Creating virtual environment (.venv)
python -m venv .venv
call .venv\Scripts\activate.bat

echo ==^> Upgrading pip
python -m pip install --upgrade pip --quiet

echo ==^> Installing packages (takes a couple of minutes)
pip install -r requirements.txt

set AWS_DEFAULT_REGION=us-east-1

echo.
echo ==================================================================
echo  Packages installed.
echo.
echo  NEXT: set your AWS credentials, then run the check:
echo.
echo    .venv\Scripts\activate
echo    set AWS_DEFAULT_REGION=us-east-1
echo    python 00_check_setup.py
echo ==================================================================
