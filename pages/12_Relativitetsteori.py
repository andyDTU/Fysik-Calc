import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Relativitetsteori", page_icon="🚀", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🚀", "Relativitetsteori")
st.title("🚀 Speciel Relativitetsteori")
st.markdown("Lorentz-faktor, tidsudvidelse, længdeforkortning og relativistisk energi")
st.divider()

c = 2.998e8   # lysets hastighed (m/s)

_REL_FORMULAS = [
    ("Lorentz-faktor",       "γ = 1/√(1−v²/c²)",             "Lorentz-faktor:  γ = 1 / √(1 − v²/c²)"),
    ("Tidsudvidelse",        "Δt = γ · Δt₀",                 "Tidsudvidelse:  Δt = γ · Δt₀"),
    ("Længdeforkortning",    "L = L₀ / γ",                   "Længdeforkortning:  L = L₀ / γ"),
    ("Relativistisk Ek",     "Ek = (γ−1)·m₀c²",              "Relativistisk kinetisk energi:  Ek = (γ − 1) · m₀c²"),
    ("Relativistisk E",      "E = γ · m₀c²",                 "Relativistisk totalenergi:  E = γ · m₀c²"),
    ("Relativistisk impuls", "p = γ · m₀ · v",               "Relativistisk impuls:  p = γ · m₀ · v"),
    ("E²–p²–relation",       "E² = (pc)² + (m₀c²)²",        "Energi–impuls relation:  E² = (pc)² + (m₀c²)²"),
]
formel = formula_card_grid(_REL_FORMULAS, "rel_formel")

REL_TIPS = {
    "Lorentz-faktor:  γ = 1 / √(1 − v²/c²)": "γ ≥ 1 altid. v → c giver γ → ∞. Ved v = 0.866c er γ = 2. Brug β = v/c for overskuelighed.",
    "Tidsudvidelse:  Δt = γ · Δt₀": "Δt₀ = egentid (målt af medrejsende ur). Δt = Δt₀·γ > Δt₀. Bevægende ure går langsomt.",
    "Længdeforkortning:  L = L₀ / γ": "L₀ = egenlængde (hvile). L = L₀/γ < L₀. Forkortning i bevægelsesretningen.",
    "Relativistisk kinetisk energi:  Ek = (γ − 1) · m₀c²": "Ved v ≪ c: Ek ≈ ½m₀v² (klassisk). Hvileenergi E₀ = m₀c² er ikke inkluderet i Ek.",
    "Relativistisk totalenergi:  E = γ · m₀c²": "E = Ek + E₀ = γm₀c². For fotoner: m₀ = 0, E = pc.",
    "Relativistisk impuls:  p = γ · m₀ · v": "p = γm₀v. Ved v ≪ c: p ≈ m₀v. Impuls bevares i relativistisk kollision.",
    "Energi–impuls relation:  E² = (pc)² + (m₀c²)²": "Gælder for ALT inkl. fotoner (m₀=0: E=pc). Lorentz-invariant.",
}
show_tips(formel, REL_TIPS)
st.divider()

