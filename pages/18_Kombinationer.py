import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, breadcrumb

st.set_page_config(page_title="Kombinationsopgaver", page_icon="🔗", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("🔗", "Kombinationsopgaver")
st.title("🔗 Kombinationsopgaver")
st.markdown("Opgaver der kræver **to eller flere trin** — de sværeste opgavetyper på DTU 10060.")
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "⚡ Energi + Kinematik",
    "🔄 Rotation + Energi",
    "🌡️ Gas + Termodynamik",
    "💥 Kollision + Energi",
    "🏃 Kinematik + Usikkerhed",
])

with tab1:
    st.subheader("Opgave 1: Bremseafstand")

    with st.container(border=True):
        st.markdown("""
**En bil (m = 1200 kg) kører 90 km/h og bremser til stop på tør asfalt med friktionskoefficient μ = 0.7.
Find bremseafstanden.**

- Startbetingelse: v₀ = 90 km/h, v = 0
- Friktionskoefficient: μ = 0.7
- g = 9.82 m/s²
""")

    with st.expander("Vis løsning – trin for trin"):
        st.markdown("**Trin 1: Omregn hastighed til SI-enheder**")
        st.latex(r"v_0 = 90 \, \frac{\text{km}}{\text{h}} = \frac{90 \times 1000}{3600} \, \frac{\text{m}}{\text{s}} = 25 \, \text{m/s}")
        v0 = 90 * 1000 / 3600
        st.markdown(f"→ v₀ = {v0:.2f} m/s")

        st.markdown("**Trin 2: Bremseacceleration fra friktion**")
        st.latex(r"a = \mu g = 0.7 \times 9.82 = 6.874 \, \text{m/s}^2")
        mu = 0.7
        g = 9.82
        a = mu * g
        st.markdown(f"→ a = {a:.3f} m/s²")

        st.markdown("**Trin 3: SUVAT — find bremseafstand**")
        st.latex(r"v^2 = v_0^2 + 2as \quad \Rightarrow \quad s = \frac{v_0^2}{2a} \quad \text{(da } v = 0\text{)}")
        s = v0**2 / (2 * a)
        st.latex(r"s = \frac{(25)^2}{2 \times 6.874} = \frac{625}{13.748} = " + f"{s:.1f}" + r" \, \text{m}")

        st.success(f"Bremseafstand: s = {s:.1f} m")
        st.warning("Fælde: Glem aldrig at omregne km/h → m/s (del med 3.6). Forkert enhed giver forkert svar med faktor 3.6² ≈ 13.")

    st.divider()

    st.subheader("Opgave 2: Vandret kast fra klippe")

    with st.container(border=True):
        st.markdown("""
**En kugle kastes vandret fra en 50 m høj klippe med starthastighed v₀ = 20 m/s.
Find kuglens samlede hastighed i det øjeblik den rammer jorden.**

- h = 50 m
- v₀ₓ = 20 m/s (vandret, konstant)
- g = 9.82 m/s²
""")

    with st.expander("Vis løsning – trin for trin"):
        st.markdown("**Trin 1: Find flyvetid fra frit fald**")
        st.latex(r"h = \frac{1}{2}g t^2 \quad \Rightarrow \quad t = \sqrt{\frac{2h}{g}}")
        h = 50.0
        g = 9.82
        t = np.sqrt(2 * h / g)
        st.latex(r"t = \sqrt{\frac{2 \times 50}{9.82}} = \sqrt{" + f"{2*h/g:.4f}" + r"} = " + f"{t:.3f}" + r" \, \text{s}")

        st.markdown("**Trin 2: Beregn hastighedskomponenter ved landing**")
        st.latex(r"v_x = v_0 = 20 \, \text{m/s} \quad \text{(ingen vandret acceleration)}")
        vx = 20.0
        vy = g * t
        st.latex(r"v_y = g \cdot t = 9.82 \times " + f"{t:.3f}" + r" = " + f"{vy:.2f}" + r" \, \text{m/s}")

        st.markdown("**Trin 3: Samlet hastighed via Pythagoras**")
        st.latex(r"v_{\text{total}} = \sqrt{v_x^2 + v_y^2}")
        v_total = np.sqrt(vx**2 + vy**2)
        st.latex(
            r"v_{\text{total}} = \sqrt{(" + f"{vx:.1f}" + r")^2 + (" + f"{vy:.2f}" + r")^2} = \sqrt{"
            + f"{vx**2:.1f}" + r" + " + f"{vy**2:.2f}" + r"} = " + f"{v_total:.2f}" + r" \, \text{m/s}"
        )

        st.success(f"Slutfart: v_total = {v_total:.2f} m/s")
        st.warning("Fælde: v_y alene er IKKE slutfarten — den vandrette komponent v_x = 20 m/s skal inkluderes i Pythagoras-summen.")

