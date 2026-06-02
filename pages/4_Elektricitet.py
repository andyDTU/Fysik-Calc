import streamlit as st
import numpy as np
import pandas as pd
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Elektricitet", page_icon="⚡", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("⚡", "Elektricitet")
st.title("⚡ Elektricitet")
st.markdown("Ohms lov, kredsløb, kondensatorer, Coulombs lov og magnetfelt")
st.divider()

k_e = 8.988e9   # Coulombs konstant
mu0 = 4 * np.pi * 1e-7  # vakuumpermeabilitet

_ELEK_FORMULAS = [
    ("Ohms lov",               "U = R · I",                  "Ohms lov:  U = R · I"),
    ("Elektrisk effekt",       "P = UI = U²/R = I²R",        "Elektrisk effekt"),
    ("Seriekobling",           "R_tot = R₁+R₂+⋯",            "Seriekobling af modstande"),
    ("Parallelkobling",        "1/R_tot = 1/R₁+1/R₂+⋯",      "Parallelkobling af modstande"),
    ("Kondensator",            "Q = C · U",                   "Kondensator:  Q = C · U"),
    ("Energi i kondensator",   "E = ½·C·U²",                 "Energi i kondensator:  E = ½ · C · U²"),
    ("RC-kredsløb",            "τ = R · C",                   "RC-kredsløb:  τ = R · C"),
    ("RC – kombinationsmatrix", "R×C → τ (find tidskonstant)", "RC – kombinationsmatrix"),
    ("RL-kredsløb",            "τ = L / R",                   "RL-kredsløb:  τ = L / R"),
    ("Coulombs lov",           "F = k·q₁q₂/r²",              "Coulombs lov:  F = k · q₁ · q₂ / r²"),
    ("Elektrisk felt",         "E = F/q = k·Q/r²",           "Elektrisk felt:  E = F / q = k · Q / r²"),
    ("Magnetfelt (ledning)",   "B = μ₀I/(2πr)",               "Magnetfelt fra uendelig ledning:  B = μ₀·I / (2π·r)"),
    ("Lorentzkraft (partikel)","F = q·v·B",                   "Lorentzkraft:  F = q · v · B"),
    ("Lorentzkraft (ledning)", "F = B·I·L",                   "Lorentzkraft på ledning:  F = B · I · L"),
    ("Induceret EMF",          "ε = B·L·v",                   "Induceret EMF:  ε = B · L · v"),
    ("Faradays lov",           "ε = −N·ΔΦ/Δt",               "Faradays lov:  ε = -N · ΔΦ / Δt"),
]
formel = formula_card_grid(_ELEK_FORMULAS, "elek_formel")

ELEK_TIPS = {
    "Ohms lov:  U = R · I": "U i Volt, R i Ohm, I i Ampere. Husk: spænding OVER en modstand, strøm IGENNEM.",
    "Elektrisk effekt": "P = U·I = U²/R = I²·R. Vælg den form der passer til de kendte størrelser.",
    "Seriekobling af modstande": "R_total = R₁ + R₂ + ⋯. Samme strøm igennem alle. Spænding fordeles.",
    "Parallelkobling af modstande": "1/R_total = 1/R₁ + 1/R₂ + ⋯. Samme spænding over alle. Strøm fordeles.",
    "Kondensator:  Q = C · U": "Q i Coulomb, C i Farad, U i Volt. Ladning Q er på platerne, ikke i kredsløbet.",
    "RC-kredsløb:  τ = R · C": "τ = R·C = tidskonstant. Efter tid τ er kondensatoren 63% ladet / 37% afladet.",
    "Coulombs lov:  F = k · q₁ · q₂ / r²": "k = 8.988×10⁹ N·m²/C². Positiv F = frastødning, negativ = tiltrækning.",
    "Lorentzkraft:  F = q · v · B": "F = qvB·sin(θ). θ er vinklen mellem v og B. Retning: højrehåndsregel (eller venstrehånd for elektroner).",
    "RC – kombinationsmatrix": "Find hvilke (R, C)-kombinationer giver en bestemt tidskonstant τ = R·C. Identificér kredsløb fra τ-krav.",
}
show_tips(formel, ELEK_TIPS)
st.divider()

