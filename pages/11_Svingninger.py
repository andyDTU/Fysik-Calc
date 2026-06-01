import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Svingninger", page_icon="〰️", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("〰️", "Svingninger")
st.title("〰️ Svingninger (SHM)")
st.markdown("Fjedermasse-system, simpelt pendul og energi i harmonisk svingning")
st.divider()

G = 9.82

_SVING_FORMULAS = [
    ("Fjedermasse",          "T = 2π√(m/k)",                  "Fjedermasse:  T = 2π√(m/k)"),
    ("Simpelt pendul",       "T = 2π√(L/g)",                  "Simpelt pendul:  T = 2π√(L/g)"),
    ("Vinkelfrekvens",       "ω = √(k/m)",                    "Vinkelfrekvens:  ω = √(k/m)"),
    ("Bevægelsesligning",    "x(t) = A·cos(ωt+φ)",            "Bevægelsesligning:  x(t) = A·cos(ωt + φ)"),
    ("Energi i svingning",   "E = ½·k·A²",                   "Energi i svingning:  E = ½·k·A²"),
    ("Dæmpet svingning",     "x(t) = A·e^(−γt)·cos(ω't+φ)", "Dæmpet svingning:  x(t) = A·e^(−γt)·cos(ω't + φ)"),
    ("Fysisk pendul",        "T = 2π√(I/(mgd))",             "Fysisk pendul:  T = 2π√(I/(mgd))"),
]
formel = formula_card_grid(_SVING_FORMULAS, "sving_formel")

SVING_TIPS = {
    "Fjedermasse:  T = 2π√(m/k)": "T afhænger ikke af amplitude. Stivere fjeder (stor k) → kortere periode.",
    "Simpelt pendul:  T = 2π√(L/g)": "Gælder kun for små vinkler (< ~15°). T afhænger ikke af masse!",
    "Vinkelfrekvens:  ω = √(k/m)": "ω = 2πf = 2π/T. Enhed: rad/s. ω² = k/m for fjedermasse-system.",
    "Bevægelsesligning:  x(t) = A·cos(ωt + φ)": "v(t) = −Aω·sin(ωt+φ), a(t) = −Aω²·cos(ωt+φ). Max fart ved x=0, max acc. ved x=±A.",
    "Energi i svingning:  E = ½·k·A²": "E = ½kA² = konstant. Ved x=0: alt er kinetisk. Ved x=±A: alt er potentielt.",
    "Dæmpet svingning:  x(t) = A·e^(−γt)·cos(ω't + φ)": "γ = b/(2m). Underdæmpet: γ < ω₀. Kritisk: γ = ω₀. Overdæmpet: γ > ω₀.",
    "Fysisk pendul:  T = 2π√(I/(mgd))": "I = inertimoment om drejningspunktet (Steiner: I = Icm + md²). d = afstand fra drejningspunkt til massemidtpunkt.",
}
show_tips(formel, SVING_TIPS)
st.divider()