# ── Lorentz-faktor ─────────────────────────────────────────────────────────────
if formel == "Lorentz-faktor:  γ = 1 / √(1 − v²/c²)":
    st.latex(r"\gamma = \frac{1}{\sqrt{1 - \beta^2}}, \quad \beta = \frac{v}{c}")
    beregn = st.radio("Givet:", ["v – hastighed (m/s)", "β = v/c", "γ – Lorentz-faktor"], horizontal=True)
    st.divider()

    if beregn == "v – hastighed (m/s)":
        v = st.number_input("v (m/s)", value=2.0e8, min_value=0.0, max_value=c*(1-1e-10), format="%.6g")
        beta = v / c
        gamma = 1 / np.sqrt(1 - beta**2)
        col1, col2, col3 = st.columns(3)
        col1.metric("β = v/c", f"{beta:.6g}")
        col2.metric("γ", f"{gamma:.6g}")
        col3.metric("v/c i %", f"{beta*100:.4g} %")
        st.success(f"**γ = {gamma:.6g}**")
        st.latex(rf"\beta = \frac{{v}}{{c}} = \frac{{{v:.4g}}}{{{c:.4g}}} = {beta:.6g}")
        st.latex(rf"\gamma = \frac{{1}}{{\sqrt{{1 - {beta:.6g}^2}}}} = {gamma:.6g}")
        if st.button("📋 Gem γ", key="gem_rel_gamma_v"):
            gem_resultat(gamma, "", "γ")

    elif beregn == "β = v/c":
        beta = st.number_input("β = v/c", value=0.8, min_value=0.0, max_value=1.0-1e-10, format="%.6g")
        v = beta * c
        gamma = 1 / np.sqrt(1 - beta**2)
        st.success(f"**γ = {gamma:.6g}**   (v = {v:.4g} m/s)")
        st.latex(rf"\gamma = \frac{{1}}{{\sqrt{{1 - {beta:.6g}^2}}}} = {gamma:.6g}")
        if st.button("📋 Gem γ", key="gem_rel_gamma_beta"):
            gem_resultat(gamma, "", "γ")

    else:
        gamma = st.number_input("γ – Lorentz-faktor", value=2.0, min_value=1.0, format="%.6g")
        beta = np.sqrt(1 - 1/gamma**2)
        v = beta * c
        st.success(f"**v = {v:.6g} m/s**   (β = {beta:.6g})")
        st.latex(rf"\beta = \sqrt{{1 - \frac{{1}}{{\gamma^2}}}} = \sqrt{{1 - \frac{{1}}{{{gamma:.4g}^2}}}} = {beta:.6g}")
        if st.button("📋 Gem v", key="gem_rel_gamma_from_gamma"):
            gem_resultat(v, "m/s", "v")

# ── Tidsudvidelse ──────────────────────────────────────────────────────────────
elif formel == "Tidsudvidelse:  Δt = γ · Δt₀":
    st.latex(r"\Delta t = \gamma \cdot \Delta t_0")
    st.markdown("**Δt₀** = egentid (ur i hvile i sin ramme) · **Δt** = tid målt i laboratorierammen")
    beregn = st.radio("Beregn:", ["Δt (laboratorieramme)", "Δt₀ (egentid)", "γ fra Δt og Δt₀"], horizontal=True)
    st.divider()

    if beregn == "Δt (laboratorieramme)":
        c1, c2 = st.columns(2)
        dt0 = c1.number_input("Δt₀ – egentid (s)", value=1.0, min_value=1e-20, format="%.6g")
        gamma = c2.number_input("γ – Lorentz-faktor", value=2.0, min_value=1.0, format="%.6g")
        dt = gamma * dt0
        st.success(f"**Δt = {dt:.6g} s**")
        st.latex(rf"\Delta t = \gamma \cdot \Delta t_0 = {gamma:.6g} \cdot {dt0:.6g} = {dt:.6g}\ \text{{s}}")
        if st.button("📋 Gem Δt", key="gem_rel_dt"):
            gem_resultat(dt, "s", "Δt")

    elif beregn == "Δt₀ (egentid)":
        c1, c2 = st.columns(2)
        dt = c1.number_input("Δt – observeret tid (s)", value=2.0, min_value=1e-20, format="%.6g")
        gamma = c2.number_input("γ – Lorentz-faktor", value=2.0, min_value=1.0, format="%.6g")
        dt0 = dt / gamma
        st.success(f"**Δt₀ = {dt0:.6g} s**")
        st.latex(rf"\Delta t_0 = \frac{{\Delta t}}{{\gamma}} = \frac{{{dt:.6g}}}{{{gamma:.6g}}} = {dt0:.6g}\ \text{{s}}")
        if st.button("📋 Gem Δt₀", key="gem_rel_dt0"):
            gem_resultat(dt0, "s", "Δt₀")

    else:
        c1, c2 = st.columns(2)
        dt = c1.number_input("Δt – observeret tid (s)", value=2.0, min_value=1e-20, format="%.6g")
        dt0 = c2.number_input("Δt₀ – egentid (s)", value=1.0, min_value=1e-20, format="%.6g")
        gamma = dt / dt0
        if gamma < 1:
            st.error("Δt < Δt₀ er ikke fysisk muligt (γ < 1)")
        else:
            beta = np.sqrt(1 - 1/gamma**2)
            v = beta * c
            st.success(f"**γ = {gamma:.6g}**   (v = {v:.4g} m/s, β = {beta:.4g})")
            if st.button("📋 Gem γ", key="gem_rel_gamma_from_t"):
                gem_resultat(gamma, "", "γ")