with tab2:
    st.subheader("Opgave 1: Cylinder ruller ned ad skråning")

    with st.container(border=True):
        st.markdown("""
**En massiv cylinder (m = 5 kg, r = 0.2 m) ruller uden glidning ned ad en 30° skråning
fra en højde h = 2 m. Find cylinderens hastighed i bunden.**

- Inertimoment for massiv cylinder: I = ½mr²
- Rulningsbetingelse: ω = v/r
- g = 9.82 m/s²
""")

    with st.expander("Vis løsning – trin for trin"):
        st.markdown("**Trin 1: Opstil energibevarelsesligningen**")
        st.latex(r"mgh = \frac{1}{2}mv^2 + \frac{1}{2}I\omega^2")

        st.markdown("**Trin 2: Indsæt I = ½mr² og ω = v/r**")
        st.latex(r"\frac{1}{2}I\omega^2 = \frac{1}{2} \cdot \frac{1}{2}mr^2 \cdot \frac{v^2}{r^2} = \frac{1}{4}mv^2")
        st.latex(r"mgh = \frac{1}{2}mv^2 + \frac{1}{4}mv^2 = \frac{3}{4}mv^2")

        st.markdown("**Trin 3: Løs for v**")
        st.latex(r"v = \sqrt{\frac{4gh}{3}}")
        g = 9.82
        h = 2.0
        v_ruller = np.sqrt(4 * g * h / 3)
        v_glider = np.sqrt(2 * g * h)
        st.latex(r"v = \sqrt{\frac{4 \times 9.82 \times 2}{3}} = \sqrt{" + f"{4*g*h/3:.4f}" + r"} = " + f"{v_ruller:.3f}" + r" \, \text{m/s}")

        st.success(f"Rulningshastighed: v = {v_ruller:.3f} m/s")
        st.info(
            f"Sammenligning: Hvis cylinderen i stedet glidede (ingen rotation) ville v = √(2gh) = {v_glider:.3f} m/s. "
            "Rulning er langsommere fordi noget af energien lagres som rotationsenergi."
        )
        st.warning("Fælde: Glemmer man rotationsenergien ½Iω², overestimerer man hastigheden med en faktor √(4/3) ≈ 1.15.")

    st.divider()

    st.subheader("Opgave 2: Svinghjul bremser")

    with st.container(border=True):
        st.markdown("""
**Et svinghjul med inertimoment I = 2 kg·m² roterer med 1000 RPM.
En bremsekraft F = 50 N virker tangentielt på radius r = 0.3 m.
Find den tid det tager at bringe hjulet til stop.**

- I = 2 kg·m²
- n = 1000 RPM
- F = 50 N, r = 0.3 m
""")

    with st.expander("Vis løsning – trin for trin"):
        st.markdown("**Trin 1: Omregn RPM → rad/s**")
        st.latex(r"\omega_0 = \frac{2\pi n}{60} = \frac{2\pi \times 1000}{60}")
        omega0 = 2 * np.pi * 1000 / 60
        st.latex(r"\omega_0 = " + f"{omega0:.3f}" + r" \, \text{rad/s}")

        st.markdown("**Trin 2: Beregn bremsemomentet**")
        F = 50.0
        r = 0.3
        tau = F * r
        st.latex(r"\tau = F \cdot r = 50 \times 0.3 = " + f"{tau:.1f}" + r" \, \text{N·m}")

        st.markdown("**Trin 3: Find vinkelacceleration (decelererende)**")
        I = 2.0
        alpha = tau / I
        st.latex(r"\alpha = \frac{\tau}{I} = \frac{" + f"{tau:.1f}" + r"}{" + f"{I:.1f}" + r"} = " + f"{alpha:.2f}" + r" \, \text{rad/s}^2")

        st.markdown("**Trin 4: Find stoptid**")
        st.latex(r"\omega = \omega_0 - \alpha t = 0 \quad \Rightarrow \quad t = \frac{\omega_0}{\alpha}")
        t_stop = omega0 / alpha
        st.latex(r"t = \frac{" + f"{omega0:.3f}" + r"}{" + f"{alpha:.2f}" + r"} = " + f"{t_stop:.3f}" + r" \, \text{s}")

        st.success(f"Stoptid: t = {t_stop:.3f} s ≈ {t_stop:.1f} s")
        st.warning("Fælde: RPM skal omregnes til rad/s ved at gange med 2π/60, ikke blot dividere med 60.")

