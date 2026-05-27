import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar

st.set_page_config(page_title="Dynamik", page_icon="💪", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
st.title("💪 Dynamik")
st.markdown("Newtons love, kræfter, impuls og kraftmoment")
st.divider()

G = 9.82

# Pre-fill from Eksamensopgaver guide
if st.session_state.pop("example_dynamik_2024q14", None):
    st.session_state["dyn_formel"] = "Spænding og tøjning:  σ = F / A"
    st.session_state["dyn_spand_mode"] = "d – diameter af cirkulært tværsnit (given F og σ_max)"
    st.session_state["dyn_F"] = 500000.0
    st.session_state["dyn_sigma"] = 1.6e9

formel = st.selectbox("Vælg formel", [
    "Newtons 2. lov:  F = m · a",
    "Tyngdekraft:  G = m · g",
    "Friktion:  f = μ · N",
    "Centripetalkraft:  Fc = m · v² / r",
    "Normalkraft i sløjfe (top/bund)",
    "Impuls:  p = m · v",
    "Impulsmomentloven:  F · Δt = Δp",
    "Kraftmoment:  τ = F · l",
    "Hældende plan",
    "Atwood-maskine:  to masser over trisse",
    "Spænding og tøjning:  σ = F / A",
], key="dyn_formel")

st.divider()

if formel == "Newtons 2. lov:  F = m · a":
    st.latex(r"F = m \cdot a")
    beregn = st.radio("Beregn:", ["F – kraft (N)", "m – masse (kg)", "a – acceleration (m/s²)"], horizontal=True)
    st.divider()

    if beregn == "F – kraft (N)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=10.0, min_value=1e-12, format="%.6g")
        a = c2.number_input("a – acceleration (m/s²)", value=2.0, format="%.6g")
        F = m * a
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = m \cdot a = {m:.6g} \cdot {a:.6g} = {F:.6g}\ \text{{N}}")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        F = c1.number_input("F – kraft (N)", value=20.0, format="%.6g")
        a = c2.number_input("a – acceleration (m/s²)", value=2.0, min_value=1e-12, format="%.6g")
        m = F / a
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{F}}{{a}} = \frac{{{F:.6g}}}{{{a:.6g}}} = {m:.6g}\ \text{{kg}}")

    else:
        c1, c2 = st.columns(2)
        F = c1.number_input("F – kraft (N)", value=20.0, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=10.0, min_value=1e-12, format="%.6g")
        a = F / m
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{F}}{{m}} = \frac{{{F:.6g}}}{{{m:.6g}}} = {a:.6g}\ \text{{m/s}}^2")

elif formel == "Tyngdekraft:  G = m · g":
    st.latex(r"G = m \cdot g")
    st.info(f"g = {G} m/s²")
    beregn = st.radio("Beregn:", ["G – tyngdekraft (N)", "m – masse (kg)"], horizontal=True)
    st.divider()

    g_val = st.number_input("g – tyngdeacceleration (m/s²)", value=G, format="%.6g")

    if beregn == "G – tyngdekraft (N)":
        m = st.number_input("m – masse (kg)", value=10.0, min_value=1e-12, format="%.6g")
        Fg = m * g_val
        st.success(f"**G = {Fg:.6g} N**")
        st.latex(rf"G = m \cdot g = {m:.6g} \cdot {g_val:.6g} = {Fg:.6g}\ \text{{N}}")

    else:
        Fg = st.number_input("G – tyngdekraft (N)", value=98.2, format="%.6g")
        m = Fg / g_val
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{G}}{{g}} = \frac{{{Fg:.6g}}}{{{g_val:.6g}}} = {m:.6g}\ \text{{kg}}")

