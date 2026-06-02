import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Rotation", page_icon="🔄", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🔄", "Rotation")
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

_ROT_FORMULAS = [
    ("Vinkelkinematik",      "ω=ω₀+αt,  θ=ω₀t+½αt²",        "Vinkelkinematik (analog til lineær kinematik)"),
    ("Lineær ↔ vinkel",      "v=ωr,  aₜ=αr,  aₐ=ω²r",       "Sammenhæng lineær ↔ vinkelbevægelse"),
    ("Inertimoment",         "½MR², MR², ⅖MR², ⅟₁₂ML²",     "Inertimoment – standardlegemer"),
    ("Steiners sætning",     "I = Icm + M·d²",                "Steiners sætning:  I = Icm + M·d²"),
    ("Rotationsenergi",      "K = ½·I·ω²",                    "Rotationskinetisk energi:  K = ½·I·ω²"),
    ("τ = I·α",              "Newton for rotation",            "Newtons 2. lov for rotation:  τ = I·α"),
    ("Arbejde & effekt",     "W = τ·θ,  P = τ·ω",            "Arbejde og effekt ved rotation"),
    ("Rulning",              "v_cm = ω·R",                    "Rulning uden glidning"),
    ("Impulsmoment",         "L = I · ω",                     "Impulsmoment:  L = I·ω"),
    ("Impulsmoment-bevarelse","I₁ω₁ = I₂ω₂",                 "Bevarelse af impulsmoment"),
    ("Trisse + masse",       "mg−T=ma,  T·R=I·α",             "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)"),
]
formel = formula_card_grid(_ROT_FORMULAS, "rot_formel")

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
        "Tynd ring (radius R)":               (r"I = MR^2",                    "MR2",      1.0),
        "Massiv skive/cylinder (radius R)":   (r"I = \frac{1}{2}MR^2",         "MR2_half", 0.5),
        "Massiv kugle (radius R)":            (r"I = \frac{2}{5}MR^2",         "MR2_2_5",  0.4),
        "Hul kugle (radius R)":               (r"I = \frac{2}{3}MR^2",         "MR2_2_3",  2/3),
        "Tynd stav om centrum (længde L)":    (r"I = \frac{1}{12}ML^2",        "rod_center",1/12),
        "Tynd stav om ende (længde L)":       (r"I = \frac{1}{3}ML^2",         "rod_end",   1/3),
        "Hul cylinder (R₁, R₂)":             (r"I = \frac{1}{2}M(R_1^2+R_2^2)","hollow_cyl", None),
        "Rektangulær plade om centrum":       (r"I = \frac{1}{12}M(a^2+b^2)",  "rect",      None),
    }

    legeme = st.selectbox("Vælg legeme:", list(data.keys()))
    latex_f, key, factor = data[legeme]
    st.latex(latex_f)

    is_simple = key not in ("hollow_cyl", "rect")
    dim_label = "L – længde (m)" if "stav" in legeme else "R – radius (m)"
    dim_short = "L" if "stav" in legeme else "R"

    beregn_in = st.radio("Beregn:", (
        ["I – inertimoment (kg·m²)", f"M – masse (kg)", f"{dim_short} – mål (m)"]
        if is_simple else
        ["I – inertimoment (kg·m²)", "M – masse (kg)"]
    ), horizontal=True)
    st.divider()

    if beregn_in == "I – inertimoment (kg·m²)":
        M = st.number_input("M – masse (kg)", value=2.0, min_value=1e-12, format="%.6g", key="in_M_a")
        if key == "hollow_cyl":
            c1, c2 = st.columns(2)
            R1 = c1.number_input("R₁ – indre radius (m)", value=0.2, min_value=0.0, format="%.6g")
            R2 = c2.number_input("R₂ – ydre radius (m)", value=0.3, min_value=1e-12, format="%.6g")
            I = 0.5 * M * (R1**2 + R2**2)
        elif key == "rect":
            c1, c2 = st.columns(2)
            a = c1.number_input("a – bredde (m)", value=0.4, min_value=1e-12, format="%.6g")
            b = c2.number_input("b – højde (m)", value=0.3, min_value=1e-12, format="%.6g")
            I = (1/12) * M * (a**2 + b**2)
        else:
            dim = st.number_input(dim_label, value=0.3, min_value=1e-12, format="%.6g", key="in_dim_a")
            I = factor * M * dim**2
        st.success(f"**I = {I:.6g} kg·m²**")
        if st.button("📋 Gem I", key="gem_in_I"):
            gem_resultat(I, "kg·m²", "I")

    elif beregn_in == "M – masse (kg)":
        I_in = st.number_input("I – inertimoment (kg·m²)", value=0.1, min_value=1e-12, format="%.6g", key="in_I_b")
        if key == "hollow_cyl":
            c1, c2 = st.columns(2)
            R1 = c1.number_input("R₁ – indre radius (m)", value=0.2, min_value=0.0, format="%.6g")
            R2 = c2.number_input("R₂ – ydre radius (m)", value=0.3, min_value=1e-12, format="%.6g")
            M = 2 * I_in / (R1**2 + R2**2)
        elif key == "rect":
            c1, c2 = st.columns(2)
            a = c1.number_input("a – bredde (m)", value=0.4, min_value=1e-12, format="%.6g")
            b = c2.number_input("b – højde (m)", value=0.3, min_value=1e-12, format="%.6g")
            M = 12 * I_in / (a**2 + b**2)
        else:
            dim = st.number_input(dim_label, value=0.3, min_value=1e-12, format="%.6g", key="in_dim_b")
            M = I_in / (factor * dim**2)
        st.success(f"**M = {M:.6g} kg**")
        st.latex(rf"M = \frac{{I}}{{\text{{factor}} \cdot {dim_short}^2}} = {M:.6g}\ \text{{kg}}")
        if st.button("📋 Gem M", key="gem_in_M"):
            gem_resultat(M, "kg", "M")

    else:
        M   = st.number_input("M – masse (kg)", value=2.0, min_value=1e-12, format="%.6g", key="in_M_c")
        I_in = st.number_input("I – inertimoment (kg·m²)", value=0.1, min_value=1e-12, format="%.6g", key="in_I_c")
        dim_sq = I_in / (factor * M)
        if dim_sq <= 0:
            st.error("Ugyldig løsning")
        else:
            dim_val = np.sqrt(dim_sq)
            st.success(f"**{dim_short} = {dim_val:.6g} m**")
            st.latex(rf"{dim_short} = \sqrt{{\frac{{I}}{{\text{{factor}} \cdot M}}}} = \sqrt{{\frac{{{I_in:.6g}}}{{{factor:.4g} \cdot {M:.6g}}}}} = {dim_val:.6g}\ \text{{m}}")
            if st.button(f"📋 Gem {dim_short}", key="gem_in_dim"):
                gem_resultat(dim_val, "m", dim_short)

