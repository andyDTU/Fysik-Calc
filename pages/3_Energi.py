import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Energi & Arbejde", page_icon="🔋", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🔋", "Energi")
st.title("🔋 Energi & Arbejde")
st.markdown("Kinetisk/potentiel energi, arbejde, effekt og energibevarelse")
st.divider()

G = 9.82

_ENERGI_FORMULAS = [
    ("Kinetisk energi",       "Ek = ½·m·v²",                 "Kinetisk energi:  Ek = ½ · m · v²"),
    ("Potentiel energi",      "Ep = m·g·h",                  "Potentiel energi:  Ep = m · g · h"),
    ("Fjeder",                "F=k·x,  Ef=½k·x²",            "Fjederkraft og -energi"),
    ("Arbejde",               "W = F·s·cos(θ)",               "Arbejde:  W = F · s · cos(θ)"),
    ("Effekt",                "P = W/t = F·v",               "Effekt:  P = W / t = F · v"),
    ("Energibevarelse",       "Ek₁+Ep₁ = Ek₂+Ep₂",         "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂"),
    ("Energibev. + friktion", "ΔE = Wfriktion",              "Energibevarelse med friktion"),
    ("Virkningsgrad",         "η = P_ud / P_ind",            "Mekanisk virkningsgrad:  η = P_ud / P_ind"),
    ("Pendul – v og T",       "v=√(2gR(1−cosθ)),  T=m(3g−2gcosθ)", "Pendul – hastighed og snorkraft (energibevarelse)"),
    ("Fjeder – fald",         "mg(h+d) = ½kd²",              "Fjeder – maks. kompression ved fald"),
]
formel = formula_card_grid(_ENERGI_FORMULAS, "energi_formel")

ENERGI_TIPS = {
    "Kinetisk energi:  Ek = ½ · m · v²": "Ek afhænger af v². Dobbelt hastighed → fire gange energien.",
    "Potentiel energi:  Ep = m · g · h": "h er højde over reference­niveau (vælges frit). Ep = 0 ved h = 0.",
    "Fjederkraft og -energi": "Hookes lov: F = k·x. Energi: Ef = ½k·x². Husk: x er forlængelsen fra ligevægt.",
    "Arbejde:  W = F · s · cos(θ)": "θ er vinklen mellem kraft og bevægelsesretning. W < 0 når kraft modvirker bevægelse.",
    "Effekt:  P = W / t = F · v": "Effekt er energi pr. tid. P = F·v gælder ved konstant kraft og hastighed.",
    "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂": "Kun gyldig uden friktion og andre ikke-konservative kræfter. Ek = ½mv², Ep = mgh.",
    "Energibevarelse med friktion": "Tabsled: W_friktion = f·d = μ·N·d. Ek₁ + Ep₁ = Ek₂ + Ep₂ + |W_friktion|.",
    "Mekanisk virkningsgrad:  η = P_ud / P_ind": "η < 1 altid. η = 1 svarer til ingen energitab (ideelt system).",
    "Pendul – hastighed og snorkraft (energibevarelse)": "Pendul slippes fra hvile i vinkel θ med lodret. v_bund = √(2gR(1−cosθ)). Snorkraft i bunden: T = m(3g − 2g·cosθ). Bruges ved centripetalbevægelse.",
    "Fjeder – maks. kompression ved fald": "Legeme falder fra højde h ned på fjeder (k). Energibev: mg(h+d) = ½kd². Løs andengradsligningen: kd² − 2mgd − 2mgh = 0.",
}
show_tips(formel, ENERGI_TIPS)
st.divider()