# ── Længdeforkortning ──────────────────────────────────────────────────────────
elif formel == "Længdeforkortning:  L = L₀ / γ":
    st.latex(r"L = \frac{L_0}{\gamma}")
    st.markdown("**L₀** = egenlængde (hvile) · **L** = observeret længde i bevægelsesretningen")
    beregn = st.radio("Beregn:", ["L (observeret)", "L₀ (egenlængde)", "γ fra L og L₀"], horizontal=True)
    st.divider()

    if beregn == "L (observeret)":
        c1, c2 = st.columns(2)
        L0 = c1.number_input("L₀ – egenlængde (m)", value=1.0, min_value=1e-20, format="%.6g")
        gamma = c2.number_input("γ – Lorentz-faktor", value=2.0, min_value=1.0, format="%.6g")
        L = L0 / gamma
        st.success(f"**L = {L:.6g} m**   (forkortning: {(1-1/gamma)*100:.3g} %)")
        st.latex(rf"L = \frac{{L_0}}{{\gamma}} = \frac{{{L0:.6g}}}{{{gamma:.6g}}} = {L:.6g}\ \text{{m}}")
        if st.button("📋 Gem L", key="gem_rel_L"):
            gem_resultat(L, "m", "L")

    elif beregn == "L₀ (egenlængde)":
        c1, c2 = st.columns(2)
        L = c1.number_input("L – observeret længde (m)", value=0.5, min_value=1e-20, format="%.6g")
        gamma = c2.number_input("γ – Lorentz-faktor", value=2.0, min_value=1.0, format="%.6g")
        L0 = L * gamma
        st.success(f"**L₀ = {L0:.6g} m**")
        st.latex(rf"L_0 = L \cdot \gamma = {L:.6g} \cdot {gamma:.6g} = {L0:.6g}\ \text{{m}}")
        if st.button("📋 Gem L₀", key="gem_rel_L0"):
            gem_resultat(L0, "m", "L₀")

    else:
        c1, c2 = st.columns(2)
        L0 = c1.number_input("L₀ – egenlængde (m)", value=1.0, min_value=1e-20, format="%.6g")
        L  = c2.number_input("L – observeret (m)", value=0.5, min_value=1e-20, format="%.6g")
        if L > L0:
            st.error("L > L₀ – forkortning kan ikke gøre objektet længere")
        else:
            gamma = L0 / L
            beta = np.sqrt(1 - 1/gamma**2)
            v = beta * c
            st.success(f"**γ = {gamma:.6g}**   (v = {v:.4g} m/s, β = {beta:.4g})")

