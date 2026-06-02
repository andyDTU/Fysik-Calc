# Fysik-Calc – CLAUDE.md

Regneværktøj til DTU kursus **10060 – Fysik og Kemi**. Streamlit multi-page app med 160+ formler, tekst-søgning, variabelfiltrer, eksamensopgaver og teorispørgsmål.

## Kør appen

```bash
python3 -m streamlit run app.py
```

## Arkitektur

```
app.py                  # Forside: emne-fliser + søgefaner (tekst + variabel)
utils.py                # Delte hjælpefunktioner + FORMLER-indeks (160 entries)
pages/
  0_Eksamensopgaver.py  # 33+ opgaver fra 2024/2025 + varianter, formeloversigt
  1_Kinematik.py        # SUVAT, kast, cirkulær, RPM
  2_Dynamik.py          # Newton, friktion, sløjfe, hældende plan, fluider
  3_Energi.py           # Ek, Ep, fjeder, energibevarelse, effekt
  4_Elektricitet.py     # Ohm, RC, LC, Kirchhoff, Coulomb, Lorentz
  5_Boelger_og_Optik.py # Doppler, Snell, linser, stående bølger, Young
  6_Termodynamik.py     # pV=nRT, varme, faser, Carnot, v_rms
  7_Atomfysik.py        # Henfald, Bohr, de Broglie, foton
  8_Usikkerhed.py       # Gennemsnit, fejlpropagation, potenslov, regression
  9_Rotation.py         # τ=Iα, inertimoment, Steiner, rulning, impulsmoment
  10_Kollisioner.py     # Elastisk/uelastisk, restitution, ballistic pendulum
  11_Svingninger.py     # Fjedermasse, pendul (find T/m/k/L/g), dæmpet, resonans
  12_Relativitetsteori.py # γ, tidsudvidelse, E=γmc²
  13_Teori.py           # 65+ multiple choice teorispørgsmål
  14_Dimensionsanalyse.py # Buckingham Π, naturlige skalaer, dimensionstjek
  15_Skalering.py       # Potenslov-skalering, faktoranalyse
  00_Søg.py             # Dedikeret søgeside (redundant med app.py)
```

## Nøgle-patterns

### formula_card_grid()
Viser klikbare formelkort og returnerer den valgte formel-nøgle (string).
```python
formel = formula_card_grid(_MY_FORMULAS, "my_key")
# _MY_FORMULAS = [("Kort navn", "ligning-hint", "Fuld nøgle som returneres"), ...]
if formel == "Fuld nøgle som returneres":
    ...
```

### gem_resultat() og show_resultat_sidebar()
Gemmer et beregnet resultat i `st.session_state["_resultat"]` til brug i næste formel.
```python
gem_resultat(value, "enhed", "symbol")   # fx gem_resultat(9.82, "m/s²", "g")
show_resultat_sidebar()                   # vises automatisk i sidebar
```

### show_tips()
Viser blå info-boks baseret på den valgte formel.
```python
TIPS = {"Fuld nøgle": "Eksamenstip-tekst..."}
show_tips(formel, TIPS)
```

### breadcrumb()
"← ⚡ Fysik-Calc"-knap øverst på alle emnesider.
```python
breadcrumb("🏃", "Kinematik")
```

## Søgefunktioner – FORMLER-indekset

**Alle** søgbare formler skal registreres i `FORMLER`-listen i `utils.py`:

```python
{
    "navn": "Formlens fulde navn (skal matche formula_card_grid-nøglen)",
    "side": "Sidenavn (matcher TILES i app.py)",
    "fil":  "pages/X_Filnavn.py",
    "key":  "session_state-nøgle fra formula_card_grid",
    "kw":   "søgeord mellemrum-adskilt (dansk + forkortelser + synonymer)",
    "vars": ["s", "v₀", "v", "a", "t"],   # variable-symboler fra _VAR_OPTS
}
```

### Tekst-søgning
Søger på `f["navn"].lower()` og `f["kw"].lower()`. Tilføj rige søgeord – typisk:
- Dansk navn + forkortelse + variabelnavne + typiske brugerord
- Eksempel: `"friktion friktionskraft normalkraft mu koefficient statisk kinetisk curling isen"`

### Variabelfiltrer (app.py)
Sorterer efter `(match_score, ratio)` hvor ratio = matchede_vars / formlens_total_vars.
Brug præcis de unicode-symboler der optræder i `_VAR_OPTS` i app.py:
`s, v, v₀, a, t, h, θ, r, ω, α, τ, I, L, T, RPM, F, m, g, μ, N, σ, p, Ek, Ep, E, W, P, k, η, U, R, C, B, q, ε, V, Q, n, λ, f, c, γ, T½, Δ, x, d, φ`

