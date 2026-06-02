import streamlit as st
from utils import show_sidebar_constants, FORMLER

st.set_page_config(page_title="Fysik-Calc", page_icon="⚡", layout="wide")
show_sidebar_constants()

st.title("⚡ Fysik-Calc")
st.markdown("**Det ultimative regneværktøj til DTU 10060 – Fysik og Kemi**")

# ── Variable-filter ELLER tekst-søgning ───────────────────────────────────────
# Flade labels: "symbol – beskrivelse"  (matcher på symbolet til venstre for " – ")
_VAR_OPTS = [
    "s – strækning/position",   "v – hastighed",          "v₀ – starthastighed",
    "a – acceleration",          "t – tid",                "h – højde",
    "θ – vinkel",                "r – radius",
    "ω – vinkelhastighed",       "α – vinkelacceleration", "τ – kraftmoment",
    "I – inertimoment / strøm",  "L – impulsmoment / induktans",
    "T – periode / temperatur",  "RPM – omdrejninger/min",
    "F – kraft",                 "m – masse",              "g – tyngdeacceleration",
    "μ – friktionskoefficient",  "N – normalkraft",        "σ – spænding (stress)",
    "p – impuls / tryk",         "Ek – kinetisk energi",  "Ep – potentiel energi",
    "E – energi (generel)",      "W – arbejde",            "P – effekt",
    "k – fjederkonstant",        "η – virkningsgrad",
    "U – elektrisk spænding",    "R – modstand (Ω)",       "C – kapacitans",
    "B – magnetfelt",            "q – ladning",            "ε – EMF",
    "V – volumen",               "Q – varme",              "n – stofmængde / brydningsindeks",
    "λ – bølgelængde",           "f – frekvens",           "c – lyshastighed",
    "γ – Lorentz-faktor",        "T½ – halvvejstid",       "Δ – usikkerhed",
    "x – koordinat / måling",    "d – afstand / spalte",   "φ – faseforskel / arbejdsfunktion",
]

# Symbol-map: trunc label til symbol  ("s – strækning" → "s")
_SYM = {opt: opt.split(" – ")[0].strip() for opt in _VAR_OPTS}

tab_var, tab_søg = st.tabs(["🔢 Hvad kender du?", "🔍 Søg på tekst"])

with tab_søg:
    søg_tekst = st.text_input(
        "søg",
        placeholder="fx 'fjeder', 'doppler', 'fusion', 'bremser', 'henfald', 'rulning', 'curling'...",
        label_visibility="collapsed",
    )

with tab_var:
    valgte_labels = st.multiselect(
        "Vælg de størrelser du kender fra opgaven:",
        options=_VAR_OPTS,
        placeholder="Klik og skriv, fx 'v₀', 'acceleration', 'tid'...",
    )
    valgte_syms = [_SYM[lbl] for lbl in valgte_labels]

st.divider()

# ── Afgør hvad der vises ─────────────────────────────────────────────────────
TILES = [
    ("🏃", "Kinematik",        "pages/1_Kinematik.py",
     "s=vt · v=v₀+at · kast · cirkulær · RPM"),
    ("💪", "Dynamik",          "pages/2_Dynamik.py",
     "F=ma · friktion · Fc=mv²/r · gravitation · hælding"),
    ("🔋", "Energi",           "pages/3_Energi.py",
     "Ek=½mv² · Ep=mgh · fjeder · arbejde · effekt"),
    ("💥", "Kollisioner",      "pages/10_Kollisioner.py",
     "elastisk · uelastisk · restitution · eksplosion"),
    ("🔄", "Rotation",         "pages/9_Rotation.py",
     "τ=Iα · inertimoment · Steiner · rulning · L=Iω"),
    ("〰️", "Svingninger",     "pages/11_Svingninger.py",
     "T=2π√(m/k) · pendul · SHM · dæmpet"),
    ("⚡", "Elektricitet",     "pages/4_Elektricitet.py",
     "Ohm · serie/parallel · kondensator · Coulomb · Lorentz"),
    ("🌡️", "Termodynamik",    "pages/6_Termodynamik.py",
     "pV=nRT · Q=mcΔT · faseovergang · Carnot · adiabat"),
    ("🌊", "Bølger & Optik",   "pages/5_Boelger_og_Optik.py",
     "v=fλ · Snell · linse · Doppler · Young"),
    ("☢️", "Atomfysik",       "pages/7_Atomfysik.py",
     "henfald · T½ · E=mc² · foton · de Broglie · Bohr"),
    ("📏", "Usikkerhed",       "pages/8_Usikkerhed.py",
     "gennemsnit · fejlpropagation · potenslov · regression"),
    ("🚀", "Relativitetsteori","pages/12_Relativitetsteori.py",
     "γ=1/√(1−v²/c²) · tidsudvidelse · E=γm₀c²"),
    ("📐", "Dimensionsanalyse", "pages/14_Dimensionsanalyse.py",
     "dimensionstjek · naturlige skalaer · Pi-grupper · Buckingham"),
    ("📏", "Skalering",         "pages/15_Skalering.py",
     "potenslov · T∝m^½ · Kepler · skaleringsanalyse"),
]
_SIDE_META = {t[1]: (t[0], t[2]) for t in TILES}
_SIDE_ORDER = [t[1] for t in TILES]

