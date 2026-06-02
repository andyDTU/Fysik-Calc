import streamlit as st
import numpy as np
from utils import show_sidebar_constants, show_resultat_sidebar, gem_resultat, show_tips, formula_card_grid, breadcrumb

st.set_page_config(page_title="Dynamik", page_icon="💪", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()
breadcrumb("💪", "Dynamik")
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

_DYN_GROUPS = [
    ("⚡ Kræfter & Newton", [
        ("Newtons 2. lov",       "F = m · a",                     "Newtons 2. lov:  F = m · a"),
        ("Tyngdekraft",          "G = m · g",                     "Tyngdekraft:  G = m · g"),
        ("Friktion",             "f = μ · N",                     "Friktion:  f = μ · N"),
        ("μ fra v-t-graf",       "μ = |a|/g = |Δv/Δt|/g",        "Friktion fra v-t-graf:  μ = |Δv/Δt| / g"),
        ("Centripetalkraft",     "Fc = m·v²/r",                   "Centripetalkraft:  Fc = m · v² / r"),
        ("Normalkraft i sløjfe", "top: N=mv²/r−mg",               "Normalkraft i sløjfe (top/bund)"),
        ("Gravitationsloven",    "F = G·m₁·m₂/r²",               "Gravitationsloven:  F = G·m₁·m₂ / r²"),
        ("Kraftmoment",          "τ = F · l",                     "Kraftmoment:  τ = F · l"),
        ("Statisk ligevægt",     "ΣF=0,  Στ=0",                   "Statisk ligevægt:  ΣF = 0 og Στ = 0"),
        ("To-snors ophæng",      "T₁=mg·cosθ₂/sin(θ₁+θ₂)",       "To-snors ophæng:  T₁ og T₂"),
        ("To-klods system",      "a_CM = F_ext / M_total",         "To-klods system:  CM-acceleration"),
    ]),
    ("🏃 Mekanik & Bevægelse", [
        ("Impuls",               "p = m · v",                     "Impuls:  p = m · v"),
        ("Impulsmomentloven",    "F·Δt = Δp",                     "Impulsmomentloven:  F · Δt = Δp"),
        ("Hældende plan",        "N=mg·cosθ,  f≤μN",              "Hældende plan"),
        ("Atwood-maskine",       "a=(m₂−m₁)g/(m₁+m₂)",          "Atwood-maskine:  to masser over trisse"),
        ("Konisk pendul",        "tanθ=ω²r/g",                    "Konisk pendul"),
        ("Snorpendel – snorkraft", "T=m(v₀²/R−2g+3gcosθ)",       "Snorpendel – snorkraft ved vilkårlig vinkel"),
        ("Kraft i vinkel",       "a=(Fcosθ−μ(mg−Fsinθ))/m",      "Kraft i vinkel på ru flade"),
        ("Satellit / Kepler",    "v=√(GM/r),  T²∝r³",             "Satellit og Keplers 3. lov"),
    ]),
    ("🌊 Fluider & Materialer", [
        ("Bernoulli-ligning",    "p+½ρv²+ρgh = konst",            "Bernoulli-ligning"),
        ("Arkimedes",            "F_b = ρ·V·g",                   "Arkimedes' princip:  F_b = ρ · V · g"),
        ("Terminal hastighed",   "v_T = √(2mg/CρA)",              "Terminal hastighed:  v_T = √(2mg / CρA)"),
        ("Spænding og tøjning",  "σ=F/A,  d=√(4F/πσ)",           "Spænding og tøjning:  σ = F / A"),
    ]),
]

# Flat list kept for initialisation and lookup
_DYN_FORMULAS = [f for _, grp in _DYN_GROUPS for f in grp]
_DYN_FULL_KEYS = [f[2] for f in _DYN_FORMULAS]

if "dyn_formel" not in st.session_state or st.session_state["dyn_formel"] not in _DYN_FULL_KEYS:
    st.session_state["dyn_formel"] = _DYN_FULL_KEYS[0]

def _dyn_card_group(label, formulas, columns=4):
    st.caption(f"**{label}**")
    cols = st.columns(columns)
    for i, (short_name, eq_hint, full_key) in enumerate(formulas):
        is_active = st.session_state["dyn_formel"] == full_key
        with cols[i % columns].container(border=True):
            st.markdown(f"**{'✓ ' if is_active else ''}{short_name}**")
            if eq_hint:
                st.caption(eq_hint)
            if st.button("Valgt" if is_active else "Vælg",
                         key=f"_dyn_{full_key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state["dyn_formel"] = full_key
                st.rerun()

for _grp_label, _grp_formulas in _DYN_GROUPS:
    _dyn_card_group(_grp_label, _grp_formulas)
    st.write("")

formel = st.session_state["dyn_formel"]

DYN_TIPS = {
    "Newtons 2. lov:  F = m · a": "Brug nettokraften ΣF, ikke bare én kraft. Husk retning (fortegn).",
    "Tyngdekraft:  G = m · g": "Tyngdekraft virker altid nedad. G = m·g = vægt i Newton.",
    "Friktion:  f = μ · N": "Statisk friktion (μs) er større end kinetisk (μk). Friktionskraft modvirker bevægelse.",
    "Centripetalkraft:  Fc = m · v² / r": "Centripetalkraft peger mod centrum. Den er en nettokraft, ikke en ekstra kraft.",
    "Normalkraft i sløjfe (top/bund)": "Top: N = mv²/r − mg (mindst). Bund: N = mv²/r + mg (størst). Minimum v ved top: √(gr). Minimum starthøjde for at gennemføre løkke: h_min = 5r/2.",
    "Gravitationsloven:  F = G·m₁·m₂ / r²": "G = 6.674×10⁻¹¹ N·m²/kg². r er centrumsafstanden. Orbital­hastighed: v = √(GM/r).",
    "Impuls:  p = m · v": "Impuls bevares i isolerede systemer. p er en vektor (retning vigtig).",
    "Impulsmomentloven:  F · Δt = Δp": "Bruges ved støde/slag: stor kraft i kort tid giver stor impulsændring.",
    "Kraftmoment:  τ = F · l": "Kraftarm l er den vinkelrette afstand fra rotationsaksen til kraftlinjen.",
    "Hældende plan": "Opsæt koordinater langs planen. Normal­kraft N = mg·cos(θ). Friktionsgrænse: f ≤ μN.",
    "Atwood-maskine:  to masser over trisse": "Acceleration a = (m₂−m₁)g/(m₁+m₂). Snorkraft T = 2m₁m₂g/(m₁+m₂).",
    "Spænding og tøjning:  σ = F / A": "σ = F/A. Cirkulært tværsnit: A = πd²/4 → d = √(4F/πσ). Youngs modul E = σ/ε.",
    "Konisk pendul": "Pendullod drejer i vandret cirkel. tanθ = ω²r/g. Periode T = 2π√(L·cosθ/g) — afhænger ikke af massen!",
    "Bernoulli-ligning": "Gælder for ideel (ikke-viskøs, inkompressibel) strømning. Torricelli: v = √(2gh) for hul i beholder.",
    "Snorpendel – snorkraft ved vilkårlig vinkel": "Snoren starter lodret, loddet har vandret hastighed v₀. T = m(v₀²/R − 2g + 3g·cosθ). Ved θ=90° (vandret snor): T = m(v₀²/R − 2g).",
    "Kraft i vinkel på ru flade": "F trækker i vinkel θ opad. Normalkraft reduceres: N = mg − F·sinθ. Acceleration a = (F·cosθ − μk·N)/m. Optimal vinkel θ_min = arctan(μk) giver mindste F for konstant v.",
    "Arkimedes' princip:  F_b = ρ · V · g": "Opdriftskraft F_b = ρ_fluid · V_nedsænket · g. Flyder når ρ_obj < ρ_fluid. Synker når ρ_obj > ρ_fluid.",
    "Terminal hastighed:  v_T = √(2mg / CρA)": "Luftmodstand F_drag = ½CρAv². Terminalhastighed nås når F_drag = mg → v_T = √(2mg/CρA). C ≈ 0.47 for kugle.",
    "Satellit og Keplers 3. lov": "Orbitalhastighed v = √(GM/r). T = 2πr/v. Keplers 3. lov: T² = (4π²/GM)·r³. Undvigelseshastighed v_e = √(2GM/r) = √2·v_orb.",
    "Statisk ligevægt:  ΣF = 0 og Στ = 0": "Vælg omdrejningspunkt smart for at eliminere ukendte kræfter. Kraftmomenter: F·d_⊥. Sæt én retning positiv.",
}
show_tips(formel, DYN_TIPS)
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
        if st.button("📋 Gem F", key="gem_dyn_n2_F"):
            gem_resultat(F, "N", "F")

    elif beregn == "m – masse (kg)":
        c1, c2 = st.columns(2)
        F = c1.number_input("F – kraft (N)", value=20.0, format="%.6g")
        a = c2.number_input("a – acceleration (m/s²)", value=2.0, min_value=1e-12, format="%.6g")
        m = F / a
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{F}}{{a}} = \frac{{{F:.6g}}}{{{a:.6g}}} = {m:.6g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_dyn_n2_m"):
            gem_resultat(m, "kg", "m")

    else:
        c1, c2 = st.columns(2)
        F = c1.number_input("F – kraft (N)", value=20.0, format="%.6g")
        m = c2.number_input("m – masse (kg)", value=10.0, min_value=1e-12, format="%.6g")
        a = F / m
        st.success(f"**a = {a:.6g} m/s²**")
        st.latex(rf"a = \frac{{F}}{{m}} = \frac{{{F:.6g}}}{{{m:.6g}}} = {a:.6g}\ \text{{m/s}}^2")
        if st.button("📋 Gem a", key="gem_dyn_n2_a"):
            gem_resultat(a, "m/s²", "a")

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
        if st.button("📋 Gem G", key="gem_dyn_tyng_G"):
            gem_resultat(Fg, "N", "G")

    else:
        Fg = st.number_input("G – tyngdekraft (N)", value=98.2, format="%.6g")
        m = Fg / g_val
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{G}}{{g}} = \frac{{{Fg:.6g}}}{{{g_val:.6g}}} = {m:.6g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_dyn_tyng_m"):
            gem_resultat(m, "kg", "m")

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
        if st.button("📋 Gem f", key="gem_dyn_frikt_f"):
            gem_resultat(f, "N", "f")

    elif beregn == "μ – friktionskoefficient":
        c1, c2 = st.columns(2)
        f = c1.number_input("f – friktionskraft (N)", value=30.0, format="%.6g")
        N = c2.number_input("N – normalkraft (N)", value=100.0, min_value=1e-12, format="%.6g")
        mu = f / N
        st.success(f"**μ = {mu:.6g}**")
        st.latex(rf"\mu = \frac{{f}}{{N}} = \frac{{{f:.6g}}}{{{N:.6g}}} = {mu:.6g}")
        if st.button("📋 Gem μ", key="gem_dyn_frikt_mu"):
            gem_resultat(mu, "", "μ")

    else:
        c1, c2 = st.columns(2)
        f  = c1.number_input("f – friktionskraft (N)", value=30.0, format="%.6g")
        mu = c2.number_input("μ – friktionskoefficient", value=0.3, min_value=1e-12, format="%.6g")
        N = f / mu
        st.success(f"**N = {N:.6g} N**")
        st.latex(rf"N = \frac{{f}}{{\mu}} = \frac{{{f:.6g}}}{{{mu:.6g}}} = {N:.6g}\ \text{{N}}")
        if st.button("📋 Gem N", key="gem_dyn_frikt_N"):
            gem_resultat(N, "N", "N")

elif formel == "Friktion fra v-t-graf:  μ = |Δv/Δt| / g":
    st.latex(r"\mu_k = \frac{|a|}{g} = \frac{|\Delta v|}{\Delta t \cdot g}")
    st.markdown(
        "Aflæs to punkter på den **lineære decelerationsfase** i v-t-grafen. "
        "Kun friktion virker (vandret flade, ingen andre kræfter). "
        "Da f = μk·mg = m·|a|, fås direkte **μk = |a|/g**."
    )
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    v1_vt = c1.number_input("v₁ – hastighed ved t₁ (m/s)", value=2.0, format="%.6g", key="vt_v1")
    t1_vt = c2.number_input("t₁ – tidspunkt (s)", value=5.0, format="%.6g", key="vt_t1")
    v2_vt = c3.number_input("v₂ – hastighed ved t₂ (m/s)", value=0.0, format="%.6g", key="vt_v2")
    t2_vt = c4.number_input("t₂ – tidspunkt (s)", value=23.0, format="%.6g", key="vt_t2")

    dt = t2_vt - t1_vt
    if abs(dt) < 1e-9:
        st.error("t₁ og t₂ må ikke være ens.")
    else:
        a_vt  = (v2_vt - v1_vt) / dt
        mu_vt = abs(a_vt) / G
        col1, col2 = st.columns(2)
        col1.metric("Deceleration |a|", f"{abs(a_vt):.4g} m/s²")
        col2.metric("μk", f"{mu_vt:.4g}")
        st.success(f"**μk = {mu_vt:.4g}**")
        st.latex(
            rf"a = \frac{{\Delta v}}{{\Delta t}} = \frac{{{v2_vt:.4g} - {v1_vt:.4g}}}{{{t2_vt:.4g} - {t1_vt:.4g}}} = {a_vt:.4g}\ \text{{m/s}}^2"
        )
        st.latex(
            rf"\mu_k = \frac{{|a|}}{{g}} = \frac{{{abs(a_vt):.4g}}}{{{G}}} = {mu_vt:.4g}"
        )
        if st.button("📋 Gem μk", key="gem_vt_mu"):
            gem_resultat(mu_vt, "", "μk")

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
        if st.button("📋 Gem Fc", key="gem_dyn_cent_Fc"):
            gem_resultat(Fc, "N", "Fc")

    elif beregn == "m (kg)":
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        v  = c2.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        r  = c3.number_input("r – radius (m)", value=5.0, min_value=1e-12, format="%.6g")
        m = Fc * r / v**2
        st.success(f"**m = {m:.6g} kg**")
        st.latex(rf"m = \frac{{F_c \cdot r}}{{v^2}} = {m:.6g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_dyn_cent_m"):
            gem_resultat(m, "kg", "m")

    elif beregn == "v (m/s)":
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        r  = c3.number_input("r – radius (m)", value=5.0, min_value=1e-12, format="%.6g")
        v = np.sqrt(Fc * r / m)
        st.success(f"**v = {v:.6g} m/s**")
        st.latex(rf"v = \sqrt{{\frac{{F_c \cdot r}}{{m}}}} = {v:.6g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_dyn_cent_v"):
            gem_resultat(v, "m/s", "v")

    else:
        c1, c2, c3 = st.columns(3)
        Fc = c1.number_input("Fc – centripetalkraft (N)", value=40.0, format="%.6g")
        m  = c2.number_input("m – masse (kg)", value=2.0, min_value=1e-12, format="%.6g")
        v  = c3.number_input("v – hastighed (m/s)", value=10.0, format="%.6g")
        r = m * v**2 / Fc
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \frac{{m v^2}}{{F_c}} = {r:.6g}\ \text{{m}}")
        if st.button("📋 Gem r", key="gem_dyn_cent_r"):
            gem_resultat(r, "m", "r")

elif formel == "Gravitationsloven:  F = G·m₁·m₂ / r²":
    G_grav = 6.674e-11   # N·m²/kg²
    st.latex(r"F = \frac{G \cdot m_1 \cdot m_2}{r^2} \qquad G = 6.674 \times 10^{-11}\ \text{N·m}^2/\text{kg}^2")
    beregn = st.radio("Beregn:", [
        "F – gravitationskraft (N)",
        "r – afstand (m)",
        "m – masse (given F, den anden masse og r)",
        "v_orbital – orbital­hastighed (m/s)",
    ], horizontal=True)
    st.divider()

    if beregn == "F – gravitationskraft (N)":
        c1, c2, c3 = st.columns(3)
        m1 = c1.number_input("m₁ (kg)", value=5.972e24, format="%.6g", help="Jordens masse: 5.972e24 kg")
        m2 = c2.number_input("m₂ (kg)", value=7.346e22, format="%.6g", help="Månens masse: 7.346e22 kg")
        r  = c3.number_input("r – centrumsafstand (m)", value=3.844e8, min_value=1e-3, format="%.6g")
        F = G_grav * m1 * m2 / r**2
        st.success(f"**F = {F:.6g} N**")
        st.latex(rf"F = \frac{{G m_1 m_2}}{{r^2}} = \frac{{{G_grav:.4g} \cdot {m1:.4g} \cdot {m2:.4g}}}{{{r:.4g}^2}} = {F:.4g}\ \text{{N}}")
        if st.button("📋 Gem F", key="gem_dyn_grav_F"):
            gem_resultat(F, "N", "F_grav")

    elif beregn == "r – afstand (m)":
        c1, c2, c3 = st.columns(3)
        m1 = c1.number_input("m₁ (kg)", value=5.972e24, format="%.6g")
        m2 = c2.number_input("m₂ (kg)", value=7.346e22, format="%.6g")
        F  = c3.number_input("F – kraft (N)", value=1.98e20, min_value=1e-20, format="%.6g")
        r = np.sqrt(G_grav * m1 * m2 / F)
        st.success(f"**r = {r:.6g} m**")
        st.latex(rf"r = \sqrt{{\frac{{G m_1 m_2}}{{F}}}} = {r:.4g}\ \text{{m}}")
        if st.button("📋 Gem r", key="gem_dyn_grav_r"):
            gem_resultat(r, "m", "r")

    elif beregn == "m – masse (given F, den anden masse og r)":
        c1, c2, c3 = st.columns(3)
        F  = c1.number_input("F – kraft (N)", value=1.98e20, format="%.6g")
        m2 = c2.number_input("m₂ – den kendte masse (kg)", value=7.346e22, format="%.6g")
        r  = c3.number_input("r – centrumsafstand (m)", value=3.844e8, min_value=1e-3, format="%.6g")
        m1 = F * r**2 / (G_grav * m2)
        st.success(f"**m₁ = {m1:.6g} kg**")
        st.latex(rf"m_1 = \frac{{F r^2}}{{G m_2}} = {m1:.4g}\ \text{{kg}}")
        if st.button("📋 Gem m₁", key="gem_dyn_grav_m"):
            gem_resultat(m1, "kg", "m₁")

    else:
        st.markdown("Orbital­hastighed for cirkulær bane: **v = √(GM/r)**")
        st.latex(r"v = \sqrt{\frac{G M}{r}}")
        c1, c2 = st.columns(2)
        M = c1.number_input("M – central­masse (kg)", value=5.972e24, format="%.6g", help="Jordens masse: 5.972e24 kg")
        r = c2.number_input("r – orbital­radius (m)", value=6.371e6 + 400e3, min_value=1e3, format="%.6g",
                             help="Jordens radius + 400 km = ISS-bane: ~6.77e6 m")
        v = np.sqrt(G_grav * M / r)
        T = 2 * np.pi * r / v
        st.success(f"**v = {v:.6g} m/s**   (T = {T:.4g} s = {T/3600:.4g} timer)")
        st.latex(rf"v = \sqrt{{\frac{{G M}}{{r}}}} = \sqrt{{\frac{{{G_grav:.4g} \cdot {M:.4g}}}{{{r:.4g}}}}} = {v:.4g}\ \text{{m/s}}")
        if st.button("📋 Gem v", key="gem_dyn_grav_v"):
            gem_resultat(v, "m/s", "v_orbital")

elif formel == "Normalkraft i sløjfe (top/bund)":
    st.latex(r"\text{Bund:}\ N_{bund} = mg + \frac{mv^2}{r} \qquad \text{Top:}\ N_{top} = \frac{mv^2}{r} - mg")
    st.markdown("""
Legeme i cirkulær bevægelse i lodret plan. Centripetalkraft = netto radialkraft.

- **Bund**: N og tyngdekraft peger i modsatte retninger → N = mg + mv²/r
- **Top**: N og tyngdekraft peger begge mod centrum → N = mv²/r − mg
- **Minimum hastighed i top**: N ≥ 0 kræver v ≥ √(g·r)
""")
    st.divider()

    beregn_sl = st.radio("Beregn:", [
        "N – normalkraft (givet m, v, r)",
        "v – hastighed (givet N, m, r)",
        "h_min – minimum starthøjde (energibevarelse)",
    ], horizontal=True)
    st.divider()

    if beregn_sl == "N – normalkraft (givet m, v, r)":
        c1, c2, c3 = st.columns(3)
        m = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="sl_m_a")
        v = c2.number_input("v – fart i det givne punkt (m/s)", value=10.0, min_value=0.0, format="%.6g", key="sl_v_a")
        r = c3.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-12, format="%.6g", key="sl_r_a")

        Fc = m * v**2 / r
        N_bund = m * G + Fc
        N_top  = Fc - m * G
        v_min  = np.sqrt(G * r)

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

    elif beregn_sl == "v – hastighed (givet N, m, r)":
        position = st.radio("Position:", ["Bund  (N = mg + mv²/r)", "Top  (N = mv²/r − mg)"], horizontal=True)
        c1, c2, c3 = st.columns(3)
        N_in = c1.number_input("N – normalkraft (N)", value=15.0, min_value=0.0, format="%.6g", key="sl_N_b")
        m    = c2.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="sl_m_b")
        r    = c3.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-12, format="%.6g", key="sl_r_b")

        if "Bund" in position:
            val = r * (N_in - m * G) / m
            latex_str = rf"v = \sqrt{{\frac{{r(N - mg)}}{{m}}}} = \sqrt{{\frac{{{r:.4g}({N_in:.4g} - {m:.4g}\cdot{G})}}{{{m:.4g}}}}} "
        else:
            val = r * (N_in + m * G) / m
            latex_str = rf"v = \sqrt{{\frac{{r(N + mg)}}{{m}}}} = \sqrt{{\frac{{{r:.4g}({N_in:.4g} + {m:.4g}\cdot{G})}}{{{m:.4g}}}}} "

        if val < 0:
            st.error("v² < 0 – normalkraften er for lille til at opretholde cirkelbevægelse.")
        else:
            v = np.sqrt(val)
            st.success(f"**v = {v:.6g} m/s**")
            st.latex(latex_str + rf"= {v:.6g}\ \text{{m/s}}")
            v_min = np.sqrt(G * r)
            st.info(f"Minimum hastighed i top: v_min = √(g·r) = {v_min:.4g} m/s")
            if st.button("📋 Gem v", key="gem_sl_v"):
                gem_resultat(v, "m/s", "v")

    elif beregn_sl == "h_min – minimum starthøjde (energibevarelse)":
        st.latex(r"h_{min} = \frac{5}{2} r \qquad v_{top} = \sqrt{g r} \qquad v_{start} = \sqrt{2g\!\left(h - 2r\right)}")
        st.info("Uden friktion. Betingelse: N ≥ 0 i toppen ↔ v_top ≥ √(gr) ↔ h ≥ 5r/2.")
        st.divider()
        mode_hmin = st.radio("Beregn:", [
            "h_min – minimum starthøjde fra radius",
            "v_top – hastighed i top (givet h og r)",
            "Hvad er N i top? (givet h og r)",
        ], horizontal=True, key="sl_hmin_mode")
        st.divider()

        if mode_hmin == "h_min – minimum starthøjde fra radius":
            c1, c2 = st.columns(2)
            r_h  = c1.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-6, format="%.6g", key="sl_r_hmin")
            g_h  = c2.number_input("g (m/s²)", value=G, format="%.6g", key="sl_g_hmin")
            h_min_val = 2.5 * r_h
            v_top_min = np.sqrt(g_h * r_h)
            col1, col2 = st.columns(2)
            col1.success(f"**h_min = 5r/2 = {h_min_val:.4g} m**")
            col2.success(f"**v_top_min = √(gr) = {v_top_min:.4g} m/s**")
            st.latex(rf"h_{{min}} = \frac{{5}}{{2}} r = \frac{{5}}{{2}} \cdot {r_h:.4g} = {h_min_val:.4g}\ \text{{m}}")
            st.latex(rf"v_{{top,min}} = \sqrt{{gr}} = \sqrt{{{g_h:.4g}\cdot{r_h:.4g}}} = {v_top_min:.4g}\ \text{{m/s}}")
            st.caption("Udledning: h = r/2 + 2r = 5r/2 via ½mv² = ½m(gr) + mg(2r)")
            if st.button("📋 Gem h_min", key="gem_sl_hmin"):
                gem_resultat(h_min_val, "m", "h_min")

        elif mode_hmin == "v_top – hastighed i top (givet h og r)":
            c1, c2, c3 = st.columns(3)
            h_val = c1.number_input("h – starthøjde (m)", value=5.0, min_value=0.0, format="%.6g", key="sl_h_vtop")
            r_val = c2.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-6, format="%.6g", key="sl_r_vtop")
            g_val = c3.number_input("g (m/s²)", value=G, format="%.6g", key="sl_g_vtop")
            ke_top = h_val - 2 * r_val
            if ke_top < 0:
                st.error(f"h = {h_val:.4g} m < 2r = {2*r_val:.4g} m: legemet når ikke toppen.")
            else:
                v_top_val = np.sqrt(2 * g_val * ke_top)
                v_min_val = np.sqrt(g_val * r_val)
                col1, col2 = st.columns(2)
                col1.success(f"**v_top = {v_top_val:.4g} m/s**")
                if v_top_val >= v_min_val:
                    col2.success(f"✅ v_top ≥ v_min ({v_min_val:.4g} m/s) – kontakt opretholdt")
                else:
                    col2.error(f"❌ v_top = {v_top_val:.4g} < v_min = {v_min_val:.4g} m/s – mister kontakt!")
                st.latex(rf"v_{{top}} = \sqrt{{2g(h - 2r)}} = \sqrt{{2 \cdot {g_val:.4g}({h_val:.4g}-2\cdot{r_val:.4g})}} = {v_top_val:.4g}\ \text{{m/s}}")
                if st.button("📋 Gem v_top", key="gem_sl_vtop"):
                    gem_resultat(v_top_val, "m/s", "v_top")

        else:
            c1, c2, c3, c4 = st.columns(4)
            h_N  = c1.number_input("h – starthøjde (m)", value=5.0, min_value=0.0, format="%.6g", key="sl_h_N")
            r_N  = c2.number_input("r – sløjferadius (m)", value=2.0, min_value=1e-6, format="%.6g", key="sl_r_N")
            m_N  = c3.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g", key="sl_m_N")
            g_N  = c4.number_input("g (m/s²)", value=G, format="%.6g", key="sl_g_N")
            ke_N = h_N - 2 * r_N
            if ke_N < 0:
                st.error(f"h < 2r: legemet når ikke toppen.")
            else:
                v_top_N = np.sqrt(2 * g_N * ke_N)
                N_top_N = m_N * v_top_N**2 / r_N - m_N * g_N
                col1, col2, col3 = st.columns(3)
                col1.metric("v_top", f"{v_top_N:.4g} m/s")
                col2.metric("N_top", f"{N_top_N:.4g} N")
                h_min_N = 2.5 * r_N
                col3.metric("h_min krævet", f"{h_min_N:.4g} m")
                if N_top_N < 0:
                    st.error("❌ Negativt N: mister kontakt i toppen. Øg starthøjden.")
                else:
                    st.success("✅ Opretholdt kontakt i toppen.")
                st.latex(rf"v_{{top}} = \sqrt{{2g(h-2r)}} = {v_top_N:.4g}\ \text{{m/s}},\quad N_{{top}} = \frac{{mv^2}}{{r}} - mg = {N_top_N:.4g}\ \text{{N}}")

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

