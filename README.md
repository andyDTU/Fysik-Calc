# ⚡ Fysik-Calc

Streamlit-baseret formelberegner til DTU kursus **10060 – Fysik og Kemi**.  
108+ formler fordelt på 12 emner med direkte navigation, søgning, formeltips og resultatbuffer.

## Kom i gang

### Krav
- Python 3.8+
- Git

### Installation

```bash
# Klon repositoriet
git clone https://github.com/andyDTU/Fysik-Calc.git
cd Fysik-Calc

# Skift til development-branch
git checkout claude/wizardly-newton-ReRbT

# Installer afhængigheder
pip3 install streamlit numpy

# Start appen
python3 -m streamlit run app.py
```

Appen åbner automatisk i din browser på `http://localhost:8501`.

---

## Funktioner

### 🔍 Global søgning (`00_Søg`)
- Søg på tværs af alle 108 formler med ét søgeord (fx `centripetal`, `v²`, `kondensator`)
- Radioknapper til direkte navigation til en beregner-side

### 📐 Konstantpanel (sidebar)
Altid tilgængeligt i sidebjælken: g, c, h, k_B, R, N_A, e, k_e, μ₀, ε₀, m_e, m_p, u

### 📋 Resultatbuffer
- Klik **📋 Gem** efter en beregning for at gemme resultatet
- Det gemte resultat vises i sidebjælken — brug det som input i næste beregning

### 💡 Formel-tips
Hver formel viser en `💡`-vejledning med eksamens-hints (fortegn, enheder, faldgruber)

### 🎯 Eksamensopgaver (`00_Eksamensopgaver`)
Opgaver fra 2024 og 2025 eksamenssæt med løsninger og direkte link til den relevante beregner

---

## Emner og formler

| Side | Emner |
|------|-------|
| 🏃 Kinematik | Uniform, jævnt acc. (1-3), vandret/skråt kast, cirkulær, RPM |
| 💪 Dynamik | F=ma, friktion, centripetal, impuls, hældende plan, Atwood, spænding/tøjning, gravitation |
| 🔋 Energi | Ek, Ep, fjeder, arbejde, effekt, energibevarelse, virkningsgrad |
| ⚡ Elektricitet | Ohm, serie/parallel, kondensator, RC/RL, Coulomb, E-felt, Lorentz, Faraday |
| 🌊 Bølger & Optik | Bølgehastighed, Snell, linser, Doppler, Young, diffraktion, stående bølger |
| 🌡️ Termodynamik | Ideel gas, varmekapacitet, faseovergang, isobar/isoterm/adiabat, Carnot |
| ☢️ Atomfysik | Henfald, halvvejstid, E=mc², fotoner, de Broglie, Bohr, fotoelektrisk |
| 📏 Usikkerhed | Gennemsnit, stdafv, fejlpropagation, potenslov-fitting, lineær regression |
| 🔄 Rotation | Vinkelkin., inertimoment, Steiner, τ=Iα, rulning, impulsmoment |
| 💥 Kollisioner | Elastisk/uelastisk, restitution, eksplosion, massemidtpunkt |
| 〰️ Svingninger | Fjedermasse, pendul, SHM, dæmpet svingning |
| 🚀 Relativitetsteori | Lorentz-faktor, tidsudvidelse, længdeforkortning, relativistisk energi |

---

## Projektstruktur

```
Fysik-Calc/
├── app.py                    # Forside
├── utils.py                  # Delte funktioner + 108-formlers indeks
├── pages/
│   ├── 00_Søg.py             # Global formel-søgning
│   ├── 0_Eksamensopgaver.py  # Eksamensguide 2024-2025
│   ├── 1_Kinematik.py
│   ├── 2_Dynamik.py
│   ├── 3_Energi.py
│   ├── 4_Elektricitet.py
│   ├── 5_Boelger_og_Optik.py
│   ├── 6_Termodynamik.py
│   ├── 7_Atomfysik.py
│   ├── 8_Usikkerhed.py
│   ├── 9_Rotation.py
│   ├── 10_Kollisioner.py
│   ├── 11_Svingninger.py
│   └── 12_Relativitetsteori.py
└── requirements.txt
```

---

## Opdatering

```bash
git pull origin claude/wizardly-newton-ReRbT
```

---

## Lavet til
DTU kursus 10060 – Fysik og Kemi, eksamensperiode 2025
