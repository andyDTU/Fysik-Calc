import streamlit as st
import numpy as np
import pandas as pd
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
    ("Fjedre serie/parallel","k_s = k₁k₂/(k₁+k₂)",          "Fjedre serie/parallel"),
    ("Tvungen svingning",    "A(ω) = F₀/m / √(…)",          "Tvungen svingning og resonans"),
    ("Q-faktor",             "Q = ω₀/(2γ)",                  "Q-faktor og resonansbredde"),
    ("Kombinationsmatrix", "m×k → T  |  L → T", "Kombinationsmatrix – svingninger"),
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
    "Fjedre serie/parallel": "Serie: svagere end svageste fjeder. Parallel: stivere end stiveste. T ændres fordi k_eff ændres.",
    "Tvungen svingning og resonans": "Resonans ved ω_drive ≈ ω₀. Amplitude divergerer hvis b → 0. Q angiver skarphed af resonanstoppen.",
    "Q-faktor og resonansbredde": "Høj Q → smal resonanspik, langsom energitab. Q = ω₀m/b = ω₀/(2γ). Halveffekt-båndbredde Δω = ω₀/Q.",
    "Kombinationsmatrix – svingninger": "Identificér hvilke (m,k)- eller L-kombinationer der giver en given periode. Samme mønster som eksamensopgaver med 'Hvilken kombination passer?'",
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

elif formel == "Fjedre serie/parallel":
    st.latex(r"\text{Serie: } \frac{1}{k_s} = \frac{1}{k_1} + \frac{1}{k_2} \qquad \text{Parallel: } k_p = k_1 + k_2")
    beregn = st.radio("Kobling:", ["Serie", "Parallel"], horizontal=True, key="sving_fjeder_kob")
    st.divider()

    c1, c2, c3 = st.columns(3)
    k1 = c1.number_input("k₁ (N/m)", value=100.0, min_value=1e-12, format="%.6g")
    k2 = c2.number_input("k₂ (N/m)", value=200.0, min_value=1e-12, format="%.6g")
    m  = c3.number_input("m – masse (kg, til T)", value=1.0, min_value=1e-12, format="%.6g")

    use_k3 = st.checkbox("Tilføj tredje fjeder k₃")
    k3 = 0.0
    if use_k3:
        k3 = st.number_input("k₃ (N/m)", value=300.0, min_value=1e-12, format="%.6g")

    if beregn == "Serie":
        if use_k3:
            k_eff = 1 / (1/k1 + 1/k2 + 1/k3)
            st.latex(rf"\frac{{1}}{{k_s}} = \frac{{1}}{{{k1:.4g}}} + \frac{{1}}{{{k2:.4g}}} + \frac{{1}}{{{k3:.4g}}}")
        else:
            k_eff = k1 * k2 / (k1 + k2)
            st.latex(rf"k_s = \frac{{k_1 k_2}}{{k_1+k_2}} = \frac{{{k1:.4g} \cdot {k2:.4g}}}{{{k1:.4g}+{k2:.4g}}}")
    else:
        k_eff = k1 + k2 + (k3 if use_k3 else 0.0)
        if use_k3:
            st.latex(rf"k_p = k_1 + k_2 + k_3 = {k1:.4g} + {k2:.4g} + {k3:.4g}")
        else:
            st.latex(rf"k_p = k_1 + k_2 = {k1:.4g} + {k2:.4g}")

    T_eff = 2 * np.pi * np.sqrt(m / k_eff)
    omega_eff = np.sqrt(k_eff / m)
    st.success(f"**k_eff = {k_eff:.6g} N/m**   →   T = {T_eff:.6g} s,  ω = {omega_eff:.6g} rad/s")
    st.latex(rf"k_{{eff}} = {k_eff:.6g}\ \text{{N/m}} \quad T = 2\pi\sqrt{{\frac{{{m:.4g}}}{{{k_eff:.4g}}}}} = {T_eff:.6g}\ \text{{s}}")
    gem_resultat(k_eff, "N/m", "k_eff")

