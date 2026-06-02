import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Kollisioner", page_icon="💥", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("💥", "Kollisioner")
st.title("💥 Kollisioner & Impulsbevarelse")
st.markdown("Elastiske, uelastiske kollisioner og bevarelse af impuls — Lecture 10 (10060)")
st.divider()

_KOL_FORMULAS = [
    ("Impulsbevarelse",      "Σp_før = Σp_efter",             "Bevarelse af impuls (generelt):  Σp_før = Σp_efter"),
    ("Uelastisk kollision",  "v'=(m₁v₁+m₂v₂)/(m₁+m₂)",      "Fuldstændig uelastisk kollision (objekter hænger sammen)"),
    ("Elastisk kollision",   "v₁'=(m₁−m₂)v₁/(m₁+m₂)",       "Elastisk kollision – 1D (KE bevaret)"),
    ("Kollision 2D",         "vektorkomponenter x og y",       "Kollision i 2D – vektorkomponenter"),
    ("Restitutionskoeff.",   "e = Δv_efter/Δv_før",           "Koefficient for restitution:  e = Δv_efter / Δv_før"),
    ("Eksplosion",           "0 = m₁v₁' + m₂v₂'",            "Eksplosion / udskydning"),
    ("Massemidtpunkt",       "x_cm = Σ(mᵢxᵢ)/M",             "Massemidtpunkt og -hastighed"),
    ("Impuls & gennemsnitskraft", "J = F·Δt = m·Δv",         "Impuls og gennemsnitskraft:  J = F·Δt = m·Δv"),
    ("Kuglestød lodret",     "v'=mv/(M+m), h=v'²/2g",        "Kuglestød – bullet i klods (lodret):  v' = mv/(M+m)"),
]
formel = formula_card_grid(_KOL_FORMULAS, "kol_formel")

KOL_TIPS = {
    "Bevarelse af impuls (generelt):  Σp_før = Σp_efter": "Impuls bevares altid (ingen ydre kræfter). To ukendte → behov for ekstra ligning (elastisk: KE bevares).",
    "Fuldstændig uelastisk kollision (objekter hænger sammen)": "v_fælles = (m₁v₁ + m₂v₂)/(m₁+m₂). Størst energitab muligt. Objekter bevæger sig sammen.",
    "Elastisk kollision – 1D (KE bevaret)": "Både impuls og kinetisk energi bevares. Formler: v₁' = (m₁−m₂)v₁/(m₁+m₂), v₂' = 2m₁v₁/(m₁+m₂).",
    "Koefficient for restitution:  e = Δv_efter / Δv_før": "e = (v₂'−v₁')/(v₁−v₂). e=1: elastisk. e=0: fuldstændig uelastisk. 0 < e < 1: delvist uelastisk.",
    "Eksplosion / udskydning": "Impuls bevares: 0 = m₁v₁' + m₂v₂'. Total impuls før = 0 (hvile).",
    "Impuls og gennemsnitskraft:  J = F·Δt = m·Δv": "Impuls J = Δp = m·Δv. Gennemsnitskraft: F_avg = J/Δt. Bruges ved slag/stød mod væg og kraftpulser.",
    "Kuglestød – bullet i klods (lodret):  v' = mv/(M+m)": "Kugle (m, v) skydes lodret op i klods (M, hvile). Fuldstændig uelastisk: v' = mv/(M+m). Klodsen stiger h = v'²/(2g).",
}
show_tips(formel, KOL_TIPS)
st.divider()