elif formel == "Friktion:  f = μ · N":
    st.latex(r"f = \mu \cdot N")
    beregn = st.radio("Beregn:", ["f – friktionskraft (N)", "μ – friktionskoefficient", "N – normalkraft (N)"], horizontal=True)
    st.divider()

    if beregn == "f – friktionskraft (N)":
        c1, c2 = st.columns(2)
        mu = c1.number_input("μ – friktionskoefficient", value=0.3, min_value=0.0, format="%.6g")
        N  = c2.number_input("N – normalkraft (N)", value=100.0, format="%.6g")
        f = mu * N
        st.success(f"**f = {f:.6g} N**")
        st.latex(rf"f = \mu \cdot N = {mu:.6g} \cdot {N:.6g} = {f:.6g}\ \text{{N}}")

    elif beregn == "μ – friktionskoefficient":
        c1, c2 = st.columns(2)
        f = c1.number_input("f – friktionskraft (N)", value=30.0, format="%.6g")
        N = c2.number_input("N – normalkraft (N)", value=100.0, min_value=1e-12, format="%.6g")
        mu = f / N
        st.success(f"**μ = {mu:.6g}**")
        st.latex(rf"\mu = \frac{{f}}{{N}} = \frac{{{f:.6g}}}{{{N:.6g}}} = {mu:.6g}")

    else:
        c1, c2 = st.columns(2)
        f  = c1.number_input("f – friktionskraft (N)", value=30.0, format="%.6g")
        mu = c2.number_input("μ – friktionskoefficient", value=0.3, min_value=1e-12, format="%.6g")
        N = f / mu
        st.success(f"**N = {N:.6g} N**")
        st.latex(rf"N = \frac{{f}}{{\mu}} = \frac{{{f:.6g}}}{{{mu:.6g}}} = {N:.6g}\ \text{{N}}")

elif formel == "Centripetalkraft:  Fc = m · v² / r":
    st.latex(r"F_c = \frac{m \cdot v^2}{r} = m \cdot \omega^2 \cdot r")
    beregn = st.radio("Beregn:", ["Fc (N)", "m (kg)", "v (m/s)", "r (m)"], horizontal=True)
    st.divider()

    if beregn == "Fc (N)":
        c1, c2, c3 = st.columns(3)
        m = c1.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        r = c3.number_input("r – radius (m)", value=5.0, min_value=1e-12, format="%.6g")
        Fc = m * v**2 / r
        st.success(f"**Fc = {Fc:.6g} N**")
        st.latex(rf"F_c = \frac{{m v^2}}{{r}} = \frac{{{m:.6g} \cdot {v:.6g}^2}}{{{r:.6g}}} = {Fc:.6g}\ \text{{N}}")

    elif beregn == "m (kg)":
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        v  = c2.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        r  = c3.number_input("r – radius (m)", value=5.0, min_value=1e-12, format="%.6g")
        m = Fc * r / v**2
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{F_c \cdot r}}{{v^2}} = {m:.6g}\ \text{{kg}}")

    elif beregn == "v (m/s)":
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        r  = c3.number_input("r – radius (m)", value=5.0, min_value=1e-12, format="%.6g")
        v = np.sqrt(Fc * r / m)
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{F_c \cdot r}}{{m}}}} = {v:.6g}\ \text{{m/s}}")

    else:
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v  = c3.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        r = m * v**2 / Fc
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \frac{{m v^2}}{{F_c}} = {r:.6g}\ \text{{m}}")