if formel == "Ohms lov:  U = R · I":
    st.latex(r"U = R \cdot I")
    beregn = st.radio("Beregn:", ["U – spænding (V)", "R – modstand (Ω)", "I – strøm (A)"], horizontal=True)
    st.divider()

    if beregn == "U – spænding (V)":
        c1, c2 = st.columns(2)
        R = c1.number_input("R – modstand (Ω)", value=10.0, min_value=1e-12, format="%.6g")
        I = c2.number_input("I – strøm (A)", value=2.0, format="%.6g")
        U = R * I
        st.success(f"**U = {U:.6g} V**")
        st.latex(rf"U = R \cdot I = {R:.6g} \cdot {I:.6g} = {U:.6g}\ \text{{V}}")

    elif beregn == "R – modstand (Ω)":
        c1, c2 = st.columns(2)
        U = c1.number_input("U – spænding (V)", value=20.0, format="%.6g")
        I = c2.number_input("I – strøm (A)", value=2.0, min_value=1e-12, format="%.6g")
        R = U / I
        st.success(f"**R = {R:.6g} Ω**")
        st.latex(rf"R = \frac{{U}}{{I}} = \frac{{{U:.6g}}}{{{I:.6g}}} = {R:.6g}\ \Omega")

    else:
        c1, c2 = st.columns(2)
        U = c1.number_input("U – spænding (V)", value=20.0, format="%.6g")
        R = c2.number_input("R – modstand (Ω)", value=10.0, min_value=1e-12, format="%.6g")
        I = U / R
        st.success(f"**I = {I:.6g} A**")
        st.latex(rf"I = \frac{{U}}{{R}} = \frac{{{U:.6g}}}{{{R:.6g}}} = {I:.6g}\ \text{{A}}")

elif formel == "Elektrisk effekt":
    st.latex(r"P = U \cdot I = \frac{U^2}{R} = I^2 \cdot R")
    beregn = st.radio("Beregn P via:", ["U og I", "U og R", "I og R"], horizontal=True)
    st.divider()

    if beregn == "U og I":
        c1, c2 = st.columns(2)
        U = c1.number_input("U – spænding (V)", value=230.0, format="%.6g")
        I = c2.number_input("I – strøm (A)", value=2.0, format="%.6g")
        P = U * I
        st.success(f"**P = {P:.6g} W**")
        st.latex(rf"P = U \cdot I = {U:.6g} \cdot {I:.6g} = {P:.6g}\ \text{{W}}")

    elif beregn == "U og R":
        c1, c2 = st.columns(2)
        U = c1.number_input("U – spænding (V)", value=230.0, format="%.6g")
        R = c2.number_input("R – modstand (Ω)", value=100.0, min_value=1e-12, format="%.6g")
        P = U**2 / R
        I = U / R
        st.success(f"**P = {P:.6g} W**   (I = {I:.6g} A)")
        st.latex(rf"P = \frac{{U^2}}{{R}} = \frac{{{U:.6g}^2}}{{{R:.6g}}} = {P:.6g}\ \text{{W}}")

    else:
        c1, c2 = st.columns(2)
        I = c1.number_input("I – strøm (A)", value=2.0, format="%.6g")
        R = c2.number_input("R – modstand (Ω)", value=100.0, format="%.6g")
        P = I**2 * R
        U = I * R
        st.success(f"**P = {P:.6g} W**   (U = {U:.6g} V)")
        st.latex(rf"P = I^2 \cdot R = {I:.6g}^2 \cdot {R:.6g} = {P:.6g}\ \text{{W}}")

elif formel == "Seriekobling af modstande":
    st.latex(r"R_{total} = R_1 + R_2 + \cdots + R_n")
    st.markdown("Indtast modstande kommasepareret, f.eks. `10, 20, 30`")
    st.divider()

    raw = st.text_input("Modstande (Ω), kommasepareret:", value="10, 20, 30")
    U_tot = st.number_input("Forsyningsspænding U (V) – valgfrit", value=0.0, format="%.6g")

    try:
        Rs = [float(x.strip()) for x in raw.split(",") if x.strip()]
        R_tot = sum(Rs)
        st.success(f"**R_total = {R_tot:.6g} Ω**")
        latex_sum = " + ".join([f"{r:.6g}" for r in Rs])
        st.latex(rf"R_{{total}} = {latex_sum} = {R_tot:.6g}\ \Omega")
        if U_tot > 0:
            I_tot = U_tot / R_tot
            st.markdown("---")
            st.markdown(f"**Strøm:** I = {I_tot:.6g} A  (samme i alle modstande)")
            data = [{"Modstand (Ω)": r, "Spænding (V)": f"{I_tot*r:.6g}", "Strøm (A)": f"{I_tot:.6g}"} for r in Rs]
            st.table(data)
    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")

