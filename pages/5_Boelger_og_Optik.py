import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Bølger & Optik", page_icon="🌊", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🌊", "Bølger & Optik")
st.title("🌊 Bølger & Optik")
st.markdown("Bølgehastighed, brydning, linser, Doppler og dobbeltspalte")
st.divider()

_BOLGE_FORMULAS = [
    ("Bølgehastighed",      "v = f · λ",                      "Bølgehastighed:  v = f · λ"),
    ("Snells lov",          "n₁sinθ₁ = n₂sinθ₂",             "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)"),
    ("Totalrefleksion",     "sinθc = n₂/n₁",                  "Totalrefleksion og kritisk vinkel"),
    ("Linsformel",          "1/f = 1/do + 1/di",              "Linsformel:  1/f = 1/do + 1/di"),
    ("Forstørring",         "M = −di/do",                     "Forstørring:  M = -di / do"),
    ("Doppler-effekt",      "f' = f·(v±v_L)/(v∓v_S)",        "Doppler-effekt"),
    ("Dobbeltspalte (Young)","d·sinθ = n·λ",                  "Dobbeltspalte (Young):  d·sin(θ) = n·λ"),
    ("Diffraktionsgitter",  "d·sinθ = m·λ",                   "Diffraktionsgitter:  d·sin(θ) = m·λ"),
    ("Enkelt­spalte",       "a·sinθ = m·λ (mørk)",            "Enkelt­spalte diffraktion"),
    ("Tyndfilm interferens","2nt = mλ (lys)",                  "Tyndfilm interferens"),
    ("Malus' lov",          "I = I₀·cos²θ",                   "Malus' lov:  I = I₀·cos²(θ)"),
    ("Stående bølger",      "λₙ = 2L/n (streng)",             "Stående bølger – streng/rør"),
    ("Brydningsindeks",     "n = c/v",                         "Lysets brydningsindeks:  n = c / v"),
]
formel = formula_card_grid(_BOLGE_FORMULAS, "bolge_formel")

BOLGE_TIPS = {
    "Bølgehastighed:  v = f · λ": "v = f·λ. For lyd i luft ≈ 343 m/s. For lys = c = 3×10⁸ m/s.",
    "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)": "n₁sin(θ₁) = n₂sin(θ₂). Større n → mindre θ (brydning mod normalen).",
    "Totalrefleksion og kritisk vinkel": "sin(θ_c) = n₂/n₁ (kræver n₁ > n₂). Bruges i optiske fibre.",
    "Linsformel:  1/f = 1/do + 1/di": "1/f = 1/do + 1/di. Konveks linse: f > 0. Konkav: f < 0. di < 0 → virtuelt billede.",
    "Doppler-effekt": "Kilde nærmer sig → frekvens øges. Kilde fjerner sig → frekvens sænkes.",
    "Dobbeltspalte (Young):  d·sin(θ) = n·λ": "Konstruktiv interferens: d·sin(θ) = nλ, n = 0,±1,±2,… Destruktiv: n + ½.",
    "Stående bølger – streng/rør": "Streng (lukket-lukket): λ_n = 2L/n. Rør (åben-åben): samme. Åben-lukket: λ_n = 4L/(2n−1).",
}
show_tips(formel, BOLGE_TIPS)
st.divider()

c_light = 2.998e8

