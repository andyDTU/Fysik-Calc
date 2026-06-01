import streamlit as st
from utils import show_sidebar_constants, show_resultat_sidebar, FORMLER

st.set_page_config(page_title="Søg formel", page_icon="🔍", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()

st.title("⚡ Fysik-Calc")
st.markdown("Søg med et stikord — eller vælg direkte fra eksamensguiden nedenfor.")
st.divider()

# ── Søgefelt ──────────────────────────────────────────────────────────────────
søg = st.text_input("🔍 Søg:",
                    placeholder="fx 'bremser', 'passer målingen', 'halveringstid', 'log-log', 'hænger fast'...",
                    label_visibility="collapsed")

st.divider()

SIDER = [
    ("🏃", "Kinematik",          "pages/1_Kinematik.py",         "kin_formel"),
    ("💪", "Dynamik",            "pages/2_Dynamik.py",           "dyn_formel"),
    ("🔋", "Energi",             "pages/3_Energi.py",            "energi_formel"),
    ("⚡", "Elektricitet",       "pages/4_Elektricitet.py",      "elek_formel"),
    ("🌊", "Bølger & Optik",    "pages/5_Boelger_og_Optik.py",  "bolge_formel"),
    ("🌡️", "Termodynamik",       "pages/6_Termodynamik.py",      "termo_formel"),
    ("☢️", "Atomfysik",          "pages/7_Atomfysik.py",         "atom_formel"),
    ("📏", "Usikkerhed",         "pages/8_Usikkerhed.py",        "usk_formel"),
    ("🔄", "Rotation",           "pages/9_Rotation.py",          "rot_formel"),
    ("💥", "Kollisioner",        "pages/10_Kollisioner.py",      "kol_formel"),
    ("〰️", "Svingninger",        "pages/11_Svingninger.py",      "sving_formel"),
    ("🚀", "Relativitetsteori",  "pages/12_Relativitetsteori.py","rel_formel"),
]

søg_lc = søg.strip().lower()

if søg_lc:
    # ── Søgeresultater ────────────────────────────────────────────────────────
    hits = [
        f for f in FORMLER
        if søg_lc in f["navn"].lower() or søg_lc in f["kw"].lower()
    ]

    if not hits:
        st.warning("Ingen formler matchede. Prøv et andet søgeord.")
    else:
        alle_sider_ord = [s[1] for s in SIDER]
        sider_i_hits = []
        for s in alle_sider_ord:
            gruppe = [f for f in hits if f["side"] == s]
            if gruppe:
                sider_i_hits.append((s, gruppe))

        for side_navn, formler in sider_i_hits:
            emoji = next((s[0] for s in SIDER if s[1] == side_navn), "📐")
            st.markdown(f"### {emoji} {side_navn}")
            for f in formler:
                col1, col2 = st.columns([5, 1])
                col1.markdown(f"**{f['navn']}**")
                if col2.button("→ Åbn", key=f"btn_{f['navn']}"):
                    st.session_state[f["key"]] = f["navn"]
                    st.switch_page(f["fil"])
            st.markdown("")

        st.caption(f"{len(hits)} formel(er) fundet for '{søg}'")

else:
    # ── Eksamensguide ─────────────────────────────────────────────────────────
    st.markdown("### 📋 Hvad handler opgaven om?")
    st.caption("Klik **→** ud for den situation der passer — du lander direkte i den rigtige beregner.")

    def _g(label, btn_key, ss_key, ss_val, page):
        c1, c2 = st.columns([8, 1])
        c1.markdown(label)
        if c2.button("→", key=btn_key, use_container_width=True):
            st.session_state[ss_key] = ss_val
            st.switch_page(page)

    tab_bev, tab_en, tab_data, tab_atom, tab_rot = st.tabs([
        "🏃 Bevægelse & Kræfter",
        "⚡ Energi",
        "📏 Data & Usikkerhed",
        "☢️ Atom & Termo",
        "🔄 Rotation & Kollision",
    ])

    with tab_bev:
        _g("Beregn **acceleration** eller **kraft**  (F = m·a)",
           "g_Fma", "dyn_formel", "Newtons 2. lov:  F = m · a", "pages/2_Dynamik.py")
        _g("**Bremser / accelererer** — hvad er **hastighed** efter tid t?",
           "g_vat", "kin_formel", "Jævnt accelereret (1):  v = v₀ + a · t", "pages/1_Kinematik.py")
        _g("Hvad er **strækning** / hvornår stopper / ankommer?",
           "g_svt", "kin_formel", "Jævnt accelereret (2):  s = v₀·t + ½·a·t²", "pages/1_Kinematik.py")
        _g("Hvad er **hastighed** givet strækning — ingen tid?  (v² = v₀² + 2as)",
           "g_v2", "kin_formel", "Jævnt accelereret (3):  v² = v₀² + 2·a·s", "pages/1_Kinematik.py")
        _g("**Kastes vandret** fra høj bygning / klippe / bord",
           "g_kv", "kin_formel", "Kastebevægelse (vandret kast)", "pages/1_Kinematik.py")
        _g("**Skyder i vinkel** θ — rækkevidde, max højde, landingstid",
           "g_ks", "kin_formel", "Kastebevægelse (skråt kast)", "pages/1_Kinematik.py")
        _g("**Cirkulær bevægelse** — centripetalkraft, periode, RPM",
           "g_circ", "dyn_formel", "Centripetalkraft:  Fc = m · v² / r", "pages/2_Dynamik.py")
        _g("**Skråplan / heldning** — acceleration, friktion, normalkraft",
           "g_skra", "dyn_formel", "Hældende plan", "pages/2_Dynamik.py")
        _g("**Snor over trisse**, to hængende masser  (Atwood)",
           "g_atw", "dyn_formel", "Atwood-maskine:  to masser over trisse", "pages/2_Dynamik.py")
        _g("**Planet / satellit** — gravitationskraft falder med afstand²",
           "g_grav", "dyn_formel", "Gravitationsloven:  F = G·m₁·m₂ / r²", "pages/2_Dynamik.py")
        _g("**Trykforskel / Bernoulli** — ideel væske, udstrømning",
           "g_bern", "dyn_formel", "Bernoulli-ligning", "pages/2_Dynamik.py")

    with tab_en:
        _g("Hvad er **hastighed i bunden / toppen** af en bane?  (energibevarelse)",
           "g_ener", "energi_formel", "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂", "pages/3_Energi.py")
        _g("**Fjeder komprimeres** af faldende masse — maks. kompression d?",
           "g_ffjed", "energi_formel", "Fjeder – maks. kompression ved fald", "pages/3_Energi.py")
        _g("**Pendul** frigives fra vinkel θ — hastighed og snorkraft i bunden?",
           "g_pend", "energi_formel", "Pendul – hastighed og snorkraft (energibevarelse)", "pages/3_Energi.py")
        _g("**Fjederkraft / fjederkonstant k** — Hookes lov, energi i fjeder",
           "g_fjed", "energi_formel", "Fjederkraft og -energi", "pages/3_Energi.py")
        _g("Beregn **arbejde** W = F·s·cosθ",
           "g_arb", "energi_formel", "Arbejde:  W = F · s · cos(θ)", "pages/3_Energi.py")
        _g("**Effektivitet / virkningsgrad** η  [%]",
           "g_eta", "energi_formel", "Mekanisk virkningsgrad:  η = P_ud / P_ind", "pages/3_Energi.py")

    with tab_data:
        _g("**Usikkerhed på beregnet resultat** — funktion af usikre variable",
           "g_fejl", "usk_formel", "Fejlpropagation – generel (numerisk)", "pages/8_Usikkerhed.py")
        _g("**Passer ny måling** / er resultatet forenelig med teorien?",
           "g_foren", "usk_formel", "Forenelighedstest – er ny måling OK?", "pages/8_Usikkerhed.py")
        _g("**Gennemsnit og standardafvigelse** — n gentagne målinger",
           "g_mean", "usk_formel", "Gennemsnit og standardafvigelse", "pages/8_Usikkerhed.py")
        _g("**Fit til potenslov** — T ∝ k^α, log-log  *(np.array data fra eksamen)*",
           "g_pot", "usk_formel", "Potenslov-fitting:  y = A · xᵅ  (log-log regression)", "pages/8_Usikkerhed.py")
        _g("**Lineær sammenhæng** — find hældning a og skæring b",
           "g_lin", "usk_formel", "Lineær regression:  y = a · x + b", "pages/8_Usikkerhed.py")
        _g("**Eksponentielt henfald i data** — semi-log fit, find λ og T½  *(np.array)*",
           "g_exp", "usk_formel", "Eksponentielt fit:  y = A · eᵇˣ  (semi-log regression)", "pages/8_Usikkerhed.py")
        _g("**Hastighed fra positionsdata** — v fra x(t), a fra v(t)  *(np.array)*",
           "g_diff", "usk_formel", "Numerisk differentiation:  dy/dx fra arrays", "pages/8_Usikkerhed.py")
        _g("**Impuls fra kraft-tid** ∫F dt  eller  **arbejde** ∫F dx  *(np.array)*",
           "g_int", "usk_formel", "Numerisk integration:  ∫y dx (trapezregel)", "pages/8_Usikkerhed.py")

    with tab_atom:
        _g("**Halvvejstid / halveringstid** T½  ↔  henfaldskonstant λ",
           "g_T12", "atom_formel", "Halvvejstid:  T½ = ln(2) / λ", "pages/7_Atomfysik.py")
        _g("Hvad er **aktiviteten** A [Bq] nu eller efter tid t?",
           "g_akt", "atom_formel", "Aktivitet:  A = λ · N", "pages/7_Atomfysik.py")
        _g("**Radioaktivt henfald** — hvad er N(t) / hvornår er X tilbage?",
           "g_Nt", "atom_formel", "Radioaktivt henfald:  N = N₀ · e^(−λt)", "pages/7_Atomfysik.py")
        _g("**Kernereaktion** — energi frigivet fra massedefekt  (E = Δm·c²)",
           "g_mc2", "atom_formel", "Energi-masse:  E = Δm · c²", "pages/7_Atomfysik.py")
        _g("**Fotoelektrisk effekt** — foton frigiver elektron fra metal",
           "g_foto", "atom_formel", "Fotoelektrisk effekt", "pages/7_Atomfysik.py")
        _g("**Ideel gaslov** — p, V, T, mol  (isoterm · isobar · isochor)",
           "g_gas", "termo_formel", "Ideel gaslov:  p · V = n · R · T", "pages/6_Termodynamik.py")
        _g("**Varmekapacitet** — Q = mcΔT, kalorimetermåling, blanding",
           "g_varme", "termo_formel", "Varmekapacitet:  Q = m · c · ΔT", "pages/6_Termodynamik.py")
        _g("**Faseovergang** — smeltning, fordampning, latent varme L",
           "g_fase", "termo_formel", "Faseovergang:  Q = m · L", "pages/6_Termodynamik.py")

    with tab_rot:
        _g("**Drejer sig** — kraftmoment τ = I·α, vinkelacceleration α",
           "g_tau", "rot_formel", "Newtons 2. lov for rotation:  τ = I·α", "pages/9_Rotation.py")
        _g("**Ruller ned** af skråplan — acceleration eller K_total",
           "g_rul", "rot_formel", "Rulning uden glidning", "pages/9_Rotation.py")
        _g("**Ruller ned fra højde h** — hvad er v i bunden?  (energibevarelse)",
           "g_rulh", "rot_formel", "Rulning uden glidning", "pages/9_Rotation.py")
        _g("**Hvad ruller?** Identificér form (kugle/cylinder/ring) fra målt v og h",
           "g_rulid", "rot_formel", "Rulning uden glidning", "pages/9_Rotation.py")
        _g("**Figurdrejer / skøjteløber** — bevarelse af impulsmoment L",
           "g_L", "rot_formel", "Bevarelse af impulsmoment", "pages/9_Rotation.py")
        _g("**Partikel/kugle rammer legeme** og klistrer fast — ω efter stød  (L = mvr)",
           "g_part", "rot_formel", "Bevarelse af impulsmoment", "pages/9_Rotation.py")
        _g("**Inertimoment** I for kugle, cylinder, ring, skive  (tabel)",
           "g_I", "rot_formel", "Inertimoment – standardlegemer", "pages/9_Rotation.py")
        _g("**Støder og hænger fast** — fuldstændig uelastisk kollision",
           "g_uel", "kol_formel", "Fuldstændig uelastisk kollision (objekter hænger sammen)", "pages/10_Kollisioner.py")
        _g("**Støder elastisk** — bevæger sig fra hinanden, KE bevaret",
           "g_el", "kol_formel", "Elastisk kollision – 1D (KE bevaret)", "pages/10_Kollisioner.py")
        _g("**Kugle skyder ind i hængende klods** — lodret uelastisk stød",
           "g_kul", "kol_formel", "Kuglestød – bullet i klods (lodret):  v' = mv/(M+m)", "pages/10_Kollisioner.py")
        _g("**Impuls og kontakttid** — gennemsnitskraft under stød mod væg / bold",
           "g_imp", "kol_formel", "Impuls og gennemsnitskraft:  J = F·Δt = m·Δv", "pages/10_Kollisioner.py")
        _g("**Svinger frem og tilbage** — periode T, frekvens f  (fjeder eller pendul)",
           "g_sving", "sving_formel", "Fjedermasse:  T = 2π√(m/k)", "pages/11_Svingninger.py")

    st.divider()
    with st.expander("📚 Vis alle beregnere"):
        PLACEHOLDER = "– vælg –"
        options = [PLACEHOLDER] + [f"{s[0]} {s[1]}" for s in SIDER]
        valg = st.radio("Vælg beregner:", options, label_visibility="collapsed", key="søg_radio")
        if valg != PLACEHOLDER:
            idx = options.index(valg) - 1
            _, _, fil, _ = SIDER[idx]
            st.switch_page(fil)
