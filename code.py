import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Simulador del Mundial", page_icon="🏆", layout="wide")

# ── CSS: fondo campo de fútbol ────────────────────────────────────────────────
st.markdown("""
<style>
/* Fondo campo de fútbol */
.stApp {
    background-color: #2d7a2d;
    background-image:
        /* Líneas blancas del campo */
        linear-gradient(white 2px, transparent 2px),
        linear-gradient(90deg, white 2px, transparent 2px),
        /* Líneas del área */
        repeating-linear-gradient(transparent, transparent 98%, white 98%, white 100%);
    background-size: 100% 100%;
}

/* Campo completo usando pseudo-elemento */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        /* Borde exterior */
        linear-gradient(white, white) top 4% left 5% / 90% 2px no-repeat,
        linear-gradient(white, white) bottom 4% left 5% / 90% 2px no-repeat,
        linear-gradient(white, white) top 4% left 5% / 2px 92% no-repeat,
        linear-gradient(white, white) top 4% right 5% / 2px 92% no-repeat,
        /* Línea del medio */
        linear-gradient(white, white) top 4% left 50% / 2px 92% no-repeat,
        /* Círculo central */
        radial-gradient(circle at 50% 50%, transparent 7.5%, white 7.5%, white 8%, transparent 8%) center / 100% 100% no-repeat,
        /* Punto central */
        radial-gradient(circle at 50% 50%, white 0.5%, transparent 0.5%) center / 100% 100% no-repeat,
        /* Área grande izquierda */
        linear-gradient(white, white) top 27% left 5% / 12% 2px no-repeat,
        linear-gradient(white, white) bottom 27% left 5% / 12% 2px no-repeat,
        linear-gradient(white, white) top 27% left 17% / 2px 46% no-repeat,
        /* Área grande derecha */
        linear-gradient(white, white) top 27% right 5% / 12% 2px no-repeat,
        linear-gradient(white, white) bottom 27% right 5% / 12% 2px no-repeat,
        linear-gradient(white, white) top 27% right 17% / 2px 46% no-repeat,
        /* Área chica izquierda */
        linear-gradient(white, white) top 38% left 5% / 6% 2px no-repeat,
        linear-gradient(white, white) bottom 38% left 5% / 6% 2px no-repeat,
        linear-gradient(white, white) top 38% left 11% / 2px 24% no-repeat,
        /* Área chica derecha */
        linear-gradient(white, white) top 38% right 5% / 6% 2px no-repeat,
        linear-gradient(white, white) bottom 38% right 5% / 6% 2px no-repeat,
        linear-gradient(white, white) top 38% right 11% / 2px 24% no-repeat;
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
}

/* Overlay oscuro para legibilidad */
.stApp::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 30, 0, 0.55);
    pointer-events: none;
    z-index: 0;
}

/* Todo el contenido encima del overlay */
.stApp > * { position: relative; z-index: 1; }
[data-testid="stHeader"] { background: rgba(0,0,0,0.4) !important; z-index: 10; }
[data-testid="stSidebar"] {
    background: rgba(0, 20, 0, 0.88) !important;
    border-right: 1px solid #2d6a4f;
    z-index: 10;
}

/* Texto */
h1, h2, h3, h4, p, label, .stMarkdown { color: #e8f5e9 !important; }

/* Botones */
.stButton > button {
    background-color: rgba(27, 67, 50, 0.85);
    color: #b7e4c7;
    border: 1px solid #52b788;
    border-radius: 8px;
}
.stButton > button:hover {
    background-color: #2d6a4f;
    color: white;
    border-color: #95d5b2;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    background: rgba(0, 20, 0, 0.75) !important;
    border-radius: 8px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: rgba(0,20,0,0.6); border-radius: 8px; }
.stTabs [data-baseweb="tab"] { color: #95d5b2 !important; }
.stTabs [aria-selected="true"] { background: rgba(45, 106, 79, 0.9) !important; }

/* Selectbox */
[data-baseweb="select"] { background: rgba(0,20,0,0.8) !important; }

/* Cards de partidos */
.match-card {
    background: rgba(0, 20, 0, 0.80);
    border: 1px solid #2d6a4f;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
}

/* Expander */
[data-testid="stExpander"] { background: rgba(0,20,0,0.7) !important; border: 1px solid #2d6a4f; border-radius: 8px; }

div[data-testid="stVerticalBlock"] { gap: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── DATOS ─────────────────────────────────────────────────────────────────────

GROUPS = {
    "A": ["México", "Sudáfrica", "República de Corea", "Chequia"],
    "B": ["Canadá", "Bosnia y Herzegovina", "Catar", "Suiza"],
    "C": ["Brasil", "Marruecos", "Haití", "Escocia"],
    "D": ["Estados Unidos", "Paraguay", "Australia", "Turquía"],
    "E": ["Alemania", "Curazao", "Costa de Marfil", "Ecuador"],
    "F": ["Países Bajos", "Japón", "Suecia", "Túnez"],
    "G": ["Bélgica", "Egipto", "RI de Irán", "Nueva Zelanda"],
    "H": ["España", "Cabo Verde", "Arabia Saudí", "Uruguay"],
    "I": ["Francia", "Senegal", "Irak", "Noruega"],
    "J": ["Argentina", "Argelia", "Austria", "Jordania"],
    "K": ["Portugal", "RD de Congo", "Uzbekistán", "Colombia"],
    "L": ["Inglaterra", "Croacia", "Ghana", "Panamá"],
}

FLAGS = {
    "México": "🇲🇽", "Sudáfrica": "🇿🇦", "República de Corea": "🇰🇷", "Chequia": "🇨🇿",
    "Canadá": "🇨🇦", "Bosnia y Herzegovina": "🇧🇦", "Catar": "🇶🇦", "Suiza": "🇨🇭",
    "Brasil": "🇧🇷", "Marruecos": "🇲🇦", "Haití": "🇭🇹", "Escocia": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "Estados Unidos": "🇺🇸", "Paraguay": "🇵🇾", "Australia": "🇦🇺", "Turquía": "🇹🇷",
    "Alemania": "🇩🇪", "Curazao": "🇨🇼", "Costa de Marfil": "🇨🇮", "Ecuador": "🇪🇨",
    "Países Bajos": "🇳🇱", "Japón": "🇯🇵", "Suecia": "🇸🇪", "Túnez": "🇹🇳",
    "Bélgica": "🇧🇪", "Egipto": "🇪🇬", "RI de Irán": "🇮🇷", "Nueva Zelanda": "🇳🇿",
    "España": "🇪🇸", "Cabo Verde": "🇨🇻", "Arabia Saudí": "🇸🇦", "Uruguay": "🇺🇾",
    "Francia": "🇫🇷", "Senegal": "🇸🇳", "Irak": "🇮🇶", "Noruega": "🇳🇴",
    "Argentina": "🇦🇷", "Argelia": "🇩🇿", "Austria": "🇦🇹", "Jordania": "🇯🇴",
    "Portugal": "🇵🇹", "RD de Congo": "🇨🇩", "Uzbekistán": "🇺🇿", "Colombia": "🇨🇴",
    "Inglaterra": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Croacia": "🇭🇷", "Ghana": "🇬🇭", "Panamá": "🇵🇦",
}

# Con 12 grupos, el cruce de octavos/16avos sigue la lógica 1ro vs 2do del grupo opuesto
# Ajustamos para 12 grupos → 24 clasificados → 24avos de final (los 12 primeros de grupo vs los 12 segundos)
R24_MATCHUPS = [
    ("A","B"),("C","D"),("E","F"),("G","H"),("I","J"),("K","L"),
    ("B","A"),("D","C"),("F","E"),("H","G"),("J","I"),("L","K"),
]

def flag(team):
    return FLAGS.get(team, "🏳️")

# ── SIMULACIÓN ────────────────────────────────────────────────────────────────

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
            table[a]["pj"]+=1; table[b]["pj"]+=1
            table[a]["gf"]+=ga; table[a]["gc"]+=gb
            table[b]["gf"]+=gb; table[b]["gc"]+=ga
            table[a]["gd"]+=ga-gb; table[b]["gd"]+=gb-ga
            if ga > gb:
                table[a]["pts"]+=3; table[a]["pg"]+=1; table[b]["pp"]+=1
            elif gb > ga:
                table[b]["pts"]+=3; table[b]["pg"]+=1; table[a]["pp"]+=1
            else:
                table[a]["pts"]+=1; table[b]["pts"]+=1
                table[a]["pe"]+=1; table[b]["pe"]+=1
    sorted_t = sorted(table.items(), key=lambda x:(x[1]["pts"],x[1]["gd"],x[1]["gf"]), reverse=True)
    return sorted_t, results

# ── SESSION STATE ─────────────────────────────────────────────────────────────

if "groups" not in st.session_state:
    st.session_state.groups = {k: list(v) for k, v in GROUPS.items()}
if "qualifiers" not in st.session_state:
    st.session_state.qualifiers = {g: (t[0], t[1]) for g, t in st.session_state.groups.items()}
if "started" not in st.session_state:
    st.session_state.started = False

# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA DE BIENVENIDA
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.started:
    import base64
    try:
        with open("yphqak29xt4.jpg", "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        img_css = f"data:image/jpeg;base64,{img_b64}"
    except FileNotFoundError:
        img_css = ""

    st.markdown(f"""
    <style>
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stSidebar"] {{ display: none !important; }}
    .stApp::before {{ display: none !important; }}
    .stApp::after {{ display: none !important; }}
    .stApp {{
        background-image: url("{img_css}") !important;
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
        background-color: #000 !important;
    }}
    .welcome-overlay {{
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.50);
        z-index: 0;
        pointer-events: none;
    }}
    .welcome-content {{
        position: relative;
        z-index: 1;
        text-align: center;
        padding: 80px 20px 20px 20px;
    }}
    div[data-testid="stButton"] > button {{
        font-size: 1.4em !important;
        padding: 18px 48px !important;
        background: linear-gradient(135deg, #c9a227, #ffd700) !important;
        color: #1a0a00 !important;
        border: none !important;
        border-radius: 50px !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        box-shadow: 0 6px 30px rgba(0,0,0,0.6) !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #ffd700, #f0d060) !important;
    }}
    </style>
    <div class="welcome-overlay"></div>
    <div class="welcome-content">
        <div style="font-size:5em; filter:drop-shadow(2px 2px 8px rgba(0,0,0,0.9));">🏆</div>
        <h1 style="font-size:3.5em; font-weight:900; color:#ffd700;
                   text-shadow:3px 3px 12px rgba(0,0,0,0.95); letter-spacing:2px; margin:10px 0;">
            Simulador del Mundial
        </h1>
        <p style="font-size:1.3em; color:#ffffff;
                  text-shadow:1px 1px 6px rgba(0,0,0,0.9); margin-bottom:50px;">
            48 equipos &nbsp;·&nbsp; 12 grupos &nbsp;·&nbsp; ¡Simula tu torneo!
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("⚽  EMPEZAR SIMULACIÓN  ⚽", use_container_width=True):
            st.session_state.started = True
            st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🏆 Mundial Sim")
    st.divider()
    if st.button("🎲 Simular TODO el torneo", use_container_width=True):
        for g, teams in st.session_state.groups.items():
            sorted_t, results = sim_group(teams)
            st.session_state[f"gr_{g}"] = (sorted_t, results)
            st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
        st.rerun()
    if st.button("🔄 Reiniciar todo", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k not in ("groups", "started"):
                del st.session_state[k]
        st.session_state.qualifiers = {g: (t[0], t[1]) for g, t in st.session_state.groups.items()}
        st.rerun()
    if st.button("⬅️ Volver al inicio", use_container_width=True):
        st.session_state.started = False
        st.rerun()

# ── Título ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 10px 0 5px 0;'>
    <h1 style='color:#ffd700 !important; text-shadow: 1px 1px 6px rgba(0,0,0,0.9);'>
        ⚽ Simulador del Mundial 🏆
    </h1>
</div>
""", unsafe_allow_html=True)
st.divider()

tab1, tab2 = st.tabs(["⚽  Fase de Grupos", "🏆  Eliminatorias"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GRUPOS
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.header("Fase de Grupos")

    if st.button("🎲 Simular TODOS los grupos", use_container_width=False):
        for g, teams in st.session_state.groups.items():
            sorted_t, results = sim_group(teams)
            st.session_state[f"gr_{g}"] = (sorted_t, results)
            st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
        st.rerun()

    st.divider()

    group_names = list(st.session_state.groups.keys())
    for row in range(0, len(group_names), 3):
        cols = st.columns(3)
        for col_idx, g in enumerate(group_names[row:row+3]):
            with cols[col_idx]:
                teams = st.session_state.groups[g]

                st.markdown(f"""
                <div style='background:rgba(0,30,0,0.75); border:1px solid #2d6a4f;
                            border-radius:10px; padding:12px; margin-bottom:4px;'>
                    <h3 style='margin:0; color:#ffd700 !important;'>Grupo {g}</h3>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🎲 Simular Grupo {g}", key=f"sim_{g}"):
                    sorted_t, results = sim_group(teams)
                    st.session_state[f"gr_{g}"] = (sorted_t, results)
                    st.session_state.qualifiers[g] = (sorted_t[0][0], sorted_t[1][0])
                    st.rerun()

                if f"gr_{g}" in st.session_state:
                    sorted_t, results = st.session_state[f"gr_{g}"]
                    data = []
                    for i, (team, s) in enumerate(sorted_t):
                        medal = "🥇" if i==0 else "🥈" if i==1 else "  "
                        gd_str = f"+{s['gd']}" if s['gd']>0 else str(s['gd'])
                        data.append({
                            "": medal,
                            "Equipo": f"{flag(team)} {team}",
                            "Pts": s["pts"], "PG": s["pg"], "PE": s["pe"],
                            "PP": s["pp"], "GD": gd_str,
                        })
                    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

                    with st.expander("📋 Partidos"):
                        for a, b, ga, gb in results:
                            st.write(f"{flag(a)} {a} **{ga}–{gb}** {b} {flag(b)}")

                    first, second = st.session_state.qualifiers[g]
                    st.markdown(f"""
                    <div style='background:rgba(27,67,50,0.8); border-radius:8px; padding:8px; font-size:0.9em;'>
                        🥇 {flag(first)} <b>{first}</b><br>
                        🥈 {flag(second)} <b>{second}</b>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    data = [{"Equipo": f"{flag(t)} {t}", "Pts":"-","PG":"-","PE":"-","PP":"-","GD":"-"} for t in teams]
                    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

                st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ELIMINATORIAS
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.header("Fase Eliminatoria")
    q = st.session_state.qualifiers

    def render_round(title, matches, key):
        st.subheader(title)
        wk = f"w_{key}"
        if wk not in st.session_state:
            st.session_state[wk] = {}

        if st.button(f"🎲 Simular {title}", key=f"sim_all_{key}"):
            for i, (a, b) in enumerate(matches):
                w, ga, gb = sim_match(a, b)
                st.session_state[wk][i] = {"w":w,"ga":ga,"gb":gb,"a":a,"b":b}
            st.rerun()

        num_cols = min(len(matches), 4)
        cols = st.columns(num_cols)
        for i, (a, b) in enumerate(matches):
            with cols[i % num_cols]:
                st.markdown(f"""
                <div style='background:rgba(0,20,0,0.82); border:1px solid #2d6a4f;
                            border-radius:10px; padding:10px; margin-bottom:6px; min-height:100px;'>
                """, unsafe_allow_html=True)

                if i in st.session_state[wk]:
                    d = st.session_state[wk][i]
                    loser = b if d["w"]==a else a
                    st.markdown(f"✅ {flag(d['w'])} **{d['w']}**")
                    st.caption(f"Resultado: {d['ga']}–{d['gb']}")
                    st.markdown(f"❌ {flag(loser)} ~~{loser}~~")
                    if st.button("↩ Cambiar", key=f"reset_{key}_{i}"):
                        del st.session_state[wk][i]; st.rerun()
                else:
                    st.markdown(f"{flag(a)} **{a}**")
                    st.caption("vs")
                    st.markdown(f"{flag(b)} **{b}**")
                    if st.button("🎲", key=f"sim_{key}_{i}", use_container_width=True):
                        w, ga, gb = sim_match(a, b)
                        st.session_state[wk][i] = {"w":w,"ga":ga,"gb":gb,"a":a,"b":b}
                        st.rerun()
                    choice = st.selectbox("Elegir", ["—", a, b], key=f"man_{key}_{i}", label_visibility="collapsed")
                    if choice != "—":
                        st.session_state[wk][i] = {"w":choice,"ga":1,"gb":0,"a":a,"b":b}
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        if len(st.session_state[wk]) == len(matches):
            winners = [st.session_state[wk][i]["w"] for i in range(len(matches))]
            losers  = [
                st.session_state[wk][i]["b"] if st.session_state[wk][i]["w"]==st.session_state[wk][i]["a"]
                else st.session_state[wk][i]["a"]
                for i in range(len(matches))
            ]
            return winners, losers
        else:
            pending = len(matches) - len(st.session_state[wk])
            st.info(f"⏳ Faltan {pending} partido(s) en esta ronda.")
            return [], []

    # Ronda de 24 (12 grupos → 24 clasificados)
    r24 = [(q[g1][0], q[g2][1]) for g1,g2 in R24_MATCHUPS if g1 in q and g2 in q]
    w_r24, _ = render_round("⚔️ Ronda de 24", r24, "r24")
    if len(w_r24) < 12: st.stop()

    # Cuartos de final (12 → 8, los 4 mejores primeros de grupo pasan directo - simplificado: 12→8)
    qf_matches = [(w_r24[i], w_r24[i+1]) for i in range(0, 8, 2)]
    w_qf, _ = render_round("🔥 Cuartos de Final", qf_matches, "qf")
    if len(w_qf) < 4: st.stop()

    # Semifinales
    sf_matches = [(w_qf[0], w_qf[1]), (w_qf[2], w_qf[3])]
    w_sf, l_sf = render_round("⭐ Semifinales", sf_matches, "sf")
    if len(w_sf) < 2: st.stop()

    # Tercer lugar
    if len(l_sf) == 2:
        st.subheader("🥉 Tercer Lugar")
        tp_key = "w_tp"
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"{flag(l_sf[0])} **{l_sf[0]}** vs {flag(l_sf[1])} **{l_sf[1]}**")
        with c2:
            if tp_key not in st.session_state:
                if st.button("🎲 Simular 3er lugar"):
                    w, ga, gb = sim_match(l_sf[0], l_sf[1])
                    st.session_state[tp_key] = (w, ga, gb); st.rerun()
            else:
                w, ga, gb = st.session_state[tp_key]
                loser = l_sf[1] if w==l_sf[0] else l_sf[0]
                st.success(f"🥉 {flag(w)} **{w}** {ga}–{gb} {flag(loser)} {loser}")
                if st.button("↩ Rejugar"):
                    del st.session_state[tp_key]; st.rerun()
        st.divider()

    # Gran Final
    st.subheader("🏆 GRAN FINAL")
    a, b = w_sf[0], w_sf[1]
    fk = "final"

    _, col2, _ = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <div style='text-align:center; background:rgba(0,20,0,0.85); border:2px solid gold;
                    border-radius:15px; padding:20px; margin-bottom:15px;'>
            <div style='font-size:1.6em; font-weight:bold; color:white;'>
                {flag(a)} {a}
            </div>
            <div style='color:#ffd700; font-size:1.2em; margin:8px 0;'>⚡ vs ⚡</div>
            <div style='font-size:1.6em; font-weight:bold; color:white;'>
                {flag(b)} {b}
            </div>
        </div>
        """, unsafe_allow_html=True)

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
            <div style='text-align:center; padding:30px;
                        background:linear-gradient(135deg,#c9a227,#f0d060);
                        border-radius:15px; border:3px solid #ffd700;'>
                <div style='font-size:3em;'>🏆</div>
                <div style='font-size:1em; color:#5a3e00; font-weight:bold; letter-spacing:3px;'>
                    CAMPEÓN DEL MUNDO
                </div>
                <div style='font-size:2.5em; font-weight:bold; color:#3a2a00;'>
                    {flag(champion)} {champion}
                </div>
                <div style='font-size:2em; margin-top:8px;'>🎉🎊🎉</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("↩ Rejugar la final"):
                del st.session_state[fk]; st.rerun()