elif formel == "Tvungen svingning og resonans":
    st.latex(r"A(\omega) = \frac{F_0/m}{\sqrt{(\omega_0^2 - \omega^2)^2 + (2\gamma\omega)^2}}")
    st.markdown("**F₀** = kraftens amplitude (N),  **ω** = drivfrekvens,  **ω₀** = naturlig frekvens,  **γ = b/(2m)**")
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)
    F0    = c1.number_input("F₀ – kraft (N)", value=1.0, min_value=1e-12, format="%.6g")
    m_tv  = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
    k_tv  = c3.number_input("k – fjeder (N/m)", value=100.0, min_value=1e-12, format="%.6g")
    b_tv  = c4.number_input("b – dæmpning (N·s/m)", value=2.0, min_value=0.0, format="%.6g")
    omega_d = c5.number_input("ω_drive (rad/s)", value=10.0, min_value=1e-12, format="%.6g")

    omega0 = np.sqrt(k_tv / m_tv)
    gamma  = b_tv / (2 * m_tv)
    denom  = np.sqrt((omega0**2 - omega_d**2)**2 + (2 * gamma * omega_d)**2)
    A_drive = (F0 / m_tv) / denom

    omega_res = np.sqrt(max(omega0**2 - 2 * gamma**2, 0.0))
    if omega_res > 0:
        denom_res = np.sqrt((omega0**2 - omega_res**2)**2 + (2 * gamma * omega_res)**2)
        A_res = (F0 / m_tv) / denom_res
    else:
        A_res = float("nan")

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("ω₀ (rad/s)", f"{omega0:.4g}")
    col2.metric("A(ω_drive) (m)", f"{A_drive:.4g}")
    col3.metric("A_resonans (m)", f"{A_res:.4g}" if not np.isnan(A_res) else "—")

    st.success(f"**A(ω_drive) = {A_drive:.6g} m**")
    st.latex(rf"A = \frac{{{F0:.4g}/{m_tv:.4g}}}{{\sqrt{{({omega0:.4g}^2-{omega_d:.4g}^2)^2+(2\cdot{gamma:.4g}\cdot{omega_d:.4g})^2}}}} = {A_drive:.6g}\ \text{{m}}")
    if omega_res > 0:
        st.caption(f"Resonans ved ω_res = {omega_res:.4g} rad/s  (A_res = {A_res:.4g} m)")
    else:
        st.caption("Overdæmpet: ingen resonanstop (γ > ω₀/√2)")
    gem_resultat(A_drive, "m", "A_tvungen")

elif formel == "Q-faktor og resonansbredde":
    st.latex(r"Q = \frac{\omega_0}{2\gamma} = \frac{\omega_0 m}{b} \qquad \Delta\omega = \frac{\omega_0}{Q} = 2\gamma")
    st.markdown("Q angiver antallet af svingninger før energien er faldet til 1/e² ≈ 14 % af startværdien.")
    st.divider()

    input_mode = st.radio("Givet:", ["k, m og b", "ω₀ og γ", "ω₀ og Q"], horizontal=True, key="sving_Q_input")
    st.divider()

    if input_mode == "k, m og b":
        c1, c2, c3 = st.columns(3)
        k_q = c1.number_input("k (N/m)", value=100.0, min_value=1e-12, format="%.6g")
        m_q = c2.number_input("m (kg)", value=1.0, min_value=1e-12, format="%.6g")
        b_q = c3.number_input("b (N·s/m)", value=2.0, min_value=1e-12, format="%.6g")
        omega0_q = np.sqrt(k_q / m_q)
        gamma_q  = b_q / (2 * m_q)

    elif input_mode == "ω₀ og γ":
        c1, c2 = st.columns(2)
        omega0_q = c1.number_input("ω₀ (rad/s)", value=10.0, min_value=1e-12, format="%.6g")
        gamma_q  = c2.number_input("γ (1/s)", value=1.0, min_value=1e-12, format="%.6g")

    else:
        c1, c2 = st.columns(2)
        omega0_q = c1.number_input("ω₀ (rad/s)", value=10.0, min_value=1e-12, format="%.6g")
        Q_in     = c2.number_input("Q", value=5.0, min_value=1e-12, format="%.6g")
        gamma_q  = omega0_q / (2 * Q_in)

    Q_q      = omega0_q / (2 * gamma_q)
    delta_omega = omega0_q / Q_q
    omega_lo = omega0_q - delta_omega / 2
    omega_hi = omega0_q + delta_omega / 2
    tau_e    = 1 / gamma_q

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Q", f"{Q_q:.4g}")
    col2.metric("ω₀ (rad/s)", f"{omega0_q:.4g}")
    col3.metric("Δω (rad/s)", f"{delta_omega:.4g}")
    col4.metric("τ_energi (s)", f"{tau_e:.4g}")

    st.success(f"**Q = {Q_q:.6g}**   (Δω = {delta_omega:.4g} rad/s,  halveffekt­frekvenser: {omega_lo:.4g} – {omega_hi:.4g} rad/s)")
    st.latex(rf"Q = \frac{{\omega_0}}{{2\gamma}} = \frac{{{omega0_q:.4g}}}{{2 \cdot {gamma_q:.4g}}} = {Q_q:.4g}")
    st.caption(f"Energien halveret efter {np.log(2)/gamma_q:.4g} s  |  Amplitude halveret efter {np.log(2)/(gamma_q):.4g} s × 2 = {2*np.log(2)/gamma_q:.4g} s")
    gem_resultat(Q_q, "", "Q")

