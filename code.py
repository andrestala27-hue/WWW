import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Simulador del Mundial", page_icon="🏆", layout="wide")

# ── DATOS ────────────────────────────────────────────────────────────────────

GROUPS = {
    "A": ["Qatar", "Ecuador", "Senegal", "Países Bajos"],
    "B": ["Inglaterra", "Irán", "Estados Unidos", "Gales"],
    "C": ["Argentina", "Arabia Saudita", "México", "Polonia"],
    "D": ["Francia", "Australia", "Dinamarca", "Túnez"],
    "E": ["España", "Costa Rica", "Alemania", "Japón"],
    "F": ["Bélgica", "Canadá", "Marruecos", "Croacia"],
    "G": ["Brasil", "Serbia", "Suiza", "Camerún"],
    "H": ["Portugal", "Ghana", "Uruguay", "Corea del Sur"],
}

FLAGS = {
    "Qatar": "🇶🇦", "Ecuador": "🇪🇨", "Senegal": "🇸🇳", "Países Bajos": "🇳🇱",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Irán": "🇮🇷", "Estados Unidos": "🇺🇸", "Gales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿",
    "Argentina": "🇦🇷", "Arabia Saudita": "🇸🇦", "México": "🇲🇽", "Polonia": "🇵🇱",
    "Francia": "🇫🇷", "Australia": "🇦🇺", "Dinamarca": "🇩🇰", "Túnez": "🇹🇳",
    "España": "🇪🇸", "Costa Rica": "🇨🇷", "Alemania": "🇩🇪", "Japón": "🇯🇵",
    "Bélgica": "🇧🇪", "Canadá": "🇨🇦", "Marruecos": "🇲🇦", "Croacia": "🇭🇷",
    "Brasil": "🇧🇷", "Serbia": "🇷🇸", "Suiza": "🇨🇭", "Camerún": "🇨🇲",
    "Portugal": "🇵🇹", "Ghana": "🇬🇭", "Uruguay": "🇺🇾", "Corea del Sur": "🇰🇷",
}

def flag(team):
    return FLAGS.get(team, "🏳️")

# Cruce de octavos: (1ro grupo X vs 2do grupo Y)
R16_MATCHUPS = [
    ("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"),
    ("B", "A"), ("D", "C"), ("F", "E"), ("H", "G"),
]

# ── SIMULACIÓN ───────────────────────────────────────────────────────────────

def sim_match(a, b):
    ga, gb = random.randint(0, 4), random.randint(0, 4)
    if ga == gb:
        winner = random.choice([a, b])
    else:
        winner = a if ga > gb else b
    return winner, ga, gb

def sim_group(teams):
    table = {t: {"pts":0,"pj":0,"pg":0,"pe":0,"pp":0,"gf":0,"gc":0,"gd":0} for t in teams}
    results = []
    for i in range(len(teams)):
        for j in range(i+1, len(teams)):
            a, b = teams[i], teams[j]
            ga, gb = random.randint(0,4), random.randint(0,4)
            results.append((a, b, ga, gb))
            table[a]["pj"] += 1; table[b]["pj"] += 1
            table[a]["gf"] += ga; table[a]["gc"] += gb
            table[b]["gf"] += gb; table[b]["gc"] += ga
            table[a]["gd"] += ga-gb; table[b]["gd"] += gb-ga
            if ga > gb:
                table[a]["pts"] += 3; table[a]["pg"] += 1; table[b]["pp"] += 1
            elif gb > ga:
                table[b]["pts"] += 3; table[b]["pg"] += 1; table[a]["pp"] += 1
            else:
                table[a]["pts"] += 1; table[b]["pts"] += 1
                table[a]["pe"] += 1; table[b]["pe"] += 1
    sorted_t = sorted(table.items(), key=lambda x: (x[1]["pts"], x[1]["gd"], x[1]["gf"]), reverse=True)
    return sorted_t, results

# ── SESSION STATE ─────────────────────────────────────────────────────────────

if "groups" not in st.session_state:
    st.session_state.groups = {k: list(v) for k, v in GROUPS.items()}
if "qualifiers" not in st.session_state:
    st.session_state.qualifiers = {g: (t[0], t[1]) for g, t in st.session_state.groups.items()}