if formel == "Bevarelse af impuls (generelt):  Σp_før = Σp_efter":
    st.latex(r"m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'")
    st.divider()

    beregn_imp = st.radio("Beregn:", [
        "Σp – vis total impuls",
        "v₁' – hastighed af m₁ efter",
        "v₂' – hastighed af m₂ efter",
        "v₁ – hastighed af m₁ før",
        "m₁ – masse af objekt 1",
    ], horizontal=True)
    st.divider()

    if beregn_imp == "Σp – vis total impuls":
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
        st.latex(rf"p_{{total}} = {m1:.4g} \cdot {v1:.4g} + {m2:.4g} \cdot {v2:.4g} = {p_total:.6g}\ \text{{kg·m/s}}")

    elif beregn_imp == "v₁' – hastighed af m₁ efter":
        st.markdown("Kendte: m₁, v₁, m₂, v₂ og **v₂'** → find v₁'")
        c1, c2, c3, c4, c5 = st.columns(5)
        m1  = c1.number_input("m₁ (kg)",  value=2.0, min_value=1e-12, format="%.6g", key="ip_m1a")
        v1  = c2.number_input("v₁ (m/s)", value=5.0, format="%.6g", key="ip_v1a")
        m2  = c3.number_input("m₂ (kg)",  value=3.0, min_value=1e-12, format="%.6g", key="ip_m2a")
        v2  = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g", key="ip_v2a")
        v2p = c5.number_input("v₂' (m/s)", value=4.0, format="%.6g", key="ip_v2pa")
        v1p = (m1*v1 + m2*v2 - m2*v2p) / m1
        st.success(f"**v₁' = {v1p:.6g} m/s**")
        st.latex(rf"v_1' = \frac{{m_1 v_1 + m_2 v_2 - m_2 v_2'}}{{m_1}} = {v1p:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₁'", key="gem_imp_v1p"):
            from utils import gem_resultat as _gem; _gem(v1p, "m/s", "v₁'")

    elif beregn_imp == "v₂' – hastighed af m₂ efter":
        st.markdown("Kendte: m₁, v₁, m₂, v₂ og **v₁'** → find v₂'")
        c1, c2, c3, c4, c5 = st.columns(5)
        m1  = c1.number_input("m₁ (kg)",  value=2.0, min_value=1e-12, format="%.6g", key="ip_m1b")
        v1  = c2.number_input("v₁ (m/s)", value=5.0, format="%.6g", key="ip_v1b")
        m2  = c3.number_input("m₂ (kg)",  value=3.0, min_value=1e-12, format="%.6g", key="ip_m2b")
        v2  = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g", key="ip_v2b")
        v1p = c5.number_input("v₁' (m/s)", value=1.0, format="%.6g", key="ip_v1pb")
        v2p = (m1*v1 + m2*v2 - m1*v1p) / m2
        st.success(f"**v₂' = {v2p:.6g} m/s**")
        st.latex(rf"v_2' = \frac{{m_1 v_1 + m_2 v_2 - m_1 v_1'}}{{m_2}} = {v2p:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₂'", key="gem_imp_v2p"):
            from utils import gem_resultat as _gem; _gem(v2p, "m/s", "v₂'")

    elif beregn_imp == "v₁ – hastighed af m₁ før":
        st.markdown("Kendte: m₁, m₂, v₂, v₁', v₂' → find **v₁**")
        c1, c2, c3, c4, c5 = st.columns(5)
        m1  = c1.number_input("m₁ (kg)",  value=2.0, min_value=1e-12, format="%.6g", key="ip_m1c")
        m2  = c2.number_input("m₂ (kg)",  value=3.0, min_value=1e-12, format="%.6g", key="ip_m2c")
        v2  = c3.number_input("v₂ (m/s)", value=0.0, format="%.6g", key="ip_v2c")
        v1p = c4.number_input("v₁' (m/s)", value=1.0, format="%.6g", key="ip_v1pc")
        v2p = c5.number_input("v₂' (m/s)", value=4.0, format="%.6g", key="ip_v2pc")
        v1 = (m1*v1p + m2*v2p - m2*v2) / m1
        st.success(f"**v₁ = {v1:.6g} m/s**")
        st.latex(rf"v_1 = \frac{{m_1 v_1' + m_2 v_2' - m_2 v_2}}{{m_1}} = {v1:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₁", key="gem_imp_v1"):
            from utils import gem_resultat as _gem; _gem(v1, "m/s", "v₁")

    else:
        st.markdown("Kendte: v₁, v₂, v₁', v₂', m₂ → find **m₁**")
        c1, c2, c3, c4, c5 = st.columns(5)
        v1  = c1.number_input("v₁ (m/s)", value=5.0, format="%.6g", key="ip_v1d")
        v2  = c2.number_input("v₂ (m/s)", value=0.0, format="%.6g", key="ip_v2d")
        v1p = c3.number_input("v₁' (m/s)", value=1.0, format="%.6g", key="ip_v1pd")
        v2p = c4.number_input("v₂' (m/s)", value=4.0, format="%.6g", key="ip_v2pd")
        m2  = c5.number_input("m₂ (kg)",  value=3.0, min_value=1e-12, format="%.6g", key="ip_m2d")
        denom = v1 - v1p
        if abs(denom) < 1e-12:
            st.error("v₁ = v₁' — kan ikke beregne m₁")
        else:
            m1 = m2 * (v2p - v2) / denom
            st.success(f"**m₁ = {m1:.6g} kg**")
            st.latex(rf"m_1 = \frac{{m_2(v_2' - v_2)}}{{v_1 - v_1'}} = {m1:.6g}\ \text{{kg}}")
            if st.button("📋 Gem m₁", key="gem_imp_m1"):
                from utils import gem_resultat as _gem; _gem(m1, "kg", "m₁")

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
        pct = f"  ({KE_loss/KE_before*100:.2f}%)" if KE_before > 1e-12 else ""
        col3.metric("ΔKE (tab)", f"{KE_loss:.4g} J{pct}")
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

    beregn_el = st.radio("Beregn:", [
        "v₁' og v₂' – standardberegning",
        "m₁ – givet m₂, v₁, v₂ og v₁'",
        "v₁ – givet masser og efterhastigheder",
    ], horizontal=True)
    st.divider()

    if beregn_el == "v₁' og v₂' – standardberegning":
        c1, c2, c3, c4 = st.columns(4)
        m1 = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g", key="el_m1a")
        v1 = c2.number_input("v₁ – før (m/s)", value=4.0, format="%.6g", key="el_v1a")
        m2 = c3.number_input("m₂ (kg)", value=6.0, min_value=1e-12, format="%.6g", key="el_m2a")
        v2 = c4.number_input("v₂ – før (m/s)", value=0.0, format="%.6g", key="el_v2a")

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

    elif beregn_el == "m₁ – givet m₂, v₁, v₂ og v₁'":
        st.markdown("Kendte: m₂, v₁, v₂, v₁' → find **m₁** (og v₂' fra elasticitets­betingelse)")
        c1, c2, c3, c4 = st.columns(4)
        m2  = c1.number_input("m₂ (kg)", value=6.0, min_value=1e-12, format="%.6g", key="el_m2b")
        v1  = c2.number_input("v₁ – før (m/s)", value=4.0, format="%.6g", key="el_v1b")
        v2  = c3.number_input("v₂ – før (m/s)", value=0.0, format="%.6g", key="el_v2b")
        v1p = c4.number_input("v₁' – efter (m/s)", value=-2.0, format="%.6g", key="el_v1pb")
        denom = v1 - v1p
        if abs(denom) < 1e-12:
            st.error("v₁ = v₁' — ingen løsning")
        else:
            m1 = m2 * (v1 + v1p - 2 * v2) / denom
            v2p = v1 - v2 + v1p
            st.success(f"**m₁ = {m1:.6g} kg**")
            st.success(f"**v₂' = {v2p:.6g} m/s** (fra elasticitets­betingelse: v₂'−v₁'=v₁−v₂)")
            st.latex(rf"m_1 = m_2 \cdot \frac{{v_1 + v_1' - 2v_2}}{{v_1 - v_1'}} = {m2:.6g} \cdot \frac{{{v1:.6g}+{v1p:.6g}-2\cdot{v2:.6g}}}{{{v1:.6g}-{v1p:.6g}}} = {m1:.6g}\ \text{{kg}}")
            st.latex(rf"v_2' = v_1 - v_2 + v_1' = {v1:.6g} - {v2:.6g} + {v1p:.6g} = {v2p:.6g}\ \text{{m/s}}")
            if st.button("📋 Gem m₁", key="gem_el_m1"):
                from utils import gem_resultat as _gem; _gem(m1, "kg", "m₁")

    else:
        st.markdown("Kendte: m₁, m₂, v₂, v₁', v₂' → find **v₁**")
        c1, c2, c3, c4, c5 = st.columns(5)
        m1  = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g", key="el_m1c")
        m2  = c2.number_input("m₂ (kg)", value=6.0, min_value=1e-12, format="%.6g", key="el_m2c")
        v2  = c3.number_input("v₂ – før (m/s)", value=0.0, format="%.6g", key="el_v2c")
        v1p = c4.number_input("v₁' – efter (m/s)", value=-2.0, format="%.6g", key="el_v1pc")
        v2p = c5.number_input("v₂' – efter (m/s)", value=2.0, format="%.6g", key="el_v2pc")
        v1 = v1p + m2 * (v2p - v2) / m1
        st.success(f"**v₁ = {v1:.6g} m/s**")
        st.latex(rf"v_1 = v_1' + \frac{{m_2(v_2' - v_2)}}{{m_1}} = {v1p:.6g} + \frac{{{m2:.6g} \cdot ({v2p:.6g} - {v2:.6g})}}{{{m1:.6g}}} = {v1:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v₁", key="gem_el_v1"):
            from utils import gem_resultat as _gem; _gem(v1, "m/s", "v₁")