elif formel == "Kombinationsmatrix – svingninger":
    mode = st.radio("Systemtype:", ["Fjedermasse – T = 2π√(m/k)", "Simpelt pendul – T = 2π√(L/g)"], horizontal=True, key="sving_mat_mode")
    st.divider()

    if mode == "Fjedermasse – T = 2π√(m/k)":
        st.latex(r"T = 2\pi\sqrt{\frac{m}{k}}")
        c1, c2 = st.columns(2)
        T_target = c1.number_input("Mål-periode T (s)", value=1.0, min_value=1e-12, format="%.6g", key="sving_mat_T_target")
        tol = c2.number_input("Tolerance ±", value=0.1, min_value=0.0, format="%.6g", key="sving_mat_tol")
        st.divider()
        mc1, mc2, mc3 = st.columns(3)
        m_min  = mc1.number_input("m_min (kg)", value=0.1, min_value=1e-12, format="%.6g", key="sving_mat_m_min")
        m_max  = mc2.number_input("m_max (kg)", value=2.0, min_value=1e-12, format="%.6g", key="sving_mat_m_max")
        m_steps = int(mc3.number_input("m – antal trin", value=6, min_value=2, max_value=50, step=1, key="sving_mat_m_steps"))
        kc1, kc2, kc3 = st.columns(3)
        k_min  = kc1.number_input("k_min (N/m)", value=10.0, min_value=1e-12, format="%.6g", key="sving_mat_k_min")
        k_max  = kc2.number_input("k_max (N/m)", value=500.0, min_value=1e-12, format="%.6g", key="sving_mat_k_max")
        k_steps = int(kc3.number_input("k – antal trin", value=6, min_value=2, max_value=50, step=1, key="sving_mat_k_steps"))

        m_vals = np.linspace(m_min, m_max, m_steps)
        k_vals = np.linspace(k_min, k_max, k_steps)

        row_labels = [f"m={mv:.3g} kg" for mv in m_vals]
        col_labels = [f"k={kv:.3g} N/m" for kv in k_vals]

        data = {}
        for kv, clabel in zip(k_vals, col_labels):
            col_data = []
            for mv in m_vals:
                T_calc = 2 * np.pi * np.sqrt(mv / kv)
                col_data.append(f"{T_calc:.3f}")
            data[clabel] = col_data

        df = pd.DataFrame(data, index=row_labels)

        def _style_fjeder(val):
            try:
                T_calc = float(val)
            except ValueError:
                return "background-color: white"
            if abs(T_calc - T_target) <= tol:
                return "background-color: #d4edda"
            return "background-color: white"

        styled = df.style.applymap(_style_fjeder)
        st.dataframe(styled, use_container_width=True)

        matches = 0
        for kv in k_vals:
            for mv in m_vals:
                T_calc = 2 * np.pi * np.sqrt(mv / kv)
                if abs(T_calc - T_target) <= tol:
                    matches += 1
        st.caption(f"Antal match (grønne celler): **{matches}** ud af {m_steps * k_steps}")

    else:
        st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")
        st.info(f"g = {G} m/s²  (DTU standard)")
        c1, c2 = st.columns(2)
        T_target = c1.number_input("Mål-periode T (s)", value=1.0, min_value=1e-12, format="%.6g", key="sving_mat_pend_T_target")
        tol = c2.number_input("Tolerance ±", value=0.1, min_value=0.0, format="%.6g", key="sving_mat_pend_tol")
        st.divider()
        lc1, lc2, lc3 = st.columns(3)
        L_min   = lc1.number_input("L_min (m)", value=0.1, min_value=1e-12, format="%.6g", key="sving_mat_L_min")
        L_max   = lc2.number_input("L_max (m)", value=3.0, min_value=1e-12, format="%.6g", key="sving_mat_L_max")
        L_steps = int(lc3.number_input("L – antal trin", value=10, min_value=2, max_value=100, step=1, key="sving_mat_L_steps"))

        L_vals = np.linspace(L_min, L_max, L_steps)
        T_vals = [2 * np.pi * np.sqrt(Lv / G) for Lv in L_vals]

        row_labels = [f"L={Lv:.3g} m" for Lv in L_vals]
        df = pd.DataFrame({"T (s)": [f"{Tv:.3f}" for Tv in T_vals]}, index=row_labels)

        def _style_pend(val):
            try:
                T_calc = float(val)
            except ValueError:
                return "background-color: white"
            if abs(T_calc - T_target) <= tol:
                return "background-color: #d4edda"
            return "background-color: white"

        styled = df.style.applymap(_style_pend)
        st.dataframe(styled, use_container_width=True)

        matches = sum(1 for Tv in T_vals if abs(Tv - T_target) <= tol)
        st.caption(f"Antal match (grønne celler): **{matches}** ud af {L_steps}")
