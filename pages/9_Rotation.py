import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips

st.set_page_config(page_title="Rotation", page_icon="🔄", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
st.title("🔄 Rotation")
st.markdown("Vinkelkinematik, inertimoment, drejningsmoment, rulning og impulsmoment — Lectures 11-12 (10060)")
st.divider()

G = 9.82

# Pre-fill from Eksamensopgaver guide
if st.session_state.pop("example_rotation_2024q13", None):
    st.session_state["rot_formel"] = "Bevarelse af impulsmoment"
    st.session_state["rot_bev_mode"] = "I₂ – slut­inertimoment (kg·m²)"
    st.session_state["rot_I1"] = 3.0
    st.session_state["rot_w1"] = 5.0
    st.session_state["rot_w2"] = 3.0

formel = st.selectbox("Vælg formel", [
    "Vinkelkinematik (analog til lineær kinematik)",
    "Sammenhæng lineær ↔ vinkelbevægelse",
    "Inertimoment – standardlegemer",
    "Steiners sætning:  I = Icm + M·d²",
    "Rotationskinetisk energi:  K = ½·I·ω²",
    "Newtons 2. lov for rotation:  τ = I·α",
    "Arbejde og effekt ved rotation",
    "Rulning uden glidning",
    "Impulsmoment:  L = I·ω",
    "Bevarelse af impulsmoment",
    "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)",
], key="rot_formel")

ROT_TIPS = {
    "Vinkelkinematik (analog til lineær kinematik)": "Analogt med lineær kinematik: α↔a, ω↔v, θ↔s. Husk enhederne: θ i rad, ω i rad/s, α i rad/s².",
    "Sammenhæng lineær ↔ vinkelbevægelse": "v = ω·r, a_t = α·r, a_c = ω²·r. Tangential­acc. og centripetalacc. er vinkelrette.",
    "Inertimoment – standardlegemer": "Solidt hulrum: I = ½MR². Tynd ring: I = MR². Kugle: I = ⅖MR². Stav: I = ⅟₁₂ML².",
    "Steiners sætning:  I = Icm + M·d²": "Flyt rotationsakse parallelt med tyngdepunktsakse. d = afstand. Giver altid I > I_cm.",
    "Rotationskinetisk energi:  K = ½·I·ω²": "Kombineret translationsenergi + rotationsenergi: K_total = ½mv² + ½Iω². Bruges ved rulning.",
    "Newtons 2. lov for rotation:  τ = I·α": "Nettodrejningsmoment = I·α. τ = F·l (kraftarm). Husk fortegn på τ.",
    "Bevarelse af impulsmoment": "L = I·ω bevares når ΣτExt = 0. Figur­skatøjer trækker arme ind → I mindskes → ω øges.",
    "Rulning uden glidning": "v_cm = ω·R. Energi: K = ½mv² + ½Iω² = ½mv²(1 + I/mR²).",
    "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)": "Newton for masse: mg − T = ma. Newton for rotation: T·R = I·α = I·a/R. Løs systemet.",
}
show_tips(formel, ROT_TIPS)
st.divider()

if formel == "Vinkelkinematik (analog til lineær kinematik)":
    st.markdown("""
| Lineær | Vinkelmæssig |
|--------|-------------|
| s | θ (rad) |
| v | ω (rad/s) |
| a | α (rad/s²) |
""")
    st.latex(r"\omega = \omega_0 + \alpha t \qquad \theta = \omega_0 t + \tfrac{1}{2}\alpha t^2 \qquad \omega^2 = \omega_0^2 + 2\alpha\theta")

    ekv = st.selectbox("Vælg ligning:", [
        "ω = ω₀ + α·t",
        "θ = ω₀·t + ½·α·t²",
        "ω² = ω₀² + 2·α·θ",
    ])
    st.divider()

    if ekv == "ω = ω₀ + α·t":
        beregn = st.radio("Beregn:", ["ω (rad/s)", "ω₀ (rad/s)", "α (rad/s²)", "t (s)"], horizontal=True)
        st.divider()
        if beregn == "ω (rad/s)":
            c1, c2, c3 = st.columns(3)
            w0 = c1.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            a  = c2.number_input("α (rad/s²)", value=2.0, format="%.6g")
            t  = c3.number_input("t (s)", value=5.0, format="%.6g")
            w = w0 + a * t
            st.success(f"**ω = {w:.6g} rad/s**")
            st.latex(rf"\omega = {w0:.6g} + {a:.6g} \cdot {t:.6g} = {w:.6g}\ \text{{rad/s}}")
        elif beregn == "ω₀ (rad/s)":
            c1, c2, c3 = st.columns(3)
            w  = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            a  = c2.number_input("α (rad/s²)", value=2.0, format="%.6g")
            t  = c3.number_input("t (s)", value=5.0, format="%.6g")
            w0 = w - a * t
            st.success(f"**ω₀ = {w0:.6g} rad/s**")
        elif beregn == "α (rad/s²)":
            c1, c2, c3 = st.columns(3)
            w  = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            w0 = c2.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            t  = c3.number_input("t (s)", value=5.0, min_value=1e-12, format="%.6g")
            a = (w - w0) / t
            st.success(f"**α = {a:.6g} rad/s²**")
            st.latex(rf"\alpha = \frac{{\omega - \omega_0}}{{t}} = \frac{{{w:.6g} - {w0:.6g}}}{{{t:.6g}}} = {a:.6g}\ \text{{rad/s}}^2")
        else:
            c1, c2, c3 = st.columns(3)
            w  = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            w0 = c2.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            a  = c3.number_input("α (rad/s²)", value=2.0, min_value=1e-12, format="%.6g")
            t = (w - w0) / a
            st.success(f"**t = {t:.6g} s**")

    elif ekv == "θ = ω₀·t + ½·α·t²":
        beregn = st.radio("Beregn:", ["θ (rad)", "ω₀ (rad/s)", "α (rad/s²)", "t (s)"], horizontal=True)
        st.divider()
        if beregn == "θ (rad)":
            c1, c2, c3 = st.columns(3)
            w0 = c1.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            a  = c2.number_input("α (rad/s²)", value=2.0, format="%.6g")
            t  = c3.number_input("t (s)", value=5.0, format="%.6g")
            theta = w0 * t + 0.5 * a * t**2
            rev = theta / (2 * np.pi)
            st.success(f"**θ = {theta:.6g} rad  =  {np.degrees(theta):.4g}°  =  {rev:.4g} omdrejninger**")
            st.latex(rf"\theta = {w0:.6g} \cdot {t:.6g} + \tfrac{{1}}{{2}} \cdot {a:.6g} \cdot {t:.6g}^2 = {theta:.6g}\ \text{{rad}}")
        elif beregn == "α (rad/s²)":
            c1, c2, c3 = st.columns(3)
            theta = c1.number_input("θ (rad)", value=25.0, format="%.6g")
            w0    = c2.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            t     = c3.number_input("t (s)", value=5.0, min_value=1e-12, format="%.6g")
            a = 2 * (theta - w0 * t) / t**2
            st.success(f"**α = {a:.6g} rad/s²**")
        else:
            st.info("Brug ligning 1 (ω = ω₀ + αt) og ligning 3 (ω² = ω₀² + 2αθ) til andre variable.")

    else:  # ω² = ω₀² + 2αθ
        beregn = st.radio("Beregn:", ["ω (rad/s)", "ω₀ (rad/s)", "α (rad/s²)", "θ (rad)"], horizontal=True)
        st.divider()
        if beregn == "ω (rad/s)":
            c1, c2, c3 = st.columns(3)
            w0    = c1.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            a     = c2.number_input("α (rad/s²)", value=2.0, format="%.6g")
            theta = c3.number_input("θ (rad)", value=25.0, format="%.6g")
            val = w0**2 + 2 * a * theta
            if val < 0:
                st.error("ω² < 0 – ingen reel løsning")
            else:
                w = np.sqrt(val)
                st.success(f"**ω = {w:.6g} rad/s**")
                st.latex(rf"\omega = \sqrt{{\omega_0^2 + 2\alpha\theta}} = {w:.6g}\ \text{{rad/s}}")
        elif beregn == "α (rad/s²)":
            c1, c2, c3 = st.columns(3)
            w     = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            w0    = c2.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            theta = c3.number_input("θ (rad)", value=25.0, min_value=1e-12, format="%.6g")
            a = (w**2 - w0**2) / (2 * theta)
            st.success(f"**α = {a:.6g} rad/s²**")
        elif beregn == "θ (rad)":
            c1, c2, c3 = st.columns(3)
            w  = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            w0 = c2.number_input("ω₀ (rad/s)", value=0.0, format="%.6g")
            a  = c3.number_input("α (rad/s²)", value=2.0, min_value=1e-12, format="%.6g")
            theta = (w**2 - w0**2) / (2 * a)
            st.success(f"**θ = {theta:.6g} rad  =  {theta/(2*np.pi):.4g} omdrejninger**")
        else:
            c1, c2, c3 = st.columns(3)
            w     = c1.number_input("ω (rad/s)", value=10.0, format="%.6g")
            a     = c2.number_input("α (rad/s²)", value=2.0, format="%.6g")
            theta = c3.number_input("θ (rad)", value=25.0, min_value=1e-12, format="%.6g")
            val = w**2 - 2 * a * theta
            if val < 0:
                st.error("ω₀² < 0 – ingen reel løsning")
            else:
                w0 = np.sqrt(val)
                st.success(f"**ω₀ = {w0:.6g} rad/s**")

elif formel == "Sammenhæng lineær ↔ vinkelbevægelse":
    st.latex(r"s = r\theta \qquad v = r\omega \qquad a_t = r\alpha \qquad a_c = \omega^2 r = \frac{v^2}{r}")
    beregn = st.radio("Beregn:", ["s og v fra θ og ω", "θ og ω fra s og v", "Centripetal­acceleration ac"], horizontal=True)
    st.divider()

    if beregn == "s og v fra θ og ω":
        c1, c2, c3 = st.columns(3)
        r     = c1.number_input("r – radius (m)", value=0.5, min_value=1e-12, format="%.6g")
        theta = c2.number_input("θ – vinkelposition (rad)", value=3.14, format="%.6g")
        omega = c3.number_input("ω – vinkelhastighed (rad/s)", value=4.0, format="%.6g")
        s = r * theta
        v = r * omega
        st.success(f"**s = {s:.6g} m**   **v = {v:.6g} m/s**")
        st.latex(rf"s = r\theta = {r:.6g} \cdot {theta:.6g} = {s:.6g}\ \text{{m}}")
        st.latex(rf"v = r\omega = {r:.6g} \cdot {omega:.6g} = {v:.6g}\ \text{{m/s}}")

    elif beregn == "θ og ω fra s og v":
        c1, c2, c3 = st.columns(3)
        r = c1.number_input("r – radius (m)", value=0.5, min_value=1e-12, format="%.6g")
        s = c2.number_input("s – buglængde (m)", value=1.57, format="%.6g")
        v = c3.number_input("v – hastighed (m/s)", value=2.0, format="%.6g")
        theta = s / r
        omega = v / r
        st.success(f"**θ = {theta:.6g} rad**   **ω = {omega:.6g} rad/s**")

    else:
        c1, c2 = st.columns(2)
        omega = c1.number_input("ω – vinkelhastighed (rad/s)", value=4.0, format="%.6g")
        r     = c2.number_input("r – radius (m)", value=0.5, min_value=1e-12, format="%.6g")
        ac = omega**2 * r
        v  = omega * r
        st.success(f"**ac = {ac:.6g} m/s²**   (v = {v:.6g} m/s)")
        st.latex(rf"a_c = \omega^2 r = {omega:.6g}^2 \cdot {r:.6g} = {ac:.6g}\ \text{{m/s}}^2")

elif formel == "Inertimoment – standardlegemer":
    st.markdown("### Inertimomenter for standard legemer om symmetriaksen")

    st.latex(r"I = \int r^2\, dm")

    data = {
        "Tynd ring (radius R)": (r"I = MR^2", "MR2"),
        "Massiv skive/cylinder (radius R)": (r"I = \frac{1}{2}MR^2", "MR2_half"),
        "Hul cylinder (R₁, R₂)": (r"I = \frac{1}{2}M(R_1^2+R_2^2)", "hollow_cyl"),
        "Massiv kugle (radius R)": (r"I = \frac{2}{5}MR^2", "MR2_2_5"),
        "Hul kugle (radius R)": (r"I = \frac{2}{3}MR^2", "MR2_2_3"),
        "Tynd stav om centrum (længde L)": (r"I = \frac{1}{12}ML^2", "rod_center"),
        "Tynd stav om ende (længde L)": (r"I = \frac{1}{3}ML^2", "rod_end"),
        "Rektangulær plade om centrum": (r"I = \frac{1}{12}M(a^2+b^2)", "rect"),
    }

    legeme = st.selectbox("Vælg legeme:", list(data.keys()))
    latex_f, key = data[legeme]
    st.latex(latex_f)
    st.divider()

    M = st.number_input("M – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")

    if key == "MR2":
        R = st.number_input("R – radius (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = M * R**2
    elif key == "MR2_half":
        R = st.number_input("R – radius (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = 0.5 * M * R**2
    elif key == "hollow_cyl":
        c1, c2 = st.columns(2)
        R1 = c1.number_input("R₁ – indre radius (m)", value=0.2, min_value=0.0, format="%.6g")
        R2 = c2.number_input("R₂ – ydre radius (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = 0.5 * M * (R1**2 + R2**2)
    elif key == "MR2_2_5":
        R = st.number_input("R – radius (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = 0.4 * M * R**2
    elif key == "MR2_2_3":
        R = st.number_input("R – radius (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = (2/3) * M * R**2
    elif key == "rod_center":
        L = st.number_input("L – længde (m)", value=1.0, min_value=1e-12, format="%.6g")
        I = (1/12) * M * L**2
    elif key == "rod_end":
        L = st.number_input("L – længde (m)", value=1.0, min_value=1e-12, format="%.6g")
        I = (1/3) * M * L**2
    else:
        c1, c2 = st.columns(2)
        a = c1.number_input("a – bredde (m)", value=0.4, min_value=1e-12, format="%.6g")
        b = c2.number_input("b – højde (m)", value=0.3, min_value=1e-12, format="%.6g")
        I = (1/12) * M * (a**2 + b**2)

    st.success(f"**I = {I:.6g} kg·m²**")

elif formel == "Steiners sætning:  I = Icm + M·d²":
    st.latex(r"I = I_{cm} + M \cdot d^2")
    st.markdown("Inertimoment om en vilkårlig akse parallel med tyngdepunktsaksen.")
    st.divider()

    c1, c2, c3 = st.columns(3)
    Icm = c1.number_input("Icm – inertimoment om cm (kg·m²)", value=0.05, min_value=0.0, format="%.6g")
    M   = c2.number_input("M – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
    d   = c3.number_input("d – afstand fra cm til ny akse (m)", value=0.3, min_value=0.0, format="%.6g")
    I = Icm + M * d**2
    st.success(f"**I = {I:.6g} kg·m²**")
    st.latex(rf"I = I_{{cm}} + Md^2 = {Icm:.6g} + {M:.6g} \cdot {d:.6g}^2 = {I:.6g}\ \text{{kg·m}}^2")

elif formel == "Rotationskinetisk energi:  K = ½·I·ω²":
    st.latex(r"K_{rot} = \frac{1}{2} I \omega^2")
    beregn = st.radio("Beregn:", ["K – kinetisk energi (J)", "I – inertimoment (kg·m²)", "ω – vinkelhastighed (rad/s)"], horizontal=True)
    st.divider()

    if beregn == "K – kinetisk energi (J)":
        c1, c2 = st.columns(2)
        I = c1.number_input("I – inertimoment (kg·m²)", value=0.5, min_value=1e-12, format="%.6g")
        w = c2.number_input("ω – vinkelhastighed (rad/s)", value=10.0, format="%.6g")
        K = 0.5 * I * w**2
        st.success(f"**K = {K:.6g} J**")
        st.latex(rf"K = \frac{{1}}{{2}} I \omega^2 = \frac{{1}}{{2}} \cdot {I:.6g} \cdot {w:.6g}^2 = {K:.6g}\ \text{{J}}")
    elif beregn == "I – inertimoment (kg·m²)":
        c1, c2 = st.columns(2)
        K = c1.number_input("K – kinetisk energi (J)", value=25.0, format="%.6g")
        w = c2.number_input("ω (rad/s)", value=10.0, min_value=1e-12, format="%.6g")
        I = 2 * K / w**2
        st.success(f"**I = {I:.6g} kg·m²**")
    else:
        c1, c2 = st.columns(2)
        K = c1.number_input("K – kinetisk energi (J)", value=25.0, format="%.6g")
        I = c2.number_input("I – inertimoment (kg·m²)", value=0.5, min_value=1e-12, format="%.6g")
        w = np.sqrt(2 * K / I)
        st.success(f"**ω = {w:.6g} rad/s**")

elif formel == "Newtons 2. lov for rotation:  τ = I·α":
    st.latex(r"\sum \tau = I \cdot \alpha")
    beregn = st.radio("Beregn:", ["τ – nettodrejningsmoment (N·m)", "I – inertimoment (kg·m²)", "α – vinkelacceleration (rad/s²)"], horizontal=True)
    st.divider()

    if beregn == "τ – nettodrejningsmoment (N·m)":
        c1, c2 = st.columns(2)
        I = c1.number_input("I – inertimoment (kg·m²)", value=2.0, min_value=1e-12, format="%.6g")
        a = c2.number_input("α – vinkelacceleration (rad/s²)", value=3.0, format="%.6g")
        tau = I * a
        st.success(f"**τ = {tau:.6g} N·m**")
        st.latex(rf"\tau = I \cdot \alpha = {I:.6g} \cdot {a:.6g} = {tau:.6g}\ \text{{N·m}}")
    elif beregn == "I – inertimoment (kg·m²)":
        c1, c2 = st.columns(2)
        tau = c1.number_input("τ – drejningsmoment (N·m)", value=6.0, format="%.6g")
        a   = c2.number_input("α (rad/s²)", value=3.0, min_value=1e-12, format="%.6g")
        I = tau / a
        st.success(f"**I = {I:.6g} kg·m²**")
    else:
        c1, c2 = st.columns(2)
        tau = c1.number_input("τ – drejningsmoment (N·m)", value=6.0, format="%.6g")
        I   = c2.number_input("I – inertimoment (kg·m²)", value=2.0, min_value=1e-12, format="%.6g")
        a = tau / I
        st.success(f"**α = {a:.6g} rad/s²**")
        st.latex(rf"\alpha = \frac{{\tau}}{{I}} = \frac{{{tau:.6g}}}{{{I:.6g}}} = {a:.6g}\ \text{{rad/s}}^2")

elif formel == "Arbejde og effekt ved rotation":
    st.latex(r"W = \tau \cdot \Delta\theta \qquad P = \tau \cdot \omega")
    beregn = st.radio("Beregn:", ["W – arbejde (J)", "P – effekt (W)", "τ fra P og ω"], horizontal=True)
    st.divider()

    if beregn == "W – arbejde (J)":
        c1, c2 = st.columns(2)
        tau   = c1.number_input("τ – drejningsmoment (N·m)", value=10.0, format="%.6g")
        dtheta = c2.number_input("Δθ – vinkelforskydning (rad)", value=5.0, format="%.6g")
        W = tau * dtheta
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = \tau \cdot \Delta\theta = {tau:.6g} \cdot {dtheta:.6g} = {W:.6g}\ \text{{J}}")
    elif beregn == "P – effekt (W)":
        c1, c2 = st.columns(2)
        tau = c1.number_input("τ – drejningsmoment (N·m)", value=10.0, format="%.6g")
        w   = c2.number_input("ω – vinkelhastighed (rad/s)", value=5.0, format="%.6g")
        P = tau * w
        st.success(f"**P = {P:.6g} W**")
        st.latex(rf"P = \tau \cdot \omega = {tau:.6g} \cdot {w:.6g} = {P:.6g}\ \text{{W}}")
    else:
        c1, c2 = st.columns(2)
        P = c1.number_input("P – effekt (W)", value=50.0, format="%.6g")
        w = c2.number_input("ω (rad/s)", value=5.0, min_value=1e-12, format="%.6g")
        tau = P / w
        st.success(f"**τ = {tau:.6g} N·m**")

elif formel == "Rulning uden glidning":
    st.latex(r"v_{cm} = \omega R \qquad K_{total} = K_{trans} + K_{rot} = \frac{1}{2}mv^2 + \frac{1}{2}I\omega^2")
    st.markdown("For et rullende objekt: brug $v = \\omega R$ og det relevante inertimoment.")
    st.divider()

    legeme = st.selectbox("Legemets form:", ["Massiv kugle: I = 2/5·mR²", "Massiv cylinder/skive: I = 1/2·mR²", "Tynd ring: I = mR²", "Hul kugle: I = 2/3·mR²"])
    if "kugle" in legeme and "2/5" in legeme:
        c_I = 2/5
    elif "cylinder" in legeme:
        c_I = 1/2
    elif "ring" in legeme:
        c_I = 1
    else:
        c_I = 2/3

    st.divider()
    beregn = st.radio("Beregn:", ["K_total fra v og m", "v fra K_total og m", "Acceleration ned ad hældning"], horizontal=True)

    if beregn == "K_total fra v og m":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = c2.number_input("v_cm – massemidpunktshastighed (m/s)", value=5.0, format="%.6g")
        K_trans = 0.5 * m * v**2
        K_rot   = 0.5 * c_I * m * v**2
        K_total = K_trans + K_rot
        col1, col2, col3 = st.columns(3)
        col1.metric("K_trans", f"{K_trans:.4g} J")
        col2.metric("K_rot", f"{K_rot:.4g} J")
        col3.metric("K_total", f"{K_total:.4g} J")
        st.latex(rf"K = \frac{{1}}{{2}}mv^2(1 + c_I) = \frac{{1}}{{2}} \cdot {m:.6g} \cdot {v:.6g}^2 \cdot (1 + {c_I}) = {K_total:.4g}\ \text{{J}}")

    elif beregn == "v fra K_total og m":
        c1, c2 = st.columns(2)
        K = c1.number_input("K_total (J)", value=35.0, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = np.sqrt(2 * K / (m * (1 + c_I)))
        st.success(f"**v_cm = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{2K}}{{m(1+c_I)}}}} = {v:.6g}\ \text{{m/s}}")

    else:
        st.markdown("For rulning ned ad hældende plan (ingen glidning):")
        st.latex(rf"a = \frac{{g\sin\theta}}{{1 + c_I}} \quad (c_I = {c_I})")
        c1, c2 = st.columns(2)
        theta = c1.number_input("θ – hældningsvinkel (grader)", value=30.0, min_value=0.1, max_value=89.9, format="%.6g")
        g_val = c2.number_input("g (m/s²)", value=G, format="%.6g")
        a = g_val * np.sin(np.radians(theta)) / (1 + c_I)
        a_glidning = g_val * np.sin(np.radians(theta))
        st.success(f"**a = {a:.4g} m/s²**  (vs. {a_glidning:.4g} m/s² ved ren glidning)")
        st.latex(rf"a = \frac{{g\sin({theta:.4g}°)}}{{1 + {c_I}}} = {a:.4g}\ \text{{m/s}}^2")

elif formel == "Impulsmoment:  L = I·ω":
    st.latex(r"L = I \cdot \omega \qquad \vec{L} = \vec{r} \times \vec{p} = m r v \sin\theta")
    beregn = st.radio("Beregn:", ["L – impulsmoment (kg·m²/s)", "I – inertimoment (kg·m²)", "ω (rad/s)"], horizontal=True)
    st.divider()

    if beregn == "L – impulsmoment (kg·m²/s)":
        c1, c2 = st.columns(2)
        I = c1.number_input("I – inertimoment (kg·m²)", value=2.0, min_value=1e-12, format="%.6g")
        w = c2.number_input("ω – vinkelhastighed (rad/s)", value=5.0, format="%.6g")
        L = I * w
        st.success(f"**L = {L:.6g} kg·m²/s**")
        st.latex(rf"L = I \cdot \omega = {I:.6g} \cdot {w:.6g} = {L:.6g}\ \text{{kg·m}}^2\text{{/s}}")
    elif beregn == "I – inertimoment (kg·m²)":
        c1, c2 = st.columns(2)
        L = c1.number_input("L (kg·m²/s)", value=10.0, format="%.6g")
        w = c2.number_input("ω (rad/s)", value=5.0, min_value=1e-12, format="%.6g")
        I = L / w
        st.success(f"**I = {I:.6g} kg·m²**")
    else:
        c1, c2 = st.columns(2)
        L = c1.number_input("L (kg·m²/s)", value=10.0, format="%.6g")
        I = c2.number_input("I (kg·m²)", value=2.0, min_value=1e-12, format="%.6g")
        w = L / I
        st.success(f"**ω = {w:.6g} rad/s**")

elif formel == "Bevarelse af impulsmoment":
    st.latex(r"L_i = L_f \implies I_1 \omega_1 = I_2 \omega_2")
    st.markdown("Bevaret når nettodrejningsmoment = 0 (ingen ydre drejningsmomenter).")
    st.divider()

    beregn = st.radio("Beregn:", ["ω₂ – slut­vinkelhastighed (rad/s)", "I₂ – slut­inertimoment (kg·m²)"], horizontal=True, key="rot_bev_mode")
    st.divider()

    if beregn == "ω₂ – slut­vinkelhastighed (rad/s)":
        c1, c2, c3 = st.columns(3)
        I1 = c1.number_input("I₁ – start­inertimoment (kg·m²)", value=3.0, min_value=1e-12, format="%.6g")
        w1 = c2.number_input("ω₁ – startvinkelhastighed (rad/s)", value=2.0, format="%.6g")
        I2 = c3.number_input("I₂ – slut­inertimoment (kg·m²)", value=1.0, min_value=1e-12, format="%.6g")
        w2 = I1 * w1 / I2
        K1 = 0.5 * I1 * w1**2
        K2 = 0.5 * I2 * w2**2
        st.success(f"**ω₂ = {w2:.6g} rad/s**")
        st.latex(rf"\omega_2 = \frac{{I_1 \omega_1}}{{I_2}} = \frac{{{I1:.6g} \cdot {w1:.6g}}}{{{I2:.6g}}} = {w2:.6g}\ \text{{rad/s}}")
        st.markdown(f"Kinetisk energi: K₁ = {K1:.4g} J → K₂ = {K2:.4g} J  (ΔK = {K2-K1:+.4g} J)")
        if K2 > K1:
            st.info("K₂ > K₁: Intern energi konverteres til kinetisk energi (fx muskelkraft hos en skater)")
        else:
            st.info("K₂ < K₁: Kinetisk energi dissiperes (omformes til indre energi)")

    else:
        c1, c2, c3 = st.columns(3)
        I1 = c1.number_input("I₁ (kg·m²)", value=3.0, min_value=1e-12, format="%.6g", key="rot_I1")
        w1 = c2.number_input("ω₁ (rad/s)", value=2.0, format="%.6g", key="rot_w1")
        w2 = c3.number_input("ω₂ (rad/s)", value=6.0, min_value=1e-12, format="%.6g", key="rot_w2")
        I2 = I1 * w1 / w2
        st.success(f"**I₂ = {I2:.6g} kg·m²**")
        st.latex(rf"I_2 = \frac{{I_1 \omega_1}}{{\omega_2}} = \frac{{{I1:.6g} \cdot {w1:.6g}}}{{{w2:.6g}}} = {I2:.6g}\ \text{{kg·m}}^2")
        if abs(w2/w1 - 0.6) < 0.01:
            I2_tilfojet = I2 - I1
            st.info(f"📋 **2024 Q13** – Skive lander på skive: ω₂/ω₁ = 0.6 → I_total = {I2:.4g} → I₂_tilføjet = I_total − I₁ = {I2_tilfojet:.4g} = **{I2_tilfojet/I1:.4g}·I₁** (= 2/3·I₁ ✓)")

elif formel == "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)":
    st.latex(r"a = \frac{m\,g}{m + I/R^2} \qquad T = \frac{m\,g\,I/R^2}{m + I/R^2} \qquad \alpha = \frac{a}{R}")
    st.markdown("Masse m ophængt i snor om trisse (radius R, inertimoment I). Snoren glider ikke.")
    st.divider()

    c1, c2, c3 = st.columns(3)
    m = c1.number_input("m – ophængt masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
    I_trisse = c2.number_input("I – trissens inertimoment (kg·m²)", value=0.5, min_value=1e-12, format="%.6g")
    R = c3.number_input("R – trissens radius (m)", value=0.2, min_value=1e-12, format="%.6g")

    a = m * G / (m + I_trisse / R**2)
    T = m * G * (I_trisse / R**2) / (m + I_trisse / R**2)
    alpha_ang = a / R
    omega_func = f"ω = √(2aΔy/R²)·R → ω² = 2aΔy/R²... brug ω=α·t"

    st.success(f"**a = {a:.4g} m/s²**   **T = {T:.4g} N**   **α = {alpha_ang:.4g} rad/s²**")
    st.latex(rf"a = \frac{{m\,g}}{{m + I/R^2}} = \frac{{{m:.4g}\cdot{G}}}{{{m:.4g} + {I_trisse:.4g}/{R:.4g}^2}} = {a:.4g}\ \text{{m/s}}^2")
    st.latex(rf"T = m(g-a) = {m:.4g}({G} - {a:.4g}) = {m*(G-a):.4g}\ \text{{N (kontrol: T={T:.4g})}}")
    st.latex(rf"\alpha = \frac{{a}}{{R}} = \frac{{{a:.4g}}}{{{R:.4g}}} = {alpha_ang:.4g}\ \text{{rad/s}}^2")

    st.markdown("**Hastighed og vinkelhastighed efter fald Δy:**")
    dy = st.number_input("Δy – faldet afstand (m)", value=1.0, min_value=0.0, format="%.6g")
    v_end = np.sqrt(2 * a * dy)
    omega_end = v_end / R
    st.info(f"v = {v_end:.4g} m/s,   ω = {omega_end:.4g} rad/s   (efter {dy:.4g} m fald)")
    st.latex(rf"v = \sqrt{{2a\Delta y}} = \sqrt{{2\cdot{a:.4g}\cdot{dy:.4g}}} = {v_end:.4g}\ \text{{m/s}},\quad \omega = v/R = {omega_end:.4g}\ \text{{rad/s}}")