# ── Relativistisk kinetisk energi ──────────────────────────────────────────────
elif formel == "Relativistisk kinetisk energi:  Ek = (γ − 1) · m₀c²":
    st.latex(r"E_k = (\gamma - 1) \cdot m_0 c^2")
    st.markdown("Totalenergi: **E = γm₀c²** · Hvileenergi: **E₀ = m₀c²** · Kinetisk: **Ek = E − E₀**")
    st.divider()

    c1, c2 = st.columns(2)
    m0_input = c1.number_input("m₀ – hvilemasse (kg)", value=9.109e-31, min_value=1e-40, format="%.6g",
                                 help="Elektron: 9.109e-31 kg, Proton: 1.673e-27 kg")
    beta = c2.number_input("β = v/c", value=0.9, min_value=0.0, max_value=1.0-1e-10, format="%.6g")

    gamma = 1 / np.sqrt(1 - beta**2)
    v = beta * c
    E0 = m0_input * c**2
    Ek = (gamma - 1) * E0
    E_total = gamma * E0
    Ek_eV = Ek / 1.602e-19

    col1, col2, col3 = st.columns(3)
    col1.metric("γ", f"{gamma:.6g}")
    col2.metric("Ek (J)", f"{Ek:.4g}")
    col3.metric("Ek (eV)", f"{Ek_eV:.4g}")

    st.success(f"**Ek = {Ek:.6g} J  =  {Ek_eV:.6g} eV**")
    st.latex(rf"E_k = (\gamma - 1) m_0 c^2 = ({gamma:.6g} - 1) \cdot {m0_input:.4g} \cdot ({c:.4g})^2 = {Ek:.4g}\ \text{{J}}")

    with st.expander("Vis klassisk sammenligning"):
        Ek_klass = 0.5 * m0_input * v**2
        rel_fejl = abs(Ek - Ek_klass) / Ek * 100
        st.markdown(f"Klassisk Ek = ½m₀v² = **{Ek_klass:.4g} J**  |  Relativistisk fejl: **{rel_fejl:.2f}%**")
        if rel_fejl < 1:
            st.info("Klassisk tilnærmelse er god (< 1% fejl) ved denne hastighed.")
        else:
            st.warning(f"Klassisk formel giver {rel_fejl:.1f}% fejl – brug relativistisk formel!")

    if st.button("📋 Gem Ek", key="gem_rel_Ek"):
        gem_resultat(Ek, "J", "Ek")

# ── Totalenergi ────────────────────────────────────────────────────────────────
elif formel == "Relativistisk totalenergi:  E = γ · m₀c²":
    st.latex(r"E = \gamma m_0 c^2 = E_k + m_0 c^2")
    st.divider()

    c1, c2 = st.columns(2)
    m0_input = c1.number_input("m₀ – hvilemasse (kg)", value=1.673e-27, min_value=1e-40, format="%.6g")
    beta = c2.number_input("β = v/c", value=0.5, min_value=0.0, max_value=1.0-1e-10, format="%.6g")

    gamma = 1 / np.sqrt(1 - beta**2)
    E0 = m0_input * c**2
    E_total = gamma * E0
    Ek = (gamma - 1) * E0
    E_eV = E_total / 1.602e-19

    col1, col2, col3 = st.columns(3)
    col1.metric("E₀ = m₀c² (J)", f"{E0:.4g}")
    col2.metric("Ek (J)", f"{Ek:.4g}")
    col3.metric("E_total (J)", f"{E_total:.4g}")

    st.success(f"**E = {E_total:.6g} J  =  {E_eV:.6g} eV**")
    st.latex(rf"E = \gamma m_0 c^2 = {gamma:.6g} \cdot {m0_input:.4g} \cdot ({c:.4g})^2 = {E_total:.4g}\ \text{{J}}")
    if st.button("📋 Gem E", key="gem_rel_Etot"):
        gem_resultat(E_total, "J", "E")

