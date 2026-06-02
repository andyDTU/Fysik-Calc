import streamlit as st
import numpy as np
from utils import show_sidebar_constants

st.set_page_config(page_title="Eksamensopgaver", page_icon="🎯", layout="wide")
show_sidebar_constants()

PAGE_MAP = {
    "kinematik":   "pages/1_Kinematik.py",
    "dynamik":     "pages/2_Dynamik.py",
    "energi":      "pages/3_Energi.py",
    "elektricitet":"pages/4_Elektricitet.py",
    "bolger":      "pages/5_Boelger_og_Optik.py",
    "termodynamik":"pages/6_Termodynamik.py",
    "atomfysik":   "pages/7_Atomfysik.py",
    "usikkerhed":  "pages/8_Usikkerhed.py",
    "rotation":    "pages/9_Rotation.py",
    "kollisioner": "pages/10_Kollisioner.py",
    "svingninger": "pages/11_Svingninger.py",
}

st.title("🎯 Eksamensopgaver – Guide & Hurtig Adgang")
st.markdown("Find hurtigt den rigtige beregner til din eksamensopgave. Klik på et eksempel for at indlæse værdier direkte.")
st.divider()

# ── Søgning ───────────────────────────────────────────────────────────────────
søg = st.text_input("🔍 Søg efter nøgleord (fx 'centrifuge', 'usikkerhed', 'kollision'):", placeholder="skriv emne eller formeltype...")