if formel == "Bølgehastighed:  v = f · λ":
    st.latex(r"v = f \cdot \lambda")
    beregn = st.radio("Beregn:", ["v – bølgehastighed (m/s)", "f – frekvens (Hz)", "λ – bølgelængde (m)"], horizontal=True)
    st.divider()

    if beregn == "v – bølgehastighed (m/s)":
        c1, c2 = st.columns(2)
        f   = c1.number_input("f – frekvens (Hz)", value=440.0, format="%.6g")
        lam = c2.number_input("λ – bølgelængde (m)", value=0.775, format="%.6g")
        v = f * lam
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = f \cdot \lambda = {f:.6g} \cdot {lam:.6g} = {v:.6g}\ \text{{m/s}}")

    elif beregn == "f – frekvens (Hz)":
        c1, c2 = st.columns(2)
        v   = c1.number_input("v – bølgehastighed (m/s)", value=340.0, format="%.6g")
        lam = c2.number_input("λ – bølgelængde (m)", value=0.775, min_value=1e-12, format="%.6g")
        f = v / lam
        T = 1 / f
        st.success(f"**f = {f:.6g} Hz**   (T = {T:.6g} s)")
        st.latex(rf"f = \frac{{v}}{{\lambda}} = \frac{{{v:.6g}}}{{{lam:.6g}}} = {f:.6g}\ \text{{Hz}}")

    else:
        c1, c2 = st.columns(2)
        v = c1.number_input("v – bølgehastighed (m/s)", value=340.0, format="%.6g")
        f = c2.number_input("f – frekvens (Hz)", value=440.0, min_value=1e-12, format="%.6g")
        lam = v / f
        st.success(f"**λ = {lam:.6g} m**")
        st.latex(rf"\lambda = \frac{{v}}{{f}} = \frac{{{v:.6g}}}{{{f:.6g}}} = {lam:.6g}\ \text{{m}}")

elif formel == "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)":
    st.latex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2")
    beregn = st.radio("Beregn:", ["θ₂ – brydningsvinkel", "θ₁ – indfaldsvinkel", "n₂ – brydningsindeks"], horizontal=True)
    st.divider()

    if beregn == "θ₂ – brydningsvinkel":
        c1, c2, c3 = st.columns(3)
        n1 = c1.number_input("n₁", value=1.0, min_value=1e-12, format="%.6g")
        theta1 = c2.number_input("θ₁ – indfaldsvinkel (grader)", value=45.0, min_value=0.0, max_value=89.9, format="%.6g")
        n2 = c3.number_input("n₂", value=1.5, min_value=1e-12, format="%.6g")
        sin2 = n1 * np.sin(np.radians(theta1)) / n2
        if abs(sin2) > 1:
            st.warning(f"Totalrefleksion! sin(θ₂) = {sin2:.4f} > 1, ingen brydning mulig.")
        else:
            theta2 = np.degrees(np.arcsin(sin2))
            st.success(f"**θ₂ = {theta2:.4g}°**")
            st.latex(rf"\theta_2 = \arcsin\!\left(\frac{{n_1 \sin\theta_1}}{{n_2}}\right) = \arcsin\!\left(\frac{{{n1:.6g} \cdot \sin({theta1:.4g}°)}}{{{n2:.6g}}}\right) = {theta2:.4g}°")

    elif beregn == "θ₁ – indfaldsvinkel":
        c1, c2, c3 = st.columns(3)
        n1 = c1.number_input("n₁", value=1.0, min_value=1e-12, format="%.6g")
        n2 = c2.number_input("n₂", value=1.5, min_value=1e-12, format="%.6g")
        theta2 = c3.number_input("θ₂ – brydningsvinkel (grader)", value=28.1, min_value=0.0, max_value=89.9, format="%.6g")
        sin1 = n2 * np.sin(np.radians(theta2)) / n1
        if abs(sin1) > 1:
            st.error("Ingen reel løsning.")
        else:
            theta1 = np.degrees(np.arcsin(sin1))
            st.success(f"**θ₁ = {theta1:.4g}°**")

    else:
        c1, c2, c3 = st.columns(3)
        n1 = c1.number_input("n₁", value=1.0, min_value=1e-12, format="%.6g")
        theta1 = c2.number_input("θ₁ (grader)", value=45.0, min_value=0.0, max_value=89.9, format="%.6g")
        theta2 = c3.number_input("θ₂ (grader)", value=28.1, min_value=0.0, max_value=89.9, format="%.6g")
        if np.sin(np.radians(theta2)) < 1e-12:
            st.error("θ₂ = 0 giver ikke mening.")
        else:
            n2 = n1 * np.sin(np.radians(theta1)) / np.sin(np.radians(theta2))
            st.success(f"**n₂ = {n2:.6g}**")

