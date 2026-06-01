import streamlit as st
from utils import show_sidebar_constants

st.set_page_config(
    page_title="Fysik-Calc",
    page_icon="⚡",
    layout="wide",
)

show_sidebar_constants()

st.title("⚡ Fysik-Calc")
st.markdown("**Det ultimative regneværktøj til DTU 10060 – Fysik og Kemi**")

col_srch, _ = st.columns([1, 3])
if col_srch.button("🔍 Søg efter formel", use_container_width=True):
    st.switch_page("pages/00_Søg.py")

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

st.divider()
st.info("💡 Tip: Brug **🔍 Søg** øverst for at finde en formel direkte, eller klik på et emne ovenfor.")