elif formel == "Parallelkobling af modstande":
    st.latex(r"\frac{1}{R_{total}} = \frac{1}{R_1} + \frac{1}{R_2} + \cdots + \frac{1}{R_n}")
    st.markdown("Indtast modstande kommasepareret, f.eks. `10, 20, 30`")
    st.divider()

    raw = st.text_input("Modstande (Ω), kommasepareret:", value="10, 20, 30")
    U_tot = st.number_input("Forsyningsspænding U (V) – valgfrit", value=0.0, format="%.6g")

    try:
        Rs = [float(x.strip()) for x in raw.split(",") if x.strip()]
        R_tot = 1 / sum(1/r for r in Rs)
        st.success(f"**R_total = {R_tot:.6g} Ω**")
        latex_sum = " + ".join([rf"\frac{{1}}{{{r:.6g}}}" for r in Rs])
        st.latex(rf"\frac{{1}}{{R_{{total}}}} = {latex_sum} \Rightarrow R_{{total}} = {R_tot:.6g}\ \Omega")
        if U_tot > 0:
            I_tot = U_tot / R_tot
            st.markdown("---")
            st.markdown(f"**Samlet strøm:** I_total = {I_tot:.6g} A")
            data = [{"Modstand (Ω)": r, "Spænding (V)": f"{U_tot:.6g}", "Strøm (A)": f"{U_tot/r:.6g}"} for r in Rs]
            st.table(data)
    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")

elif formel == "Kondensator:  Q = C · U":
    st.latex(r"Q = C \cdot U")
    beregn = st.radio("Beregn:", ["Q – ladning (C)", "C – kapacitans (F)", "U – spænding (V)"], horizontal=True)
    st.divider()

    if beregn == "Q – ladning (C)":
        c1, c2 = st.columns(2)
        C = c1.number_input("C – kapacitans (F)", value=100e-6, format="%.6g")
        U = c2.number_input("U – spænding (V)", value=12.0, format="%.6g")
        Q = C * U
        st.success(f"**Q = {Q:.6g} C**")
        st.latex(rf"Q = C \cdot U = {C:.6g} \cdot {U:.6g} = {Q:.6g}\ \text{{C}}")

    elif beregn == "C – kapacitans (F)":
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – ladning (C)", value=1.2e-3, format="%.6g")
        U = c2.number_input("U – spænding (V)", value=12.0, min_value=1e-12, format="%.6g")
        C = Q / U
        st.success(f"**C = {C:.6g} F**")
        st.latex(rf"C = \frac{{Q}}{{U}} = \frac{{{Q:.6g}}}{{{U:.6g}}} = {C:.6g}\ \text{{F}}")

    else:
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – ladning (C)", value=1.2e-3, format="%.6g")
        C = c2.number_input("C – kapacitans (F)", value=100e-6, min_value=1e-12, format="%.6g")
        U = Q / C
        st.success(f"**U = {U:.6g} V**")
        st.latex(rf"U = \frac{{Q}}{{C}} = \frac{{{Q:.6g}}}{{{C:.6g}}} = {U:.6g}\ \text{{V}}")

elif formel == "Energi i kondensator:  E = ½ · C · U²":
    st.latex(r"E = \frac{1}{2} C U^2 = \frac{Q^2}{2C} = \frac{QU}{2}")
    beregn = st.radio("Beregn via:", ["C og U", "Q og C"], horizontal=True)
    st.divider()

    if beregn == "C og U":
        c1, c2 = st.columns(2)
        C = c1.number_input("C – kapacitans (F)", value=100e-6, format="%.6g")
        U = c2.number_input("U – spænding (V)", value=12.0, format="%.6g")
        E = 0.5 * C * U**2
        Q = C * U
        st.success(f"**E = {E:.6g} J**   (Q = {Q:.6g} C)")
        st.latex(rf"E = \frac{{1}}{{2}} \cdot {C:.6g} \cdot {U:.6g}^2 = {E:.6g}\ \text{{J}}")
    else:
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – ladning (C)", value=1.2e-3, format="%.6g")
        C = c2.number_input("C – kapacitans (F)", value=100e-6, min_value=1e-12, format="%.6g")
        E = Q**2 / (2 * C)
        st.success(f"**E = {E:.6g} J**")
        st.latex(rf"E = \frac{{Q^2}}{{2C}} = \frac{{{Q:.6g}^2}}{{2 \cdot {C:.6g}}} = {E:.6g}\ \text{{J}}")

