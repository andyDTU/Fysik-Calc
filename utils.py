import streamlit as st

SEARCH_INDEX = [
    # Kinematik
    {"label": "Uniform bevægelse › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Uniform bevægelse:  s = v · t", "keywords": ["uniform bevægelse", "konstant hastighed", "s=vt", "strækning tid hastighed", "jævn bevægelse", "beregn tid", "beregn strækning", "s v t"]},
    {"label": "Jævnt accelereret v=v₀+at › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Jævnt accelereret (1):  v = v₀ + a · t", "keywords": ["jævnt accelereret", "v=v0+at", "starthastighed", "sluthastighed", "acceleration tid", "bremse", "accelererer"]},
    {"label": "Jævnt accelereret s=v₀t+½at² › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Jævnt accelereret (2):  s = v₀·t + ½·a·t²", "keywords": ["strækning acceleration", "s=v0t", "½at²", "lodret kast", "frit fald", "bolde mødes", "kastet op"]},
    {"label": "Kastebevægelse skråt kast › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Kastebevægelse (skråt kast)", "keywords": ["skråt kast", "projektil", "rækkevidde", "maks højde", "affyringsvinkel", "kasteparabel", "kaste op"]},
    {"label": "Kastebevægelse vandret kast › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Kastebevægelse (vandret kast)", "keywords": ["vandret kast", "horisontal kast", "faldhøjde", "rækkevidde vandret", "flyvetid vandret"]},
    {"label": "Cirkulær bevægelse › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Cirkulær bevægelse", "keywords": ["cirkulær bevægelse", "banehastighed", "vinkelhastighed", "omløbstid", "centripetal acc", "omega", "radius cirkle", "frekvens omløb"]},
    {"label": "Centrifuge RPM › Kinematik", "page": "pages/1_Kinematik.py", "nav_key": "kin_formel", "nav_value": "Cirkulær bevægelse – RPM-omregner og centripetal", "keywords": ["centrifuge", "rpm", "omdrejninger pr minut", "centripetal g-kraft", "radius centrifuge", "10000 rpm"]},
    # Dynamik
    {"label": "F = m·a › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Newtons 2. lov:  F = m · a", "keywords": ["newton", "kraft masse acceleration", "F=ma", "newtons 2 lov", "nettoktraft", "resultantkraft", "beregn kraft"]},
    {"label": "Friktion › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Friktion:  f = μ · N", "keywords": ["friktion", "friktionskraft", "normalkraft", "mu koefficient", "glidnings", "statisk friktion", "kinetisk friktion"]},
    {"label": "Hældende plan › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Hældende plan", "keywords": ["hældende plan", "skråplan", "skrå flade", "vinkel plan", "acceleration ned ad", "friktion skråplan", "hældning"]},
    {"label": "Centripetalkraft › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Centripetalkraft:  Fc = m · v² / r", "keywords": ["centripetalkraft", "cirkulær kraft", "Fc", "mv2/r", "kraft cirkulær", "centripetal kraft"]},
    {"label": "Impulsmomentloven F·Δt=Δp › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Impulsmomentloven:  F · Δt = Δp", "keywords": ["impulsmomentloven", "impulssætning", "kraft tid", "impulsændring", "F delta t", "stødet", "kraft støds"]},
    {"label": "Spænding og tøjning › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Spænding og tøjning:  σ = F / A", "keywords": ["spænding tøjning", "youngs modul", "sigma epsilon", "kulfiber", "tværsnit diameter", "normalspænding", "stress strain"]},
    {"label": "Atwood-maskine › Dynamik", "page": "pages/2_Dynamik.py", "nav_key": "dyn_formel", "nav_value": "Atwood-maskine:  to masser over trisse", "keywords": ["atwood", "to masser trisse", "ophængt masse", "trisse acceleration", "snorkraft"]},
    # Energi
    {"label": "Kinetisk energi › Energi", "page": "pages/3_Energi.py", "nav_key": None, "nav_value": None, "keywords": ["kinetisk energi", "bevægelsesenergi", "Ek", "½mv2", "hastighed energi", "beregn energi"]},
    {"label": "Potentiel energi › Energi", "page": "pages/3_Energi.py", "nav_key": None, "nav_value": None, "keywords": ["potentiel energi", "tyngdepotentiel", "Ep", "mgh", "højdeenergi", "gravitationsenergi"]},
    {"label": "Fjeder Hookes lov › Energi", "page": "pages/3_Energi.py", "nav_key": None, "nav_value": None, "keywords": ["fjeder", "fjederkonstant", "fjederkraft", "hookes lov", "forlængelse fjeder", "fjederstivhed", "elastisk"]},
    {"label": "Energibevarelse › Energi", "page": "pages/3_Energi.py", "nav_key": None, "nav_value": None, "keywords": ["energibevarelse", "mekanisk energi", "friktionsfri", "hastighed fra højde", "bevar energi", "konservativ"]},
    {"label": "Effekt › Energi", "page": "pages/3_Energi.py", "nav_key": None, "nav_value": None, "keywords": ["effekt", "watt", "P=Wt", "F·v kraft hastighed", "afsæt", "motor effekt"]},
    # Elektricitet
    {"label": "Ohms lov › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["ohms lov", "spænding modstand strøm", "U=RI", "volt ampere ohm", "elektrisk kredsløb"]},
    {"label": "Seriekobling › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["seriekobling", "serie modstande", "total modstand serie", "modstande i serie"]},
    {"label": "Parallelkobling › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["parallelkobling", "parallel modstande", "modstande parallel", "total modstand parallel"]},
    {"label": "Lorentzkraft › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["lorentzkraft", "magnetfelt kraft", "ladning magnetfelt", "qvB", "kraft ladning", "magnetisk kraft"]},
    {"label": "Coulombs lov › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["coulombs lov", "elektrisk kraft ladning", "tiltrækning frastødning", "coulomb", "ladning afstand"]},
    {"label": "Faradays lov › Elektricitet", "page": "pages/4_Elektricitet.py", "nav_key": None, "nav_value": None, "keywords": ["faradays lov", "induceret emf", "flux spole", "vindinger", "induktion", "elektromagnetisk induktion"]},
    # Bølger & Optik
    {"label": "Bølgehastighed › Bølger & Optik", "page": "pages/5_Boelger_og_Optik.py", "nav_key": None, "nav_value": None, "keywords": ["bølgehastighed", "frekvens bølgelængde", "v=fλ", "lyd bølge", "lambda", "bølge"]},
    {"label": "Snells lov brydning › Bølger & Optik", "page": "pages/5_Boelger_og_Optik.py", "nav_key": None, "nav_value": None, "keywords": ["snells lov", "brydning", "lysets brydning", "brydningsindeks", "indfaldsvinkel", "brydningsvinkel"]},
    {"label": "Linsformel › Bølger & Optik", "page": "pages/5_Boelger_og_Optik.py", "nav_key": None, "nav_value": None, "keywords": ["linsformel", "linse", "brændvidde", "billedafstand", "genstandsafstand", "konveks", "optik billede"]},
    {"label": "Doppler-effekt › Bølger & Optik", "page": "pages/5_Boelger_og_Optik.py", "nav_key": None, "nav_value": None, "keywords": ["doppler", "doppler-effekt", "frekvensforskydning", "kilde bevæger", "rødforskydning", "blåforskydning"]},
    {"label": "Dobbeltspalte Young › Bølger & Optik", "page": "pages/5_Boelger_og_Optik.py", "nav_key": None, "nav_value": None, "keywords": ["dobbeltspalte", "young", "interferens", "diffraktion spalte", "spalteafstand", "fringe interferens"]},
    # Termodynamik
    {"label": "Ideel gaslov pV=nRT › Termodynamik", "page": "pages/6_Termodynamik.py", "nav_key": None, "nav_value": None, "keywords": ["ideel gaslov", "pV=nRT", "tryk volumen temperatur", "gas beregn", "stofmængde gas", "mol gas"]},
    {"label": "Kombineret gaslov › Termodynamik", "page": "pages/6_Termodynamik.py", "nav_key": None, "nav_value": None, "keywords": ["kombineret gaslov", "to tilstande gas", "p1V1/T1", "isoterm", "isobar", "isochor"]},
    {"label": "Varmekapacitet Q=mcΔT › Termodynamik", "page": "pages/6_Termodynamik.py", "nav_key": None, "nav_value": None, "keywords": ["varmekapacitet", "Q=mcΔT", "opvarmning afkøling", "spec varmekapacitet", "kalorimetri", "varme"]},
    {"label": "Faseovergang Q=mL › Termodynamik", "page": "pages/6_Termodynamik.py", "nav_key": None, "nav_value": None, "keywords": ["faseovergang", "latent varme", "smeltning", "fordampning", "smeltevarme", "dampvarme", "fase"]},
    {"label": "Carnot-virkningsgrad › Termodynamik", "page": "pages/6_Termodynamik.py", "nav_key": None, "nav_value": None, "keywords": ["carnot", "virkningsgrad termodynamik", "varmepumpe", "varmemaskine", "nyttevirkningsgrad"]},
    # Atomfysik
    {"label": "Radioaktivt henfald › Atomfysik", "page": "pages/7_Atomfysik.py", "nav_key": None, "nav_value": None, "keywords": ["radioaktivt henfald", "N=N0 exp", "henfaldskonstant", "radioaktivitet", "henfald"]},
    {"label": "Halvvejstid › Atomfysik", "page": "pages/7_Atomfysik.py", "nav_key": None, "nav_value": None, "keywords": ["halvvejstid", "T1/2", "halvt tilbage", "henfaldstid", "halverings"]},
    {"label": "E=mc² massedefekt › Atomfysik", "page": "pages/7_Atomfysik.py", "nav_key": None, "nav_value": None, "keywords": ["E=mc2", "massedefekt", "kerneenergi", "kernefysik", "atommasseenhed", "fusion fission"]},
    {"label": "Fotonenergi E=hf › Atomfysik", "page": "pages/7_Atomfysik.py", "nav_key": None, "nav_value": None, "keywords": ["fotonenergi", "foton", "E=hf", "planck konstant", "fotonstråling", "bølgelængde foton energi"]},
    # Usikkerhed
    {"label": "Gennemsnit og stdafv. › Usikkerhed", "page": "pages/8_Usikkerhed.py", "nav_key": None, "nav_value": None, "keywords": ["gennemsnit", "standardafvigelse", "statistik", "middelværdi", "spredning", "måleværdier"]},
    {"label": "Fejlpropagation › Usikkerhed", "page": "pages/8_Usikkerhed.py", "nav_key": None, "nav_value": None, "keywords": ["fejlpropagation", "usikkerhed formel", "type A type B", "måleusikkerhed", "u(x)"]},
    {"label": "Potenslov-fitting › Usikkerhed", "page": "pages/8_Usikkerhed.py", "nav_key": None, "nav_value": None, "keywords": ["potenslov fitting", "log-log regression", "y=Axα", "eksponent fitting", "lineær regression log"]},
    # Rotation
    {"label": "Inertimoment › Rotation", "page": "pages/9_Rotation.py", "nav_key": "rot_formel", "nav_value": "Inertimoment – standardlegemer", "keywords": ["inertimoment", "masseinertimoment", "I rotation", "skive kugle cylinder inertimoment"]},
    {"label": "Impulsmomentbevarelse › Rotation", "page": "pages/9_Rotation.py", "nav_key": "rot_formel", "nav_value": "Bevarelse af impulsmoment", "keywords": ["impulsmomentbevarelse", "I1w1=I2w2", "skater rotation", "vinkelhastighed ændres", "skive lander"]},
    {"label": "τ=I·α drejningsmoment › Rotation", "page": "pages/9_Rotation.py", "nav_key": "rot_formel", "nav_value": "Newtons 2. lov for rotation:  τ = I·α", "keywords": ["drejningsmoment", "vinkelacceleration", "tau=Ialpha", "torque", "rotationens newton"]},
    # Kollisioner
    {"label": "Elastisk kollision › Kollisioner", "page": "pages/10_Kollisioner.py", "nav_key": None, "nav_value": None, "keywords": ["elastisk kollision", "KE bevaret", "elastisk stød", "hastighederne bytter", "bolde støder elastisk"]},
    {"label": "Uelastisk kollision › Kollisioner", "page": "pages/10_Kollisioner.py", "nav_key": None, "nav_value": None, "keywords": ["uelastisk kollision", "klæber sammen", "fuldstændig uelastisk", "KE-tab kollision", "hænger sammen"]},
    {"label": "Eksplosion › Kollisioner", "page": "pages/10_Kollisioner.py", "nav_key": None, "nav_value": None, "keywords": ["eksplosion", "udskydning raket", "impulsbevarelse eksplosion", "dele flyver fra hinanden"]},
]


def render_search_sidebar():
    with st.sidebar:
        st.markdown("---")
        søg = st.text_input("🔍 Søg formel...", key="sidebar_search", placeholder="fx 'halvvejstid'")
        if søg and len(søg) >= 2:
            søg_lower = søg.lower()
            hits = [e for e in SEARCH_INDEX if any(søg_lower in kw for kw in e["keywords"])]
            if hits:
                st.markdown(f"**{len(hits)} resultat{'er' if len(hits) != 1 else ''}:**")
                for hit in hits[:8]:
                    if st.button(hit["label"], key=f"srch_{hit['label'][:40]}", use_container_width=True):
                        if hit.get("nav_key") and hit.get("nav_value"):
                            st.session_state[hit["nav_key"]] = hit["nav_value"]
                        try:
                            st.switch_page(hit["page"])
                        except Exception:
                            st.info(f"👈 Gå til siden i menuen til venstre.")
            else:
                st.caption("Ingen resultater – prøv et andet søgeord.")


def _render_styled_tab_nav(options, key, nav_key=None):
    """Styled radio-knapper som erstatning for st.selectbox til formelvalg.
    nav_key: session state nøgle der bruges til deep-linking fra forsiden."""
    if nav_key and st.session_state.get(nav_key) in options:
        st.session_state[key] = st.session_state.pop(nav_key)

    st.markdown("""<style>
    div[data-testid="stRadio"] > label { display: none; }
    div[data-testid="stRadio"] > div { flex-wrap: wrap; gap: 6px; }
    div[data-testid="stRadio"] > div > label {
        border: 1px solid #ddd; border-radius: 6px;
        padding: 4px 10px; cursor: pointer; font-size: 0.9em;
    }
    div[data-testid="stRadio"] > div > label:has(input:checked) {
        border-bottom: 3px solid #e74c3c; font-weight: 600;
    }
    </style>""", unsafe_allow_html=True)
    return st.radio("Vælg beregning:", options, key=key, horizontal=True, label_visibility="collapsed")