with tab3:
    st.subheader("Opgave 1: Isobar opvarmning af idealgas")

    with st.container(border=True):
        st.markdown("""
**1 mol idealgas opvarmes isobart (konstant tryk) fra T₁ = 300 K til T₂ = 600 K
ved tryk p = 2 atm. Find volumenændringen og det udførte arbejde.**

- n = 1 mol, R = 8.314 J/(mol·K)
- T₁ = 300 K, T₂ = 600 K
- p = 2 atm = 2 × 101325 Pa
""")

    with st.expander("Vis løsning – trin for trin"):
        R = 8.314
        n = 1.0
        T1 = 300.0
        T2 = 600.0
        p_atm = 2.0
        p_Pa = p_atm * 101325

        st.markdown("**Trin 1: Find startvolumen via idealgas-loven**")
        st.latex(r"pV_1 = nRT_1 \quad \Rightarrow \quad V_1 = \frac{nRT_1}{p}")
        V1 = n * R * T1 / p_Pa
        st.latex(
            r"V_1 = \frac{1 \times 8.314 \times 300}{2 \times 101325} = \frac{2494.2}{202650} = "
            + f"{V1:.5f}" + r" \, \text{m}^3"
        )

        st.markdown("**Trin 2: Find slutvolumen — ved isobar proces fordobles V med T**")
        V2 = n * R * T2 / p_Pa
        st.latex(r"V_2 = \frac{nRT_2}{p} = \frac{1 \times 8.314 \times 600}{2 \times 101325} = " + f"{V2:.5f}" + r" \, \text{m}^3")
        st.latex(r"\Delta V = V_2 - V_1 = " + f"{V2-V1:.5f}" + r" \, \text{m}^3")

        st.markdown("**Trin 3: Udført arbejde ved isobar proces**")
        W = p_Pa * (V2 - V1)
        W_check = n * R * (T2 - T1)
        st.latex(r"W = p \cdot \Delta V = " + f"{p_Pa:.0f}" + r" \times " + f"{V2-V1:.5f}" + r" = " + f"{W:.1f}" + r" \, \text{J}")
        st.latex(r"\text{Tjek: } W = nR\Delta T = 1 \times 8.314 \times 300 = " + f"{W_check:.1f}" + r" \, \text{J} \checkmark")

        st.success(f"ΔV = {V2-V1:.5f} m³,  W = {W:.1f} J ≈ {W:.0f} J")
        st.warning("Fælde: Glem ikke at konvertere atm → Pa (gang med 101325). Regner du med atm i stedet for Pa, får du W i enheder af atm·m³, ikke joule.")

    st.divider()

    st.subheader("Opgave 2: Adiabatisk kompression")

    with st.container(border=True):
        st.markdown("""
**En gas (γ = 1.4) komprimeres adiabatisk fra V₁ = 10 L, p₁ = 1 atm
til V₂ = 2 L. T₁ = 300 K. Find p₂ og T₂.**

- γ = 1.4 (diatomisk idealgas, fx luft)
- V₁ = 10 L, V₂ = 2 L (brug ratio direkte)
""")

    with st.expander("Vis løsning – trin for trin"):
        gamma = 1.4
        V1 = 10.0
        V2 = 2.0
        p1 = 1.0
        T1 = 300.0
        ratio = V1 / V2

        st.markdown("**Trin 1: Find p₂ via adiabatisk relation**")
        st.latex(r"p_1 V_1^{\gamma} = p_2 V_2^{\gamma} \quad \Rightarrow \quad p_2 = p_1 \left(\frac{V_1}{V_2}\right)^{\gamma}")
        p2 = p1 * ratio**gamma
        st.latex(
            r"p_2 = 1 \cdot \left(\frac{10}{2}\right)^{1.4} = 5^{1.4} = "
            + f"{p2:.4f}" + r" \, \text{atm}"
        )

        st.markdown("**Trin 2: Find T₂ via adiabatisk temperaturrelation**")
        st.latex(r"T_2 = T_1 \left(\frac{V_1}{V_2}\right)^{\gamma - 1}")
        T2 = T1 * ratio**(gamma - 1)
        st.latex(
            r"T_2 = 300 \cdot 5^{0.4} = 300 \times "
            + f"{ratio**(gamma-1):.4f}" + r" = " + f"{T2:.1f}" + r" \, \text{K}"
        )

        st.success(f"p₂ = {p2:.3f} atm,  T₂ = {T2:.1f} K")
        st.warning(
            "Fælde: I temperaturformlen bruges eksponenten γ−1 = 0.4, IKKE γ = 1.4. "
            "Bruger man γ i stedet for γ−1, overestimerer man temperaturen kraftigt."
        )