elif formel == "Kollision i 2D – vektorkomponenter":
    st.latex(r"\sum p_x: \quad m_1 v_{1x} + m_2 v_{2x} = m_1 v_{1x}' + m_2 v_{2x}'")
    st.latex(r"\sum p_y: \quad m_1 v_{1y} + m_2 v_{2y} = m_1 v_{1y}' + m_2 v_{2y}'")
    st.info("Impuls bevares uafhængigt i x- og y-retning. Vælg kollisionstype for at finde ubekendte.")
    st.divider()

    mode = st.radio("Kollisionstype:", [
        "Fuldstændig uelastisk (klæber sammen)",
        "Givet v₁' – find v₂' (impulsbevarelse alene)",
        "Vis samlet impuls og KE",
    ], horizontal=True)
    st.divider()

    st.markdown("**Objekt 1 – før kollision:**")
    c1, c2, c3 = st.columns(3)
    m1  = c1.number_input("m₁ (kg)", value=2.0, min_value=1e-12, format="%.6g", key="2d_m1")
    v1x = c2.number_input("v₁ₓ (m/s)", value=3.0, format="%.6g", key="2d_v1x")
    v1y = c3.number_input("v₁ᵧ (m/s)", value=0.0, format="%.6g", key="2d_v1y")

    st.markdown("**Objekt 2 – før kollision:**")
    c4, c5, c6 = st.columns(3)
    m2  = c4.number_input("m₂ (kg)", value=3.0, min_value=1e-12, format="%.6g", key="2d_m2")
    v2x = c5.number_input("v₂ₓ (m/s)", value=-1.0, format="%.6g", key="2d_v2x")
    v2y = c6.number_input("v₂ᵧ (m/s)", value=2.0, format="%.6g", key="2d_v2y")

    px_tot = m1 * v1x + m2 * v2x
    py_tot = m1 * v1y + m2 * v2y
    KE_before = 0.5 * m1 * (v1x**2 + v1y**2) + 0.5 * m2 * (v2x**2 + v2y**2)

    st.divider()

    if mode == "Fuldstændig uelastisk (klæber sammen)":
        M = m1 + m2
        vx_f = px_tot / M
        vy_f = py_tot / M
        v_f  = np.sqrt(vx_f**2 + vy_f**2)
        KE_after = 0.5 * M * v_f**2
        angle = np.degrees(np.arctan2(vy_f, vx_f))

        col1, col2, col3 = st.columns(3)
        col1.success(f"**vₓ' = {vx_f:.6g} m/s**")
        col2.success(f"**vᵧ' = {vy_f:.6g} m/s**")
        col3.success(f"**|v'| = {v_f:.6g} m/s,  θ = {angle:.4g}°**")

        col4, col5, col6 = st.columns(3)
        col4.metric("KE før", f"{KE_before:.4g} J")
        col5.metric("KE efter", f"{KE_after:.4g} J")
        col6.metric("KE-tab", f"{KE_before - KE_after:.4g} J")

        with st.expander("Vis udregning"):
            st.latex(rf"v_x' = \frac{{p_x}}{{M}} = \frac{{{px_tot:.6g}}}{{{M:.6g}}} = {vx_f:.6g}\ \text{{m/s}}")
            st.latex(rf"v_y' = \frac{{p_y}}{{M}} = \frac{{{py_tot:.6g}}}{{{M:.6g}}} = {vy_f:.6g}\ \text{{m/s}}")
            st.latex(rf"|v'| = \sqrt{{v_x'^2 + v_y'^2}} = {v_f:.6g}\ \text{{m/s}}")
            st.latex(rf"\theta = \arctan\!\left(\frac{{v_y'}}{{v_x'}}\right) = {angle:.4g}°")

    elif mode == "Givet v₁' – find v₂' (impulsbevarelse alene)":
        st.markdown("**Objekt 1 – efter kollision (kendte):**")
        c7, c8 = st.columns(2)
        v1x_after = c7.number_input("v₁ₓ' (m/s)", value=1.0, format="%.6g", key="2d_v1xa")
        v1y_after = c8.number_input("v₁ᵧ' (m/s)", value=2.0, format="%.6g", key="2d_v1ya")

        v2x_after = (px_tot - m1 * v1x_after) / m2
        v2y_after = (py_tot - m1 * v1y_after) / m2
        v2_after  = np.sqrt(v2x_after**2 + v2y_after**2)
        angle2    = np.degrees(np.arctan2(v2y_after, v2x_after))

        KE_after = (0.5 * m1 * (v1x_after**2 + v1y_after**2)
                    + 0.5 * m2 * (v2x_after**2 + v2y_after**2))

        col1, col2, col3 = st.columns(3)
        col1.success(f"**v₂ₓ' = {v2x_after:.6g} m/s**")
        col2.success(f"**v₂ᵧ' = {v2y_after:.6g} m/s**")
        col3.success(f"**|v₂'| = {v2_after:.6g} m/s,  θ = {angle2:.4g}°**")

        col4, col5, col6 = st.columns(3)
        col4.metric("KE før", f"{KE_before:.4g} J")
        col5.metric("KE efter", f"{KE_after:.4g} J")
        col6.metric("ΔKE", f"{KE_after - KE_before:.4g} J")

        with st.expander("Vis udregning"):
            st.latex(rf"v_{{2x}}' = \frac{{p_x - m_1 v_{{1x}}'}}{{m_2}} = \frac{{{px_tot:.6g} - {m1:.6g} \cdot {v1x_after:.6g}}}{{{m2:.6g}}} = {v2x_after:.6g}\ \text{{m/s}}")
            st.latex(rf"v_{{2y}}' = \frac{{p_y - m_1 v_{{1y}}'}}{{m_2}} = \frac{{{py_tot:.6g} - {m1:.6g} \cdot {v1y_after:.6g}}}{{{m2:.6g}}} = {v2y_after:.6g}\ \text{{m/s}}")

    else:
        p_tot = np.sqrt(px_tot**2 + py_tot**2)
        angle_p = np.degrees(np.arctan2(py_tot, px_tot))
        col1, col2, col3 = st.columns(3)
        col1.metric("pₓ total", f"{px_tot:.6g} kg·m/s")
        col2.metric("pᵧ total", f"{py_tot:.6g} kg·m/s")
        col3.metric("|p| total", f"{p_tot:.6g} kg·m/s,  θ={angle_p:.4g}°")
        st.metric("KE total (før)", f"{KE_before:.6g} J")
        with st.expander("Vis udregning"):
            st.latex(rf"p_x = m_1 v_{{1x}} + m_2 v_{{2x}} = {m1:.6g}\cdot{v1x:.6g} + {m2:.6g}\cdot{v2x:.6g} = {px_tot:.6g}\ \text{{kg·m/s}}")
            st.latex(rf"p_y = m_1 v_{{1y}} + m_2 v_{{2y}} = {m1:.6g}\cdot{v1y:.6g} + {m2:.6g}\cdot{v2y:.6g} = {py_tot:.6g}\ \text{{kg·m/s}}")
            st.latex(rf"|p| = \sqrt{{p_x^2+p_y^2}} = {p_tot:.6g}\ \text{{kg·m/s}}")

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
        KE_pct = f"  ({(1 - KE_after/KE_before)*100:.2f}%)" if KE_before > 1e-12 else ""
        st.metric("KE-tab", f"{KE_before - KE_after:.4g} J{KE_pct}")