elif formel == "Steiners sætning:  I = Icm + M·d²":
    st.latex(r"I = I_{cm} + M \cdot d^2")
    st.markdown("Inertimoment om en vilkårlig akse parallel med tyngdepunktsaksen.")
    st.divider()

    beregn_st = st.radio("Beregn:", [
        "I – inertimoment om ny akse",
        "Icm – inertimoment om cm",
        "d – afstand fra cm til ny akse",
        "M – masse",
    ], horizontal=True)
    st.divider()

    if beregn_st == "I – inertimoment om ny akse":
        c1, c2, c3 = st.columns(3)
        Icm = c1.number_input("Icm (kg·m²)", value=0.05, min_value=0.0, format="%.6g", key="st_Icm_a")
        M   = c2.number_input("M (kg)", value=2.0, min_value=1e-12, format="%.6g", key="st_M_a")
        d   = c3.number_input("d (m)", value=0.3, min_value=0.0, format="%.6g", key="st_d_a")
        I = Icm + M * d**2
        st.success(f"**I = {I:.6g} kg·m²**")
        st.latex(rf"I = I_{{cm}} + Md^2 = {Icm:.6g} + {M:.6g} \cdot {d:.6g}^2 = {I:.6g}\ \text{{kg·m}}^2")
        if st.button("📋 Gem I", key="gem_st_I"):
            gem_resultat(I, "kg·m²", "I")

    elif beregn_st == "Icm – inertimoment om cm":
        c1, c2, c3 = st.columns(3)
        I   = c1.number_input("I – om ny akse (kg·m²)", value=0.23, min_value=0.0, format="%.6g", key="st_I_b")
        M   = c2.number_input("M (kg)", value=2.0, min_value=1e-12, format="%.6g", key="st_M_b")
        d   = c3.number_input("d (m)", value=0.3, min_value=0.0, format="%.6g", key="st_d_b")
        Icm = I - M * d**2
        if Icm < 0:
            st.error("Icm < 0 – kontrollér værdier (I skal være større end M·d²)")
        else:
            st.success(f"**Icm = {Icm:.6g} kg·m²**")
            st.latex(rf"I_{{cm}} = I - Md^2 = {I:.6g} - {M:.6g} \cdot {d:.6g}^2 = {Icm:.6g}\ \text{{kg·m}}^2")
            if st.button("📋 Gem Icm", key="gem_st_Icm"):
                gem_resultat(Icm, "kg·m²", "Icm")

    elif beregn_st == "d – afstand fra cm til ny akse":
        c1, c2, c3 = st.columns(3)
        I   = c1.number_input("I – om ny akse (kg·m²)", value=0.23, min_value=0.0, format="%.6g", key="st_I_c")
        Icm = c2.number_input("Icm (kg·m²)", value=0.05, min_value=0.0, format="%.6g", key="st_Icm_c")
        M   = c3.number_input("M (kg)", value=2.0, min_value=1e-12, format="%.6g", key="st_M_c")
        diff = I - Icm
        if diff < 0:
            st.error("I < Icm – ikke muligt (Steiners sætning kræver I ≥ Icm)")
        else:
            d = np.sqrt(diff / M)
            st.success(f"**d = {d:.6g} m**")
            st.latex(rf"d = \sqrt{{\frac{{I - I_{{cm}}}}{{M}}}} = \sqrt{{\frac{{{I:.6g} - {Icm:.6g}}}{{{M:.6g}}}}} = {d:.6g}\ \text{{m}}")
            if st.button("📋 Gem d", key="gem_st_d"):
                gem_resultat(d, "m", "d")

    else:
        c1, c2, c3 = st.columns(3)
        I   = c1.number_input("I – om ny akse (kg·m²)", value=0.23, min_value=0.0, format="%.6g", key="st_I_d")
        Icm = c2.number_input("Icm (kg·m²)", value=0.05, min_value=0.0, format="%.6g", key="st_Icm_d")
        d   = c3.number_input("d (m)", value=0.3, min_value=1e-12, format="%.6g", key="st_d_d")
        M = (I - Icm) / d**2
        if M <= 0:
            st.error("M ≤ 0 – kontrollér værdier (I skal være større end Icm)")
        else:
            st.success(f"**M = {M:.6g} kg**")
            st.latex(rf"M = \frac{{I - I_{{cm}}}}{{d^2}} = \frac{{{I:.6g} - {Icm:.6g}}}{{{d:.6g}^2}} = {M:.6g}\ \text{{kg}}")
            if st.button("📋 Gem M", key="gem_st_M"):
                gem_resultat(M, "kg", "M")

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
    beregn = st.radio("Beregn:", ["K_total fra v og m", "v fra K_total og m", "v fra faldshøjde h (energibevarelse)", "Acceleration ned ad hældning", "Identificér rullende legeme fra v og h"], horizontal=True, key="rot_rulning_mode")

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

    elif beregn == "v fra faldshøjde h (energibevarelse)":
        st.markdown("Energibevarelse: $mgh = \\frac{1}{2}mv^2(1+c_I)$ → $v = \\sqrt{\\frac{2gh}{1+c_I}}$")
        st.latex(rf"v = \sqrt{{\frac{{2gh}}{{1 + c_I}}}} \quad (c_I = {c_I})")
        c1, c2 = st.columns(2)
        h = c1.number_input("h – faldshøjde (m)", value=1.8, min_value=1e-6, format="%.6g")
        g_val = c2.number_input("g (m/s²)", value=G, format="%.6g")
        v = np.sqrt(2 * g_val * h / (1 + c_I))
        st.success(f"**v_cm = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{2 \cdot {g_val:.4g} \cdot {h:.4g}}}{{1 + {c_I}}}}} = {v:.6g}\ \text{{m/s}}")
        gem_resultat(v, "m/s", "v_cm")

    elif beregn == "Identificér rullende legeme fra v og h":
        st.markdown("Giv den målte hastighed og faldshøjden — appen finder hvilken form der passer.")
        st.latex(r"v_{forventet} = \sqrt{\frac{2gh}{1+c_I}}")
        c1, c2, c3 = st.columns(3)
        v_malt = c1.number_input("v_målt (m/s)", value=4.43, min_value=1e-6, format="%.6g")
        h      = c2.number_input("h – faldshøjde (m)", value=1.8, min_value=1e-6, format="%.6g")
        g_val  = c3.number_input("g (m/s²)", value=G, format="%.6g")
        st.divider()
        former = [
            ("Massiv kugle",        2/5,  r"I = \frac{2}{5}mR^2"),
            ("Massiv cylinder/disk",1/2,  r"I = \frac{1}{2}mR^2"),
            ("Hul kugle",           2/3,  r"I = \frac{2}{3}mR^2"),
            ("Tynd ring/hoop",      1.0,  r"I = mR^2"),
        ]
        bedste, bedste_afv = None, 1e9
        for navn, ci, _ in former:
            v_exp = np.sqrt(2 * g_val * h / (1 + ci))
            afv = abs(v_exp - v_malt)
            if afv < bedste_afv:
                bedste_afv, bedste = afv, navn
        rows = []
        for navn, ci, latex_I in former:
            v_exp = np.sqrt(2 * g_val * h / (1 + ci))
            marker = "✅" if navn == bedste else ""
            rows.append({"Form": f"{marker} {navn}", "c_I": ci, "v_forventet (m/s)": round(v_exp, 4), "Afvigelse (m/s)": round(abs(v_exp - v_malt), 4)})
        import pandas as pd
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.success(f"**Bedste match: {bedste}** (afvigelse {bedste_afv:.4g} m/s)")

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

    beregn = st.radio("Beregn:", ["ω₂ – slut­vinkelhastighed (rad/s)", "I₂ – slut­inertimoment (kg·m²)", "Partikel rammer legeme (L=mvr)"], horizontal=True, key="rot_bev_mode")
    st.divider()

    if beregn == "Partikel rammer legeme (L=mvr)":
        st.markdown("Partikel med masse **m** og hastighed **v** rammer legeme (I_legeme) i afstanden **r** fra rotationsaksen og klistrer fast.")
        st.latex(r"L_i = m\,v\,r \qquad L_f = I_{total}\,\omega_f \qquad \omega_f = \frac{m\,v\,r}{I_{total}}")
        st.markdown("*I_total = I_legeme + I_partikel_efter_stød = I_legeme + m·r²*")
        c1, c2, c3, c4 = st.columns(4)
        m_p  = c1.number_input("m – partikelens masse (kg)", value=0.002, min_value=1e-12, format="%.6g")
        v_p  = c2.number_input("v – partikelens hastighed (m/s)", value=500.0, format="%.6g")
        r_p  = c3.number_input("r – afstand fra akse til partikel (m)", value=0.5, min_value=1e-12, format="%.6g")
        I_leg = c4.number_input("I_legeme (kg·m²) – legemets inertimoment FØR stød", value=0.3125, min_value=0.0, format="%.6g")
        L_i = m_p * v_p * r_p
        I_tot = I_leg + m_p * r_p**2
        w_f = L_i / I_tot
        K_i = 0.5 * m_p * v_p**2
        K_f = 0.5 * I_tot * w_f**2
        st.success(f"**ω_f = {w_f:.6g} rad/s**")
        st.latex(rf"\omega_f = \frac{{m\,v\,r}}{{I_{{leg}} + m\,r^2}} = \frac{{{m_p:.4g} \cdot {v_p:.4g} \cdot {r_p:.4g}}}{{{I_leg:.4g} + {m_p:.4g} \cdot {r_p:.4g}^2}} = {w_f:.6g}\ \text{{rad/s}}")
        st.markdown(f"L_i = {L_i:.4g} kg·m²/s | I_total = {I_tot:.4g} kg·m² | K_i = {K_i:.4g} J → K_f = {K_f:.4g} J (tab = {K_i-K_f:.4g} J)")
        gem_resultat(w_f, "rad/s", "ω_f")

    elif beregn == "ω₂ – slut­vinkelhastighed (rad/s)":
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

    beregn_tr = st.radio("Beregn:", [
        "a, T, α – standard",
        "m – ophængt masse fra a",
        "I – trissens inertimoment fra a",
    ], horizontal=True)
    st.divider()

    if beregn_tr == "a, T, α – standard":
        c1, c2, c3 = st.columns(3)
        m        = c1.number_input("m – ophængt masse (kg)", value=2.0, min_value=1e-12, format="%.6g", key="tr_m_a")
        I_trisse = c2.number_input("I – trissens inertimoment (kg·m²)", value=0.5, min_value=1e-12, format="%.6g", key="tr_I_a")
        R        = c3.number_input("R – trissens radius (m)", value=0.2, min_value=1e-12, format="%.6g", key="tr_R_a")
        g_tr     = st.number_input("g (m/s²)", value=G, format="%.6g", key="tr_g_a")
        a = m * g_tr / (m + I_trisse / R**2)
        T = m * g_tr * (I_trisse / R**2) / (m + I_trisse / R**2)
        alpha_ang = a / R
        st.success(f"**a = {a:.4g} m/s²**   **T = {T:.4g} N**   **α = {alpha_ang:.4g} rad/s²**")
        st.latex(rf"a = \frac{{m\,g}}{{m + I/R^2}} = \frac{{{m:.4g}\cdot{g_tr:.4g}}}{{{m:.4g} + {I_trisse:.4g}/{R:.4g}^2}} = {a:.4g}\ \text{{m/s}}^2")
        st.latex(rf"T = m(g-a) = {m:.4g} \cdot ({g_tr:.4g} - {a:.4g}) = {m*(g_tr-a):.4g}\ \text{{N}}")
        st.latex(rf"\alpha = \frac{{a}}{{R}} = \frac{{{a:.4g}}}{{{R:.4g}}} = {alpha_ang:.4g}\ \text{{rad/s}}^2")
        st.markdown("**Hastighed og vinkelhastighed efter fald Δy:**")
        dy = st.number_input("Δy – faldet afstand (m)", value=1.0, min_value=0.0, format="%.6g")
        v_end = np.sqrt(2 * a * dy)
        omega_end = v_end / R
        st.info(f"v = {v_end:.4g} m/s,   ω = {omega_end:.4g} rad/s   (efter {dy:.4g} m fald)")

    elif beregn_tr == "m – ophængt masse fra a":
        st.markdown("Kendte: a, I, R, g → find **m**  via  m·g = a·(m + I/R²)  →  m = a·I/R² / (g − a)")
        c1, c2, c3 = st.columns(3)
        a_in     = c1.number_input("a – acceleration (m/s²)", value=3.0, min_value=1e-12, format="%.6g", key="tr_a_b")
        I_trisse = c2.number_input("I – trissens inertimoment (kg·m²)", value=0.5, min_value=1e-12, format="%.6g", key="tr_I_b")
        R        = c3.number_input("R – trissens radius (m)", value=0.2, min_value=1e-12, format="%.6g", key="tr_R_b")
        g_tr     = st.number_input("g (m/s²)", value=G, format="%.6g", key="tr_g_b")
        denom = g_tr - a_in
        if abs(denom) < 1e-12 or denom <= 0:
            st.error("g − a ≤ 0 – acceleration kan ikke overstige g")
        else:
            m = a_in * I_trisse / (R**2 * denom)
            st.success(f"**m = {m:.6g} kg**")
            st.latex(rf"m = \frac{{a \cdot I/R^2}}{{g - a}} = \frac{{{a_in:.4g} \cdot {I_trisse:.4g}/{R:.4g}^2}}{{{g_tr:.4g} - {a_in:.4g}}} = {m:.6g}\ \text{{kg}}")
            if st.button("📋 Gem m", key="gem_tr_m"):
                gem_resultat(m, "kg", "m")

    else:
        st.markdown("Kendte: a, m, R, g → find **I**  via  I = R²·m·(g/a − 1)")
        c1, c2, c3 = st.columns(3)
        a_in = c1.number_input("a – acceleration (m/s²)", value=3.0, min_value=1e-12, format="%.6g", key="tr_a_c")
        m    = c2.number_input("m – ophængt masse (kg)", value=2.0, min_value=1e-12, format="%.6g", key="tr_m_c")
        R    = c3.number_input("R – trissens radius (m)", value=0.2, min_value=1e-12, format="%.6g", key="tr_R_c")
        g_tr = st.number_input("g (m/s²)", value=G, format="%.6g", key="tr_g_c")
        I_trisse = R**2 * m * (g_tr / a_in - 1)
        if I_trisse <= 0:
            st.error("I ≤ 0 – acceleration kan ikke overstige g")
        else:
            st.success(f"**I = {I_trisse:.6g} kg·m²**")
            st.latex(rf"I = R^2 \cdot m \left(\frac{{g}}{{a}} - 1\right) = {R:.4g}^2 \cdot {m:.4g} \cdot \left(\frac{{{g_tr:.4g}}}{{{a_in:.4g}}} - 1\right) = {I_trisse:.6g}\ \text{{kg·m}}^2")
            if st.button("📋 Gem I", key="gem_tr_I"):
                gem_resultat(I_trisse, "kg·m²", "I")