elif formel == "Totalrefleksion og kritisk vinkel":
    st.latex(r"\sin\theta_c = \frac{n_2}{n_1} \quad (n_1 > n_2)")
    st.divider()
    c1, c2 = st.columns(2)
    n1 = c1.number_input("n₁ – tættere medium (fx glas)", value=1.5, min_value=1.001, format="%.6g")
    n2 = c2.number_input("n₂ – tyndere medium (fx luft)", value=1.0, min_value=0.1, format="%.6g")
    if n1 <= n2:
        st.error("Totalrefleksion kræver n₁ > n₂")
    else:
        theta_c = np.degrees(np.arcsin(n2 / n1))
        st.success(f"**Kritisk vinkel θc = {theta_c:.4g}°**")
        st.markdown("For indfaldsvinkler **større** end θc sker totalrefleksion.")
        st.latex(rf"\theta_c = \arcsin\!\left(\frac{{{n2:.6g}}}{{{n1:.6g}}}\right) = {theta_c:.4g}°")

elif formel == "Linsformel:  1/f = 1/do + 1/di":
    st.latex(r"\frac{1}{f} = \frac{1}{d_o} + \frac{1}{d_i}")
    st.info("Konvention: reelle billeder har di > 0, virtuelle di < 0. Konvekse linser: f > 0.")
    beregn = st.radio("Beregn:", ["di – billedafstand (m)", "do – genstandsafstand (m)", "f – brændvidde (m)"], horizontal=True)
    st.divider()

    if beregn == "di – billedafstand (m)":
        c1, c2 = st.columns(2)
        f  = c1.number_input("f – brændvidde (m)", value=0.2, format="%.6g")
        do = c2.number_input("do – genstandsafstand (m)", value=0.5, min_value=1e-12, format="%.6g")
        if abs(1/f - 1/do) < 1e-12:
            st.error("1/f = 1/do – ingen billedafstand.")
        else:
            di = 1 / (1/f - 1/do)
            M = -di / do
            st.success(f"**di = {di:.4g} m**   (M = {M:.4g})")
            st.latex(rf"\frac{{1}}{{d_i}} = \frac{{1}}{{f}} - \frac{{1}}{{d_o}} = \frac{{1}}{{{f:.6g}}} - \frac{{1}}{{{do:.6g}}} \Rightarrow d_i = {di:.4g}\ \text{{m}}")

    elif beregn == "do – genstandsafstand (m)":
        c1, c2 = st.columns(2)
        f  = c1.number_input("f – brændvidde (m)", value=0.2, format="%.6g")
        di = c2.number_input("di – billedafstand (m)", value=0.333, format="%.6g")
        if abs(1/f - 1/di) < 1e-12:
            st.error("Ingen løsning.")
        else:
            do = 1 / (1/f - 1/di)
            st.success(f"**do = {do:.4g} m**")

    else:
        c1, c2 = st.columns(2)
        do = c1.number_input("do – genstandsafstand (m)", value=0.5, min_value=1e-12, format="%.6g")
        di = c2.number_input("di – billedafstand (m)", value=0.333, format="%.6g")
        f = 1 / (1/do + 1/di)
        st.success(f"**f = {f:.4g} m**")
        st.latex(rf"\frac{{1}}{{f}} = \frac{{1}}{{d_o}} + \frac{{1}}{{d_i}} \Rightarrow f = {f:.4g}\ \text{{m}}")