if valgte_syms:
    # ── Variabel-filter resultater ────────────────────────────────────────────
    # Beregn match-score for hver formel (hvor mange valgte variable den bruger)
    hits_scored = []
    for f in FORMLER:
        vars_in_formula = f.get("vars", [])
        matched_vars = [sym for sym in valgte_syms if sym in vars_in_formula]
        match_score = len(matched_vars)
        if match_score > 0:
            hits_scored.append((f, match_score, matched_vars))

    # Sortér efter match-score (bedste først)
    hits_scored.sort(key=lambda x: x[1], reverse=True)
    hits = [f for f, _, _ in hits_scored]

    if not hits:
        st.warning(
            f"Ingen formel bruger **nogen** af de valgte størrelser. "
            f"Prøv med andre variable."
        )
    else:
        st.markdown(f"**{len(hits)} formel(er) fundet – sorteret efter bedste match**")
        for side_navn in _SIDE_ORDER:
            gruppe = [(f, score, matched) for f, score, matched in hits_scored if f["side"] == side_navn]
            if not gruppe:
                continue
            emoji = _SIDE_META[side_navn][0]
            st.markdown(f"#### {emoji} {side_navn}")
            for f, score, matched_vars in gruppe:
                col1, col2 = st.columns([5, 1])
                match_text = f" ({', '.join(matched_vars)})" if len(matched_vars) < len(valgte_syms) else ""
                col1.markdown(f"**{f['navn']}**{match_text}")
                if col2.button("→ Åbn", key=f"vf_{f['navn']}", use_container_width=True):
                    st.session_state[f["key"]] = f["navn"]
                    st.switch_page(f["fil"])
            st.markdown("")

elif søg_tekst.strip():
    # ── Tekst-søgning resultater ──────────────────────────────────────────────
    lc = søg_tekst.strip().lower()
    hits = [f for f in FORMLER
            if lc in f["navn"].lower() or lc in f["kw"].lower()]

    if not hits:
        st.warning(f"Ingen formler fundet for **'{søg_tekst}'** – prøv et andet ord.")
    else:
        st.markdown(f"**{len(hits)} formel(er) fundet for '{søg_tekst}'**")
        for side_navn in _SIDE_ORDER:
            gruppe = [f for f in hits if f["side"] == side_navn]
            if not gruppe:
                continue
            emoji = _SIDE_META[side_navn][0]
            st.markdown(f"#### {emoji} {side_navn}")
            for f in gruppe:
                col1, col2 = st.columns([5, 1])
                col1.markdown(f"**{f['navn']}**")
                if col2.button("→ Åbn", key=f"ts_{f['navn']}", use_container_width=True):
                    st.session_state[f["key"]] = f["navn"]
                    st.switch_page(f["fil"])
            st.markdown("")

else:
    # ── Emne-fliser (default) ─────────────────────────────────────────────────
    cols_per_row = 3
    rows = [TILES[i:i+cols_per_row] for i in range(0, len(TILES), cols_per_row)]
    for row in rows:
        grid = st.columns(cols_per_row)
        for col, (emoji, navn, fil, formler) in zip(grid, row):
            with col.container(border=True):
                st.markdown(f"### {emoji} {navn}")
                st.caption(formler)
                if st.button(f"Åbn {navn}", key=f"tile_{navn}", use_container_width=True):
                    st.switch_page(fil)
    st.markdown("")
    st.info("💡 **Tip:** Søg på fx 'bremser', 'curling', 'fusion', 'fjeder', 'henfald' — eller vælg variable du kender i fanen 🔢.")
