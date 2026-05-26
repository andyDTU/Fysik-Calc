import streamlit as st
import numpy as np

st.set_page_config(page_title="Kollisioner", page_icon="💥", layout="wide")
st.title("💥 Kollisioner & Impulsbevarelse")
st.markdown("Elastiske, uelastiske kollisioner og bevarelse af impuls — Lecture 10 (10060)")
st.divider()

formel = st.selectbox("Vælg formel / kollisionstype", [
    "Bevarelse af impuls (generelt):  Σp_før = Σp_efter",
    "Fuldstændig uelastisk kollision (objekter hænger sammen)",
    "Elastisk kollision – 1D (KE bevaret)",
    "Koefficient for restitution:  e = Δv_efter / Δv_før",
    "Eksplosion / udskydning",
    "Massemidtpunkt og -hastighed",
])

st.divider()

if formel == "Bevarelse af impuls (generelt):  Σp_før = Σp_efter":
    st.latex(r"m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'")
    st.info("To ukendte kræver en ekstra betingelse (elastisk, uelastisk eller givet e).")
    st.divider()

    st.markdown("**Beregn impuls og bevægelsesmængde:**")
    c1, c2, c3, c4 = st.columns(4)
    m1 = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g")
    v1 = c2.number_input("v₁ – før (m/s)", value=5.0, format="%.6g")
    m2 = c3.number_input("m₂ (kg)", value=3.0, min_value=1e-12, format="%.6g")
    v2 = c4.number_input("v₂ – før (m/s)", value=-2.0, format="%.6g")

    p_total = m1 * v1 + m2 * v2
    v_cm = p_total / (m1 + m2)

    col1, col2, col3 = st.columns(3)
    col1.metric("p₁ = m₁·v₁", f"{m1*v1:.4g} kg·m/s")
    col2.metric("p₂ = m₂·v₂", f"{m2*v2:.4g} kg·m/s")
    col3.metric("Σp = p₁ + p₂", f"{p_total:.4g} kg·m/s")

    st.info(f"Massemidtpunktshastighed v_cm = {v_cm:.4g} m/s — bevares under kollision.")
    st.latex(rf"p_{{total}} = m_1 v_1 + m_2 v_2 = {m1:.6g} \cdot {v1:.6g} + {m2:.6g} \cdot {v2:.6g} = {p_total:.6g}\ \text{{kg·m/s}}")

elif formel == "Fuldstændig uelastisk kollision (objekter hænger sammen)":
    st.latex(r"m_1 v_1 + m_2 v_2 = (m_1 + m_2) v'")
    st.markdown("Objekterne hænger sammen efter kollisionen. Maksimalt KE-tab.")
    st.divider()

    beregn = st.radio("Beregn:", ["v' – fælles hastighed efter", "m₁ – masse 1 (kg)", "v₁ – starthastig­hed 1 (m/s)"], horizontal=True)
    st.divider()

    if beregn == "v' – fælles hastighed efter":
        c1, c2, c3, c4 = st.columns(4)
        m1 = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=6.0, format="%.6g")
        m2 = c3.number_input("m₂ (kg)", value=4.0, min_value=1e-12, format="%.6g")
        v2 = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g")

        v_after = (m1 * v1 + m2 * v2) / (m1 + m2)
        KE_before = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
        KE_after  = 0.5 * (m1 + m2) * v_after**2
        KE_loss   = KE_before - KE_after

        st.success(f"**v' = {v_after:.6g} m/s**")
        col1, col2, col3 = st.columns(3)
        col1.metric("KE før", f"{KE_before:.4g} J")
        col2.metric("KE efter", f"{KE_after:.4g} J")
        col3.metric("ΔKE (tab)", f"{KE_loss:.4g} J  ({KE_loss/KE_before*100:.2f}%)")
        st.latex(rf"v' = \frac{{m_1 v_1 + m_2 v_2}}{{m_1 + m_2}} = \frac{{{m1:.6g} \cdot {v1:.6g} + {m2:.6g} \cdot {v2:.6g}}}{{{m1+m2:.6g}}} = {v_after:.6g}\ \text{{m/s}}")

    elif beregn == "m₁ – masse 1 (kg)":
        c1, c2, c3, c4 = st.columns(4)
        v1      = c1.number_input("v₁ (m/s)", value=6.0, format="%.6g")
        m2      = c2.number_input("m₂ (kg)", value=4.0, min_value=1e-12, format="%.6g")
        v2      = c3.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        v_after = c4.number_input("v' – fælles hastighed (m/s)", value=2.0, format="%.6g")
        denom = v1 - v_after
        if abs(denom) < 1e-12:
            st.error("v₁ = v' – kan ikke beregne m₁")
        else:
            m1 = m2 * (v_after - v2) / denom
            st.success(f"**m₁ = {m1:.6g} kg**")
            st.latex(rf"m_1 = \frac{{m_2(v' - v_2)}}{{v_1 - v'}} = {m1:.6g}\ \text{{kg}}")

    else:
        c1, c2, c3, c4 = st.columns(4)
        m1      = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g")
        m2      = c2.number_input("m₂ (kg)", value=4.0, min_value=1e-12, format="%.6g")
        v2      = c3.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        v_after = c4.number_input("v' – fælles hastighed (m/s)", value=2.0, format="%.6g")
        v1 = ((m1 + m2) * v_after - m2 * v2) / m1
        st.success(f"**v₁ = {v1:.6g} m/s**")

