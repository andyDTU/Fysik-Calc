#!/bin/bash
# Fysik-Calc starter – dobbeltklik på denne fil for at starte appen

# Gå til den mappe hvor dette script ligger (= Fysik-Calc-mappen)
cd "$(dirname "$0")"

echo "Starter Fysik-Calc..."
python3 -m streamlit run app.py
