import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import re

DB_FILE = "atendimentos.xlsx"
ESPECIALIDADES = [
    "Clínica Geral", "Cardiologia", "Dermatologia",
    "Ginecologia", "Ortopedia", "Pediatria", "Psiquiatria", "Neurologia",
]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Amil", "Porto Seguro", "Outro"]
STATUS_OPTS = ["aguardando", "confirmado", "realizado", "cancelado"]

st.set_page_config(
    page_title="ClinícaVita — Atendimento",
    page_icon="🩺",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* ── FUNDO GERAL ── */
.stApp { background: linear-gradient(160deg, #0f1e1a 0%, #152920 50%, #0f1e1a 100%) !important; }
[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="block-container"] { padding-top: 2rem !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1510 0%, #152920 100%) !important;
    border-right: 1px solid #2a5c4a !important;
}
[data-testid="stSidebar"] * { color: #a8dcc8 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 1rem !important; font-weight: 600 !important; }

/* ── INPUTS ── */
input, textarea, select,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
.stSelectbox select {
    background: #0f1e1a !important;
    border: 1.5px solid #2a5c4a !important;
    border-radius: 10px !important;
    color: #e0f5ee !important;
    font-size: 1rem !important;
}
input:focus, textarea:focus { border-color: #3dcc9e !important; box-shadow: 0 0 0 3px rgba(61,204,158,.15) !important; }

/* ── LABELS ── */
label, .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label {
    color: #7ecfb0 !important;
    font-weight: 600 !important;
    font-size: .92rem !important;
}

/* ── BOTÕES ── */
.stButton > button {
    background: linear-gradient(135deg, #3dcc9e 0%, #2a9970 100%) !important;
    color: #0a1510 !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    padding: 1rem 2.5rem !important;
    letter-spacing: .03em !important;
    box-shadow: 0 6px 28px rgba(61,204,158,.35) !important;
    transition: all .2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #50e0b0 0%, #3dcc9e 100%) !important;
    box-shadow: 0 10px 40px rgba(61,204,158,.55) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #c8a96e 0%, #a07840 100%) !important;
    color: #0a1510 !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    padding: .85rem 2rem !important;
    box-shadow: 0 6px 24px rgba(200,169,110,.35) !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    box-shadow: 0 10px 36px rgba(200,169,110,.55) !important;
    transform: translateY(-2px) !important;
}

/* ── MÉTRICAS ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #152920 0%, #0f1e1a 100%) !important;
    border: 1px solid #2a5c4a !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,.4) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #3dcc9e !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #7ecfb0 !important;
    font-weight: 600 !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: rgba(21,41,32,.7) !important;
    border: 1px solid #2a5c4a !important;
    border-radius: 20px !important;
    padding: 2rem !important;
    box-shadow: 0 8px 40px rgba(0,0,0,.4) !important;
    backdrop-filter: blur(10px) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 16px !important; overflow: hidden !important; }

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: .35rem 1rem;
    border-radius: 20px;
    font-size: .82rem;
    font-weight: 700;
    letter-spacing: .04em;
}
.badge-aguardando { background: rgba(200,169,110,.2); color: #f0c070; border: 1px solid rgba(200,169,110,.4); }
.badge-confirmado { background: rgba(61,204,158,.15); color: #3dcc9e; border: 1px solid rgba(61,204,158,.35); }
.badge-realizado  { background: rgba(100,140,255,.15); color: #8ab4ff; border: 1px solid rgba(100,140,255,.3); }
.badge-cancelado  { background: rgba(255,80,80,.15);  color: #ff7070; border: 1px solid rgba(255,80,80,.3);  }

/* ── SECTION HEADER ── */
.section-header {
    background: linear-gradient(135deg, #1a4d3a 0%, #0f2d20 100%);
    border: 1px solid #2a5c4a;
    border-left: 5px solid #3dcc9e;
    color: #e0f5ee;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.75rem;
    box-shadow: 0 4px 24px rgba(0,0,0,.35);
}
.section-header h2 { margin: 0; font-size: 1.5rem; font-weight: 800; color: #fff; }
.section-header p  { margin: .3rem 0 0; font-size: .9rem; color: #7ecfb0; }

/* ── SEARCH INPUT ── */
.stTextInput input { color: #e0f5ee !important; }

/* ── HEADINGS ── */
h1, h2, h3 { color: #e0f5ee !important; }
p, li, span { color: #a8dcc8; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #0f1e1a !important;
    border: 1.5px solid #2a5c4a !important;
    border-radius: 10px !important;
    color: #e0f5ee !important;
}

/* ── DATE INPUT ── */
[data-testid="stDateInput"] input { color: #e0f5ee !important; }

/* ── SUCCESS / ERROR / INFO ── */
[data-testid="stAlert"] { border-radius: 12px !important; }

/* ── DIVIDER ── */
hr { border-color: #2a5c4a !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1e1a; }
::-webkit-scrollbar-thumb { background: #2a5c4a; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── BANCO DE DADOS ──
def load_db() -> pd.DataFrame:
    cols = ["ID", "Nome", "CPF", "RG", "Nascimento", "Sexo",
            "Telefone", "Email", "Especialidade", "Convenio",
            "Queixa", "Data", "Hora", "Status"]
    if os.path.exists(DB_FILE):
        df = pd.read_excel(DB_FILE)
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        return df[cols]
    return pd.DataFrame(columns=cols)


def save_db(df: pd.DataFrame):
    df.to_excel(DB_FILE, index=False)


def next_id(df: pd.DataFrame) -> str:
    if df.empty:
        return "#0001"
    last = df["ID"].str.replace("#", "").astype(int).max()
    return f"#{last + 1:04d}"


def status_badge(s: str) -> str:
    return f'<span class="badge badge-{s}">{s.capitalize()}</span>'


# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem">
      <div style="font-size:3rem">🩺</div>
      <div style="font-size:1.5rem;font-weight:800;color:#3dcc9e;letter-spacing:.04em">ClinícaVita</div>
      <div style="font-size:.78rem;color:#5aaa88;margin-top:.2rem">Central de Atendimento</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    aba = st.radio("Navegação", ["📋 Atendimento", "📅 Agendados", "⚙️ Gerenciar"])
    st.markdown("---")
    now = datetime.now()
    st.markdown(f"""
    <div style="font-size:.85rem;line-height:2">
      📅 &nbsp;<strong>{now.strftime('%d/%m/%Y')}</strong><br>
      🕐 &nbsp;<strong>{now.strftime('%H:%M')}</strong>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:.82rem;color:#3dcc9e;font-weight:700">● Sistema online</div>', unsafe_allow_html=True)


df = load_db()


# ════════════════════════════════════════
# ABA 1 — ATENDIMENTO
# ════════════════════════════════════════
if aba == "📋 Atendimento":
    st.markdown("""
    <div class="section-header">
      <h2>📋 Registro de Paciente</h2>
      <p>Preencha os dados do paciente para iniciar o atendimento.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_atendimento", clear_on_submit=True):
        st.markdown("**Identificação**")
        c1, c2 = st.columns(2)
        nome       = c1.text_input("Nome completo *")
        nascimento = c2.date_input("Data de nascimento *", value=None, min_value=date(1900, 1, 1))

        c3, c4, c5 = st.columns(3)
        cpf  = c3.text_input("CPF *",  placeholder="000.000.000-00", max_chars=14)
        rg   = c4.text_input("RG *",   placeholder="00.000.000-0",   max_chars=12)
        sexo = c5.selectbox("Sexo", ["", "Masculino", "Feminino", "Outro / Prefiro não informar"])

        st.markdown("---")
        st.markdown("**Contato**")
        c6, c7 = st.columns(2)
        telefone = c6.text_input("Telefone / WhatsApp *", placeholder="(00) 00000-0000", max_chars=15)
        email    = c7.text_input("E-mail", placeholder="exemplo@email.com")

        st.markdown("---")
        st.markdown("**Atendimento**")
        c8, c9 = st.columns(2)
        especialidade = c8.selectbox("Especialidade *", [""] + ESPECIALIDADES)
        convenio      = c9.selectbox("Convênio", CONVENIOS)

        queixa = st.text_area("Queixa principal / Observações", height=100,
                              placeholder="Descreva brevemente o motivo da consulta...")

        submitted = st.form_submit_button("✅ Registrar Atendimento", use_container_width=True)

    if submitted:
        erros = []
        if not nome.strip():     erros.append("Nome completo")
        if not cpf.strip():      erros.append("CPF")
        if not rg.strip():       erros.append("RG")
        if not telefone.strip(): erros.append("Telefone")
        if not especialidade:    erros.append("Especialidade")
        if nascimento is None:   erros.append("Data de nascimento")

        if erros:
            st.error(f"Campos obrigatórios faltando: {', '.join(erros)}")
        else:
            novo = {
                "ID":           next_id(df),
                "Nome":         nome.strip(),
                "CPF":          cpf.strip(),
                "RG":           rg.strip(),
                "Nascimento":   nascimento.strftime("%d/%m/%Y") if nascimento else "",
                "Sexo":         sexo,
                "Telefone":     telefone.strip(),
                "Email":        email.strip(),
                "Especialidade": especialidade,
                "Convenio":     convenio,
                "Queixa":       queixa.strip(),
                "Data":         date.today().strftime("%d/%m/%Y"),
                "Hora":         datetime.now().strftime("%H:%M"),
                "Status":       "aguardando",
            }
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            save_db(df)
            st.success(f"✅ Paciente **{nome}** registrado! Protocolo: **{novo['ID']}**")
            st.balloons()


# ════════════════════════════════════════
# ABA 2 — AGENDADOS
# ════════════════════════════════════════
elif aba == "📅 Agendados":
    st.markdown("""
    <div class="section-header">
      <h2>📅 Agenda do Dia</h2>
      <p>Consulte e gerencie os atendimentos do dia.</p>
    </div>
    """, unsafe_allow_html=True)

    hoje = date.today().strftime("%d/%m/%Y")
    df_hoje = df[df["Data"] == hoje].copy() if not df.empty else pd.DataFrame(columns=df.columns)

    total  = len(df_hoje)
    conf   = len(df_hoje[df_hoje["Status"].isin(["confirmado", "realizado"])]) if total else 0
    agua   = len(df_hoje[df_hoje["Status"] == "aguardando"]) if total else 0
    realiz = len(df_hoje[df_hoje["Status"] == "realizado"]) if total else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total hoje",  total)
    m2.metric("Confirmados", conf)
    m3.metric("Aguardando",  agua)
    m4.metric("Realizados",  realiz)

    st.markdown("---")

    c_busca, c_status = st.columns([3, 1])
    busca     = c_busca.text_input("🔍 Buscar por nome ou CPF")
    filtro_st = c_status.selectbox("Status", ["Todos"] + STATUS_OPTS)

    exibir = df_hoje.copy()
    if busca:
        exibir = exibir[
            exibir["Nome"].str.contains(busca, case=False, na=False) |
            exibir["CPF"].str.contains(busca, na=False)
        ]
    if filtro_st != "Todos":
        exibir = exibir[exibir["Status"] == filtro_st]

    st.markdown(f"**{len(exibir)} agendamento(s) encontrado(s)**")

    if exibir.empty:
        st.info("Nenhum agendamento encontrado para hoje.")
    else:
        cols_show = ["ID", "Nome", "CPF", "Hora", "Especialidade", "Convenio", "Status"]
        html_rows = ""
        for _, row in exibir[cols_show].iterrows():
            badge = status_badge(str(row["Status"]))
            html_rows += f"""<tr style="border-bottom:1px solid #1e4535;transition:background .15s" onmouseover="this.style.background='rgba(61,204,158,.07)'" onmouseout="this.style.background='transparent'">
              <td style="padding:.9rem 1.1rem;color:#3dcc9e;font-weight:700">{row['ID']}</td>
              <td style="padding:.9rem 1.1rem;color:#e0f5ee;font-weight:600">{row['Nome']}</td>
              <td style="padding:.9rem 1.1rem;color:#5aaa88;font-size:.85rem">{row['CPF']}</td>
              <td style="padding:.9rem 1.1rem;color:#e0f5ee;font-weight:700">{row['Hora']}</td>
              <td style="padding:.9rem 1.1rem;color:#a8dcc8">{row['Especialidade']}</td>
              <td style="padding:.9rem 1.1rem;color:#a8dcc8">{row['Convenio']}</td>
              <td style="padding:.9rem 1.1rem">{badge}</td>
            </tr>"""

        headers = ["ID", "Nome", "CPF", "Horário", "Especialidade", "Convênio", "Status"]
        header_html = "".join(
            f'<th style="text-align:left;padding:.85rem 1.1rem;font-size:.75rem;text-transform:uppercase;'
            f'letter-spacing:.08em;color:#5aaa88;border-bottom:1px solid #1e4535;font-weight:700">{h}</th>'
            for h in headers
        )
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:rgba(15,30,26,.85);border-radius:16px;
                      overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.5);border:1px solid #1e4535">
          <thead style="background:rgba(21,41,32,.9)"><tr>{header_html}</tr></thead>
          <tbody>{html_rows}</tbody>
        </table><br>
        """, unsafe_allow_html=True)

    if not df.empty:
        xlsx_bytes = df.to_excel.__func__  # dummy reference to force import
        import io
        buf = io.BytesIO()
        df.to_excel(buf, index=False)
        st.download_button(
            "⬇️ Exportar todos os registros (.xlsx)",
            buf.getvalue(),
            file_name="atendimentos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# ════════════════════════════════════════
# ABA 3 — GERENCIAR
# ════════════════════════════════════════
elif aba == "⚙️ Gerenciar":
    st.markdown("""
    <div class="section-header">
      <h2>⚙️ Gerenciar Atendimentos</h2>
      <p>Atualize o status de um paciente pelo protocolo.</p>
    </div>
    """, unsafe_allow_html=True)

    if df.empty:
        st.info("Nenhum atendimento registrado ainda.")
    else:
        ids = df["ID"].tolist()
        col_a, col_b = st.columns(2)
        protocolo   = col_a.selectbox("Protocolo", ids)
        novo_status = col_b.selectbox("Novo status", STATUS_OPTS)

        row = df[df["ID"] == protocolo].iloc[0]
        st.markdown(
            f"**Paciente:** {row['Nome']} &nbsp;|&nbsp; "
            f"**CPF:** {row['CPF']} &nbsp;|&nbsp; "
            f"**Especialidade:** {row['Especialidade']} &nbsp;|&nbsp; "
            f"**Status atual:** {status_badge(str(row['Status']))}",
            unsafe_allow_html=True,
        )

        if st.button("Atualizar status"):
            df.loc[df["ID"] == protocolo, "Status"] = novo_status
            save_db(df)
            st.success(f"Status de **{protocolo}** atualizado para **{novo_status}**.")
            st.rerun()

        st.markdown("---")
        st.markdown("**Todos os registros**")
        st.dataframe(df, use_container_width=True, hide_index=True)