elif formel == "Forstørring:  M = -di / do":
    st.latex(r"M = -\frac{d_i}{d_o} = \frac{h_i}{h_o}")
    c1, c2 = st.columns(2)
    di = c1.number_input("di – billedafstand (m)", value=0.333, format="%.6g")
    do = c2.number_input("do – genstandsafstand (m)", value=0.5, min_value=1e-12, format="%.6g")
    M = -di / do
    st.success(f"**M = {M:.4g}**")
    if M < 0:
        st.info("M < 0: billede er omvendt (reelt billede)")
    else:
        st.info("M > 0: billede er opret (virtuelt billede)")
    st.latex(rf"M = -\frac{{d_i}}{{d_o}} = -\frac{{{di:.6g}}}{{{do:.6g}}} = {M:.4g}")

elif formel == "Doppler-effekt":
    st.latex(r"f' = f \cdot \frac{v \pm v_{obs}}{v \mp v_{kilde}}")
    st.markdown("""
- **+v_obs**: observatør bevæger sig mod kilden
- **−v_obs**: observatør bevæger sig fra kilden
- **−v_kilde**: kilde bevæger sig mod observatøren
- **+v_kilde**: kilde bevæger sig fra observatøren
""")
    st.divider()

    c1, c2 = st.columns(2)
    f_kilde = c1.number_input("f – kildefrekvens (Hz)", value=440.0, format="%.6g")
    v_lyd   = c2.number_input("v – lydhastighed (m/s)", value=343.0, format="%.6g")

    c3, c4 = st.columns(2)
    v_obs   = c3.number_input("v_obs – observatørhastighed (m/s)", value=0.0, format="%.6g")
    v_kilde = c4.number_input("v_kilde – kildehastighed (m/s)", value=30.0, format="%.6g")

    obs_mod = st.checkbox("Observatør bevæger sig MOD kilden", value=False)
    kilde_mod = st.checkbox("Kilde bevæger sig MOD observatøren", value=True)

    v_obs_sign   = v_obs if obs_mod else -v_obs
    v_kilde_sign = v_kilde if not kilde_mod else -v_kilde

    denom = v_lyd + v_kilde_sign
    if abs(denom) < 1e-12:
        st.error("Nævner = 0 – ugyldigt scenarie.")
    else:
        f_prime = f_kilde * (v_lyd + v_obs_sign) / denom
        st.success(f"**f' = {f_prime:.4g} Hz**")
        delta = f_prime - f_kilde
        st.markdown(f"Frekvensforskydning: {delta:+.4g} Hz  ({'rød­forskydn.' if delta < 0 else 'blåforskydn.'})")

elif formel == "Dobbeltspalte (Young):  d·sin(θ) = n·λ":
    st.latex(r"d \cdot \sin\theta = n \cdot \lambda \qquad \tan\theta \approx \frac{y}{L}")
    beregn = st.radio("Beregn:", ["λ – bølgelængde (m)", "d – spalteafstand (m)", "y – fringe-afstand (m)", "L – skærmafstand (m)"], horizontal=True)
    st.divider()

    n_order = st.number_input("n – orden (heltal)", value=1, min_value=1, step=1)

    if beregn == "λ – bølgelængde (m)":
        c1, c2, c3 = st.columns(3)
        d = c1.number_input("d – spalteafstand (m)", value=1e-4, format="%.6g")
        y = c2.number_input("y – afstand til n-te maksimum (m)", value=0.005, format="%.6g")
        L = c3.number_input("L – skærmafstand (m)", value=1.0, min_value=1e-12, format="%.6g")
        lam = d * y / (n_order * L)
        st.success(f"**λ = {lam:.6g} m  =  {lam*1e9:.4g} nm**")
        st.latex(rf"\lambda = \frac{{d \cdot y}}{{n \cdot L}} = \frac{{{d:.6g} \cdot {y:.6g}}}{{{n_order} \cdot {L:.6g}}} = {lam:.6g}\ \text{{m}}")

    elif beregn == "d – spalteafstand (m)":
        c1, c2, c3 = st.columns(3)
        lam = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
        y   = c2.number_input("y – afstand til n-te maksimum (m)", value=0.005, format="%.6g")
        L   = c3.number_input("L – skærmafstand (m)", value=1.0, min_value=1e-12, format="%.6g")
        d = n_order * lam * L / y
        st.success(f"**d = {d:.6g} m**")

    elif beregn == "y – fringe-afstand (m)":
        c1, c2, c3 = st.columns(3)
        lam = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
        d   = c2.number_input("d – spalteafstand (m)", value=1e-4, min_value=1e-12, format="%.6g")
        L   = c3.number_input("L – skærmafstand (m)", value=1.0, format="%.6g")
        y = n_order * lam * L / d
        st.success(f"**y = {y:.6g} m**")
        st.latex(rf"y = \frac{{n \lambda L}}{{d}} = \frac{{{n_order} \cdot {lam:.6g} \cdot {L:.6g}}}{{{d:.6g}}} = {y:.6g}\ \text{{m}}")

    else:
        c1, c2, c3 = st.columns(3)
        lam = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
        d   = c2.number_input("d – spalteafstand (m)", value=1e-4, min_value=1e-12, format="%.6g")
        y   = c3.number_input("y – afstand til n-te maksimum (m)", value=0.005, min_value=1e-12, format="%.6g")
        L = n_order * lam * d / (d * y / (n_order * lam))
        L2 = d * y / (n_order * lam)
        st.success(f"**L = {L2:.6g} m**")