if formel == "Fjedermasse:  T = 2π√(m/k)":
    st.latex(r"T = 2\pi\sqrt{\frac{m}{k}}")
    beregn = st.radio("Beregn:", ["T – periode (s)", "m – masse (kg)", "k – fjederkonstant (N/m)"], horizontal=True)
    st.divider()

    if beregn == "T – periode (s)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        k = c2.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * np.sqrt(m / k)
        omega = np.sqrt(k / m)
        f = 1 / T
        st.success(f"**T = {T:.6g} s**   (f = {f:.6g} Hz,  ω = {omega:.6g} rad/s)")
        st.latex(rf"T = 2\pi\sqrt{{\frac{{{m:.6g}}}{{{k:.6g}}}}} = {T:.6g}\ \text{{s}}")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        T = c1.number_input("T – periode (s)", value=0.628, min_value=1e-12, format="%.6g")
        k = c2.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        m = k * (T / (2 * np.pi))**2
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = k \left(\frac{{T}}{{2\pi}}\right)^2 = {k:.6g} \cdot \left(\frac{{{T:.6g}}}{{2\pi}}\right)^2 = {m:.6g}\ \text{{kg}}")

    else:
        c1, c2 = st.columns(2)
        T = c1.number_input("T – periode (s)", value=0.628, min_value=1e-12, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        k = m * (2 * np.pi / T)**2
        st.success(f"**k = {k:.6g} N/m**")
        st.latex(rf"k = m \left(\frac{{2\pi}}{{T}}\right)^2 = {m:.6g} \cdot \left(\frac{{2\pi}}{{{T:.6g}}}\right)^2 = {k:.6g}\ \text{{N/m}}")

elif formel == "Simpelt pendul:  T = 2π√(L/g)":
    st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")
    st.info(f"g = {G} m/s²  (DTU standard)")
    beregn = st.radio("Beregn:", ["T – periode (s)", "L – pendullængde (m)"], horizontal=True)
    st.divider()

    if beregn == "T – periode (s)":
        L = st.number_input("L – pendullængde (m)", value=1.0, min_value=1e-12, format="%.6g")
        T = 2 * np.pi * np.sqrt(L / G)
        f = 1 / T
        st.success(f"**T = {T:.6g} s**   (f = {f:.6g} Hz)")
        st.latex(rf"T = 2\pi\sqrt{{\frac{{{L:.6g}}}{{{G}}}}} = {T:.6g}\ \text{{s}}")
        st.caption("Gælder for små udsving (θ < ~15°). For større vinkler tilføjes korrektionstled.")
    else:
        T = st.number_input("T – periode (s)", value=2.0, min_value=1e-12, format="%.6g")
        L = G * (T / (2 * np.pi))**2
        st.success(f"**L = {L:.6g} m**")
        st.latex(rf"L = g\left(\frac{{T}}{{2\pi}}\right)^2 = {G} \cdot \left(\frac{{{T:.6g}}}{{2\pi}}\right)^2 = {L:.6g}\ \text{{m}}")

elif formel == "Vinkelfrekvens:  ω = √(k/m)":
    st.latex(r"\omega = \sqrt{\frac{k}{m}} = \frac{2\pi}{T} = 2\pi f")
    beregn = st.radio("Givet:", ["k og m", "T – periode", "f – frekvens"], horizontal=True)
    st.divider()

    if beregn == "k og m":
        c1, c2 = st.columns(2)
        k = c1.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        omega = np.sqrt(k / m)
        T = 2 * np.pi / omega
        f = omega / (2 * np.pi)
        st.success(f"**ω = {omega:.6g} rad/s**   (T = {T:.6g} s,  f = {f:.6g} Hz)")
        st.latex(rf"\omega = \sqrt{{\frac{{k}}{{m}}}} = \sqrt{{\frac{{{k:.6g}}}{{{m:.6g}}}}} = {omega:.6g}\ \text{{rad/s}}")

    elif beregn == "T – periode":
        T = st.number_input("T – periode (s)", value=0.628, min_value=1e-12, format="%.6g")
        omega = 2 * np.pi / T
        f = 1 / T
        st.success(f"**ω = {omega:.6g} rad/s**   (f = {f:.6g} Hz)")
        st.latex(rf"\omega = \frac{{2\pi}}{{T}} = \frac{{2\pi}}{{{T:.6g}}} = {omega:.6g}\ \text{{rad/s}}")

    else:
        f = st.number_input("f – frekvens (Hz)", value=1.0, min_value=1e-12, format="%.6g")
        omega = 2 * np.pi * f
        T = 1 / f
        st.success(f"**ω = {omega:.6g} rad/s**   (T = {T:.6g} s)")
        st.latex(rf"\omega = 2\pi f = 2\pi \cdot {f:.6g} = {omega:.6g}\ \text{{rad/s}}")

elif formel == "Bevægelsesligning:  x(t) = A·cos(ωt + φ)":
    st.latex(r"x(t) = A \cos(\omega t + \varphi)")
    st.markdown("Beregn position, hastighed og acceleration til et givet tidspunkt")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    A     = c1.number_input("A – amplitude (m)", value=0.1, format="%.6g")
    omega = c2.number_input("ω – vinkelfrekvens (rad/s)", value=10.0, min_value=1e-12, format="%.6g")
    phi   = c3.number_input("φ – startfase (grader)", value=0.0, format="%.6g")
    t     = c4.number_input("t – tid (s)", value=0.0, min_value=0.0, format="%.6g")

    phi_rad = np.radians(phi)
    x = A * np.cos(omega * t + phi_rad)
    v = -A * omega * np.sin(omega * t + phi_rad)
    a = -A * omega**2 * np.cos(omega * t + phi_rad)
    T = 2 * np.pi / omega

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("x(t) – position (m)", f"{x:.6g}")
    col2.metric("v(t) – hastighed (m/s)", f"{v:.6g}")
    col3.metric("a(t) – acceleration (m/s²)", f"{a:.6g}")

    st.latex(rf"x({t:.4g}) = {A:.4g}\cos({omega:.4g} \cdot {t:.4g} + {phi:.4g}°) = {x:.6g}\ \text{{m}}")
    st.caption(f"T = {T:.6g} s   |   f = {1/T:.6g} Hz   |   a_max = {A*omega**2:.6g} m/s²")

elif formel == "Energi i svingning:  E = ½·k·A²":
    st.latex(r"E = \frac{1}{2}kA^2 = \frac{1}{2}mv^2 + \frac{1}{2}kx^2")
    st.markdown("Totalenergi er konstant og lig med den potentielle energi i amplitude")
    beregn = st.radio("Beregn:", ["E – totalenergi (J)", "A – amplitude (m)", "v – hastighed ved given x (m/s)"], horizontal=True)
    st.divider()

    if beregn == "E – totalenergi (J)":
        c1, c2 = st.columns(2)
        k = c1.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        A = c2.number_input("A – amplitude (m)", value=0.1, format="%.6g")
        E = 0.5 * k * A**2
        st.success(f"**E = {E:.6g} J**")
        st.latex(rf"E = \frac{{1}}{{2}} k A^2 = \frac{{1}}{{2}} \cdot {k:.6g} \cdot {A:.6g}^2 = {E:.6g}\ \text{{J}}")

    elif beregn == "A – amplitude (m)":
        c1, c2 = st.columns(2)
        E = c1.number_input("E – totalenergi (J)", value=0.5, min_value=0.0, format="%.6g")
        k = c2.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        A = np.sqrt(2 * E / k)
        st.success(f"**A = {A:.6g} m**")
        st.latex(rf"A = \sqrt{{\frac{{2E}}{{k}}}} = \sqrt{{\frac{{2 \cdot {E:.6g}}}{{{k:.6g}}}}} = {A:.6g}\ \text{{m}}")

    else:
        c1, c2, c3 = st.columns(3)
        k = c1.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        A = c2.number_input("A – amplitude (m)", value=0.1, format="%.6g")
        x = c3.number_input("x – aktuel position (m)", value=0.05, format="%.6g")
        if abs(x) > abs(A):
            st.error(f"|x| = {abs(x):.4g} > A = {abs(A):.4g}: position kan ikke overstige amplituden.")
        else:
            v = np.sqrt(k / 1.0) * np.sqrt(A**2 - x**2)
            m_note = st.number_input("m – masse (kg, bruges kun til v)", value=1.0, min_value=1e-12, format="%.6g")
            v = np.sqrt(k / m_note) * np.sqrt(A**2 - x**2)
            E = 0.5 * k * A**2
            st.success(f"**v = {v:.6g} m/s**   (E_total = {E:.6g} J)")
            st.latex(rf"v = \omega\sqrt{{A^2 - x^2}} = \sqrt{{\frac{{k}}{{m}}}}\sqrt{{{A:.4g}^2 - {x:.4g}^2}} = {v:.6g}\ \text{{m/s}}")

elif formel == "Dæmpet svingning:  x(t) = A·e^(−γt)·cos(ω't + φ)":
    st.latex(r"x(t) = A e^{-\gamma t} \cos(\omega' t + \varphi)")
    st.latex(r"\omega' = \sqrt{\omega_0^2 - \gamma^2}, \quad \gamma = \frac{b}{2m}")
    st.markdown("**b** = dæmpningskoefficient (N·s/m),  **ω₀** = naturlig frekvens uden dæmpning")
    st.divider()

    c1, c2, c3 = st.columns(3)
    k  = c1.number_input("k – fjederkonstant (N/m)", value=100.0, min_value=1e-12, format="%.6g")
    m  = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
    b  = c3.number_input("b – dæmpningskoef. (N·s/m)", value=1.0, min_value=0.0, format="%.6g")

    omega0 = np.sqrt(k / m)
    gamma  = b / (2 * m)

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("ω₀ (rad/s)", f"{omega0:.6g}")
    col2.metric("γ (1/s)", f"{gamma:.6g}")

    if gamma < omega0:
        omega_prime = np.sqrt(omega0**2 - gamma**2)
        T_d = 2 * np.pi / omega_prime
        col3.metric("ω' – dæmpet (rad/s)", f"{omega_prime:.6g}")
        st.success(f"**Underdæmpet** – svinger med T' = {T_d:.6g} s")
        st.latex(rf"\omega' = \sqrt{{\omega_0^2 - \gamma^2}} = \sqrt{{{omega0:.4g}^2 - {gamma:.4g}^2}} = {omega_prime:.6g}\ \text{{rad/s}}")
        tau_env = 1 / gamma if gamma > 0 else float("inf")
        st.caption(f"Amplitude halveret efter t = {np.log(2)/gamma:.4g} s  (τ_env = {tau_env:.4g} s)")
    elif gamma == omega0:
        col3.metric("ω' – dæmpet (rad/s)", "0")
        st.warning("**Kritisk dæmpet** – systemet vender tilbage uden svingning")
    else:
        col3.metric("ω' – dæmpet (rad/s)", "imaginær")
        st.error("**Overdæmpet** – systemet vender langsomt tilbage, ingen svingning")

elif formel == "Fysisk pendul:  T = 2π√(I/(mgd))":
    st.latex(r"T = 2\pi\sqrt{\frac{I}{mgd}}")
    st.markdown("""
**I** = inertimoment om drejningspunktet (brug Steiners sætning: I = Icm + md²)
**d** = afstand fra drejningspunkt til massemidtpunkt
**Gælder for små udsving (θ < ~15°)**
""")
    st.divider()

    beregn = st.radio("Beregn:", ["T – periode (s)", "I – inertimoment (kg·m²)", "d – afstand cm → pivot (m)"], horizontal=True)
    st.divider()

    if beregn == "T – periode (s)":
        c1, c2, c3 = st.columns(3)
        I_fys = c1.number_input("I – inertimoment om pivot (kg·m²)", value=0.5, min_value=1e-12, format="%.6g")
        m_fys = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        d_fys = c3.number_input("d – afstand cm → pivot (m)", value=0.5, min_value=1e-6, format="%.6g")

        T_fys = 2 * np.pi * np.sqrt(I_fys / (m_fys * G * d_fys))
        omega_fys = np.sqrt(m_fys * G * d_fys / I_fys)
        L_eff = I_fys / (m_fys * d_fys)

        st.success(f"**T = {T_fys:.4g} s**   (f = {1/T_fys:.4g} Hz,  ω = {omega_fys:.4g} rad/s)")
        st.latex(rf"T = 2\pi\sqrt{{\frac{{I}}{{mgd}}}} = 2\pi\sqrt{{\frac{{{I_fys:.4g}}}{{{m_fys:.4g}\cdot{G}\cdot{d_fys:.4g}}}}} = {T_fys:.4g}\ \text{{s}}")
        st.caption(f"Ækvivalent pendul­længde L_eff = I/(md) = {L_eff:.4g} m")
        if st.button("📋 Gem T", key="gem_sving_fys_T"):
            gem_resultat(T_fys, "s", "T_fysisk_pendul")

    elif beregn == "I – inertimoment (kg·m²)":
        c1, c2, c3 = st.columns(3)
        T_fys = c1.number_input("T – periode (s)", value=1.0, min_value=1e-12, format="%.6g")
        m_fys = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        d_fys = c3.number_input("d – afstand cm → pivot (m)", value=0.5, min_value=1e-6, format="%.6g")

        I_fys = m_fys * G * d_fys * (T_fys / (2 * np.pi))**2
        st.success(f"**I = {I_fys:.4g} kg·m²**")
        st.latex(rf"I = m g d \left(\frac{{T}}{{2\pi}}\right)^2 = {m_fys:.4g}\cdot{G}\cdot{d_fys:.4g}\cdot\left(\frac{{{T_fys:.4g}}}{{2\pi}}\right)^2 = {I_fys:.4g}\ \text{{kg·m}}^2")

    else:
        c1, c2, c3 = st.columns(3)
        T_fys = c1.number_input("T – periode (s)", value=1.0, min_value=1e-12, format="%.6g")
        m_fys = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        I_fys = c3.number_input("I – inertimoment om pivot (kg·m²)", value=0.5, min_value=1e-12, format="%.6g")

        d_fys = I_fys / (m_fys * G) * (2 * np.pi / T_fys)**2
        st.success(f"**d = {d_fys:.4g} m**")
        st.latex(rf"d = \frac{{I}}{{{m_fys:.4g}\cdot{G}}} \cdot \left(\frac{{2\pi}}{{{T_fys:.4g}}}\right)^2 = {d_fys:.4g}\ \text{{m}}")
