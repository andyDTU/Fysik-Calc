import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, breadcrumb

st.set_page_config(page_title="Enhedsomregner", page_icon="⚖️", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("⚖️", "Enhedsomregner")
st.title("⚖️ Enhedsomregner")
st.markdown("Omregn enheder der hyppigt forveksles på DTU 10060 eksamen.")
st.divider()

kategori = st.selectbox(
    "Vælg kategori",
    [
        "🌡️ Temperatur",
        "💨 Tryk",
        "⚡ Energi",
        "📐 Vinkel",
        "🏃 Hastighed",
        "⚖️ Masse",
        "🔄 Frekvens / Periode",
        "🔋 Effekt",
    ],
)

st.divider()

if kategori == "🌡️ Temperatur":
    st.subheader("🌡️ Temperatur")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["°C", "K", "°F"], key="temp_from")
        val = st.number_input("Værdi", value=0.0, format="%.4f", key="temp_val")

    if from_unit == "°C":
        kelvin = val + 273.15
        fahrenheit = val * 9 / 5 + 32
        celsius = val
    elif from_unit == "K":
        kelvin = val
        celsius = val - 273.15
        fahrenheit = celsius * 9 / 5 + 32
    else:
        kelvin = (val - 32) * 5 / 9 + 273.15
        celsius = kelvin - 273.15
        fahrenheit = val

    with col_out:
        st.metric("Celsius (°C)", f"{celsius:.4f}")
        st.metric("Kelvin (K)", f"{kelvin:.4f}")
        st.metric("Fahrenheit (°F)", f"{fahrenheit:.4f}")

    if st.button("📋 Gem Kelvin-værdi"):
        gem_resultat(kelvin, "K", "T")

elif kategori == "💨 Tryk":
    st.subheader("💨 Tryk")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["Pa", "bar", "atm", "mmHg", "kPa"], key="tryk_from")
        val = st.number_input("Værdi", value=101325.0, min_value=1e-30, format="%.6g", key="tryk_val")

    if from_unit == "Pa":
        pa = val
    elif from_unit == "bar":
        pa = val * 100000
    elif from_unit == "atm":
        pa = val * 101325
    elif from_unit == "mmHg":
        pa = val * 133.322
    else:
        pa = val * 1000

    bar = pa / 100000
    atm = pa / 101325
    mmhg = pa / 133.322
    kpa = pa / 1000

    with col_out:
        st.metric("Pascal (Pa)", f"{pa:.6g}")
        st.metric("Bar", f"{bar:.6g}")
        st.metric("Atmosfære (atm)", f"{atm:.6g}")
        st.metric("mmHg (Torr)", f"{mmhg:.6g}")
        st.metric("Kilopascal (kPa)", f"{kpa:.6g}")

    if st.button("📋 Gem Pa-værdi"):
        gem_resultat(pa, "Pa", "p")

elif kategori == "⚡ Energi":
    st.subheader("⚡ Energi")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["J", "kJ", "MJ", "eV", "cal", "kWh"], key="energi_from")
        val = st.number_input("Værdi", value=1.0, format="%.6g", key="energi_val")

    if from_unit == "J":
        joule = val
    elif from_unit == "kJ":
        joule = val * 1e3
    elif from_unit == "MJ":
        joule = val * 1e6
    elif from_unit == "eV":
        joule = val * 1.602e-19
    elif from_unit == "cal":
        joule = val * 4.184
    else:
        joule = val * 3.6e6

    kj = joule / 1e3
    mj = joule / 1e6
    ev = joule / 1.602e-19
    cal = joule / 4.184
    kwh = joule / 3.6e6

    with col_out:
        st.metric("Joule (J)", f"{joule:.6g}")
        st.metric("Kilojoule (kJ)", f"{kj:.6g}")
        st.metric("Megajoule (MJ)", f"{mj:.6g}")
        st.metric("Elektronvolt (eV)", f"{ev:.6g}")
        st.metric("Kalorie (cal)", f"{cal:.6g}")
        st.metric("Kilowatt-time (kWh)", f"{kwh:.6g}")

    if st.button("📋 Gem Joule-værdi"):
        gem_resultat(joule, "J", "E")

elif kategori == "📐 Vinkel":
    st.subheader("📐 Vinkel")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["grader (°)", "radianer (rad)"], key="vinkel_from")
        val = st.number_input("Værdi", value=90.0, format="%.6g", key="vinkel_val")

    if from_unit == "grader (°)":
        deg = val
        rad = val * np.pi / 180
    else:
        rad = val
        deg = val * 180 / np.pi

    with col_out:
        st.metric("Grader (°)", f"{deg:.6g}")
        st.metric("Radianer (rad)", f"{rad:.6g}")

    if st.button("📋 Gem radianer"):
        gem_resultat(rad, "rad", "θ")

    st.markdown("**Referencetabel – common vinkler**")
    ref_degs = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270, 360]
    ref_data = {"Grader (°)": ref_degs, "Radianer (rad)": [round(d * np.pi / 180, 6) for d in ref_degs]}
    st.table(ref_data)

