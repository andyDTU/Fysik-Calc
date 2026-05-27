import streamlit as st
from utils import render_search_sidebar

st.set_page_config(
    page_title="Fysik-Calc",
    page_icon="⚡",
    layout="wide",
)

render_search_sidebar()

st.title("⚡ Fysik-Calc")
st.subheader("Det ultimative regneværktøj til fysikeksamen")
st.markdown("Klik på en opgavetype herunder, eller søg i sidepanelet.")
st.divider()

TASKS = [
    # Bevægelse
    ("🏃 Bevægelse", [
        ("📏", "Beregn strækning/tid", "s = v·t", "pages/1_Kinematik.py", "kin_formel", "Uniform bevægelse:  s = v · t"),
        ("🚀", "Hastig. ved acceleration", "v = v₀ + a·t", "pages/1_Kinematik.py", "kin_formel", "Jævnt accelereret (1):  v = v₀ + a · t"),
        ("📐", "Strækning ved acceleration", "s = v₀t + ½at²", "pages/1_Kinematik.py", "kin_formel", "Jævnt accelereret (2):  s = v₀·t + ½·a·t²"),
        ("🎯", "Skråt kast", "rækkevidde og højde", "pages/1_Kinematik.py", "kin_formel", "Kastebevægelse (skråt kast)"),
        ("🔁", "Cirkulær bevægelse", "v, ω, T, ac", "pages/1_Kinematik.py", "kin_formel", "Cirkulær bevægelse"),
        ("🌀", "Centrifuge (RPM)", "ω → radius", "pages/1_Kinematik.py", "kin_formel", "Cirkulær bevægelse – RPM-omregner og centripetal"),
    ]),
    # Kræfter
    ("💪 Kræfter", [
        ("⚙️", "Kraft, masse, acceleration", "F = m·a", "pages/2_Dynamik.py", "dyn_formel", "Newtons 2. lov:  F = m · a"),
        ("🏔️", "Hældende plan", "friktion og acceleration", "pages/2_Dynamik.py", "dyn_formel", "Hældende plan"),
        ("🔗", "Friktion", "f = μ·N", "pages/2_Dynamik.py", "dyn_formel", "Friktion:  f = μ · N"),
        ("💫", "Impulsmomentloven", "F·Δt = Δp", "pages/2_Dynamik.py", "dyn_formel", "Impulsmomentloven:  F · Δt = Δp"),
        ("🧱", "Spænding og tøjning", "σ, ε, E-modul", "pages/2_Dynamik.py", "dyn_formel", "Spænding og tøjning:  σ = F / A"),
        ("⚖️", "Atwood-maskine", "to masser over trisse", "pages/2_Dynamik.py", "dyn_formel", "Atwood-maskine:  to masser over trisse"),
    ]),
    # Energi
    ("🔋 Energi", [
        ("⚡", "Kinetisk energi", "Ek = ½mv²", "pages/3_Energi.py", "energi_formel", "Kinetisk energi:  Ek = ½ · m · v²"),
        ("⬆️", "Potentiel energi", "Ep = mgh", "pages/3_Energi.py", "energi_formel", "Potentiel energi:  Ep = m · g · h"),
        ("🌀", "Energibevarelse", "Ek₁+Ep₁ = Ek₂+Ep₂", "pages/3_Energi.py", "energi_formel", "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂"),
        ("🔩", "Fjeder (Hookes lov)", "F = k·x", "pages/3_Energi.py", "energi_formel", "Fjederkraft og -energi"),
        ("💡", "Effekt", "P = W/t = F·v", "pages/3_Energi.py", "energi_formel", "Effekt:  P = W / t = F · v"),
        ("📉", "Energi med friktion", "friktionskorrektion", "pages/3_Energi.py", "energi_formel", "Energibevarelse med friktion"),
    ]),
    # Elektricitet
    ("⚡ Elektricitet", [
        ("🔌", "Ohms lov", "U = R·I", "pages/4_Elektricitet.py", "el_formel", "Ohms lov:  U = R · I"),
        ("🔋", "Kondensator", "Q = C·U", "pages/4_Elektricitet.py", "el_formel", "Kondensator:  Q = C · U"),
        ("🧲", "Lorentzkraft", "F = q·v·B", "pages/4_Elektricitet.py", "el_formel", "Lorentzkraft:  F = q · v · B"),
        ("⚡", "Faradays lov", "ε = −N·ΔΦ/Δt", "pages/4_Elektricitet.py", "el_formel", "Faradays lov:  ε = -N · ΔΦ / Δt"),
    ]),
    # Termodynamik
    ("🌡️ Termodynamik", [
        ("💨", "Ideel gaslov", "pV = nRT", "pages/6_Termodynamik.py", "termo_formel", "Ideel gaslov:  p · V = n · R · T"),
        ("🔥", "Varmekapacitet", "Q = m·c·ΔT", "pages/6_Termodynamik.py", "termo_formel", "Varmekapacitet:  Q = m · c · ΔT"),
        ("💧", "Faseovergang", "Q = m·L", "pages/6_Termodynamik.py", "termo_formel", "Faseovergang:  Q = m · L"),
        ("♻️", "Carnot-virkningsgrad", "η = 1 − Tk/Tv", "pages/6_Termodynamik.py", "termo_formel", "Carnot-virkningsgrad:  η = 1 − Tk/Tv"),
    ]),
    # Bølger & Optik
    ("🌊 Bølger & Optik", [
        ("〰️", "Bølgehastighed", "v = f·λ", "pages/5_Boelger_og_Optik.py", None, None),
        ("🔭", "Snells lov / Brydning", "n₁sinθ₁ = n₂sinθ₂", "pages/5_Boelger_og_Optik.py", None, None),
        ("🔬", "Dobbeltspalte", "d·sin(θ) = nλ", "pages/5_Boelger_og_Optik.py", None, None),
        ("📡", "Doppler-effekt", "frekvensforskydning", "pages/5_Boelger_og_Optik.py", None, None),
    ]),
    # Atomfysik
    ("☢️ Atomfysik", [
        ("☢️", "Radioaktivt henfald", "N = N₀·e^(−λt)", "pages/7_Atomfysik.py", "atom_formel", "Radioaktivt henfald:  N = N₀ · e^(−λt)"),
        ("⚛️", "E = mc²", "massedefekt → energi", "pages/7_Atomfysik.py", "atom_formel", "Energi-masse:  E = Δm · c²"),
        ("💫", "Fotonenergi", "E = h·f", "pages/7_Atomfysik.py", "atom_formel", "Fotonenergí:  E = h · f = h·c / λ"),
    ]),
    # Rotation & Kollisioner
    ("🔄 Rotation & Kollisioner", [
        ("🔄", "Inertimoment", "standardlegemer", "pages/9_Rotation.py", "rot_formel", "Inertimoment – standardlegemer"),
        ("🌀", "Impulsmomentbevarelse", "I₁ω₁ = I₂ω₂", "pages/9_Rotation.py", "rot_formel", "Bevarelse af impulsmoment"),
        ("💥", "Elastisk kollision", "KE og impuls bevares", "pages/10_Kollisioner.py", "koll_formel", "Elastisk kollision – 1D (KE bevaret)"),
        ("🫂", "Uelastisk kollision", "objekter hænger sammen", "pages/10_Kollisioner.py", "koll_formel", "Fuldstændig uelastisk kollision (objekter hænger sammen)"),
    ]),
    # Usikkerhed
    ("📏 Usikkerhed", [
        ("📊", "Gennemsnit og stdafv.", "statistik", "pages/8_Usikkerhed.py", "usikk_formel", "Gennemsnit og standardafvigelse"),
        ("📉", "Fejlpropagation", "usikkerhed i formel", "pages/8_Usikkerhed.py", "usikk_formel", "Fejlpropagation – generel (numerisk)"),
        ("📈", "Potenslov-fitting", "y = A·xᵅ (log-log)", "pages/8_Usikkerhed.py", "usikk_formel", "Potenslov-fitting:  y = A · xᵅ  (log-log regression)"),
    ]),
]