elif formel == "Konisk pendul":
    st.latex(r"T\cos\theta = mg \qquad T\sin\theta = \frac{mv^2}{r} = m\omega^2 r")
    st.latex(r"\tan\theta = \frac{\omega^2 r}{g} \qquad T_{periode} = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{L\cos\theta}{g}}")
    st.markdown("Loddet drejer i vandret cirkel. **L** = snorlængde, **r = L·sinθ**, θ = halvtopvinkel.")
    st.divider()

    mode = st.radio("Givet:", ["L og θ (snorlængde + vinkel)", "L og ω (snorlængde + vinkelhastighed)", "r og v (radius + hastighed)"], horizontal=True)
    st.divider()

    if mode == "L og θ (snorlængde + vinkel)":
        c1, c2, c3 = st.columns(3)
        L_pend = c1.number_input("L – snorlængde (m)", value=0.5, min_value=1e-6, format="%.6g")
        theta  = c2.number_input("θ – halvtopvinkel (°)", value=30.0, min_value=0.01, max_value=89.9, format="%.6g")
        m      = c3.number_input("m – masse (kg)", value=0.1, min_value=1e-12, format="%.6g")
        th_r   = np.radians(theta)
        r_k    = L_pend * np.sin(th_r)
        omega_k = np.sqrt(G * np.tan(th_r) / r_k)
        v_k    = omega_k * r_k
        T_k    = m * G / np.cos(th_r)
        period = 2 * np.pi / omega_k

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ω (rad/s)", f"{omega_k:.4g}")
        col2.metric("v (m/s)", f"{v_k:.4g}")
        col3.metric("T_snor (N)", f"{T_k:.4g}")
        col4.metric("Periode (s)", f"{period:.4g}")

        with st.expander("Vis udregning"):
            st.latex(rf"r = L\sin\theta = {L_pend:.4g}\cdot\sin({theta:.4g}°) = {r_k:.4g}\ \text{{m}}")
            st.latex(rf"\omega = \sqrt{{\frac{{g\tan\theta}}{{r}}}} = \sqrt{{\frac{{{G}\cdot\tan({theta:.4g}°)}}{{{r_k:.4g}}}}} = {omega_k:.4g}\ \text{{rad/s}}")
            st.latex(rf"T_{{snor}} = \frac{{mg}}{{\cos\theta}} = \frac{{{m:.4g}\cdot{G}}}{{\cos({theta:.4g}°)}} = {T_k:.4g}\ \text{{N}}")
            st.latex(rf"T_{{periode}} = \frac{{2\pi}}{{\omega}} = {period:.4g}\ \text{{s}}")

    elif mode == "L og ω (snorlængde + vinkelhastighed)":
        c1, c2, c3 = st.columns(3)
        L_pend = c1.number_input("L – snorlængde (m)", value=0.5, min_value=1e-6, format="%.6g")
        omega_k = c2.number_input("ω – vinkelhastighed (rad/s)", value=5.0, min_value=1e-6, format="%.6g")
        m      = c3.number_input("m – masse (kg)", value=0.1, min_value=1e-12, format="%.6g")
        cos_th = G / (omega_k**2 * L_pend)
        if cos_th > 1.0:
            st.error(f"ω = {omega_k:.4g} rad/s er for lav til at holde pendlet i luften. Minimum ω = {np.sqrt(G/L_pend):.4g} rad/s.")
        else:
            th_r   = np.arccos(cos_th)
            theta  = np.degrees(th_r)
            r_k    = L_pend * np.sin(th_r)
            v_k    = omega_k * r_k
            T_k    = m * G / cos_th
            period = 2 * np.pi / omega_k

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("θ (°)", f"{theta:.4g}")
            col2.metric("v (m/s)", f"{v_k:.4g}")
            col3.metric("T_snor (N)", f"{T_k:.4g}")
            col4.metric("Periode (s)", f"{period:.4g}")

            with st.expander("Vis udregning"):
                st.latex(rf"\cos\theta = \frac{{g}}{{\omega^2 L}} = \frac{{{G}}}{{{omega_k:.4g}^2 \cdot {L_pend:.4g}}} = {cos_th:.4g}\ \Rightarrow\ \theta = {theta:.4g}°")
                st.latex(rf"r = L\sin\theta = {r_k:.4g}\ \text{{m}},\quad v = \omega r = {v_k:.4g}\ \text{{m/s}}")
                st.latex(rf"T_{{snor}} = \frac{{mg}}{{\cos\theta}} = {T_k:.4g}\ \text{{N}}")

    else:
        c1, c2, c3 = st.columns(3)
        r_k = c1.number_input("r – cirkelradius (m)", value=0.25, min_value=1e-6, format="%.6g")
        v_k = c2.number_input("v – hastighed (m/s)", value=2.0, min_value=1e-6, format="%.6g")
        m   = c3.number_input("m – masse (kg)", value=0.1, min_value=1e-12, format="%.6g")
        omega_k = v_k / r_k
        theta   = np.degrees(np.arctan(v_k**2 / (r_k * G)))
        T_k     = m * np.sqrt(G**2 + (v_k**2 / r_k)**2)
        period  = 2 * np.pi / omega_k

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ω (rad/s)", f"{omega_k:.4g}")
        col2.metric("θ (°)", f"{theta:.4g}")
        col3.metric("T_snor (N)", f"{T_k:.4g}")
        col4.metric("Periode (s)", f"{period:.4g}")

        with st.expander("Vis udregning"):
            st.latex(rf"\omega = v/r = {v_k:.4g}/{r_k:.4g} = {omega_k:.4g}\ \text{{rad/s}}")
            st.latex(rf"\tan\theta = \frac{{v^2}}{{rg}} = \frac{{{v_k:.4g}^2}}{{{r_k:.4g}\cdot{G}}} = {v_k**2/(r_k*G):.4g}\ \Rightarrow\ \theta = {theta:.4g}°")
            st.latex(rf"T_{{snor}} = m\sqrt{{g^2 + (v^2/r)^2}} = {T_k:.4g}\ \text{{N}}")

