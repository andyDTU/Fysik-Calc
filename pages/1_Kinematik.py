import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Kinematik", page_icon="🏃", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🏃", "Kinematik")
st.title("🏃 Kinematik")
st.markdown("Beregn størrelser inden for bevægelse og kinematik")
st.divider()

G = 9.82

# Pre-fill from Eksamensopgaver guide
if st.session_state.pop("example_kinematik_2025q7", None):
    st.session_state["kin_formel"] = "Cirkulær bevægelse – RPM-omregner og centripetal"
    st.session_state["kin_rpm_mode"] = "r – radius (given ac og RPM)"
    st.session_state["kin_rpm_val"] = 10000.0
    st.session_state["kin_ac_g"] = 8500.0

if st.session_state.pop("example_kinematik_2025q4", None):
    st.session_state["kin_formel"] = "Jævnt accelereret (2):  s = v₀·t + ½·a·t²"
    st.session_state["kin_ja2_mode"] = "s (m)"
    st.session_state["kin_ja2_v0"] = 50.0
    st.session_state["kin_ja2_a"] = -9.82
    st.session_state["kin_ja2_t"] = 2.0

_KIN_FORMULAS = [
    ("Uniform bevægelse",   "s = v · t",                      "Uniform bevægelse:  s = v · t"),
    ("Jævnt acc. (1)",      "v = v₀ + a · t",                 "Jævnt accelereret (1):  v = v₀ + a · t"),
    ("Jævnt acc. (2)",      "s = v₀·t + ½·a·t²",             "Jævnt accelereret (2):  s = v₀·t + ½·a·t²"),
    ("Jævnt acc. (3)",      "v² = v₀² + 2·a·s",              "Jævnt accelereret (3):  v² = v₀² + 2·a·s"),
    ("Vertikalt kast",      "t=(v₀+√(v₀²+2gh₀))/g  ±δ",     "Vertikalt kast"),
    ("v-t-graf (stykvis)",  "x=x₀+Σ½(vᵢ+vᵢ₊₁)·Δtᵢ",        "Stykvis bevægelse (v-t-graf)"),
    ("Vandret kast",        "x = v₀·t,  y = ½·g·t²",         "Kastebevægelse (vandret kast)"),
    ("Skråt kast",          "x = v₀cosθ·t,  y = h₀+v₀sinθ·t−½gt²", "Kastebevægelse (skråt kast)"),
    ("Skråt kast – matrix", "alle v₀×θ kombinationer",        "Skråt kast – kombinationsmatrix"),
    ("Cirkulær bevægelse",  "v=ω·r,  aₐ=v²/r,  T=2π/ω",     "Cirkulær bevægelse"),
    ("Cirkulær (RPM)",      "ω = 2π·RPM/60,  r = aₐ/ω²",    "Cirkulær bevægelse – RPM-omregner og centripetal"),
    ("To kugler mødes",    "t=H/v₀,  h=v₀t−½gt²",           "To kugler mødes – lodret kast"),
]
formel = formula_card_grid(_KIN_FORMULAS, "kin_formel")

KIN_TIPS = {
    "Uniform bevægelse:  s = v · t": "Bruges ved konstant fart (acceleration = 0). Husk: s er tilbagelagt strækning.",
    "Jævnt accelereret (1):  v = v₀ + a · t": "Find slut- eller starthastighed. Brug a = −g = −9.82 m/s² ved frit fald.",
    "Jævnt accelereret (2):  s = v₀·t + ½·a·t²": "Find strækning eller tid. Sæt v₀ = 0 ved start fra ro. Diskriminant < 0 → ingen reel løsning.",
    "Jævnt accelereret (3):  v² = v₀² + 2·a·s": "Bruges når tid er ukendt. Find v eller strækning direkte fra start- og sluttilstand.",
    "Vertikalt kast": "Kastes opad (v₀ > 0) eller falder fra ro (v₀ = 0). Aktivér usikkerhed (checkbox) for eksakt fejlpropagation – typisk eksamensspørgsmål.",
    "Stykvis bevægelse (v-t-graf)": "Aflæs v_start, v_slut og Δt for hver fase direkte fra grafen. Arealet under kurven = trapez = ½(v_start+v_slut)·Δt. Konstant hastighed → rektangel (v_start=v_slut).",
    "Skråt kast – kombinationsmatrix": "Identificér hurtigt hvilket kast der passer til et givet landingspunkt. Skriv flere v₀- og θ-værdier, og angiv mål-x. Husk: sin(2·40°)=sin(2·50°) → samme rækkevidde, forskellig højde.",
    "Kastebevægelse (vandret kast)": "x-retning: uniform (v₀). y-retning: frit fald (v₀y = 0). Flyvetid t = √(2h/g).",
    "Kastebevægelse (skråt kast)": "Opdel i vₓ = v₀cos(θ) og vᵧ = v₀sin(θ). Maks. rækkevidde ved θ = 45° (uden luftmodstand).",
    "Cirkulær bevægelse": "Centripetal­acceleration peger mod centrum: ac = v²/r = ω²r. Perioden T = 2πr/v.",
    "Cirkulær bevægelse – RPM-omregner og centripetal": "RPM → ω: gang med 2π/60. Centrifuge: r = ac/ω².",
    "To kugler mødes – lodret kast": "Kugle 1 kastes opad med v₀ fra h=0; kugle 2 slippes fra H. ½gt²-leddene udligner hinanden → t_møde = H/v₀. Uafhængigt af g!",
}
show_tips(formel, KIN_TIPS)
st.divider()

