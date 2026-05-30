@echo off
:: Fysik-Calc starter – dobbeltklik på denne fil for at starte appen

:: Gå til den mappe hvor dette script ligger (= Fysik-Calc-mappen)
cd /d "%~dp0"

echo Starter Fysik-Calc...
python -m streamlit run app.py
pause