elif formel == "Bernoulli-ligning":
    st.latex(r"p_1 + \tfrac{1}{2}\rho v_1^2 + \rho g h_1 = p_2 + \tfrac{1}{2}\rho v_2^2 + \rho g h_2")
    st.markdown("Ideel (ikke-viskøs, inkompressibel) strømning. Kontinuitetsligning: **A₁v₁ = A₂v₂**.")
    st.divider()

    mode = st.radio("Beregn:", [
        "Hastighed v₂ (given p₁, p₂, v₁, h₁, h₂, ρ)",
        "Torricelli – udstrømningshastighed (hul i beholder)",
        "Differenstryk Δp (given v₁, v₂, h₁, h₂, ρ)",
    ], horizontal=True)
    st.divider()

    if mode == "Hastighed v₂ (given p₁, p₂, v₁, h₁, h₂, ρ)":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Punkt 1**")
            p1   = st.number_input("p₁ – tryk (Pa)", value=101325.0, format="%.6g")
            v1   = st.number_input("v₁ – hastighed (m/s)", value=1.0, min_value=0.0, format="%.6g")
            h1   = st.number_input("h₁ – højde (m)", value=5.0, format="%.6g")
        with c2:
            st.markdown("**Punkt 2**")
            p2   = st.number_input("p₂ – tryk (Pa)", value=101325.0, format="%.6g")
            h2   = st.number_input("h₂ – højde (m)", value=0.0, format="%.6g")
        rho  = st.number_input("ρ – densitet (kg/m³)", value=1000.0, min_value=1e-6, format="%.6g",
                                help="Vand ≈ 1000, Luft ≈ 1.2 kg/m³")

        # p1 + ½ρv1² + ρgh1 = p2 + ½ρv2² + ρgh2
        lhs = p1 + 0.5*rho*v1**2 + rho*G*h1
        rhs_without_v2 = p2 + rho*G*h2
        v2_sq = 2*(lhs - rhs_without_v2)/rho
        if v2_sq < 0:
            st.error(f"Ingen reel løsning: højre side > venstre side. Tjek inputs.")
        else:
            v2 = np.sqrt(v2_sq)
            st.success(f"**v₂ = {v2:.4g} m/s**")
            st.latex(rf"v_2 = \sqrt{{v_1^2 + \frac{{2(p_1-p_2)}}{{\rho}} + 2g(h_1-h_2)}} = {v2:.4g}\ \text{{m/s}}")
            if st.button("📋 Gem v₂", key="gem_dyn_bern_v2"):
                gem_resultat(v2, "m/s", "v₂")

    elif mode == "Torricelli – udstrømningshastighed (hul i beholder)":
        st.latex(r"v = \sqrt{2 g h}")
        st.info("Hul i siden af en åben beholder. h = højde fra hullet til vandoverfladen. p ved overfladen = p ved hullet = atmosfæretryk.")
        c1, c2 = st.columns(2)
        h_tor  = c1.number_input("h – vandhøjde over hullet (m)", value=1.0, min_value=0.0, format="%.6g")
        d_hul  = c2.number_input("d – huldiameter (m, 0 = ignorer)", value=0.0, min_value=0.0, format="%.6g")

        v_tor = np.sqrt(2 * G * h_tor)
        st.success(f"**v = {v_tor:.4g} m/s**")
        st.latex(rf"v = \sqrt{{2gh}} = \sqrt{{2 \cdot {G} \cdot {h_tor:.4g}}} = {v_tor:.4g}\ \text{{m/s}}")
        if d_hul > 0:
            A_hul = np.pi * (d_hul/2)**2
            Q_flow = A_hul * v_tor
            st.info(f"Volumenstrøm: Q = A·v = {A_hul:.4g} m² · {v_tor:.4g} m/s = **{Q_flow:.4g} m³/s** = {Q_flow*1000:.4g} L/s")
        if st.button("📋 Gem v", key="gem_dyn_torr_v"):
            gem_resultat(v_tor, "m/s", "v_Torricelli")

    else:
        st.latex(r"\Delta p = p_1 - p_2 = \tfrac{1}{2}\rho(v_2^2 - v_1^2) + \rho g(h_2 - h_1)")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Punkt 1**")
            v1 = st.number_input("v₁ (m/s)", value=1.0, min_value=0.0, format="%.6g")
            h1 = st.number_input("h₁ (m)", value=0.0, format="%.6g")
        with c2:
            st.markdown("**Punkt 2**")
            v2 = st.number_input("v₂ (m/s)", value=5.0, min_value=0.0, format="%.6g")
            h2 = st.number_input("h₂ (m)", value=0.0, format="%.6g")
        rho = st.number_input("ρ – densitet (kg/m³)", value=1000.0, min_value=1e-6, format="%.6g")

        dp = 0.5*rho*(v2**2 - v1**2) + rho*G*(h2 - h1)
        st.success(f"**Δp = p₁ − p₂ = {dp:.4g} Pa  =  {dp/1e5:.4g} bar**")
        st.latex(rf"\Delta p = \tfrac{{1}}{{2}}\rho(v_2^2-v_1^2) + \rho g(h_2-h_1) = \tfrac{{1}}{{2}}\cdot{rho:.4g}\cdot({v2:.4g}^2-{v1:.4g}^2)+{rho:.4g}\cdot{G}\cdot({h2:.4g}-{h1:.4g}) = {dp:.4g}\ \text{{Pa}}")