for gi, (group_name, tasks) in enumerate(TASKS):
    st.markdown(f"#### {group_name}")
    n_cols = min(len(tasks), 4)
    cols = st.columns(max(n_cols, 1))
    for i, (emoji, titel, under, page, nav_key, nav_value) in enumerate(tasks):
        with cols[i % 4 if len(tasks) > 4 else i % len(tasks)]:
            if st.button(
                f"{emoji} **{titel}**\n\n_{under}_",
                key=f"card_{gi}_{i}",
                use_container_width=True,
                help=under,
            ):
                if nav_key and nav_value:
                    st.session_state[nav_key] = nav_value
                try:
                    st.switch_page(page)
                except Exception:
                    st.info(f"👈 Naviger til siden i menuen til venstre.")
    st.markdown("")

st.divider()
with st.expander("📐 Konstanter"):
    st.markdown("""
| Konstant | Symbol | Værdi |
|----------|--------|-------|
| Tyngdeacceleration | g | 9.82 m/s² |
| Lysets hastighed | c | 2.998 × 10⁸ m/s |
| Plancks konstant | h | 6.626 × 10⁻³⁴ J·s |
| Boltzmanns konstant | k_B | 1.381 × 10⁻²³ J/K |
| Gaskonstant | R | 8.314 J/(mol·K) |
| Avogadros tal | N_A | 6.022 × 10²³ mol⁻¹ |
| Elementarladning | e | 1.602 × 10⁻¹⁹ C |
| Coulombs konstant | k | 8.988 × 10⁹ N·m²/C² |
| Vakuumpermeabilitet | μ₀ | 4π × 10⁻⁷ T·m/A |
| Elektronmasse | m_e | 9.109 × 10⁻³¹ kg |
| Protonmasse | m_p | 1.673 × 10⁻²⁷ kg |
| Atommasse enhed | u | 1.661 × 10⁻²⁷ kg |
""")