elif formel == "Elastisk kollision – 1D (KE bevaret)":
    st.latex(r"v_1' = \frac{m_1-m_2}{m_1+m_2}v_1 + \frac{2m_2}{m_1+m_2}v_2")
    st.latex(r"v_2' = \frac{2m_1}{m_1+m_2}v_1 + \frac{m_2-m_1}{m_1+m_2}v_2")
    st.info("Både impuls og kinetisk energi bevares. e = 1.")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    m1 = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g")
    v1 = c2.number_input("v₁ – før (m/s)", value=4.0, format="%.6g")
    m2 = c3.number_input("m₂ (kg)", value=6.0, min_value=1e-12, format="%.6g")
    v2 = c4.number_input("v₂ – før (m/s)", value=0.0, format="%.6g")

    M = m1 + m2
    v1_after = ((m1 - m2) * v1 + 2 * m2 * v2) / M
    v2_after = (2 * m1 * v1 + (m2 - m1) * v2) / M

    KE_before = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
    KE_after  = 0.5 * m1 * v1_after**2 + 0.5 * m2 * v2_after**2

    col1, col2 = st.columns(2)
    col1.success(f"**v₁' = {v1_after:.6g} m/s**")
    col2.success(f"**v₂' = {v2_after:.6g} m/s**")

    col3, col4, col5 = st.columns(3)
    col3.metric("KE før", f"{KE_before:.4g} J")
    col4.metric("KE efter", f"{KE_after:.4g} J")
    col5.metric("ΔKE", f"{abs(KE_after - KE_before):.2e} J  (≈0)")

    with st.expander("Vis udregning"):
        st.latex(rf"v_1' = \frac{{{m1:.6g}-{m2:.6g}}}{{{M:.6g}}} \cdot {v1:.6g} + \frac{{2 \cdot {m2:.6g}}}{{{M:.6g}}} \cdot {v2:.6g} = {v1_after:.6g}\ \text{{m/s}}")
        st.latex(rf"v_2' = \frac{{2 \cdot {m1:.6g}}}{{{M:.6g}}} \cdot {v1:.6g} + \frac{{{m2:.6g}-{m1:.6g}}}{{{M:.6g}}} \cdot {v2:.6g} = {v2_after:.6g}\ \text{{m/s}}")

    st.markdown("**Specialtilfælde:**")
    if abs(m1 - m2) < 1e-6 * M:
        st.info("m₁ ≈ m₂: Hastighederne bytter — v₁' ≈ v₂ og v₂' ≈ v₁")
    if abs(v2) < 1e-9:
        st.info(f"m₂ i ro: v₁' = {v1_after:.4g} m/s,  v₂' = {v2_after:.4g} m/s")

elif formel == "Koefficient for restitution:  e = Δv_efter / Δv_før":
    st.latex(r"e = \frac{v_2' - v_1'}{v_1 - v_2} \quad (0 \leq e \leq 1)")
    st.markdown("""
- **e = 1**: Fuldstændig elastisk (ingen KE-tab)
- **e = 0**: Fuldstændig uelastisk (maks. KE-tab, objekter hænger sammen)
- **0 < e < 1**: Delvist elastisk
""")
    st.divider()

    beregn = st.radio("Beregn:", ["e – koefficient", "v₁' og v₂' fra e"], horizontal=True)
    st.divider()

    if beregn == "e – koefficient":
        c1, c2, c3, c4 = st.columns(4)
        v1      = c1.number_input("v₁ – før (m/s)", value=5.0, format="%.6g")
        v2      = c2.number_input("v₂ – før (m/s)", value=0.0, format="%.6g")
        v1_aft  = c3.number_input("v₁' – efter (m/s)", value=1.0, format="%.6g")
        v2_aft  = c4.number_input("v₂' – efter (m/s)", value=4.0, format="%.6g")
        denom = v1 - v2
        if abs(denom) < 1e-12:
            st.error("v₁ = v₂ – ingen kollision")
        else:
            e = (v2_aft - v1_aft) / denom
            st.success(f"**e = {e:.4f}**")
            st.latex(rf"e = \frac{{v_2' - v_1'}}{{v_1 - v_2}} = \frac{{{v2_aft:.6g} - {v1_aft:.6g}}}{{{v1:.6g} - {v2:.6g}}} = {e:.4f}")

    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        m1 = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=5.0, format="%.6g")
        m2 = c3.number_input("m₂ (kg)", value=3.0, min_value=1e-12, format="%.6g")
        v2 = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        e  = c5.number_input("e – restitution (0–1)", value=0.8, min_value=0.0, max_value=1.0, format="%.6g")

        # Solve: p conserved + e definition
        # m1*v1' + m2*v2' = m1*v1 + m2*v2
        # v2' - v1' = e*(v1 - v2)
        p = m1 * v1 + m2 * v2
        dv = e * (v1 - v2)
        # v2' = v1' + dv  →  m1*v1' + m2*(v1' + dv) = p
        v1_aft = (p - m2 * dv) / (m1 + m2)
        v2_aft = v1_aft + dv

        KE_before = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
        KE_after  = 0.5 * m1 * v1_aft**2 + 0.5 * m2 * v2_aft**2

        col1, col2 = st.columns(2)
        col1.success(f"**v₁' = {v1_aft:.6g} m/s**")
        col2.success(f"**v₂' = {v2_aft:.6g} m/s**")
        st.metric("KE-tab", f"{KE_before - KE_after:.4g} J  ({(1 - KE_after/KE_before)*100:.2f}%)")