elif formel == "Snorpendel – snorkraft ved vilkårlig vinkel":
    st.latex(r"T = m\!\left(\frac{v_0^2}{R} - 2g + 3g\cos\theta\right)")
    st.markdown("""
Snoren starter **lodret** (θ = 0°), loddet har **vandret** starthastighed v₀.
θ måles fra den lodrette position (ned). Energibevarelse + centripetal giver:

- v²(θ) = v₀² − 2gR(1 − cosθ)
- T − mg·cosθ = mv²/R  →  **T = m(v₀²/R − 2g + 3g·cosθ)**

Snoren er vandret ved **θ = 90°**: T = m(v₀²/R − 2g)
""")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    m_sp  = c1.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
    v0_sp = c2.number_input("v₀ – starthastighed nede (m/s)", value=10.0, min_value=0.0, format="%.6g")
    R_sp  = c3.number_input("R – snorlængde (m)", value=1.0, min_value=1e-6, format="%.6g")
    theta_sp = c4.number_input("θ – vinkel fra lodret (°)", value=90.0, min_value=0.0, max_value=180.0, format="%.6g")

    th_r_sp = np.radians(theta_sp)
    v2_sp   = v0_sp**2 - 2*G*R_sp*(1 - np.cos(th_r_sp))
    T_sp    = m_sp * (v0_sp**2/R_sp - 2*G + 3*G*np.cos(th_r_sp))

    col1, col2, col3 = st.columns(3)
    col1.metric("v(θ) – hastighed (m/s)", f"{np.sqrt(max(v2_sp,0)):.4g}" if v2_sp >= 0 else "—")
    col2.metric("T – snorkraft (N)", f"{T_sp:.4g}")
    col3.metric("mg – tyngde (N)", f"{m_sp*G:.4g}")

    if v2_sp < 0:
        v_min = np.sqrt(2*G*R_sp*(1 - np.cos(th_r_sp)))
        st.error(f"Loddet når ikke til θ = {theta_sp:.4g}°. Minimum v₀ for at nå dette punkt: {v_min:.4g} m/s.")
    elif T_sp < 0:
        st.warning(f"T = {T_sp:.4g} N < 0: snoren slapper (loddet er i frit fald). Kræver v₀ ≥ {np.sqrt(R_sp*(2*G - 3*G*np.cos(th_r_sp))):.4g} m/s for stram snor ved θ.")
    else:
        st.success(f"**T = {T_sp:.4g} N** ved θ = {theta_sp:.4g}°")

    with st.expander("Vis udregning"):
        st.latex(rf"v^2(\theta) = v_0^2 - 2gR(1-\cos\theta) = {v0_sp:.4g}^2 - 2\cdot{G}\cdot{R_sp:.4g}\cdot(1-\cos{theta_sp:.4g}°) = {v2_sp:.4g}\ \text{{m}}^2/\text{{s}}^2")
        st.latex(rf"T = m\!\left(\frac{{v_0^2}}{{R}} - 2g + 3g\cos\theta\right) = {m_sp:.4g}\!\left(\frac{{{v0_sp:.4g}^2}}{{{R_sp:.4g}}} - 2\cdot{G} + 3\cdot{G}\cdot\cos{theta_sp:.4g}°\right) = {T_sp:.4g}\ \text{{N}}")

    if abs(m_sp - 1.0) < 0.01 and abs(v0_sp - 10.0) < 0.1 and abs(R_sp - 1.0) < 0.01 and abs(theta_sp - 90.0) < 0.1:
        st.success(f"📋 **2025 Q10** – m=1 kg, v₀=10 m/s, R=1 m, θ=90° → T = {T_sp:.4g} N ✓ (svar F: 80.4 N)")

    if st.button("📋 Gem T", key="gem_dyn_snor_T"):
        gem_resultat(T_sp, "N", "T_snor")

