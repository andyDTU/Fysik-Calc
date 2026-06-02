import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Termodynamik", page_icon="🌡️", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🌡️", "Termodynamik")
st.title("🌡️ Termodynamik")
st.markdown("Ideel gaslov, varme, faseovergange og termodynamikkens love")
st.divider()

R = 8.314    # J/(mol·K)
k_B = 1.381e-23

_TERMO_FORMULAS = [
    ("Ideel gaslov",         "pV = nRT",                      "Ideel gaslov:  p · V = n · R · T"),
    ("Kombineret gaslov",    "p₁V₁/T₁ = p₂V₂/T₂",           "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂"),
    ("Varmekapacitet",       "Q = m·c·ΔT",                   "Varmekapacitet:  Q = m · c · ΔT"),
    ("Faseovergang",         "Q = m · L",                     "Faseovergang:  Q = m · L"),
    ("Isobar arbejde",       "W = p·ΔV",                     "Arbejde af gas – isobar:  W = p · ΔV"),
    ("Isoterm arbejde",      "W = nRT·ln(V₂/V₁)",            "Arbejde af gas – isoterm:  W = nRT·ln(V₂/V₁)"),
    ("Adiabatisk proces",    "pV^γ = konst",                  "Adiabatisk proces:  pV^γ = konst"),
    ("1. termodynamikslov",  "ΔU = Q − W",                   "1. termodynamikslov:  ΔU = Q − W"),
    ("Intern energi (idealgas)", "U = (f/2)nRT",             "Intern energi idealgas:  U = (f/2)·n·R·T"),
    ("Entropi",              "ΔS = Q_rev/T",                  "Entropi:  ΔS = Q_rev / T"),
    ("Carnot-virkningsgrad", "η = 1 − Tk/Tv",                "Carnot-virkningsgrad:  η = 1 − Tk/Tv"),
    ("Termisk udvidelse",    "ΔL = α·L₀·ΔT",                 "Termisk udvidelse"),
    ("Varmledning",          "Q/t = k·A·ΔT/L",               "Varmledning:  Q/t = k·A·ΔT/L"),
]
formel = formula_card_grid(_TERMO_FORMULAS, "termo_formel")

TERMO_TIPS = {
    "Ideel gaslov:  p · V = n · R · T": "T skal være i Kelvin (K = °C + 273.15). p i Pascal, V i m³, n i mol.",
    "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂": "Hold konstante størrelser på begge sider. Isokorm: V₁=V₂. Isobar: p₁=p₂.",
    "Varmekapacitet:  Q = m · c · ΔT": "c for vand = 4186 J/(kg·K). Husk: ΔT i Kelvin = ΔT i Celsius.",
    "Faseovergang:  Q = m · L": "L_v (vand→damp) ≈ 2.26×10⁶ J/kg. L_f (is→vand) ≈ 3.34×10⁵ J/kg. Ingen temp.-ændring!",
    "Adiabatisk proces:  pV^γ = konst": "Q = 0. γ = Cp/Cv ≈ 1.4 for diatomisk gas. Gælder for hurtige processer.",
    "1. termodynamikslov:  ΔU = Q − W": "ΔU = Q − W. Q > 0: varme TIL systemet. W > 0: arbejde AF systemet.",
    "Intern energi idealgas:  U = (f/2)·n·R·T": "Monoatomisk idealgas: f = 3 → U = (3/2)nRT. Diatomisk: f = 5 → U = (5/2)nRT. Cv = (f/2)R.",
    "Entropi:  ΔS = Q_rev / T": "Isoterm: ΔS = Q/T = nR·ln(V₂/V₁). Isobar: ΔS = nCp·ln(T₂/T₁). Adiabatisk: ΔS = 0. Isochor: ΔS = nCv·ln(T₂/T₁).",
    "Carnot-virkningsgrad:  η = 1 − Tk/Tv": "η = 1 − Tk/Tv. Absolut temperatur! Max. virkningsgrad for enhver varmemaskine.",
    "Varmledning:  Q/t = k·A·ΔT/L": "k = varmeledningsevne (W/(m·K)). Fouriers lov. Stationær tilstand: samme Q/t hele vejen igennem.",
}
show_tips(formel, TERMO_TIPS)
st.divider()