elif formel == "Diffraktionsgitter:  d·sin(θ) = m·λ":
    st.latex(r"d \cdot \sin\theta = m \cdot \lambda")
    st.markdown("**d** = gitterafstand (m) = 1/N hvor N = antal linjer pr. meter.  Skarpe maksima i modsætning til dobbeltspalte.")
    beregn = st.radio("Beregn:", ["θ – diffrakt.vinkel (°)", "λ – bølgelængde (m)", "d – gitterafstand (m)"], horizontal=True)
    st.divider()

    m_order = st.number_input("m – orden (heltal, m ≥ 1)", value=1, min_value=1, step=1)

    if beregn == "θ – diffrakt.vinkel (°)":
        c1, c2 = st.columns(2)
        lam = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
        d   = c2.number_input("d – gitterafstand (m)  [= 1/linjer·m⁻¹]", value=1/600e3, format="%.6g")
        sin_val = m_order * lam / d
        if abs(sin_val) > 1:
            st.error(f"Ingen maksimum: sin(θ) = {sin_val:.4f} > 1 (orden m={m_order} eksisterer ikke).")
        else:
            theta = np.degrees(np.arcsin(sin_val))
            st.success(f"**θ = {theta:.4g}°**  for orden m = {m_order}")
            st.latex(rf"\theta = \arcsin\!\left(\frac{{m\lambda}}{{d}}\right) = \arcsin\!\left(\frac{{{m_order}\cdot{lam:.4g}}}{{{d:.4g}}}\right) = {theta:.4g}°")
            st.caption(f"Gitter med {1/d:.4g} linjer/m → d = {d:.4g} m")

    elif beregn == "λ – bølgelængde (m)":
        c1, c2 = st.columns(2)
        d     = c1.number_input("d – gitterafstand (m)", value=1/600e3, format="%.6g")
        theta = c2.number_input("θ – diffrakt.vinkel (°)", value=19.3, min_value=0.0, max_value=89.9, format="%.6g")
        lam = d * np.sin(np.radians(theta)) / m_order
        st.success(f"**λ = {lam:.6g} m  =  {lam*1e9:.4g} nm**")
        st.latex(rf"\lambda = \frac{{d\sin\theta}}{{m}} = \frac{{{d:.4g}\cdot\sin({theta:.4g}°)}}{{{m_order}}} = {lam:.6g}\ \text{{m}}")

    else:
        c1, c2 = st.columns(2)
        lam   = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
        theta = c2.number_input("θ – diffrakt.vinkel (°)", value=19.3, min_value=0.1, max_value=89.9, format="%.6g")
        d = m_order * lam / np.sin(np.radians(theta))
        N_lines = 1 / d
        st.success(f"**d = {d:.6g} m**   ({N_lines:.4g} linjer/m)")
        st.latex(rf"d = \frac{{m\lambda}}{{\sin\theta}} = \frac{{{m_order}\cdot{lam:.4g}}}{{\sin({theta:.4g}°)}} = {d:.6g}\ \text{{m}}")

