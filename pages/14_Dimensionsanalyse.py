import streamlit as st
import numpy as np
import pandas as pd
import itertools
from utils import show_sidebar_constants, show_resultat_sidebar, formula_card_grid, breadcrumb

st.set_page_config(page_title="Dimensionsanalyse", page_icon="📐", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("📐", "Dimensionsanalyse")
st.title("📐 Dimensionsanalyse")
st.markdown("Dimensionstjek, naturlige skalaer og Buckingham Π-sætningen.")
st.divider()

_DIM_FORMULAS = [
    ("Dimensionstjek",    "Er formlen dimensionsrigtig?",    "Dimensionstjek – formel"),
    ("Naturlige skalaer", "λ og τ fra modelvariable",        "Naturlige skalaer"),
    ("Pi-grupper",        "Buckingham Π-sætning",            "Pi-grupper (Buckingham Π)"),
]

formel = formula_card_grid(_DIM_FORMULAS, "dim_formel")
st.divider()

if formel == "Dimensionstjek – formel":
    st.latex(r"[A] = M^a L^b T^c")
    st.markdown("Tjek om venstre og højre side af en formel har samme dimension.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Venstre side**")
        lhs_navn = st.text_input("Navn (venstre)", value="F", key="lhs_navn")
        lhs_M = st.number_input("M-eksponent", value=1, min_value=-4, max_value=4, step=1, format="%d", key="lhs_M")
        lhs_L = st.number_input("L-eksponent", value=1, min_value=-4, max_value=4, step=1, format="%d", key="lhs_L")
        lhs_T = st.number_input("T-eksponent", value=-2, min_value=-4, max_value=4, step=1, format="%d", key="lhs_T")

    with c2:
        st.markdown("**Højre side**")
        rhs_navn = st.text_input("Navn (højre)", value="m·a", key="rhs_navn")
        rhs_M = st.number_input("M-eksponent", value=1, min_value=-4, max_value=4, step=1, format="%d", key="rhs_M")
        rhs_L = st.number_input("L-eksponent", value=1, min_value=-4, max_value=4, step=1, format="%d", key="rhs_L")
        rhs_T = st.number_input("T-eksponent", value=-2, min_value=-4, max_value=4, step=1, format="%d", key="rhs_T")

    if st.button("Tjek dimension", type="primary"):
        if lhs_M == rhs_M and lhs_L == rhs_L and lhs_T == rhs_T:
            st.success(f"✅ Dimensionshomogen!  [{lhs_navn}] = [{rhs_navn}] = M^{lhs_M} L^{lhs_L} T^{lhs_T}")
        else:
            st.error("❌ Ikke dimensionshomogen")
            diff_M = rhs_M - lhs_M
            diff_L = rhs_L - lhs_L
            diff_T = rhs_T - lhs_T
            mangler = []
            if diff_M != 0:
                mangler.append(f"M: venstre={lhs_M}, højre={rhs_M} (difference {diff_M:+d})")
            if diff_L != 0:
                mangler.append(f"L: venstre={lhs_L}, højre={rhs_L} (difference {diff_L:+d})")
            if diff_T != 0:
                mangler.append(f"T: venstre={lhs_T}, højre={rhs_T} (difference {diff_T:+d})")
            for m_item in mangler:
                st.warning(m_item)

    with st.expander("Eksempler på dimensioner"):
        st.markdown("""
| Størrelse | Dimension | M | L | T |
|-----------|-----------|---|---|---|
| Kraft F | MLT⁻² | 1 | 1 | -2 |
| Energi E | ML²T⁻² | 1 | 2 | -2 |
| Hastighed v | LT⁻¹ | 0 | 1 | -1 |
| Acceleration a | LT⁻² | 0 | 1 | -2 |
| Tryk p | ML⁻¹T⁻² | 1 | -1 | -2 |
| Effekt P | ML²T⁻³ | 1 | 2 | -3 |
| Impuls p | MLT⁻¹ | 1 | 1 | -1 |
| Vinkelfrekvens ω | T⁻¹ | 0 | 0 | -1 |
| Inertimoment I | ML² | 1 | 2 | 0 |
| Ladning q | T·A (her: dimensionsløs T) | 0 | 0 | 1 |
""")

elif formel == "Naturlige skalaer":
    st.latex(r"\lambda,\ \tau,\ \mu \text{ — konstrueret fra modellens parametre}")
    st.markdown("Identificér hvilke kombinationer af variable der har dimension af **længde**, **tid** og **masse**.")
    st.divider()

    PRESETS = {
        "Brugerdefineret": {
            "Variabel": ["", "", "", "", "", "", ""],
            "M": [0, 0, 0, 0, 0, 0, 0],
            "L": [0, 0, 0, 0, 0, 0, 0],
            "T": [0, 0, 0, 0, 0, 0, 0],
        },
        "Mekanisk pendul: m, g, L": {
            "Variabel": ["m", "g", "L", "", "", "", ""],
            "M": [1, 0, 0, 0, 0, 0, 0],
            "L": [0, 1, 1, 0, 0, 0, 0],
            "T": [0, -2, 0, 0, 0, 0, 0],
        },
        "Bølge: f, λ, v": {
            "Variabel": ["f", "λ", "v", "", "", "", ""],
            "M": [0, 0, 0, 0, 0, 0, 0],
            "L": [0, 1, 1, 0, 0, 0, 0],
            "T": [-1, 0, -1, 0, 0, 0, 0],
        },
        "Fjedermasse: m, k": {
            "Variabel": ["m", "k", "", "", "", "", ""],
            "M": [1, 1, 0, 0, 0, 0, 0],
            "L": [0, 0, 0, 0, 0, 0, 0],
            "T": [0, -2, 0, 0, 0, 0, 0],
        },
        "Elektricitet RC: R, C": {
            "Variabel": ["R", "C", "", "", "", "", ""],
            "M": [1, -1, 0, 0, 0, 0, 0],
            "L": [2, -2, 0, 0, 0, 0, 0],
            "T": [-3, 4, 0, 0, 0, 0, 0],
        },
        "Hydrodynamik: ρ, v, L, μ": {
            "Variabel": ["ρ", "v", "L", "μ", "", "", ""],
            "M": [1, 0, 0, 1, 0, 0, 0],
            "L": [-3, 1, 1, -1, 0, 0, 0],
            "T": [0, -1, 0, -1, 0, 0, 0],
        },
        "Q6-model: m, v, L, g, F (acceleration)": {
            "Variabel": ["m", "v", "L", "g", "F", "", ""],
            "M": [1, 0, 0, 0, 1, 0, 0],
            "L": [0, 1, 1, 1, 1, 0, 0],
            "T": [0, -1, 0, -2, -2, 0, 0],
        },
    }

    preset = st.selectbox("Vælg model (eller 'Brugerdefineret'):", list(PRESETS.keys()))
    p = PRESETS[preset]
    var_data = pd.DataFrame({"Variabel": p["Variabel"], "M": p["M"], "L": p["L"], "T": p["T"]})
    edited = st.data_editor(var_data, num_rows="fixed", key="dim_vars", use_container_width=True)

    if preset == "Q6-model: m, v, L, g, F (acceleration)":
        st.info("**Q6-model hint:** λ = v²/g har dimension [L], τ = L/v har dimension [T].")

    if st.button("Find naturlige skalaer", type="primary"):
        rows = edited[edited["Variabel"].str.strip() != ""].copy()
        if len(rows) < 2:
            st.warning("Angiv mindst 2 variable.")
        else:
            vars_list = list(rows["Variabel"])
            dims = list(zip(rows["M"], rows["L"], rows["T"]))
            eksponenter = [-2, -1, 0, 1, 2]

            targets = {
                "[L] (længde)":   (0, 1, 0),
                "[T] (tid)":      (0, 0, 1),
                "[M] (masse)":    (1, 0, 0),
            }

            n_vars = min(len(vars_list), 4)
            found_any = False

            for target_label, target_dim in targets.items():
                løsninger = []
                for idx_combo in itertools.combinations(range(len(vars_list)), min(n_vars, len(vars_list))):
                    combo_vars = [vars_list[i] for i in idx_combo]
                    combo_dims = [dims[i] for i in idx_combo]
                    for exps in itertools.product(eksponenter, repeat=len(combo_vars)):
                        if all(e == 0 for e in exps):
                            continue
                        res_M = sum(combo_dims[j][0] * exps[j] for j in range(len(combo_vars)))
                        res_L = sum(combo_dims[j][1] * exps[j] for j in range(len(combo_vars)))
                        res_T = sum(combo_dims[j][2] * exps[j] for j in range(len(combo_vars)))
                        if (res_M, res_L, res_T) == target_dim:
                            parts = []
                            for vn, ex in zip(combo_vars, exps):
                                if ex != 0:
                                    parts.append(f"{vn}^{ex}" if ex != 1 else vn)
                            expr = " · ".join(parts)
                            løsninger.append(expr)
                            if len(løsninger) >= 5:
                                break
                    if len(løsninger) >= 5:
                        break

                if løsninger:
                    found_any = True
                    st.success(f"**{target_label}**: " + ",   ".join(løsninger[:5]))
                else:
                    st.info(f"**{target_label}**: Ingen kombination fundet med eksponenter ±1,±2.")

            if not found_any:
                st.warning("Ingen naturlige skalaer fundet. Prøv med flere variable eller andre dimensioner.")

elif formel == "Pi-grupper (Buckingham Π)":
    st.latex(r"\Pi\text{-teoremet: } n \text{ variable} - k \text{ dimensioner} = \text{antal dimensionsløse grupper}")
    st.divider()

    PRESETS_PI = {
        "Brugerdefineret": {
            "Variabel": ["", "", "", "", "", "", ""],
            "M": [0, 0, 0, 0, 0, 0, 0],
            "L": [0, 0, 0, 0, 0, 0, 0],
            "T": [0, 0, 0, 0, 0, 0, 0],
        },
        "Mekanisk pendul: m, g, L, T": {
            "Variabel": ["m", "g", "L", "T", "", "", ""],
            "M": [1, 0, 0, 0, 0, 0, 0],
            "L": [0, 1, 1, 0, 0, 0, 0],
            "T": [0, -2, 0, 1, 0, 0, 0],
        },
        "Fjedermasse: m, k, T": {
            "Variabel": ["m", "k", "T", "", "", "", ""],
            "M": [1, 1, 0, 0, 0, 0, 0],
            "L": [0, 0, 0, 0, 0, 0, 0],
            "T": [0, -2, 1, 0, 0, 0, 0],
        },
        "Hydrodynamik: ρ, v, L, μ, F": {
            "Variabel": ["ρ", "v", "L", "μ", "F", "", ""],
            "M": [1, 0, 0, 1, 1, 0, 0],
            "L": [-3, 1, 1, -1, 1, 0, 0],
            "T": [0, -1, 0, -1, -2, 0, 0],
        },
    }

    preset_pi = st.selectbox("Vælg model:", list(PRESETS_PI.keys()), key="pi_preset")
    p2 = PRESETS_PI[preset_pi]
    var_data2 = pd.DataFrame({"Variabel": p2["Variabel"], "M": p2["M"], "L": p2["L"], "T": p2["T"]})
    edited2 = st.data_editor(var_data2, num_rows="fixed", key="pi_vars", use_container_width=True)

    if st.button("Find Pi-grupper", type="primary"):
        rows2 = edited2[edited2["Variabel"].str.strip() != ""].copy()
        n = len(rows2)
        if n < 2:
            st.warning("Angiv mindst 2 variable.")
        else:
            vars_list2 = list(rows2["Variabel"])
            A = np.array(list(zip(rows2["M"], rows2["L"], rows2["T"])), dtype=float)
            k_dims = np.linalg.matrix_rank(A)
            n_pi = n - k_dims
            st.info(f"**n = {n}** variable,  **k = {k_dims}** uafhængige grunddimensioner  →  **{n_pi} Pi-gruppe(r)**")

            if n_pi <= 0:
                st.warning("Ingen dimensionsløse grupper (alle variable er dimensionelt uafhængige).")
            else:
                U, s, Vt = np.linalg.svd(A.T)
                tol = 1e-9
                nullspace = Vt[np.abs(s) < tol if len(s) >= Vt.shape[0] else np.ones(Vt.shape[0], dtype=bool)]
                if nullspace.shape[0] == 0:
                    nullspace = Vt[k_dims:]

                pi_idx = 1
                for vec in nullspace:
                    if pi_idx > n_pi:
                        break
                    parts = []
                    for j, vn in enumerate(vars_list2):
                        exp_val = vec[j]
                        exp_r = round(exp_val * 2) / 2
                        if abs(exp_r) > 1e-6:
                            if abs(exp_r - round(exp_r)) < 0.01:
                                exp_str = str(int(round(exp_r)))
                            else:
                                exp_str = f"{exp_r:.2g}"
                            parts.append(f"{vn}^{{{exp_str}}}")
                    if parts:
                        expr = r" \cdot ".join(parts)
                        st.success(f"Π{pi_idx} = " + f"${expr}$")
                        pi_idx += 1
