import streamlit as st
from utils import show_sidebar_constants, show_resultat_sidebar, FORMLER

st.set_page_config(page_title="Søg formel", page_icon="🔍", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()

st.title("⚡ Fysik-Calc")
st.markdown("Søg efter en formel, eller vælg en beregner direkte.")
st.divider()

# ── Søgefelt ──────────────────────────────────────────────────────────────────
søg = st.text_input("🔍 Søg efter beregner",
                    placeholder="fx 'centripetal', 'usikkerhed', 'gaslov', 'v²'...",
                    label_visibility="collapsed")

st.divider()

SIDER = [
    ("🏃", "Kinematik",     "pages/1_Kinematik.py",         "kin_formel"),
    ("💪", "Dynamik",       "pages/2_Dynamik.py",           "dyn_formel"),
    ("🔋", "Energi",        "pages/3_Energi.py",            "energi_formel"),
    ("⚡", "Elektricitet",  "pages/4_Elektricitet.py",      "elek_formel"),
    ("🌊", "Bølger & Optik","pages/5_Boelger_og_Optik.py",  "bolge_formel"),
    ("🌡️", "Termodynamik",  "pages/6_Termodynamik.py",      "termo_formel"),
    ("☢️", "Atomfysik",     "pages/7_Atomfysik.py",         "atom_formel"),
    ("📏", "Usikkerhed",    "pages/8_Usikkerhed.py",        "usk_formel"),
    ("🔄", "Rotation",      "pages/9_Rotation.py",          "rot_formel"),
    ("💥", "Kollisioner",   "pages/10_Kollisioner.py",      "kol_formel"),
    ("〰️", "Svingninger",   "pages/11_Svingninger.py",      "sving_formel"),
]

søg_lc = søg.strip().lower()

if søg_lc:
    # ── Søgeresultater ────────────────────────────────────────────────────────
    hits = [
        f for f in FORMLER
        if søg_lc in f["navn"].lower() or søg_lc in f["kw"].lower()
    ]

    if not hits:
        st.warning("Ingen formler matchede. Prøv et andet søgeord.")
    else:
        alle_sider_ord = [s[1] for s in SIDER]
        sider_i_hits = []
        for s in alle_sider_ord:
            gruppe = [f for f in hits if f["side"] == s]
            if gruppe:
                sider_i_hits.append((s, gruppe))

        for side_navn, formler in sider_i_hits:
            emoji = next((s[0] for s in SIDER if s[1] == side_navn), "📐")
            st.markdown(f"### {emoji} {side_navn}")
            for f in formler:
                col1, col2 = st.columns([5, 1])
                col1.markdown(f"**{f['navn']}**")
                if col2.button("→ Åbn", key=f"btn_{f['navn']}"):
                    st.session_state[f["key"]] = f["navn"]
                    st.switch_page(f["fil"])
            st.markdown("")

        st.caption(f"{len(hits)} formel(er) fundet for '{søg}'")

else:
    # ── Direkte navigation (radioknapper) ─────────────────────────────────────
    st.markdown("**Vælg beregner:**")

    PLACEHOLDER = "– vælg –"
    options = [PLACEHOLDER] + [f"{s[0]} {s[1]}" for s in SIDER]

    valg = st.radio("Vælg beregner:", options,
                    label_visibility="collapsed",
                    key="søg_radio")

    if valg != PLACEHOLDER:
        idx = options.index(valg) - 1
        _, _, fil, _ = SIDER[idx]
        st.switch_page(fil)