with tab4:
    st.subheader("Opgave 1: Kollision med restitutionskoefficient")

    with st.container(border=True):
        st.markdown("""
**En kugle (m = 0.5 kg) bevæger sig med v₁ = 8 m/s og rammer en stationær klods (M = 2 kg)
centralt. Restitutionskoefficient e = 0.6.
Find hastighederne efter kollisionen og det kinetiske energitab.**

- m = 0.5 kg, M = 2 kg
- v₁ = 8 m/s (kugle), V₁ = 0 (klods stationær)
- e = 0.6
""")

    with st.expander("Vis løsning – trin for trin"):
        m = 0.5
        M = 2.0
        v1 = 8.0
        e = 0.6

        st.markdown("**Trin 1: Opstil impulsbevarelse**")
        st.latex(r"mv_1 = mv_1' + MV_2'")
        st.latex(r"0.5 \times 8 = 0.5 \, v_1' + 2 \, V_2' \quad \Rightarrow \quad 4 = 0.5 \, v_1' + 2 \, V_2'")

        st.markdown("**Trin 2: Restitutionsbetingelse**")
        st.latex(r"e = \frac{V_2' - v_1'}{v_1 - 0} \quad \Rightarrow \quad V_2' - v_1' = e \cdot v_1 = 0.6 \times 8 = 4.8 \, \text{m/s}")

        st.markdown("**Trin 3: Løs ligningssystemet**")
        st.latex(r"V_2' = \frac{(1+e) m \, v_1}{m + M}, \qquad v_1' = \frac{(m - eM) v_1}{m + M}")
        V2_prime = (1 + e) * m * v1 / (m + M)
        v1_prime = (m - e * M) * v1 / (m + M)
        st.latex(
            r"V_2' = \frac{(1 + 0.6) \times 0.5 \times 8}{0.5 + 2} = \frac{"
            + f"{(1+e)*m*v1:.2f}" + r"}{2.5} = " + f"{V2_prime:.3f}" + r" \, \text{m/s}"
        )
        st.latex(
            r"v_1' = \frac{(0.5 - 0.6 \times 2) \times 8}{2.5} = \frac{"
            + f"{(m - e*M)*v1:.2f}" + r"}{2.5} = " + f"{v1_prime:.3f}" + r" \, \text{m/s}"
        )

        st.markdown("**Trin 4: Kinetisk energitab**")
        st.latex(r"\Delta E_k = \frac{1}{2}mv_1^2 - \frac{1}{2}mv_1'^2 - \frac{1}{2}MV_2'^2")
        Ek_before = 0.5 * m * v1**2
        Ek_after = 0.5 * m * v1_prime**2 + 0.5 * M * V2_prime**2
        delta_Ek = Ek_before - Ek_after
        st.latex(
            r"\Delta E_k = \frac{1}{2}(0.5)(8)^2 - \frac{1}{2}(0.5)("
            + f"{v1_prime:.3f}" + r")^2 - \frac{1}{2}(2)(" + f"{V2_prime:.3f}" + r")^2 = "
            + f"{delta_Ek:.3f}" + r" \, \text{J}"
        )

        st.success(
            f"v₁' = {v1_prime:.3f} m/s (kugle),  "
            f"V₂' = {V2_prime:.3f} m/s (klods),  "
            f"ΔEk = {delta_Ek:.3f} J tabt"
        )
        st.warning(
            "Fælde: Restitutionskoefficienten defineres som (relativ separationshastighed)/(relativ tilnærmelseshastighed). "
            "Fortegnene skal være konsekvente — opstil altid impulsbevarelse og restitutionsbetingelse som to separate ligninger."
        )

    st.divider()

    st.subheader("Opgave 2: Ballistic pendulum")

    with st.container(border=True):
        st.markdown("""
**I et ballistic pendulum-forsøg skydes en kugle (m = 10 g) ind i en stationær klods (M = 990 g).
Systemet svinger op til en højde h = 12.5 cm. Find kuglens starthastighed v₀.**

- m = 10 g = 0.010 kg
- M = 990 g = 0.990 kg
- h = 12.5 cm = 0.125 m
- g = 9.82 m/s²
""")

    with st.expander("Vis løsning – trin for trin"):
        m = 0.010
        M = 0.990
        h = 0.125
        g = 9.82

        st.markdown("**Trin 1: Find fælles hastighed efter uelastisk kollision via energibevarelse (svingning)**")
        st.latex(r"\frac{1}{2}(m + M)v'^2 = (m + M)gh \quad \Rightarrow \quad v' = \sqrt{2gh}")
        v_prime = np.sqrt(2 * g * h)
        st.latex(r"v' = \sqrt{2 \times 9.82 \times 0.125} = \sqrt{" + f"{2*g*h:.4f}" + r"} = " + f"{v_prime:.4f}" + r" \, \text{m/s}")

        st.markdown("**Trin 2: Brug impulsbevarelse under selve kollisionen for at finde v₀**")
        st.latex(r"m v_0 = (m + M) v' \quad \Rightarrow \quad v_0 = \frac{(m + M) \, v'}{m}")
        v0 = (m + M) * v_prime / m
        st.latex(
            r"v_0 = \frac{(0.010 + 0.990) \times " + f"{v_prime:.4f}" + r"}{0.010}"
            + r" = \frac{1.000 \times " + f"{v_prime:.4f}" + r"}{0.010} = " + f"{v0:.2f}" + r" \, \text{m/s}"
        )

        st.success(f"Kuglens starthastighed: v₀ = {v0:.2f} m/s")
        st.info(
            "Metoden bruger to forskellige bevaringslove i to separate faser: "
            "(1) Under kollisionen bruges kun impulsbevarelse (energi er IKKE bevaret — uelastisk). "
            "(2) Under svingningen bruges kun energibevarelse (impuls er IKKE bevaret — pendultov giver ekstern kraft)."
        )
        st.warning("Fælde: Man må IKKE bruge energibevarelse direkte fra kugle til toppunkt — noget energi omsættes til varme i selve kollisionen.")