elif formel == "RC-kredsløb:  τ = R · C":
    st.latex(r"\tau = R \cdot C")
    st.markdown("**Opladning:** $V_C(t) = V_0(1 - e^{-t/\\tau})$   |   **Afladning:** $V_C(t) = V_0 \\cdot e^{-t/\\tau}$")
    st.divider()

    mode = st.radio("Proces:", ["Opladning – kondensator lades op", "Afladning – kondensator aflades"], horizontal=True)
    st.divider()

    c1, c2, c3 = st.columns(3)
    R   = c1.number_input("R – modstand (Ω)", value=1000.0, min_value=1e-12, format="%.6g")
    C   = c2.number_input("C – kapacitans (F)", value=100e-6, min_value=1e-12, format="%.6g")
    V0  = c3.number_input("V₀ – kildespænding (V)", value=9.0, format="%.6g")
    tau = R * C

    st.success(f"**τ = {tau:.6g} s**   (63% nået efter {tau:.6g} s, 99% efter {5*tau:.6g} s)")
    st.latex(rf"\tau = R \cdot C = {R:.6g} \cdot {C:.6g} = {tau:.6g}\ \text{{s}}")

    t_val = st.number_input("t – beregn ved tid (s)", value=tau, min_value=0.0, format="%.6g")

    if mode == "Opladning – kondensator lades op":
        Vc = V0 * (1 - np.exp(-t_val / tau))
        Ic = (V0 / R) * np.exp(-t_val / tau)
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric(f"V_C({t_val:.4g} s)", f"{Vc:.6g} V")
        col2.metric(f"I({t_val:.4g} s)", f"{Ic:.6g} A")
        st.latex(rf"V_C(t) = V_0\left(1 - e^{{-t/\tau}}\right) = {V0:.4g}\left(1 - e^{{-{t_val:.4g}/{tau:.4g}}}\right) = {Vc:.6g}\ \text{{V}}")
    else:
        Vc = V0 * np.exp(-t_val / tau)
        Ic = (V0 / R) * np.exp(-t_val / tau)
        st.divider()
        col1, col2 = st.columns(2)
        col1.metric(f"V_C({t_val:.4g} s)", f"{Vc:.6g} V")
        col2.metric(f"I({t_val:.4g} s)", f"{Ic:.6g} A")
        st.latex(rf"V_C(t) = V_0 \cdot e^{{-t/\tau}} = {V0:.4g} \cdot e^{{-{t_val:.4g}/{tau:.4g}}} = {Vc:.6g}\ \text{{V}}")

    E_c = 0.5 * C * V0**2
    st.caption(f"Energi lagret ved fuld opladning: E = ½CV₀² = {E_c:.6g} J")

elif formel == "RC – kombinationsmatrix":
    st.latex(r"\tau = R \cdot C")
    st.divider()
    tau_target = st.number_input("Mål-τ (s)", value=0.01, format="%.6g", key="rc_mat_tau")
    tol = st.number_input("Tolerance ± (s)", value=0.001, format="%.6g", key="rc_mat_tol")
    R_scale_lbl = st.radio("R-enhed:", ["Ω", "kΩ", "MΩ"], horizontal=True, key="rc_mat_ru")
    scale_R = {"Ω": 1, "kΩ": 1e3, "MΩ": 1e6}[R_scale_lbl]
    C_scale_lbl = st.radio("C-enhed:", ["F", "mF", "μF", "nF"], horizontal=True, key="rc_mat_cu")
    scale_C = {"F": 1, "mF": 1e-3, "μF": 1e-6, "nF": 1e-9}[C_scale_lbl]
    c1, c2, c3 = st.columns(3)
    R_min = c1.number_input(f"R min ({R_scale_lbl})", value=1.0, format="%.6g", key="rc_mat_rmin")
    R_max = c2.number_input(f"R max ({R_scale_lbl})", value=100.0, format="%.6g", key="rc_mat_rmax")
    R_steps = c3.number_input("R antal trin", value=8, min_value=2, step=1, key="rc_mat_rsteps")
    c1, c2, c3 = st.columns(3)
    C_min = c1.number_input(f"C min ({C_scale_lbl})", value=1.0, format="%.6g", key="rc_mat_cmin")
    C_max = c2.number_input(f"C max ({C_scale_lbl})", value=1000.0, format="%.6g", key="rc_mat_cmax")
    C_steps = c3.number_input("C antal trin", value=8, min_value=2, step=1, key="rc_mat_csteps")
    R_vals = np.linspace(R_min, R_max, int(R_steps)) * scale_R
    C_vals = np.linspace(C_min, C_max, int(C_steps)) * scale_C
    rows = [f"R={R/scale_R:.1f} {R_scale_lbl}" for R in R_vals]
    cols = [f"C={C/scale_C:.1f} {C_scale_lbl}" for C in C_vals]
    data = {}
    for C, col in zip(C_vals, cols):
        col_data = []
        for R in R_vals:
            tau = R * C
            col_data.append(f"{tau:.4g} s")
        data[col] = col_data
    df = pd.DataFrame(data, index=rows)

    def style_rc(val):
        try:
            tau_val = float(val.replace(" s", ""))
            if abs(tau_val - tau_target) <= tol:
                return "background-color: #d4edda"
        except Exception:
            pass
        return ""

    styled = df.style.applymap(style_rc)
    st.dataframe(styled, use_container_width=True)
    matches = []
    for R, row in zip(R_vals, rows):
        for C, col in zip(C_vals, cols):
            tau = R * C
            if abs(tau - tau_target) <= tol:
                matches.append(f"{row}, {col} → τ={tau:.4g} s")
    if matches:
        st.success("Matches fundet:")
        for m in matches:
            st.write(f"- {m}")
    else:
        st.info("Ingen matches inden for tolerancen.")