elif formel == "Kraft i vinkel på ru flade":
    st.latex(r"a = \frac{F\cos\theta - \mu_k(mg - F\sin\theta)}{m}")
    st.markdown("Blok (masse **m**) trækkes med kraft **F** i vinkel **θ** over horisontalt underlag med kinetisk friktion **μk**.")
    st.divider()

    mode_kv = st.radio("Beregn:", [
        "a – acceleration",
        "F – kraft for konstant hastighed (a=0)",
        "θ_min – optimal vinkel for mindste F",
    ], horizontal=True)
    st.divider()

    c1_kv, c2_kv, c3_kv, c4_kv = st.columns(4)
    m_kv  = c1_kv.number_input("m – masse (kg)", value=5.0, min_value=1e-12, format="%.6g", key="kv_m")
    mu_kv = c2_kv.number_input("μk – kinetisk friktionskoefficient", value=0.3, min_value=0.0, format="%.6g", key="kv_mu")
    g_kv  = c3_kv.number_input("g (m/s²)", value=G, format="%.6g", key="kv_g")

    if mode_kv == "a – acceleration":
        F_kv    = c4_kv.number_input("F – kraft (N)", value=30.0, min_value=0.0, format="%.6g", key="kv_F")
        theta_kv = st.number_input("θ – kraftens vinkel over vandret (°)", value=20.0, min_value=0.0, max_value=89.9, format="%.6g", key="kv_th")
        th_r_kv = np.radians(theta_kv)
        N_kv    = m_kv * g_kv - F_kv * np.sin(th_r_kv)
        if N_kv < 0:
            st.warning(f"N = {N_kv:.4g} N < 0 — blokken løftes af underlaget. Reducer F eller θ.")
        else:
            f_kv = mu_kv * N_kv
            a_kv = (F_kv * np.cos(th_r_kv) - f_kv) / m_kv
            col1, col2, col3 = st.columns(3)
            col1.metric("N – normalkraft", f"{N_kv:.4g} N")
            col2.metric("f – friktionskraft", f"{f_kv:.4g} N")
            col3.success(f"**a = {a_kv:.4g} m/s²**")
            st.latex(rf"N = mg - F\sin\theta = {m_kv:.4g}\cdot{g_kv:.4g} - {F_kv:.4g}\cdot\sin({theta_kv:.4g}°) = {N_kv:.4g}\ \text{{N}}")
            st.latex(rf"a = \frac{{F\cos\theta - \mu_k N}}{{m}} = \frac{{{F_kv:.4g}\cdot\cos({theta_kv:.4g}°) - {mu_kv:.4g}\cdot{N_kv:.4g}}}{{{m_kv:.4g}}} = {a_kv:.4g}\ \text{{m/s}}^2")
            if a_kv < 0:
                st.info("a < 0: friktionen overvinder trækkraften — blokken bevæger sig ikke (ved a=0-betingelse).")
            if st.button("📋 Gem a", key="gem_kv_a"):
                gem_resultat(a_kv, "m/s²", "a")

    elif mode_kv == "F – kraft for konstant hastighed (a=0)":
        theta_kv = st.number_input("θ – kraftens vinkel over vandret (°)", value=20.0, min_value=0.0, max_value=89.9, format="%.6g", key="kv_th2")
        th_r_kv = np.radians(theta_kv)
        denom_kv = np.cos(th_r_kv) + mu_kv * np.sin(th_r_kv)
        if abs(denom_kv) < 1e-12:
            st.error("Ingen løsning ved denne vinkel.")
        else:
            F_kv = mu_kv * m_kv * g_kv / denom_kv
            N_kv = m_kv * g_kv - F_kv * np.sin(th_r_kv)
            col1, col2 = st.columns(2)
            col1.success(f"**F = {F_kv:.4g} N** (konstant v)")
            col2.metric("N – normalkraft", f"{N_kv:.4g} N")
            st.latex(rf"F = \frac{{\mu_k m g}}{{\cos\theta + \mu_k \sin\theta}} = \frac{{{mu_kv:.4g}\cdot{m_kv:.4g}\cdot{g_kv:.4g}}}{{\cos({theta_kv:.4g}°) + {mu_kv:.4g}\cdot\sin({theta_kv:.4g}°)}} = {F_kv:.4g}\ \text{{N}}")
            if st.button("📋 Gem F", key="gem_kv_F"):
                gem_resultat(F_kv, "N", "F")

    else:
        theta_min = np.degrees(np.arctan(mu_kv))
        th_r_min = np.radians(theta_min)
        F_min_val = mu_kv * m_kv * g_kv / (np.cos(th_r_min) + mu_kv * np.sin(th_r_min))
        st.success(f"**θ_min = arctan(μk) = arctan({mu_kv:.4g}) = {theta_min:.4g}°**")
        st.info(f"Mindste nødvendige kraft ved θ_min: **F_min = {F_min_val:.4g} N**")
        st.latex(rf"\theta_{{min}} = \arctan(\mu_k) = \arctan({mu_kv:.4g}) = {theta_min:.4g}°")
        st.latex(rf"F_{{min}} = \frac{{\mu_k m g}}{{\cos\theta_{{min}} + \mu_k \sin\theta_{{min}}}} = {F_min_val:.4g}\ \text{{N}}")
        with st.expander("Afledning"):
            st.markdown(r"""
**Minimer** $F = \frac{\mu_k m g}{\cos\theta + \mu_k \sin\theta}$ med hensyn til $\theta$:

$\frac{dF}{d\theta} = 0 \implies -\sin\theta + \mu_k\cos\theta = 0 \implies \tan\theta = \mu_k$

$\therefore\; \theta_{min} = \arctan(\mu_k)$
""")

