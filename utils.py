import streamlit as st
import re as _re

# ── np.array-parser (bruges i Usikkerhed og andre arrayfelt-inputs) ──────────

def parse_numpy_array(text: str):
    """Parse both plain CSV and np.array([...]) syntax into a list of floats.

    Accepts:
      "1.2, 1.5, 2.2"
      "np.array([1.2, 1.5, 2.2])"
      "np.array([1.2,1.5,2.2])"
    """
    import numpy as np
    text = text.strip()
    m = _re.search(r'np\.array\s*\(\s*\[(.*?)\]\s*\)', text, _re.DOTALL)
    if m:
        text = m.group(1)
    return np.array([float(v.strip()) for v in text.split(",") if v.strip()])

# ── Konstantpanel (sidebar) ─────────────────────────────────────────────────

def show_sidebar_constants():
    with st.sidebar:
        with st.expander("📐 Konstanter", expanded=False):
            st.markdown("""
| Symbol | Navn | Værdi |
|--------|------|-------|
| **g** | Tyngdeaccl. | 9.82 m/s² |
| **c** | Lysets hast. | 2.998×10⁸ m/s |
| **h** | Planck | 6.626×10⁻³⁴ J·s |
| **k_B** | Boltzmann | 1.381×10⁻²³ J/K |
| **R** | Gaskonstant | 8.314 J/(mol·K) |
| **N_A** | Avogadro | 6.022×10²³ mol⁻¹ |
| **e** | Elementarladning | 1.602×10⁻¹⁹ C |
| **k_e** | Coulomb k | 8.988×10⁹ N·m²/C² |
| **μ₀** | Permeabilitet | 4π×10⁻⁷ T·m/A |
| **ε₀** | Permittivitet | 8.854×10⁻¹² F/m |
| **m_e** | Elektronmasse | 9.109×10⁻³¹ kg |
| **m_p** | Protonmasse | 1.673×10⁻²⁷ kg |
| **u** | Atommasse enhed | 1.661×10⁻²⁷ kg |
""")

# ── Resultat-buffer (kæd beregninger) ────────────────────────────────────────

def gem_resultat(val, unit, symbol):
    """Gem et beregnet resultat i session_state til brug i næste formel."""
    st.session_state["_resultat"] = {"val": float(val), "unit": unit, "symbol": symbol}

def show_resultat_sidebar():
    """Vis gemt resultat i sidebar + slet-knap."""
    r = st.session_state.get("_resultat")
    if r:
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"📋 **Gemt:** {r['symbol']} = **{r['val']:.6g}** {r['unit']}")
            if st.button("🗑 Slet gemt resultat", key="_slet_resultat"):
                del st.session_state["_resultat"]
                st.rerun()

def get_gemt_resultat():
    """Returner gemt resultat dict eller None."""
    return st.session_state.get("_resultat")

def indsæt_knap(input_key, label=None):
    """
    Vis 'Indsæt gemt resultat'-knap. Returner (value, was_inserted).
    Bruges ved siden af number_input() – kald EFTER number_input med samme key.
    """
    r = st.session_state.get("_resultat")
    if r is None:
        return False
    btn_label = label or f"📋 Indsæt {r['symbol']}={r['val']:.4g} {r['unit']}"
    if st.button(btn_label, key=f"_indsæt_{input_key}"):
        st.session_state[input_key] = r["val"]
        st.rerun()
    return False

# ── Formel-tips ───────────────────────────────────────────────────────────────

def show_tips(formel: str, tips_dict: dict):
    """Vis hurtig-vejledning for den valgte formel."""
    tip = tips_dict.get(formel)
    if tip:
        st.info(f"💡 {tip}")

# ── Formelkort-grid (erstatter selectbox på emne-sider) ──────────────────────