elif formel == "RL-kredsløb:  τ = L / R":
    st.latex(r"\tau = \frac{L}{R}")
    st.markdown("**Strøm til/frakobling:** $I(t) = \\frac{V}{R}(1 - e^{-t/\\tau})$   |   **Afladning:** $I(t) = I_0 \\cdot e^{-t/\\tau}$")
    st.divider()

    mode = st.radio("Proces:", ["Tilkobling – strøm opbygges", "Frakobling – strøm aftager"], horizontal=True)
    st.divider()

    c1, c2, c3 = st.columns(3)
    R   = c1.number_input("R – modstand (Ω)", value=10.0, min_value=1e-12, format="%.6g")
    L   = c2.number_input("L – induktans (H)", value=0.1, min_value=1e-12, format="%.6g")
    V   = c3.number_input("V – forsyningsspænding (V)", value=12.0, format="%.6g")
    tau = L / R
    I_max = V / R

    st.success(f"**τ = {tau:.6g} s**   (I_max = V/R = {I_max:.6g} A)")
    st.latex(rf"\tau = \frac{{L}}{{R}} = \frac{{{L:.6g}}}{{{R:.6g}}} = {tau:.6g}\ \text{{s}}")

    t_val = st.number_input("t – beregn ved tid (s)", value=tau, min_value=0.0, format="%.6g")

    if mode == "Tilkobling – strøm opbygges":
        I_t = I_max * (1 - np.exp(-t_val / tau))
        st.divider()
        st.metric(f"I({t_val:.4g} s)", f"{I_t:.6g} A")
        st.latex(rf"I(t) = \frac{{V}}{{R}}\left(1 - e^{{-t/\tau}}\right) = {I_max:.4g}\left(1 - e^{{-{t_val:.4g}/{tau:.4g}}}\right) = {I_t:.6g}\ \text{{A}}")
    else:
        I0 = st.number_input("I₀ – startstrøm (A)", value=I_max, min_value=0.0, format="%.6g")
        I_t = I0 * np.exp(-t_val / tau)
        st.divider()
        st.metric(f"I({t_val:.4g} s)", f"{I_t:.6g} A")
        st.latex(rf"I(t) = I_0 \cdot e^{{-t/\tau}} = {I0:.4g} \cdot e^{{-{t_val:.4g}/{tau:.4g}}} = {I_t:.6g}\ \text{{A}}")

    E_L = 0.5 * L * I_max**2
    st.caption(f"Energi lagret ved fuld strøm: E = ½LI_max² = {E_L:.6g} J")

elif formel == "Coulombs lov:  F = k · q₁ · q₂ / r²":
    st.latex(r"F = k \cdot \frac{q_1 \cdot q_2}{r^2}")
    st.info(f"k = {k_e:.4g} N·m²/C²")
    beregn = st.radio("Beregn:", ["F – kraft (N)", "r – afstand (m)"], horizontal=True)
    st.divider()

    if beregn == "F – kraft (N)":
        c1, c2, c3 = st.columns(3)
        q1 = c1.number_input("q₁ – ladning (C)", value=1e-6, format="%.6g")
        q2 = c2.number_input("q₂ – ladning (C)", value=2e-6, format="%.6g")
        r  = c3.number_input("r – afstand (m)", value=0.1, min_value=1e-12, format="%.6g")
        F = k_e * abs(q1 * q2) / r**2
        retning = "tiltrækkende" if q1 * q2 < 0 else "frastødende"
        st.success(f"**F = {F:.6g} N  ({retning})**")
        st.latex(rf"F = k \frac{{q_1 q_2}}{{r^2}} = {k_e:.4g} \cdot \frac{{{q1:.6g} \cdot {q2:.6g}}}{{{r:.6g}^2}} = {F:.6g}\ \text{{N}}")
    else:
        c1, c2, c3 = st.columns(3)
        F  = c1.number_input("F – kraft (N)", value=1.8, format="%.6g")
        q1 = c2.number_input("q₁ (C)", value=1e-6, format="%.6g")
        q2 = c3.number_input("q₂ (C)", value=2e-6, format="%.6g")
        r = np.sqrt(k_e * abs(q1 * q2) / F)
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \sqrt{{k \frac{{|q_1 q_2|}}{{F}}}} = {r:.6g}\ \text{{m}}")