elif formel == "Arkimedes' princip:  F_b = ρ · V · g":
    st.latex(r"F_b = \rho_{\text{fluid}} \cdot V_{\text{nedsænket}} \cdot g")
    beregn = st.radio("Beregn:", [
        "F_b – opdriftskraft (N)",
        "V – nedsænket volumen (m³)",
        "ρ – fluiddensitet (kg/m³)",
        "Flyder / synker?",
    ], horizontal=True)
    st.divider()

    if beregn == "F_b – opdriftskraft (N)":
        c1, c2, c3 = st.columns(3)
        rho_f = c1.number_input("ρ_fluid (kg/m³)", value=1000.0, min_value=1e-6, format="%.6g",
                                 help="Ferskvand=1000, Saltvand≈1025, Luft≈1.2")
        V_ark = c2.number_input("V – nedsænket volumen (m³)", value=0.001, min_value=1e-20, format="%.6g")
        g_ark = c3.number_input("g (m/s²)", value=G, format="%.6g")
        Fb = rho_f * V_ark * g_ark
        st.success(f"**F_b = {Fb:.6g} N**")
        st.latex(rf"F_b = \rho \cdot V \cdot g = {rho_f:.4g} \cdot {V_ark:.4g} \cdot {g_ark:.4g} = {Fb:.4g}\ \text{{N}}")
        if st.button("📋 Gem F_b", key="gem_ark_Fb"):
            gem_resultat(Fb, "N", "F_b")

    elif beregn == "V – nedsænket volumen (m³)":
        c1, c2, c3 = st.columns(3)
        Fb = c1.number_input("F_b – opdriftskraft (N)", value=9.82, format="%.6g")
        rho_f = c2.number_input("ρ_fluid (kg/m³)", value=1000.0, min_value=1e-6, format="%.6g")
        g_ark = c3.number_input("g (m/s²)", value=G, format="%.6g")
        V_ark = Fb / (rho_f * g_ark)
        st.success(f"**V = {V_ark:.6g} m³**")
        st.latex(rf"V = \frac{{F_b}}{{\rho g}} = \frac{{{Fb:.4g}}}{{{rho_f:.4g} \cdot {g_ark:.4g}}} = {V_ark:.4g}\ \text{{m}}^3")
        if st.button("📋 Gem V", key="gem_ark_V"):
            gem_resultat(V_ark, "m³", "V")

    elif beregn == "ρ – fluiddensitet (kg/m³)":
        c1, c2, c3 = st.columns(3)
        Fb = c1.number_input("F_b – opdriftskraft (N)", value=9.82, format="%.6g")
        V_ark = c2.number_input("V – volumen (m³)", value=0.001, min_value=1e-20, format="%.6g")
        g_ark = c3.number_input("g (m/s²)", value=G, format="%.6g")
        rho_f = Fb / (V_ark * g_ark)
        st.success(f"**ρ = {rho_f:.6g} kg/m³**")
        st.latex(rf"\rho = \frac{{F_b}}{{V \cdot g}} = \frac{{{Fb:.4g}}}{{{V_ark:.4g} \cdot {g_ark:.4g}}} = {rho_f:.4g}\ \text{{kg/m}}^3")
        if st.button("📋 Gem ρ", key="gem_ark_rho"):
            gem_resultat(rho_f, "kg/m³", "ρ")

    else:
        st.markdown("**Flyder / synker?** — Sammenlign densiteter")
        c1, c2, c3 = st.columns(3)
        rho_obj = c1.number_input("ρ_objekt (kg/m³)", value=800.0, min_value=1e-6, format="%.6g",
                                   help="Balsatræ≈120, Egetræ≈700, Is≈917, Aluminium≈2700, Stål≈7800")
        rho_fl  = c2.number_input("ρ_fluid (kg/m³)", value=1000.0, min_value=1e-6, format="%.6g")
        m_obj   = c3.number_input("m – masse (kg)", value=1.0, min_value=1e-12, format="%.6g")
        V_tot = m_obj / rho_obj
        if rho_obj < rho_fl:
            frac = rho_obj / rho_fl
            V_sub = frac * V_tot
            st.success(f"**Flyder!** ρ_obj = {rho_obj:.4g} < ρ_fluid = {rho_fl:.4g}")
            st.info(f"Nedsænket brøkdel: {frac*100:.2f}%  →  V_sub = {V_sub:.4g} m³")
            st.latex(rf"\frac{{V_{{sub}}}}{{V_{{tot}}}} = \frac{{\rho_{{obj}}}}{{\rho_{{fluid}}}} = \frac{{{rho_obj:.4g}}}{{{rho_fl:.4g}}} = {frac:.4f}")
        elif rho_obj > rho_fl:
            st.error(f"**Synker!** ρ_obj = {rho_obj:.4g} > ρ_fluid = {rho_fl:.4g}")
            Fb_val = rho_fl * V_tot * G
            Fg_val = m_obj * G
            st.info(f"F_b = {Fb_val:.4g} N  vs  F_g = {Fg_val:.4g} N  →  Nettokraft nedad = {Fg_val - Fb_val:.4g} N")
        else:
            st.info("ρ_obj = ρ_fluid → neutralt opdrift (svæver)")

elif formel == "Terminal hastighed:  v_T = √(2mg / CρA)":
    st.latex(r"v_T = \sqrt{\frac{2mg}{C \rho A}} \qquad F_{\text{drag}} = \tfrac{1}{2}C\rho A v^2")
    st.info("C ≈ 0.47 for kugle, ≈ 1.0 for cylinder, ≈ 1.3 for flad plade")
    beregn = st.radio("Beregn:", [
        "v_T – terminalhastighed (m/s)",
        "F_drag – luftmodstand ved given v",
        "m – masse fra v_T",
    ], horizontal=True)
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    m_t   = c1.number_input("m – masse (kg)", value=0.01, min_value=1e-12, format="%.6g", key="term_m")
    C_t   = c2.number_input("C – modstandskoefficient", value=0.47, min_value=1e-6, format="%.6g", key="term_C")
    rho_t = c3.number_input("ρ_luft (kg/m³)", value=1.225, min_value=1e-6, format="%.6g", key="term_rho")
    A_t   = c4.number_input("A – frontareal (m²)", value=float(np.pi * 0.02**2), min_value=1e-12, format="%.6g",
                              help="Kugle r=2cm: πr²", key="term_A")

    if beregn == "v_T – terminalhastighed (m/s)":
        g_t = st.number_input("g (m/s²)", value=G, format="%.6g", key="term_g")
        vT = np.sqrt(2 * m_t * g_t / (C_t * rho_t * A_t))
        st.success(f"**v_T = {vT:.4g} m/s  =  {vT*3.6:.4g} km/h**")
        st.latex(rf"v_T = \sqrt{{\frac{{2mg}}{{C\rho A}}}} = \sqrt{{\frac{{2\cdot{m_t:.4g}\cdot{g_t:.4g}}}{{{C_t:.4g}\cdot{rho_t:.4g}\cdot{A_t:.4g}}}}} = {vT:.4g}\ \text{{m/s}}")
        if st.button("📋 Gem v_T", key="gem_term_vT"):
            gem_resultat(vT, "m/s", "v_T")

    elif beregn == "F_drag – luftmodstand ved given v":
        v_given = st.number_input("v – aktuel hastighed (m/s)", value=10.0, min_value=0.0, format="%.6g", key="term_v")
        Fdrag = 0.5 * C_t * rho_t * A_t * v_given**2
        vT = np.sqrt(2 * m_t * G / (C_t * rho_t * A_t))
        st.success(f"**F_drag = {Fdrag:.4g} N**")
        st.latex(rf"F_{{drag}} = \tfrac{{1}}{{2}}C\rho A v^2 = \tfrac{{1}}{{2}}\cdot{C_t:.4g}\cdot{rho_t:.4g}\cdot{A_t:.4g}\cdot{v_given:.4g}^2 = {Fdrag:.4g}\ \text{{N}}")
        st.info(f"Terminalhastighed: v_T = {vT:.4g} m/s = {vT*3.6:.4g} km/h")
        if st.button("📋 Gem F_drag", key="gem_term_Fd"):
            gem_resultat(Fdrag, "N", "F_drag")

    else:
        vT_given = st.number_input("v_T – terminalhastighed (m/s)", value=30.0, min_value=1e-6, format="%.6g", key="term_vT2")
        g_t2 = st.number_input("g (m/s²)", value=G, format="%.6g", key="term_g2")
        m_calc = 0.5 * C_t * rho_t * A_t * vT_given**2 / g_t2
        st.success(f"**m = {m_calc:.4g} kg**")
        st.latex(rf"m = \frac{{C\rho A v_T^2}}{{2g}} = \frac{{{C_t:.4g}\cdot{rho_t:.4g}\cdot{A_t:.4g}\cdot{vT_given:.4g}^2}}{{2\cdot{g_t2:.4g}}} = {m_calc:.4g}\ \text{{kg}}")
        if st.button("📋 Gem m", key="gem_term_m2"):
            gem_resultat(m_calc, "kg", "m")

