# ⚡ Fysik-Calc

Formelberegner til DTU kursus **10060 – Fysik og Kemi**.  
117 formler fordelt på 12 emner med søgning, formeltips og resultatbuffer.

---

## Første gang – sådan installerer du alt fra bunden

### Trin 1 – Installer Python

1. Gå til **[python.org/downloads](https://www.python.org/downloads/)**
2. Klik på den store gule knap "Download Python 3.x.x"
3. Åbn den downloadede fil og følg installationen
   - **Windows:** Sæt flueben ved **"Add Python to PATH"** inden du klikker Install
   - **Mac:** Klik bare Next → Install

Tjek at det virkede: åbn Terminal (Mac) eller Kommandoprompt (Windows) og skriv:
```
python3 --version
```
Du bør se noget som `Python 3.11.4`. Hvis det virker, fortsæt til Trin 2.

---

### Trin 2 – Installer Git

1. Gå til **[git-scm.com/downloads](https://git-scm.com/downloads)**
2. Download og installer for dit styresystem
3. Tjek at det virkede:
```
git --version
```
Du bør se noget som `git version 2.39.0`.

---

### Trin 3 – Download Fysik-Calc

Åbn Terminal (Mac) eller Kommandoprompt (Windows) og kør disse kommandoer én ad gangen:

```bash
git clone https://github.com/andyDTU/Fysik-Calc.git
```
*(Dette downloader alle filer til en mappe der hedder `Fysik-Calc`)*

```bash
cd Fysik-Calc
```
*(Dette "går ind i" mappen)*

```bash
git checkout claude/wizardly-newton-ReRbT
```
*(Dette skifter til den nyeste version af appen)*

---

### Trin 4 – Installer afhængigheder

```bash
pip3 install streamlit numpy
```
*(Installerer de Python-pakker appen bruger — gøres kun én gang)*

Hvis `pip3` ikke virker, prøv:
```bash
python3 -m pip install streamlit numpy
```

---

### Trin 5 – Start appen

```bash
python3 -m streamlit run app.py
```

Appen åbner automatisk i din browser. Ellers gå til **[http://localhost:8501](http://localhost:8501)**

---

## Næste gang du vil bruge appen

Du behøver ikke installere noget igen.

### Den nemme måde – dobbeltklik på start-scriptet

- **Mac:** Dobbeltklik på filen **`start_mac.command`** i Fysik-Calc-mappen  
  *(Første gang skal du måske godkende den: højreklik → Åbn → Åbn)*
- **Windows:** Dobbeltklik på filen **`start_windows.bat`** i Fysik-Calc-mappen

Appen åbner automatisk i din browser.

---

### Den manuelle måde – via terminalen

> ⚠️ **Vigtigt:** Du SKAL være inde i `Fysik-Calc`-mappen – ikke i en anden projektmappe.  
> Tjek at det er rigtigt: skriv `ls` og se om `app.py` er i listen.  
> Hvis du ser filer fra et andet projekt, er du i den forkerte mappe!

1. Åbn Terminal / Kommandoprompt
2. Gå til mappen — skriv **præcist** dette (med stort F):
```bash
cd ~/Fysik-Calc
```
3. Tjek at du er det rigtige sted:
```bash
ls
```
Du skal se `app.py`, `utils.py`, `pages/` osv. i listen.

4. Start appen:
```bash
python3 -m streamlit run app.py
```

---

## Opdatering – hent de nyeste formler

Når der er tilføjet nye formler eller rettelser, henter du dem sådan:

**Trin 1 – Stop appen** hvis den kører  
Klik i terminalen og tryk **`Ctrl + C`** (hold Ctrl nede og tryk C)

**Trin 2 – Gå til den rigtige mappe**

> ⚠️ Dette trin er vigtigt – du skal være i `Fysik-Calc`-mappen, ikke en anden mappe

Skriv præcist dette:
```bash
cd ~/Fysik-Calc
```

Tjek at du er det rigtige sted med:
```bash
ls
```
Du skal se `app.py` i listen. Ser du noget andet, er du i den forkerte mappe.

**Trin 3 – Hent opdateringen:**
```bash
git pull origin claude/wizardly-newton-ReRbT
```
Du bør se noget tekst der slutter med "Already up to date." eller en liste af opdaterede filer.

**Trin 4 – Start appen igen:**
```bash
python3 -m streamlit run app.py
```

Det er det! Appen kører nu med de nyeste formler.

---

### Fejlfinding – "det åbner et andet projekt"

Hvis appen åbner noget der **ikke** er Fysik-Calc (fx en kemi-regner):

1. Stop appen med `Ctrl + C`
2. Tjek hvilken mappe du er i:
```bash
pwd
```
Stien skal slutte med `/Fysik-Calc`. Hvis den ikke gør det, er du det forkerte sted.

3. Gå til den rigtige mappe med **fuld sti**:
```bash
cd ~/Fysik-Calc
```
4. Start igen:
```bash
python3 -m streamlit run app.py
```

---

### Fejlfinding

**"cd: no such file or directory"**  
Du er ikke det rigtige sted. Prøv at skrive `cd ~/Fysik-Calc` eller find mappen i Finder/Stifinder og åbn en terminal derfra.

**"command not found: python3"**  
Python er ikke installeret korrekt. Gå tilbage til Trin 1 og sørg for at sætte flueben ved "Add to PATH".

**"command not found: git"**  
Git er ikke installeret. Gå tilbage til Trin 2.

**Siden viser en fejl i browseren**  
Kig i terminalen – der står hvad der gik galt. Skriv til Anders hvis du sidder fast.

---

## Funktioner

### 🔍 Søg efter formel
Skriv fx `centripetal`, `usikkerhed` eller `gaslov` – find formlen uden at vide hvilken side den er på.

### 💡 Formel-tips
Hver formel viser en blå boks med eksamens-hints (hvad må man ikke glemme, hvilke fortegn, hvilke enheder).

### 📋 Resultatbuffer
Klik **📋 Gem** efter en beregning → resultatet gemmes i sidebjælken → brug det direkte som input i næste beregning.

### 📐 Konstantpanel
Alle fysiske konstanter (g, c, h, R, ...) altid tilgængeligt i sidebjælken.

### 🎯 Eksamensopgaver
Opgaver fra 2024 og 2025 med facit og direkte link til den rigtige beregner.

---

## Emner (117 formler)

| Side | Indhold |
|------|---------|
| 🏃 Kinematik | Uniform, jævnt acc., kast, cirkulær, RPM |
| 💪 Dynamik | F=ma, friktion, centripetal, gravitation, hældende plan, Atwood, spænding |
| 🔋 Energi | Ek, Ep, fjeder, arbejde, effekt, energibevarelse |
| ⚡ Elektricitet | Ohm, serie/parallel, kondensator, RC/RL, Coulomb, Lorentz, Faraday |
| 🌊 Bølger & Optik | Bølgehastighed, Snell, linser, Doppler, Young, diffraktion |
| 🌡️ Termodynamik | Ideel gas, varmekapacitet, faseovergang, isobar/isoterm/adiabat, Carnot |
| ☢️ Atomfysik | Henfald, halvvejstid, E=mc², fotoner, de Broglie, Bohr |
| 📏 Usikkerhed | Gennemsnit, fejlpropagation, potenslov-fitting, lineær regression |
| 🔄 Rotation | Vinkelkin., inertimoment, Steiner, τ=Iα, rulning, impulsmoment |
| 💥 Kollisioner | Elastisk/uelastisk, restitution, eksplosion, massemidtpunkt |
| 〰️ Svingninger | Fjedermasse, pendul, SHM, dæmpet svingning |
| 🚀 Relativitetsteori | Lorentz-faktor, tidsudvidelse, længdeforkortning, relativistisk energi |

---

Lavet til DTU kursus 10060 – Fysik og Kemi, eksamensperiode 2025