# ── Relativistisk impuls ───────────────────────────────────────────────────────
elif formel == "Relativistisk impuls:  p = γ · m₀ · v":
    st.latex(r"p = \gamma m_0 v")
    st.divider()

    c1, c2 = st.columns(2)
    m0_input = c1.number_input("m₀ – hvilemasse (kg)", value=1.673e-27, min_value=1e-40, format="%.6g")
    beta = c2.number_input("β = v/c", value=0.5, min_value=0.0, max_value=1.0-1e-10, format="%.6g")

    gamma = 1 / np.sqrt(1 - beta**2)
    v = beta * c
    p = gamma * m0_input * v
    p_klass = m0_input * v

    st.success(f"**p = {p:.6g} kg·m/s**")
    st.latex(rf"p = \gamma m_0 v = {gamma:.6g} \cdot {m0_input:.4g} \cdot {v:.4g} = {p:.4g}\ \text{{kg·m/s}}")
    st.caption(f"Klassisk p = m₀v = {p_klass:.4g} kg·m/s  (forskel: {(p/p_klass - 1)*100:.2f}%)")
    if st.button("📋 Gem p", key="gem_rel_p"):
        gem_resultat(p, "kg·m/s", "p")

# ── E² = (pc)² + (m₀c²)² ──────────────────────────────────────────────────────
elif formel == "Energi–impuls relation:  E² = (pc)² + (m₀c²)²":
    st.latex(r"E^2 = (pc)^2 + (m_0 c^2)^2")
    st.markdown("Gælder for alle partikler inkl. fotoner (m₀ = 0: E = pc).")
    beregn = st.radio("Beregn:", ["E (given p og m₀)", "p (given E og m₀)", "m₀ (given E og p)"], horizontal=True)
    st.divider()

    if beregn == "E (given p og m₀)":
        c1, c2 = st.columns(2)
        p = c1.number_input("p – impuls (kg·m/s)", value=1e-20, format="%.6g")
        m0_input = c2.number_input("m₀ – hvilemasse (kg, 0=foton)", value=9.109e-31, min_value=0.0, format="%.6g")
        E = np.sqrt((p * c)**2 + (m0_input * c**2)**2)
        E_eV = E / 1.602e-19
        st.success(f"**E = {E:.6g} J  =  {E_eV:.4g} eV**")
        st.latex(rf"E = \sqrt{{(pc)^2 + (m_0 c^2)^2}} = {E:.4g}\ \text{{J}}")
        if st.button("📋 Gem E", key="gem_rel_Eimp"):
            gem_resultat(E, "J", "E")

    elif beregn == "p (given E og m₀)":
        c1, c2 = st.columns(2)
        E = c1.number_input("E – totalenergi (J)", value=1e-13, min_value=0.0, format="%.6g")
        m0_input = c2.number_input("m₀ – hvilemasse (kg, 0=foton)", value=9.109e-31, min_value=0.0, format="%.6g")
        val = (E**2 - (m0_input * c**2)**2) / c**2
        if val < 0:
            st.error("E < m₀c² – energien er lavere end hvileenergien. Ikke fysisk muligt.")
        else:
            p = np.sqrt(val)
            st.success(f"**p = {p:.6g} kg·m/s**")
            st.latex(rf"p = \frac{{\sqrt{{E^2 - (m_0 c^2)^2}}}}{{c}} = {p:.4g}\ \text{{kg·m/s}}")
            if st.button("📋 Gem p", key="gem_rel_pimp"):
                gem_resultat(p, "kg·m/s", "p")

    else:
        c1, c2 = st.columns(2)
        E = c1.number_input("E – totalenergi (J)", value=1e-13, min_value=0.0, format="%.6g")
        p = c2.number_input("p – impuls (kg·m/s)", value=1e-22, min_value=0.0, format="%.6g")
        val = (E**2 - (p * c)**2) / c**4
        if val < 0:
            st.error("E² < (pc)² – ikke en gyldig massiv partikel.")
        else:
            m0_input = np.sqrt(val)
            st.success(f"**m₀ = {m0_input:.6g} kg**")
            st.latex(rf"m_0 = \frac{{\sqrt{{E^2 - (pc)^2}}}}{{c^2}} = {m0_input:.4g}\ \text{{kg}}")
            if st.button("📋 Gem m₀", key="gem_rel_m0"):
                gem_resultat(m0_input, "kg", "m₀")