elif formel == "Satellit og Keplers 3. lov":
    G_grav_s = 6.674e-11
    M_earth_s = 5.97e24
    R_earth_s = 6.371e6
    st.latex(r"v = \sqrt{\frac{GM}{r}} \qquad T = \frac{2\pi r}{v} \qquad T^2 = \frac{4\pi^2}{GM}\,r^3")
    st.info(f"G = {G_grav_s:.4g} N·m²/kg²   M_jord = {M_earth_s:.4g} kg   R_jord = {R_earth_s:.4g} m")
    beregn = st.radio("Beregn:", [
        "v og T fra r (orbital­radius)",
        "r fra T (omløbstid)",
        "v_e – undvigelseshastighed",
        "Keplers 3. lov: T₁/T₂ fra r₁/r₂",
    ], horizontal=True)
    st.divider()

    if beregn == "v og T fra r (orbital­radius)":
        c1, c2 = st.columns(2)
        M_c = c1.number_input("M – centralmasse (kg)", value=M_earth_s, format="%.6g",
                               help=f"Jordens masse: {M_earth_s:.4g} kg")
        r_c = c2.number_input("r – orbitalradius (m)", value=R_earth_s + 400e3, format="%.6g",
                               help=f"ISS: R_jord + 400 km = {R_earth_s + 400e3:.4g} m")
        v_orb = np.sqrt(G_grav_s * M_c / r_c)
        T_orb = 2 * np.pi * r_c / v_orb
        st.success(f"**v = {v_orb:.4g} m/s**   **T = {T_orb:.4g} s = {T_orb/60:.4g} min**")
        st.latex(rf"v = \sqrt{{\frac{{GM}}{{r}}}} = {v_orb:.4g}\ \text{{m/s}},\quad T = \frac{{2\pi r}}{{v}} = {T_orb:.4g}\ \text{{s}}")
        if r_c > R_earth_s:
            st.caption(f"Højde over Jordan: {(r_c - R_earth_s)/1e3:.4g} km")
        if st.button("📋 Gem v", key="gem_sat_v"):
            gem_resultat(v_orb, "m/s", "v_orbital")

    elif beregn == "r fra T (omløbstid)":
        c1, c2 = st.columns(2)
        M_c = c1.number_input("M – centralmasse (kg)", value=M_earth_s, format="%.6g")
        T_c = c2.number_input("T – omløbstid (s)", value=5400.0, format="%.6g", help="ISS ≈ 5540 s ≈ 92 min")
        r_c = (G_grav_s * M_c * T_c**2 / (4 * np.pi**2))**(1/3)
        v_c = 2 * np.pi * r_c / T_c
        st.success(f"**r = {r_c:.4g} m**   (v = {v_c:.4g} m/s)")
        st.latex(rf"r = \left(\frac{{GMT^2}}{{4\pi^2}}\right)^{{1/3}} = {r_c:.4g}\ \text{{m}}")
        if r_c > R_earth_s:
            st.caption(f"Højde over Jordan: {(r_c - R_earth_s)/1e3:.4g} km")
        if st.button("📋 Gem r", key="gem_sat_r"):
            gem_resultat(r_c, "m", "r")

    elif beregn == "v_e – undvigelseshastighed":
        c1, c2 = st.columns(2)
        M_c = c1.number_input("M – masse (kg)", value=M_earth_s, format="%.6g")
        r_c = c2.number_input("r – afstand fra centrum (m)", value=R_earth_s, format="%.6g",
                               help="Jordens radius: 6.371e6 m")
        v_e = np.sqrt(2 * G_grav_s * M_c / r_c)
        v_orb_e = np.sqrt(G_grav_s * M_c / r_c)
        st.success(f"**v_e = {v_e:.4g} m/s  =  {v_e/1e3:.4g} km/s**")
        st.info(f"Orbitalhastighed samme afstand: {v_orb_e:.4g} m/s  (v_e = √2 · v_orb)")
        st.latex(rf"v_e = \sqrt{{\frac{{2GM}}{{r}}}} = {v_e:.4g}\ \text{{m/s}}")
        if st.button("📋 Gem v_e", key="gem_sat_ve"):
            gem_resultat(v_e, "m/s", "v_e")

    else:
        st.markdown("Keplers 3. lov: **T² ∝ r³**")
        st.latex(r"\frac{T_1^2}{T_2^2} = \frac{r_1^3}{r_2^3}")
        kepler_mode = st.radio("Find:", ["T₁ (given r₁, r₂, T₂)", "r₁ (given T₁, T₂, r₂)"], horizontal=True)
        c1, c2, c3 = st.columns(3)
        if kepler_mode == "T₁ (given r₁, r₂, T₂)":
            r1_k = c1.number_input("r₁ (m)", value=R_earth_s + 400e3, format="%.6g", key="kep_r1")
            r2_k = c2.number_input("r₂ (m)", value=R_earth_s + 2000e3, format="%.6g", key="kep_r2")
            T2_k = c3.number_input("T₂ (s)", value=7128.0, format="%.6g", key="kep_T2")
            T1_k = T2_k * (r1_k / r2_k)**(3/2)
            st.success(f"**T₁ = {T1_k:.4g} s = {T1_k/60:.4g} min**")
            st.latex(rf"T_1 = T_2\!\left(\frac{{r_1}}{{r_2}}\right)^{{3/2}} = {T2_k:.4g}\cdot\left(\frac{{{r1_k:.4g}}}{{{r2_k:.4g}}}\right)^{{3/2}} = {T1_k:.4g}\ \text{{s}}")
        else:
            T1_k = c1.number_input("T₁ (s)", value=5540.0, format="%.6g", key="kep_T1b")
            T2_k = c2.number_input("T₂ (s)", value=7128.0, format="%.6g", key="kep_T2b")
            r2_k = c3.number_input("r₂ (m)", value=R_earth_s + 2000e3, format="%.6g", key="kep_r2b")
            r1_k = r2_k * (T1_k / T2_k)**(2/3)
            st.success(f"**r₁ = {r1_k:.4g} m**")
            st.latex(rf"r_1 = r_2\!\left(\frac{{T_1}}{{T_2}}\right)^{{2/3}} = {r2_k:.4g}\cdot\left(\frac{{{T1_k:.4g}}}{{{T2_k:.4g}}}\right)^{{2/3}} = {r1_k:.4g}\ \text{{m}}")

elif formel == "Statisk ligevægt:  ΣF = 0 og Στ = 0":
    st.latex(r"\sum F = 0 \qquad \sum \tau = 0")
    st.markdown("Legemet er i hvile. Vælg omdrejningspunkt klogt for at eliminere ukendte kræfter.")
    beregn = st.radio("Scenarie:", [
        "Bjælke på hængsel + snor",
        "To understøtninger – punktlaster",
        "Vippepunkt: hvornår tipper kassen?",
    ], horizontal=True)
    st.divider()

    if beregn == "Bjælke på hængsel + snor":
        st.markdown("Vandret bjælke (masse M, længde L) med hængsel i venstre ende og skrå snor ved højre ende.")
        st.latex(r"T\sin\phi \cdot L = Mg\cdot\frac{L}{2} + F_{\text{last}}\cdot d")
        c1, c2, c3, c4, c5 = st.columns(5)
        M_bj   = c1.number_input("M – bjælkemasse (kg)", value=10.0, min_value=0.0, format="%.6g", key="liev_M")
        L_bj   = c2.number_input("L – bjælkelængde (m)", value=2.0, min_value=1e-6, format="%.6g", key="liev_L")
        F_last = c3.number_input("F_last – last (N)", value=50.0, min_value=0.0, format="%.6g", key="liev_Fl")
        d_last = c4.number_input("d – lastens afstand fra hængsel (m)", value=1.5, min_value=0.0, format="%.6g", key="liev_d")
        phi_deg = c5.number_input("φ – snorvinkel over vandret (°)", value=45.0, min_value=1.0, max_value=89.9, format="%.6g", key="liev_phi")
        phi_r = np.radians(phi_deg)
        T_snor = (M_bj * G * L_bj / 2 + F_last * d_last) / (L_bj * np.sin(phi_r))
        H_x = T_snor * np.cos(phi_r)
        V_y = M_bj * G + F_last - T_snor * np.sin(phi_r)
        col1, col2, col3 = st.columns(3)
        col1.metric("Snorkraft T", f"{T_snor:.4g} N")
        col2.metric("Hængselsreaktion x", f"{H_x:.4g} N")
        col3.metric("Hængselsreaktion y", f"{V_y:.4g} N")
        st.latex(rf"T = \frac{{MgL/2 + F_{{last}}d}}{{L\sin\phi}} = \frac{{{M_bj:.4g}\cdot{G}\cdot{L_bj:.4g}/2 + {F_last:.4g}\cdot{d_last:.4g}}}{{{L_bj:.4g}\cdot\sin({phi_deg:.4g}°)}} = {T_snor:.4g}\ \text{{N}}")
        if st.button("📋 Gem T_snor", key="gem_liev_T"):
            gem_resultat(T_snor, "N", "T_snor")

    elif beregn == "To understøtninger – punktlaster":
        st.markdown("Bjælke understøttet i A (x=0) og B (x=L). Tag moment om A: R_B·L = ΣF_i·x_i + Mg·L/2.")
        c1, c2 = st.columns(2)
        L_b2 = c1.number_input("L – spænd (m)", value=4.0, min_value=1e-6, format="%.6g", key="liev2_L")
        M_b2 = c2.number_input("M – bjælkemasse (kg, 0=masseløs)", value=0.0, min_value=0.0, format="%.6g", key="liev2_M")
        n_laster = st.number_input("Antal punktlaster", value=2, min_value=1, max_value=5, step=1, key="liev2_n")
        F_vals, d_vals = [], []
        cols_f = st.columns(int(n_laster))
        for i in range(int(n_laster)):
            with cols_f[i]:
                F_vals.append(st.number_input(f"F_{i+1} (N)", value=100.0 if i == 0 else 200.0,
                                               format="%.6g", key=f"liev_F_{i}"))
                d_vals.append(st.number_input(f"x_{i+1} (m)", value=1.0 if i == 0 else 3.0,
                                               min_value=0.0, max_value=float(L_b2),
                                               format="%.6g", key=f"liev_d_{i}"))
        tau_om_A = sum(F * d for F, d in zip(F_vals, d_vals)) + M_b2 * G * L_b2 / 2
        R_B = tau_om_A / L_b2
        R_A = sum(F_vals) + M_b2 * G - R_B
        col1, col2 = st.columns(2)
        col1.success(f"**R_A = {R_A:.4g} N**")
        col2.success(f"**R_B = {R_B:.4g} N**")
        st.latex(rf"R_B = \frac{{\sum F_i x_i + Mg\cdot L/2}}{{L}} = {R_B:.4g}\ \text{{N}},\quad R_A = {R_A:.4g}\ \text{{N}}")
        if st.button("📋 Gem R_A", key="gem_liev_RA"):
            gem_resultat(R_A, "N", "R_A")

    else:
        st.markdown("Kasse (bredde b, højde h, masse M) skubbes med vandret kraft F. Hvornår tipper fremfor at glide?")
        st.latex(r"F_{\text{tip}} = \frac{Mgb}{2h} \qquad F_{\text{glide}} = \mu M g")
        c1, c2, c3, c4 = st.columns(4)
        M_k  = c1.number_input("M – masse (kg)", value=20.0, min_value=1e-12, format="%.6g", key="tip_M")
        b_k  = c2.number_input("b – bredde (m)", value=0.5, min_value=1e-6, format="%.6g", key="tip_b")
        h_k  = c3.number_input("h – højde (m)", value=1.0, min_value=1e-6, format="%.6g", key="tip_h")
        mu_k2 = c4.number_input("μ – friktionskoefficient", value=0.4, min_value=0.0, format="%.6g", key="tip_mu")
        F_tip = M_k * G * b_k / (2 * h_k)
        F_glide = mu_k2 * M_k * G
        col1, col2 = st.columns(2)
        col1.metric("F_tip – tipper", f"{F_tip:.4g} N")
        col2.metric("F_glide – glider", f"{F_glide:.4g} N")
        if F_tip < F_glide:
            st.success(f"**Tipper** inden den glider  (F_tip {F_tip:.4g} N < F_glide {F_glide:.4g} N)")
        elif F_glide < F_tip:
            st.info(f"**Glider** inden den tipper  (F_glide {F_glide:.4g} N < F_tip {F_tip:.4g} N)")
        else:
            st.info("Tipper og glider samtid.")