elif kategori == "🏃 Hastighed":
    st.subheader("🏃 Hastighed")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["m/s", "km/h", "mph"], key="hast_from")
        val = st.number_input("Værdi", value=10.0, format="%.6g", key="hast_val")

    if from_unit == "m/s":
        ms = val
    elif from_unit == "km/h":
        ms = val / 3.6
    else:
        ms = val * 0.44704

    kmh = ms * 3.6
    mph = ms / 0.44704

    with col_out:
        st.metric("Meter pr. sekund (m/s)", f"{ms:.6g}")
        st.metric("Kilometer pr. time (km/h)", f"{kmh:.6g}")
        st.metric("Miles pr. time (mph)", f"{mph:.6g}")

    if st.button("📋 Gem m/s-værdi"):
        gem_resultat(ms, "m/s", "v")

elif kategori == "⚖️ Masse":
    st.subheader("⚖️ Masse")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["kg", "g", "mg", "u"], key="masse_from")
        val = st.number_input("Værdi", value=1.0, min_value=1e-60, format="%.6g", key="masse_val")

    if from_unit == "kg":
        kg = val
    elif from_unit == "g":
        kg = val / 1e3
    elif from_unit == "mg":
        kg = val / 1e6
    else:
        kg = val * 1.66054e-27

    g = kg * 1e3
    mg = kg * 1e6
    u = kg / 1.66054e-27

    with col_out:
        st.metric("Kilogram (kg)", f"{kg:.6g}")
        st.metric("Gram (g)", f"{g:.6g}")
        st.metric("Milligram (mg)", f"{mg:.6g}")
        st.metric("Atommasseenhed (u)", f"{u:.6g}")

    if st.button("📋 Gem kg-værdi"):
        gem_resultat(kg, "kg", "m")

elif kategori == "🔄 Frekvens / Periode":
    st.subheader("🔄 Frekvens / Periode")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["Hz (f)", "s (T)", "rad/s (ω)", "RPM"], key="freq_from")
        val = st.number_input("Værdi", value=1.0, min_value=1e-30, format="%.6g", key="freq_val")

    if from_unit == "Hz (f)":
        f = val
    elif from_unit == "s (T)":
        f = 1 / val
    elif from_unit == "rad/s (ω)":
        f = val / (2 * np.pi)
    else:
        f = val / 60

    T = 1 / f
    omega = 2 * np.pi * f
    rpm = f * 60

    with col_out:
        st.metric("Frekvens f (Hz)", f"{f:.6g}")
        st.metric("Periode T (s)", f"{T:.6g}")
        st.metric("Vinkelfrekvens ω (rad/s)", f"{omega:.6g}")
        st.metric("Omdrejninger pr. minut (RPM)", f"{rpm:.6g}")

    if st.button("📋 Gem ω (rad/s)"):
        gem_resultat(omega, "rad/s", "ω")

elif kategori == "🔋 Effekt":
    st.subheader("🔋 Effekt")
    col_in, col_out = st.columns(2)
    with col_in:
        from_unit = st.selectbox("Fra enhed", ["W", "kW", "MW", "hk"], key="effekt_from")
        val = st.number_input("Værdi", value=1000.0, min_value=1e-30, format="%.6g", key="effekt_val")

    if from_unit == "W":
        w = val
    elif from_unit == "kW":
        w = val * 1e3
    elif from_unit == "MW":
        w = val * 1e6
    else:
        w = val * 735.5

    kw = w / 1e3
    mw = w / 1e6
    hk = w / 735.5

    with col_out:
        st.metric("Watt (W)", f"{w:.6g}")
        st.metric("Kilowatt (kW)", f"{kw:.6g}")
        st.metric("Megawatt (MW)", f"{mw:.6g}")
        st.metric("Hestekraft (hk)", f"{hk:.6g}")

    if st.button("📋 Gem W-værdi"):
        gem_resultat(w, "W", "P")

st.divider()
st.subheader("📏 Potenser – SI-præfikser")
potenser = {
    "Præfiks": ["nano (n)", "mikro (μ)", "milli (m)", "kilo (k)", "mega (M)", "giga (G)", "tera (T)"],
    "Symbol": ["n", "μ", "m", "k", "M", "G", "T"],
    "Faktor": ["10⁻⁹", "10⁻⁶", "10⁻³", "10³", "10⁶", "10⁹", "10¹²"],
    "Eksempel": [
        "1 nm = 1×10⁻⁹ m",
        "1 μm = 1×10⁻⁶ m",
        "1 mm = 0.001 m",
        "1 km = 1000 m",
        "1 MHz = 10⁶ Hz",
        "1 GHz = 10⁹ Hz",
        "1 THz = 10¹² Hz",
    ],
}
st.table(potenser)