if formel == "Kinetisk energi:  Ek = ½ · m · v²":
    st.latex(r"E_k = \frac{1}{2} m v^2")
    beregn = st.radio("Beregn:", ["Ek – kinetisk energi (J)", "m – masse (kg)", "v – hastighed (m/s)"], horizontal=True)
    st.divider()

    if beregn == "Ek – kinetisk energi (J)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        Ek = 0.5 * m * v**2
        st.success(f"**Ek = {Ek:.6g} J**")
        st.latex(rf"E_k = \frac{{1}}{{2}} \cdot {m:.6g} \cdot {v:.6g}^2 = {Ek:.6g}\ \text{{J}}")
        if st.button("📋 Gem Ek", key="gem_en_ek_Ek"):
            gem_resultat(Ek, "J", "Ek")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        Ek = c1.number_input("Ek – kinetisk energi (J)", value=100.0, min_value=0.0, format="%.6g")
        v  = c2.number_input("v – hastighed (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        m = 2 * Ek / v**2
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{2 E_k}}{{v^2}} = \frac{{2 \cdot {Ek:.6g}}}{{{v:.6g}^2}} = {m:.6g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_en_ek_m"):
            gem_resultat(m, "kg", "m")

    else:
        c1, c2 = st.columns(2)
        Ek = c1.number_input("Ek – kinetisk energi (J)", value=100.0, min_value=0.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = np.sqrt(2 * Ek / m)
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{2 E_k}}{{m}}}} = \sqrt{{\frac{{2 \cdot {Ek:.6g}}}{{{m:.6g}}}}} = {v:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_en_ek_v"):
            gem_resultat(v, "m/s", "v")

elif formel == "Potentiel energi:  Ep = m · g · h":
    st.latex(r"E_p = m \cdot g \cdot h")
    beregn = st.radio("Beregn:", ["Ep – potentiel energi (J)", "m – masse (kg)", "h – højde (m)"], horizontal=True)
    st.divider()
    g_val = st.number_input("g (m/s²)", value=G, format="%.6g")

    if beregn == "Ep – potentiel energi (J)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=5.0, min_value=1e-12, format="%.6g")
        h = c2.number_input("h – højde (m)", value=10.0, format="%.6g")
        Ep = m * g_val * h
        st.success(f"**Ep = {Ep:.6g} J**")
        st.latex(rf"E_p = {m:.6g} \cdot {g_val:.6g} \cdot {h:.6g} = {Ep:.6g}\ \text{{J}}")
        if st.button("📋 Gem Ep", key="gem_en_ep_Ep"):
            gem_resultat(Ep, "J", "Ep")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        Ep = c1.number_input("Ep (J)", value=490.0, format="%.6g")
        h  = c2.number_input("h – højde (m)", value=10.0, min_value=1e-12, format="%.6g")
        m = Ep / (g_val * h)
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{E_p}}{{g h}} = {m:.6g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_en_ep_m"):
            gem_resultat(m, "kg", "m")

    else:
        c1, c2 = st.columns(2)
        Ep = c1.number_input("Ep (J)", value=490.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=5.0, min_value=1e-12, format="%.6g")
        h = Ep / (m * g_val)
        st.success(f"**h = {h:.6g} m**")
        st.latex(rf"h = \frac{{E_p}}{{mg}} = {h:.6g}\ \text{{m}}")
        if st.button("📋 Gem h", key="gem_en_ep_h"):
            gem_resultat(h, "m", "h")

elif formel == "Fjederkraft og -energi":
    st.latex(r"F = k \cdot x \qquad E_{fj} = \frac{1}{2} k x^2")
    beregn = st.radio("Beregn:", ["F – fjederkraft (N)", "k – fjederkonstant (N/m)", "x – forlængelse (m)", "E – fjederenergi (J)"], horizontal=True)
    st.divider()

    if beregn == "F – fjederkraft (N)":
        c1, c2 = st.columns(2)
        k = c1.number_input("k – fjederkonstant (N/m)", value=200.0, min_value=1e-12, format="%.6g")
        x = c2.number_input("x – forlængelse (m)", value=0.1, format="%.6g")
        F = k * x
        E = 0.5 * k * x**2
        st.success(f"**F = {F:.6g} N**   (Efj = {E:.6g} J)")
        st.latex(rf"F = k \cdot x = {k:.6g} \cdot {x:.6g} = {F:.6g}\ \text{{N}}")

    elif beregn == "k – fjederkonstant (N/m)":
        c1, c2 = st.columns(2)
        F = c1.number_input("F – fjederkraft (N)", value=20.0, format="%.6g")
        x = c2.number_input("x – forlængelse (m)", value=0.1, min_value=1e-12, format="%.6g")
        k = F / x
        st.success(f"**k = {k:.6g} N/m**")
        st.latex(rf"k = \frac{{F}}{{x}} = \frac{{{F:.6g}}}{{{x:.6g}}} = {k:.6g}\ \text{{N/m}}")

    elif beregn == "x – forlængelse (m)":
        c1, c2 = st.columns(2)
        F = c1.number_input("F – fjederkraft (N)", value=20.0, format="%.6g")
        k = c2.number_input("k – fjederkonstant (N/m)", value=200.0, min_value=1e-12, format="%.6g")
        x = F / k
        E = 0.5 * k * x**2
        st.success(f"**x = {x:.6g} m**   (Efj = {E:.6g} J)")
        st.latex(rf"x = \frac{{F}}{{k}} = {x:.6g}\ \text{{m}}")

    else:
        c1, c2 = st.columns(2)
        k = c1.number_input("k – fjederkonstant (N/m)", value=200.0, min_value=1e-12, format="%.6g")
        x = c2.number_input("x – forlængelse (m)", value=0.1, format="%.6g")
        E = 0.5 * k * x**2
        F = k * x
        st.success(f"**E = {E:.6g} J**   (F = {F:.6g} N)")
        st.latex(rf"E_{{fj}} = \frac{{1}}{{2}} k x^2 = \frac{{1}}{{2}} \cdot {k:.6g} \cdot {x:.6g}^2 = {E:.6g}\ \text{{J}}")

elif formel == "Arbejde:  W = F · s · cos(θ)":
    st.latex(r"W = F \cdot s \cdot \cos\theta")
    beregn = st.radio("Beregn:", ["W – arbejde (J)", "F – kraft (N)", "s – strækning (m)"], horizontal=True)
    st.divider()

    if beregn == "W – arbejde (J)":
        c1, c2, c3 = st.columns(3)
        F     = c1.number_input("F – kraft (N)", value=50.0, format="%.6g")
        s     = c2.number_input("s – strækning (m)", value=10.0, format="%.6g")
        theta = c3.number_input("θ – vinkel mellem F og s (grader)", value=0.0, min_value=0.0, max_value=180.0, format="%.6g")
        W = F * s * np.cos(np.radians(theta))
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = {F:.6g} \cdot {s:.6g} \cdot \cos({theta:.4g}°) = {W:.6g}\ \text{{J}}")

    elif beregn == "F – kraft (N)":
        c1, c2, c3 = st.columns(3)
        W     = c1.number_input("W – arbejde (J)", value=500.0, format="%.6g")
        s     = c2.number_input("s – strækning (m)", value=10.0, min_value=1e-12, format="%.6g")
        theta = c3.number_input("θ (grader)", value=0.0, min_value=0.0, max_value=89.9, format="%.6g")
        cos_t = np.cos(np.radians(theta))
        F = W / (s * cos_t)
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = \frac{{W}}{{s \cos\theta}} = {F:.6g}\ \text{{N}}")

    else:
        c1, c2, c3 = st.columns(3)
        W     = c1.number_input("W – arbejde (J)", value=500.0, format="%.6g")
        F     = c2.number_input("F – kraft (N)", value=50.0, min_value=1e-12, format="%.6g")
        theta = c3.number_input("θ (grader)", value=0.0, min_value=0.0, max_value=89.9, format="%.6g")
        s = W / (F * np.cos(np.radians(theta)))
        st.success(f"**s = {s:.6g} m**")
        st.latex(rf"s = \frac{{W}}{{F \cos\theta}} = {s:.6g}\ \text{{m}}")

elif formel == "Effekt:  P = W / t = F · v":
    st.latex(r"P = \frac{W}{t} = F \cdot v")
    beregn = st.radio("Beregn:", ["P – effekt (W)", "W – arbejde (J)", "t – tid (s)", "F – kraft (N)", "v – hastighed (m/s)"], horizontal=True)
    st.divider()

    metode = st.radio("Via:", ["W og t", "F og v"], horizontal=True)

    if beregn == "P – effekt (W)":
        if metode == "W og t":
            c1, c2 = st.columns(2)
            W = c1.number_input("W – arbejde (J)", value=1000.0, format="%.6g")
            t = c2.number_input("t – tid (s)", value=10.0, min_value=1e-12, format="%.6g")
            P = W / t
            st.success(f"**P = {P:.6g} W**")
            st.latex(rf"P = \frac{{W}}{{t}} = \frac{{{W:.6g}}}{{{t:.6g}}} = {P:.6g}\ \text{{W}}")
        else:
            c1, c2 = st.columns(2)
            F = c1.number_input("F – kraft (N)", value=100.0, format="%.6g")
            v = c2.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
            P = F * v
            st.success(f"**P = {P:.6g} W**")
            st.latex(rf"P = F \cdot v = {F:.6g} \cdot {v:.6g} = {P:.6g}\ \text{{W}}")

    elif beregn == "W – arbejde (J)":
        c1, c2 = st.columns(2)
        P = c1.number_input("P – effekt (W)", value=100.0, format="%.6g")
        t = c2.number_input("t – tid (s)", value=10.0, min_value=1e-12, format="%.6g")
        W = P * t
        st.success(f"**W = {W:.6g} J**")
        st.latex(rf"W = P \cdot t = {P:.6g} \cdot {t:.6g} = {W:.6g}\ \text{{J}}")

    elif beregn == "t – tid (s)":
        c1, c2 = st.columns(2)
        W = c1.number_input("W – arbejde (J)", value=1000.0, format="%.6g")
        P = c2.number_input("P – effekt (W)", value=100.0, min_value=1e-12, format="%.6g")
        t = W / P
        st.success(f"**t = {t:.6g} s**")
        st.latex(rf"t = \frac{{W}}{{P}} = \frac{{{W:.6g}}}{{{P:.6g}}} = {t:.6g}\ \text{{s}}")

    elif beregn == "F – kraft (N)":
        c1, c2 = st.columns(2)
        P = c1.number_input("P – effekt (W)", value=1000.0, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        F = P / v
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = \frac{{P}}{{v}} = {F:.6g}\ \text{{N}}")

    else:
        c1, c2 = st.columns(2)
        P = c1.number_input("P – effekt (W)", value=1000.0, format="%.6g")
        F = c2.number_input("F – kraft (N)", value=100.0, min_value=1e-12, format="%.6g")
        v = P / F
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \frac{{P}}{{F}} = {v:.6g}\ \text{{m/s}}")

elif formel == "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂":
    st.latex(r"\tfrac{1}{2}(1+c_I)mv_1^2 + mgh_1 = \tfrac{1}{2}(1+c_I)mv_2^2 + mgh_2")
    st.markdown("Find den ukendte hastighed eller højde i et friktionsfrit system.")

    rot = st.checkbox("Inkluder rotationsenergi (rullende legeme)")
    if rot:
        legeme_map = {"Massiv kugle (c=2/5)": 2/5, "Massiv cylinder/skive (c=1/2)": 1/2,
                      "Tynd ring (c=1)": 1.0, "Hul kugle (c=2/3)": 2/3}
        leg = st.selectbox("Legemets form:", list(legeme_map.keys()))
        c_I = legeme_map[leg]
        st.info(f"c_I = {c_I:.4g}  →  effektiv masse = (1 + {c_I:.4g})·m")
    else:
        c_I = 0.0
    st.divider()

    beregn = st.radio("Beregn:", ["v₂ – sluthastighed (m/s)", "v₁ – starthastighed (m/s)", "h₂ – sluthøjde (m)", "h₁ – starthøjde (m)"], horizontal=True)
    st.divider()

    if beregn == "v₂ – sluthastighed (m/s)":
        c1, c2, c3 = st.columns(3)
        v1 = c1.number_input("v₁ – starthastighed (m/s)", value=0.0, format="%.6g")
        h1 = c2.number_input("h₁ – starthøjde (m)", value=10.0, format="%.6g")
        h2 = c3.number_input("h₂ – sluthøjde (m)", value=0.0, format="%.6g")
        val = v1**2 + 2 * G * (h1 - h2) / (1 + c_I)
        if val < 0:
            st.error("Ingen reel løsning – energien rækker ikke til sluthøjden.")
        else:
            v2 = np.sqrt(val)
            st.success(f"**v₂ = {v2:.6g} m/s**")
            st.latex(rf"v_2 = \sqrt{{\frac{{v_1^2 + 2g(h_1 - h_2)}}{{1+c_I}}}} = {v2:.6g}\ \text{{m/s}}")

    elif beregn == "v₁ – starthastighed (m/s)":
        c1, c2, c3 = st.columns(3)
        v2 = c1.number_input("v₂ – sluthastighed (m/s)", value=10.0, format="%.6g")
        h1 = c2.number_input("h₁ – starthøjde (m)", value=10.0, format="%.6g")
        h2 = c3.number_input("h₂ – sluthøjde (m)", value=0.0, format="%.6g")
        val = v2**2 - 2 * G * (h1 - h2) / (1 + c_I)
        if val < 0:
            st.error("Ingen reel løsning.")
        else:
            v1 = np.sqrt(val)
            st.success(f"**v₁ = {v1:.6g} m/s**")

    elif beregn == "h₂ – sluthøjde (m)":
        c1, c2, c3 = st.columns(3)
        v1 = c1.number_input("v₁ (m/s)", value=0.0, format="%.6g")
        h1 = c2.number_input("h₁ (m)", value=10.0, format="%.6g")
        v2 = c3.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        h2 = h1 + (1 + c_I) * (v1**2 - v2**2) / (2 * G)
        st.success(f"**h₂ = {h2:.6g} m**")
        st.latex(rf"h_2 = h_1 + \frac{{(1+c_I)(v_1^2 - v_2^2)}}{{2g}} = {h2:.6g}\ \text{{m}}")

    else:
        c1, c2, c3 = st.columns(3)
        v1 = c1.number_input("v₁ (m/s)", value=0.0, format="%.6g")
        h2 = c2.number_input("h₂ (m)", value=0.0, format="%.6g")
        v2 = c3.number_input("v₂ (m/s)", value=10.0, format="%.6g")
        h1 = h2 + (1 + c_I) * (v2**2 - v1**2) / (2 * G)
        st.success(f"**h₁ = {h1:.6g} m**")
        st.latex(rf"h_1 = h_2 + \frac{{(1+c_I)(v_2^2 - v_1^2)}}{{2g}} = {h1:.6g}\ \text{{m}}")

elif formel == "Energibevarelse med friktion":
    st.latex(r"\tfrac{1}{2}mv_1^2 + mgh_1 = \tfrac{1}{2}mv_2^2 + mgh_2 + W_f")
    st.latex(r"W_f = \mu\,m\,g\cos\theta \cdot s \quad \text{(friktion langs skråning)}")
    st.markdown("Find hastighed eller friktion inkl. energitab til friktion.")
    st.divider()

    beregn = st.radio("Beregn:", ["v₂ – sluthastighed (m/s)", "μ – friktionskoefficient", "s – strækning (m)"], horizontal=True)
    st.divider()

    if beregn == "v₂ – sluthastighed (m/s)":
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        m  = c1.number_input("m (kg)", value=5.0, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=0.0, format="%.6g")
        h1 = c3.number_input("h₁ (m)", value=10.0, format="%.6g")
        h2 = c4.number_input("h₂ (m)", value=0.0, format="%.6g")
        mu_f = c5.number_input("μ", value=0.2, min_value=0.0, format="%.6g")
        theta_f = c6.number_input("θ (°, hældning)", value=30.0, min_value=0.0, max_value=89.9, format="%.6g")
        s_dist = st.number_input("s – strækning langs planen (m)", value=20.0, min_value=0.0, format="%.6g")
        Wf = mu_f * m * G * np.cos(np.radians(theta_f)) * s_dist
        val = v1**2 + 2*G*(h1-h2) - 2*Wf/m
        if val < 0:
            st.error(f"Friktionswork ({Wf:.4g} J) overstiger tilgængelig energi – legemet når ikke frem.")
        else:
            v2 = np.sqrt(val)
            st.success(f"**v₂ = {v2:.4g} m/s**   (W_f = {Wf:.4g} J tab til friktion)")
            st.latex(rf"v_2 = \sqrt{{v_1^2 + 2g(h_1-h_2) - 2W_f/m}} = {v2:.4g}\ \text{{m/s}}")

    elif beregn == "μ – friktionskoefficient":
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        m  = c1.number_input("m (kg)", value=5.0, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=10.0, format="%.6g")
        h1 = c3.number_input("h₁ (m)", value=0.0, format="%.6g")
        v2 = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        h2 = c5.number_input("h₂ (m)", value=0.0, format="%.6g")
        theta_f = c6.number_input("θ (°)", value=0.0, min_value=0.0, max_value=89.9, format="%.6g")
        s_dist = st.number_input("s – strækning (m)", value=10.0, min_value=1e-12, format="%.6g")
        Wf = 0.5*m*(v1**2 - v2**2) + m*G*(h1-h2)
        N = m * G * np.cos(np.radians(theta_f))
        if N * s_dist < 1e-12:
            st.error("Kan ikke beregne μ – normalkraft eller strækning er nul.")
        else:
            mu_calc = Wf / (N * s_dist)
            st.success(f"**μ = {mu_calc:.4g}**   (W_f = {Wf:.4g} J)")
            st.latex(rf"\mu = \frac{{W_f}}{{N\cdot s}} = \frac{{{Wf:.4g}}}{{{N:.4g} \cdot {s_dist:.4g}}} = {mu_calc:.4g}")

    else:
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        m  = c1.number_input("m (kg)", value=5.0, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=10.0, format="%.6g")
        h1 = c3.number_input("h₁ (m)", value=0.0, format="%.6g")
        v2 = c4.number_input("v₂ (m/s)", value=0.0, format="%.6g")
        h2 = c5.number_input("h₂ (m)", value=0.0, format="%.6g")
        mu_f = c6.number_input("μ", value=0.3, min_value=0.0, format="%.6g")
        theta_f = st.number_input("θ (°)", value=0.0, min_value=0.0, max_value=89.9, format="%.6g")
        Wf = 0.5*m*(v1**2 - v2**2) + m*G*(h1-h2)
        N = m * G * np.cos(np.radians(theta_f))
        if abs(mu_f * N) < 1e-12:
            st.error("μ=0 – kan ikke beregne s.")
        else:
            s_calc = Wf / (mu_f * N)
            st.success(f"**s = {s_calc:.4g} m**   (W_f = {Wf:.4g} J)")
            st.latex(rf"s = \frac{{W_f}}{{\mu N}} = \frac{{{Wf:.4g}}}{{{mu_f:.4g} \cdot {N:.4g}}} = {s_calc:.4g}\ \text{{m}}")

elif formel == "Mekanisk virkningsgrad:  η = P_ud / P_ind":
    st.latex(r"\eta = \frac{P_{ud}}{P_{ind}} = \frac{W_{ud}}{W_{ind}}")
    beregn = st.radio("Beregn:", ["η – virkningsgrad", "P_ud (W)", "P_ind (W)"], horizontal=True)
    st.divider()

    if beregn == "η – virkningsgrad":
        c1, c2 = st.columns(2)
        P_ud  = c1.number_input("P_ud – nytteeffekt (W)", value=800.0, format="%.6g")
        P_ind = c2.number_input("P_ind – tilført effekt (W)", value=1000.0, min_value=1e-12, format="%.6g")
        eta = P_ud / P_ind
        st.success(f"**η = {eta:.4f}  =  {eta*100:.2f}%**")
        st.latex(rf"\eta = \frac{{{P_ud:.6g}}}{{{P_ind:.6g}}} = {eta:.4f}")

    elif beregn == "P_ud (W)":
        c1, c2 = st.columns(2)
        eta   = c1.number_input("η – virkningsgrad (0–1)", value=0.8, min_value=0.0, max_value=1.0, format="%.6g")
        P_ind = c2.number_input("P_ind – tilført effekt (W)", value=1000.0, format="%.6g")
        P_ud = eta * P_ind
        st.success(f"**P_ud = {P_ud:.6g} W**")
        st.latex(rf"P_{{ud}} = \eta \cdot P_{{ind}} = {eta:.6g} \cdot {P_ind:.6g} = {P_ud:.6g}\ \text{{W}}")

    else:
        c1, c2 = st.columns(2)
        eta  = c1.number_input("η – virkningsgrad (0–1)", value=0.8, min_value=0.001, max_value=1.0, format="%.6g")
        P_ud = c2.number_input("P_ud – nytteeffekt (W)", value=800.0, format="%.6g")
        P_ind = P_ud / eta
        st.success(f"**P_ind = {P_ind:.6g} W**")
        st.latex(rf"P_{{ind}} = \frac{{P_{{ud}}}}{{\eta}} = \frac{{{P_ud:.6g}}}{{{eta:.6g}}} = {P_ind:.6g}\ \text{{W}}")

elif formel == "Pendul – hastighed og snorkraft (energibevarelse)":
    st.latex(r"v = \sqrt{2gR(1 - \cos\theta)} \qquad T = m(3g - 2g\cos\theta)")
    st.markdown("Pendul slippes fra hvile i vinkel **θ** fra lodret. Find hastighed og snorkraft når snoren er lodret (bunden).")
    st.divider()

    beregn_pend = st.radio("Beregn:", ["v og T i bunden (givet θ)", "θ – udgangsvinkel (givet v i bunden)"], horizontal=True)
    st.divider()

    c1_p, c2_p, c3_p = st.columns(3)
    m_pend = c1_p.number_input("m – masse (kg)", value=0.5, min_value=1e-12, format="%.6g", key="pend_m")
    R_pend = c2_p.number_input("R – snorens længde (m)", value=1.0, min_value=1e-12, format="%.6g", key="pend_R")
    g_pend = c3_p.number_input("g (m/s²)", value=G, format="%.6g", key="pend_g")

    if beregn_pend == "v og T i bunden (givet θ)":
        theta_pend = st.number_input("θ – udgangsvinkel fra lodret (°)", value=45.0, min_value=0.0, max_value=179.9, format="%.6g", key="pend_th")
        th_r = np.radians(theta_pend)
        v_pend = np.sqrt(2 * g_pend * R_pend * (1 - np.cos(th_r)))
        T_pend = m_pend * (3 * g_pend - 2 * g_pend * np.cos(th_r))

        col1, col2 = st.columns(2)
        col1.success(f"**v = {v_pend:.6g} m/s**")
        col2.success(f"**T = {T_pend:.6g} N**")
        st.latex(rf"v = \sqrt{{2gR(1-\cos\theta)}} = \sqrt{{2 \cdot {g_pend:.6g} \cdot {R_pend:.6g} \cdot (1 - \cos {theta_pend:.4g}°)}} = {v_pend:.6g}\ \text{{m/s}}")
        st.latex(rf"T = m(3g - 2g\cos\theta) = {m_pend:.6g}(3 \cdot {g_pend:.6g} - 2 \cdot {g_pend:.6g} \cdot \cos {theta_pend:.4g}°) = {T_pend:.6g}\ \text{{N}}")

        with st.expander("Afledning"):
            st.markdown("""
**Energibevarelse** (hvile ved θ → bevægelse ved bunden):
- Ep-tab: ΔEp = mgR(1 − cosθ)
- Ek-gevinst: ½mv²
- v = √(2gR(1−cosθ))

**Centripetalbetingelse** i bunden (nedad = positiv):
- T − mg = mv²/R
- T = mg + mv²/R = mg + 2mg(1−cosθ) = m·g(3 − 2cosθ)
""")

        if abs(theta_pend - 90.0) < 0.5:
            st.info(f"θ = 90°: v = √(2gR) = {np.sqrt(2*g_pend*R_pend):.4g} m/s, T = 3mg = {3*m_pend*g_pend:.4g} N")

    else:
        v_given = st.number_input("v – hastighed i bunden (m/s)", value=3.13, min_value=0.0, format="%.6g", key="pend_vg")
        val_cos = 1 - v_given**2 / (2 * g_pend * R_pend)
        if val_cos < -1 or val_cos > 1:
            st.error("Hastigheden er for stor – snoren ville ikke holdes stram hele vejen.")
        else:
            theta_found = np.degrees(np.arccos(val_cos))
            T_found = m_pend * (3 * g_pend - 2 * g_pend * val_cos)
            st.success(f"**θ = {theta_found:.4g}°**")
            st.info(f"Snorkraft i bunden: T = {T_found:.4g} N")
            st.latex(rf"\theta = \arccos\!\left(1 - \frac{{v^2}}{{2gR}}\right) = \arccos\!\left(1 - \frac{{{v_given:.6g}^2}}{{2 \cdot {g_pend:.6g} \cdot {R_pend:.6g}}}\right) = {theta_found:.4g}°")

elif formel == "Fjeder – maks. kompression ved fald":
    st.latex(r"mg(h + d) = \frac{1}{2}k d^2")
    st.markdown("Legeme (masse **m**) falder fra højde **h** over fjederens øverste ende og komprimerer den en afstand **d**. Løses ved andengradsligning: **kd² − 2mgd − 2mgh = 0**")
    st.divider()

    beregn_fj = st.radio("Beregn:", ["d – maks. kompression (m)", "h – faldhøjde (m)", "k – fjederkonstant (N/m)"], horizontal=True)
    st.divider()

    if beregn_fj == "d – maks. kompression (m)":
        c1, c2, c3 = st.columns(3)
        m_fj = c1.number_input("m – masse (kg)", value=1.2, min_value=1e-12, format="%.6g", key="fj_m")
        h_fj = c2.number_input("h – faldhøjde over fjeder (m)", value=0.80, min_value=0.0, format="%.6g", key="fj_h")
        k_fj = c3.number_input("k – fjederkonstant (N/m)", value=1600.0, min_value=1e-12, format="%.6g", key="fj_k")
        g_fj = st.number_input("g (m/s²)", value=G, format="%.6g", key="fj_g")

        # kd² - 2mgd - 2mgh = 0
        a_q = k_fj
        b_q = -2 * m_fj * g_fj
        c_q = -2 * m_fj * g_fj * h_fj
        disc = b_q**2 - 4 * a_q * c_q
        d_fj = (-b_q + np.sqrt(disc)) / (2 * a_q)

        st.success(f"**d = {d_fj:.6g} m**")
        st.latex(rf"d = \frac{{mg + \sqrt{{m^2g^2 + 2kmgh}}}}{{k}} = \frac{{{m_fj:.6g}\cdot{g_fj:.6g} + \sqrt{{({m_fj:.6g}\cdot{g_fj:.6g})^2 + 2\cdot{k_fj:.6g}\cdot{m_fj:.6g}\cdot{g_fj:.6g}\cdot{h_fj:.6g}}}}}{{{k_fj:.6g}}} = {d_fj:.6g}\ \text{{m}}")

        with st.expander("Vis udregning"):
            st.markdown(f"**a** = k = {a_q:.6g}, **b** = −2mg = {b_q:.6g}, **c** = −2mgh = {c_q:.6g}")
            st.markdown(f"Diskriminant = b²−4ac = {disc:.6g}")
            st.markdown(f"d = (−b + √disc) / 2a = {d_fj:.6g} m")
            Ef = 0.5 * k_fj * d_fj**2
            Ep_lost = m_fj * g_fj * (h_fj + d_fj)
            st.metric("Fjederenergi Ef = ½kd²", f"{Ef:.4g} J")
            st.metric("Tyngdekraftpotentiale frigivet", f"{Ep_lost:.4g} J")

        if abs(m_fj - 1.2) < 0.01 and abs(h_fj - 0.80) < 0.01 and abs(k_fj - 1600.0) < 1.0:
            st.success("📋 Svarer til opgave fra kap. 8 (m=1.2 kg, h=0.80 m, k=1600 N/m).")

    elif beregn_fj == "h – faldhøjde (m)":
        c1, c2, c3 = st.columns(3)
        m_fj = c1.number_input("m – masse (kg)", value=1.2, min_value=1e-12, format="%.6g", key="fj_m2")
        d_fj = c2.number_input("d – kompression (m)", value=0.1, min_value=1e-12, format="%.6g", key="fj_d2")
        k_fj = c3.number_input("k – fjederkonstant (N/m)", value=1600.0, min_value=1e-12, format="%.6g", key="fj_k2")
        g_fj = st.number_input("g (m/s²)", value=G, format="%.6g", key="fj_g2")

        h_fj = (0.5 * k_fj * d_fj**2 - m_fj * g_fj * d_fj) / (m_fj * g_fj)
        if h_fj < 0:
            st.warning(f"h = {h_fj:.4g} m (negativ → legemet rammer fjeder fra under fjedertoppen; muligt men usædvanligt)")
        else:
            st.success(f"**h = {h_fj:.6g} m**")
        st.latex(rf"h = \frac{{\frac{{1}}{{2}}kd^2}}{{mg}} - d = \frac{{{0.5*k_fj*d_fj**2:.6g}}}{{{m_fj*g_fj:.6g}}} - {d_fj:.6g} = {h_fj:.6g}\ \text{{m}}")

    else:
        c1, c2, c3 = st.columns(3)
        m_fj = c1.number_input("m – masse (kg)", value=1.2, min_value=1e-12, format="%.6g", key="fj_m3")
        h_fj = c2.number_input("h – faldhøjde (m)", value=0.80, min_value=0.0, format="%.6g", key="fj_h3")
        d_fj = c3.number_input("d – kompression (m)", value=0.1, min_value=1e-12, format="%.6g", key="fj_d3")
        g_fj = st.number_input("g (m/s²)", value=G, format="%.6g", key="fj_g3")

        k_fj = 2 * m_fj * g_fj * (h_fj + d_fj) / d_fj**2
        st.success(f"**k = {k_fj:.6g} N/m**")
        st.latex(rf"k = \frac{{2mg(h+d)}}{{d^2}} = \frac{{2 \cdot {m_fj:.6g} \cdot {g_fj:.6g} \cdot ({h_fj:.6g}+{d_fj:.6g})}}{{{d_fj:.6g}^2}} = {k_fj:.6g}\ \text{{N/m}}")