elif formel == "Normalkraft i sløjfe (top/bund)":
    st.latex(r"\text{Bund:}\ N_{bund} = mg + \frac{mv^2}{r} \qquad \text{Top:}\ N_{top} = \frac{mv^2}{r} - mg")
    st.markdown("""
Legeme i cirkulær bevægelse i lodret plan. Centripetalkraft = netto radialkraft.

- **Bund**: N og tyngdekraft peger i modsatte retninger → N = mg + mv²/r
- **Top**: N og tyngdekraft peger begge mod centrum → N = mv²/r − mg
- **Minimum hastighed i top**: N ≥ 0 kræver v ≥ √(g·r)
""")
    st.divider()

    c1, c2, c3 = st.columns(3)
    m = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
    v = c2.number_input("v – fart i det givne punkt (m/s)", value=10.0, min_value=0.0, format="%.6g")
    r = c3.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-12, format="%.6g")

    Fc = m * v**2 / r
    N_bund = m * G + Fc
    N_top  = Fc - m * G
    v_min  = np.sqrt(G * r)

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("N (bund)", f"{N_bund:.4g} N")
    col2.metric("N (top)", f"{N_top:.4g} N")
    col3.metric("v_min (top)", f"{v_min:.4g} m/s")

    if N_top < 0:
        st.warning(f"⚠️ N_top = {N_top:.4g} N < 0: legemet mister kontakten i toppen! Minimum: v ≥ {v_min:.4g} m/s.")
    else:
        st.success("Legemet holder kontakten i toppen.")

    with st.expander("Vis udregning"):
        st.latex(rf"F_c = \frac{{mv^2}}{{r}} = \frac{{{m:.4g}\cdot{v:.4g}^2}}{{{r:.4g}}} = {Fc:.4g}\ \text{{N}}")
        st.latex(rf"N_{{bund}} = mg + F_c = {m:.4g}\cdot{G} + {Fc:.4g} = {N_bund:.4g}\ \text{{N}}")
        st.latex(rf"N_{{top}} = F_c - mg = {Fc:.4g} - {m:.4g}\cdot{G} = {N_top:.4g}\ \text{{N}}")
        st.latex(rf"v_{{min}} = \sqrt{{gr}} = \sqrt{{{G}\cdot{r:.4g}}} = {v_min:.4g}\ \text{{m/s}}")

elif formel == "Impuls:  p = m · v":
    st.latex(r"p = m \cdot v")
    beregn = st.radio("Beregn:", ["p – impuls (kg·m/s)", "m – masse (kg)", "v – hastighed (m/s)"], horizontal=True)
    st.divider()

    if beregn == "p – impuls (kg·m/s)":
        c1, c2 = st.columns(2)
        m = c1.number_input("m – masse (kg)", value=70.0, min_value=1e-12, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=5.0, format="%.6g")
        p = m * v
        st.success(f"**p = {p:.6g} kg·m/s**")
        st.latex(rf"p = m \cdot v = {m:.6g} \cdot {v:.6g} = {p:.6g}\ \text{{kg·m/s}}")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        p = c1.number_input("p – impuls (kg·m/s)", value=350.0, format="%.6g")
        v = c2.number_input("v – hastighed (m/s)", value=5.0, min_value=1e-12, format="%.6g")
        m = p / v
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{p}}{{v}} = \frac{{{p:.6g}}}{{{v:.6g}}} = {m:.6g}\ \text{{kg}}")

    else:
        c1, c2 = st.columns(2)
        p = c1.number_input("p – impuls (kg·m/s)", value=350.0, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=70.0, min_value=1e-12, format="%.6g")
        v = p / m
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \frac{{p}}{{m}} = \frac{{{p:.6g}}}{{{m:.6g}}} = {v:.6g}\ \text{{m/s}}")

