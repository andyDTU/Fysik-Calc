import streamlit as st

st.set_page_config(
    page_title="Fysik-Calc",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Fysik-Calc")
st.subheader("Det ultimative regneværktøj til fysikeksamen")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏃 Kinematik")
    st.markdown("Uniform bevægelse, jævnt accelereret bevægelse, kastebevægelse, cirkulær bevægelse")
    st.markdown("---")
    st.markdown("### ⚡ Elektricitet")
    st.markdown("Ohms lov, serie/parallelkobling, kondensator, Coulombs lov, magnetfelt, Lorentzkraft")

with col2:
    st.markdown("### 💪 Dynamik")
    st.markdown("Newtons love, tyngdekraft, friktion, centripetalkraft, impuls, kraftmoment")
    st.markdown("---")
    st.markdown("### 🌊 Bølger & Optik")
    st.markdown("Bølgehastighed, Snells lov, linsformel, Doppler-effekt, dobbeltspalte")

with col3:
    st.markdown("### 🔋 Energi & Arbejde")
    st.markdown("Kinetisk/potentiel energi, fjederkraft, arbejde, effekt, energibevarelse")
    st.markdown("---")
    st.markdown("### ☢️ Atomfysik")
    st.markdown("Radioaktivt henfald, halvvejstid, E=mc², fotonenergI, de Broglie, Bohrs model")

st.divider()

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("### 🌡️ Termodynamik")
    st.markdown("Ideel gaslov, varmekapacitet, faseovergang, 1. termodynamikslov, Carnot-virkningsgrad")

st.divider()
st.info("👈 Vælg et emne i menuen til venstre for at komme i gang.")

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
