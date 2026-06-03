import streamlit as st
from utils import show_sidebar_constants, show_resultat_sidebar, breadcrumb

st.set_page_config(page_title="Formelblad", page_icon="📋", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("📋", "Formelblad")
st.title("📋 Formelblad – DTU 10060")
st.markdown("Officielt formelblad-indhold med links til beregnere.")
st.divider()

st.info("📋 Disse formler er baseret på DTU 10060 pensummet. Klik '→ Beregner' for at åbne den tilhørende regner med alle varianter.")

st.subheader("Vigtige konstanter")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("| Symbol | Værdi |")
    st.markdown("|--------|-------|")
    st.markdown("| **g** | 9.82 m/s² |")
    st.markdown("| **R** | 8.314 J/(mol·K) |")
    st.markdown("| **Nₐ** | 6.022×10²³ mol⁻¹ |")
    st.markdown("| **k_B** | 1.381×10⁻²³ J/K |")
with col2:
    st.markdown("| Symbol | Værdi |")
    st.markdown("|--------|-------|")
    st.markdown("| **c** | 3×10⁸ m/s |")
    st.markdown("| **h** | 6.626×10⁻³⁴ J·s |")
    st.markdown("| **e** | 1.602×10⁻¹⁹ C |")
    st.markdown("| **mₑ** | 9.109×10⁻³¹ kg |")
with col3:
    st.markdown("| Symbol | Værdi |")
    st.markdown("|--------|-------|")
    st.markdown("| **ε₀** | 8.854×10⁻¹² F/m |")
    st.markdown("| **G** | 6.674×10⁻¹¹ N·m²/kg² |")

st.divider()

with st.expander("🏃 Kinematik", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.latex(r"v = v_0 + at")
        st.latex(r"s = v_0 t + \tfrac{1}{2}at^2")
        st.latex(r"v^2 = v_0^2 + 2as")
        st.latex(r"s = \tfrac{1}{2}(v_0 + v)\,t")
        st.caption("Centripetalacceleration og cirkulær bevægelse:")
        st.latex(r"a_c = \frac{v^2}{r} = \omega^2 r, \quad v = \omega r, \quad T = \frac{2\pi}{\omega}")
    with col2:
        st.page_link("pages/1_Kinematik.py", label="→ Åbn Kinematik-beregner", icon="🏃")

with st.expander("⚡ Dynamik", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.latex(r"F = ma")
        st.latex(r"G = mg \quad (g = 9{,}82\ \text{m/s}^2)")
        st.latex(r"f \leq \mu N")
        st.latex(r"F_c = \frac{mv^2}{r}")
        st.caption("Gravitationsloven (G = 6.674×10⁻¹¹ N·m²/kg²):")
        st.latex(r"F = G\frac{m_1 m_2}{r^2}")
        st.caption("Impuls-momentumsætningen:")
        st.latex(r"F \cdot \Delta t = m \cdot \Delta v")
        st.caption("Arbejde:")
        st.latex(r"W = F \cdot d \cdot \cos\theta")
    with col2:
        st.page_link("pages/2_Dynamik.py", label="→ Åbn Dynamik-beregner", icon="⚡")

with st.expander("🔋 Energi", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.latex(r"E_k = \tfrac{1}{2}mv^2")
        st.latex(r"E_p = mgh")
        st.caption("Fjederpotentiel:")
        st.latex(r"E_{fj} = \tfrac{1}{2}kx^2")
        st.caption("Effekt:")
        st.latex(r"P = \frac{W}{t} = F \cdot v")
    with col2:
        st.page_link("pages/3_Energi.py", label="→ Åbn Energi-beregner", icon="🔋")

with st.expander("🌡️ Termodynamik", expanded=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Ideel gaslov (R = 8.314 J/(mol·K)):")
        st.latex(r"pV = nRT")
        st.caption("Varmekapacitet:")
        st.latex(r"Q = m \cdot c \cdot \Delta T")
        st.caption("Faseovergang (latent varme):")
        st.latex(r"Q = m \cdot L")
        st.caption("1. termodynamikslov:")
        st.latex(r"\Delta U = Q - W")
        st.caption("Carnot-virkningsgrad:")
        st.latex(r"\eta = 1 - \frac{T_k}{T_v}")
        st.caption("Molekylær rms-hastighed:")
        st.latex(r"v_{rms} = \sqrt{\frac{3RT}{M}}")
        st.caption("Adiabatisk proces:")
        st.latex(r"pV^\gamma = \text{konst}")
    with col2:
        st.page_link("pages/6_Termodynamik.py", label="→ Åbn Termodynamik-beregner", icon="🌡️")

with st.expander("🔄 Rotation", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.latex(r"\tau = I\alpha, \quad \vec{\tau} = \vec{r} \times \vec{F}")
        st.caption("Impulsmoment:")
        st.latex(r"L = I\omega")
        st.caption("Rulningsbetingelse:")
        st.latex(r"v = \omega r")
        st.caption("Steiners sætning:")
        st.latex(r"I = I_{cm} + md^2")
        st.caption("Inertimoment – vigtige former:")
        st.latex(r"I_{\text{cylinder}} = \tfrac{1}{2}mr^2")
        st.latex(r"I_{\text{kugle}} = \tfrac{2}{5}mr^2")
        st.latex(r"I_{\text{stav (center)}} = \tfrac{1}{12}mL^2")
    with col2:
        st.page_link("pages/9_Rotation.py", label="→ Åbn Rotation-beregner", icon="🔄")

with st.expander("🌊 Svingninger", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Fjedermasse-system:")
        st.latex(r"T = 2\pi\sqrt{\frac{m}{k}}, \quad \omega = \sqrt{\frac{k}{m}}")
        st.caption("Simpelt pendul:")
        st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")
        st.caption("SHM-bevægelsesligning:")
        st.latex(r"x(t) = A \cdot \cos(\omega t + \varphi)")
    with col2:
        st.page_link("pages/11_Svingninger.py", label="→ Åbn Svingninger-beregner", icon="🌊")

with st.expander("〰️ Bølger & Optik", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.latex(r"v = f \cdot \lambda")
        st.caption("Doppler-effekt:")
        st.latex(r"f' = f \cdot \frac{v \pm v_{obs}}{v \mp v_{src}}")
        st.caption("Snells brydningslov:")
        st.latex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2")
        st.caption("Tyndlinseligning:")
        st.latex(r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}")
        st.caption("Youngs dobbeltspalte:")
        st.latex(r"d \cdot \sin\theta = m\lambda")
    with col2:
        st.page_link("pages/5_Boelger_og_Optik.py", label="→ Åbn Bølger & Optik-beregner", icon="〰️")

with st.expander("⚡ Elektricitet", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Ohms lov:")
        st.latex(r"U = R \cdot I")
        st.caption("Elektrisk effekt:")
        st.latex(r"P = U \cdot I = \frac{U^2}{R} = I^2 R")
        st.caption("Kondensator:")
        st.latex(r"Q = C \cdot U, \quad E = \tfrac{1}{2}CU^2")
        st.caption("Coulombs lov (k = 8.99×10⁹ N·m²/C²):")
        st.latex(r"F = k\frac{q_1 q_2}{r^2}")
        st.caption("Lorentzkraft:")
        st.latex(r"F = qvB\sin\theta")
    with col2:
        st.page_link("pages/4_Elektricitet.py", label="→ Åbn Elektricitet-beregner", icon="⚡")

with st.expander("⚛️ Atomfysik", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Fotonenergi (h = 6.626×10⁻³⁴ J·s):")
        st.latex(r"E = hf = \frac{hc}{\lambda}")
        st.caption("Radioaktivt henfald:")
        st.latex(r"N = N_0 \cdot e^{-\lambda t}, \quad T_{1/2} = \frac{\ln 2}{\lambda}")
        st.caption("de Broglies bølgelængde:")
        st.latex(r"\lambda = \frac{h}{p} = \frac{h}{mv}")
    with col2:
        st.page_link("pages/7_Atomfysik.py", label="→ Åbn Atomfysik-beregner", icon="⚛️")

with st.expander("🚀 Relativitetsteori", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Lorentz-faktoren:")
        st.latex(r"\gamma = \frac{1}{\sqrt{1 - v^2/c^2}}")
        st.caption("Tidsudvidelse:")
        st.latex(r"\Delta t = \gamma \cdot \Delta t_0")
        st.caption("Længdekontraktion:")
        st.latex(r"L' = \frac{L_0}{\gamma}")
        st.caption("Relativistisk energi:")
        st.latex(r"E = \gamma m_0 c^2, \quad E_k = (\gamma - 1)m_0 c^2")
        st.caption("Energi-impuls-relation:")
        st.latex(r"E^2 = (m_0 c^2)^2 + (pc)^2")
    with col2:
        st.page_link("pages/12_Relativitetsteori.py", label="→ Åbn Relativitetsteori-beregner", icon="🚀")

with st.expander("📊 Usikkerhed", expanded=False):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.caption("Fejlpropagation (generel):")
        st.latex(r"\delta f = \sqrt{\sum_i \left(\frac{\partial f}{\partial x_i}\cdot \delta x_i\right)^2}")
        st.caption("Potenslov:")
        st.latex(r"\text{Hvis } f = x^n \text{, så } \frac{\delta f}{f} = n \cdot \frac{\delta x}{x}")
    with col2:
        st.page_link("pages/8_Usikkerhed.py", label="→ Åbn Usikkerhed-beregner", icon="📊")