elif formel == "Impulsmomentloven:  F · Δt = Δp":
    st.latex(r"F \cdot \Delta t = \Delta p = m \cdot (v_2 - v_1)")
    beregn = st.radio("Beregn:", ["F – gennemsnitskraft (N)", "Δt – tidinterval (s)", "Δp – impulsændring (kg·m/s)"], horizontal=True)
    st.divider()

    if beregn == "F – gennemsnitskraft (N)":
        c1, c2, c3, c4 = st.columns(4)
        m  = c1.number_input("m – masse (kg)", value=0.5, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ – starthastighed (m/s)", value=0.0, format="%.6g")
        v2 = c3.number_input("v₂ – sluthastighed (m/s)", value=20.0, format="%.6g")
        dt = c4.number_input("Δt – tid (s)", value=0.1, min_value=1e-12, format="%.6g")
        dp = m * (v2 - v1)
        F = dp / dt
        st.success(f"**F = {F:.6g} N**  (Δp = {dp:.6g} kg·m/s)")
        st.latex(rf"F = \frac{{\Delta p}}{{\Delta t}} = \frac{{{dp:.6g}}}{{{dt:.6g}}} = {F:.6g}\ \text{{N}}")

    elif beregn == "Δt – tidinterval (s)":
        c1, c2, c3, c4 = st.columns(4)
        m  = c1.number_input("m – masse (kg)", value=0.5, min_value=1e-12, format="%.6g")
        v1 = c2.number_input("v₁ (m/s)", value=0.0, format="%.6g")
        v2 = c3.number_input("v₂ (m/s)", value=20.0, format="%.6g")
        F  = c4.number_input("F – kraft (N)", value=100.0, min_value=1e-12, format="%.6g")
        dp = m * (v2 - v1)
        dt = dp / F
        st.success(f"**Δt = {dt:.6g} s**")
        st.latex(rf"\Delta t = \frac{{\Delta p}}{{F}} = \frac{{{dp:.6g}}}{{{F:.6g}}} = {dt:.6g}\ \text{{s}}")

    else:
        c1, c2, c3 = st.columns(3)
        F  = c1.number_input("F – kraft (N)", value=100.0, format="%.6g")
        dt = c2.number_input("Δt – tid (s)", value=0.1, min_value=1e-12, format="%.6g")
        dp = F * dt
        st.success(f"**Δp = {dp:.6g} kg·m/s**")
        st.latex(rf"\Delta p = F \cdot \Delta t = {F:.6g} \cdot {dt:.6g} = {dp:.6g}\ \text{{kg·m/s}}")

elif formel == "Kraftmoment:  τ = F · l":
    st.latex(r"\tau = F \cdot l \cdot \sin\theta")
    beregn = st.radio("Beregn:", ["τ – kraftmoment (N·m)", "F – kraft (N)", "l – arm (m)"], horizontal=True)
    st.divider()

    if beregn == "τ – kraftmoment (N·m)":
        c1, c2, c3 = st.columns(3)
        F     = c1.number_input("F – kraft (N)", value=50.0, format="%.6g")
        l     = c2.number_input("l – kraftarm (m)", value=2.0, min_value=1e-12, format="%.6g")
        theta = c3.number_input("θ – vinkel (grader)", value=90.0, min_value=0.0, max_value=180.0, format="%.6g")
        tau = F * l * np.sin(np.radians(theta))
        st.success(f"**τ = {tau:.6g} N·m**")
        st.latex(rf"\tau = {F:.6g} \cdot {l:.6g} \cdot \sin({theta:.4g}°) = {tau:.6g}\ \text{{N·m}}")

    elif beregn == "F – kraft (N)":
        c1, c2, c3 = st.columns(3)
        tau   = c1.number_input("τ – kraftmoment (N·m)", value=100.0, format="%.6g")
        l     = c2.number_input("l – kraftarm (m)", value=2.0, min_value=1e-12, format="%.6g")
        theta = c3.number_input("θ – vinkel (grader)", value=90.0, min_value=1.0, max_value=180.0, format="%.6g")
        F = tau / (l * np.sin(np.radians(theta)))
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = \frac{{\tau}}{{l \sin\theta}} = {F:.6g}\ \text{{N}}")

    else:
        c1, c2, c3 = st.columns(3)
        tau   = c1.number_input("τ – kraftmoment (N·m)", value=100.0, format="%.6g")
        F     = c2.number_input("F – kraft (N)", value=50.0, min_value=1e-12, format="%.6g")
        theta = c3.number_input("θ – vinkel (grader)", value=90.0, min_value=1.0, max_value=180.0, format="%.6g")
        l = tau / (F * np.sin(np.radians(theta)))
        st.success(f"**l = {l:.6g} m**")
        st.latex(rf"l = \frac{{\tau}}{{F \sin\theta}} = {l:.6g}\ \text{{m}}")

elif formel == "Hældende plan":
    st.latex(r"F_{\parallel} = m g \sin\theta \qquad N = m g \cos\theta \qquad f = \mu \cdot N")
    st.markdown("Analyse af legeme på hældende plan. Valgfri ydre kraft langs planen (+ = op ad, − = ned ad).")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    m      = c1.number_input("m – masse (kg)", value=10.0, min_value=1e-12, format="%.6g")
    theta  = c2.number_input("θ – hældningsvinkel (°)", value=30.0, min_value=0.0, max_value=89.9, format="%.6g")
    mu     = c3.number_input("μ – friktionskoefficient (0 = ingen)", value=0.2, min_value=0.0, format="%.6g")
    F_ext  = c4.number_input("F_ydre langs plan (N, + op, − ned, 0=ingen)", value=0.0, format="%.6g")

    th_r  = np.radians(theta)
    N     = m * G * np.cos(th_r)
    F_par = m * G * np.sin(th_r)   # tyngdekraft-komponent ned ad planen
    f_max = mu * N

    # Nettoretning: F_ext (op) mod F_par (ned) + friktion (modsat bevægelse)
    # Friktion: modsat netto-bevægelse
    F_tryk = F_ext - F_par          # positiv = objekt accelererer op
    if abs(F_tryk) <= f_max:
        friktion = -F_tryk          # statisk friktion balancerer nettotendensen
        F_net = 0.0
    elif F_tryk > 0:
        friktion = -f_max           # friktion er ned ad (modsat bevægelse opad)
        F_net = F_ext - F_par - f_max
    else:
        friktion = f_max            # friktion er op ad (modsat bevægelse nedad)
        F_net = F_ext - F_par + f_max

    a = F_net / m

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Normalkraft N", f"{N:.4g} N")
    col2.metric("Tyngd.-komp. (ned)", f"{F_par:.4g} N")
    col3.metric("Resultantkraft", f"{F_net:.4g} N")
    col4.metric("Acceleration a", f"{a:.4g} m/s²")

    if abs(F_net) < 1e-9:
        st.info("Legemet er i ligevægt (nul-acceleration).")
    elif F_net > 0:
        st.info("Netto­kraft OP ad planen – legemet accelererer opad.")
    else:
        st.info("Netto­kraft NED ad planen – legemet accelererer nedad.")

    with st.expander("Vis udregning"):
        st.latex(rf"N = mg\cos\theta = {m:.4g}\cdot{G}\cdot\cos({theta:.4g}°) = {N:.4g}\ \text{{N}}")
        st.latex(rf"F_{{\parallel}} = mg\sin\theta = {F_par:.4g}\ \text{{N (ned)}},\quad f_{{max}} = \mu N = {f_max:.4g}\ \text{{N}}")
        st.latex(rf"F_{{net}} = F_{{ydre}} - F_{{\parallel}} \pm f = {F_ext:.4g} - {F_par:.4g} + ({friktion:.4g}) = {F_net:.4g}\ \text{{N}}")
        st.latex(rf"a = \frac{{F_{{net}}}}{{m}} = {a:.4g}\ \text{{m/s}}^2")

elif formel == "Atwood-maskine:  to masser over trisse":
    st.latex(r"a = \frac{(m_2 - m_1)\,g}{m_1 + m_2} \qquad T = \frac{2\,m_1 m_2\,g}{m_1 + m_2}")
    st.markdown("Trissen er masseløs og friktionsfri. m₂ > m₁ → m₂ accelererer nedad.")
    st.divider()

    beregn = st.radio("Beregn:", ["a og T (given m₁, m₂)", "m₂ (given a og m₁)"], horizontal=True)
    st.divider()

    if beregn == "a og T (given m₁, m₂)":
        c1, c2 = st.columns(2)
        m1 = c1.number_input("m₁ – lettere masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        m2 = c2.number_input("m₂ – tungere masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        a  = (m2 - m1) * G / (m1 + m2)
        T  = 2 * m1 * m2 * G / (m1 + m2)
        st.success(f"**a = {a:.4g} m/s²**   **T = {T:.4g} N**")
        st.latex(rf"a = \frac{{({m2:.4g} - {m1:.4g}) \cdot {G}}}{{{m1:.4g} + {m2:.4g}}} = {a:.4g}\ \text{{m/s}}^2")
        st.latex(rf"T = \frac{{2 \cdot {m1:.4g} \cdot {m2:.4g} \cdot {G}}}{{{m1:.4g} + {m2:.4g}}} = {T:.4g}\ \text{{N}}")
        if a < 0:
            st.info("a < 0: m₁ er tungere – m₁ accelererer nedad, m₂ opad.")
        elif a > 0:
            st.info("a > 0: m₂ er tungere – m₂ accelererer nedad, m₁ opad.")
        else:
            st.info("a = 0: ligevægt (m₁ = m₂).")

    else:
        c1, c2 = st.columns(2)
        a_val = c1.number_input("a – acceleration (m/s²)", value=3.27, format="%.6g")
        m1    = c2.number_input("m₁ – lette masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        # a = (m2-m1)g/(m1+m2) → m2(g-a) = m1(g+a) → m2 = m1(g+a)/(g-a)
        if abs(G - a_val) < 1e-9:
            st.error("a = g – ingen løsning (uendelig masse)")
        else:
            m2 = m1 * (G + a_val) / (G - a_val)
            st.success(f"**m₂ = {m2:.4g} kg**")
            st.latex(rf"m_2 = m_1 \frac{{g + a}}{{g - a}} = {m1:.4g} \cdot \frac{{{G} + {a_val:.4g}}}{{{G} - {a_val:.4g}}} = {m2:.4g}\ \text{{kg}}")

elif formel == "Spænding og tøjning:  σ = F / A":
    st.latex(r"\sigma = \frac{F}{A} \qquad \varepsilon = \frac{\Delta L}{L_0} \qquad E = \frac{\sigma}{\varepsilon}")
    st.markdown("Normalspænding, tøjning og Youngs modul. Tværsnitsareal for cirkulært tværsnit: A = πd²/4.")
    st.divider()

    beregn = st.selectbox("Beregn:", [
        "σ – normalspænding (given F og A)",
        "F – kraft (given σ og A)",
        "A – areal (given F og σ)",
        "d – diameter af cirkulært tværsnit (given F og σ_max)",
        "ε – tøjning (given ΔL og L₀)",
        "E – Youngs modul (given σ og ε)",
    ], key="dyn_spand_mode")

    st.divider()

    if beregn == "σ – normalspænding (given F og A)":
        c1, c2 = st.columns(2)
        F_val = c1.number_input("F – kraft (N)", value=1000.0, format="%.6g")
        A_val = c2.number_input("A – tværsnitsareal (m²)", value=1e-4, min_value=1e-20, format="%.6g")
        sigma = F_val / A_val
        st.success(f"**σ = {sigma:.6g} Pa = {sigma/1e6:.6g} MPa**")
        st.latex(rf"\sigma = \frac{{F}}{{A}} = \frac{{{F_val:.6g}}}{{{A_val:.6g}}} = {sigma:.6g}\ \text{{Pa}}")

    elif beregn == "F – kraft (given σ og A)":
        c1, c2 = st.columns(2)
        sigma = c1.number_input("σ – spænding (Pa)", value=1e6, format="%.6g")
        A_val = c2.number_input("A – tværsnitsareal (m²)", value=1e-4, min_value=1e-20, format="%.6g")
        F_val = sigma * A_val
        st.success(f"**F = {F_val:.6g} N**")
        st.latex(rf"F = \sigma \cdot A = {sigma:.6g} \cdot {A_val:.6g} = {F_val:.6g}\ \text{{N}}")

    elif beregn == "A – areal (given F og σ)":
        c1, c2 = st.columns(2)
        F_val = c1.number_input("F – kraft (N)", value=1000.0, format="%.6g")
        sigma = c2.number_input("σ – spænding (Pa)", value=1e6, min_value=1e-20, format="%.6g")
        A_val = F_val / sigma
        st.success(f"**A = {A_val:.6g} m²**")
        st.latex(rf"A = \frac{{F}}{{\sigma}} = \frac{{{F_val:.6g}}}{{{sigma:.6g}}} = {A_val:.6g}\ \text{{m}}^2")

    elif beregn == "d – diameter af cirkulært tværsnit (given F og σ_max)":
        st.info("Cirkulært tværsnit: A = πd²/4  →  d = √(4F / (π·σ_max))")
        c1, c2 = st.columns(2)
        F_val   = c1.number_input("F – kraft (N)", value=5000.0, format="%.6g", key="dyn_F")
        sigma   = c2.number_input("σ_max – maksimal spænding (Pa)", value=50e6, min_value=1e-20, format="%.6g", key="dyn_sigma")
        d = np.sqrt(4 * F_val / (np.pi * sigma))
        A_val = np.pi * d**2 / 4
        st.success(f"**d = {d:.6g} m = {d*1000:.6g} mm**")
        st.latex(rf"d = \sqrt{{\frac{{4F}}{{\pi \sigma_{{max}}}}}} = \sqrt{{\frac{{4 \cdot {F_val:.6g}}}{{\pi \cdot {sigma:.6g}}}}} = {d:.6g}\ \text{{m}}")
        st.latex(rf"A = \frac{{\pi d^2}}{{4}} = {A_val:.6g}\ \text{{m}}^2")
        if abs(F_val - 500000.0) < 1 and abs(sigma - 1.6e9) < 1e6:
            st.success(f"📋 **2024 Q14** – Kulfiber: m=50 kg, v=100 m/s, R=1 m → F=500 000 N, σ_max=1600 MPa → d ≈ 2.0 cm ✓")

    elif beregn == "ε – tøjning (given ΔL og L₀)":
        c1, c2 = st.columns(2)
        dL = c1.number_input("ΔL – forlængelse (m)", value=0.001, format="%.6g")
        L0 = c2.number_input("L₀ – original længde (m)", value=1.0, min_value=1e-12, format="%.6g")
        eps = dL / L0
        st.success(f"**ε = {eps:.6g}  ({eps*100:.4g}%)**")
        st.latex(rf"\varepsilon = \frac{{\Delta L}}{{L_0}} = \frac{{{dL:.6g}}}{{{L0:.6g}}} = {eps:.6g}")

    elif beregn == "E – Youngs modul (given σ og ε)":
        c1, c2 = st.columns(2)
        sigma = c1.number_input("σ – spænding (Pa)", value=1e6, format="%.6g")
        eps   = c2.number_input("ε – tøjning (dimensionsløs)", value=0.01, min_value=1e-20, format="%.6g")
        E_mod = sigma / eps
        st.success(f"**E = {E_mod:.6g} Pa = {E_mod/1e9:.6g} GPa**")
        st.latex(rf"E = \frac{{\sigma}}{{\varepsilon}} = \frac{{{sigma:.6g}}}{{{eps:.6g}}} = {E_mod:.6g}\ \text{{Pa}}")
        st.markdown("**Typiske Youngs-moduler:**")
        st.markdown("""
| Materiale | E (GPa) |
|-----------|---------|
| Stål | ~200 |
| Aluminium | ~70 |
| Beton | ~30 |
| Gummi | ~0.01–0.1 |
""")