# ── SIDEBAR ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🏆 Mundial Sim")
    st.divider()
    if st.button("🎲 Simular TODO el torneo", use_container_width=True):
        for g, teams in st.session_state.groups.items():
            sorted_t, results = sim_group(teams)
            st.session_state[f"gr_{g}"] = (sorted_t, results)
            st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
        st.rerun()
    if st.button("🔄 Reiniciar todo", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k != "groups":
                del st.session_state[k]
        st.session_state.qualifiers = {g: (t[0], t[1]) for g, t in st.session_state.groups.items()}
        st.rerun()

# ── TÍTULO ────────────────────────────────────────────────────────────────────

st.title("⚽ Simulador del Mundial 🏆")
st.divider()

tab1, tab2 = st.tabs(["⚽ Fase de Grupos", "🏆 Eliminatorias"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GRUPOS
# ═══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.header("Fase de Grupos")

    # Botón para simular todos los grupos
    if st.button("🎲 Simular todos los grupos"):
        for g, teams in st.session_state.groups.items():
            sorted_t, results = sim_group(teams)
            st.session_state[f"gr_{g}"] = (sorted_t, results)
            st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
        st.rerun()

    st.divider()

    # Mostrar grupos en pares de columnas
    group_names = list(st.session_state.groups.keys())
    for row in range(0, len(group_names), 2):
        cols = st.columns(2)
        for col_idx, g in enumerate(group_names[row:row+2]):
            with cols[col_idx]:
                teams = st.session_state.groups[g]
                st.subheader(f"Grupo {g}")

                # Botón simular
                if st.button(f"🎲 Simular Grupo {g}", key=f"sim_{g}"):
                    sorted_t, results = sim_group(teams)
                    st.session_state[f"gr_{g}"] = (sorted_t, results)
                    st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
                    st.rerun()

                # Mostrar tabla
                if f"gr_{g}" in st.session_state:
                    sorted_t, results = st.session_state[f"gr_{g}"]
                    data = []
                    for i, (team, s) in enumerate(sorted_t):
                        medal = "🥇" if i==0 else "🥈" if i==1 else "  "
                        gd_str = f"+{s['gd']}" if s['gd'] > 0 else str(s['gd'])
                        data.append({
                            "": medal,
                            "Equipo": f"{flag(team)} {team}",
                            "Pts": s["pts"], "PJ": s["pj"],
                            "PG": s["pg"], "PE": s["pe"], "PP": s["pp"],
                            "GF": s["gf"], "GC": s["gc"], "GD": gd_str,
                        })
                    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

                    with st.expander("Ver partidos"):
                        for a, b, ga, gb in results:
                            st.write(f"{flag(a)} {a} **{ga}–{gb}** {b} {flag(b)}")

                    first, second = st.session_state.qualifiers[g]
                    st.success(f"Clasificados: 🥇 {flag(first)} {first}  |  🥈 {flag(second)} {second}")
                else:
                    # Tabla vacía
                    data = [{"Equipo": f"{flag(t)} {t}", "Pts":0,"PJ":0,"PG":0,"PE":0,"PP":0,"GF":0,"GC":0,"GD":0} for t in teams]
                    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

                st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ELIMINATORIAS
# ═══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.header("Fase Eliminatoria")
    q = st.session_state.qualifiers

    # ── Función para renderizar una ronda ─────────────────────────────────────
    def render_round(title, matches, key):
        st.subheader(title)
        wk = f"w_{key}"
        if wk not in st.session_state:
            st.session_state[wk] = {}

        if st.button(f"🎲 Simular {title}", key=f"sim_all_{key}"):
            for i, (a, b) in enumerate(matches):
                w, ga, gb = sim_match(a, b)
                st.session_state[wk][i] = {"w": w, "ga": ga, "gb": gb, "a": a, "b": b}
            st.rerun()

        cols = st.columns(min(len(matches), 4))
        for i, (a, b) in enumerate(matches):
            with cols[i % len(cols)]:
                if i in st.session_state[wk]:
                    d = st.session_state[wk][i]
                    loser = b if d["w"] == a else a
                    st.markdown(f"✅ {flag(d['w'])} **{d['w']}**")
                    st.caption(f"{d['ga']}–{d['gb']}")
                    st.markdown(f"~~{flag(loser)} {loser}~~")
                    if st.button("↩", key=f"reset_{key}_{i}"):
                        del st.session_state[wk][i]
                        st.rerun()
                else:
                    st.markdown(f"{flag(a)} **{a}**")
                    st.caption("vs")
                    st.markdown(f"{flag(b)} **{b}**")
                    if st.button("🎲", key=f"sim_{key}_{i}"):
                        w, ga, gb = sim_match(a, b)
                        st.session_state[wk][i] = {"w": w, "ga": ga, "gb": gb, "a": a, "b": b}
                        st.rerun()
                    choice = st.selectbox("Manual", ["—", a, b], key=f"man_{key}_{i}", label_visibility="collapsed")
                    if choice != "—":
                        st.session_state[wk][i] = {"w": choice, "ga": 1, "gb": 0, "a": a, "b": b}
                        st.rerun()

        st.divider()

        if len(st.session_state[wk]) == len(matches):
            winners = [st.session_state[wk][i]["w"] for i in range(len(matches))]
            losers  = [
                st.session_state[wk][i]["b"] if st.session_state[wk][i]["w"] == st.session_state[wk][i]["a"]
                else st.session_state[wk][i]["a"]
                for i in range(len(matches))
            ]
            return winners, losers
        else:
            pending = len(matches) - len(st.session_state[wk])
            st.info(f"⏳ Faltan {pending} partido(s) en esta ronda.")
            return [], []

    # ── Octavos ───────────────────────────────────────────────────────────────
    r16 = [(q[g1][0], q[g2][1]) for g1, g2 in R16_MATCHUPS if g1 in q and g2 in q]
    w_r16, _ = render_round("⚔️ Octavos de Final", r16, "r16")
    if len(w_r16) < 8:
        st.stop()

    # ── Cuartos ───────────────────────────────────────────────────────────────
    qf = [(w_r16[i], w_r16[i+1]) for i in range(0, 8, 2)]
    w_qf, _ = render_round("🔥 Cuartos de Final", qf, "qf")
    if len(w_qf) < 4:
        st.stop()

    # ── Semis ─────────────────────────────────────────────────────────────────
    sf = [(w_qf[0], w_qf[1]), (w_qf[2], w_qf[3])]
    w_sf, l_sf = render_round("⭐ Semifinales", sf, "sf")
    if len(w_sf) < 2:
        st.stop()

    # ── Tercer lugar ──────────────────────────────────────────────────────────
    if len(l_sf) == 2:
        st.subheader("🥉 Tercer Lugar")
        tp_key = "w_tp"
        if tp_key not in st.session_state:
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"{flag(l_sf[0])} **{l_sf[0]}** vs {flag(l_sf[1])} **{l_sf[1]}**")
            with c2:
                if st.button("🎲 Simular 3er lugar"):
                    w, ga, gb = sim_match(l_sf[0], l_sf[1])
                    st.session_state[tp_key] = (w, ga, gb)
                    st.rerun()
        else:
            w, ga, gb = st.session_state[tp_key]
            loser = l_sf[1] if w == l_sf[0] else l_sf[0]
            st.success(f"🥉 {flag(w)} **{w}** {ga}–{gb} {loser} {flag(loser)}")
            if st.button("↩ Rejugar 3er lugar"):
                del st.session_state[tp_key]
                st.rerun()
        st.divider()

    # ── Final ─────────────────────────────────────────────────────────────────
    st.subheader("🏆 GRAN FINAL")
    a, b = w_sf[0], w_sf[1]
    fk = "final"

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"### {flag(a)} {a}  vs  {b} {flag(b)}")
        if fk not in st.session_state:
            bc1, bc2, bc3 = st.columns(3)
            with bc1:
                if st.button(f"🏆 {a}"):
                    st.session_state[fk] = a; st.rerun()
            with bc2:
                if st.button("🎲 Simular"):
                    w, _, _ = sim_match(a, b)
                    st.session_state[fk] = w; st.rerun()
            with bc3:
                if st.button(f"🏆 {b}"):
                    st.session_state[fk] = b; st.rerun()
        else:
            champion = st.session_state[fk]
            st.balloons()
            st.markdown(f"""
            <div style='text-align:center; padding:30px; background:linear-gradient(135deg,#c9a227,#f0d060);
                        border-radius:15px; border:3px solid gold;'>
                <div style='font-size:3em;'>🏆</div>
                <div style='font-size:1em; color:#5a3e00; font-weight:bold;'>CAMPEÓN DEL MUNDO</div>
                <div style='font-size:2.5em; font-weight:bold; color:#3a2a00;'>
                    {flag(champion)} {champion}
                </div>
                <div style='font-size:2em;'>🎉🎊🎉</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("↩ Rejugar la final"):
                del st.session_state[fk]; st.rerun()
