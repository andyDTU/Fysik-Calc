import streamlit as st
from utils import show_sidebar_constants, show_resultat_sidebar, FORMLER

st.set_page_config(page_title="Søg formel", page_icon="🔍", layout="wide")
show_sidebar_constants()
show_resultat_sidebar()

st.title("🔍 Søg efter formel")
st.markdown("Skriv et nøgleord – formelnavn, symbol eller emne – og hop direkte til beregneren.")
st.divider()

# ── Søgefelt ──────────────────────────────────────────────────────────────────
søg = st.text_input("", placeholder="fx  centripetal  /  v²  /  kondensator  /  RSS  /  planck ...",
                    label_visibility="collapsed")

# ── Side-filter ───────────────────────────────────────────────────────────────
alle_sider = sorted(set(f["side"] for f in FORMLER))
med_filter = st.checkbox("Filtrer på emne", value=False)
if med_filter:
    valgte_sider = st.multiselect("Emner:", alle_sider, default=alle_sider)
else:
    valgte_sider = alle_sider

st.divider()

# ── Filtrer formler ───────────────────────────────────────────────────────────
søg_lc = søg.strip().lower()

if søg_lc:
    hits = [
        f for f in FORMLER
        if f["side"] in valgte_sider
        and (søg_lc in f["navn"].lower() or søg_lc in f["kw"].lower())
    ]
else:
    hits = [f for f in FORMLER if f["side"] in valgte_sider]

# ── Vis resultater ────────────────────────────────────────────────────────────
if not hits:
    st.warning("Ingen formler matchede din søgning. Prøv et andet søgeord.")
else:
    # Grupper efter side
    sider_i_hits = []
    for s in alle_sider:
        gruppe = [f for f in hits if f["side"] == s]
        if gruppe:
            sider_i_hits.append((s, gruppe))

    for side_navn, formler in sider_i_hits:
        emoji_map = {
            "Kinematik": "🏃", "Dynamik": "💪", "Energi": "🔋",
            "Elektricitet": "⚡", "Bølger & Optik": "🌊", "Termodynamik": "🌡️",
            "Atomfysik": "☢️", "Usikkerhed": "📏", "Rotation": "🔄",
            "Kollisioner": "💥", "Svingninger": "〰️",
        }
        emoji = emoji_map.get(side_navn, "📐")
        st.markdown(f"### {emoji} {side_navn}")

        for f in formler:
            col1, col2 = st.columns([5, 1])
            col1.markdown(f"**{f['navn']}**")
            if col2.button("→ Åbn", key=f"btn_{f['navn']}"):
                st.session_state[f["key"]] = f["navn"]
                st.switch_page(f["fil"])

        st.markdown("")

# ── Bundlinje: antal resultater ───────────────────────────────────────────────
if søg_lc:
    st.caption(f"{len(hits)} formel(er) fundet for '{søg}'  –  {len(FORMLER)} formler i alt")
else:
    st.caption(f"Viser alle {len(hits)} formler  –  brug søgefeltet til at filtrere")
