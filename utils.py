import streamlit as st

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

# ── Komplet formel-indeks (bruges af søgesiden) ───────────────────────────────

FORMLER = [
    # ── Kinematik ──
    {"navn": "Uniform bevægelse:  s = v · t",                   "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "uniform bevægelse konstant hastighed s v t"},
    {"navn": "Jævnt accelereret (1):  v = v₀ + a · t",         "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kinematik acceleration hastighed tid v v0 a t"},
    {"navn": "Jævnt accelereret (2):  s = v₀·t + ½·a·t²",     "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "strækning position s v0 a t kinematik frit fald"},
    {"navn": "Jævnt accelereret (3):  v² = v₀² + 2·a·s",      "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "hastighed strækning v2 a s kinematik"},
    {"navn": "Kastebevægelse (vandret kast)",                    "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kast vandret projektil horisontal vertikal højde"},
    {"navn": "Kastebevægelse (skråt kast)",                     "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "kast skråt vinkel projektil horisontal vertikal"},
    {"navn": "Cirkulær bevægelse",                              "side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "cirkulær bevægelse centripetal radius hastighed periode"},
    {"navn": "Cirkulær bevægelse – RPM-omregner og centripetal","side": "Kinematik",    "fil": "pages/1_Kinematik.py",        "key": "kin_formel",   "kw": "RPM cirkel centripetal omdrejning hastighed radius ac omregn"},
    # ── Dynamik ──
    {"navn": "Newtons 2. lov:  F = m · a",                     "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "newton kraft masse acceleration F m a lov nettokraft"},
    {"navn": "Tyngdekraft:  G = m · g",                        "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "tyngde vægt masse g G newton"},
    {"navn": "Friktion:  f = μ · N",                           "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "friktion friktionskraft normalkraft mu koefficient statisk kinetisk"},
    {"navn": "Centripetalkraft:  Fc = m · v² / r",             "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "centripetal kraft cirkel radius hastighed Fc mv2 r"},
    {"navn": "Normalkraft i sløjfe (top/bund)",                 "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "normalkraft sløjfe loop top bund minimum hastighed N vmin"},
    {"navn": "Impuls:  p = m · v",                             "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "impuls masse hastighed p m v kg m/s"},
    {"navn": "Impulsmomentloven:  F · Δt = Δp",                "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "impulsmomentlov F delta t p kraft tid"},
    {"navn": "Kraftmoment:  τ = F · l",                        "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "kraftmoment tau torque F l arm vinkel"},
    {"navn": "Hældende plan",                                   "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "hældning plan skrå friktion normalkraft vinkel theta"},
    {"navn": "Atwood-maskine:  to masser over trisse",         "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "atwood trisse masse acceleration snor T"},
    {"navn": "Spænding og tøjning:  σ = F / A",                "side": "Dynamik",      "fil": "pages/2_Dynamik.py",          "key": "dyn_formel",   "kw": "spænding tøjning youngs modul sigma epsilon E areal diameter"},
    # ── Energi ──
    {"navn": "Kinetisk energi:  Ek = ½ · m · v²",             "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "kinetisk energi Ek masse hastighed v m joule"},
    {"navn": "Potentiel energi:  Ep = m · g · h",              "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "potentiel energi Ep højde h masse g joule"},
    {"navn": "Fjederkraft og -energi",                          "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "fjeder potentiel energi Ef k x strækket Hookes lov"},
    {"navn": "Arbejde:  W = F · s · cos(θ)",                   "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "arbejde W kraft strækning vinkel theta cos"},
    {"navn": "Effekt:  P = W / t = F · v",                     "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "effekt P watt arbejde tid kraft hastighed"},
    {"navn": "Energibevarelse:  Ek₁ + Ep₁ = Ek₂ + Ep₂",      "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "energibevarelse konservation hastighed højde v h kinetisk potentiel rulning"},
    {"navn": "Energibevarelse med friktion",                    "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "energibevarelse friktion tab varme Q W_frikt"},
    {"navn": "Mekanisk virkningsgrad:  η = P_ud / P_ind",      "side": "Energi",       "fil": "pages/3_Energi.py",           "key": "energi_formel","kw": "virkningsgrad eta P_ud P_ind effektivitet"},
    # ── Elektricitet ──
    {"navn": "Ohms lov:  U = R · I",                           "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "ohm spænding modstand strøm U R I volt ampere"},
    {"navn": "Elektrisk effekt",                                "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "elektrisk effekt P watt U I R"},
    {"navn": "Seriekobling af modstande",                       "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "serie kobling modstand R total sum strøm"},
    {"navn": "Parallelkobling af modstande",                    "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "parallel kobling modstand R total spænding"},
    {"navn": "Kondensator:  Q = C · U",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "kondensator ladning kapacitans spænding Q C U farad"},
    {"navn": "Energi i kondensator:  E = ½ · C · U²",          "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "energi kondensator E C U halvt farad joule"},
    {"navn": "RC-kredsløb:  τ = R · C",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "RC tidskonstant kondensator opladning afladning tau eksponentiel"},
    {"navn": "RL-kredsløb:  τ = L / R",                        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "RL induktans tidskonstant strøm tau L R"},
    {"navn": "Coulombs lov:  F = k · q₁ · q₂ / r²",           "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "coulomb kraft ladning afstand k q r elektrisk"},
    {"navn": "Elektrisk felt:  E = F / q = k · Q / r²",        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "elektrisk felt feltstyrke E kraft ladning r"},
    {"navn": "Magnetfelt fra uendelig ledning:  B = μ₀·I / (2π·r)", "side": "Elektricitet", "fil": "pages/4_Elektricitet.py", "key": "elek_formel", "kw": "magnetfelt ledning B mu0 strøm I radius r tesla"},
    {"navn": "Lorentzkraft:  F = q · v · B",                   "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "lorentz kraft ladning hastighed magnetfelt F q v B sin theta"},
    {"navn": "Lorentzkraft på ledning:  F = B · I · L",        "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "lorentz kraft ledning B I L sin theta"},
    {"navn": "Induceret EMF:  ε = B · L · v",                  "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "induceret EMF epsilon B L v induktion"},
    {"navn": "Faradays lov:  ε = -N · ΔΦ / Δt",               "side": "Elektricitet", "fil": "pages/4_Elektricitet.py",     "key": "elek_formel",  "kw": "faraday EMF flux induktion epsilon N delta Phi vindinger"},
    # ── Bølger & Optik ──
    {"navn": "Bølgehastighed:  v = f · λ",                     "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "bølgehastighed frekvens bølgelængde v f lambda lyd lys"},
    {"navn": "Snells lov:  n₁·sin(θ₁) = n₂·sin(θ₂)",          "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "snell brydning refraktion n1 n2 theta vinkel glas"},
    {"navn": "Totalrefleksion og kritisk vinkel",               "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "totalrefleksion kritisk vinkel n1 n2 fiber optik"},
    {"navn": "Linsformel:  1/f = 1/do + 1/di",                 "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "lins linse brændvidde billede genstand do di f optik"},
    {"navn": "Forstørring:  M = -di / do",                     "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "forstørring M di do billede genstand"},
    {"navn": "Doppler-effekt",                                  "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "doppler frekvens kilde observatør hastighed lyd"},
    {"navn": "Dobbeltspalte (Young):  d·sin(θ) = n·λ",         "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "young dobbeltspalte interferens maksima d n lambda theta"},
    {"navn": "Diffraktionsgitter:  d·sin(θ) = m·λ",            "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "diffraktionsgitter gitter linjer lambda m theta skarpe"},
    {"navn": "Enkelt­spalte diffraktion",                       "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "enkelt spalte diffraktion minima a lambda theta"},
    {"navn": "Tyndfilm interferens",                            "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "tyndfilm sæbefilm olie interferens fasevending n t konstruktiv"},
    {"navn": "Malus' lov:  I = I₀·cos²(θ)",                   "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "malus polarisering polarisator intensitet I0 cos theta lys"},
    {"navn": "Stående bølger – streng/rør",                    "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "stående bølger streng rør harmonisk frekvens L v n"},
    {"navn": "Lysets brydningsindeks:  n = c / v",             "side": "Bølger & Optik","fil": "pages/5_Boelger_og_Optik.py","key": "bolge_formel", "kw": "brydningsindeks n c v lys medium glas"},
    # ── Termodynamik ──
    {"navn": "Ideel gaslov:  p · V = n · R · T",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "ideel gas tryk volumen stofmængde temperatur p V n R T"},
    {"navn": "Kombineret gaslov:  p₁V₁/T₁ = p₂V₂/T₂",        "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "kombineret gaslov to tilstande p1 V1 T1 p2 V2 T2"},
    {"navn": "Varmekapacitet:  Q = m · c · ΔT",                "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "varmekapacitet Q m c delta T vand aluminium joule"},
    {"navn": "Faseovergang:  Q = m · L",                       "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "faseovergang fordampning smeltning latent varme Q m L"},
    {"navn": "Arbejde af gas – isobar:  W = p · ΔV",           "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "isobar arbejde gas W p delta V konstant tryk"},
    {"navn": "Arbejde af gas – isoterm:  W = nRT·ln(V₂/V₁)",  "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "isoterm arbejde gas W nRT ln V2 V1 konstant temperatur"},
    {"navn": "Adiabatisk proces:  pV^γ = konst",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "adiabatisk Q=0 gamma pV T2 p2 V2 arbejde"},
    {"navn": "1. termodynamikslov:  ΔU = Q − W",               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "termodynamikslov delta U Q W intern energi"},
    {"navn": "Carnot-virkningsgrad:  η = 1 − Tk/Tv",           "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "carnot virkningsgrad eta temperatur kold varm T maksimal"},
    {"navn": "Termisk udvidelse",                               "side": "Termodynamik", "fil": "pages/6_Termodynamik.py",     "key": "termo_formel", "kw": "termisk udvidelse alpha beta delta L V temperatur"},
    # ── Atomfysik ──
    {"navn": "Radioaktivt henfald:  N = N₀ · e^(−λt)",        "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "radioaktiv henfald N N0 lambda t eksponentiel"},
    {"navn": "Aktivitet:  A = λ · N",                          "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "aktivitet A lambda N becquerel Bq"},
    {"navn": "Halvvejstid:  T½ = ln(2) / λ",                   "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "halvvejstid T halv lambda ln 2"},
    {"navn": "Energi-masse:  E = Δm · c²",                     "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "E mc2 masse energi Einstein delta m c MeV"},
    {"navn": "Fotonenergí:  E = h · f = h·c / λ",              "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "foton energi h f lambda c Planck lys eV"},
    {"navn": "de Broglie bølgelængde:  λ = h / (m·v)",         "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "de broglie bølgelængde lambda h m v partikelbølge"},
    {"navn": "Bohrs model – hydrogenspektret",                  "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "bohr hydrogen spektrum energi niveau n Z eV 13.6"},
    {"navn": "Fotoelektrisk effekt",                            "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "fotoelektrisk effekt foton elektron arbejdsfunktion phi h f eV"},
    {"navn": "Compton-spredning",                               "side": "Atomfysik",    "fil": "pages/7_Atomfysik.py",        "key": "atom_formel",  "kw": "compton spredning bølgelængde delta lambda vinkel theta elektron"},
    # ── Usikkerhed ──
    {"navn": "Gennemsnit og standardafvigelse",                 "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "gennemsnit standardafvigelse middel mean std SEM type A"},
    {"navn": "Standardmåleusikkerhed (type A)",                 "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "standardmåleusikkerhed type A SEM n målinger"},
    {"navn": "Forenelighedstest – er ny måling OK?",            "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "forenelighed test z-score ny måling acceptabel k sigma"},
    {"navn": "Relativ og absolut usikkerhed",                   "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "relativ absolut usikkerhed procent delta"},
    {"navn": "Fejlpropagation – addition/subtraktion",          "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation addition subtraktion z x y delta RSS"},
    {"navn": "Fejlpropagation – multiplikation/division",       "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation multiplikation division relativ usikkerhed RSS"},
    {"navn": "Fejlpropagation – potens:  z = xⁿ",              "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation potens z xn n eksponent"},
    {"navn": "Fejlpropagation – generel (numerisk)",            "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "fejlpropagation numerisk generel partiel afledt RSS"},
    {"navn": "Samlet usikkerhed (type A + B)",                  "side": "Usikkerhed",   "fil": "pages/8_Usikkerhed.py",       "key": "usk_formel",   "kw": "samlet usikkerhed type A B kombination kvadrat"},
    {"navn": "Potenslov-fitting:  y = A · xᵅ  (log-log regression)", "side": "Usikkerhed", "fil": "pages/8_Usikkerhed.py",   "key": "usk_formel",   "kw": "potenslov fitting regression log alpha A R2 sigma"},
    # ── Rotation ──
    {"navn": "Vinkelkinematik (analog til lineær kinematik)",   "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "vinkelkinematik alpha omega theta t acceleration rotation"},
    {"navn": "Sammenhæng lineær ↔ vinkelbevægelse",            "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "lineær vinkel hastighed acceleration v omega r s theta"},
    {"navn": "Inertimoment – standardlegemer",                  "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "inertimoment I tabel kugle cylinder ring skive standard"},
    {"navn": "Steiners sætning:  I = Icm + M·d²",              "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "steiner parallel axis Icm M d parallelflytte akse"},
    {"navn": "Rotationskinetisk energi:  K = ½·I·ω²",          "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rotationsenergi K I omega halvt joule"},
    {"navn": "Newtons 2. lov for rotation:  τ = I·α",          "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rotation newton kraftmoment inertimoment tau I alpha"},
    {"navn": "Arbejde og effekt ved rotation",                  "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "arbejde effekt rotation W P tau theta omega"},
    {"navn": "Rulning uden glidning",                           "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "rulning slip v omega r hastighed glidning"},
    {"navn": "Impulsmoment:  L = I·ω",                         "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "impulsmoment L I omega"},
    {"navn": "Bevarelse af impulsmoment",                       "side": "Rotation",     "fil": "pages/9_Rotation.py",         "key": "rot_formel",   "kw": "impulsmoment bevarelse L I1 omega1 I2 omega2 figur skøjte"},
    {"navn": "Trisse + ophængt masse (Yo-Yo / Atwood med rotation)", "side": "Rotation", "fil": "pages/9_Rotation.py",       "key": "rot_formel",   "kw": "trisse masse yo-yo atwood rotation snor"},
    # ── Kollisioner ──
    {"navn": "Bevarelse af impuls (generelt):  Σp_før = Σp_efter", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py",  "key": "kol_formel",   "kw": "impulsbevarelse kollision masse hastighed m v p"},
    {"navn": "Fuldstændig uelastisk kollision (objekter hænger sammen)", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py", "key": "kol_formel", "kw": "uelastisk kollision fuldstændig hænger samme V m1 m2"},
    {"navn": "Elastisk kollision – 1D (KE bevaret)",            "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "elastisk kollision 1D KE bevaret v1 v2 masse"},
    {"navn": "Kollision i 2D – vektorkomponenter",              "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "kollision 2D vektor vinkel x y komponent"},
    {"navn": "Koefficient for restitution:  e = Δv_efter / Δv_før", "side": "Kollisioner", "fil": "pages/10_Kollisioner.py", "key": "kol_formel",   "kw": "restitution koefficient e elastisk uelastisk e=1 e=0"},
    {"navn": "Eksplosion / udskydning",                         "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "eksplosion udskydning masse impuls v1 v2"},
    {"navn": "Massemidtpunkt og -hastighed",                    "side": "Kollisioner",  "fil": "pages/10_Kollisioner.py",     "key": "kol_formel",   "kw": "massemidtpunkt CM hastighed r xcm vcm"},
    # ── Svingninger ──
    {"navn": "Fjedermasse:  T = 2π√(m/k)",                     "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "fjeder masse periode T k m svingning SHM"},
    {"navn": "Simpelt pendul:  T = 2π√(L/g)",                  "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "pendul periode T L g svingning"},
    {"navn": "Vinkelfrekvens:  ω = √(k/m)",                    "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "vinkelfrekvens omega k m T f rad/s SHM"},
    {"navn": "Bevægelsesligning:  x(t) = A·cos(ωt + φ)",       "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "bevægelsesligning x t A cos omega phi position hastighed"},
    {"navn": "Energi i svingning:  E = ½·k·A²",                "side": "Svingninger",  "fil": "pages/11_Svingninger.py",     "key": "sving_formel", "kw": "energi fjeder amplitude E k A SHM svingning"},
    {"navn": "Dæmpet svingning:  x(t) = A·e^(−γt)·cos(ω't + φ)", "side": "Svingninger", "fil": "pages/11_Svingninger.py",  "key": "sving_formel", "kw": "dæmpet svingning gamma omega prime underdæmpet overdæmpet"},
]
