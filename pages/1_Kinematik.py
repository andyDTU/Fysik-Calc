import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar

st.set_page_config(page_title="Kinematik", page_icon="🏃", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
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

formel = st.selectbox("Vælg formel", [
    "Uniform bevægelse:  s = v · t",
    "Jævnt accelereret (1):  v = v₀ + a · t",
    "Jævnt accelereret (2):  s = v₀·t + ½·a·t²",
    "Jævnt accelereret (3):  v² = v₀² + 2·a·s",
    "Kastebevægelse (vandret kast)",
    "Kastebevægelse (skråt kast)",
    "Cirkulær bevægelse",
    "Cirkulær bevægelse – RPM-omregner og centripetal",
], key="kin_formel")

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

    elif beregn == "v – hastighed (m/s)":
        c1, c2 = st.columns(2)
        s = c1.number_input("s – strækning (m)", value=50.0, format="%.6g")
        t = c2.number_input("t – tid (s)", value=5.0, min_value=1e-12, format="%.6g")
        v = s / t
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \frac{{s}}{{t}} = \frac{{{s:.6g}}}{{{t:.6g}}} = {v:.6g}\ \text{{m/s}}")

    else:
        c1, c2 = st.columns(2)
        s = c1.number_input("s – strækning (m)", value=50.0, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        t = s / v
        st.success(f"**t = {t:.6g} s**")
        st.latex(rf"t = \frac{{s}}{{v}} = \frac{{{s:.6g}}}{{{v:.6g}}} = {t:.6g}\ \text{{s}}")

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

    elif beregn == "v₀ (m/s)":
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v – sluthastighed (m/s)", value=10.0, format="%.6g")
        a  = c2.number_input("a – acceleration (m/s²)", value=2.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=5.0, format="%.6g")
        v0 = v - a * t
        st.success(f"**v₀ = {v0:.6g} m/s**")
        st.latex(rf"v_0 = v - a \cdot t = {v:.6g} - {a:.6g} \cdot {t:.6g} = {v0:.6g}\ \text{{m/s}}")

    elif beregn == "a (m/s²)":
        c1, c2, c3 = st.columns(3)
        v  = c1.number_input("v – sluthastig­hed (m/s)", value=10.0, format="%.6g")
        v0 = c2.number_input("v₀ – starthastig­hed (m/s)", value=0.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=5.0, min_value=1e-12, format="%.6g")
        a = (v - v0) / t
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{v - v_0}}{{t}} = \frac{{{v:.6g} - {v0:.6g}}}{{{t:.6g}}} = {a:.6g}\ \text{{m/s}}^2")

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

    elif beregn == "a (m/s²)":
        c1, c2, c3 = st.columns(3)
        s  = c1.number_input("s (m)", value=25.0, format="%.6g")
        v0 = c2.number_input("v₀ (m/s)", value=0.0, format="%.6g")
        t  = c3.number_input("t (s)", value=5.0, min_value=1e-12, format="%.6g")
        a = 2 * (s - v0 * t) / t**2
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{2(s - v_0 t)}}{{t^2}} = {a:.6g}\ \text{{m/s}}^2")

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
                else:
                    st.success(f"**t₁ = {solutions[0]:.6g} s  |  t₂ = {solutions[1]:.6g} s**")
                    st.info("To løsninger – vælg den fysisk meningsfulde.")

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

    # Solve -½g t² + v0y t + h0 = 0 for landing time
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

    elif beregn == "ω – vinkelhastighed (rad/s)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        omega = v / r
        T = 2 * np.pi / omega
        st.success(f"**ω = {omega:.6g} rad/s  (T = {T:.6g} s)**")
        st.latex(rf"\omega = \frac{{v}}{{r}} = \frac{{{v:.6g}}}{{{r:.6g}}} = {omega:.6g}\ \text{{rad/s}}")

    elif beregn == "r – radius (m)":
        c1, c2 = st.columns(2)
        v     = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        omega = c2.number_input("ω – vinkelhastighed (rad/s)", value=2.0, min_value=1e-12, format="%.6g")
        r = v / omega
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \frac{{v}}{{\omega}} = \frac{{{v:.6g}}}{{{omega:.6g}}} = {r:.6g}\ \text{{m}}")

    elif beregn == "ac – centripetal­acceleration (m/s²)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        ac = v**2 / r
        st.success(f"**aₐ = {ac:.6g} m/s²**")
        st.latex(rf"a_c = \frac{{v^2}}{{r}} = \frac{{{v:.6g}^2}}{{{r:.6g}}} = {ac:.6g}\ \text{{m/s}}^2")

    elif beregn == "T – omløbstid (s)":
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * r / v
        st.success(f"**T = {T:.6g} s**")
        st.latex(rf"T = \frac{{2\pi r}}{{v}} = \frac{{2\pi \cdot {r:.6g}}}{{{v:.6g}}} = {T:.6g}\ \text{{s}}")

    else:
        c1, c2 = st.columns(2)
        v = c1.number_input("v – banehastighed (m/s)", value=6.0, format="%.6g")
        r = c2.number_input("r – radius (m)", value=3.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * r / v
        f = 1 / T
        st.success(f"**f = {f:.6g} Hz  (T = {T:.6g} s)**")
        st.latex(rf"f = \frac{{v}}{{2\pi r}} = {f:.6g}\ \text{{Hz}}")

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

    elif beregn == "ac – centripetal­acceleration (given r og RPM)":
        c1, c2 = st.columns(2)
        rpm = c1.number_input("RPM – omdrejninger pr. minut", value=10000.0, format="%.6g")
        r   = c2.number_input("r – radius (m)", value=0.076, min_value=1e-12, format="%.6g")
        omega = rpm * 2 * np.pi / 60
        ac = omega**2 * r
        ac_g = ac / G
        st.success(f"**ac = {ac:.6g} m/s²  =  {ac_g:.4g} × g**")
        st.latex(rf"a_c = \omega^2 r = {omega:.6g}^2 \cdot {r:.6g} = {ac:.6g}\ \text{{m/s}}^2")

    else:
        omega = st.number_input("ω – vinkelhastighed (rad/s)", value=100.0, format="%.6g")
        rpm = omega * 60 / (2 * np.pi)
        st.success(f"**RPM = {rpm:.6g}  (f = {omega/(2*np.pi):.6g} Hz)**")
        st.latex(rf"\text{{RPM}} = \frac{{\omega \cdot 60}}{{2\pi}} = \frac{{{omega:.6g} \cdot 60}}{{2\pi}} = {rpm:.6g}")
