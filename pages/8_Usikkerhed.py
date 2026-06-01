import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid, breadcrumb, parse_numpy_array

st.set_page_config(page_title="Usikkerhed", page_icon="📏", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("📏", "Usikkerhed")
st.title("📏 Usikkerhed & Fejlanalyse")
st.markdown("Måleusikkerhed, fejlpropagation og statistik — Lecture 3 (10060)")
st.divider()

# Pre-fill fra Eksamensopgaver guide
if st.session_state.pop("example_usikkerhed_2024q1", None):
    st.session_state["usk_formel"] = "Fejlpropagation – generel (numerisk)"
if st.session_state.pop("example_usikkerhed_2025q2", None):
    st.session_state["usk_formel"] = "Forenelighedstest – er ny måling OK?"
if st.session_state.pop("example_usikkerhed_2025q3", None):
    st.session_state["usk_formel"] = "Potenslov-fitting:  y = A · xᵅ  (log-log regression)"

_USK_FORMULAS = [
    ("Gennemsnit og stdafv.",  "x̄,  s = √(Σ(xᵢ−x̄)²/(n−1))",  "Gennemsnit og standardafvigelse"),
    ("Standardusikkerhed A",   "u_A = s/√n",                   "Standardmåleusikkerhed (type A)"),
    ("Forenelighedstest",      "|x_ny − x̄|/u_A < 2?",         "Forenelighedstest – er ny måling OK?"),
    ("Relativ/absolut",        "Δx/x  og  Δx",                 "Relativ og absolut usikkerhed"),
    ("Fejlprop. +/−",          "Δz = √(Δx²+Δy²)",             "Fejlpropagation – addition/subtraktion"),
    ("Fejlprop. ×/÷",          "Δz/z = √((Δx/x)²+(Δy/y)²)",   "Fejlpropagation – multiplikation/division"),
    ("Fejlprop. potens",       "Δz/z = |n|·Δx/x",             "Fejlpropagation – potens:  z = xⁿ"),
    ("Fejlprop. generel",      "numerisk ±Δ-metode",           "Fejlpropagation – generel (numerisk)"),
    ("Samlet usikkerhed",      "u_tot = √(u_A²+u_B²)",        "Samlet usikkerhed (type A + B)"),
    ("Potenslov-fitting",      "y = A·xᵅ  (log-log)",          "Potenslov-fitting:  y = A · xᵅ  (log-log regression)"),
    ("Lineær regression",      "y = a·x + b",                  "Lineær regression:  y = a · x + b"),
]
formel = formula_card_grid(_USK_FORMULAS, "usk_formel")

USK_TIPS = {
    "Gennemsnit og standardafvigelse": "s er standardafvigelsen for stikprøven (n−1 i nævner). SEM = s/√n er usikkerheden på middelværdien.",
    "Standardmåleusikkerhed (type A)": "Type A = statistisk. u_A = s/√n. Bruges når du har gentagne målinger.",
    "Forenelighedstest – er ny måling OK?": "Beregn |x_ny − x̄| / u_A. Er det < 2 er målingen forenelig (95% konfidens).",
    "Relativ og absolut usikkerhed": "Relativ usikkerhed = Δx/x (dimensionsløs). Absolut = Δx (samme enhed som x).",
    "Fejlpropagation – addition/subtraktion": "Δz = √(Δx² + Δy²). Absolutte usikkerheder lægges i kvadrat sammen.",
    "Fejlpropagation – multiplikation/division": "Δz/z = √((Δx/x)² + (Δy/y)²). Relative usikkerheder kombineres.",
    "Fejlpropagation – potens:  z = xⁿ": "Δz/z = |n| · Δx/x. Eksponenten forstærker den relative usikkerhed.",
    "Fejlpropagation – generel (numerisk)": "Numerisk partiel differentiering: variér én variabel ad gangen med ±Δ og se effekten.",
    "Samlet usikkerhed (type A + B)": "u_total = √(u_A² + u_B²). Type B er f.eks. instrument­usikkerhed fra specifikationer.",
    "Potenslov-fitting:  y = A · xᵅ  (log-log regression)": "ln(y) = ln(A) + α·ln(x). Hældningen på log-log-plot er α. R² tæt på 1 = godt fit.",
    "Lineær regression:  y = a · x + b": "Mindste kvadraters metode. Hældning a = Σ(xᵢ−x̄)(yᵢ−ȳ) / Σ(xᵢ−x̄)². R² = 1: perfekt fit.",
}
show_tips(formel, USK_TIPS)
st.divider()

if formel == "Gennemsnit og standardafvigelse":
    st.latex(r"\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i \qquad s = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n-1}}")
    st.markdown("Indtast måleværdier kommasepareret, f.eks. `9.81, 9.79, 9.83, 9.80`")
    st.divider()

    raw = st.text_input("Måleværdier:", value="9.81, 9.79, 9.83, 9.80, 9.82",
                        help="Paste direkte fra eksamen: np.array([9.81, 9.79, ...]) eller plain 9.81, 9.79, ...")
    try:
        vals = parse_numpy_array(raw)
        n = len(vals)
        if n < 2:
            st.error("Mindst 2 måleværdier kræves for at beregne standardafvigelse.")
            st.stop()
        mean = np.mean(vals)
        std  = np.std(vals, ddof=1)
        sem  = std / np.sqrt(n)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("n – antal målinger", n)
        col2.metric("x̄ – gennemsnit", f"{mean:.6g}")
        col3.metric("s – std.afvigelse", f"{std:.4g}")
        col4.metric("u(x̄) – std.usikkerhed", f"{sem:.4g}")

        rel_str = f"  (relativ usikkerhed: {sem/abs(mean)*100:.3g}%)" if abs(mean) > 1e-12 else ""
        st.success(f"**Resultat: x̄ = {mean:.6g} ± {sem:.4g}**{rel_str}")

        with st.expander("Vis tabel"):
            rows = [{"i": i+1, "xᵢ": v, "xᵢ − x̄": f"{v-mean:.4g}", "(xᵢ − x̄)²": f"{(v-mean)**2:.4g}"} for i, v in enumerate(vals)]
            st.table(rows)

        with st.expander("Vis udregning"):
            st.latex(rf"\bar{{x}} = \frac{{1}}{{{n}}}\sum x_i = {mean:.6g}")
            st.latex(rf"s = \sqrt{{\frac{{\sum(x_i - \bar{{x}})^2}}{{{n}-1}}}} = {std:.4g}")
            st.latex(rf"u(\bar{{x}}) = \frac{{s}}{{\sqrt{{n}}}} = \frac{{{std:.4g}}}{{\sqrt{{{n}}}}} = {sem:.4g}")
    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")

elif formel == "Standardmåleusikkerhed (type A)":
    st.latex(r"u(\bar{x}) = \frac{s}{\sqrt{n}}")
    st.markdown("Beregn type A-usikkerhed fra kendte statistiske størrelser.")
    st.divider()

    c1, c2 = st.columns(2)
    s = c1.number_input("s – standardafvigelse", value=0.015, min_value=0.0, format="%.6g")
    n = c2.number_input("n – antal målinger", value=5, min_value=1, step=1)
    u = s / np.sqrt(n)
    st.success(f"**u(x̄) = {u:.6g}**")
    st.latex(rf"u(\bar{{x}}) = \frac{{s}}{{\sqrt{{n}}}} = \frac{{{s:.6g}}}{{\sqrt{{{n}}}}} = {u:.6g}")

elif formel == "Forenelighedstest – er ny måling OK?":
    st.latex(r"|x_{ny} - \bar{x}| \leq 2s \quad \Rightarrow \quad \text{forenelig}")
    st.markdown("Tjek om en ny enkeltmåling er forenelig med et eksisterende datasæt (sammenlign med ±2σ).")
    st.divider()

    raw = st.text_input("Eksisterende måleværdier:", value="20.1, 20.2, 20.5, 19.8",
                        help="Accepts np.array([...]) syntax direkte fra eksamen")
    x_ny = st.number_input("Ny måleværdi:", value=20.6, format="%.6g")

    try:
        vals = parse_numpy_array(raw)
        n = len(vals)
        mean = np.mean(vals)
        s = np.std(vals, ddof=1)
        u = s / np.sqrt(n)
        afstand = abs(x_ny - mean)
        afstand_s = afstand / s

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("x̄", f"{mean:.4g}")
        col2.metric("s (σ̂)", f"{s:.4g}")
        col3.metric("|x_ny − x̄|", f"{afstand:.4g}")
        col4.metric("afstand i σ", f"{afstand_s:.2f}σ")

        if afstand <= 2 * s:
            st.success(f"**Forenelig** – ny måling er {afstand_s:.2f}σ fra middelværdi (≤ 2σ).")
        elif afstand <= 3 * s:
            st.warning(f"**Måske forenelig** – {afstand_s:.2f}σ fra middelværdi (2σ–3σ).")
        else:
            st.error(f"**Ikke forenelig** – {afstand_s:.2f}σ fra middelværdi (> 3σ).")

        with st.expander("Vis udregning"):
            st.latex(rf"\bar{{x}} = {mean:.4g},\quad s = {s:.4g},\quad u(\bar{{x}}) = s/\sqrt{{n}} = {u:.4g}")
            st.latex(rf"|x_{{ny}} - \bar{{x}}| = |{x_ny:.4g} - {mean:.4g}| = {afstand:.4g} = {afstand_s:.2f}\sigma")
    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")

elif formel == "Relativ og absolut usikkerhed":
    st.latex(r"\text{Absolut: } \Delta x \qquad \text{Relativ: } \frac{\Delta x}{x} \times 100\%")
    beregn = st.radio("Beregn:", ["Relativ ud fra absolut", "Absolut ud fra relativ"], horizontal=True)
    st.divider()

    if beregn == "Relativ ud fra absolut":
        c1, c2 = st.columns(2)
        x  = c1.number_input("x – måleværdi", value=9.82, format="%.6g")
        dx = c2.number_input("Δx – absolut usikkerhed", value=0.02, min_value=0.0, format="%.6g")
        rel = dx / abs(x) * 100
        st.success(f"**Relativ usikkerhed = {rel:.4g}%**")
        st.latex(rf"\frac{{\Delta x}}{{x}} \times 100\% = \frac{{{dx:.6g}}}{{{x:.6g}}} \times 100\% = {rel:.4g}\%")

    else:
        c1, c2 = st.columns(2)
        x   = c1.number_input("x – måleværdi", value=9.82, format="%.6g")
        rel = c2.number_input("Relativ usikkerhed (%)", value=0.2, min_value=0.0, format="%.6g")
        dx = rel / 100 * abs(x)
        st.success(f"**Δx = {dx:.6g}**")
        st.latex(rf"\Delta x = \frac{{\text{{rel}}\%}}{{100}} \cdot x = \frac{{{rel:.6g}}}{{100}} \cdot {x:.6g} = {dx:.6g}")

elif formel == "Fejlpropagation – addition/subtraktion":
    st.latex(r"z = x \pm y \implies u(z) = \sqrt{(\Delta x)^2 + (\Delta y)^2} \quad \text{(uafhængige fejl, RSS)}")
    st.info("For uafhængige målinger bruges RSS (kvadratisk sum). Absolut sum gælder kun for maksimalt korrelerede fejl.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        x  = st.number_input("x", value=10.0, format="%.6g", key="add_x")
        dx = st.number_input("Δx", value=0.1, min_value=0.0, format="%.6g", key="add_dx")
    with c2:
        y  = st.number_input("y", value=5.0, format="%.6g", key="add_y")
        dy = st.number_input("Δy", value=0.05, min_value=0.0, format="%.6g", key="add_dy")

    op = st.radio("Operation:", ["x + y", "x − y"], horizontal=True)
    z = x + y if op == "x + y" else x - y
    dz_rss = np.sqrt(dx**2 + dy**2)
    dz_abs = dx + dy
    rel = dz_rss / abs(z) * 100 if abs(z) > 1e-12 else float('inf')

    st.success(f"**z = {z:.6g} ± {dz_rss:.4g}** (RSS)   (relativ: {rel:.3g}%)")
    if op == "x + y":
        st.latex(rf"z = {x:.6g} + {y:.6g} = {z:.6g}")
    else:
        st.latex(rf"z = {x:.6g} - {y:.6g} = {z:.6g}")
    st.latex(rf"u(z) = \sqrt{{(\Delta x)^2 + (\Delta y)^2}} = \sqrt{{{dx:.4g}^2 + {dy:.4g}^2}} = {dz_rss:.4g}")
    st.caption(f"Worst case (absolut sum): Δz = {dx:.4g} + {dy:.4g} = {dz_abs:.4g}")

elif formel == "Fejlpropagation – multiplikation/division":
    st.latex(r"z = x \cdot y \text{ eller } \frac{x}{y} \implies \frac{u(z)}{|z|} = \sqrt{\left(\frac{\Delta x}{|x|}\right)^2 + \left(\frac{\Delta y}{|y|}\right)^2} \quad \text{(RSS)}")
    st.info("For uafhængige målinger bruges RSS (kvadratisk sum). Absolut sum gælder kun for maksimalt korrelerede fejl.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        x  = st.number_input("x", value=10.0, format="%.6g", key="mul_x")
        dx = st.number_input("Δx", value=0.1, min_value=0.0, format="%.6g", key="mul_dx")
    with c2:
        y  = st.number_input("y", value=5.0, format="%.6g", key="mul_y")
        dy = st.number_input("Δy", value=0.1, min_value=0.0, format="%.6g", key="mul_dy")

    op = st.radio("Operation:", ["x · y", "x / y"], horizontal=True)
    if op == "x · y":
        z = x * y
    else:
        if abs(y) < 1e-12:
            st.error("y = 0")
            st.stop()
        z = x / y

    rel_x = dx / abs(x) if abs(x) > 1e-12 else 0
    rel_y = dy / abs(y) if abs(y) > 1e-12 else 0
    rel_z_rss = np.sqrt(rel_x**2 + rel_y**2)
    rel_z_abs = rel_x + rel_y
    dz_rss = rel_z_rss * abs(z)
    dz_abs = rel_z_abs * abs(z)

    st.success(f"**z = {z:.6g} ± {dz_rss:.4g}** (RSS)   (relativ: {rel_z_rss*100:.3g}%)")
    st.latex(rf"\frac{{u(z)}}{{|z|}} = \sqrt{{\left(\frac{{\Delta x}}{{|x|}}\right)^2 + \left(\frac{{\Delta y}}{{|y|}}\right)^2}} = \sqrt{{{rel_x:.4g}^2 + {rel_y:.4g}^2}} = {rel_z_rss:.4g}")
    st.latex(rf"u(z) = {rel_z_rss:.4g} \cdot {abs(z):.6g} = {dz_rss:.4g}")
    st.caption(f"Worst case (absolut sum): Δz = {dz_abs:.4g}  (relativ: {rel_z_abs*100:.3g}%)")

elif formel == "Fejlpropagation – potens:  z = xⁿ":
    st.latex(r"z = x^n \implies \frac{\Delta z}{|z|} = |n| \cdot \frac{\Delta x}{|x|}")
    st.divider()

    c1, c2, c3 = st.columns(3)
    x  = c1.number_input("x – måleværdi", value=4.0, format="%.6g")
    dx = c2.number_input("Δx – absolut usikkerhed", value=0.1, min_value=0.0, format="%.6g")
    n  = c3.number_input("n – eksponent", value=2.0, format="%.6g")

    z = x**n
    dz = abs(n) * (dx / abs(x)) * abs(z)
    rel = dz / abs(z) * 100

    st.success(f"**z = x^n = {z:.6g} ± {dz:.6g}**   (relativ: {rel:.3g}%)")
    st.latex(rf"z = {x:.6g}^{{{n:.6g}}} = {z:.6g}")
    st.latex(rf"\frac{{\Delta z}}{{|z|}} = |n| \cdot \frac{{\Delta x}}{{|x|}} = {abs(n):.6g} \cdot \frac{{{dx:.6g}}}{{{abs(x):.6g}}} = {abs(n)*dx/abs(x):.4g}")
    st.latex(rf"\Delta z = {dz:.4g}")

elif formel == "Fejlpropagation – generel (numerisk)":
    st.latex(r"\Delta z = \left|\frac{\partial z}{\partial x_i}\right|\Delta x_i + \cdots \approx \sum_i \frac{|f(x_i+\delta) - f(x_i-\delta)|}{2\delta}\Delta x_i")
    st.markdown("Vælg formel og beregn usikkerhed numerisk via centrale differencer.")
    st.divider()

    valg = st.selectbox("Formel:", [
        "z = ½mv²  (kinetisk energi)",
        "t = (v₀ + √(v₀²+2gh)) / g  (2024 eksamen Q1)",
        "x = v·cos(θ)·t  (vandret kastebevægelse-rækkevidde)",
        "Fc = mv²/r  (centripetalkraft)",
        "E = hf  (fotonenergi)",
    ])
    st.divider()

    eps = 1e-7

    if valg == "z = ½mv²  (kinetisk energi)":
        c1, c2, c3, c4 = st.columns(4)
        m  = c1.number_input("m (kg)", value=2.0, format="%.6g")
        dm = c2.number_input("Δm (kg)", value=0.01, min_value=0.0, format="%.6g")
        v  = c3.number_input("v (m/s)", value=10.0, format="%.6g")
        dv = c4.number_input("Δv (m/s)", value=0.1, min_value=0.0, format="%.6g")
        f = lambda m_, v_: 0.5 * m_ * v_**2
        z = f(m, v)
        dz_dm = abs(f(m+eps, v) - f(m-eps, v)) / (2*eps)
        dz_dv = abs(f(m, v+eps) - f(m, v-eps)) / (2*eps)
        dz = np.sqrt((dz_dm * dm)**2 + (dz_dv * dv)**2)
        pct = f"{dz/z*100:.3g}%" if abs(z) > 1e-12 else "–"
        st.success(f"**E_k = {z:.6g} J ± {dz:.4g} J** (RSS)   ({pct})")
        st.latex(rf"\frac{{\partial z}}{{\partial m}} = \tfrac{{1}}{{2}}v^2 = {dz_dm:.6g},\quad \frac{{\partial z}}{{\partial v}} = mv = {dz_dv:.6g}")
        st.latex(rf"u(E_k) = \sqrt{{({dz_dm:.4g}\cdot{dm:.4g})^2 + ({dz_dv:.4g}\cdot{dv:.4g})^2}} = {dz:.4g}\ \text{{J}}")

    elif valg == "t = (v₀ + √(v₀²+2gh)) / g  (2024 eksamen Q1)":
        st.markdown("**2024 eksamensopgave 1:** sten kastet op fra højde h med starthastighed v₀.")
        st.latex(r"t = \frac{v_0 + \sqrt{v_0^2 + 2gh}}{g}")
        c1, c2, c3 = st.columns(3)
        v0 = c1.number_input("v₀ (m/s)", value=4.20, format="%.6g")
        dv0 = c1.number_input("Δv₀ (m/s)", value=0.05, min_value=0.0, format="%.6g")
        h  = c2.number_input("h (m)", value=1.60, format="%.6g")
        dh = c2.number_input("Δh (m)", value=0.05, min_value=0.0, format="%.6g")
        g  = c3.number_input("g (m/s²)", value=9.82, format="%.6g")
        dg = c3.number_input("Δg (m/s²)", value=0.01, min_value=0.0, format="%.6g")
        f2 = lambda v0_, h_, g_: (v0_ + np.sqrt(v0_**2 + 2*g_*h_)) / g_
        t = f2(v0, h, g)
        dt_dv0 = abs(f2(v0+eps, h, g) - f2(v0-eps, h, g)) / (2*eps)
        dt_dh  = abs(f2(v0, h+eps, g) - f2(v0, h-eps, g)) / (2*eps)
        dt_dg  = abs(f2(v0, h, g+eps) - f2(v0, h, g-eps)) / (2*eps)
        delta_v0 = dt_dv0 * dv0
        delta_h  = dt_dh  * dh
        delta_g  = dt_dg  * dg
        dt_rss = np.sqrt(delta_v0**2 + delta_h**2 + delta_g**2)
        dt_abs = delta_v0 + delta_h + delta_g
        st.success(f"**t = {t:.4g} s ± {dt_rss:.4g} s** (RSS, uafhængige usikkerheder)")
        col1, col2, col3 = st.columns(3)
        col1.metric("δt fra v₀", f"{delta_v0:.4g} s")
        col2.metric("δt fra h", f"{delta_h:.4g} s")
        col3.metric("δt fra g", f"{delta_g:.4g} s")
        st.latex(rf"u(t) = \sqrt{{\delta t(v_0)^2 + \delta t(h)^2 + \delta t(g)^2}} = \sqrt{{{delta_v0:.4f}^2 + {delta_h:.4f}^2 + {delta_g:.4f}^2}} = {dt_rss:.4f}\ \text{{s}}")
        st.caption(f"Absolut sum (worst case): Δt = {dt_abs:.4f} s")
        if delta_h < delta_v0:
            st.info(f"δt(h) < δt(v₀): {delta_h:.4g} < {delta_v0:.4g}  →  v₀ bidrager mest")
        else:
            st.info(f"δt(h) > δt(v₀): {delta_h:.4g} > {delta_v0:.4g}  →  h bidrager mest")

    elif valg == "x = v·cos(θ)·t  (vandret kastebevægelse-rækkevidde)":
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        v  = c1.number_input("v (m/s)", value=10.0, format="%.6g")
        dv = c2.number_input("Δv", value=0.1, min_value=0.0, format="%.6g")
        th = c3.number_input("θ (°)", value=45.0, format="%.6g")
        dth = c4.number_input("Δθ (°)", value=1.0, min_value=0.0, format="%.6g")
        t  = c5.number_input("t (s)", value=2.0, format="%.6g")
        dt = c6.number_input("Δt (s)", value=0.05, min_value=0.0, format="%.6g")
        f3 = lambda v_, th_, t_: v_ * np.cos(np.radians(th_)) * t_
        z = f3(v, th, t)
        dx_dv  = abs(f3(v+eps*1e6, th, t) - f3(v-eps*1e6, th, t)) / (2*eps*1e6)
        dx_dth = abs(f3(v, th+0.0001, t) - f3(v, th-0.0001, t)) / 0.0002
        dx_dt  = abs(f3(v, th, t+eps*1e4) - f3(v, th, t-eps*1e4)) / (2*eps*1e4)
        dz = dx_dv*dv + dx_dth*dth + dx_dt*dt
        st.success(f"**x = {z:.4g} m ± {dz:.4g} m**   ({dz/z*100:.3g}%)")

    elif valg == "Fc = mv²/r  (centripetalkraft)":
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        m  = c1.number_input("m (kg)", value=0.5, format="%.6g")
        dm = c2.number_input("Δm", value=0.001, min_value=0.0, format="%.6g")
        v  = c3.number_input("v (m/s)", value=10.0, format="%.6g")
        dv = c4.number_input("Δv", value=0.1, min_value=0.0, format="%.6g")
        r  = c5.number_input("r (m)", value=2.0, format="%.6g")
        dr = c6.number_input("Δr", value=0.01, min_value=0.0, format="%.6g")
        f4 = lambda m_, v_, r_: m_ * v_**2 / r_
        z = f4(m, v, r)
        dF_dm = abs(f4(m+eps, v, r) - f4(m-eps, v, r)) / (2*eps)
        dF_dv = abs(f4(m, v+eps, r) - f4(m, v-eps, r)) / (2*eps)
        dF_dr = abs(f4(m, v, r+eps) - f4(m, v, r-eps)) / (2*eps)
        dz = np.sqrt((dF_dm*dm)**2 + (dF_dv*dv)**2 + (dF_dr*dr)**2)
        pct = f"{dz/z*100:.3g}%" if abs(z) > 1e-12 else "–"
        st.success(f"**Fc = {z:.4g} N ± {dz:.4g} N** (RSS)   ({pct})")

    else:
        h_planck = 6.626e-34
        c1, c2, c3, c4 = st.columns(4)
        h  = c1.number_input("h (J·s)", value=h_planck, format="%.6g")
        dh_val = c2.number_input("Δh (J·s)", value=0.0, min_value=0.0, format="%.6g")
        fq = c3.number_input("f (Hz)", value=6e14, format="%.6g")
        df = c4.number_input("Δf (Hz)", value=1e12, min_value=0.0, format="%.6g")
        E = h * fq
        dE = h*df + fq*dh_val
        st.success(f"**E = {E:.4g} J ± {dE:.4g} J  =  {E/1.6e-19:.4g} eV**")

elif formel == "Samlet usikkerhed (type A + B)":
    st.latex(r"u_c = \sqrt{u_A^2 + u_B^2}")
    st.info("Kombineret usikkerhed fra statistisk (type A) og systematisk (type B) bidrag.")
    st.divider()

    c1, c2 = st.columns(2)
    uA = c1.number_input("u_A – type A usikkerhed (statistisk)", value=0.02, min_value=0.0, format="%.6g")
    uB = c2.number_input("u_B – type B usikkerhed (systematisk, f.eks. apparaturets opløsning)", value=0.01, min_value=0.0, format="%.6g")

    uc = np.sqrt(uA**2 + uB**2)
    x_val = st.number_input("x – måleværdi (til relativ usikkerhed)", value=9.82, format="%.6g")
    rel = uc / abs(x_val) * 100 if x_val != 0 else 0

    st.success(f"**u_c = {uc:.6g}**   (relativ: {rel:.3g}%)")
    st.latex(rf"u_c = \sqrt{{u_A^2 + u_B^2}} = \sqrt{{{uA:.6g}^2 + {uB:.6g}^2}} = {uc:.6g}")

    st.markdown("---")
    st.markdown("**Type B – typiske bidrag:**")
    st.markdown("""
| Kilde | Beregning |
|-------|-----------|
| Digitalinstrument (aflæsningsopløsning d) | u_B = d / √12 ≈ 0.289·d |
| Analoginstrument (mindste skaladelvist d) | u_B = d / 2 |
| Fabrikantens specifikation (± a) | u_B = a / √3 ≈ 0.577·a |
""")

    st.markdown("**Omregner til type B:**")
    c3, c4 = st.columns(2)
    kilde = c3.radio("Kilde:", ["Digitalinstrument (opløsning d)", "Fabrikantspecifikation (± a)"], horizontal=False)
    val_in = c4.number_input("Værdi (d eller a)", value=0.01, min_value=0.0, format="%.6g")
    if "Digital" in kilde:
        uB_calc = val_in / np.sqrt(12)
        st.info(f"u_B = d/√12 = {val_in:.6g}/√12 = {uB_calc:.6g}")
    else:
        uB_calc = val_in / np.sqrt(3)
        st.info(f"u_B = a/√3 = {val_in:.6g}/√3 = {uB_calc:.6g}")

elif formel == "Potenslov-fitting:  y = A · xᵅ  (log-log regression)":
    st.latex(r"y = A \cdot x^\alpha \quad \Leftrightarrow \quad \ln y = \alpha \ln x + \ln A")
    st.markdown("Brug lineær regression på log-transformerede data til at finde eksponenten α.")
    st.markdown("**Eksempel (2025 Q3):** T ∝ k^α  →  lav log-log fit af T vs k")
    st.divider()

    st.info("💡 Paste direkte fra eksamens kode: `np.array([1.2,1.5,2.2,2.4,3.4])` — wrapperen fjernes automatisk")
    raw_x = st.text_input("x-værdier:", value="1.2, 1.5, 2.2, 2.4, 3.4",
                          help="Fx: np.array([1.2,1.5,2.2,2.4,3.4])  eller  1.2, 1.5, 2.2, 2.4, 3.4")
    raw_y = st.text_input("y-værdier:", value="2.56, 2.29, 1.89, 1.81, 1.52",
                          help="Fx: np.array([2.56,2.29,1.89,1.81,1.52])  eller  2.56, 2.29, 1.89, 1.81, 1.52")
    x_label = st.text_input("x-navn (til visning):", value="k")
    y_label = st.text_input("y-navn (til visning):", value="T")

    try:
        x_vals = parse_numpy_array(raw_x)
        y_vals = parse_numpy_array(raw_y)

        if len(x_vals) != len(y_vals):
            st.error("Antal x- og y-værdier er ikke ens.")
        elif any(x <= 0 for x in x_vals) or any(y <= 0 for y in y_vals):
            st.error("Alle værdier skal være positive (log kræver x>0, y>0).")
        else:
            log_x = np.log(x_vals)
            log_y = np.log(y_vals)
            n = len(x_vals)

            # Lineær regression på log-log: log_y = α·log_x + ln(A)
            coeffs, cov = np.polyfit(log_x, log_y, 1, cov=True)
            alpha, lnA = coeffs
            A = np.exp(lnA)
            sigma_alpha = np.sqrt(cov[0, 0])
            sigma_lnA   = np.sqrt(cov[1, 1])

            # R² for log-log fit
            log_y_fit = alpha * log_x + lnA
            ss_res = np.sum((log_y - log_y_fit)**2)
            ss_tot = np.sum((log_y - np.mean(log_y))**2)
            R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0

            st.success(f"**α = {alpha:.4g} ± {sigma_alpha:.4g}**   (A = {A:.4g},  R² = {R2:.4f})")
            st.latex(rf"{y_label} = {A:.4g} \cdot {x_label}^{{{alpha:.4g} \pm {sigma_alpha:.4g}}}")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("α (eksponent)", f"{alpha:.4g}")
            col2.metric("σ_α (usikkerhed)", f"{sigma_alpha:.4g}")
            col3.metric("A (præfaktor)", f"{A:.4g}")
            col4.metric("R² (log-log)", f"{R2:.4f}")

            with st.expander("Vis data og residualer"):
                rows = []
                for xi, yi in zip(x_vals, y_vals):
                    yi_fit = A * xi**alpha
                    rows.append({x_label: xi, y_label: yi, f"{y_label}_fit": f"{yi_fit:.4g}", "residual": f"{yi-yi_fit:.4g}"})
                st.table(rows)

            with st.expander("Vis udregning"):
                st.latex(r"\alpha = \frac{\sum \ln x_i \cdot \ln y_i - n\overline{\ln x}\,\overline{\ln y}}{\sum (\ln x_i)^2 - n(\overline{\ln x})^2}")
                st.latex(rf"\alpha = {alpha:.6g},\quad \ln A = {lnA:.6g},\quad A = e^{{{lnA:.6g}}} = {A:.6g}")
    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")

elif formel == "Lineær regression:  y = a · x + b":
    st.latex(r"y = a \cdot x + b \qquad a = \frac{\sum(x_i-\bar{x})(y_i-\bar{y})}{\sum(x_i-\bar{x})^2} \qquad b = \bar{y} - a\bar{x}")
    st.markdown("Mindste kvadraters metode – lineær sammenhæng. Brug **Potenslov-fitting** til T ∝ k^α.")
    st.divider()

    col_x, col_y = st.columns(2)
    x_label = col_x.text_input("Navn på x", value="x")
    y_label = col_y.text_input("Navn på y", value="y")

    raw_x = st.text_input("x-værdier:", value="1.0, 2.0, 3.0, 4.0, 5.0",
                          help="Fx: np.array([1.0,2.0,3.0])  eller  1.0, 2.0, 3.0")
    raw_y = st.text_input("y-værdier:", value="2.1, 3.9, 6.2, 7.8, 10.1",
                          help="Fx: np.array([2.1,3.9,6.2])  eller  2.1, 3.9, 6.2")

    try:
        x_vals = parse_numpy_array(raw_x)
        y_vals = parse_numpy_array(raw_y)

        if len(x_vals) != len(y_vals):
            st.error(f"Antal x-værdier ({len(x_vals)}) ≠ antal y-værdier ({len(y_vals)})")
        elif len(x_vals) < 2:
            st.error("Minimum 2 datapunkter kræves.")
        else:
            n = len(x_vals)
            x_mean = np.mean(x_vals)
            y_mean = np.mean(y_vals)
            Sxx = np.sum((x_vals - x_mean)**2)
            Sxy = np.sum((x_vals - x_mean) * (y_vals - y_mean))
            a_coef = Sxy / Sxx
            b_coef = y_mean - a_coef * x_mean

            y_fit = a_coef * x_vals + b_coef
            ss_res = np.sum((y_vals - y_fit)**2)
            ss_tot = np.sum((y_vals - y_mean)**2)
            R2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0

            if n > 2:
                s2 = ss_res / (n - 2)
                sigma_a = np.sqrt(s2 / Sxx)
                sigma_b = np.sqrt(s2 * (1/n + x_mean**2/Sxx))
            else:
                sigma_a = sigma_b = float("nan")

            st.success(f"**a = {a_coef:.4g} ± {sigma_a:.4g}**   |   **b = {b_coef:.4g} ± {sigma_b:.4g}**   |   **R² = {R2:.4f}**")
            st.latex(rf"{y_label} = {a_coef:.4g} \cdot {x_label} + ({b_coef:.4g})")

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Hældning a", f"{a_coef:.4g}")
            col2.metric("σ_a", f"{sigma_a:.4g}")
            col3.metric("Skæring b", f"{b_coef:.4g}")
            col4.metric("R²", f"{R2:.4f}")

            if R2 > 0.99:
                st.info("R² > 0.99 – meget godt lineært fit.")
            elif R2 < 0.90:
                st.warning("R² < 0.90 – overvej om sammenhængen er lineær, eller prøv Potenslov-fitting.")

            with st.expander("Vis data og residualer"):
                rows = []
                for xi, yi in zip(x_vals, y_vals):
                    yi_fit_val = a_coef * xi + b_coef
                    rows.append({x_label: xi, y_label: yi,
                                  f"{y_label}_fit": f"{yi_fit_val:.4g}",
                                  "residual": f"{yi - yi_fit_val:.4g}"})
                st.table(rows)

            with st.expander("Forudsig y for en given x"):
                x_pred = st.number_input("x-værdi:", value=float(np.mean(x_vals)), format="%.6g",
                                          key="linreg_pred_x")
                y_pred = a_coef * x_pred + b_coef
                st.success(f"**{y_label}({x_pred:.4g}) = {y_pred:.6g}**")

    except ValueError:
        st.error("Ugyldig input – brug kommaseparerede tal.")
