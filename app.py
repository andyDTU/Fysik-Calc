import streamlit as st
from utils import show_sidebar_constants, FORMLER

st.set_page_config(
    page_title="Fysik-Calc",
    page_icon="⚡",
    layout="wide",
)

show_sidebar_constants()

st.title("⚡ Fysik-Calc")
st.markdown("**Det ultimative regneværktøj til DTU 10060 – Fysik og Kemi**")

søg = st.text_input(
    "søg",
    placeholder="🔍 Søg efter formel – fx 'centripetal', 'gaslov', 'kollision', 'v²'...",
    label_visibility="collapsed",
)

st.divider()

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
]

_SIDE_META = {t[1]: (t[0], t[2]) for t in TILES}

søg_lc = søg.strip().lower()

if søg_lc:
    # ── Søgeresultater ────────────────────────────────────────────────────────
    hits = [f for f in FORMLER
            if søg_lc in f["navn"].lower() or søg_lc in f["kw"].lower()]

    if not hits:
        st.warning(f"Ingen formler fandt for **'{søg}'** – prøv et andet ord.")
    else:
        st.markdown(f"**{len(hits)} formel(er) fundet for '{søg}'**")

        # Grupper efter side i original rækkefølge
        sider_orden = [t[1] for t in TILES]
        for side_navn in sider_orden:
            gruppe = [f for f in hits if f["side"] == side_navn]
            if not gruppe:
                continue
            emoji = _SIDE_META[side_navn][0]
            st.markdown(f"#### {emoji} {side_navn}")
            for f in gruppe:
                col1, col2 = st.columns([5, 1])
                col1.markdown(f"**{f['navn']}**")
                if col2.button("→ Åbn", key=f"srch_{f['navn']}", use_container_width=True):
                    st.session_state[f["key"]] = f["navn"]
                    st.switch_page(f["fil"])
            st.markdown("")

else:
    # ── Emne-fliser ───────────────────────────────────────────────────────────
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