## Tilføj en ny formel – tjekliste

1. **pages/X_Filnavn.py** – tilføj tuple til `_X_FORMULAS`:
   ```python
   ("Kort navn", "ligning", "Fuld nøgle")
   ```
2. **pages/X_Filnavn.py** – tilføj tip til `X_TIPS`:
   ```python
   "Fuld nøgle": "Eksamenstip..."
   ```
3. **pages/X_Filnavn.py** – implementér `elif formel == "Fuld nøgle":` sektionen
4. **utils.py** – tilføj entry i `FORMLER`-listen med `navn`, `side`, `fil`, `key`, `kw`, `vars`
5. **Syntaktjek**: `python3 -m py_compile pages/X_Filnavn.py utils.py`
6. **Søgetjek**: verificér at tekst-søgning og variabelfiltrer rammer formlen

## Søgetjek-script
```bash
python3 -c "
import re
with open('utils.py') as f: content = f.read()
p = re.compile(r'\"navn\": \"([^\"]+)\".*?\"kw\": \"([^\"]+)\"', re.DOTALL)
f = [{'navn': m.group(1), 'kw': m.group(2)} for m in p.finditer(content)]
for søg in ['dit søgeord']:
    hits = [x['navn'] for x in f if søg in x['navn'].lower() or søg in x['kw'].lower()]
    print(søg, '->', hits)
"
```

## Eksamensopgaver (pages/0_Eksamensopgaver.py)

Opgaver er dicts i `OPGAVER`-listen:
```python
{
    "år": "2025",           # "2024", "2025" eller "Variant"
    "nr": "Q7",
    "titel": "...",
    "tekst": "Opgavetekst med tal",
    "modul": "🏃 Kinematik",
    "formel": "SUVAT – universal løser",
    "værdier": "Hvad man skal indtaste",
    "svar": "Facit med enhed",
    "tags": ["kinematik", "suvat", ...],
    "page_key": "kinematik_2025q7",  # eller None
}
```

`page_key` aktiverer "Indlæs i beregner"-knap. Tilsvarende `if st.session_state.pop("example_{page_key}", None):` skal stå øverst i den relevante page-fil med pre-fill af session_state.

## Kendte gotchas

### Streamlit number_input
- `min_value` skal ALTID være ≤ `value`, ellers sættes værdien til min_value lydløst
- For meget små fysiske konstanter (fx elektron-ladning 1.6e-19): brug `min_value=1e-30`

### elif efter else – Python-fejl
Ved `formula_card_grid` bruges `if/elif/elif...` – aldrig `if/else/elif`.
Brug `elif beregn == "..."` selv for den næstsidste mulighed.

### SVD nullspace (Dimensionsanalyse)
```python
U, s, Vt = np.linalg.svd(A.T, full_matrices=True)
nullspace = Vt[k_dims:]   # KORREKT – ikke Vt[np.abs(s) < tol]
```

### Pandas styling
`df.style.applymap()` til grøn highlighting af matrix-celler:
```python
def farve(val):
    return "background-color: #d4edda" if abs(val - target) < tol else ""
st.dataframe(df.style.applymap(farve))
```

### SUVAT-kombo-sortering
Alle 10 kombinationer bruger `tuple(sorted(ukend_keys))` som nøgle i `if/elif`-kæden.

## Teorispørgsmål (pages/13_Teori.py)

```python
{
    "emne": "Dynamik",
    "q": "Spørgsmålstekst?",
    "options": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
    "correct": "C",
    "explain": "Forklaring med fysisk intuition og formel.",
}
```

## Git-workflow

```bash
# Udviklingsbranch
git add <filer>
git commit -m "Beskrivende commit-besked"
git push -u origin claude/busy-davinci-Su5Jz

# Push til main
git push origin claude/busy-davinci-Su5Jz:main
```

## Emnestruktur – TILES i app.py

Nye emner skal tilføjes til `TILES`-listen i `app.py` for at vises på forsiden:
```python
("emoji", "SideNavn", "pages/X_Filnavn.py", "formel1 · formel2 · ..."),
```
`SideNavn` skal matche `"side"`-feltet i `FORMLER`-entries i utils.py.

## Statistik (pr. juni 2026)

| Kategori | Antal |
|----------|-------|
| Formler i FORMLER-indeks | 160 |
| Eksamensopgaver | 33 (2024: 8, 2025: 9, Variant: 16) |
| Teorispørgsmål | 65 |
| Emnesider | 15 |