elif formel == "Elektrisk felt:  E = F / q = k · Q / r²":
    st.latex(r"E = \frac{F}{q} = k \cdot \frac{Q}{r^2}")
    beregn = st.radio("Beregn:", ["E – feltstyrke (N/C)", "F – kraft på ladning (N)", "r – afstand (m)"], horizontal=True)
    st.divider()

    if beregn == "E – feltstyrke (N/C)":
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – kildeladning (C)", value=1e-6, format="%.6g")
        r = c2.number_input("r – afstand (m)", value=0.1, min_value=1e-12, format="%.6g")
        E_field = k_e * abs(Q) / r**2
        st.success(f"**E = {E_field:.6g} N/C**")
        st.latex(rf"E = k \frac{{Q}}{{r^2}} = {k_e:.4g} \cdot \frac{{{Q:.6g}}}{{{r:.6g}^2}} = {E_field:.6g}\ \text{{N/C}}")

    elif beregn == "F – kraft på ladning (N)":
        c1, c2 = st.columns(2)
        E_field = c1.number_input("E – feltstyrke (N/C)", value=90000.0, format="%.6g")
        q       = c2.number_input("q – prøveladning (C)", value=1e-6, format="%.6g")
        F = E_field * q
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = E \cdot q = {E_field:.6g} \cdot {q:.6g} = {F:.6g}\ \text{{N}}")

    else:
        c1, c2 = st.columns(2)
        E_field = c1.number_input("E – feltstyrke (N/C)", value=90000.0, format="%.6g")
        Q       = c2.number_input("Q – kildeladning (C)", value=1e-6, format="%.6g")
        r = np.sqrt(k_e * abs(Q) / E_field)
        st.success(f"**r = {r:.6g} m**")

elif formel == "Magnetfelt fra uendelig ledning:  B = μ₀·I / (2π·r)":
    st.latex(r"B = \frac{\mu_0 \cdot I}{2\pi \cdot r}")
    st.info(f"μ₀ = 4π × 10⁻⁷ T·m/A")
    beregn = st.radio("Beregn:", ["B – magnetfelt (T)", "I – strøm (A)", "r – afstand (m)"], horizontal=True)
    st.divider()

    if beregn == "B – magnetfelt (T)":
        c1, c2 = st.columns(2)
        I = c1.number_input("I – strøm (A)", value=10.0, format="%.6g")
        r = c2.number_input("r – afstand fra ledning (m)", value=0.05, min_value=1e-12, format="%.6g")
        B = mu0 * I / (2 * np.pi * r)
        st.success(f"**B = {B:.6g} T**")
        st.latex(rf"B = \frac{{\mu_0 I}}{{2\pi r}} = \frac{{4\pi \times 10^{{-7}} \cdot {I:.6g}}}{{2\pi \cdot {r:.6g}}} = {B:.6g}\ \text{{T}}")

    elif beregn == "I – strøm (A)":
        c1, c2 = st.columns(2)
        B = c1.number_input("B – magnetfelt (T)", value=4e-5, format="%.6g")
        r = c2.number_input("r – afstand (m)", value=0.05, min_value=1e-12, format="%.6g")
        I = B * 2 * np.pi * r / mu0
        st.success(f"**I = {I:.6g} A**")

    else:
        c1, c2 = st.columns(2)
        B = c1.number_input("B – magnetfelt (T)", value=4e-5, format="%.6g")
        I = c2.number_input("I – strøm (A)", value=10.0, format="%.6g")
        r = mu0 * I / (2 * np.pi * B)
        st.success(f"**r = {r:.6g} m**")