OPGAVER = [
    # ── 2024 ──────────────────────────────────────────────────────────────────
    {
        "år": "2024", "nr": "Q1",
        "titel": "Sten kastet lodret op",
        "tekst": "Sten kastes op fra h=1.60 m med v₀=4.20 m/s, g=9.82 m/s². Find t og usikkerhed.",
        "modul": "📏 Usikkerhed", "formel": "Fejlpropagation – generel → t=(v₀+√(v₀²+2gh))/g",
        "værdier": "v₀=4.20, h=1.60, g=9.82, Δv₀=0.05, Δh=0.05, Δg=0.01",
        "svar": "t = 1.141 ± 0.011 s",
        "tags": ["kinematik", "usikkerhed", "kast", "fejlpropagation", "lodret"],
        "page_key": "usikkerhed_2024q1",
    },
    {
        "år": "2024", "nr": "Q3",
        "titel": "Position fra hastigheds-tid-graf",
        "tekst": "Hastighed som funktion af tid givet grafisk. x=10 m ved t=0. Find x(t=10 s).",
        "modul": "🏃 Kinematik", "formel": "s = v·t (stykvis for hvert interval)",
        "værdier": "Aflæs arealet under v(t)-kurven + startposition",
        "svar": "x = 47.0 m (svar E)",
        "tags": ["kinematik", "uniform", "graf", "position", "areal"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q5",
        "titel": "Skråt kast – identifikation af punkt",
        "tekst": "Kast med v₀=10/11/12 m/s og θ=40°/50°/60°. Rød cirkel markerer et nedslagspunkt.",
        "modul": "🏃 Kinematik", "formel": "Kastebevægelse (skråt kast) – beregn x_max for hvert kast",
        "værdier": "fx v₀=11 m/s, θ=50° → x_max = v₀²sin(2θ)/g = 121·sin(100°)/9.82 ≈ 12.1 m",
        "svar": "11 m/s og 50° (svar E)",
        "tags": ["kinematik", "skråt kast", "projektil"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q13",
        "titel": "Impulsmomentbevarelse – skive lander på skive",
        "tekst": "Skive I₁ roterer med ω₁. Hvilende skive I₂ lægges på. Fælles ω₂ = 3/5·ω₁. Find I₂.",
        "modul": "🔄 Rotation", "formel": "Bevarelse af impulsmoment → I₂",
        "værdier": "ω₂/ω₁ = 0.6 → I₂ = I₁·(1/0.6 - 1) = 2/3·I₁",
        "svar": "I₂ = 2/3·I₁ (svar D – officiel facitliste siger A, men D er korrekt)",
        "tags": ["rotation", "impulsmoment", "bevarelse", "skive", "inertimoment"],
        "page_key": "rotation_2024q13",
    },
    {
        "år": "2024", "nr": "Q14",
        "titel": "Kulfiber-diameter – cirkulær bevægelse + spænding",
        "tekst": "Masse m=50 kg roterer med v=100 m/s i R=1.0 m. σmax=1600 MPa. Find d.",
        "modul": "💪 Dynamik", "formel": "Spænding og tøjning → d (cirkulært tværsnit)",
        "værdier": "F = mv²/R = 500 000 N, σmax = 1.6e9 Pa",
        "svar": "d = 2.0 cm (svar A – officiel facitliste siger C, men A er korrekt)",
        "tags": ["dynamik", "spænding", "stress", "kulfiber", "cirkulær", "centripetal"],
        "page_key": "dynamik_2024q14",
    },
    # ── 2025 ──────────────────────────────────────────────────────────────────
    {
        "år": "2025", "nr": "Q2",
        "titel": "Forenelighedstest – ny prøve",
        "tekst": "Målinger: 20.1, 20.2, 20.5, 19.8 g. Ny prøve: 20.6 g. Er de forenelige?",
        "modul": "📏 Usikkerhed", "formel": "Forenelighedstest – er ny måling OK?",
        "værdier": "Eksisterende: 20.1, 20.2, 20.5, 19.8 | Ny: 20.6",
        "svar": "1.56σ fra middelværdi → forenelig (svar A)",
        "tags": ["usikkerhed", "statistik", "forenelig", "prøve", "t-test"],
        "page_key": "usikkerhed_2025q2",
    },
    {
        "år": "2025", "nr": "Q3",
        "titel": "Potenslov-fitting T ∝ k^α",
        "tekst": "k=[1.2,1.5,2.2,2.4,3.4], T=[2.56,2.29,1.89,1.81,1.52]. Find α.",
        "modul": "📏 Usikkerhed", "formel": "Potenslov-fitting: y = A·xᵅ",
        "værdier": "x: 1.2, 1.5, 2.2, 2.4, 3.4  |  y: 2.56, 2.29, 1.89, 1.81, 1.52",
        "svar": "α = −0.50 (svar E)",
        "tags": ["usikkerhed", "potenslov", "fitting", "log-log", "regression", "eksponent"],
        "page_key": "usikkerhed_2025q3",
    },
    {
        "år": "2025", "nr": "Q4",
        "titel": "To bolde mødes – lodret kast",
        "tekst": "Bold 1 kastes op med v₀=50 m/s. Samtidig slippes bold 2 fra 100 m over. Mødes ved h=?",
        "modul": "🏃 Kinematik", "formel": "Jævnt accelereret (2): s = v₀t + ½at²",
        "værdier": "y₁=50t−4.91t², y₂=100−4.91t²  →  50t=100, t=2 s",
        "svar": "h = 80.4 m (svar I)",
        "tags": ["kinematik", "lodret kast", "mødes", "jævnt accelereret"],
        "page_key": "kinematik_2025q4",
    },
    {
        "år": "2025", "nr": "Q5",
        "titel": "Bådproblem – relativ hastighed",
        "tekst": "Båd sejler L med strøm på tid T, mod strøm på tid 2T. Find v i forhold til v₀.",
        "modul": "🏃 Kinematik", "formel": "Uniform bevægelse: v = s/t",
        "værdier": "(v+v₀)·T = L, (v−v₀)·2T = L  →  v+v₀ = 2(v−v₀)  →  v=3v₀",
        "svar": "v = 3v₀ (svar B)",
        "tags": ["kinematik", "relativ hastighed", "båd", "uniform"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q7",
        "titel": "Centrifuge – radius fra RPM og centripetal",
        "tekst": "Centrifuge roterer 10 000 rpm. Centripetal­acceleration = 8500g. Find radius.",
        "modul": "🏃 Kinematik", "formel": "Cirkulær bevægelse – RPM-omregner → r fra ac og RPM",
        "værdier": "RPM = 10000, ac = 8500 × g",
        "svar": "r = 7.6 cm (svar C)",
        "tags": ["kinematik", "cirkulær", "centrifuge", "rpm", "centripetal", "radius"],
        "page_key": "kinematik_2025q7",
    },
    {
        "år": "2025", "nr": "Q8",
        "titel": "To klodser – massemidtpunkts-acceleration",
        "tekst": "2 klodser á m=1 kg. F=20 N trækkes i øverste klods. μS=0.80, μK=0.50. Find a_COM.",
        "modul": "💪 Dynamik", "formel": "Newtons 2. lov: a = F / M_total",
        "værdier": "a = F/(m₁+m₂) = 20/2 = 10 m/s² (altid uanset friktion)",
        "svar": "a = 10 m/s² (svar D)",
        "tags": ["dynamik", "newton", "friktion", "massemidtpunkt", "com", "acceleration"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q6",
        "titel": "Dimensionsanalyse – naturlige skalaer",
        "tekst": "Model a = f(m, v, L, g, F). Hvilke er naturlige skalaer for længde λ og tid τ?",
        "modul": "📐 Dimensionsanalyse", "formel": "Naturlige skalaer → tjek M/L/T-eksponenter",
        "værdier": "λ: v²/g = [LT⁻¹]²/[LT⁻²] = [L] ✓ (D) | τ: L/v = [L]/[LT⁻¹] = [T] ✓ (F) | τ: √(mL/F) = [T] ✓ (H)",
        "svar": "λ=v²/g (D) og τ=L/v (F) eller τ=√(mL/F) (H)",
        "tags": ["dimensionsanalyse", "naturlige skalaer", "buckingham", "lambda", "tau", "dimension"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q9",
        "titel": "Kernereaktion – energifordeling (fusion)",
        "tekst": "²H + ³H → ⁴He (3.5 MeV) + n. Total frigivet energi: 17.6 MeV. Hvilken % får He?",
        "modul": "💥 Kollisioner", "formel": "Eksplosion – energifordeling: KE₁ = E·m₂/(m₁+m₂)",
        "værdier": "m_He=4 u, m_n=1 u, E=17.6 MeV → KE_He = 17.6·1/(4+1) = 3.52 MeV ≈ 20%",
        "svar": "He får 20%, neutron 80% (svar D)",
        "tags": ["atomfysik", "fusion", "kernereaktion", "energifordeling", "helium", "neutron", "MeV"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q7",
        "titel": "Pendul – periode og inertimoment",
        "tekst": "Fysisk pendul: stang l=0.50 m, masse m=0.30 kg, drejer om enden. Find T.",
        "modul": "〰️ Svingninger", "formel": "Fysisk pendul: T = 2π√(I/mgd)",
        "værdier": "I = ml²/3 = 0.30·0.50²/3 = 0.025 kg·m², d = l/2 = 0.25 m",
        "svar": "T = 2π√(0.025/(0.30·9.82·0.25)) ≈ 1.03 s",
        "tags": ["svingninger", "pendul", "fysisk pendul", "inertimoment", "periode"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q9",
        "titel": "Doppler – ambulance nærmer sig",
        "tekst": "Ambulance: f=800 Hz, v_kilde=30 m/s. Lydhastighed v=343 m/s. Hvad hører du?",
        "modul": "🌊 Bølger & Optik", "formel": "Doppler-effekt: f' = f·v/(v−v_kilde)",
        "værdier": "f' = 800·343/(343−30) = 800·343/313 ≈ 876 Hz",
        "svar": "f' ≈ 876 Hz",
        "tags": ["bølger", "doppler", "ambulance", "frekvens", "lydhastighed", "kilde"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q10",
        "titel": "RC-kredsløb – hvornår er spænding 90% af V₀?",
        "tekst": "R=10 kΩ, C=100 μF. Hvornår er V_C = 0.9·V₀ under opladning?",
        "modul": "⚡ Elektricitet", "formel": "RC-kredsløb: V_C(t) = V₀(1−e^(−t/τ))",
        "værdier": "τ = RC = 10000·100e-6 = 1.0 s | 0.9 = 1−e^(−t) → t = ln(10) ≈ 2.30 s",
        "svar": "t = τ·ln(10) ≈ 2.30 s",
        "tags": ["elektricitet", "rc", "kondensator", "opladning", "tidskonstant", "eksponentiel"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q10",
        "titel": "Radioaktivt henfald – tid til 1% tilbage",
        "tekst": "Isotop med T½=5730 år (¹⁴C). Hvornår er kun 1% tilbage?",
        "modul": "☢️ Atomfysik", "formel": "Radioaktivt henfald: N/N₀ = (½)^(t/T½)",
        "værdier": "0.01 = 0.5^(t/5730) → t = 5730·ln(0.01)/ln(0.5) = 5730·6.644 ≈ 38 069 år",
        "svar": "t ≈ 38 000 år (≈ 6.64 halvvejstider)",
        "tags": ["atomfysik", "henfald", "radioaktiv", "halvvejstid", "kulstof", "procent"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q11",
        "titel": "Energibevarelse – fjeder skyder klods op ad skråning",
        "tekst": "Fjeder k=800 N/m komprimeres x=0.15 m. Klods m=0.5 kg, μ=0.20, θ=30°. Find v_top ved h=0.40 m.",
        "modul": "🔋 Energi", "formel": "Energibevarelse: ½kx² = mgh + ½mv² + μ·mg·cosθ·d",
        "værdier": "½·800·0.0225 = 9.0 J | mgh=1.962 J | friktion≈0.68 J | ½mv²=6.36 J → v=5.04 m/s",
        "svar": "v ≈ 5.0 m/s",
        "tags": ["energi", "fjeder", "skråning", "friktion", "energibevarelse", "klods"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q12",
        "titel": "Rulning – kugle ned ad bakke",
        "tekst": "Massiv kugle (I=2/5·mr²) ruller fra h=2.0 m. Find v nederst.",
        "modul": "🔄 Rotation", "formel": "Rulning uden glidning: v = √(2gh/(1 + I/(mr²)))",
        "værdier": "v = √(2·9.82·2.0/(1+2/5)) = √(39.28/1.4) = √28.06 ≈ 5.30 m/s",
        "svar": "v ≈ 5.30 m/s",
        "tags": ["rotation", "rulning", "kugle", "energibevarelse", "inertimoment", "bakke"],
        "page_key": None,
    },
    {
        "år": "2025", "nr": "Q13",
        "titel": "Carnot-virkningsgrad",
        "tekst": "Varmepumpe: T_kold=5°C, T_varm=35°C. Find Carnot-COP for opvarmning.",
        "modul": "🌡️ Termodynamik", "formel": "Carnot COP_varmepumpe = T_H/(T_H − T_C)",
        "værdier": "T_C=278 K, T_H=308 K → COP = 308/(308−278) = 308/30 ≈ 10.3",
        "svar": "COP ≈ 10.3 (effektiv varmepumpe!)",
        "tags": ["termodynamik", "carnot", "virkningsgrad", "varmepumpe", "cop", "temperatur"],
        "page_key": None,
    },
    {
        "år": "2024", "nr": "Q11",
        "titel": "Lorentz-faktor – relativistisk elektron",
        "tekst": "Elektron accelereres til v = 0.995c. Find γ og kinetisk energi.",
        "modul": "🚀 Relativitetsteori", "formel": "γ = 1/√(1−v²/c²), Ek = (γ−1)m₀c²",
        "værdier": "γ = 1/√(1−0.990025) = 1/√0.009975 ≈ 10.01 | Ek = 9.01·m_e·c² ≈ 4.61 MeV",
        "svar": "γ ≈ 10.0, Ek ≈ 4.6 MeV",
        "tags": ["relativitetsteori", "lorentz", "gamma", "elektron", "kinetisk energi", "MeV"],
        "page_key": None,
    },
]

# ── Filtrering ─────────────────────────────────────────────────────────────────
år_filter = st.radio("Vis:", ["Alle", "2024", "2025"], horizontal=True)

def matcher(opgave, søgeord, år):
    if år != "Alle" and opgave["år"] != år:
        return False
    if søgeord:
        søgeord_lower = søgeord.lower()
        text = (opgave["titel"] + " " + opgave["tekst"] + " " + " ".join(opgave["tags"])).lower()
        return søgeord_lower in text
    return True

filtrerede = [o for o in OPGAVER if matcher(o, søg, år_filter)]

st.markdown(f"**{len(filtrerede)} opgaver vises**")
st.divider()

# ── Opgave-kort ───────────────────────────────────────────────────────────────
for opgave in filtrerede:
    farve = "🟡" if opgave["år"] == "2024" else "🟢"
    with st.expander(f"{farve} **{opgave['år']} {opgave['nr']}** – {opgave['titel']}"):
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"**Opgave:** {opgave['tekst']}")
            st.markdown(f"**Brug:** {opgave['modul']} → *{opgave['formel']}*")
            st.markdown(f"**Indlæs disse værdier:**")
            st.code(opgave["værdier"], language=None)
        with col2:
            st.success(f"**Svar:** {opgave['svar']}")
            if opgave.get("page_key"):
                if st.button(f"📋 Indlæs i beregner", key=f"btn_{opgave['page_key']}"):
                    st.session_state[f"example_{opgave['page_key']}"] = True
                    emne = opgave["page_key"].split("_")[0]
                    fil = PAGE_MAP.get(emne)
                    if fil:
                        st.switch_page(fil)
        st.markdown(" ".join([f"`{t}`" for t in opgave["tags"]]))

st.divider()

# ── Formeltyper oversigt ───────────────────────────────────────────────────────
with st.expander("📚 Hurtig formeloversigt – hvad beregner hvilken side?"):
    st.markdown("""
| Opgavetype | Side | Formel |
|------------|------|--------|
| Postion/hastighed/tid | 🏃 Kinematik | Uniform / Jævnt acc. (1)-(3) |
| Kastet lodret op + tid | 🏃 Kinematik | Jævnt acc. (2): s=v₀t+½at² |
| Skrå kast rækkevidde/højde | 🏃 Kinematik | Kastebevægelse (skråt kast) |
| Centrifuge / cirkulær | 🏃 Kinematik | Cirkulær – RPM-omregner |
| Newton F=ma, friktion | 💪 Dynamik | Newtons 2. lov / Friktion |
| Hældende plan | 💪 Dynamik | Hældende plan |
| Atwood-maskine (to masser) | 💪 Dynamik | Atwood-maskine |
| Stress/strain, kulfiber | 💪 Dynamik | Spænding og tøjning → d |
| Kinetisk/potentiel energi | 🔋 Energi | Ek, Ep, Energibevarelse |
| Fjeder | 🔋 Energi | Fjederkraft og -energi |
| Ohm's lov, kredsløb | ⚡ Elektricitet | Ohms lov / Serie/Parallelkobling |
| Kollision (elastisk/uelastisk) | 💥 Kollisioner | Vælg type |
| Gaslov, varme | 🌡️ Termodynamik | pV=nRT / Q=mcΔT |
| Bølgelængde, frekvens | 🌊 Bølger | v=fλ |
| Radioaktivt henfald | ☢️ Atomfysik | Henfald / Halvvejstid |
| Gennemsnit, standardafvigelse | 📏 Usikkerhed | Gennemsnit og stdafv. |
| Fejlpropagation specifik formel | 📏 Usikkerhed | Fejlpropagation – generel (numerisk) |
| Potenslov-fitting (log-log) | 📏 Usikkerhed | Potenslov-fitting y=A·xᵅ |
| Impulsmoment / rotationsbevarelse | 🔄 Rotation | Bevarelse af impulsmoment |
| Partikel/kugle rammer legeme → ω | 🔄 Rotation | Bevarelse af impulsmoment → Partikel rammer legeme |
| Ruller ned fra højde h → v | 🔄 Rotation | Rulning uden glidning → v fra faldshøjde h |
| Identificér rullende legeme fra v og h | 🔄 Rotation | Rulning uden glidning → Identificér rullende legeme |
| Trisse + ophængt masse | 🔄 Rotation | Trisse + ophængt masse |
""")