if formel == "Ideel gaslov:  p · V = n · R · T":
    st.latex(r"p \cdot V = n \cdot R \cdot T")
    st.info(f"R = {R} J/(mol·K)")
    beregn = st.radio("Beregn:", ["p – tryk (Pa)", "V – volumen (m³)", "n – stofmængde (mol)", "T – temperatur (K)"], horizontal=True)
    st.divider()

    if beregn == "p – tryk (Pa)":
        c1, c2, c3 = st.columns(3)
        n = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        T = c2.number_input("T – temperatur (K)", value=293.15, min_value=0.01, format="%.6g")
        V = c3.number_input("V – volumen (m³)", value=0.0245, min_value=1e-12, format="%.6g")
        p = n * R * T / V
        st.success(f"**p = {p:.6g} Pa  =  {p/1e5:.4g} bar  =  {p/101325:.4g} atm**")
        st.latex(rf"p = \frac{{nRT}}{{V}} = \frac{{{n:.6g} \cdot {R} \cdot {T:.6g}}}{{{V:.6g}}} = {p:.6g}\ \text{{Pa}}")

    elif beregn == "V – volumen (m³)":
        c1, c2, c3 = st.columns(3)
        n = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        R_val = R
        T = c2.number_input("T – temperatur (K)", value=293.15, min_value=0.01, format="%.6g")
        p = c3.number_input("p – tryk (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
        V = n * R_val * T / p
        st.success(f"**V = {V:.6g} m³  =  {V*1000:.4g} L**")
        st.latex(rf"V = \frac{{nRT}}{{p}} = \frac{{{n:.6g} \cdot {R_val} \cdot {T:.6g}}}{{{p:.6g}}} = {V:.6g}\ \text{{m}}^3")

    elif beregn == "n – stofmængde (mol)":
        c1, c2, c3 = st.columns(3)
        p = c1.number_input("p – tryk (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
        V = c2.number_input("V – volumen (m³)", value=0.0245, min_value=1e-12, format="%.6g")
        T = c3.number_input("T – temperatur (K)", value=293.15, min_value=0.01, format="%.6g")
        n = p * V / (R * T)
        st.success(f"**n = {n:.6g} mol**")
        st.latex(rf"n = \frac{{pV}}{{RT}} = \frac{{{p:.6g} \cdot {V:.6g}}}{{{R} \cdot {T:.6g}}} = {n:.6g}\ \text{{mol}}")

    else:
        c1, c2, c3 = st.columns(3)
        p = c1.number_input("p – tryk (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
        V = c2.number_input("V – volumen (m³)", value=0.0245, min_value=1e-12, format="%.6g")
        n = c3.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        T = p * V / (n * R)
        st.success(f"**T = {T:.6g} K  =  {T - 273.15:.4g} °C**")
        st.latex(rf"T = \frac{{pV}}{{nR}} = \frac{{{p:.6g} \cdot {V:.6g}}}{{{n:.6g} \cdot {R}}} = {T:.6g}\ \text{{K}}")

elif formel == "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂":
    st.latex(r"\frac{p_1 V_1}{T_1} = \frac{p_2 V_2}{T_2}")
    st.markdown("Beregn én ukendt ud fra to tilstande. Lad den ukendte stå som 0.")
    beregn = st.radio("Beregn:", ["p₂", "V₂", "T₂", "p₁", "V₁", "T₁"], horizontal=True)
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Tilstand 1**")
        p1 = st.number_input("p₁ (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
        V1 = st.number_input("V₁ (m³)", value=0.001, min_value=1e-12, format="%.6g")
        T1 = st.number_input("T₁ (K)", value=293.15, min_value=0.01, format="%.6g")
    with c2:
        st.markdown("**Tilstand 2**")
        p2 = st.number_input("p₂ (Pa)", value=202650.0, min_value=1e-12 if beregn != "p₂" else 0.0, format="%.6g")
        V2 = st.number_input("V₂ (m³)", value=0.0005, min_value=1e-12 if beregn != "V₂" else 0.0, format="%.6g")
        T2 = st.number_input("T₂ (K)", value=293.15, min_value=0.01 if beregn != "T₂" else 0.0, format="%.6g")

    k = p1 * V1 / T1

    if beregn == "p₂":
        result = k * T2 / V2
        st.success(f"**p₂ = {result:.6g} Pa  =  {result/1e5:.4g} bar**")
        st.latex(rf"p_2 = \frac{{p_1 V_1 T_2}}{{T_1 V_2}} = {result:.6g}\ \text{{Pa}}")
    elif beregn == "V₂":
        result = k * T2 / p2
        st.success(f"**V₂ = {result:.6g} m³  =  {result*1000:.4g} L**")
    elif beregn == "T₂":
        result = p2 * V2 / k
        st.success(f"**T₂ = {result:.6g} K  =  {result-273.15:.4g} °C**")
    elif beregn == "p₁":
        result = p2 * V2 * T1 / (V1 * T2)
        st.success(f"**p₁ = {result:.6g} Pa**")
    elif beregn == "V₁":
        result = p2 * V2 * T1 / (p1 * T2)
        st.success(f"**V₁ = {result:.6g} m³**")
    else:
        result = p1 * V1 * T2 / (p2 * V2)
        st.success(f"**T₁ = {result:.6g} K  =  {result-273.15:.4g} °C**")

elif formel == "Varmekapacitet:  Q = m · c · ΔT":
    st.latex(r"Q = m \cdot c \cdot \Delta T")

    st.markdown("**Almindelige specifikke varmekapaciteter:**")
    st.markdown("""
| Stof | c (J/(kg·K)) |
|------|-------------|
| Vand | 4182 |
| Is | 2090 |
| Aluminium | 900 |
| Jern | 449 |
| Kobber | 385 |
| Luft (konstant tryk) | 1005 |
""")

    beregn = st.radio("Beregn:", ["Q – varme (J)", "m – masse (kg)", "c – spec. varmekapacitet (J/(kg·K))", "ΔT – temperaturændring (K)"], horizontal=True)
    st.divider()

    if beregn == "Q – varme (J)":
        c1, c2, c3 = st.columns(3)
        m   = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        c_v = c2.number_input("c – spec. varmekapacitet (J/(kg·K))", value=4182.0, format="%.6g")
        dT  = c3.number_input("ΔT – temperaturændring (K eller °C)", value=10.0, format="%.6g")
        Q = m * c_v * dT
        st.success(f"**Q = {Q:.6g} J  =  {Q/1000:.4g} kJ**")
        st.latex(rf"Q = m c \Delta T = {m:.6g} \cdot {c_v:.6g} \cdot {dT:.6g} = {Q:.6g}\ \text{{J}}")

    elif beregn == "m – masse (kg)":
        c1, c2, c3 = st.columns(3)
        Q   = c1.number_input("Q – varme (J)", value=41820.0, format="%.6g")
        c_v = c2.number_input("c (J/(kg·K))", value=4182.0, min_value=1e-12, format="%.6g")
        dT  = c3.number_input("ΔT (K)", value=10.0, min_value=1e-12, format="%.6g")
        m = Q / (c_v * dT)
        st.success(f"**m = {m:.6g} kg**")

    elif beregn == "c – spec. varmekapacitet (J/(kg·K))":
        c1, c2, c3 = st.columns(3)
        Q  = c1.number_input("Q – varme (J)", value=41820.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        dT = c3.number_input("ΔT (K)", value=10.0, min_value=1e-12, format="%.6g")
        c_v = Q / (m * dT)
        st.success(f"**c = {c_v:.6g} J/(kg·K)**")

    else:
        c1, c2, c3 = st.columns(3)
        Q   = c1.number_input("Q – varme (J)", value=41820.0, format="%.6g")
        m   = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        c_v = c3.number_input("c (J/(kg·K))", value=4182.0, min_value=1e-12, format="%.6g")
        dT = Q / (m * c_v)
        st.success(f"**ΔT = {dT:.6g} K**")

elif formel == "Faseovergang:  Q = m · L":
    st.latex(r"Q = m \cdot L")
    st.markdown("""
| Stof / Overgang | L (J/kg) |
|----------------|---------|
| Vand → Damp (fordampning, 100°C) | 2 260 000 |
| Is → Vand (smeltning, 0°C) | 334 000 |
| Alkohol (fordampning) | 855 000 |
""")
    beregn = st.radio("Beregn:", ["Q – varme (J)", "m – masse (kg)", "L – latent varme (J/kg)"], horizontal=True)
    st.divider()

    if beregn == "Q – varme (J)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        L = c2.number_input("L – latent varme (J/kg)", value=2260000.0, format="%.6g")
        Q = m * L
        st.success(f"**Q = {Q:.6g} J  =  {Q/1e6:.4g} MJ**")
        st.latex(rf"Q = m \cdot L = {m:.6g} \cdot {L:.6g} = {Q:.6g}\ \text{{J}}")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – varme (J)", value=2260000.0, format="%.6g")
        L = c2.number_input("L (J/kg)", value=2260000.0, min_value=1e-12, format="%.6g")
        m = Q / L
        st.success(f"**m = {m:.6g} kg**")

    else:
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – varme (J)", value=2260000.0, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        L = Q / m
        st.success(f"**L = {L:.6g} J/kg**")

elif formel == "Arbejde af gas – isobar:  W = p · ΔV":
    st.latex(r"W = p \cdot \Delta V \quad \text{(isobar – konstant tryk)}")
    st.info("Gælder for isobar proces (konstant tryk). For isoterm brug: W = nRT·ln(V₂/V₁).")
    beregn = st.radio("Beregn:", ["W – arbejde (J)", "p – tryk (Pa)", "ΔV – volumensændring (m³)"], horizontal=True)
    st.divider()

    if beregn == "W – arbejde (J)":
        c1, c2 = st.columns(2)
        p  = c1.number_input("p – tryk (Pa)", value=101325.0, format="%.6g")
        dV = c2.number_input("ΔV – volumensændring (m³)", value=0.001, format="%.6g")
        W = p * dV
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = p \cdot \Delta V = {p:.6g} \cdot {dV:.6g} = {W:.6g}\ \text{{J}}")

    elif beregn == "p – tryk (Pa)":
        c1, c2 = st.columns(2)
        W  = c1.number_input("W – arbejde (J)", value=101.325, format="%.6g")
        dV = c2.number_input("ΔV (m³)", value=0.001, min_value=1e-12, format="%.6g")
        p = W / dV
        st.success(f"**p = {p:.6g} Pa**")

    else:
        c1, c2 = st.columns(2)
        W = c1.number_input("W – arbejde (J)", value=101.325, format="%.6g")
        p = c2.number_input("p – tryk (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
        dV = W / p
        st.success(f"**ΔV = {dV:.6g} m³**")

elif formel == "Arbejde af gas – isoterm:  W = nRT·ln(V₂/V₁)":
    st.latex(r"W = nRT\ln\!\frac{V_2}{V_1} = p_1 V_1 \ln\!\frac{V_2}{V_1}")
    st.info("Gælder for isoterm proces (konstant temperatur): ΔT = 0, ΔU = 0, Q = W.")
    st.info(f"R = {R} J/(mol·K)")
    beregn = st.radio("Beregn:", ["W – arbejde (J)", "V₂ – slutvolumen (m³)", "T – temperatur (K)"], horizontal=True)
    st.divider()

    if beregn == "W – arbejde (J)":
        c1, c2, c3, c4 = st.columns(4)
        n  = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        T  = c2.number_input("T – temperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        V1 = c3.number_input("V₁ – startvolumen (m³)", value=0.001, min_value=1e-12, format="%.6g")
        V2 = c4.number_input("V₂ – slutvolumen (m³)", value=0.002, min_value=1e-12, format="%.6g")
        if V2 <= 0 or V1 <= 0:
            st.error("Volumen skal være positiv.")
        else:
            W = n * R * T * np.log(V2 / V1)
            st.success(f"**W = {W:.6g} J**")
            st.latex(rf"W = nRT\ln\frac{{V_2}}{{V_1}} = {n:.4g}\cdot{R}\cdot{T:.4g}\cdot\ln\!\left(\frac{{{V2:.4g}}}{{{V1:.4g}}}\right) = {W:.6g}\ \text{{J}}")
            if W > 0:
                st.caption("W > 0: gassen udvider sig og udfører arbejde.")
            else:
                st.caption("W < 0: gassen komprimeres, omgivelserne udfører arbejde.")

    elif beregn == "V₂ – slutvolumen (m³)":
        c1, c2, c3, c4 = st.columns(4)
        n  = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        T  = c2.number_input("T – temperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        V1 = c3.number_input("V₁ – startvolumen (m³)", value=0.001, min_value=1e-12, format="%.6g")
        W  = c4.number_input("W – arbejde (J)", value=1000.0, format="%.6g")
        V2 = V1 * np.exp(W / (n * R * T))
        st.success(f"**V₂ = {V2:.6g} m³**")
        st.latex(rf"V_2 = V_1 \cdot e^{{W/(nRT)}} = {V1:.4g} \cdot e^{{{W:.4g}/({n:.4g}\cdot{R}\cdot{T:.4g})}} = {V2:.6g}\ \text{{m}}^3")

    else:
        c1, c2, c3, c4 = st.columns(4)
        n  = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        W  = c2.number_input("W – arbejde (J)", value=1729.0, format="%.6g")
        V1 = c3.number_input("V₁ (m³)", value=0.001, min_value=1e-12, format="%.6g")
        V2 = c4.number_input("V₂ (m³)", value=0.002, min_value=1e-12, format="%.6g")
        if abs(np.log(V2 / V1)) < 1e-12:
            st.error("V₁ = V₂ – ingen isoterm proces.")
        else:
            T = W / (n * R * np.log(V2 / V1))
            st.success(f"**T = {T:.6g} K  =  {T-273.15:.4g} °C**")

elif formel == "Adiabatisk proces:  pV^γ = konst":
    st.latex(r"p V^\gamma = \text{konst} \qquad T V^{\gamma-1} = \text{konst}")
    st.latex(r"W = \frac{p_1 V_1 - p_2 V_2}{\gamma - 1} = \frac{nR(T_1 - T_2)}{\gamma - 1}")
    st.info("Adiabatisk: ingen varmeudveksling (Q = 0). ΔU = −W.")
    st.divider()

    gamma_map = {
        "Monoatomisk ideal gas (He, Ar) – γ = 5/3 ≈ 1.667": 5/3,
        "Diatomisk ideal gas (N₂, O₂, luft) – γ = 7/5 = 1.4": 7/5,
        "Triatomisk (CO₂) – γ ≈ 1.3": 1.3,
    }
    gamma_choice = st.selectbox("Gastype:", list(gamma_map.keys()))
    gamma = gamma_map[gamma_choice]
    st.caption(f"γ = {gamma:.4g}")

    beregn = st.radio("Beregn:", ["p₂ og T₂ (given V₁, V₂, p₁, T₁)", "W – adiabatisk arbejde (J)"], horizontal=True)
    st.divider()

    if beregn == "p₂ og T₂ (given V₁, V₂, p₁, T₁)":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Tilstand 1**")
            p1 = st.number_input("p₁ (Pa)", value=101325.0, min_value=1e-12, format="%.6g")
            V1 = st.number_input("V₁ (m³)", value=0.001, min_value=1e-12, format="%.6g")
            T1 = st.number_input("T₁ (K)", value=300.0, min_value=0.01, format="%.6g")
        with c2:
            st.markdown("**Tilstand 2**")
            V2 = st.number_input("V₂ (m³)", value=0.0002, min_value=1e-12, format="%.6g")

        p2 = p1 * (V1 / V2)**gamma
        T2 = T1 * (V1 / V2)**(gamma - 1)
        W  = (p1 * V1 - p2 * V2) / (gamma - 1)

        col1, col2, col3 = st.columns(3)
        col1.metric("p₂ (Pa)", f"{p2:.6g}")
        col2.metric("T₂ (K)", f"{T2:.6g}  ({T2-273.15:.4g} °C)")
        col3.metric("W – arbejde (J)", f"{W:.6g}")

        st.latex(rf"p_2 = p_1\!\left(\frac{{V_1}}{{V_2}}\right)^\gamma = {p1:.4g}\cdot\left(\frac{{{V1:.4g}}}{{{V2:.4g}}}\right)^{{{gamma:.4g}}} = {p2:.6g}\ \text{{Pa}}")
        st.latex(rf"T_2 = T_1\!\left(\frac{{V_1}}{{V_2}}\right)^{{\gamma-1}} = {T1:.4g}\cdot\left(\frac{{{V1:.4g}}}{{{V2:.4g}}}\right)^{{{gamma-1:.4g}}} = {T2:.6g}\ \text{{K}}")

    else:
        c1, c2 = st.columns(2)
        n  = c1.number_input("n – stofmængde (mol)", value=1.0, min_value=1e-12, format="%.6g")
        T1 = c1.number_input("T₁ – starttemperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        T2 = c2.number_input("T₂ – sluttemperatur (K)", value=500.0, min_value=0.01, format="%.6g")
        W = n * R * (T1 - T2) / (gamma - 1)
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = \frac{{nR(T_1 - T_2)}}{{\gamma - 1}} = \frac{{{n:.4g}\cdot{R}\cdot({T1:.4g}-{T2:.4g})}}{{{gamma:.4g}-1}} = {W:.6g}\ \text{{J}}")
        st.caption("W > 0: gas udfører arbejde (afkøler). W < 0: gas komprimeres (opvarmes).")

elif formel == "1. termodynamikslov:  ΔU = Q − W":
    st.latex(r"\Delta U = Q - W")
    st.markdown("""
- **Q > 0**: varme tilføres systemet
- **W > 0**: systemet udfører arbejde på omgivelserne
""")
    beregn = st.radio("Beregn:", ["ΔU – intern energiændring (J)", "Q – tilført varme (J)", "W – udført arbejde (J)"], horizontal=True)
    st.divider()

    if beregn == "ΔU – intern energiændring (J)":
        c1, c2 = st.columns(2)
        Q = c1.number_input("Q – tilført varme (J)", value=500.0, format="%.6g")
        W = c2.number_input("W – udført arbejde (J)", value=200.0, format="%.6g")
        dU = Q - W
        st.success(f"**ΔU = {dU:.6g} J**")
        st.latex(rf"\Delta U = Q - W = {Q:.6g} - {W:.6g} = {dU:.6g}\ \text{{J}}")

    elif beregn == "Q – tilført varme (J)":
        c1, c2 = st.columns(2)
        dU = c1.number_input("ΔU – intern energiændring (J)", value=300.0, format="%.6g")
        W  = c2.number_input("W – udført arbejde (J)", value=200.0, format="%.6g")
        Q = dU + W
        st.success(f"**Q = {Q:.6g} J**")
        st.latex(rf"Q = \Delta U + W = {dU:.6g} + {W:.6g} = {Q:.6g}\ \text{{J}}")

    else:
        c1, c2 = st.columns(2)
        Q  = c1.number_input("Q – tilført varme (J)", value=500.0, format="%.6g")
        dU = c2.number_input("ΔU (J)", value=300.0, format="%.6g")
        W = Q - dU
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = Q - \Delta U = {Q:.6g} - {dU:.6g} = {W:.6g}\ \text{{J}}")

elif formel == "Carnot-virkningsgrad:  η = 1 − Tk/Tv":
    st.latex(r"\eta_{Carnot} = 1 - \frac{T_k}{T_v}")
    st.info("Temperaturer skal angives i Kelvin!")
    beregn = st.radio("Beregn:", ["η – Carnot-virkningsgrad", "Tk – kold reservoir (K)", "Tv – varm reservoir (K)"], horizontal=True)
    st.divider()

    if beregn == "η – Carnot-virkningsgrad":
        c1, c2 = st.columns(2)
        Tv = c1.number_input("Tv – varm temperatur (K)", value=500.0, min_value=0.01, format="%.6g")
        Tk = c2.number_input("Tk – kold temperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        if Tk >= Tv:
            st.error("Tk skal være lavere end Tv!")
        else:
            eta = 1 - Tk / Tv
            st.success(f"**η = {eta:.4f}  =  {eta*100:.2f}%**")
            st.latex(rf"\eta = 1 - \frac{{T_k}}{{T_v}} = 1 - \frac{{{Tk:.6g}}}{{{Tv:.6g}}} = {eta:.4f}")

    elif beregn == "Tk – kold reservoir (K)":
        c1, c2 = st.columns(2)
        eta = c1.number_input("η – virkningsgrad (0–1)", value=0.4, min_value=0.0, max_value=0.9999, format="%.6g")
        Tv  = c2.number_input("Tv – varm temperatur (K)", value=500.0, min_value=0.01, format="%.6g")
        Tk = Tv * (1 - eta)
        st.success(f"**Tk = {Tk:.4g} K  =  {Tk-273.15:.4g} °C**")

    else:
        c1, c2 = st.columns(2)
        eta = c1.number_input("η – virkningsgrad (0–1)", value=0.4, min_value=0.0, max_value=0.9999, format="%.6g")
        Tk  = c2.number_input("Tk – kold temperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        Tv = Tk / (1 - eta)
        st.success(f"**Tv = {Tv:.4g} K  =  {Tv-273.15:.4g} °C**")

elif formel == "Varmledning:  Q/t = k·A·ΔT/L":
    st.latex(r"\frac{Q}{t} = \frac{k \cdot A \cdot \Delta T}{L}")
    st.markdown("""
**Fouriers lov** – varmestrøm gennem en stav/plade i stationær tilstand.

- **k** = varmeledningsevne (W/(m·K))
- **A** = tværsnitsareal (m²)
- **ΔT** = temperaturforskel (K)
- **L** = tykkelse/længde af staven (m)
- **Q/t** = varmestrøm (W)
""")
    st.markdown("""
| Materiale | k (W/(m·K)) |
|-----------|------------|
| Kobber | 385 |
| Aluminium | 205 |
| Jern / Stål | 50 |
| Beton | 1.0 |
| Glas | 1.0 |
| Træ | 0.1–0.2 |
| Luft | 0.025 |
""")
    beregn = st.radio("Beregn:", ["Q/t – varmestrøm (W)", "ΔT – temperaturforskel (K)", "L – tykkelse (m)", "A – areal (m²)", "k – varmeledningsevne (W/(m·K))"], horizontal=True)
    st.divider()

    if beregn == "Q/t – varmestrøm (W)":
        c1, c2, c3, c4 = st.columns(4)
        k_vl  = c1.number_input("k (W/(m·K))", value=385.0, min_value=1e-12, format="%.6g")
        A_vl  = c2.number_input("A – areal (m²)", value=1e-4, min_value=1e-12, format="%.6g")
        dT_vl = c3.number_input("ΔT (K)", value=100.0, format="%.6g")
        L_vl  = c4.number_input("L – tykkelse (m)", value=0.01, min_value=1e-12, format="%.6g")
        P_vl = k_vl * A_vl * dT_vl / L_vl
        st.success(f"**Q/t = {P_vl:.4g} W**")
        st.latex(rf"\frac{{Q}}{{t}} = \frac{{k A \Delta T}}{{L}} = \frac{{{k_vl:.4g}\cdot{A_vl:.4g}\cdot{dT_vl:.4g}}}{{{L_vl:.4g}}} = {P_vl:.4g}\ \text{{W}}")

    elif beregn == "ΔT – temperaturforskel (K)":
        c1, c2, c3, c4 = st.columns(4)
        P_vl  = c1.number_input("Q/t – varmestrøm (W)", value=385.0, format="%.6g")
        k_vl  = c2.number_input("k (W/(m·K))", value=385.0, min_value=1e-12, format="%.6g")
        A_vl  = c3.number_input("A – areal (m²)", value=1e-4, min_value=1e-12, format="%.6g")
        L_vl  = c4.number_input("L – tykkelse (m)", value=0.01, min_value=1e-12, format="%.6g")
        dT_vl = P_vl * L_vl / (k_vl * A_vl)
        st.success(f"**ΔT = {dT_vl:.4g} K**")
        st.latex(rf"\Delta T = \frac{{(Q/t)\cdot L}}{{k A}} = {dT_vl:.4g}\ \text{{K}}")

    elif beregn == "L – tykkelse (m)":
        c1, c2, c3, c4 = st.columns(4)
        P_vl  = c1.number_input("Q/t – varmestrøm (W)", value=3.85, format="%.6g")
        k_vl  = c2.number_input("k (W/(m·K))", value=385.0, min_value=1e-12, format="%.6g")
        A_vl  = c3.number_input("A – areal (m²)", value=1e-4, min_value=1e-12, format="%.6g")
        dT_vl = c4.number_input("ΔT (K)", value=100.0, min_value=1e-12, format="%.6g")
        L_vl = k_vl * A_vl * dT_vl / P_vl
        st.success(f"**L = {L_vl:.4g} m  =  {L_vl*100:.4g} cm**")
        st.latex(rf"L = \frac{{k A \Delta T}}{{Q/t}} = {L_vl:.4g}\ \text{{m}}")

    elif beregn == "A – areal (m²)":
        c1, c2, c3, c4 = st.columns(4)
        P_vl  = c1.number_input("Q/t – varmestrøm (W)", value=3.85, format="%.6g")
        k_vl  = c2.number_input("k (W/(m·K))", value=385.0, min_value=1e-12, format="%.6g")
        L_vl  = c3.number_input("L – tykkelse (m)", value=0.01, min_value=1e-12, format="%.6g")
        dT_vl = c4.number_input("ΔT (K)", value=100.0, min_value=1e-12, format="%.6g")
        A_vl = P_vl * L_vl / (k_vl * dT_vl)
        st.success(f"**A = {A_vl:.4g} m²**")
        st.latex(rf"A = \frac{{(Q/t)\cdot L}}{{k\cdot\Delta T}} = {A_vl:.4g}\ \text{{m}}^2")

    else:
        c1, c2, c3, c4 = st.columns(4)
        P_vl  = c1.number_input("Q/t – varmestrøm (W)", value=3.85, format="%.6g")
        A_vl  = c2.number_input("A – areal (m²)", value=1e-4, min_value=1e-12, format="%.6g")
        L_vl  = c3.number_input("L – tykkelse (m)", value=0.01, min_value=1e-12, format="%.6g")
        dT_vl = c4.number_input("ΔT (K)", value=100.0, min_value=1e-12, format="%.6g")
        k_vl = P_vl * L_vl / (A_vl * dT_vl)
        st.success(f"**k = {k_vl:.4g} W/(m·K)**")
        st.latex(rf"k = \frac{{(Q/t)\cdot L}}{{A\cdot\Delta T}} = {k_vl:.4g}\ \text{{W/(m·K)}}")

elif formel == "Termisk udvidelse":
    st.latex(r"\Delta L = \alpha \cdot L_0 \cdot \Delta T \qquad \Delta V = \beta \cdot V_0 \cdot \Delta T")
    type_ = st.radio("Type:", ["Lineær udvidelse (ΔL)", "Volumetrisk udvidelse (ΔV)"], horizontal=True)
    st.divider()

    st.markdown("""
| Materiale | α (10⁻⁶ K⁻¹) |
|-----------|--------------|
| Stål | 12 |
| Aluminium | 23 |
| Kobber | 17 |
| Glas | 9 |
| Beton | 12 |
""")

    if type_ == "Lineær udvidelse (ΔL)":
        c1, c2, c3 = st.columns(3)
        alpha = c1.number_input("α – lineær udvidelseskoeff. (10⁻⁶ K⁻¹)", value=12.0, format="%.6g")
        L0    = c2.number_input("L₀ – originallængde (m)", value=10.0, format="%.6g")
        dT    = c3.number_input("ΔT – temperaturændring (K)", value=100.0, format="%.6g")
        dL = (alpha * 1e-6) * L0 * dT
        L_ny = L0 + dL
        st.success(f"**ΔL = {dL:.6g} m  →  ny længde: {L_ny:.6g} m**")
        st.latex(rf"\Delta L = \alpha L_0 \Delta T = {alpha:.6g} \times 10^{{-6}} \cdot {L0:.6g} \cdot {dT:.6g} = {dL:.6g}\ \text{{m}}")
    else:
        c1, c2, c3 = st.columns(3)
        beta = c1.number_input("β – volumetrisk udvidelseskoeff. (10⁻⁶ K⁻¹)", value=36.0, format="%.6g")
        V0   = c2.number_input("V₀ – originalvolumen (m³)", value=0.001, format="%.6g")
        dT   = c3.number_input("ΔT – temperaturændring (K)", value=100.0, format="%.6g")
        dV = (beta * 1e-6) * V0 * dT
        V_ny = V0 + dV
        st.success(f"**ΔV = {dV:.6g} m³  →  nyt volumen: {V_ny:.6g} m³**")
        st.latex(rf"\Delta V = \beta V_0 \Delta T = {beta:.6g} \times 10^{{-6}} \cdot {V0:.6g} \cdot {dT:.6g} = {dV:.6g}\ \text{{m}}^3")

elif formel == "Intern energi idealgas:  U = (f/2)·n·R·T":
    st.latex(r"U = \frac{f}{2} n R T \qquad \Delta U = n C_v \Delta T \qquad C_v = \frac{f}{2}R")
    st.info("Monoatomisk gas (He, Ar, ...): f = 3 → Cv = (3/2)R ≈ 12.47 J/(mol·K).  "
            "Diatomisk gas (N₂, O₂, luft) ved stuetemperatur: f = 5 → Cv = (5/2)R ≈ 20.79 J/(mol·K).")
    st.divider()

    gastype = st.radio("Gastype:", ["Monoatomisk  (f = 3)", "Diatomisk  (f = 5)", "Brugerdefineret f"], horizontal=True)
    if gastype == "Monoatomisk  (f = 3)":
        f = 3
    elif gastype == "Diatomisk  (f = 5)":
        f = 5
    else:
        f = st.number_input("f – frihedsgrader", value=3, min_value=1, max_value=9, step=1)

    Cv = (f / 2) * R
    Cp = Cv + R
    gamma = Cp / Cv
    st.markdown(f"**Cv = {Cv:.4g} J/(mol·K)  |  Cp = {Cp:.4g} J/(mol·K)  |  γ = Cp/Cv = {gamma:.4g}**")
    st.divider()

    beregn_u = st.radio("Beregn:", ["U – total intern energi (J)", "ΔU – ændring (J)", "T fra U"], horizontal=True)

    if beregn_u == "U – total intern energi (J)":
        c1, c2 = st.columns(2)
        n_u = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g")
        T_u = c2.number_input("T – temperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        U = (f / 2) * n_u * R * T_u
        st.success(f"**U = {U:.6g} J  =  {U/1000:.4g} kJ**")
        st.latex(rf"U = \frac{{{f}}}{{2}} \cdot {n_u:.6g} \cdot {R} \cdot {T_u:.6g} = {U:.6g}\ \text{{J}}")

    elif beregn_u == "ΔU – ændring (J)":
        c1, c2, c3 = st.columns(3)
        n_u  = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g")
        T1_u = c2.number_input("T₁ – starttemperatur (K)", value=300.0, min_value=0.01, format="%.6g")
        T2_u = c3.number_input("T₂ – sluttemperatur (K)", value=400.0, min_value=0.01, format="%.6g")
        dU = n_u * Cv * (T2_u - T1_u)
        st.success(f"**ΔU = {dU:.6g} J  =  {dU/1000:.4g} kJ**")
        st.latex(rf"\Delta U = n C_v \Delta T = {n_u:.6g} \cdot {Cv:.4g} \cdot {T2_u - T1_u:.6g} = {dU:.6g}\ \text{{J}}")

    else:
        c1, c2 = st.columns(2)
        n_u = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g")
        U_u = c2.number_input("U – intern energi (J)", value=7482.0, format="%.6g")
        T_res = U_u / ((f / 2) * n_u * R)
        st.success(f"**T = {T_res:.6g} K  =  {T_res - 273.15:.4g} °C**")
        st.latex(rf"T = \frac{{U}}{{\frac{{f}}{{2}} n R}} = \frac{{{U_u:.6g}}}{{\frac{{{f}}}{{2}} \cdot {n_u:.6g} \cdot {R}}} = {T_res:.6g}\ \text{{K}}")

elif formel == "Entropi:  ΔS = Q_rev / T":
    st.latex(r"\Delta S = \frac{Q_\text{rev}}{T}")
    st.info("Entropi måler uorden. For reversible processer: ΔS = Q_rev/T.  "
            "Adiabatisk reversibel: ΔS = 0 (isentropisk).  "
            "For irreversible processer: ΔS > Q/T.")
    st.divider()

    proces = st.radio(
        "Procestype:",
        ["Isoterm (ΔT = 0)",
         "Isobar (Δp = 0) – idealgas",
         "Isochor (ΔV = 0) – idealgas",
         "Adiabatisk (Q = 0)",
         "Generel idealgas  ΔS = nCv·ln(T₂/T₁) + nR·ln(V₂/V₁)"],
        horizontal=False,
    )
    st.divider()

    gastype_s = st.radio("Gastype:", ["Monoatomisk  (f = 3)", "Diatomisk  (f = 5)", "Brugerdefineret f"], horizontal=True, key="s_gastype")
    if gastype_s == "Monoatomisk  (f = 3)":
        f_s = 3
    elif gastype_s == "Diatomisk  (f = 5)":
        f_s = 5
    else:
        f_s = st.number_input("f – frihedsgrader", value=3, min_value=1, max_value=9, step=1, key="s_f")

    Cv_s = (f_s / 2) * R
    Cp_s = Cv_s + R

    if proces == "Isoterm (ΔT = 0)":
        st.latex(r"\Delta S = \frac{Q}{T} = nR\ln\!\left(\frac{V_2}{V_1}\right)")
        c1, c2, c3 = st.columns(3)
        n_s  = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g", key="si_n")
        T_s  = c2.number_input("T – temperatur (K, konstant)", value=300.0, min_value=0.01, format="%.6g", key="si_T")
        mode_s = c3.radio("Givet:", ["V₂/V₁ (volumenforhold)", "Q – varme (J)"], key="si_mode")
        st.divider()
        if mode_s == "V₂/V₁ (volumenforhold)":
            ratio = st.number_input("V₂/V₁", value=2.0, min_value=1e-9, format="%.6g", key="si_ratio")
            dS = n_s * R * np.log(ratio)
            st.success(f"**ΔS = {dS:.6g} J/K**")
            st.latex(rf"\Delta S = nR\ln(V_2/V_1) = {n_s:.4g} \cdot {R} \cdot \ln({ratio:.4g}) = {dS:.6g}\ \text{{J/K}}")
        else:
            Q_s = st.number_input("Q – tilført varme (J)", value=1000.0, format="%.6g", key="si_Q")
            dS = Q_s / T_s
            st.success(f"**ΔS = {dS:.6g} J/K**")
            st.latex(rf"\Delta S = \frac{{Q}}{{T}} = \frac{{{Q_s:.6g}}}{{{T_s:.6g}}} = {dS:.6g}\ \text{{J/K}}")

    elif proces == "Isobar (Δp = 0) – idealgas":
        st.latex(r"\Delta S = n C_p \ln\!\left(\frac{T_2}{T_1}\right)")
        st.markdown(f"Cp = {Cp_s:.4g} J/(mol·K)")
        c1, c2, c3 = st.columns(3)
        n_s  = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g", key="sp_n")
        T1_s = c2.number_input("T₁ – starttemperatur (K)", value=300.0, min_value=0.01, format="%.6g", key="sp_T1")
        T2_s = c3.number_input("T₂ – sluttemperatur (K)", value=400.0, min_value=0.01, format="%.6g", key="sp_T2")
        dS = n_s * Cp_s * np.log(T2_s / T1_s)
        st.success(f"**ΔS = {dS:.6g} J/K**")
        st.latex(rf"\Delta S = nC_p\ln(T_2/T_1) = {n_s:.4g} \cdot {Cp_s:.4g} \cdot \ln\!\left(\frac{{{T2_s:.4g}}}{{{T1_s:.4g}}}\right) = {dS:.6g}\ \text{{J/K}}")

    elif proces == "Isochor (ΔV = 0) – idealgas":
        st.latex(r"\Delta S = n C_v \ln\!\left(\frac{T_2}{T_1}\right)")
        st.markdown(f"Cv = {Cv_s:.4g} J/(mol·K)")
        c1, c2, c3 = st.columns(3)
        n_s  = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g", key="sv_n")
        T1_s = c2.number_input("T₁ – starttemperatur (K)", value=300.0, min_value=0.01, format="%.6g", key="sv_T1")
        T2_s = c3.number_input("T₂ – sluttemperatur (K)", value=400.0, min_value=0.01, format="%.6g", key="sv_T2")
        dS = n_s * Cv_s * np.log(T2_s / T1_s)
        st.success(f"**ΔS = {dS:.6g} J/K**")
        st.latex(rf"\Delta S = nC_v\ln(T_2/T_1) = {n_s:.4g} \cdot {Cv_s:.4g} \cdot \ln\!\left(\frac{{{T2_s:.4g}}}{{{T1_s:.4g}}}\right) = {dS:.6g}\ \text{{J/K}}")

    elif proces == "Adiabatisk (Q = 0)":
        st.latex(r"\Delta S = 0 \quad (\text{reversibel adiabatisk = isentropisk})")
        st.success("**ΔS = 0 J/K** — ingen entropi­ændring ved reversibel adiabatisk proces.")
        st.markdown("Gælder kun for **reversibel** adiabatisk. Irreversibel adiabatisk: ΔS > 0.")

    else:
        st.latex(r"\Delta S = nC_v\ln\!\left(\frac{T_2}{T_1}\right) + nR\ln\!\left(\frac{V_2}{V_1}\right)")
        c1, c2 = st.columns(2)
        n_s  = c1.number_input("n – stofmængde (mol)", value=2.0, min_value=1e-12, format="%.6g", key="sg_n")
        c2.markdown(f"Cv = {Cv_s:.4g} J/(mol·K)")
        cc1, cc2, cc3, cc4 = st.columns(4)
        T1_s = cc1.number_input("T₁ (K)", value=300.0, min_value=0.01, format="%.6g", key="sg_T1")
        T2_s = cc2.number_input("T₂ (K)", value=400.0, min_value=0.01, format="%.6g", key="sg_T2")
        V1_s = cc3.number_input("V₁ (m³)", value=0.03, min_value=1e-12, format="%.6g", key="sg_V1")
        V2_s = cc4.number_input("V₂ (m³)", value=0.06, min_value=1e-12, format="%.6g", key="sg_V2")
        dS = n_s * Cv_s * np.log(T2_s / T1_s) + n_s * R * np.log(V2_s / V1_s)
        st.success(f"**ΔS = {dS:.6g} J/K**")
        st.latex(
            rf"\Delta S = {n_s:.4g}\cdot{Cv_s:.4g}\cdot\ln\!\left(\frac{{{T2_s:.4g}}}{{{T1_s:.4g}}}\right)"
            rf" + {n_s:.4g}\cdot{R}\cdot\ln\!\left(\frac{{{V2_s:.4g}}}{{{V1_s:.4g}}}\right) = {dS:.6g}\ \text{{J/K}}"
        )