elif formel == "To-snors ophæng:  T₁ og T₂":
    st.latex(r"T_1 = \frac{mg\cos\theta_2}{\sin(\theta_1+\theta_2)} \qquad T_2 = \frac{mg\cos\theta_1}{\sin(\theta_1+\theta_2)}")
    st.markdown(
        "En masse **m** hænger fra loftet i to snore, der danner vinklerne **θ₁** og **θ₂** med lodret. "
        "Fra ΣFₓ = 0: T₁sin θ₁ = T₂sin θ₂, og ΣFᵧ = 0: T₁cos θ₁ + T₂cos θ₂ = mg."
    )
    st.info("💡 Vinklerne er målt fra **lodret** til snoren. Hvis opgaven angiver vinklen fra vandret, trækker du den fra 90°.")
    st.divider()

    c1, c2, c3 = st.columns(3)
    m_snor  = c1.number_input("m – masse (kg)", value=5.0, min_value=1e-12, format="%.6g", key="tsnor_m")
    th1_deg = c2.number_input("θ₁ – vinkel fra lodret, snor 1 (°)", value=30.0, min_value=0.1, max_value=89.9, format="%.6g", key="tsnor_t1")
    th2_deg = c3.number_input("θ₂ – vinkel fra lodret, snor 2 (°)", value=45.0, min_value=0.1, max_value=89.9, format="%.6g", key="tsnor_t2")

    th1_r = np.radians(th1_deg)
    th2_r = np.radians(th2_deg)
    denom = np.sin(th1_r + th2_r)

    if abs(denom) < 1e-12:
        st.error("θ₁ + θ₂ = 180° → singulær (parallelle snore). Prøv andre vinkler.")
    else:
        mg = m_snor * G
        T1 = mg * np.cos(th2_r) / denom
        T2 = mg * np.cos(th1_r) / denom
        ratio = T2 / T1

        col1, col2, col3 = st.columns(3)
        col1.metric("T₁", f"{T1:.4g} N")
        col2.metric("T₂", f"{T2:.4g} N")
        col3.metric("T₂/T₁", f"{ratio:.4g}")

        st.latex(
            rf"T_1 = \frac{{mg\cos\theta_2}}{{\sin(\theta_1+\theta_2)}} "
            rf"= \frac{{{mg:.4g}\cdot\cos({th2_deg:.4g}°)}}{{\sin({th1_deg:.4g}°+{th2_deg:.4g}°)}} = {T1:.4g}\ \text{{N}}"
        )
        st.latex(
            rf"T_2 = \frac{{mg\cos\theta_1}}{{\sin(\theta_1+\theta_2)}} "
            rf"= \frac{{{mg:.4g}\cdot\cos({th1_deg:.4g}°)}}{{\sin({th1_deg:.4g}°+{th2_deg:.4g}°)}} = {T2:.4g}\ \text{{N}}"
        )
        st.markdown(f"**Kontrol:** T₁cosθ₁ + T₂cosθ₂ = {T1*np.cos(th1_r) + T2*np.cos(th2_r):.4g} N  ≈  mg = {mg:.4g} N")

        col_g1, col_g2 = st.columns(2)
        if col_g1.button("📋 Gem T₁", key="gem_T1_snor"):
            gem_resultat(T1, "N", "T₁")
        if col_g2.button("📋 Gem T₂", key="gem_T2_snor"):
            gem_resultat(T2, "N", "T₂")

elif formel == "To-klods system:  CM-acceleration":
    st.latex(r"a_\text{CM} = \frac{F_\text{ekstern}}{M_\text{total}}")
    st.markdown(
        "Klods **m₁** (øverste) og **m₂** (nederste) på **glat** underlag. "
        "Vandret kraft **F** trækkes i øverste klods. Friktion *mellem* klodserne er en intern kraft "
        "og påvirker **ikke** massemidtpunktets acceleration."
    )
    st.info("💡 Nøgleindsigt: a_CM afhænger kun af den *ydre* kraft og den *samlede* masse, "
            "uanset om klodserne glider på hinanden eller ej.")
    st.divider()

    c1, c2, c3, c4, c5 = st.columns(5)
    m1_tk = c1.number_input("m₁ – øverste klods (kg)", value=1.0, min_value=1e-9, format="%.6g", key="tk_m1")
    m2_tk = c2.number_input("m₂ – nederste klods (kg)", value=1.0, min_value=1e-9, format="%.6g", key="tk_m2")
    F_tk  = c3.number_input("F – vandret kraft på m₁ (N)", value=20.0, format="%.6g", key="tk_F")
    mu_s  = c4.number_input("μₛ – statisk friktionskoeff.", value=0.80, min_value=0.0, format="%.6g", key="tk_mus")
    mu_k  = c5.number_input("μₖ – kinetisk friktionskoeff.", value=0.50, min_value=0.0, format="%.6g", key="tk_muk")

    M_tot = m1_tk + m2_tk
    a_cm = F_tk / M_tot

    # Glidningstest: hvis de bevæger sig SAMMEN, kræver det friktion = m2*a_cm på m2
    f_needed = m2_tk * a_cm          # friktionskraft der skal til for at m2 følger med
    f_max_s  = mu_s * m2_tk * G      # maks. statisk friktion (normalkraft = m2*g)
    glider   = f_needed > f_max_s

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("a_CM", f"{a_cm:.4g} m/s²")
    col2.metric("Krævet friktion (m₂·a_CM)", f"{f_needed:.4g} N")
    col3.metric("Maks. statisk friktion", f"{f_max_s:.4g} N")

    if glider:
        f_kin = mu_k * m2_tk * G
        a1 = (F_tk - f_kin) / m1_tk
        a2 = f_kin / m2_tk
        st.error(
            f"**Klodserne GLIDER på hinanden** (krævet friktion {f_needed:.4g} N > μₛ·m₂g = {f_max_s:.4g} N). "
            f"Kinetisk friktion = {f_kin:.4g} N."
        )
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("a₁ (øverste)", f"{a1:.4g} m/s²")
        col_b.metric("a₂ (nederste)", f"{a2:.4g} m/s²")
        col_c.metric("a_CM = F/M_total", f"{a_cm:.4g} m/s²", delta="uændret!")
        st.latex(
            rf"a_1 = \frac{{F - \mu_k m_2 g}}{{m_1}} = \frac{{{F_tk:.4g} - {f_kin:.4g}}}{{{m1_tk:.4g}}} = {a1:.4g}\ \text{{m/s}}^2"
        )
        st.latex(
            rf"a_2 = \frac{{\mu_k m_2 g}}{{m_2}} = \frac{{{f_kin:.4g}}}{{{m2_tk:.4g}}} = {a2:.4g}\ \text{{m/s}}^2"
        )
    else:
        st.success(
            f"**Klodserne bevæger sig SAMMEN** (krævet friktion {f_needed:.4g} N ≤ μₛ·m₂g = {f_max_s:.4g} N)."
        )

    st.latex(
        rf"a_{{\text{{CM}}}} = \frac{{F}}{{m_1 + m_2}} = \frac{{{F_tk:.4g}}}{{{m1_tk:.4g} + {m2_tk:.4g}}} = {a_cm:.4g}\ \text{{m/s}}^2"
    )
    if st.button("📋 Gem a_CM", key="gem_acm"):
        gem_resultat(a_cm, "m/s²", "a_CM")
