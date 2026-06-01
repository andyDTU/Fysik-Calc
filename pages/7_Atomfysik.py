import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, show_tips, formula_card_grid

st.set_page_config(page_title="Atomfysik & Kvantemekanik", page_icon="☢️", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
st.title("☢️ Atomfysik & Kvantemekanik")
st.markdown("Radioaktivitet, energi-masse-ækvivalens, fotoner og Bohrs model")
st.divider()

h   = 6.626e-34   # Plancks konstant (J·s)
c   = 2.998e8     # lyshastighed (m/s)
eV  = 1.602e-19   # 1 eV i joule
m_e = 9.109e-31   # elektronmasse (kg)
u   = 1.661e-27   # atommasseenhed (kg)
ln2 = np.log(2)

_ATOM_FORMULAS = [
    ("Radioaktivt henfald",  "N = N₀·e^(−λt)",               "Radioaktivt henfald:  N = N₀ · e^(−λt)"),
    ("Aktivitet",            "A = λ · N",                     "Aktivitet:  A = λ · N"),
    ("Halvvejstid",          "T½ = ln(2)/λ",                  "Halvvejstid:  T½ = ln(2) / λ"),
    ("Energi–masse",         "E = Δm·c²",                    "Energi-masse:  E = Δm · c²"),
    ("Fotonenergí",          "E = h·f = hc/λ",               "Fotonenergí:  E = h · f = h·c / λ"),
    ("de Broglie",           "λ = h/(m·v)",                   "de Broglie bølgelængde:  λ = h / (m·v)"),
    ("Bohrs model",          "En = −13.6 eV/n²",             "Bohrs model – hydrogenspektret"),
    ("Fotoelektrisk effekt", "Ek = hf − φ",                  "Fotoelektrisk effekt"),
    ("Compton-spredning",    "Δλ = (h/mₑc)(1−cosθ)",         "Compton-spredning"),
]
formel = formula_card_grid(_ATOM_FORMULAS, "atom_formel")

ATOM_TIPS = {
    "Radioaktivt henfald:  N = N₀ · e^(−λt)": "λ = ln(2)/T½. N(t) = N₀·e^(−λt). Aktivitet A = λN. Enheder: Bq = henfald/s.",
    "Halvvejstid:  T½ = ln(2) / λ": "T½ = ln(2)/λ ≈ 0.693/λ. Efter n halvtider: N = N₀·(½)ⁿ.",
    "Energi-masse:  E = Δm · c²": "Δm i kg, c = 3×10⁸ m/s. 1 u = 931.5 MeV/c². Bruges til binding­senergi og kernereaktioner.",
    "Fotonenergí:  E = h · f = h·c / λ": "E = hf = hc/λ. h = 6.626×10⁻³⁴ J·s. 1 eV = 1.602×10⁻¹⁹ J.",
    "de Broglie bølgelængde:  λ = h / (m·v)": "λ = h/(mv) = h/p. Partikler viser bølgeegenskaber. Gælder for elektroner, neutroner, etc.",
    "Fotoelektrisk effekt": "E_k = hf − φ. φ = arbejdsfunktion (J eller eV). Ingen elektroner hvis f < f_grænse.",
    "Bohrs model – hydrogenspektret": "E_n = −13.6 eV/n². Foton udsendes: ΔE = hf = E_i − E_f. n=1 er grundtilstand.",
}
show_tips(formel, ATOM_TIPS)
st.divider()

if formel == "Radioaktivt henfald:  N = N₀ · e^(−λt)":
    st.latex(r"N(t) = N_0 \cdot e^{-\lambda t}")
    beregn = st.radio("Beregn:", ["N(t) – antal kerner til tid t", "N₀ – startantal", "λ – henfalds­konstant (s⁻¹)", "t – tid (s)"], horizontal=True)
    st.divider()

    if beregn == "N(t) – antal kerner til tid t":
        c1, c2, c3 = st.columns(3)
        N0  = c1.number_input("N₀ – startantal kerner", value=1e10, format="%.6g")
        lam = c2.number_input("λ – henfaldskonstant (s⁻¹)", value=1e-4, min_value=1e-20, format="%.6g")
        t   = c3.number_input("t – tid (s)", value=10000.0, min_value=0.0, format="%.6g")
        N = N0 * np.exp(-lam * t)
        frac = N / N0
        st.success(f"**N(t) = {N:.6g}**   ({frac*100:.4g}% tilbage)")
        st.latex(rf"N = {N0:.6g} \cdot e^{{-{lam:.6g} \cdot {t:.6g}}} = {N:.6g}")

    elif beregn == "N₀ – startantal":
        c1, c2, c3 = st.columns(3)
        N   = c1.number_input("N(t) – antal kerner nu", value=3.7e9, format="%.6g")
        lam = c2.number_input("λ (s⁻¹)", value=1e-4, min_value=1e-20, format="%.6g")
        t   = c3.number_input("t – tid (s)", value=10000.0, min_value=0.0, format="%.6g")
        N0 = N * np.exp(lam * t)
        st.success(f"**N₀ = {N0:.6g}**")
        st.latex(rf"N_0 = N \cdot e^{{\lambda t}} = {N:.6g} \cdot e^{{{lam:.6g} \cdot {t:.6g}}} = {N0:.6g}")

    elif beregn == "λ – henfalds­konstant (s⁻¹)":
        c1, c2, c3 = st.columns(3)
        N0 = c1.number_input("N₀ – startantal", value=1e10, min_value=1.0, format="%.6g")
        N  = c2.number_input("N(t) – antal nu", value=3.7e9, min_value=1.0, format="%.6g")
        t  = c3.number_input("t – tid (s)", value=10000.0, min_value=1e-12, format="%.6g")
        if N >= N0:
            st.error("N(t) skal være mindre end N₀ for henfald.")
        else:
            lam = -np.log(N / N0) / t
            T_half = ln2 / lam
            st.success(f"**λ = {lam:.6g} s⁻¹**   (T½ = {T_half:.6g} s  =  {T_half/3600:.4g} timer)")
            st.latex(rf"\lambda = -\frac{{\ln(N/N_0)}}{{t}} = {lam:.6g}\ \text{{s}}^{{-1}}")

    else:
        c1, c2, c3 = st.columns(3)
        N0  = c1.number_input("N₀ – startantal", value=1e10, min_value=1.0, format="%.6g")
        N   = c2.number_input("N(t) – antal nu", value=3.7e9, min_value=1.0, format="%.6g")
        lam = c3.number_input("λ (s⁻¹)", value=1e-4, min_value=1e-20, format="%.6g")
        if N >= N0:
            st.error("N(t) skal være mindre end N₀.")
        else:
            t = -np.log(N / N0) / lam
            st.success(f"**t = {t:.6g} s  =  {t/3600:.4g} timer  =  {t/86400:.4g} dage**")
            st.latex(rf"t = -\frac{{\ln(N/N_0)}}{{\lambda}} = {t:.6g}\ \text{{s}}")

elif formel == "Aktivitet:  A = λ · N":
    st.latex(r"A = \lambda \cdot N = \frac{\ln 2}{T_{1/2}} \cdot N")
    beregn = st.radio("Beregn:", ["A – aktivitet (Bq)", "λ – henfaldskonstant (s⁻¹)", "N – antal kerner"], horizontal=True)
    st.divider()
    metode = st.radio("Angiv λ via:", ["λ direkte", "T½"], horizontal=True)
    st.divider()

    if metode == "T½":
        T_half = st.number_input("T½ – halvvejstid (s)", value=5730 * 365.25 * 86400, format="%.6g")
        lam_val = ln2 / T_half
        st.info(f"λ = {lam_val:.6g} s⁻¹")
    else:
        lam_val = st.number_input("λ (s⁻¹)", value=3.84e-12, format="%.6g")

    if beregn == "A – aktivitet (Bq)":
        N = st.number_input("N – antal radioaktive kerner", value=6.022e23, format="%.6g")
        A = lam_val * N
        st.success(f"**A = {A:.6g} Bq  =  {A/3.7e10:.4g} Ci**")
        st.latex(rf"A = \lambda \cdot N = {lam_val:.6g} \cdot {N:.6g} = {A:.6g}\ \text{{Bq}}")

    elif beregn == "λ – henfaldskonstant (s⁻¹)":
        c1, c2 = st.columns(2)
        A = c1.number_input("A – aktivitet (Bq)", value=3.7e10, format="%.6g")
        N = c2.number_input("N – antal kerner", value=6.022e23, format="%.6g")
        lam_res = A / N
        T_res = ln2 / lam_res
        st.success(f"**λ = {lam_res:.6g} s⁻¹**   (T½ = {T_res:.6g} s  =  {T_res/(365.25*86400):.4g} år)")

    else:
        c1, c2 = st.columns(2)
        A = c1.number_input("A – aktivitet (Bq)", value=3.7e10, format="%.6g")
        N = A / lam_val
        st.success(f"**N = {N:.6g} kerner**")

elif formel == "Halvvejstid:  T½ = ln(2) / λ":
    st.latex(r"T_{1/2} = \frac{\ln 2}{\lambda}")
    beregn = st.radio("Beregn:", ["T½ (s)", "λ (s⁻¹)"], horizontal=True)
    st.divider()

    if beregn == "T½ (s)":
        lam = st.number_input("λ – henfaldskonstant (s⁻¹)", value=1e-4, min_value=1e-30, format="%.6g")
        T_half = ln2 / lam
        st.success(f"**T½ = {T_half:.6g} s  =  {T_half/60:.4g} min  =  {T_half/3600:.4g} timer  =  {T_half/86400:.4g} dage  =  {T_half/(365.25*86400):.4g} år**")
        st.latex(rf"T_{{1/2}} = \frac{{\ln 2}}{{\lambda}} = \frac{{{ln2:.6f}}}{{{lam:.6g}}} = {T_half:.6g}\ \text{{s}}")
    else:
        T_half = st.number_input("T½ – halvvejstid (s)", value=6931.5, min_value=1e-12, format="%.6g")
        lam = ln2 / T_half
        st.success(f"**λ = {lam:.6g} s⁻¹**")
        st.latex(rf"\lambda = \frac{{\ln 2}}{{T_{{1/2}}}} = \frac{{{ln2:.6f}}}{{{T_half:.6g}}} = {lam:.6g}\ \text{{s}}^{{-1}}")

elif formel == "Energi-masse:  E = Δm · c²":
    st.latex(r"E = \Delta m \cdot c^2")
    st.info(f"c = {c:.4g} m/s,   1 u = {u:.4g} kg,   1 u·c² = 931.5 MeV")
    beregn = st.radio("Beregn:", ["E – frigivet energi (J)", "Δm – massedefekt (kg)"], horizontal=True)
    enhed = st.radio("Masseenhed:", ["kg", "u (atommasseenhed)"], horizontal=True)
    st.divider()

    if beregn == "E – frigivet energi (J)":
        if enhed == "kg":
            dm = st.number_input("Δm – massedefekt (kg)", value=1e-29, format="%.6g")
            dm_kg = dm
        else:
            dm = st.number_input("Δm – massedefekt (u)", value=0.006, format="%.6g")
            dm_kg = dm * u
        E = dm_kg * c**2
        st.success(f"**E = {E:.6g} J  =  {E/eV/1e6:.4g} MeV**")
        st.latex(rf"E = \Delta m \cdot c^2 = {dm_kg:.6g}\ \text{{kg}} \cdot ({c:.4g})^2 = {E:.6g}\ \text{{J}}")

    else:
        E = st.number_input("E – energi (J)", value=9e-13, format="%.6g")
        dm_kg = E / c**2
        dm_u = dm_kg / u
        st.success(f"**Δm = {dm_kg:.6g} kg  =  {dm_u:.6g} u**")
        st.latex(rf"\Delta m = \frac{{E}}{{c^2}} = \frac{{{E:.6g}}}{{{c:.4g}^2}} = {dm_kg:.6g}\ \text{{kg}}")

elif formel == "Fotonenergí:  E = h · f = h·c / λ":
    st.latex(r"E = h \cdot f = \frac{h \cdot c}{\lambda}")
    st.info(f"h = {h:.4g} J·s,   c = {c:.4g} m/s")
    beregn = st.radio("Beregn:", ["E – fotonenergí (J)", "f – frekvens (Hz)", "λ – bølgelængde (m)"], horizontal=True)
    st.divider()

    if beregn == "E – fotonenergí (J)":
        metode = st.radio("Via:", ["frekvens f", "bølgelængde λ"], horizontal=True)
        if metode == "frekvens f":
            f_val = st.number_input("f – frekvens (Hz)", value=5e14, format="%.6g")
            E_ph = h * f_val
        else:
            lam_val = st.number_input("λ – bølgelængde (m)", value=550e-9, format="%.6g")
            f_val = c / lam_val
            E_ph = h * c / lam_val
        st.success(f"**E = {E_ph:.6g} J  =  {E_ph/eV:.4g} eV**")
        st.latex(rf"E = h \cdot f = {h:.4g} \cdot {f_val:.4g} = {E_ph:.6g}\ \text{{J}}")

    elif beregn == "f – frekvens (Hz)":
        E_ph = st.number_input("E – fotonenergí (J)", value=3.31e-19, format="%.6g")
        f_val = E_ph / h
        lam_val = c / f_val
        st.success(f"**f = {f_val:.6g} Hz**   (λ = {lam_val:.6g} m  =  {lam_val*1e9:.4g} nm)")
        st.latex(rf"f = \frac{{E}}{{h}} = \frac{{{E_ph:.6g}}}{{{h:.4g}}} = {f_val:.6g}\ \text{{Hz}}")

    else:
        E_ph = st.number_input("E – fotonenergí (J)", value=3.31e-19, format="%.6g")
        lam_val = h * c / E_ph
        st.success(f"**λ = {lam_val:.6g} m  =  {lam_val*1e9:.4g} nm**")
        st.latex(rf"\lambda = \frac{{hc}}{{E}} = \frac{{{h:.4g} \cdot {c:.4g}}}{{{E_ph:.6g}}} = {lam_val:.6g}\ \text{{m}}")

elif formel == "de Broglie bølgelængde:  λ = h / (m·v)":
    st.latex(r"\lambda = \frac{h}{m \cdot v} = \frac{h}{p}")
    beregn = st.radio("Beregn:", ["λ – bølgelængde (m)", "v – hastighed (m/s)", "m – masse (kg)"], horizontal=True)
    st.divider()

    if beregn == "λ – bølgelængde (m)":
        c1, c2 = st.columns(2)
        m_val = c1.number_input("m – masse (kg)", value=m_e, format="%.6g")
        v_val = c2.number_input("v – hastighed (m/s)", value=1e6, format="%.6g")
        lam = h / (m_val * v_val)
        st.success(f"**λ = {lam:.6g} m  =  {lam*1e9:.4g} nm  =  {lam*1e10:.4g} Å**")
        st.latex(rf"\lambda = \frac{{h}}{{mv}} = \frac{{{h:.4g}}}{{{m_val:.4g} \cdot {v_val:.4g}}} = {lam:.6g}\ \text{{m}}")

    elif beregn == "v – hastighed (m/s)":
        c1, c2 = st.columns(2)
        lam   = c1.number_input("λ – bølgelængde (m)", value=7.28e-10, format="%.6g")
        m_val = c2.number_input("m – masse (kg)", value=m_e, min_value=1e-40, format="%.6g")
        v = h / (m_val * lam)
        st.success(f"**v = {v:.6g} m/s**")

    else:
        c1, c2 = st.columns(2)
        lam   = c1.number_input("λ – bølgelængde (m)", value=7.28e-10, format="%.6g")
        v_val = c2.number_input("v – hastighed (m/s)", value=1e6, min_value=1e-12, format="%.6g")
        m_val = h / (lam * v_val)
        st.success(f"**m = {m_val:.6g} kg**")

elif formel == "Bohrs model – hydrogenspektret":
    st.latex(r"E_n = -\frac{13{,}6 \cdot Z^2\ \text{eV}}{n^2} \qquad \Delta E = E_{n_2} - E_{n_1} = h \cdot f")
    st.divider()

    col0, col1, col2 = st.columns(3)
    Z  = col0.number_input("Z – atomnummer (H=1, He=2, Li=3…)", value=1, min_value=1, step=1)
    n1 = col1.number_input("n₁ – lavere energiniveau", value=2, min_value=1, step=1)
    n2 = col2.number_input("n₂ – højere energiniveau", value=3, min_value=2, step=1)

    if Z == 1:
        ion_navn = "H"
    elif Z == 2:
        ion_navn = "He⁺"
    elif Z == 3:
        ion_navn = "Li²⁺"
    else:
        ion_navn = f"Z={Z} ion"

    if n2 <= n1:
        st.error("n₂ skal være større end n₁")
    else:
        E1 = -13.6 * Z**2 / n1**2
        E2 = -13.6 * Z**2 / n2**2
        dE_eV = E2 - E1
        dE_J  = dE_eV * eV
        f_val = abs(dE_J) / h
        lam   = h * c / abs(dE_J)

        st.info(f"Ion: **{ion_navn}**  (Z={Z})")
        col1, col2, col3 = st.columns(3)
        col1.metric(f"E_{n1}", f"{E1:.4f} eV")
        col2.metric(f"E_{n2}", f"{E2:.4f} eV")
        col3.metric("ΔE", f"{abs(dE_eV):.4f} eV")

        st.success(f"**λ = {lam*1e9:.4g} nm  |  f = {f_val:.4g} Hz**")

        if Z == 1:
            if n1 == 1:
                serie = "Lyman (UV)"
            elif n1 == 2:
                serie = "Balmer (synligt/UV)"
            elif n1 == 3:
                serie = "Paschen (IR)"
            else:
                serie = f"Serie med n₁={n1} (IR)"
            st.info(f"Hydrogen-serie: **{serie}**")

        with st.expander("Vis udregning"):
            st.latex(rf"E_{{{n1}}} = -\frac{{13.6 \cdot {Z}^2}}{{{n1}^2}} = {E1:.4f}\ \text{{eV}}")
            st.latex(rf"E_{{{n2}}} = -\frac{{13.6 \cdot {Z}^2}}{{{n2}^2}} = {E2:.4f}\ \text{{eV}}")
            st.latex(rf"\Delta E = {abs(dE_eV):.4f}\ \text{{eV}} = {abs(dE_J):.4g}\ \text{{J}}")
            st.latex(rf"\lambda = \frac{{hc}}{{\Delta E}} = {lam:.4g}\ \text{{m}} = {lam*1e9:.4g}\ \text{{nm}}")

elif formel == "Fotoelektrisk effekt":
    st.latex(r"E_k = h \cdot f - W \qquad W = h \cdot f_0")
    st.markdown("Ek = kinetisk energi af udslynget elektron, W = udtrækningsenergi (arbejdsfunktion), f₀ = tærskelfrekvens")
    st.divider()

    beregn = st.radio("Beregn:", ["Ek – kinetisk energi (J)", "f – fotonfrekvens (Hz)", "W – arbejdsfunktion (J)", "f₀ – tærskelfrekvens (Hz)"], horizontal=True)
    st.divider()

    if beregn == "Ek – kinetisk energi (J)":
        c1, c2 = st.columns(2)
        f_val = c1.number_input("f – fotonfrekvens (Hz)", value=8e14, format="%.6g")
        W_val = c2.number_input("W – arbejdsfunktion (J)", value=3.7e-19, format="%.6g")
        Ek = h * f_val - W_val
        if Ek < 0:
            st.warning(f"Ek < 0: fotonet har ikke nok energi til at frigøre elektronen. (Ek = {Ek:.4g} J)")
        else:
            st.success(f"**Ek = {Ek:.6g} J  =  {Ek/eV:.4g} eV**")
            st.latex(rf"E_k = hf - W = {h:.4g} \cdot {f_val:.4g} - {W_val:.4g} = {Ek:.6g}\ \text{{J}}")

    elif beregn == "f – fotonfrekvens (Hz)":
        c1, c2 = st.columns(2)
        Ek = c1.number_input("Ek – kinetisk energi (J)", value=1.6e-19, format="%.6g")
        W  = c2.number_input("W – arbejdsfunktion (J)", value=3.7e-19, format="%.6g")
        f_val = (Ek + W) / h
        st.success(f"**f = {f_val:.6g} Hz**   (λ = {c/f_val*1e9:.4g} nm)")

    elif beregn == "W – arbejdsfunktion (J)":
        c1, c2 = st.columns(2)
        f_val = c1.number_input("f – fotonfrekvens (Hz)", value=8e14, format="%.6g")
        Ek    = c2.number_input("Ek – kinetisk energi (J)", value=1.6e-19, format="%.6g")
        W = h * f_val - Ek
        if W < 0:
            st.error("Negativ arbejdsfunktion – ugyldig kombination.")
        else:
            st.success(f"**W = {W:.6g} J  =  {W/eV:.4g} eV**")

    else:
        W = st.number_input("W – arbejdsfunktion (J)", value=3.7e-19, format="%.6g")
        f0 = W / h
        lam0 = c / f0
        st.success(f"**f₀ = {f0:.6g} Hz**   (λ₀ = {lam0*1e9:.4g} nm)")
        st.latex(rf"f_0 = \frac{{W}}{{h}} = \frac{{{W:.4g}}}{{{h:.4g}}} = {f0:.6g}\ \text{{Hz}}")

elif formel == "Compton-spredning":
    st.latex(r"\Delta\lambda = \frac{h}{m_e c}(1 - \cos\theta)")
    st.info(f"Compton-bølgelængde: λ_C = h/(mₑc) = {h/(m_e*c)*1e12:.4g} pm")
    st.divider()

    c1, c2 = st.columns(2)
    lam_in = c1.number_input("λ – indfalds­bølgelængde (m)", value=0.1e-10, format="%.6g")
    theta  = c2.number_input("θ – spredningsvinkel (grader)", value=90.0, min_value=0.0, max_value=180.0, format="%.6g")

    lam_C = h / (m_e * c)
    dlam = lam_C * (1 - np.cos(np.radians(theta)))
    lam_out = lam_in + dlam

    col1, col2, col3 = st.columns(3)
    col1.metric("Δλ", f"{dlam*1e12:.4g} pm")
    col2.metric("λ_ud", f"{lam_out*1e12:.4g} pm")
    col3.metric("Energitab", f"{(1 - lam_in/lam_out)*100:.2f}%")

    with st.expander("Vis udregning"):
        st.latex(rf"\Delta\lambda = \frac{{h}}{{m_e c}}(1-\cos\theta) = {lam_C:.4g} \cdot (1-\cos({theta:.4g}°)) = {dlam:.4g}\ \text{{m}}")
        st.latex(rf"\lambda_{{ud}} = \lambda_{{ind}} + \Delta\lambda = {lam_in:.4g} + {dlam:.4g} = {lam_out:.4g}\ \text{{m}}")