elif formel == "Eksplosion / udskydning":
    st.latex(r"0 = m_1 v_1' + m_2 v_2' \quad \text{(system i ro før)}")
    st.markdown("Impuls bevares. Starter systemet i ro, er den samlede impuls = 0 efterfølgende.")
    st.divider()

    beregn = st.radio("Beregn:", ["v₂' – hastighed af del 2", "m₁ – masse af del 1"], horizontal=True)
    st.divider()

    if beregn == "v₂' – hastighed af del 2":
        c1, c2, c3 = st.columns(3)
        m1  = c1.number_input("m₁ – masse af del 1 (kg)", value=3.0, min_value=1e-12, format="%.6g")
        v1p = c2.number_input("v₁' – hastighed af del 1 (m/s)", value=-2.0, format="%.6g")
        m2  = c3.number_input("m₂ – masse af del 2 (kg)", value=1.0, min_value=1e-12, format="%.6g")
        v2p = -m1 * v1p / m2
        st.success(f"**v₂' = {v2p:.6g} m/s**")
        KE = 0.5 * m1 * v1p**2 + 0.5 * m2 * v2p**2
        st.info(f"Frigivet kinetisk energi: {KE:.4g} J")
        st.latex(rf"v_2' = -\frac{{m_1 v_1'}}{{m_2}} = -\frac{{{m1:.6g} \cdot {v1p:.6g}}}{{{m2:.6g}}} = {v2p:.6g}\ \text{{m/s}}")
    else:
        c1, c2, c3 = st.columns(3)
        v1p = c1.number_input("v₁' (m/s)", value=-2.0, format="%.6g")
        m2  = c2.number_input("m₂ (kg)", value=1.0, min_value=1e-12, format="%.6g")
        v2p = c3.number_input("v₂' (m/s)", value=6.0, format="%.6g")
        if abs(v1p) < 1e-12:
            st.error("v₁' = 0 – ugyldig")
        else:
            m1 = -m2 * v2p / v1p
            st.success(f"**m₁ = {m1:.6g} kg**")

elif formel == "Massemidtpunkt og -hastighed":
    st.latex(r"x_{cm} = \frac{\sum m_i x_i}{\sum m_i} \qquad v_{cm} = \frac{\sum m_i v_i}{\sum m_i}")
    st.markdown("Beregn massemidtpunktets position og hastighed for et system af partikler.")
    st.divider()

    n = st.number_input("Antal partikler", value=2, min_value=2, max_value=6, step=1)
    masses, positions, velocities = [], [], []

    cols = st.columns(int(n))
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**Partikel {i+1}**")
            m = st.number_input(f"m_{i+1} (kg)", value=float(i+1)*2, min_value=1e-12, key=f"m{i}", format="%.6g")
            x = st.number_input(f"x_{i+1} (m)", value=float(i)*3, key=f"x{i}", format="%.6g")
            v = st.number_input(f"v_{i+1} (m/s)", value=float(i+1)*1.5, key=f"v{i}", format="%.6g")
            masses.append(m); positions.append(x); velocities.append(v)

    M_tot = sum(masses)
    x_cm  = sum(m * x for m, x in zip(masses, positions)) / M_tot
    v_cm  = sum(m * v for m, v in zip(masses, velocities)) / M_tot
    p_tot = sum(m * v for m, v in zip(masses, velocities))

    col1, col2, col3 = st.columns(3)
    col1.metric("x_cm – position", f"{x_cm:.4g} m")
    col2.metric("v_cm – hastighed", f"{v_cm:.4g} m/s")
    col3.metric("Σp – samlet impuls", f"{p_tot:.4g} kg·m/s")

    st.latex(rf"x_{{cm}} = \frac{{\sum m_i x_i}}{{M}} = {x_cm:.4g}\ \text{{m}}")
    st.latex(rf"v_{{cm}} = \frac{{\sum m_i v_i}}{{M}} = {v_cm:.4g}\ \text{{m/s}}")