def formula_card_grid(formulas, key, columns=2):
    """
    formulas: list of (short_name, eq_hint, full_key) tuples
    key: session_state key that stores the selected full_key
    Returns the currently selected full_key string.
    """
    full_keys = [f[2] for f in formulas]
    if key not in st.session_state or st.session_state[key] not in full_keys:
        st.session_state[key] = full_keys[0]

    grid_cols = st.columns(columns)
    for i, (short_name, eq_hint, full_key) in enumerate(formulas):
        grid_col = grid_cols[i % columns]
        is_active = st.session_state[key] == full_key
        with grid_col.container(border=True):
            marker = "✓ " if is_active else ""
            st.markdown(f"**{marker}{short_name}**")
            if eq_hint:
                st.caption(eq_hint)
            btn_label = "Valgt" if is_active else "Vælg"
            if st.button(btn_label, key=f"{key}_card_{i}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state[key] = full_key

    return st.session_state[key]

# ── Breadcrumb-navigation ─────────────────────────────────────────────────────

def breadcrumb(page_emoji, page_name):
    """Vis '← ⚡ Fysik-Calc' knap øverst på emnesider."""
    if st.button("← ⚡ Fysik-Calc", key="_bc_home"):
        st.switch_page("app.py")

# ── Komplet formel-indeks (bruges af søgesiden) ───────────────────────────────

FORMLER = [
    # ── Kinematik ──
    {"navn": "Uniform bevægelse:  s = v · t",                   "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "uniform bevægelse konstant hastighed s v t",                                                      "vars": ["s", "v", "t"]},
    {"navn": "Jævnt accelereret (1):  v = v₀ + a · t",         "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kinematik acceleration hastighed tid v v0 a t bremse bremsning opbremsning accelererer decelererer hvornår stopper ankommer curling isen glidning",   "vars": ["v", "v₀", "a", "t"]},
    {"navn": "Jævnt accelereret (2):  s = v₀·t + ½·a·t²",     "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "strækning position s v0 a t kinematik frit fald bremse bremseafstand hvor langt faldtid stopper",  "vars": ["s", "v₀", "a", "t"]},
    {"navn": "Jævnt accelereret (3):  v² = v₀² + 2·a·s",      "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "hastighed strækning v2 a s kinematik bremse bremselængde ingen tid givet",                         "vars": ["v", "v₀", "a", "s"]},
    {"navn": "Vertikalt kast",                                     "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "vertikalt kast lodret opad stenhøjde landingstid usikkerhed fejlpropagation h0 v0 t g",            "vars": ["h", "v₀", "t", "g"]},
    {"navn": "Stykvis bevægelse (v-t-graf)",                       "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "stykvis bevægelse v-t graf trapez rektangel areal position faser konstant acceleration",             "vars": ["s", "v", "t", "x"]},
    {"navn": "Kastebevægelse (vandret kast)",                    "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kast vandret projektil horisontal vertikal højde bold kugle sten ramp kastes vandret fra bygning tårn klippe bord landingsafstand faldtid", "vars": ["x", "h", "v₀", "t", "g"]},
    {"navn": "Kastebevægelse (skråt kast)",                     "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kast skråt vinkel projektil horisontal vertikal bold kugle sten football skyder i vinkel rækkevidde max højde landingstid", "vars": ["x", "h", "v₀", "θ", "t", "g"]},
    {"navn": "Skråt kast – kombinationsmatrix",                 "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "skråt kast kombinationer matrix v0 vinkel rækkevidde højde sammenlign identificer graf",             "vars": ["x", "v₀", "θ", "h", "t"]},
    {"navn": "Cirkulær bevægelse",                              "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "cirkulær bevægelse centripetal radius hastighed periode",                                         "vars": ["v", "ω", "r", "T", "f"]},
    {"navn": "Cirkulær bevægelse – RPM-omregner og centripetal","side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "RPM cirkel centripetal omdrejning hastighed radius ac omregn",                                    "vars": ["ω", "r", "RPM"]},
    {"navn": "To kugler mødes – lodret kast",                  "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "to kugler mødes lodret kast opad falder slippes højde tid mødehøjde",                           "vars": ["h", "v₀", "H", "t", "g"]},
    # ── Dynamik ──
    {"navn": "Newtons 2. lov:  F = m · a",                     "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "newton kraft masse acceleration F m a lov nettokraft",                                            "vars": ["F", "m", "a"]},
    {"navn": "Tyngdekraft:  G = m · g",                        "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "tyngde vægt masse g G newton",                                                                    "vars": ["F", "m", "g"]},
    {"navn": "Friktion fra v-t-graf:  μ = |Δv/Δt| / g",          "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "friktion v-t graf deceleration mu kinetisk koefficient aflæs bremsning glider isen curling curlingsten glidningskoefficient hockeyspiller puck",  "vars": ["μ", "v", "t", "a", "g"]},
    {"navn": "Friktion:  f = μ · N",                           "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "friktion friktionskraft normalkraft mu koefficient statisk kinetisk",                             "vars": ["F", "μ", "N", "m"]},
    {"navn": "Centripetalkraft:  Fc = m · v² / r",             "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "centripetal kraft cirkel radius hastighed Fc mv2 r",                                             "vars": ["F", "m", "v", "r"]},
    {"navn": "Normalkraft i sløjfe (top/bund)",                 "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "normalkraft sløjfe loop top bund minimum hastighed N vmin",                                       "vars": ["N", "F", "m", "v", "r", "g"]},
    {"navn": "Gravitationsloven:  F = G·m₁·m₂ / r²",            "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "gravitation Newton G masse afstand planet orbital F r",                                          "vars": ["F", "m", "r", "g"]},
    {"navn": "Impuls:  p = m · v",                             "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "impuls masse hastighed p m v kg m/s",                                                             "vars": ["p", "m", "v"]},
    {"navn": "Impulsmomentloven:  F · Δt = Δp",                "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "impulsmomentlov F delta t p kraft tid",                                                           "vars": ["F", "t", "p", "m", "v"]},
    {"navn": "Kraftmoment:  τ = F · l",                        "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "kraftmoment tau torque F l arm vinkel",                                                           "vars": ["τ", "F", "l"]},
    {"navn": "Hældende plan",                                   "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "hældning plan skrå skråplan friktion normalkraft vinkel theta kile rampe",                     "vars": ["F", "m", "g", "θ", "μ", "N", "a"]},
    {"navn": "Atwood-maskine:  to masser over trisse",         "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "atwood trisse masse acceleration snor T",                                                         "vars": ["m", "a", "g", "F"]},
    {"navn": "Spænding og tøjning:  σ = F / A",                "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "spænding tøjning youngs modul sigma epsilon E areal diameter",                                    "vars": ["σ", "F", "A", "d"]},
    {"navn": "Konisk pendul",                                  "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "konisk pendul cirkulær vandret drejer snor vinkel theta omega vinkelhastighed periode masse",       "vars": ["θ", "ω", "v", "r", "L", "T"]},
    {"navn": "Bernoulli-ligning",                              "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "bernoulli tryk hastighed tyngdekraft ideel strøm Torricelli udstrømning hul beholder densitet",   "vars": ["p", "v", "h", "ρ"]},
    {"navn": "Snorpendel – snorkraft ved vilkårlig vinkel",    "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "snorpendel snorkraft vinkel centripetal energibevarelse lodret vandret T m v0 R theta",           "vars": ["T", "m", "v₀", "R", "θ"]},
    {"navn": "Kraft i vinkel på ru flade",                     "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "kraft vinkel ru flade friktion acceleration normalkraft angled force theta mu optimal vinkel",      "vars": ["F", "m", "θ", "μ", "a", "N"]},
    {"navn": "Arkimedes' princip:  F_b = ρ · V · g",           "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "arkimedes opdrift opdriftskraft flyder synker fluid nedsænket volumen densitet opdriftslov",          "vars": ["F_b", "ρ", "V", "g"]},
    {"navn": "Terminal hastighed:  v_T = √(2mg / CρA)",         "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "terminal hastighed luftmodstand drag vT faldskærm kugle CρA frit fald",                              "vars": ["v_T", "m", "C", "ρ", "A"]},
    {"navn": "Satellit og Keplers 3. lov",                      "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "satellit kepler orbital periode radius T r GM undvigelseshastighed ISS planet omløbstid",             "vars": ["v", "T", "r", "M"]},
    {"navn": "Statisk ligevægt:  ΣF = 0 og Στ = 0",            "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "statisk ligevægt bjælke hængsel snor kraftmoment reaktionskraft understøtning tau omdrejningspunkt",  "vars": ["F", "τ", "d"]},
    {"navn": "To-snors ophæng:  T₁ og T₂",                      "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "to snore ophæng snorkraft T1 T2 theta vinkel loft lampe masse hænger to strenge ligevægt",              "vars": ["T", "F", "m", "θ", "g"]},
    {"navn": "To-klods system:  CM-acceleration",                 "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "to klodser system massemidtpunkt CM acceleration friktion glider glidning intern ekstern kraft a_CM",    "vars": ["F", "m", "a", "μ"]},
    # ── Energi ──
    {"navn": "Kinetisk energi:  Ek = ½ · m · v²",             "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "kinetisk energi Ek masse hastighed v m joule",                                                    "vars": ["Ek", "m", "v"]},
    {"navn": "Potentiel energi:  Ep = m · g · h",              "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "potentiel energi Ep højde h masse g joule",                                                       "vars": ["Ep", "m", "g", "h"]},
    {"navn": "Fjederkraft og -energi",                          "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "fjeder spring potentiel energi Ef k x strækket Hookes lov kompression",                        "vars": ["F", "k", "x"]},
    {"navn": "Arbejde:  W = F · s · cos(θ)",                   "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "arbejde W kraft strækning vinkel theta cos",                                                      "vars": ["W", "F", "s", "θ"]},
    {"navn": "Effekt:  P = W / t = F · v",                     "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "effekt P watt arbejde tid kraft hastighed",                                                       "vars": ["P", "W", "t", "F", "v"]},
    {"navn": "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂",      "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "energibevarelse konservation hastighed højde v h kinetisk potentiel rulning hastighed bunden toppen glider rutsjeban rutschebane rutsjebane frigives slipper", "vars": ["Ek", "Ep", "v", "h", "m"]},
    {"navn": "Energibevarelse med friktion",                    "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "energibevarelse friktion tab varme Q W_frikt gnidning energitab",                                 "vars": ["Ek", "Ep", "v", "h", "m", "μ", "F"]},
    {"navn": "Mekanisk virkningsgrad:  η = P_ud / P_ind",      "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "virkningsgrad eta P_ud P_ind effektivitet",                                                       "vars": ["η", "P"]},
    {"navn": "Pendul – hastighed og snorkraft (energibevarelse)", "side": "Energi",     "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "pendul hastighed snorkraft energibevarelse v bunden theta frigivelse vinkel T centripetal",         "vars": ["v", "T", "m", "R", "θ", "g"]},
    {"navn": "Fjeder – maks. kompression ved fald",             "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "fjeder kompression fald andengradsligning k h d mg energibevarelse fjederkonstant",               "vars": ["d", "k", "m", "h", "g"]},
    # ── Elektricitet ──
    {"navn": "Ohms lov:  U = R · I",                           "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "ohm spænding modstand strøm U R I volt ampere",                                                   "vars": ["U", "R", "I"]},
    {"navn": "Elektrisk effekt",                                "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "elektrisk effekt P watt U I R",                                                                   "vars": ["P", "U", "I", "R"]},
    {"navn": "Seriekobling af modstande",                       "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "serie kobling modstand R total sum strøm",                                                        "vars": ["R"]},
    {"navn": "Parallelkobling af modstande",                    "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "parallel kobling modstand R total spænding",                                                      "vars": ["R"]},
    {"navn": "Kondensator:  Q = C · U",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "kondensator ladning kapacitans spænding Q C U farad",                                             "vars": ["Q", "C", "U"]},
    {"navn": "Energi i kondensator:  E = ½ · C · U²",          "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "energi kondensator E C U halvt farad joule",                                                      "vars": ["E", "C", "U"]},
    {"navn": "RC-kredsløb:  τ = R · C",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "RC tidskonstant kondensator opladning afladning tau eksponentiel",                                "vars": ["τ", "R", "C", "t"]},
    {"navn": "RL-kredsløb:  τ = L / R",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "RL induktans tidskonstant strøm tau L R",                                                         "vars": ["τ", "L", "R", "t"]},
    {"navn": "Coulombs lov:  F = k · q₁ · q₂ / r²",           "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "coulomb kraft ladning afstand k q r elektrisk",                                                   "vars": ["F", "q", "r"]},
    {"navn": "Elektrisk felt:  E = F / q = k · Q / r²",        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "elektrisk felt feltstyrke E kraft ladning r",                                                     "vars": ["E", "F", "q", "r"]},
    {"navn": "Magnetfelt fra uendelig ledning:  B = μ₀·I / (2π·r)", "side": "Elektricitet", "fil": "pages/4_Elektricitet.py", "key": "elek_formel", "kw": "magnetfelt ledning B mu0 strøm I radius r tesla",                                                "vars": ["B", "I", "r"]},
    {"navn": "Lorentzkraft:  F = q · v · B",                   "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "lorentz kraft ladning hastighed magnetfelt F q v B sin theta",                                    "vars": ["F", "q", "v", "B"]},
    {"navn": "Lorentzkraft på ledning:  F = B · I · L",        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "lorentz kraft ledning B I L sin theta",                                                           "vars": ["F", "B", "I", "L"]},
    {"navn": "Induceret EMF:  ε = B · L · v",                  "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "induceret EMF epsilon B L v induktion",                                                           "vars": ["ε", "B", "L", "v"]},
    {"navn": "Faradays lov:  ε = -N · ΔΦ / Δt",               "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "faraday EMF flux induktion epsilon N delta Phi vindinger",                                         "vars": ["ε", "N", "t"]},
    # ── Bølger & Optik ──
    {"navn": "Bølgehastighed:  v = f · λ",                     "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "bølgehastighed frekvens bølgelængde v f lambda lyd lys",                                          "vars": ["v", "f", "λ"]},
    {"navn": "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)",          "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "snell brydning refraktion n1 n2 theta vinkel glas",                                               "vars": ["n", "θ"]},
    {"navn": "Totalrefleksion og kritisk vinkel",               "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "totalrefleksion kritisk vinkel n1 n2 fiber optik",                                                "vars": ["n", "θ"]},
    {"navn": "Linsformel:  1/f = 1/do + 1/di",                 "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "lins linse brændvidde billede genstand do di f optik",                                            "vars": ["f", "d"]},
    {"navn": "Forstørring:  M = -di / do",                     "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "forstørring M di do billede genstand",                                                            "vars": ["M", "d"]},
    {"navn": "Doppler-effekt",                                  "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "doppler frekvens kilde observatør hastighed lyd",                                                 "vars": ["f", "v"]},
    {"navn": "Dobbeltspalte (Young):  d·sin(θ) = n·λ",         "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "young dobbeltspalte interferens maksima d n lambda theta",                                         "vars": ["d", "θ", "n", "λ"]},
    {"navn": "Diffraktionsgitter:  d·sin(θ) = m·λ",            "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "diffraktionsgitter gitter linjer lambda m theta skarpe",                                           "vars": ["d", "θ", "λ"]},
    {"navn": "Enkelt­spalte diffraktion",                       "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "enkelt spalte diffraktion minima a lambda theta",                                                  "vars": ["a", "θ", "λ"]},
    {"navn": "Tyndfilm interferens",                            "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "tyndfilm sæbefilm olie interferens fasevending n t konstruktiv",                                    "vars": ["n", "t", "λ"]},
    {"navn": "Malus' lov:  I = I₀·cos²(θ)",                   "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "malus polarisering polarisator intensitet I0 cos theta lys",                                       "vars": ["I", "θ"]},
    {"navn": "Stående bølger – streng/rør",                    "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "stående bølger streng rør harmonisk frekvens L v n",                                              "vars": ["λ", "L", "f", "v"]},
    {"navn": "Lysets brydningsindeks:  n = c / v",             "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "brydningsindeks n c v lys medium glas",                                                           "vars": ["n", "c", "v"]},
    {"navn": "Lydintensitet og dB:  β = 10·log₁₀(I/I₀)",      "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "lydintensitet decibel dB beta log I I0 lydniveau afstand støj høretab smertegrænse",                  "vars": ["β", "I", "r"]},
    {"navn": "Slagfrekvens (beats):  f_beat = |f₁ − f₂|",      "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "slagfrekvens beats slag interferens f1 f2 stemning instrument pulsering",                            "vars": ["f_beat", "f₁", "f₂"]},
    # ── Termodynamik ──
    {"navn": "Ideel gaslov:  p · V = n · R · T",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "ideel gas tryk volumen stofmængde temperatur p V n R T",                                           "vars": ["p", "V", "n", "T"]},
    {"navn": "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂",        "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "kombineret gaslov to tilstande p1 V1 T1 p2 V2 T2",                                                "vars": ["p", "V", "T"]},
    {"navn": "Varmekapacitet:  Q = m · c · ΔT",                "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "varmekapacitet Q m c delta T vand aluminium joule",                                                "vars": ["Q", "m", "c", "T"]},
    {"navn": "Faseovergang:  Q = m · L",                       "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "faseovergang fordampning smeltning latent varme Q m L",                                            "vars": ["Q", "m", "L"]},
    {"navn": "Arbejde af gas – isobar:  W = p · ΔV",           "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "isobar arbejde gas W p delta V konstant tryk",                                                     "vars": ["W", "p", "V"]},
    {"navn": "Arbejde af gas – isoterm:  W = nRT·ln(V₂/V₁)",  "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "isoterm arbejde gas W nRT ln V2 V1 konstant temperatur",                                           "vars": ["W", "n", "T", "V"]},
    {"navn": "Adiabatisk proces:  pV^γ = konst",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "adiabatisk Q=0 gamma pV T2 p2 V2 arbejde",                                                        "vars": ["p", "V", "T", "γ"]},
    {"navn": "1. termodynamikslov:  ΔU = Q − W",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "termodynamikslov delta U Q W intern energi",                                                       "vars": ["Q", "W"]},
    {"navn": "Intern energi idealgas:  U = (f/2)·n·R·T",        "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "intern energi idealgas U nRT monoatomisk diatomisk Cv Cp frihedsgrader f gamma",              "vars": ["U", "n", "T", "Q", "W"]},
    {"navn": "Entropi:  ΔS = Q_rev / T",                         "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "entropi delta S Q T isoterm isobar isochor adiabatisk reversibel nCp nCv ln J/K uorden",          "vars": ["Q", "T", "n", "V", "p"]},
    {"navn": "Carnot-virkningsgrad:  η = 1 − Tk/Tv",           "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "carnot virkningsgrad eta temperatur kold varm T maksimal",                                         "vars": ["η", "T"]},
    {"navn": "Termisk udvidelse",                               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "termisk udvidelse alpha beta delta L V temperatur",                                                 "vars": ["L", "T"]},
    {"navn": "Varmledning:  Q/t = k·A·ΔT/L",                  "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "varmledning Fourier varmestrøm k A delta T L stav plade kobber stål ledningsevne",               "vars": ["Q", "k", "A", "T", "L"]},
    # ── Atomfysik ──
    {"navn": "Radioaktivt henfald:  N = N₀ · e^(−λt)",        "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik radioaktiv henfald N N0 lambda t eksponentiel kerne nuklid hvornår rest tilbage mængde",  "vars": ["N", "λ", "t"]},
    {"navn": "Aktivitet:  A = λ · N",                          "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik aktivitet A lambda N becquerel Bq radioaktiv",                                    "vars": ["A", "λ", "N"]},
    {"navn": "Halvvejstid:  T½ = ln(2) / λ",                   "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik halvvejstid halveringstid T halv lambda ln 2 henfald halverer halvt halvdelen",   "vars": ["T½", "λ"]},
    {"navn": "Energi-masse:  E = Δm · c²",                     "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik E mc2 masse energi Einstein delta m c MeV kerneenergi",                          "vars": ["E", "m", "c"]},
    {"navn": "Fotonenergí:  E = h · f = h·c / λ",              "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik foton energi h f lambda c Planck lys eV kvante",                                 "vars": ["E", "h", "f", "λ"]},
    {"navn": "de Broglie bølgelængde:  λ = h / (m·v)",         "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik de broglie bølgelængde lambda h m v partikelbølge kvante",                       "vars": ["λ", "h", "m", "v", "p"]},
    {"navn": "Bohrs model – hydrogenspektret",                  "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik bohr hydrogen spektrum energi niveau n Z eV 13.6 kerne",                         "vars": ["E", "n", "h", "f"]},
    {"navn": "Fotoelektrisk effekt",                            "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik fotoelektrisk effekt foton elektron arbejdsfunktion phi h f eV",               "vars": ["E", "h", "f"]},
    {"navn": "Compton-spredning",                               "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "atom atomfysik compton spredning bølgelængde delta lambda vinkel theta elektron",              "vars": ["λ", "θ", "m"]},
    # ── Usikkerhed ──
    {"navn": "Gennemsnit og standardafvigelse",                 "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "gennemsnit standardafvigelse middel mean std SEM type A",                                          "vars": ["x̄", "s", "n", "σ"]},
    {"navn": "Standardmåleusikkerhed (type A)",                 "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "standardmåleusikkerhed type A SEM n målinger",                                                    "vars": ["u", "s", "n"]},
    {"navn": "Forenelighedstest – er ny måling OK?",            "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "forenelighed test z-score ny måling acceptabel k sigma passer forenelig afviger stemmer overens",  "vars": ["x̄", "u", "n"]},
    {"navn": "Relativ og absolut usikkerhed",                   "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "relativ absolut usikkerhed procent delta",                                                         "vars": ["Δ", "x"]},
    {"navn": "Fejlpropagation – addition/subtraktion",          "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation addition subtraktion z x y delta RSS",                                             "vars": ["Δ", "x", "y", "z"]},
    {"navn": "Fejlpropagation – multiplikation/division",       "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation multiplikation division relativ usikkerhed RSS",                                   "vars": ["Δ", "x", "y", "z"]},
    {"navn": "Fejlpropagation – potens:  z = xⁿ",              "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation potens z xn n eksponent",                                                          "vars": ["Δ", "x", "n", "z"]},
    {"navn": "Fejlpropagation – generel (numerisk)",            "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation numerisk generel partiel afledt RSS",                                              "vars": ["Δ", "x", "y", "z"]},
    {"navn": "Samlet usikkerhed (type A + B)",                  "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "samlet usikkerhed type A B kombination kvadrat",                                                   "vars": ["u"]},
    {"navn": "Potenslov-fitting:  y = A · xᵅ  (log-log regression)", "side": "Usikkerhed", "fil": "pages/8_Usikkerhed.py",   "key": "usk_formel",   "kw": "potenslov fitting regression log alpha A R2 sigma",                                                "vars": ["α", "A", "x", "y"]},
    {"navn": "Lineær regression:  y = a · x + b",              "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "lineær regression hældning a b R2 mindste kvadrater",                                              "vars": ["a", "b", "x", "y"]},
    {"navn": "Eksponentielt fit:  y = A · eᵇˣ  (semi-log regression)", "side": "Usikkerhed", "fil": "pages/8_Usikkerhed.py", "key": "usk_formel",   "kw": "eksponentiel fit semi-log henfald henfaldskonstant lambda halvtid T½ radioaktiv decay RC eksponentiel vækst b",  "vars": ["b", "A", "x", "y", "λ", "T½"]},
    {"navn": "Numerisk differentiation:  dy/dx fra arrays",   "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "numerisk differentiation diff hastighed acceleration x t v a central differens array",                  "vars": ["dy/dx", "x", "y"]},
    {"navn": "Numerisk integration:  ∫y dx (trapezregel)",    "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "numerisk integration trapezregel areal impuls arbejde F t x v trapez array",                           "vars": ["∫y dx", "x", "y"]},
    # ── Rotation ──
    {"navn": "Vinkelkinematik (analog til lineær kinematik)",   "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "vinkelkinematik alpha omega theta t acceleration rotation",                                         "vars": ["ω", "α", "θ", "t"]},
    {"navn": "Sammenhæng lineær ↔ vinkelbevægelse",            "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "lineær vinkel hastighed acceleration v omega r s theta",                                           "vars": ["v", "ω", "r", "a", "α"]},
    {"navn": "Inertimoment – standardlegemer",                  "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "inertimoment I tabel kugle cylinder ring skive standard",                                          "vars": ["I", "m", "R", "L"]},
    {"navn": "Steiners sætning:  I = Icm + M·d²",              "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "steiner parallel axis Icm M d parallelflytte akse",                                               "vars": ["I", "m", "d"]},
    {"navn": "Rotationskinetisk energi:  K = ½·I·ω²",          "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rotationsenergi K I omega halvt joule",                                                            "vars": ["K", "I", "ω"]},
    {"navn": "Newtons 2. lov for rotation:  τ = I·α",          "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rotation newton kraftmoment inertimoment tau I alpha",                                             "vars": ["τ", "I", "α"]},
    {"navn": "Arbejde og effekt ved rotation",                  "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "arbejde effekt rotation W P tau theta omega",                                                      "vars": ["W", "τ", "θ", "P", "ω"]},
    {"navn": "Rulning uden glidning",                           "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rulning slip v omega r hastighed glidning ruller ned skråplan cylinder kugle ring bunden bowlingkugle triller hælder bakke rampe",  "vars": ["v", "ω", "R", "I", "m"]},
    {"navn": "Impulsmoment:  L = I·ω",                         "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "impulsmoment L I omega",                                                                           "vars": ["L", "I", "ω"]},
    {"navn": "Bevarelse af impulsmoment",                       "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "impulsmoment bevarelse L I1 omega1 I2 omega2 figur skøjte figurdrejer drejer hurtigere trækker arme",  "vars": ["L", "I", "ω"]},
    {"navn": "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)", "side": "Rotation", "fil": "pages/9_Rotation.py",       "key": "rot_formel",   "kw": "trisse masse yo-yo atwood rotation snor",                                                          "vars": ["m", "g", "a", "I", "R"]},
    {"navn": "Rulning – v fra faldshøjde h (energibevarelse)",    "side": "Rotation",  "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rulning energibevarelse faldshøjde h v bunden ruller ned hastighed cylinder kugle ring skive c_I mgh", "vars": ["v", "h", "g", "c_I"]},
    {"navn": "Rulning – identificér legeme (v og h)",              "side": "Rotation",  "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "identificer rulning legeme form v h faldshøjde kugle cylinder ring hul massiv bedste match afvigelse",  "vars": ["v", "h"]},
    {"navn": "Partikel rammer roterende legeme (L=mvr)",           "side": "Rotation",  "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "partikel rammer legeme impulsmoment L mvr omega bullet kugle klistrer fast rotation stød støder",       "vars": ["m", "v", "r", "I", "ω"]},
    # ── Kollisioner ──
    {"navn": "Bevarelse af impuls (generelt):  Σp_før = Σp_efter", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py",  "key": "kol_formel",   "kw": "impulsbevarelse kollision masse hastighed m v p",                                                  "vars": ["p", "m", "v"]},
    {"navn": "Fuldstændig uelastisk kollision (objekter hænger sammen)", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py", "key": "kol_formel", "kw": "uelastisk kollision fuldstændig hænger sammen klæber støder fast V m1 m2",                        "vars": ["m", "v"]},
    {"navn": "Elastisk kollision – 1D (KE bevaret)",            "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "elastisk kollision 1D KE bevaret v1 v2 masse støder fra hinanden spreder",                          "vars": ["m", "v", "Ek"]},
    {"navn": "Kollision i 2D – vektorkomponenter",              "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "kollision 2D vektor vinkel x y komponent",                                                         "vars": ["m", "v", "θ"]},
    {"navn": "Koefficient for restitution:  e = Δv_efter / Δv_før", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py", "key": "kol_formel",   "kw": "restitution koefficient e elastisk uelastisk e=1 e=0",                                             "vars": ["e", "v"]},
    {"navn": "Eksplosion / udskydning",                         "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "eksplosion udskydning masse impuls v1 v2 fusion spaltning kernereaktion energifordeling MeV helium neutron KE procent fordeling",  "vars": ["m", "v", "p", "E"]},
    {"navn": "Massemidtpunkt og -hastighed",                    "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "massemidtpunkt CM hastighed r xcm vcm",                                                            "vars": ["m", "x", "r", "v"]},
    {"navn": "Impuls og gennemsnitskraft:  J = F·Δt = m·Δv",   "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "impuls gennemsnitskraft J Favg delta p kontakttid stød slag væg",                                   "vars": ["J", "F", "Δt", "m", "v", "p"]},
    {"navn": "Kuglestød – bullet i klods (lodret):  v' = mv/(M+m)", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py", "key": "kol_formel",   "kw": "kugle bullet klods lodret uelastisk stød højde h impulsbevarelse kuglestød",                         "vars": ["m", "M", "v", "h"]},
    # ── Svingninger ──
    {"navn": "Fjedermasse:  T = 2π√(m/k)",                     "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "fjeder masse periode T k m svingning SHM",                                                         "vars": ["T", "m", "k", "f", "ω"]},
    {"navn": "Simpelt pendul:  T = 2π√(L/g)",                  "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "pendul periode T L g svingning",                                                                   "vars": ["T", "L", "g", "f"]},
    {"navn": "Vinkelfrekvens:  ω = √(k/m)",                    "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "vinkelfrekvens omega k m T f rad/s SHM",                                                           "vars": ["ω", "k", "m"]},
    {"navn": "Bevægelsesligning:  x(t) = A·cos(ωt + φ)",       "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "bevægelsesligning x t A cos omega phi position hastighed",                                          "vars": ["x", "A", "ω", "t"]},
    {"navn": "Energi i svingning:  E = ½·k·A²",                "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "energi fjeder amplitude E k A SHM svingning",                                                      "vars": ["E", "k", "A"]},
    {"navn": "Dæmpet svingning:  x(t) = A·e^(−γt)·cos(ω't + φ)", "side": "Svingninger", "fil": "pages/11_Svingninger.py",  "key": "sving_formel", "kw": "dæmpet svingning gamma omega prime underdæmpet overdæmpet",                                         "vars": ["x", "A", "γ", "ω", "t"]},
    {"navn": "Fysisk pendul:  T = 2π√(I/(mgd))",               "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "fysisk pendul inertimoment I m g d periode T steiner massemidtpunkt pivot",                        "vars": ["T", "I", "m", "d", "g"]},
    {"navn": "Fjedre serie/parallel",                           "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "fjedre serie parallel kobling k_eff effektiv fjederkonstant k1 k2 to fjedre periode T",              "vars": ["k", "T", "m"]},
    {"navn": "Tvungen svingning og resonans",                   "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "tvungen svingning resonans frekvens amplitude F0 drivfrekvens omega0 dæmpning resonansfrekvens",     "vars": ["A", "F₀", "ω", "ω₀", "γ"]},
    {"navn": "Q-faktor og resonansbredde",                      "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "Q faktor resonansbredde kvalitetsfaktor båndbredde delta omega halveffekt dæmpning gamma",           "vars": ["Q", "ω₀", "γ", "Δω"]},
    # ── Relativitetsteori ──
    {"navn": "Lorentz-faktor:  γ = 1 / √(1 − v²/c²)",          "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "Lorentz gamma beta v c relativitet faktor",                                                  "vars": ["γ", "v", "c"]},
    {"navn": "Tidsudvidelse:  Δt = γ · Δt₀",                   "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "tidsudvidelse egentid delta t gamma ur bevæger",                                              "vars": ["Δt", "γ", "t"]},
    {"navn": "Længdeforkortning:  L = L₀ / γ",                 "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "længdeforkortning L L0 gamma kontraktion",                                                    "vars": ["L", "γ"]},
    {"navn": "Relativistisk kinetisk energi:  Ek = (γ − 1) · m₀c²", "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "relativistisk kinetisk energi Ek gamma m0 c2",                                           "vars": ["Ek", "γ", "m", "c"]},
    {"navn": "Relativistisk totalenergi:  E = γ · m₀c²",       "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "totalenergi E gamma m0 c2 hvileenergi",                                                       "vars": ["E", "γ", "m", "c"]},
    {"navn": "Relativistisk impuls:  p = γ · m₀ · v",          "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "relativistisk impuls p gamma m0 v",                                                           "vars": ["p", "γ", "m", "v"]},
    {"navn": "Energi–impuls relation:  E² = (pc)² + (m₀c²)²", "side": "Relativitetsteori", "fil": "pages/12_Relativitetsteori.py", "key": "rel_formel", "kw": "energi impuls relation E p c m0 foton",                                                       "vars": ["E", "p", "m", "c"]},
    # ── Dimensionsanalyse ──
    {
        "navn": "Dimensionstjek",
        "side": "Dimensionsanalyse",
        "fil": "pages/14_Dimensionsanalyse.py",
        "kw": "dimension analyse enhed M L T grundstørrelse homogen formel tjek",
        "key": "dim_formel",
        "vars": [],
    },
    {
        "navn": "Naturlige skalaer",
        "side": "Dimensionsanalyse",
        "fil": "pages/14_Dimensionsanalyse.py",
        "kw": "naturlig skala lambda tau pi-gruppe buckingham skalering model",
        "key": "dim_formel",
        "vars": [],
    },
    # ── Skalering ──
    {
        "navn": "Skaleringsanalyse",
        "side": "Skalering",
        "fil": "pages/15_Skalering.py",
        "kw": "skalering potenslov fordobling faktor T sqrt m k Kepler",
        "key": "skalering_formel",
        "vars": ["m", "k", "L", "r", "v"],
    },
]