# ── Uniform bevægelse ──────────────────────────────────────────────────────────
if formel == "Uniform bevægelse:  s = v · t":
    st.latex(r"s = v \cdot t")
    beregn = st.radio("Beregn:", ["s – strækning (m)", "v – hastighed (m/s)", "t – tid (s)"], horizontal=True)
    st.divider()

    if beregn == "s – strækning (m)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        t = c2.number_input("t – tid (s)", value=5.0, format="%.6g")
        s = v * t
        st.success(f"**s = {s:.6g} m**")
        st.latex(rf"s = {v:.6g} \cdot {t:.6g} = {s:.6g}\ \text{{m}}")
        if st.button("📋 Gem s", key="gem_kin_unif_s"):
            gem_resultat(s, "m", "s")

    elif beregn == "v – hastighed (m/s)":
        c1, c2 = st.columns(2)
        s = c1.number_input("s – strækning (m)", value=50.0, format="%.6g")
        t = c2.number_input("t – tid (s)", value=5.0, min_value=1e-12, format="%.6g")
        v = s / t
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \frac{{s}}{{t}} = \frac{{{s:.6g}}}{{{t:.6g}}} = {v:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_kin_unif_v"):
            gem_resultat(v, "m/s", "v")

    else:
        c1, c2 = st.columns(2)
        s = c1.number_input("s – strækning (m)", value=50.0, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        t = s / v
        st.success(f"**t = {t:.6g} s**")
        st.latex(rf"t = \frac{{s}}{{v}} = \frac{{{s:.6g}}}{{{v:.6g}}} = {t:.6g}\ \text{{s}}")
        if st.button("📋 Gem t", key="gem_kin_unif_t"):
            gem_resultat(t, "s", "t")

# ── v = v0 + at ────────────────────────────────────────────────────────────────
elif formel == "Jævnt accelereret (1):  v = v₀ + a · t":
    st.latex(r"v = v_0 + a \cdot t")
    beregn = st.radio("Beregn:", ["v (m/s)", "v₀ (m/s)", "a (m/s²)", "t (s)"], horizontal=True)
    st.divider()

    if beregn == "v (m/s)":
        c1, c2, c3 = st.columns(3)
        v0 = c1.number_input("v₀ – starthastighed (m/s)", value=0.0, format="%.6g")
        a  = c2.number_input("a – acceleration (m/s²)", value=2.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=5.0, format="%.6g")
        v = v0 + a * t
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = {v0:.6g} + {a:.6g} \cdot {t:.6g} = {v:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_kin_ja1_v"):
            gem_resultat(v, "m/s", "v")

    elif beregn == "v₀ (m/s)":
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v – sluthastighed (m/s)", value=10.0, format="%.6g")
        a  = c2.number_input("a – acceleration (m/s²)", value=2.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=5.0, format="%.6g")
        v0 = v - a * t
        st.success(f"**v₀ = {v0:.6g} m/s**")
        st.latex(rf"v_0 = v - a \cdot t = {v:.6g} - {a:.6g} \cdot {t:.6g} = {v0:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₀", key="gem_kin_ja1_v0"):
            gem_resultat(v0, "m/s", "v₀")

    elif beregn == "a (m/s²)":
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v – sluthastig­hed (m/s)", value=10.0, format="%.6g")
        v0 = c2.number_input("v₀ – starthastig­hed (m/s)", value=0.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=5.0, min_value=1e-12, format="%.6g")
        a = (v - v0) / t
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{v - v_0}}{{t}} = \frac{{{v:.6g} - {v0:.6g}}}{{{t:.6g}}} = {a:.6g}\ \text{{m/s}}^2")
        if st.button("📋 Gem a", key="gem_kin_ja1_a"):
            gem_resultat(a, "m/s²", "a")

    else:
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v – sluthastig­hed (m/s)", value=10.0, format="%.6g")
        v0 = c2.number_input("v₀ – starthastig­hed (m/s)", value=0.0, format="%.6g")
        a  = c3.number_input("a – acceleration (m/s²)", value=2.0, format="%.6g")
        if abs(a) < 1e-12:
            st.error("a = 0 – kan ikke beregne t")
        else:
            t = (v - v0) / a
            st.success(f"**t = {t:.6g} s**")
            st.latex(rf"t = \frac{{v - v_0}}{{a}} = \frac{{{v:.6g} - {v0:.6g}}}{{{a:.6g}}} = {t:.6g}\ \text{{s}}")
            if st.button("📋 Gem t", key="gem_kin_ja1_t"):
                gem_resultat(t, "s", "t")

# ── s = v0*t + 0.5*a*t^2 ──────────────────────────────────────────────────────
elif formel == "Jævnt accelereret (2):  s = v₀·t + ½·a·t²":
    st.latex(r"s = v_0 \cdot t + \tfrac{1}{2} a \cdot t^2")
    beregn = st.radio("Beregn:", ["s (m)", "v₀ (m/s)", "a (m/s²)", "t (s)"], horizontal=True, key="kin_ja2_mode")
    st.divider()

    if beregn == "s (m)":
        c1, c2, c3 = st.columns(3)
        v0 = c1.number_input("v₀ (m/s)", value=0.0, format="%.6g", key="kin_ja2_v0")
        a  = c2.number_input("a (m/s²)", value=2.0, format="%.6g", key="kin_ja2_a")
        t  = c3.number_input("t (s)", value=5.0, format="%.6g", key="kin_ja2_t")
        s = v0 * t + 0.5 * a * t**2
        st.success(f"**s = {s:.6g} m**")
        st.latex(rf"s = {v0:.6g} \cdot {t:.6g} + \tfrac{{1}}{{2}} \cdot {a:.6g} \cdot {t:.6g}^2 = {s:.6g}\ \text{{m}}")
        if st.button("📋 Gem s", key="gem_kin_ja2_s"):
            gem_resultat(s, "m", "s")
        if abs(v0 - 50.0) < 0.01 and abs(a + 9.82) < 0.01 and abs(t - 2.0) < 0.01:
            st.info("📋 **2025 Q4** – To bolde mødes: bold 1 kastes op (v₀=50 m/s), bold 2 slippes fra 100 m. De mødes ved h ≈ 80.4 m (t=2 s). ✓")

    elif beregn == "v₀ (m/s)":
        c1, c2, c3 = st.columns(3)
        s = c1.number_input("s (m)", value=25.0, format="%.6g")
        a = c2.number_input("a (m/s²)", value=2.0, format="%.6g")
        t = c3.number_input("t (s)", value=5.0, min_value=1e-12, format="%.6g")
        v0 = (s - 0.5 * a * t**2) / t
        st.success(f"**v₀ = {v0:.6g} m/s**")
        st.latex(rf"v_0 = \frac{{s - \frac{{1}}{{2}}a t^2}}{{t}} = {v0:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₀", key="gem_kin_ja2_v0"):
            gem_resultat(v0, "m/s", "v₀")

    elif beregn == "a (m/s²)":
        c1, c2, c3 = st.columns(3)
        s  = c1.number_input("s (m)", value=25.0, format="%.6g")
        v0 = c2.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        t  = c3.number_input("t (s)", value=5.0, min_value=1e-12, format="%.6g")
        a = 2 * (s - v0 * t) / t**2
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{2(s - v_0 t)}}{{t^2}} = {a:.6g}\ \text{{m/s}}^2")
        if st.button("📋 Gem a", key="gem_kin_ja2_a"):
            gem_resultat(a, "m/s²", "a")

    else:
        c1, c2, c3 = st.columns(3)
        s  = c1.number_input("s (m)", value=25.0, format="%.6g")
        v0 = c2.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        a  = c3.number_input("a (m/s²)", value=2.0, format="%.6g")
        if abs(a) < 1e-12:
            if abs(v0) < 1e-12:
                st.error("Kan ikke beregne t: a=0 og v₀=0")
            else:
                t = s / v0
                st.success(f"**t = {t:.6g} s**")
                if st.button("📋 Gem t", key="gem_kin_ja2_t_lin"):
                    gem_resultat(t, "s", "t")
        else:
            disc = v0**2 + 2 * a * s
            if disc < 0:
                st.error("Ingen reel løsning (diskriminant < 0)")
            else:
                t1 = (-v0 + np.sqrt(disc)) / a
                t2 = (-v0 - np.sqrt(disc)) / a
                solutions = sorted([t for t in [t1, t2] if t >= -1e-9])
                if not solutions:
                    st.error("Ingen positiv tidsløsning")
                elif len(solutions) == 1 or abs(solutions[0] - solutions[1]) < 1e-9:
                    st.success(f"**t = {solutions[0]:.6g} s**")
                    if st.button("📋 Gem t", key="gem_kin_ja2_t1"):
                        gem_resultat(solutions[0], "s", "t")
                else:
                    st.success(f"**t₁ = {solutions[0]:.6g} s  |  t₂ = {solutions[1]:.6g} s**")
                    st.info("To løsninger – vælg den fysisk meningsfulde.")
                    c_a, c_b = st.columns(2)
                    if c_a.button(f"📋 Gem t₁ = {solutions[0]:.6g} s", key="gem_kin_ja2_ta"):
                        gem_resultat(solutions[0], "s", "t₁")
                    if c_b.button(f"📋 Gem t₂ = {solutions[1]:.6g} s", key="gem_kin_ja2_tb"):
                        gem_resultat(solutions[1], "s", "t₂")

# ── v^2 = v0^2 + 2as ──────────────────────────────────────────────────────────
elif formel == "Jævnt accelereret (3):  v² = v₀² + 2·a·s":
    st.latex(r"v^2 = v_0^2 + 2 \cdot a \cdot s")
    beregn = st.radio("Beregn:", ["v (m/s)", "v₀ (m/s)", "a (m/s²)", "s (m)"], horizontal=True)
    st.divider()

    if beregn == "v (m/s)":
        c1, c2, c3 = st.columns(3)
        v0 = c1.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        a  = c2.number_input("a (m/s²)", value=2.0, format="%.6g")
        s  = c3.number_input("s (m)", value=25.0, format="%.6g")
        val = v0**2 + 2 * a * s
        if val < 0:
            st.error("v² < 0 – ingen reel løsning")
        else:
            v = np.sqrt(val)
            st.success(f"**v = {v:.6g} m/s**")
            st.latex(rf"v = \sqrt{{v_0^2 + 2as}} = \sqrt{{{v0:.6g}^2 + 2 \cdot {a:.6g} \cdot {s:.6g}}} = {v:.6g}\ \text{{m/s}}")
            if st.button("📋 Gem v", key="gem_kin_ja3_v"):
                gem_resultat(v, "m/s", "v")

    elif beregn == "v₀ (m/s)":
        c1, c2, c3 = st.columns(3)
        v = c1.number_input("v (m/s)", value=10.0, format="%.6g")
        a = c2.number_input("a (m/s²)", value=2.0, format="%.6g")
        s = c3.number_input("s (m)", value=25.0, format="%.6g")
        val = v**2 - 2 * a * s
        if val < 0:
            st.error("v₀² < 0 – ingen reel løsning")
        else:
            v0 = np.sqrt(val)
            st.success(f"**v₀ = {v0:.6g} m/s**")
            st.latex(rf"v_0 = \sqrt{{v^2 - 2as}} = {v0:.6g}\ \text{{m/s}}")
            if st.button("📋 Gem v₀", key="gem_kin_ja3_v0"):
                gem_resultat(v0, "m/s", "v₀")

    elif beregn == "a (m/s²)":
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v (m/s)", value=10.0, format="%.6g")
        v0 = c2.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        s  = c3.number_input("s (m)", value=25.0, format="%.6g")
        if abs(s) < 1e-12:
            st.error("s = 0 – kan ikke beregne a")
        else:
            a = (v**2 - v0**2) / (2 * s)
            st.success(f"**a = {a:.6g} m/s²**")
            st.latex(rf"a = \frac{{v^2 - v_0^2}}{{2s}} = {a:.6g}\ \text{{m/s}}^2")
            if st.button("📋 Gem a", key="gem_kin_ja3_a"):
                gem_resultat(a, "m/s²", "a")

    else:
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v (m/s)", value=10.0, format="%.6g")
        v0 = c2.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        a  = c3.number_input("a (m/s²)", value=2.0, format="%.6g")
        if abs(a) < 1e-12:
            st.error("a = 0 – kan ikke beregne s")
        else:
            s = (v**2 - v0**2) / (2 * a)
            st.success(f"**s = {s:.6g} m**")
            st.latex(rf"s = \frac{{v^2 - v_0^2}}{{2a}} = {s:.6g}\ \text{{m}}")
            if st.button("📋 Gem s", key="gem_kin_ja3_s"):
                gem_resultat(s, "m", "s")

# ── Vertikalt kast ─────────────────────────────────────────────────────────────
elif formel == "Vertikalt kast":
    st.latex(r"y(t) = h_0 + v_0 \cdot t - \tfrac{1}{2}g \cdot t^2 = 0 \quad\Rightarrow\quad t = \frac{v_0 + \sqrt{v_0^2 + 2g h_0}}{g}")
    st.markdown("Sten kastes **lodret opad** fra højden **h₀** med starthastighed **v₀** (opad = positiv). Beregner landingstidspunkt, maks. højde og landingshastighed.")

    vis_usk = st.checkbox("Medtag usikkerhed (fejlpropagation)", key="kin_vkast_usk")
    st.divider()

    if not vis_usk:
        c1, c2, c3 = st.columns(3)
        h0 = c1.number_input("h₀ – starthøjde (m)", value=1.60, min_value=0.0, format="%.6g")
        v0 = c2.number_input("v₀ – starthastighed opad (m/s)", value=4.20, format="%.6g")
        g  = c3.number_input("g – tyngdeaccl. (m/s²)", value=9.82, min_value=0.001, format="%.6g")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**h₀ (m)**")
            h0  = st.number_input("h₀", value=1.60, min_value=0.0, format="%.6g", label_visibility="collapsed", key="kin_vkast_h0")
            dh0 = st.number_input("δh₀ (m)", value=0.05, min_value=0.0, format="%.6g", key="kin_vkast_dh0")
        with c2:
            st.markdown("**v₀ (m/s)**")
            v0  = st.number_input("v₀", value=4.20, format="%.6g", label_visibility="collapsed", key="kin_vkast_v0")
            dv0 = st.number_input("δv₀ (m/s)", value=0.05, min_value=0.0, format="%.6g", key="kin_vkast_dv0")
        with c3:
            st.markdown("**g (m/s²)**")
            g   = st.number_input("g", value=9.82, min_value=0.001, format="%.6g", label_visibility="collapsed", key="kin_vkast_g")
            dg  = st.number_input("δg (m/s²)", value=0.01, min_value=0.0, format="%.6g", key="kin_vkast_dg")

    disc = v0**2 + 2.0 * g * h0
    if disc < 0:
        st.error("Ingen reel løsning: v₀² + 2·g·h₀ < 0")
        st.stop()

    D      = np.sqrt(disc)
    t_land = (v0 + D) / g
    h_max  = h0 + v0**2 / (2.0 * g)
    t_top  = max(v0 / g, 0.0)
    v_land = D  # = √(v₀² + 2·g·h₀)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Landingstid  t", f"{t_land:.4g} s")
    col2.metric("Maks. højde  h_max", f"{h_max:.4g} m")
    col3.metric("Tid til top", f"{t_top:.4g} s")
    col4.metric("Landingshastighed", f"{v_land:.4g} m/s")

    if vis_usk:
        # ── Fejlpropagation for t_land ──
        dt_dh0 = 1.0 / D
        dt_dv0 = (D + v0) / (g * D)
        dt_dg  = (-v0 * D - v0**2 - g * h0) / (g**2 * D)
        dt = np.sqrt((dt_dh0 * dh0)**2 + (dt_dv0 * dv0)**2 + (dt_dg * dg)**2)

        # ── Fejlpropagation for v_land = D = √(v₀²+2g·h₀) ──
        dv_dv0 = v0 / D
        dv_dg  = h0 / D
        dv_dh0 = g  / D
        dv = np.sqrt((dv_dv0 * dv0)**2 + (dv_dg * dg)**2 + (dv_dh0 * dh0)**2)

        # ── Fejlpropagation for h_max = h₀ + v₀²/(2g) ──
        dhm_dh0 = 1.0
        dhm_dv0 = v0 / g
        dhm_dg  = -v0**2 / (2.0 * g**2)
        dhm = np.sqrt((dhm_dh0 * dh0)**2 + (dhm_dv0 * dv0)**2 + (dhm_dg * dg)**2)

        st.success(
            f"**t = {t_land:.4g} ± {dt:.2g} s**  "
            f" |  **h_max = {h_max:.4g} ± {dhm:.2g} m**  "
            f" |  **v_land = {v_land:.4g} ± {dv:.2g} m/s**"
        )

        # ── Bidragsrangering (til eksamensspørgsmål som "hvem dominerer?") ──
        contrib = {"δt(v₀)": abs(dt_dv0 * dv0), "δt(h₀)": abs(dt_dh0 * dh0), "δt(g)": abs(dt_dg * dg)}
        ranked = sorted(contrib.items(), key=lambda x: x[1], reverse=True)
        rank_str = " > ".join(f"**{k}** ({v:.4g} s)" for k, v in ranked)
        st.info(f"Bidragsrangering: {rank_str}")

        with st.expander("Vis fejlpropagation – landingstid t"):
            st.latex(r"D = \sqrt{v_0^2 + 2g h_0}, \quad t = \frac{v_0 + D}{g}")
            st.latex(
                r"\frac{\partial t}{\partial h_0} = \frac{1}{D}, \quad"
                r"\frac{\partial t}{\partial v_0} = \frac{D + v_0}{g D}, \quad"
                r"\frac{\partial t}{\partial g} = \frac{-v_0 D - v_0^2 - g h_0}{g^2 D}"
            )
            st.latex(
                r"\delta t = \sqrt{\!\left(\frac{\partial t}{\partial h_0}\delta h_0\right)^{\!2}"
                r"+\left(\frac{\partial t}{\partial v_0}\delta v_0\right)^{\!2}"
                r"+\left(\frac{\partial t}{\partial g}\delta g\right)^{\!2}}"
            )
            st.markdown(f"""
| Bidrag | Partiel afledede | Usikkerhed | Bidrag til δt |
|--------|-----------------|------------|--------------|
| ∂t/∂h₀ | {dt_dh0:.5g} s/m | δh₀ = {dh0:.4g} m | {dt_dh0*dh0:.5g} s |
| ∂t/∂v₀ | {dt_dv0:.5g} s/(m/s) | δv₀ = {dv0:.4g} m/s | {dt_dv0*dv0:.5g} s |
| ∂t/∂g  | {dt_dg:.5g} s/(m/s²) | δg = {dg:.4g} m/s² | {abs(dt_dg*dg):.5g} s |
| **δt** | | | **{dt:.5g} s** |
""")

        with st.expander("Vis fejlpropagation – h_max og v_land"):
            st.latex(r"h_{max} = h_0 + \frac{v_0^2}{2g}")
            st.latex(
                rf"\delta h_{{max}} = \sqrt{{(\delta h_0)^2 + \left(\frac{{v_0}}{{g}}\delta v_0\right)^2"
                rf" + \left(\frac{{v_0^2}}{{2g^2}}\delta g\right)^2}} = {dhm:.5g}\ \text{{m}}"
            )
            st.latex(r"v_{land} = \sqrt{v_0^2 + 2g h_0} = D")
            st.latex(
                rf"\delta v_{{land}} = \sqrt{{\left(\frac{{v_0}}{{D}}\delta v_0\right)^2"
                rf" + \left(\frac{{h_0}}{{D}}\delta g\right)^2"
                rf" + \left(\frac{{g}}{{D}}\delta h_0\right)^2}} = {dv:.5g}\ \text{{m/s}}"
            )

        if abs(h0 - 1.60) < 0.01 and abs(v0 - 4.20) < 0.01 and abs(g - 9.82) < 0.01:
            st.info("📋 **Eksempel (Spg. 1)** – svar I: t = 1.141 ± 0.011 s ✓")
    else:
        with st.expander("Vis udregning"):
            st.latex(rf"D = \sqrt{{{v0:.6g}^2 + 2 \cdot {g:.6g} \cdot {h0:.6g}}} = {D:.6g}")
            st.latex(rf"t = \frac{{{v0:.6g} + {D:.6g}}}{{{g:.6g}}} = {t_land:.6g}\ \text{{s}}")
            st.latex(rf"h_{{max}} = {h0:.6g} + \frac{{{v0:.6g}^2}}{{2 \cdot {g:.6g}}} = {h_max:.6g}\ \text{{m}}")
            st.latex(rf"v_{{land}} = D = {v_land:.6g}\ \text{{m/s}}")

    ca, cb, cc = st.columns(3)
    if ca.button("📋 Gem t", key="gem_kin_vkast_t"):
        gem_resultat(t_land, "s", "t")
    if cb.button("📋 Gem h_max", key="gem_kin_vkast_hmax"):
        gem_resultat(h_max, "m", "h_max")
    if cc.button("📋 Gem v_land", key="gem_kin_vkast_vlnd"):
        gem_resultat(v_land, "m/s", "v_land")

# ── Stykvis bevægelse (v-t-graf) ───────────────────────────────────────────────
elif formel == "Stykvis bevægelse (v-t-graf)":
    st.latex(r"x = x_0 + \sum_{i} \underbrace{\frac{v_{i,\text{start}} + v_{i,\text{slut}}}{2} \cdot \Delta t_i}_{\text{trapez-areal fase } i}")
    st.markdown("Aflæs **v_start**, **v_slut** og **Δt** for hver fase direkte fra grafen. Konstant hastighed: sæt v_start = v_slut (rektangel). Op til 4 faser.")
    st.divider()

    c_x0, c_n = st.columns([2, 1])
    x0 = c_x0.number_input("x₀ – startposition ved t=0 (m)", value=10.0, format="%.6g")
    n_faser = c_n.radio("Antal faser:", [2, 3, 4], horizontal=False, key="kin_pw_n")
    st.divider()

    _DEFAULT_VS  = [4.0, 4.0,  0.0,  0.0]
    _DEFAULT_VE  = [4.0, 10.0, 0.0,  0.0]
    _DEFAULT_DT  = [4.0, 6.0,  0.0,  0.0]

    phase_data = []
    cols_header = st.columns([1, 2, 2, 2, 2])
    cols_header[0].markdown("**Fase**")
    cols_header[1].markdown("**v_start (m/s)**")
    cols_header[2].markdown("**v_slut (m/s)**")
    cols_header[3].markdown("**Δt (s)**")
    cols_header[4].markdown("**Areal (m)**")

    t_cumul = 0.0
    for i in range(n_faser):
        row = st.columns([1, 2, 2, 2, 2])
        row[0].markdown(f"**{i+1}**")
        vs = row[1].number_input("v_s", value=_DEFAULT_VS[i], format="%.6g",
                                  label_visibility="collapsed", key=f"kin_pw_vs_{i}")
        ve = row[2].number_input("v_e", value=_DEFAULT_VE[i], format="%.6g",
                                  label_visibility="collapsed", key=f"kin_pw_ve_{i}")
        dt = row[3].number_input("dt", value=_DEFAULT_DT[i], min_value=0.0, format="%.6g",
                                  label_visibility="collapsed", key=f"kin_pw_dt_{i}")
        area = 0.5 * (vs + ve) * dt
        row[4].markdown(f"{area:.6g}")
        phase_data.append((vs, ve, dt, area, t_cumul))
        t_cumul += dt

    total_area = sum(p[3] for p in phase_data)
    x_final    = x0 + total_area

    st.divider()
    col_res = st.columns(3)
    col_res[0].metric("Samlet strækning Δx", f"{total_area:.6g} m")
    col_res[1].metric("Slutposition x", f"{x_final:.6g} m")
    col_res[2].metric("Samlet tid", f"{t_cumul:.6g} s")

    with st.expander("Vis fase-for-fase udregning"):
        rows_md = "| Fase | Interval | v_start | v_slut | Δt | Areal |\n|------|----------|---------|--------|----|-------|\n"
        x_run = x0
        for i, (vs, ve, dt, area, t0) in enumerate(phase_data):
            x_run += area
            shape = "rektangel" if abs(vs - ve) < 1e-9 else "trapez"
            rows_md += f"| {i+1} | {t0:.4g}→{t0+dt:.4g} s | {vs:.6g} m/s | {ve:.6g} m/s | {dt:.6g} s | {area:.6g} m ({shape}) |\n"
        rows_md += f"| **Total** | | | | {t_cumul:.6g} s | **{total_area:.6g} m** |"
        st.markdown(rows_md)
        st.latex(rf"x = {x0:.6g} + {total_area:.6g} = {x_final:.6g}\ \text{{m}}")

    # Genkend eksamenseksemplet (Spg. 3)
    if (abs(x0 - 10.0) < 0.01 and n_faser == 2
            and abs(phase_data[0][0] - 4) < 0.1 and abs(phase_data[0][1] - 4) < 0.1
            and abs(phase_data[0][2] - 4) < 0.1
            and abs(phase_data[1][0] - 4) < 0.1 and abs(phase_data[1][1] - 10) < 0.1
            and abs(phase_data[1][2] - 6) < 0.1):
        st.info("📋 **Eksempel (Spg. 3)** – svar I: x = 68.0 m ✓")

    if st.button("📋 Gem x", key="gem_kin_pw_x"):
        gem_resultat(x_final, "m", "x")

# ── Vandret kast ───────────────────────────────────────────────────────────────
elif formel == "Kastebevægelse (vandret kast)":
    st.latex(r"\text{Vandret: }x = v_0 \cdot t \qquad \text{Lodret: }y = \tfrac{1}{2} g \cdot t^2")
    st.markdown("Startes vandret (v₀ₓ = v₀, v₀ᵧ = 0) fra højden h.")
    st.divider()

    beregn_vkast = st.radio("Beregn:", ["x og slutfart (given v₀ og h)", "v₀ – given rækkevidde x og højde h"], horizontal=True)
    st.divider()

    if beregn_vkast == "x og slutfart (given v₀ og h)":
        c1, c2 = st.columns(2)
        v0 = c1.number_input("v₀ – vandret starthastighed (m/s)", value=15.0, min_value=0.001, format="%.6g")
        h  = c2.number_input("h – starthøjde (m)", value=20.0, min_value=0.001, format="%.6g")
        t = np.sqrt(2 * h / G)
        x = v0 * t
        vy = G * t
        v_end = np.sqrt(v0**2 + vy**2)
        theta = np.degrees(np.arctan(vy / v0))
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Flyvetid t", f"{t:.4g} s")
        col2.metric("Rækkevidde x", f"{x:.4g} m")
        col3.metric("Slutfart", f"{v_end:.4g} m/s")
        col4.metric("Nedslagsvinkel", f"{theta:.4g}°")
        with st.expander("Vis udregning"):
            st.latex(rf"t = \sqrt{{\frac{{2h}}{{g}}}} = {t:.6g}\ \text{{s}},\quad x = v_0 t = {x:.6g}\ \text{{m}}")
            st.latex(rf"v_y = g t = {vy:.6g}\ \text{{m/s}},\quad v_{{slut}} = \sqrt{{v_0^2 + v_y^2}} = {v_end:.6g}\ \text{{m/s}}")
        ca, cb = st.columns(2)
        if ca.button("📋 Gem x", key="gem_kin_vkast_x"):
            gem_resultat(x, "m", "x")
        if cb.button("📋 Gem v_slut", key="gem_kin_vkast_vslut"):
            gem_resultat(v_end, "m/s", "v_slut")
    else:
        c1, c2 = st.columns(2)
        x_mål = c1.number_input("x – rækkevidde (m)", value=30.0, min_value=0.001, format="%.6g")
        h     = c2.number_input("h – starthøjde (m)", value=20.0, min_value=0.001, format="%.6g")
        t = np.sqrt(2 * h / G)
        v0_calc = x_mål / t
        vy = G * t
        v_end = np.sqrt(v0_calc**2 + vy**2)
        st.success(f"**v₀ = {v0_calc:.4g} m/s**   (flyvetid t = {t:.4g} s)")
        st.latex(rf"t = \sqrt{{\frac{{2h}}{{g}}}} = {t:.6g}\ \text{{s}},\quad v_0 = \frac{{x}}{{t}} = \frac{{{x_mål:.4g}}}{{{t:.4g}}} = {v0_calc:.4g}\ \text{{m/s}}")
        if st.button("📋 Gem v₀", key="gem_kin_vkast_v0"):
            gem_resultat(v0_calc, "m/s", "v₀")

# ── Skråt kast ─────────────────────────────────────────────────────────────────
elif formel == "Kastebevægelse (skråt kast)":
    st.latex(r"x = v_0 \cos\theta \cdot t \qquad y = h_0 + v_0 \sin\theta \cdot t - \tfrac{1}{2}g t^2")
    st.divider()

    c1, c2, c3 = st.columns(3)
    v0    = c1.number_input("v₀ – starthastighed (m/s)", value=20.0, min_value=0.001, format="%.6g")
    theta = c2.number_input("θ – affyringsvinkel (grader)", value=45.0, min_value=0.1, max_value=89.9, format="%.6g")
    h0    = c3.number_input("h₀ – starthøjde (m, 0=fra jorden)", value=0.0, format="%.6g")

    th_r = np.radians(theta)
    v0x = v0 * np.cos(th_r)
    v0y = v0 * np.sin(th_r)
    t_top = v0y / G
    h_max = h0 + v0y**2 / (2 * G)

    disc = v0y**2 + 2 * G * h0
    if disc < 0:
        st.error("Bolden når ikke ned – diskriminant < 0")
        st.stop()
    t_land = (v0y + np.sqrt(disc)) / G
    x_max = v0x * t_land

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Flyvetid", f"{t_land:.4g} s")
    col2.metric("Maks. rækkevidde", f"{x_max:.4g} m")
    col3.metric("Maks. højde", f"{h_max:.4g} m")
    col4.metric("Tid til top", f"{t_top:.4g} s")

    with st.expander("Vis udregning"):
        st.latex(rf"v_{{0x}} = {v0:.6g}\cos({theta:.4g}°) = {v0x:.6g}\ \text{{m/s}}")
        st.latex(rf"v_{{0y}} = {v0:.6g}\sin({theta:.4g}°) = {v0y:.6g}\ \text{{m/s}}")
        st.latex(rf"t_{{top}} = \frac{{v_{{0y}}}}{{g}} = {t_top:.6g}\ \text{{s}},\quad h_{{max}} = h_0 + \frac{{v_{{0y}}^2}}{{2g}} = {h_max:.6g}\ \text{{m}}")
        st.latex(rf"t_{{land}}: \quad 0 = h_0 + v_{{0y}}t - \tfrac{{1}}{{2}}gt^2 \Rightarrow t = \frac{{v_{{0y}} + \sqrt{{v_{{0y}}^2 + 2g h_0}}}}{{g}} = {t_land:.6g}\ \text{{s}}")
        st.latex(rf"x_{{max}} = v_{{0x}} \cdot t_{{land}} = {v0x:.6g} \cdot {t_land:.6g} = {x_max:.6g}\ \text{{m}}")

    ca, cb, cc = st.columns(3)
    if ca.button("📋 Gem x_max", key="gem_kin_skrat_x"):
        gem_resultat(x_max, "m", "x_max")
    if cb.button("📋 Gem h_max", key="gem_kin_skrat_h"):
        gem_resultat(h_max, "m", "h_max")
    if cc.button("📋 Gem t_land", key="gem_kin_skrat_t"):
        gem_resultat(t_land, "s", "t_land")

# ── Skråt kast – kombinationsmatrix ────────────────────────────────────────────
elif formel == "Skråt kast – kombinationsmatrix":
    st.latex(r"x = \frac{v_0^2\sin(2\theta)}{g} \qquad h_{max} = \frac{v_0^2\sin^2\!\theta}{2g} \qquad t = \frac{2v_0\sin\theta}{g}")
    st.markdown("Generer en tabel over **alle kombinationer** af v₀ og θ. Brug **Find match** til at identificere kastet fra en graf.")
    st.divider()

    c1, c2, c3 = st.columns(3)
    v0_str    = c1.text_input("v₀-værdier (m/s), komma-adskilt", value="10, 11, 12", key="kin_mat_v0")
    theta_str = c2.text_input("θ-værdier (grader), komma-adskilt", value="40, 50, 60", key="kin_mat_th")
    g_mat     = c3.number_input("g (m/s²)", value=9.82, min_value=0.001, format="%.6g", key="kin_mat_g")

    st.divider()
    match_mode = st.radio("Find match:", [
        "Ingen filter",
        "📍 Landingspunkt x  (y = 0)",
        "📍 Punkt på banen  (x, y)",
        "📏 Maksimalhøjde  h_max",
    ], horizontal=True, key="kin_mat_mode")

    tol = st.number_input("Tolerance ±", value=0.3, min_value=0.0, format="%.4g", key="kin_mat_tol",
                          help="Bruges af alle match-modes. Enhed: m")

    target_x = target_y = h_min = h_max_filt = 0.0
    if match_mode == "📍 Landingspunkt x  (y = 0)":
        target_x = st.number_input("Mål-x – landingspunkt (m)", value=10.7, min_value=0.0, format="%.4g", key="kin_mat_tx")
    elif match_mode == "📍 Punkt på banen  (x, y)":
        c_px, c_py = st.columns(2)
        target_x = c_px.number_input("x – vandret afstand (m)", value=8.0, min_value=0.0, format="%.4g", key="kin_mat_px")
        target_y = c_py.number_input("y – højde i det punkt (m)", value=3.0, min_value=0.0, format="%.4g", key="kin_mat_py")
    elif match_mode == "📏 Maksimalhøjde  h_max":
        c_h1, c_h2 = st.columns(2)
        h_min      = c_h1.number_input("h_max mindst (m)", value=4.0, min_value=0.0, format="%.4g", key="kin_mat_hmin")
        h_max_filt = c_h2.number_input("h_max højest (m, 0 = ingen øvre grænse)", value=5.0, min_value=0.0, format="%.4g", key="kin_mat_hmax")

    try:
        v0_list    = [float(v.strip()) for v in v0_str.split(",") if v.strip()]
        theta_list = [float(t.strip()) for t in theta_str.split(",") if t.strip()]
    except ValueError:
        st.error("Tjek at v₀ og θ kun indeholder tal adskilt af kommaer.")
        st.stop()

    if not v0_list or not theta_list:
        st.warning("Angiv mindst én v₀- og én θ-værdi.")
        st.stop()

    # ── Byg tabel ──
    rows = []
    matches = []
    for v0v in v0_list:
        for thv in theta_list:
            th_r = np.radians(thv)
            x_r  = v0v**2 * np.sin(2 * th_r) / g_mat
            h_r  = v0v**2 * np.sin(th_r)**2  / (2 * g_mat)
            t_r  = 2 * v0v * np.sin(th_r)    / g_mat

            if match_mode == "📍 Landingspunkt x  (y = 0)":
                hit = abs(x_r - target_x) <= tol
            elif match_mode == "📍 Punkt på banen  (x, y)":
                # Baneformel: y_calc = x*tanθ − g*x²/(2*v₀²*cos²θ)
                y_calc = target_x * np.tan(th_r) - g_mat * target_x**2 / (2 * v0v**2 * np.cos(th_r)**2)
                hit = (target_x <= x_r) and (abs(y_calc - target_y) <= tol)
            elif match_mode == "📏 Maksimalhøjde  h_max":
                hit = (h_r >= h_min - tol) and (h_max_filt == 0 or h_r <= h_max_filt + tol)
            else:
                hit = False

            rows.append((v0v, thv, x_r, h_r, t_r, hit))
            if hit:
                matches.append((v0v, thv, x_r, h_r))

    # Markdown-tabel
    header = "| v₀ (m/s) | θ (°) | x_max (m) | h_max (m) | t_land (s) | Match |"
    sep    = "|----------|-------|-----------|-----------|------------|-------|"
    lines  = [header, sep]
    for v0v, thv, x_r, h_r, t_r, hit in rows:
        mark = "**✓**" if hit else ""
        bold = lambda s: f"**{s}**" if hit else str(s)
        row_str = f"| {bold(v0v)} | {bold(str(thv)+'°')} | {bold(f'{x_r:.3f}')} | {bold(f'{h_r:.3f}')} | {t_r:.3f} | {mark} |"
        lines.append(row_str)
    st.markdown("\n".join(lines))

    if matches:
        mode_label = {
            "📍 Landingspunkt x  (y = 0)": f"lander ved x ≈ {target_x:.4g} m",
            "📍 Punkt på banen  (x, y)":   f"passerer gennem ({target_x:.4g}, {target_y:.4g}) m",
            "📏 Maksimalhøjde  h_max":      f"har h_max i [{h_min:.4g}–{h_max_filt:.4g}] m",
        }.get(match_mode, "")
        st.success(
            f"Kast der {mode_label}:  " +
            "  |  ".join(f"**v₀={v0v} m/s, θ={thv}°** → x={x_r:.3f} m, h={h_r:.3f} m"
                         for v0v, thv, x_r, h_r in matches)
        )
        if len(matches) > 1 and match_mode == "📍 Landingspunkt x  (y = 0)":
            st.info("Flere kast matcher samme landingspunkt. Skift til **'Punkt på banen'** eller **'Maksimalhøjde'** for at skelne dem.")
    elif match_mode != "Ingen filter":
        st.warning("Ingen kombinationer matcher. Prøv at øge tolerancen eller justér filterværdierne.")

    st.caption("Tip: sin(2·40°) = sin(2·50°) ≈ 0.985 → 40° og 50° giver altid samme rækkevidde med samme v₀, men forskellig højde.")

# ── Cirkulær bevægelse ─────────────────────────────────────────────────────────
elif formel == "Cirkulær bevægelse":
    st.latex(r"v = \omega \cdot r \qquad a_c = \frac{v^2}{r} = \omega^2 r \qquad T = \frac{2\pi}{\omega}")
    beregn = st.radio("Beregn:", ["v – banehastighed (m/s)", "ω – vinkelhastighed (rad/s)", "r – radius (m)", "ac – centripetal­acceleration (m/s²)", "T – omløbstid (s)", "f – frekvens (Hz)"], horizontal=True)
    st.divider()

    if beregn == "v – banehastighed (m/s)":
        c1, c2 = st.columns(2)
        omega = c1.number_input("ω – vinkelhastighed (rad/s)", value=2.0, format="%.6g")
        r     = c2.number_input("r – radius (m)", value=3.0, format="%.6g")
        v = omega * r
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \omega \cdot r = {omega:.6g} \cdot {r:.6g} = {v:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_kin_circ_v"):
            gem_resultat(v, "m/s", "v")

    elif beregn == "ω – vinkelhastighed (rad/s)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        omega = v / r
        T = 2 * np.pi / omega
        st.success(f"**ω = {omega:.6g} rad/s  (T = {T:.6g} s)**")
        st.latex(rf"\omega = \frac{{v}}{{r}} = \frac{{{v:.6g}}}{{{r:.6g}}} = {omega:.6g}\ \text{{rad/s}}")
        if st.button("📋 Gem ω", key="gem_kin_circ_omega"):
            gem_resultat(omega, "rad/s", "ω")

    elif beregn == "r – radius (m)":
        c1, c2 = st.columns(2)
        v     = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        omega = c2.number_input("ω – vinkelhastighed (rad/s)", value=2.0, min_value=1e-12, format="%.6g")
        r = v / omega
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \frac{{v}}{{\omega}} = \frac{{{v:.6g}}}{{{omega:.6g}}} = {r:.6g}\ \text{{m}}")
        if st.button("📋 Gem r", key="gem_kin_circ_r"):
            gem_resultat(r, "m", "r")

    elif beregn == "ac – centripetal­acceleration (m/s²)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        ac = v**2 / r
        st.success(f"**aₐ = {ac:.6g} m/s²**")
        st.latex(rf"a_c = \frac{{v^2}}{{r}} = \frac{{{v:.6g}^2}}{{{r:.6g}}} = {ac:.6g}\ \text{{m/s}}^2")
        if st.button("📋 Gem ac", key="gem_kin_circ_ac"):
            gem_resultat(ac, "m/s²", "ac")

    elif beregn == "T – omløbstid (s)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * r / v
        st.success(f"**T = {T:.6g} s**")
        st.latex(rf"T = \frac{{2\pi r}}{{v}} = \frac{{2\pi \cdot {r:.6g}}}{{{v:.6g}}} = {T:.6g}\ \text{{s}}")
        if st.button("📋 Gem T", key="gem_kin_circ_T"):
            gem_resultat(T, "s", "T")

    else:
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * r / v
        f = 1 / T
        st.success(f"**f = {f:.6g} Hz  (T = {T:.6g} s)**")
        st.latex(rf"f = \frac{{v}}{{2\pi r}} = {f:.6g}\ \text{{Hz}}")
        if st.button("📋 Gem f", key="gem_kin_circ_f"):
            gem_resultat(f, "Hz", "f")

# ── Cirkulær bevægelse – RPM og centripetal ────────────────────────────────────
elif formel == "Cirkulær bevægelse – RPM-omregner og centripetal":
    st.latex(r"\omega = \frac{2\pi \cdot \text{rpm}}{60} \qquad a_c = \omega^2 r \qquad r = \frac{a_c}{\omega^2}")
    st.markdown("Bruges til centrifuge-opgaver: omdan rpm → ω → find radius eller centripetal­acceleration.")
    st.divider()

    beregn = st.radio("Beregn:", [
        "ω – vinkelhastighed fra RPM",
        "r – radius (given ac og RPM)",
        "ac – centripetal­acceleration (given r og RPM)",
        "RPM – given ω",
    ], horizontal=True, key="kin_rpm_mode")
    st.divider()

    if beregn == "ω – vinkelhastighed fra RPM":
        rpm = st.number_input("RPM – omdrejninger pr. minut", value=10000.0, format="%.6g")
        omega = rpm * 2 * np.pi / 60
        f_hz = rpm / 60
        T_s = 60 / rpm
        st.success(f"**ω = {omega:.6g} rad/s**   (f = {f_hz:.6g} Hz, T = {T_s:.6g} s)")
        st.latex(rf"\omega = \frac{{2\pi \cdot {rpm:.6g}}}{{60}} = {omega:.6g}\ \text{{rad/s}}")
        if st.button("📋 Gem ω", key="gem_kin_rpm_omega"):
            gem_resultat(omega, "rad/s", "ω")

    elif beregn == "r – radius (given ac og RPM)":
        st.markdown("**Eksempel: centrifuge med 10000 RPM og ac = 8500g → find r**")
        c1, c2 = st.columns(2)
        rpm = c1.number_input("RPM – omdrejninger pr. minut", value=10000.0, format="%.6g", key="kin_rpm_val")
        ac_g = c2.number_input("ac – centripetal­acceleration (× g)", value=8500.0, format="%.6g", key="kin_ac_g")
        ac = ac_g * G
        omega = rpm * 2 * np.pi / 60
        r = ac / omega**2
        st.success(f"**r = {r:.6g} m  =  {r*100:.4g} cm**")
        st.latex(rf"\omega = \frac{{2\pi \cdot {rpm:.6g}}}{{60}} = {omega:.6g}\ \text{{rad/s}}")
        st.latex(rf"a_c = {ac_g:.6g} \cdot g = {ac:.6g}\ \text{{m/s}}^2")
        st.latex(rf"r = \frac{{a_c}}{{\omega^2}} = \frac{{{ac:.6g}}}{{{omega:.6g}^2}} = {r:.6g}\ \text{{m}}")
        st.info(f"Check: aₐ/g = ω²r/g = {omega**2*r/G:.4g} (skal = {ac_g:.4g})")
        if abs(rpm - 10000.0) < 1 and abs(ac_g - 8500.0) < 1:
            st.success("📋 **2025 Q7** – Centrifuge: 10 000 RPM, 8500g → r ≈ 7.6 cm ✓")
        if st.button("📋 Gem r", key="gem_kin_rpm_r"):
            gem_resultat(r, "m", "r")

    elif beregn == "ac – centripetal­acceleration (given r og RPM)":
        c1, c2 = st.columns(2)
        rpm = c1.number_input("RPM – omdrejninger pr. minut", value=10000.0, format="%.6g")
        r   = c2.number_input("r – radius (m)", value=0.076, min_value=1e-12, format="%.6g")
        omega = rpm * 2 * np.pi / 60
        ac = omega**2 * r
        ac_g = ac / G
        st.success(f"**ac = {ac:.6g} m/s²  =  {ac_g:.4g} × g**")
        st.latex(rf"a_c = \omega^2 r = {omega:.6g}^2 \cdot {r:.6g} = {ac:.6g}\ \text{{m/s}}^2")
        if st.button("📋 Gem ac", key="gem_kin_rpm_ac"):
            gem_resultat(ac, "m/s²", "ac")

    else:
        omega = st.number_input("ω – vinkelhastighed (rad/s)", value=100.0, format="%.6g")
        rpm = omega * 60 / (2 * np.pi)
        st.success(f"**RPM = {rpm:.6g}  (f = {omega/(2*np.pi):.6g} Hz)**")
        st.latex(rf"\text{{RPM}} = \frac{{\omega \cdot 60}}{{2\pi}} = \frac{{{omega:.6g} \cdot 60}}{{2\pi}} = {rpm:.6g}")
        if st.button("📋 Gem RPM", key="gem_kin_rpm_rpm"):
            gem_resultat(rpm, "RPM", "RPM")

elif formel == "To kugler mødes – lodret kast":
    st.latex(r"h_1(t) = v_0 t - \tfrac{1}{2}gt^2 \qquad h_2(t) = H - \tfrac{1}{2}gt^2")
    st.latex(r"h_1 = h_2 \;\Rightarrow\; v_0 t = H \;\Rightarrow\; t_{m\varnothing de} = \frac{H}{v_0}")
    st.info("Nøgleobservation: ½gt²-leddene udligner hinanden — mødetidspunktet er uafhængigt af g!")
    st.markdown("""
**Kugle 1** kastes lodret opad fra h = 0 med starthastighed v₀.
**Kugle 2** slippes fra hvile fra højden H **på samme tidspunkt**.
""")
    st.divider()

    c1, c2, c3 = st.columns(3)
    v0_m = c1.number_input("v₀ – starthastighed opad (m/s)", value=50.0, min_value=1e-6, format="%.6g")
    H_m  = c2.number_input("H – startshøjde for kugle 2 (m)", value=100.0, min_value=0.0, format="%.6g")
    g_m  = c3.number_input("g – tyngdeacceleration (m/s²)", value=G, format="%.6g")

    t_meet = H_m / v0_m
    h_meet = v0_m * t_meet - 0.5 * g_m * t_meet**2

    col1, col2 = st.columns(2)
    col1.metric("Mødetidspunkt t", f"{t_meet:.4g} s")
    col2.metric("Mødehøjde h", f"{h_meet:.4g} m")

    if h_meet < 0:
        st.warning(f"⚠️ h = {h_meet:.4g} m < 0: kugle 1 når ikke op til kugle 2 inden den rammer jorden.")
    elif h_meet > H_m:
        st.warning(f"⚠️ h = {h_meet:.4g} m > H: beregn er ugyldig — kugle 1 er allerede forbi kugle 2s startposition.")
    else:
        st.success(f"Kuglerne mødes ved h = {h_meet:.4g} m efter t = {t_meet:.4g} s")

    with st.expander("Vis udregning"):
        st.latex(rf"t_{{m\varnothing de}} = \frac{{H}}{{v_0}} = \frac{{{H_m:.4g}}}{{{v0_m:.4g}}} = {t_meet:.4g}\ \text{{s}}")
        st.latex(rf"h = v_0 t - \tfrac{{1}}{{2}}g t^2 = {v0_m:.4g}\cdot{t_meet:.4g} - \tfrac{{1}}{{2}}\cdot{g_m:.4g}\cdot{t_meet:.4g}^2 = {h_meet:.4g}\ \text{{m}}")
        st.caption("Samme resultat fra kugle 2: h = H − ½g·t² = " + f"{H_m:.4g} − ½·{g_m:.4g}·{t_meet:.4g}² = {H_m - 0.5*g_m*t_meet**2:.4g} m ✓")

    if abs(v0_m - 50.0) < 0.1 and abs(H_m - 100.0) < 0.1:
        st.success(f"📋 **2025 Q4** – v₀=50 m/s, H=100 m → t=2.0 s, h={v0_m*H_m/v0_m - 0.5*g_m*(H_m/v0_m)**2:.4g} m ✓ (svar I: 80.4 m)")

    if st.button("📋 Gem h_møde", key="gem_kin_meet_h"):
        gem_resultat(h_meet, "m", "h_møde")