elif formel == "Eksplosion / udskydning":
    st.latex(r"0 = m_1 v_1' + m_2 v_2' \quad \text{(system i ro før)}")
    st.markdown("Impuls bevares. Starter systemet i ro, er den samlede impuls = 0 efterfølgende.")
    st.divider()

    beregn = st.radio("Beregn:", ["v₂' – hastighed af del 2", "v₁' – hastighed af del 1", "m₁ – masse af del 1"], horizontal=True)
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
        if st.button("📋 Gem v₂'", key="gem_eksp_v2"):
            gem_resultat(v2p, "m/s", "v₂'")

    elif beregn == "v₁' – hastighed af del 1":
        st.markdown("**Kendt:** masse og hastighed af del 2 → Find hastighed af del 1")
        c1, c2, c3 = st.columns(3)
        m1  = c1.number_input("m₁ – masse af del 1 (kg)", value=2.0, min_value=1e-12, format="%.6g", key="eksp_m1b")
        m2  = c2.number_input("m₂ – masse af del 2 (kg)", value=6.0, min_value=1e-12, format="%.6g", key="eksp_m2b")
        v2p = c3.number_input("v₂' – hastighed af del 2 (m/s)", value=1.0, format="%.6g", key="eksp_v2b")
        v1p = -m2 * v2p / m1
        st.success(f"**v₁' = {v1p:.6g} m/s  (|v₁'| = {abs(v1p):.6g} m/s)**")
        KE = 0.5 * m1 * v1p**2 + 0.5 * m2 * v2p**2
        st.info(f"Frigivet kinetisk energi: {KE:.4g} J")
        st.latex(
            rf"v_1' = -\frac{{m_2 v_2'}}{{m_1}} = -\frac{{{m2:.6g} \cdot {v2p:.6g}}}{{{m1:.6g}}} = {v1p:.6g}\ \text{{m/s}}"
        )
        if st.button("📋 Gem v₁'", key="gem_eksp_v1"):
            gem_resultat(abs(v1p), "m/s", "|v₁'|")

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