elif formel == "Tyndfilm interferens":
    st.latex(r"2nt = m\lambda \quad \text{(konstruktiv, en fasevending)}")
    st.latex(r"2nt = \left(m+\tfrac{1}{2}\right)\lambda \quad \text{(destruktiv, en fasevending)}")
    st.markdown("""
**Fase­vendinger:** lys der reflekteres fra et optisk tættere medium (n_høj) får en fasevending (½λ).

| Situation | Konstruktiv | Destruktiv |
|-----------|-------------|------------|
| Én fasevending (fx sæbefilm i luft) | 2nt = mλ | 2nt = (m+½)λ |
| Ingen el. to fasvend. | 2nt = (m+½)λ | 2nt = mλ |
""")
    st.divider()

    fasvend = st.radio("Antal fase­vendinger:", ["1 (fx sæbefilm i luft eller olie på vand)", "0 eller 2"], horizontal=True)
    beregn  = st.radio("Beregn:", ["λ – bølgelængde (m)", "t – filmtykkelse (m)", "m – orden"], horizontal=True)
    st.divider()

    if fasvend == "1 (fx sæbefilm i luft eller olie på vand)":
        konstruktiv = r"2nt = m\lambda"
        destruktiv  = r"2nt = \left(m+\tfrac{1}{2}\right)\lambda"
        konstruktiv_fn = lambda n, t, m: 2*n*t / m if m > 0 else 0
        t_konstruktiv  = lambda n, lam, m: m * lam / (2 * n)
        t_destruktiv   = lambda n, lam, m: (m + 0.5) * lam / (2 * n)
    else:
        konstruktiv = r"2nt = \left(m+\tfrac{1}{2}\right)\lambda"
        destruktiv  = r"2nt = m\lambda"
        t_konstruktiv  = lambda n, lam, m: (m + 0.5) * lam / (2 * n)
        t_destruktiv   = lambda n, lam, m: m * lam / (2 * n)

    mode = st.radio("Betingelse:", ["Konstruktiv (max)", "Destruktiv (min)"], horizontal=True)
    m_ord = st.number_input("m – orden (heltal ≥ 1)", value=1, min_value=1, step=1)

    c1, c2 = st.columns(2)
    n_film = c1.number_input("n – brydningsindeks for filmen", value=1.33, min_value=1.0, format="%.6g")

    if beregn == "λ – bølgelængde (m)":
        t = c2.number_input("t – filmtykkelse (m)", value=200e-9, min_value=1e-12, format="%.6g")
        if mode == "Konstruktiv (max)":
            lam = t_konstruktiv(n_film, 1.0, m_ord)  # dummy; solve for lam
            lam = 2 * n_film * t / m_ord if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else 2 * n_film * t / (m_ord + 0.5)
        else:
            lam = 2 * n_film * t / (m_ord + 0.5) if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else 2 * n_film * t / m_ord
        st.success(f"**λ = {lam:.6g} m  =  {lam*1e9:.4g} nm**")
        st.caption("Synligt lys: 380–700 nm")

    elif beregn == "t – filmtykkelse (m)":
        lam = c2.number_input("λ – bølgelængde i luft (m)", value=550e-9, format="%.6g")
        if mode == "Konstruktiv (max)":
            t = 2 * n_film * 1.0 / m_ord  # wrong, fix:
            t = (m_ord * lam / (2 * n_film)) if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else ((m_ord + 0.5) * lam / (2 * n_film))
        else:
            t = ((m_ord + 0.5) * lam / (2 * n_film)) if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else (m_ord * lam / (2 * n_film))
        st.success(f"**t = {t:.6g} m  =  {t*1e9:.4g} nm**")

    else:
        lam = c2.number_input("λ – bølgelængde i luft (m)", value=550e-9, format="%.6g")
        t   = st.number_input("t – filmtykkelse (m)", value=200e-9, format="%.6g")
        if mode == "Konstruktiv (max)":
            m_float = (2 * n_film * t / lam) if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else (2 * n_film * t / lam - 0.5)
        else:
            m_float = (2 * n_film * t / lam - 0.5) if fasvend == "1 (fx sæbefilm i luft eller olie på vand)" else (2 * n_film * t / lam)
        m_nearest = round(m_float)
        st.success(f"**m ≈ {m_float:.3f}** → nærmeste heltal: **m = {m_nearest}**")