with tab5:
    st.subheader("Opgave 1: Flyvetid med fejlpropagation")

    with st.container(border=True):
        st.markdown("""
**En bold kastes lodret op fra højden h₀ = 1.60 ± 0.05 m med starthastighed v₀ = 4.20 ± 0.10 m/s.
Tyngdeaccelerationen er g = 9.82 ± 0.01 m/s².
Find boldens flyvetid t ± δt (tid fra kast til den rammer jorden).**

- h₀ = 1.60 ± 0.05 m
- v₀ = 4.20 ± 0.10 m/s (opad positiv)
- g = 9.82 ± 0.01 m/s²
""")

    with st.expander("Vis løsning – trin for trin"):
        h0 = 1.60
        v0_val = 4.20
        g = 9.82
        dh0 = 0.05
        dv0 = 0.10
        dg = 0.01

        st.markdown("**Trin 1: Find flyvetiden fra kinematik (lodret bevægelse, nedad positiv y-akse)**")
        st.latex(r"h_0 + v_0 t - \frac{1}{2}g t^2 = 0 \quad \Rightarrow \quad t = \frac{v_0 + \sqrt{v_0^2 + 2gh_0}}{g}")

        D = np.sqrt(v0_val**2 + 2 * g * h0)
        t = (v0_val + D) / g
        st.latex(
            r"D \equiv \sqrt{v_0^2 + 2gh_0} = \sqrt{" + f"{v0_val}^2 + 2 \\times {g} \\times {h0}" + r"} = \sqrt{"
            + f"{v0_val**2 + 2*g*h0:.4f}" + r"} = " + f"{D:.4f}" + r" \, \text{m/s}"
        )
        st.latex(r"t = \frac{" + f"{v0_val} + {D:.4f}" + r"}{" + f"{g}" + r"} = " + f"{t:.4f}" + r" \, \text{s}")

        st.markdown("**Trin 2: Beregn partielle afledede for fejlpropagation**")

        st.latex(r"\frac{\partial t}{\partial h_0} = \frac{g}{D \cdot g} = \frac{1}{D}")
        dt_dh0 = 1.0 / D
        st.latex(r"\frac{\partial t}{\partial h_0} = \frac{1}{" + f"{D:.4f}" + r"} = " + f"{dt_dh0:.5f}")

        st.latex(r"\frac{\partial t}{\partial v_0} = \frac{1}{g}\left(1 + \frac{v_0}{D}\right) = \frac{D + v_0}{gD}")
        dt_dv0 = (D + v0_val) / (g * D)
        st.latex(
            r"\frac{\partial t}{\partial v_0} = \frac{" + f"{D:.4f} + {v0_val}" + r"}{" + f"{g} \\times {D:.4f}" + r"} = "
            + f"{dt_dv0:.5f}"
        )

        st.latex(r"\frac{\partial t}{\partial g} = -\frac{v_0 D + v_0^2 + g h_0}{g^2 D}")
        dt_dg = -(v0_val * D + v0_val**2 + g * h0) / (g**2 * D)
        st.latex(r"\frac{\partial t}{\partial g} = " + f"{dt_dg:.5f}" + r" \, \text{s}^2/\text{m}")

        st.markdown("**Trin 3: Samlet usikkerhed via kvadratisk fejlpropagation**")
        st.latex(
            r"\delta t = \sqrt{\left(\frac{\partial t}{\partial h_0} \delta h_0\right)^2"
            r"+ \left(\frac{\partial t}{\partial v_0} \delta v_0\right)^2"
            r"+ \left(\frac{\partial t}{\partial g} \delta g\right)^2}"
        )

        term_h0 = (dt_dh0 * dh0)**2
        term_v0 = (dt_dv0 * dv0)**2
        term_g  = (dt_dg  * dg )**2
        delta_t = np.sqrt(term_h0 + term_v0 + term_g)

        st.latex(
            r"\delta t = \sqrt{("
            + f"{dt_dh0:.5f}" + r" \times " + f"{dh0}" + r")^2 + ("
            + f"{dt_dv0:.5f}" + r" \times " + f"{dv0}" + r")^2 + ("
            + f"{abs(dt_dg):.5f}" + r" \times " + f"{dg}" + r")^2}"
        )
        st.latex(
            r"\delta t = \sqrt{" + f"{term_h0:.6f}" + r" + " + f"{term_v0:.6f}" + r" + " + f"{term_g:.8f}" + r"}"
            + r" = " + f"{delta_t:.4f}" + r" \, \text{s}"
        )

        st.success(f"t = {t:.3f} ± {delta_t:.3f} s")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Bidrag fra δh₀", f"{np.sqrt(term_h0)*1000:.2f} ms")
        with col2:
            st.metric("Bidrag fra δv₀", f"{np.sqrt(term_v0)*1000:.2f} ms")
        with col3:
            st.metric("Bidrag fra δg", f"{np.sqrt(term_g)*1000:.2f} ms")

        st.warning(
            "Fælde: De partielle bidrag skal KVADRERES inden summering og rod trækkes til sidst. "
            "En hyppig fejl er at summere de absolutte bidrag direkte, hvilket overvurderer usikkerheden "
            "(medmindre bidragene er 100% korrelerede)."
        )