elif formel == "Impuls og gennemsnitskraft:  J = F·Δt = m·Δv":
    st.latex(r"J = \Delta p = m \cdot \Delta v = F_{avg} \cdot \Delta t")
    st.divider()

    mode_imp = st.radio("Beregn:", [
        "J – impuls fra Δv",
        "F_avg – gennemsnitskraft fra J og Δt",
        "Stød mod væg (elastisk) – F_avg",
    ], horizontal=True)
    st.divider()

    G_kol = 9.82

    if mode_imp == "J – impuls fra Δv":
        c1, c2, c3 = st.columns(3)
        m_imp   = c1.number_input("m – masse (kg)", value=0.1, min_value=1e-12, format="%.6g", key="imp_m")
        v1_imp  = c2.number_input("v₁ – hastighed før (m/s)", value=10.0, format="%.6g", key="imp_v1")
        v2_imp  = c3.number_input("v₂ – hastighed efter (m/s)", value=-8.0, format="%.6g", key="imp_v2")
        J_imp = m_imp * (v2_imp - v1_imp)
        st.success(f"**J = {J_imp:.6g} N·s**")
        st.latex(rf"J = m(v_2 - v_1) = {m_imp:.6g} \cdot ({v2_imp:.6g} - {v1_imp:.6g}) = {J_imp:.6g}\ \text{{N·s}}")
        dt_opt = st.number_input("Δt – kontakttid (s, valgfrit)", value=0.001, min_value=1e-12, format="%.6g", key="imp_dt_opt")
        F_avg_opt = abs(J_imp) / dt_opt
        st.info(f"Gennemsnitskraft: **F_avg = |J|/Δt = {F_avg_opt:.4g} N**")
        st.latex(rf"F_{{avg}} = \frac{{|J|}}{{\Delta t}} = \frac{{{abs(J_imp):.6g}}}{{{dt_opt:.6g}}} = {F_avg_opt:.6g}\ \text{{N}}")

    elif mode_imp == "F_avg – gennemsnitskraft fra J og Δt":
        c1, c2 = st.columns(2)
        J_val = c1.number_input("J – impuls (N·s)", value=1.8, format="%.6g", key="imp_J")
        dt_val = c2.number_input("Δt – kontakttid (s)", value=0.001, min_value=1e-12, format="%.6g", key="imp_dt")
        F_avg_val = abs(J_val) / dt_val
        st.success(f"**F_avg = {F_avg_val:.6g} N**")
        st.latex(rf"F_{{avg}} = \frac{{|J|}}{{\Delta t}} = \frac{{{abs(J_val):.6g}}}{{{dt_val:.6g}}} = {F_avg_val:.6g}\ \text{{N}}")

    else:
        st.markdown("**Elastisk stød mod væg** — kun normalkraftskomponenten vendes.")
        c1, c2, c3, c4 = st.columns(4)
        m_w  = c1.number_input("m – masse (kg)", value=0.1, min_value=1e-12, format="%.6g", key="wall_m")
        v_w  = c2.number_input("v – fart (m/s)", value=10.0, min_value=0.0, format="%.6g", key="wall_v")
        ang  = c3.number_input("θ – vinkel med væg­normalen (°)", value=0.0, min_value=0.0, max_value=89.9, format="%.6g", key="wall_ang")
        dt_w = c4.number_input("Δt – kontakttid (s)", value=1e-3, min_value=1e-15, format="%.6g", key="wall_dt")
        v_n = v_w * np.cos(np.radians(ang))
        J_w = 2 * m_w * v_n
        F_avg_w = J_w / dt_w
        st.success(f"**|J| = {J_w:.6g} N·s**")
        st.success(f"**F_avg = {F_avg_w:.6g} N**")
        st.latex(rf"J = 2 m v \cos\theta = 2 \cdot {m_w:.6g} \cdot {v_w:.6g} \cdot \cos({ang:.4g}°) = {J_w:.6g}\ \text{{N·s}}")
        st.latex(rf"F_{{avg}} = \frac{{J}}{{\Delta t}} = \frac{{{J_w:.6g}}}{{{dt_w:.6g}}} = {F_avg_w:.6g}\ \text{{N}}")