elif formel == "Malus' lov:  I = I₀·cos²(θ)":
    st.latex(r"I = I_0 \cdot \cos^2\!\theta")
    st.markdown("Intensiteten af lineært polariseret lys efter en polarisator med vinkel θ til polariseringsplanet.")
    beregn = st.radio("Beregn:", ["I – transmitteret intensitet", "θ – vinkel (°)", "I₀ – indfaldsintensitet"], horizontal=True)
    st.divider()

    if beregn == "I – transmitteret intensitet":
        c1, c2 = st.columns(2)
        I0    = c1.number_input("I₀ – indfaldsintensitet (W/m²)", value=100.0, min_value=0.0, format="%.6g")
        theta = c2.number_input("θ – vinkel (grader)", value=45.0, min_value=0.0, max_value=90.0, format="%.6g")
        I = I0 * np.cos(np.radians(theta))**2
        st.success(f"**I = {I:.6g} W/m²**   ({I/I0*100:.2f}% af I₀)" if I0 > 1e-12 else f"**I = {I:.6g} W/m²**")
        st.latex(rf"I = I_0\cos^2\theta = {I0:.4g}\cdot\cos^2({theta:.4g}°) = {I:.6g}\ \text{{W/m}}^2")

    elif beregn == "θ – vinkel (°)":
        c1, c2 = st.columns(2)
        I0 = c1.number_input("I₀ – indfaldsintensitet (W/m²)", value=100.0, min_value=1e-12, format="%.6g")
        I  = c2.number_input("I – transmitteret intensitet (W/m²)", value=50.0, min_value=0.0, format="%.6g")
        if I > I0:
            st.error("I kan ikke være større end I₀.")
        else:
            theta = np.degrees(np.arccos(np.sqrt(I / I0)))
            st.success(f"**θ = {theta:.4g}°**")
            st.latex(rf"\theta = \arccos\!\sqrt{{\frac{{I}}{{I_0}}}} = \arccos\!\sqrt{{\frac{{{I:.4g}}}{{{I0:.4g}}}}} = {theta:.4g}°")

    else:
        c1, c2 = st.columns(2)
        I     = c1.number_input("I – transmitteret intensitet (W/m²)", value=50.0, min_value=0.0, format="%.6g")
        theta = c2.number_input("θ – vinkel (grader)", value=45.0, min_value=0.0, max_value=89.9, format="%.6g")
        cos2 = np.cos(np.radians(theta))**2
        if cos2 < 1e-12:
            st.error("θ = 90° giver cos²(θ) = 0 – ingen løsning.")
        else:
            I0 = I / cos2
            st.success(f"**I₀ = {I0:.6g} W/m²**")
            st.latex(rf"I_0 = \frac{{I}}{{\cos^2\theta}} = \frac{{{I:.4g}}}{{\cos^2({theta:.4g}°)}} = {I0:.6g}\ \text{{W/m}}^2")