elif formel == "Lorentzkraft:  F = q · v · B":
    st.latex(r"F = q \cdot v \cdot B \cdot \sin\theta")
    beregn = st.radio("Beregn:", ["F – Lorentzkraft (N)", "q – ladning (C)", "v – hastighed (m/s)", "B – magnetfelt (T)"], horizontal=True)
    st.divider()

    theta = st.number_input("θ – vinkel mellem v og B (grader)", value=90.0, min_value=0.0, max_value=180.0, format="%.6g")
    st.divider()

    if beregn == "F – Lorentzkraft (N)":
        c1, c2, c3 = st.columns(3)
        q = c1.number_input("q – ladning (C)", value=1.6e-19, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=1e6, format="%.6g")
        B = c3.number_input("B – magnetfelt (T)", value=0.1, format="%.6g")
        F = abs(q) * v * B * np.sin(np.radians(theta))
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = qvB\sin\theta = {abs(q):.6g} \cdot {v:.6g} \cdot {B:.6g} \cdot \sin({theta:.4g}°) = {F:.6g}\ \text{{N}}")

    elif beregn == "q – ladning (C)":
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.6e-14, format="%.6g")
        v = c2.number_input("v (m/s)", value=1e6, format="%.6g")
        B = c3.number_input("B (T)", value=0.1, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0° eller 180°: sin(θ) = 0 → ingen Lorentzkraft, kan ikke beregne q.")
        else:
            q = F / (v * B * sin_t)
            st.success(f"**q = {q:.6g} C**")

    elif beregn == "v – hastighed (m/s)":
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.6e-14, format="%.6g")
        q = c2.number_input("q (C)", value=1.6e-19, min_value=1e-12, format="%.6g")
        B = c3.number_input("B (T)", value=0.1, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0° eller 180°: sin(θ) = 0 → ingen Lorentzkraft, kan ikke beregne v.")
        else:
            v = F / (abs(q) * B * sin_t)
            st.success(f"**v = {v:.6g} m/s**")

    else:
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.6e-14, format="%.6g")
        q = c2.number_input("q (C)", value=1.6e-19, min_value=1e-12, format="%.6g")
        v = c3.number_input("v (m/s)", value=1e6, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0° eller 180°: sin(θ) = 0 → ingen Lorentzkraft, kan ikke beregne B.")
        else:
            B = F / (abs(q) * v * sin_t)
            st.success(f"**B = {B:.6g} T**")

elif formel == "Lorentzkraft på ledning:  F = B · I · L":
    st.latex(r"F = B \cdot I \cdot L \cdot \sin\theta")
    beregn = st.radio("Beregn:", ["F (N)", "B (T)", "I (A)", "L (m)"], horizontal=True)
    st.divider()
    theta = st.number_input("θ – vinkel (grader)", value=90.0, min_value=0.0, max_value=180.0, format="%.6g")
    st.divider()

    if beregn == "F (N)":
        c1, c2, c3 = st.columns(3)
        B = c1.number_input("B (T)", value=0.5, format="%.6g")
        I = c2.number_input("I (A)", value=10.0, format="%.6g")
        L = c3.number_input("L (m)", value=0.2, format="%.6g")
        F = B * I * L * np.sin(np.radians(theta))
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = BIL\sin\theta = {B:.6g} \cdot {I:.6g} \cdot {L:.6g} \cdot \sin({theta:.4g}°) = {F:.6g}\ \text{{N}}")
    elif beregn == "B (T)":
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.0, format="%.6g")
        I = c2.number_input("I (A)", value=10.0, min_value=1e-12, format="%.6g")
        L = c3.number_input("L (m)", value=0.2, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0°/180°: ingen kraft på ledningen, kan ikke beregne B.")
        else:
            B = F / (I * L * sin_t)
            st.success(f"**B = {B:.6g} T**")
    elif beregn == "I (A)":
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.0, format="%.6g")
        B = c2.number_input("B (T)", value=0.5, min_value=1e-12, format="%.6g")
        L = c3.number_input("L (m)", value=0.2, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0°/180°: ingen kraft på ledningen, kan ikke beregne I.")
        else:
            I = F / (B * L * sin_t)
            st.success(f"**I = {I:.6g} A**")
    else:
        c1, c2, c3 = st.columns(3)
        F = c1.number_input("F (N)", value=1.0, format="%.6g")
        B = c2.number_input("B (T)", value=0.5, min_value=1e-12, format="%.6g")
        I = c3.number_input("I (A)", value=10.0, min_value=1e-12, format="%.6g")
        sin_t = np.sin(np.radians(theta))
        if abs(sin_t) < 1e-12:
            st.error("θ = 0°/180°: ingen kraft på ledningen, kan ikke beregne L.")
        else:
            L = F / (B * I * sin_t)
            st.success(f"**L = {L:.6g} m**")

elif formel == "Induceret EMF:  ε = B · L · v":
    st.latex(r"\varepsilon = B \cdot L \cdot v")
    beregn = st.radio("Beregn:", ["ε – EMF (V)", "B (T)", "L (m)", "v (m/s)"], horizontal=True)
    st.divider()

    if beregn == "ε – EMF (V)":
        c1, c2, c3 = st.columns(3)
        B = c1.number_input("B (T)", value=0.5, format="%.6g")
        L = c2.number_input("L – lederlængde (m)", value=0.3, format="%.6g")
        v = c3.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        emf = B * L * v
        st.success(f"**ε = {emf:.6g} V**")
        st.latex(rf"\varepsilon = B L v = {B:.6g} \cdot {L:.6g} \cdot {v:.6g} = {emf:.6g}\ \text{{V}}")
    elif beregn == "B (T)":
        c1, c2, c3 = st.columns(3)
        emf = c1.number_input("ε (V)", value=1.5, format="%.6g")
        L   = c2.number_input("L (m)", value=0.3, min_value=1e-12, format="%.6g")
        v   = c3.number_input("v (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        B = emf / (L * v)
        st.success(f"**B = {B:.6g} T**")
    elif beregn == "L (m)":
        c1, c2, c3 = st.columns(3)
        emf = c1.number_input("ε (V)", value=1.5, format="%.6g")
        B   = c2.number_input("B (T)", value=0.5, min_value=1e-12, format="%.6g")
        v   = c3.number_input("v (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        L = emf / (B * v)
        st.success(f"**L = {L:.6g} m**")
    else:
        c1, c2, c3 = st.columns(3)
        emf = c1.number_input("ε (V)", value=1.5, format="%.6g")
        B   = c2.number_input("B (T)", value=0.5, min_value=1e-12, format="%.6g")
        L   = c3.number_input("L (m)", value=0.3, min_value=1e-12, format="%.6g")
        v = emf / (B * L)
        st.success(f"**v = {v:.6g} m/s**")

elif formel == "Faradays lov:  ε = -N · ΔΦ / Δt":
    st.latex(r"\varepsilon = -N \cdot \frac{\Delta\Phi}{\Delta t}")
    st.markdown("Φ = magnetisk flux = B · A · cos(θ)")
    beregn = st.radio("Beregn:", ["ε – induceret EMF (V)", "N – antal vindinger", "ΔΦ – fluxændring (Wb)", "Δt – tid (s)"], horizontal=True)
    st.divider()

    if beregn == "ε – induceret EMF (V)":
        c1, c2, c3 = st.columns(3)
        N   = c1.number_input("N – antal vindinger", value=100, min_value=1, step=1)
        dPhi = c2.number_input("ΔΦ – fluxændring (Wb)", value=0.05, format="%.6g")
        dt  = c3.number_input("Δt – tid (s)", value=0.1, min_value=1e-12, format="%.6g")
        emf = -N * dPhi / dt
        st.success(f"**|ε| = {abs(emf):.6g} V**")
        st.latex(rf"\varepsilon = -N \frac{{\Delta\Phi}}{{\Delta t}} = -{N} \cdot \frac{{{dPhi:.6g}}}{{{dt:.6g}}} = {emf:.6g}\ \text{{V}}")

    elif beregn == "N – antal vindinger":
        c1, c2, c3 = st.columns(3)
        emf  = c1.number_input("|ε| – EMF (V)", value=50.0, format="%.6g")
        dPhi = c2.number_input("ΔΦ (Wb)", value=0.05, min_value=1e-12, format="%.6g")
        dt   = c3.number_input("Δt (s)", value=0.1, min_value=1e-12, format="%.6g")
        N = emf * dt / dPhi
        st.success(f"**N = {N:.4g} vindinger**")

    elif beregn == "ΔΦ – fluxændring (Wb)":
        c1, c2, c3 = st.columns(3)
        emf = c1.number_input("|ε| – EMF (V)", value=50.0, format="%.6g")
        N   = c2.number_input("N – vindinger", value=100, min_value=1, step=1)
        dt  = c3.number_input("Δt (s)", value=0.1, min_value=1e-12, format="%.6g")
        dPhi = emf * dt / N
        st.success(f"**ΔΦ = {dPhi:.6g} Wb**")

    else:
        c1, c2, c3 = st.columns(3)
        emf  = c1.number_input("|ε| – EMF (V)", value=50.0, format="%.6g")
        N    = c2.number_input("N – vindinger", value=100, min_value=1, step=1)
        dPhi = c3.number_input("ΔΦ (Wb)", value=0.05, min_value=1e-12, format="%.6g")
        dt = N * dPhi / emf
        st.success(f"**Δt = {dt:.6g} s**")
