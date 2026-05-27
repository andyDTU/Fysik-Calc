import streamlit as st
import numpy as np
from utils import render_search_sidebar

st.set_page_config(page_title="Energi & Arbejde", page_icon="🔋", layout="wide")
render_search_sidebar()
st.title("🔋 Energi & Arbejde")
st.markdown("Kinetisk/potentiel energi, arbejde, effekt og energibevarelse")
st.divider()

G = 9.82

formel = st.selectbox("Vælg formel", [
    "Kinetisk energi:  Ek = ½ · m · v²",
    "Potentiel energi:  Ep = m · g · h",
    "Fjederkraft og -energi",
    "Arbejde:  W = F · s · cos(θ)",
    "Effekt:  P = W / t = F · v",
    "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂",
    "Energibevarelse med friktion",
    "Mekanisk virkningsgrad:  η = P_ud / P_ind",
])

_ENERGI_CONTEXT = {
    "Kinetisk energi:  Ek = ½ · m · v²": "Bruges til at beregne **bevægelsesenergien** fra masse og hastighed.",
    "Potentiel energi:  Ep = m · g · h": "Bruges til **gravitationsenergi** fra masse og højde.",
    "Fjederkraft og -energi": "Bruges til **Hookes lov** – find fjederkraft, stivhed k eller kompression/forlængelse.",
    "Arbejde:  W = F · s · cos(θ)": "Bruges til at beregne **udført arbejde** langs en strækning med en kraft i vinkel θ.",
    "Effekt:  P = W / t = F · v": "Bruges til at beregne **effekt** – via arbejde/tid ELLER kraft × hastighed.",
    "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂": "Bruges i **friktionsfrie systemer** – forbinder hastighed og højde direkte.",
    "Energibevarelse med friktion": "Bruges når systemet har **friktion** – beregn energitab eller sluthastig­hed.",
    "Mekanisk virkningsgrad:  η = P_ud / P_ind": "Bruges til at beregne **nytteeffekt** i maskiner og motorer.",
}
if formel in _ENERGI_CONTEXT:
    st.info(f"💡 **Hvornår bruger du denne?** {_ENERGI_CONTEXT[formel]}")

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

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        Ek = c1.number_input("Ek – kinetisk energi (J)", value=100.0, min_value=0.0, format="%.6g")
        v  = c2.number_input("v – hastighed (m/s)", value=10.0, min_value=1e-12, format="%.6g")
        m = 2 * Ek / v**2
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{2 E_k}}{{v^2}} = \frac{{2 \cdot {Ek:.6g}}}{{{v:.6g}^2}} = {m:.6g}\ \text{{kg}}")

    else:
        c1, c2 = st.columns(2)
        Ek = c1.number_input("Ek – kinetisk energi (J)", value=100.0, min_value=0.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = np.sqrt(2 * Ek / m)
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{2 E_k}}{{m}}}} = \sqrt{{\frac{{2 \cdot {Ek:.6g}}}{{{m:.6g}}}}} = {v:.6g}\ \text{{m/s}}")

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

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        Ep = c1.number_input("Ep (J)", value=490.0, format="%.6g")
        h  = c2.number_input("h – højde (m)", value=10.0, min_value=1e-12, format="%.6g")
        m = Ep / (g_val * h)
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{E_p}}{{g h}} = {m:.6g}\ \text{{kg}}")

    else:
        c1, c2 = st.columns(2)
        Ep = c1.number_input("Ep (J)", value=490.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=5.0, min_value=1e-12, format="%.6g")
        h = Ep / (m * g_val)
        st.success(f"**h = {h:.6g} m**")
        st.latex(rf"h = \frac{{E_p}}{{mg}} = {h:.6g}\ \text{{m}}")

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
    st.latex(r"E_{k1} + E_{p1} = E_{k2} + E_{p2}")
    st.latex(r"\frac{1}{2}mv_1^2 + mgh_1 = \frac{1}{2}mv_2^2 + mgh_2")
    st.markdown("Find den ukendte hastighed eller højde i et friktionsfrit system.")
    st.divider()

    beregn = st.radio("Beregn:", ["v₂ – sluthastighed (m/s)", "v₁ – starthastighed (m/s)", "h₂ – sluthøjde (m)", "h₁ – starthøjde (m)"], horizontal=True)
    st.divider()

    if beregn == "v₂ – sluthastighed (m/s)":
        c1, c2, c3 = st.columns(3)
        v1 = c1.number_input("v₁ – starthastighed (m/s)", value=0.0, format="%.6g")
        h1 = c2.number_input("h₁ – starthøjde (m)", value=10.0, format="%.6g")
        h2 = c3.number_input("h₂ – sluthøjde (m)", value=0.0, format="%.6g")
        val = v1**2 + 2 * G * (h1 - h2)
        if val < 0:
            st.error("Ingen reel løsning – energien rækker ikke til sluthøjden.")
        else:
            v2 = np.sqrt(val)
            st.success(f"**v₂ = {v2:.6g} m/s**")
            st.latex(rf"v_2 = \sqrt{{v_1^2 + 2g(h_1 - h_2)}} = \sqrt{{{v1:.6g}^2 + 2 \cdot {G} \cdot ({h1:.6g} - {h2:.6g})}} = {v2:.6g}\ \text{{m/s}}")

    elif beregn == "v₁ – starthastighed (m/s)":
        c1, c2, c3 = st.columns(3)
        v2 = c1.number_input("v₂ – sluthastighed (m/s)", value=14.0, format="%.6g")
        h1 = c2.number_input("h₁ – starthøjde (m)", value=10.0, format="%.6g")
        h2 = c3.number_input("h₂ – sluthøjde (m)", value=0.0, format="%.6g")
        val = v2**2 - 2 * G * (h1 - h2)
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
        h2 = h1 + (v1**2 - v2**2) / (2 * G)
        st.success(f"**h₂ = {h2:.6g} m**")
        st.latex(rf"h_2 = h_1 + \frac{{v_1^2 - v_2^2}}{{2g}} = {h2:.6g}\ \text{{m}}")

    else:
        c1, c2, c3 = st.columns(3)
        v1 = c1.number_input("v₁ (m/s)", value=0.0, format="%.6g")
        h2 = c2.number_input("h₂ (m)", value=0.0, format="%.6g")
        v2 = c3.number_input("v₂ (m/s)", value=14.0, format="%.6g")
        h1 = h2 + (v2**2 - v1**2) / (2 * G)
        st.success(f"**h₁ = {h1:.6g} m**")
        st.latex(rf"h_1 = h_2 + \frac{{v_2^2 - v_1^2}}{{2g}} = {h1:.6g}\ \text{{m}}")

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
