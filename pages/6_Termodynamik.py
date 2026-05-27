import streamlit as st
import numpy as np

st.set_page_config(page_title="Termodynamik", page_icon="🌡️", layout="wide")
st.title("🌡️ Termodynamik")
st.markdown("Ideel gaslov, varme, faseovergange og termodynamikkens love")
st.divider()

R = 8.314    # J/(mol·K)
k_B = 1.381e-23

formel = st.selectbox("Vælg formel", [
    "Ideel gaslov:  p · V = n · R · T",
    "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂",
    "Varmekapacitet:  Q = m · c · ΔT",
    "Faseovergang:  Q = m · L",
    "Arbejde af gas – isobar:  W = p · ΔV",
    "Arbejde af gas – isoterm:  W = nRT·ln(V₂/V₁)",
    "Adiabatisk proces:  pV^γ = konst",
    "1. termodynamikslov:  ΔU = Q − W",
    "Carnot-virkningsgrad:  η = 1 − Tk/Tv",
    "Termisk udvidelse",
])

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
