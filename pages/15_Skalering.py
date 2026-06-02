import streamlit as st
import numpy as np
import pandas as pd
from fractions import Fraction
from utils import show_sidebar_constants, show_resultat_sidebar, breadcrumb

st.set_page_config(page_title="Skalering", page_icon="📏", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("📏", "Skalering")
st.title("📏 Skaleringsanalyse")
st.markdown("Hvad sker der med Y, når X ændres med en faktor? Baseret på potenslov-relationer.")
st.divider()

SCALE_FORMULAS = [
    {
        "navn": "Fjedermasse-periode  T = 2π√(m/k)",
        "latex": r"T = 2\pi\sqrt{\frac{m}{k}}",
        "vars": {"m": 0.5, "k": -0.5},
        "target": "T",
        "beskrivelse": "Periode for fjeder-masse-system",
    },
    {
        "navn": "Pendul-periode  T = 2π√(L/g)",
        "latex": r"T = 2\pi\sqrt{\frac{L}{g}}",
        "vars": {"L": 0.5, "g": -0.5},
        "target": "T",
        "beskrivelse": "",
    },
    {
        "navn": "Projektilrækkevidde  x = v₀²sin(2θ)/g",
        "latex": r"x = \frac{v_0^2 \sin 2\theta}{g}",
        "vars": {"v₀": 2.0, "g": -1.0},
        "target": "x",
        "beskrivelse": "",
    },
    {
        "navn": "Keplers 3. lov  T² ∝ r³",
        "latex": r"T \propto r^{3/2}",
        "vars": {"r": 1.5},
        "target": "T",
        "beskrivelse": "Omløbstid for planet/satellit",
    },
    {
        "navn": "Coulombs lov  F = kq₁q₂/r²",
        "latex": r"F = k\frac{q_1 q_2}{r^2}",
        "vars": {"q₁": 1.0, "q₂": 1.0, "r": -2.0},
        "target": "F",
        "beskrivelse": "",
    },
    {
        "navn": "Kinetisk energi  Ek = ½mv²",
        "latex": r"E_k = \frac{1}{2}mv^2",
        "vars": {"m": 1.0, "v": 2.0},
        "target": "Ek",
        "beskrivelse": "",
    },
    {
        "navn": "Gravitationsfelt  g = GM/r²",
        "latex": r"g = \frac{GM}{r^2}",
        "vars": {"M": 1.0, "r": -2.0},
        "target": "g",
        "beskrivelse": "",
    },
    {
        "navn": "RC tidskonstant  τ = RC",
        "latex": r"\tau = R \cdot C",
        "vars": {"R": 1.0, "C": 1.0},
        "target": "τ",
        "beskrivelse": "",
    },
    {
        "navn": "Tyngdekraftens potentielle energi  Ep = mgh",
        "latex": r"E_p = mgh",
        "vars": {"m": 1.0, "g": 1.0, "h": 1.0},
        "target": "Ep",
        "beskrivelse": "",
    },
    {
        "navn": "Elektrisk modstand (cylindrisk)  R = ρL/A",
        "latex": r"R = \frac{\rho L}{A}",
        "vars": {"ρ": 1.0, "L": 1.0, "A": -1.0},
        "target": "R",
        "beskrivelse": "",
    },
]

valgt = st.selectbox("Vælg formel:", [f["navn"] for f in SCALE_FORMULAS])
f_data = next(f for f in SCALE_FORMULAS if f["navn"] == valgt)

st.latex(f_data["latex"])
if f_data["beskrivelse"]:
    st.caption(f_data["beskrivelse"])
st.divider()

terms = " · ".join([f"{v}^{{{exp}}}" for v, exp in f_data["vars"].items()])
st.info(f"{f_data['target']} ∝ {terms}")
st.divider()

st.subheader("Angiv ændringsfaktorer")
st.markdown("Hvad ændres med hvilken faktor? (1.0 = uændret, 2.0 = fordoblet, 0.5 = halveret)")
cols = st.columns(min(len(f_data["vars"]), 4))
factors = {}
for i, (var_name, exp) in enumerate(f_data["vars"].items()):
    col = cols[i % len(cols)]
    factors[var_name] = col.number_input(
        f"Faktor for {var_name}",
        value=2.0,
        min_value=0.01,
        format="%.4g",
        key=f"scale_{valgt}_{var_name}",
    )

result_factor = 1.0
for var_name, exp in f_data["vars"].items():
    result_factor *= factors[var_name] ** exp

st.divider()
st.subheader(f"Resultat for {f_data['target']}")

frac = Fraction(result_factor).limit_denominator(100)
if abs(float(frac) - result_factor) < 0.001:
    frac_str = f" = {frac}" if frac.denominator != 1 else ""
else:
    frac_str = ""

if result_factor > 1:
    st.success(f"**{f_data['target']} øges med faktor {result_factor:.4g}{frac_str}** (≈ {result_factor:.4g}×)")
elif result_factor < 1:
    st.warning(f"**{f_data['target']} falder med faktor {1/result_factor:.4g}{frac_str}** (ny værdi = {result_factor:.4g} × gammel)")
else:
    st.info(f"**{f_data['target']} er uændret** (faktor = 1)")

with st.expander("Vis udregning"):
    terms_list = []
    for var_name, exp in f_data["vars"].items():
        contribution = factors[var_name] ** exp
        terms_list.append(f"{var_name}^{{{exp}}} = {factors[var_name]:.4g}^{{{exp}}} = {contribution:.4g}")
    for t in terms_list:
        st.latex(t)
    st.latex(rf"\Rightarrow {f_data['target']} \times {result_factor:.4g}")

st.divider()
st.subheader("Sensitivitetstabel")
st.markdown("Effekt af at **fordoble** hver enkelt variabel:")
rows = []
for var_name, exp in f_data["vars"].items():
    factor_if_doubled = 2.0 ** exp
    rows.append({
        "Variabel": var_name,
        "Eksponent": exp,
        "Faktor (ved fordobling)": f"{factor_if_doubled:.4g}×",
        "Effekt": "øges" if factor_if_doubled > 1 else ("falder" if factor_if_doubled < 1 else "uændret"),
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
