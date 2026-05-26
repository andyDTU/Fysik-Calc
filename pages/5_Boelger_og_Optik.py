import streamlit as st
import numpy as np

st.set_page_config(page_title="Bølger & Optik", page_icon="🌊", layout="wide")
st.title("🌊 Bølger & Optik")
st.markdown("Bølgehastighed, brydning, linser, Doppler og dobbeltspalte")
st.divider()

formel = st.selectbox("Vælg formel", [
    "Bølgehastighed:  v = f · λ",
    "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)",
    "Totalrefleksion og kritisk vinkel",
    "Linsformel:  1/f = 1/do + 1/di",
    "Forstørring:  M = -di / do",
    "Doppler-effekt",
    "Dobbeltspalte (Young):  d·sin(θ) = n·λ",
    "Enkelt­spalte diffraktion",
    "Stående bølger – streng/rør",
    "Lysets brydningsindeks:  n = c / v",
])

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
