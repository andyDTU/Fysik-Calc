import streamlit as st
import numpy as np

st.set_page_config(page_title="Usikkerhed", page_icon="📏", layout="wide")
st.title("📏 Usikkerhed & Fejlanalyse")
st.markdown("Måleusikkerhed, fejlpropagation og statistik — Lecture 3 (10060)")
st.divider()

formel = st.selectbox("Vælg beregning", [
    "Gennemsnit og standardafvigelse",
    "Standardmåleusikkerhed (type A)",
    "Relativ og absolut usikkerhed",
    "Fejlpropagation – addition/subtraktion",
    "Fejlpropagation – multiplikation/division",
    "Fejlpropagation – potens:  z = xⁿ",
    "Fejlpropagation – generel formel",
    "Samlet usikkerhed (type A + B)",
])

st.divider()

if formel == "Gennemsnit og standardafvigelse":
    st.latex(r"\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i \qquad s = \sqrt{\frac{\sum(x_i - \bar{x})^2}{n-1}}")
    st.markdown("Indtast måleværdier kommasepareret, f.eks. `9.81, 9.79, 9.83, 9.80`")
    st.divider()

    raw = st.text_input("Måleværdier:", value="9.81, 9.79, 9.83, 9.80, 9.82")
    try:
        vals = np.array([float(x.strip()) for x in raw.split(",") if x.strip()])
        n = len(vals)
        mean = np.mean(vals)
        std  = np.std(vals, ddof=1)
        sem  = std / np.sqrt(n)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("n – antal målinger", n)
        col2.metric("x̄ – gennemsnit", f"{mean:.6g}")
        col3.metric("s – std.afvigelse", f"{std:.4g}")
        col4.metric("u(x̄) – std.usikkerhed", f"{sem:.4g}")

        st.success(f"**Resultat: x̄ = {mean:.6g} ± {sem:.4g}**   (relativ usikkerhed: {sem/mean*100:.3g}%)")

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
    st.latex(r"z = x \pm y \implies \Delta z = \Delta x + \Delta y")
    st.info("Absolutte usikkerheder adderes altid ved addition og subtraktion.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        x  = st.number_input("x", value=10.0, format="%.6g")
        dx = st.number_input("Δx", value=0.1, min_value=0.0, format="%.6g")
    with c2:
        y  = st.number_input("y", value=5.0, format="%.6g")
        dy = st.number_input("Δy", value=0.05, min_value=0.0, format="%.6g")

    op = st.radio("Operation:", ["x + y", "x − y"], horizontal=True)
    z = x + y if op == "x + y" else x - y
    dz = dx + dy
    rel = dz / abs(z) * 100 if z != 0 else float('inf')

    st.success(f"**z = {z:.6g} ± {dz:.6g}**   (relativ: {rel:.3g}%)")
    if op == "x + y":
        st.latex(rf"z = {x:.6g} + {y:.6g} = {z:.6g}")
    else:
        st.latex(rf"z = {x:.6g} - {y:.6g} = {z:.6g}")
    st.latex(rf"\Delta z = \Delta x + \Delta y = {dx:.6g} + {dy:.6g} = {dz:.6g}")

elif formel == "Fejlpropagation – multiplikation/division":
    st.latex(r"z = x \cdot y \text{ eller } z = \frac{x}{y} \implies \frac{\Delta z}{|z|} = \frac{\Delta x}{|x|} + \frac{\Delta y}{|y|}")
    st.info("Relative usikkerheder adderes ved multiplikation og division.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        x  = st.number_input("x", value=10.0, format="%.6g")
        dx = st.number_input("Δx", value=0.1, min_value=0.0, format="%.6g")
    with c2:
        y  = st.number_input("y", value=5.0, format="%.6g")
        dy = st.number_input("Δy", value=0.1, min_value=0.0, format="%.6g")

    op = st.radio("Operation:", ["x · y", "x / y"], horizontal=True)
    if op == "x · y":
        z = x * y
    else:
        if abs(y) < 1e-12:
            st.error("y = 0")
            st.stop()
        z = x / y

    rel_x = dx / abs(x) if x != 0 else 0
    rel_y = dy / abs(y) if y != 0 else 0
    rel_z = rel_x + rel_y
    dz = rel_z * abs(z)

    st.success(f"**z = {z:.6g} ± {dz:.6g}**   (relativ: {rel_z*100:.3g}%)")
    st.latex(rf"\frac{{\Delta z}}{{|z|}} = \frac{{\Delta x}}{{|x|}} + \frac{{\Delta y}}{{|y|}} = \frac{{{dx:.6g}}}{{{abs(x):.6g}}} + \frac{{{dy:.6g}}}{{{abs(y):.6g}}} = {rel_z:.4g}")
    st.latex(rf"\Delta z = {rel_z:.4g} \cdot |z| = {rel_z:.4g} \cdot {abs(z):.6g} = {dz:.4g}")

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

elif formel == "Fejlpropagation – generel formel":
    st.latex(r"\Delta z = \left|\frac{\partial z}{\partial x}\right|\Delta x + \left|\frac{\partial z}{\partial y}\right|\Delta y + \cdots")
    st.markdown("Beregn usikkerhed ved en vilkårlig funktion ved numerisk differentiering.")
    st.divider()

    st.markdown("**Eksempel: z = ½mv²**")

    c1, c2, c3, c4 = st.columns(4)
    m  = c1.number_input("m (kg)", value=2.0, format="%.6g")
    dm = c2.number_input("Δm (kg)", value=0.01, min_value=0.0, format="%.6g")
    v  = c3.number_input("v (m/s)", value=10.0, format="%.6g")
    dv = c4.number_input("Δv (m/s)", value=0.1, min_value=0.0, format="%.6g")

    z = 0.5 * m * v**2
    dz_dm = 0.5 * v**2
    dz_dv = m * v
    dz = abs(dz_dm) * dm + abs(dz_dv) * dv

    st.success(f"**E_k = {z:.6g} J ± {dz:.4g} J**   (relativ: {dz/z*100:.3g}%)")
    with st.expander("Vis udregning"):
        st.latex(rf"z = \frac{{1}}{{2}} m v^2 = \frac{{1}}{{2}} \cdot {m:.6g} \cdot {v:.6g}^2 = {z:.6g}\ \text{{J}}")
        st.latex(rf"\frac{{\partial z}}{{\partial m}} = \frac{{1}}{{2}}v^2 = {dz_dm:.6g}")
        st.latex(rf"\frac{{\partial z}}{{\partial v}} = m v = {dz_dv:.6g}")
        st.latex(rf"\Delta z = {dz_dm:.6g} \cdot {dm:.6g} + {dz_dv:.6g} \cdot {dv:.6g} = {dz:.4g}\ \text{{J}}")

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