elif formel == "Enkelt­spalte diffraktion":
    st.latex(r"a \cdot \sin\theta = n \cdot \lambda \quad \text{(minima)}")
    st.divider()
    c1, c2, c3 = st.columns(3)
    lam = c1.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
    a   = c2.number_input("a – spaltebredde (m)", value=1e-4, min_value=1e-12, format="%.6g")
    n   = c3.number_input("n – orden (minimum)", value=1, min_value=1, step=1)
    sin_theta = n * lam / a
    if sin_theta > 1:
        st.error("sin(θ) > 1 – ingen minimum af denne orden.")
    else:
        theta = np.degrees(np.arcsin(sin_theta))
        st.success(f"**θ = {theta:.4g}°  for {n}. minimum**")
        st.latex(rf"\theta = \arcsin\!\left(\frac{{n\lambda}}{{a}}\right) = \arcsin\!\left(\frac{{{n} \cdot {lam:.6g}}}{{{a:.6g}}}\right) = {theta:.4g}°")

elif formel == "Stående bølger – streng/rør":
    st.markdown("### Stående bølger")
    type_ = st.radio("Type:", ["Streng (fastspændt begge ender)", "Rør åbent i begge ender", "Rør lukket i én ende"], horizontal=True)
    st.divider()

    if type_ == "Streng (fastspændt begge ender)" or type_ == "Rør åbent i begge ender":
        st.latex(r"L = n \cdot \frac{\lambda}{2} \quad \Rightarrow \quad f_n = n \cdot \frac{v}{2L}")
        c1, c2, c3 = st.columns(3)
        v = c1.number_input("v – bølgehastighed (m/s)", value=340.0 if "Rør" in type_ else 100.0, format="%.6g")
        L = c2.number_input("L – længde (m)", value=1.0, min_value=1e-12, format="%.6g")
        n = c3.number_input("n – harmonisk orden", value=1, min_value=1, step=1)
        lam = 2 * L / n
        f = v / lam
        st.success(f"**λ = {lam:.4g} m,   f_{n} = {f:.4g} Hz**")
        st.latex(rf"f_{{{n}}} = n \cdot \frac{{v}}{{2L}} = {n} \cdot \frac{{{v:.6g}}}{{2 \cdot {L:.6g}}} = {f:.4g}\ \text{{Hz}}")

    else:
        st.latex(r"L = n \cdot \frac{\lambda}{4} \quad (n = 1, 3, 5, \ldots) \quad \Rightarrow \quad f_n = n \cdot \frac{v}{4L}")
        c1, c2, c3 = st.columns(3)
        v = c1.number_input("v – bølgehastighed (m/s)", value=340.0, format="%.6g")
        L = c2.number_input("L – rørlængde (m)", value=1.0, min_value=1e-12, format="%.6g")
        n = c3.number_input("n – ulige harmonisk orden (1,3,5...)", value=1, min_value=1, step=2)
        lam = 4 * L / n
        f = v / lam
        st.success(f"**λ = {lam:.4g} m,   f_{n} = {f:.4g} Hz**")
        st.latex(rf"f_{{{n}}} = {n} \cdot \frac{{{v:.6g}}}{{4 \cdot {L:.6g}}} = {f:.4g}\ \text{{Hz}}")

elif formel == "Lysets brydningsindeks:  n = c / v":
    st.latex(r"n = \frac{c}{v}")
    st.info(f"c = {c_light:.4g} m/s")
    beregn = st.radio("Beregn:", ["n – brydningsindeks", "v – lyshastighed i medium (m/s)"], horizontal=True)
    st.divider()

    if beregn == "n – brydningsindeks":
        v = st.number_input("v – lyshastighed i medium (m/s)", value=2e8, format="%.6g")
        n = c_light / v
        st.success(f"**n = {n:.6g}**")
        st.latex(rf"n = \frac{{c}}{{v}} = \frac{{{c_light:.4g}}}{{{v:.6g}}} = {n:.6g}")
    else:
        n = st.number_input("n – brydningsindeks", value=1.5, min_value=1.0, format="%.6g")
        v = c_light / n
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \frac{{c}}{{n}} = \frac{{{c_light:.4g}}}{{{n:.6g}}} = {v:.6g}\ \text{{m/s}}")