elif formel == "Kuglestød – bullet i klods (lodret):  v' = mv/(M+m)":
    st.latex(r"v' = \frac{m \cdot v_i}{M + m} \qquad h = \frac{v'^2}{2g}")
    st.markdown("Kugle (masse **m**, hastighed **v_i** opad) skydes lodret ind i klods (masse **M**, i hvile). Fuldstændig uelastisk kollision. Klodsen stiger til højde **h**.")
    st.divider()

    G_kol2 = 9.82
    mode_kb = st.radio("Beregn:", ["h – maksimal højde", "v_i – kugles starthastighed", "m – kugles masse"], horizontal=True)
    st.divider()

    if mode_kb == "h – maksimal højde":
        c1, c2, c3 = st.columns(3)
        m_kb  = c1.number_input("m – kugles masse (kg)", value=0.01, min_value=1e-12, format="%.6g", key="kb_m")
        vi_kb = c2.number_input("v_i – kugles hastighed (m/s)", value=400.0, min_value=0.0, format="%.6g", key="kb_vi")
        M_kb  = c3.number_input("M – klodses masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="kb_M")
        g_kb  = st.number_input("g (m/s²)", value=G_kol2, format="%.6g", key="kb_g")

        vp_kb = m_kb * vi_kb / (M_kb + m_kb)
        h_kb  = vp_kb**2 / (2 * g_kb)

        col1, col2 = st.columns(2)
        col1.success(f"**v' = {vp_kb:.6g} m/s** (efter stød)")
        col2.success(f"**h = {h_kb:.6g} m**")
        st.latex(rf"v' = \frac{{m \cdot v_i}}{{M+m}} = \frac{{{m_kb:.6g} \cdot {vi_kb:.6g}}}{{{M_kb+m_kb:.6g}}} = {vp_kb:.6g}\ \text{{m/s}}")
        st.latex(rf"h = \frac{{v'^2}}{{2g}} = \frac{{{vp_kb:.6g}^2}}{{2 \cdot {g_kb:.6g}}} = {h_kb:.6g}\ \text{{m}}")

        KE_before = 0.5 * m_kb * vi_kb**2
        KE_after  = 0.5 * (M_kb + m_kb) * vp_kb**2
        with st.expander("Vis energitab"):
            col3, col4, col5 = st.columns(3)
            col3.metric("KE før (kugle)", f"{KE_before:.4g} J")
            col4.metric("KE efter (system)", f"{KE_after:.4g} J")
            pct = (1 - KE_after / KE_before) * 100 if KE_before > 0 else 0
            col5.metric("Tab", f"{KE_before-KE_after:.4g} J  ({pct:.1f}%)")

    elif mode_kb == "v_i – kugles starthastighed":
        c1, c2, c3 = st.columns(3)
        m_kb  = c1.number_input("m – kugles masse (kg)", value=0.01, min_value=1e-12, format="%.6g", key="kb_m2")
        M_kb  = c2.number_input("M – klodses masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="kb_M2")
        h_kb  = c3.number_input("h – opnået højde (m)", value=0.8, min_value=0.0, format="%.6g", key="kb_h2")
        g_kb  = st.number_input("g (m/s²)", value=G_kol2, format="%.6g", key="kb_g2")

        vp_kb = np.sqrt(2 * g_kb * h_kb)
        vi_kb = vp_kb * (M_kb + m_kb) / m_kb
        st.success(f"**v_i = {vi_kb:.6g} m/s**")
        st.latex(rf"v' = \sqrt{{2gh}} = {vp_kb:.6g}\ \text{{m/s}}")
        st.latex(rf"v_i = v' \cdot \frac{{M+m}}{{m}} = {vp_kb:.6g} \cdot \frac{{{M_kb+m_kb:.6g}}}{{{m_kb:.6g}}} = {vi_kb:.6g}\ \text{{m/s}}")

    else:
        c1, c2, c3 = st.columns(3)
        vi_kb = c1.number_input("v_i – kugles hastighed (m/s)", value=400.0, min_value=1e-12, format="%.6g", key="kb_vi3")
        M_kb  = c2.number_input("M – klodses masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="kb_M3")
        h_kb  = c3.number_input("h – opnået højde (m)", value=0.8, min_value=0.0, format="%.6g", key="kb_h3")
        g_kb  = st.number_input("g (m/s²)", value=G_kol2, format="%.6g", key="kb_g3")

        vp_kb = np.sqrt(2 * g_kb * h_kb)
        denom_kb = vi_kb - vp_kb
        if abs(denom_kb) < 1e-12:
            st.error("Ingen løsning – v_i = v'")
        else:
            m_kb = M_kb * vp_kb / denom_kb
            if m_kb <= 0:
                st.error("Ugyldig løsning – kontrollér inputværdier.")
            else:
                st.success(f"**m = {m_kb:.6g} kg**")
                st.latex(rf"m = \frac{{M \cdot v'}}{{v_i - v'}} = \frac{{{M_kb:.6g} \cdot {vp_kb:.6g}}}{{{vi_kb:.6g} - {vp_kb:.6g}}} = {m_kb:.6g}\ \text{{kg}}")
