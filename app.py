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
    page_title="UBS Vila Nova — SMS São Paulo",
    page_icon="🏥",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Source Sans 3', Arial, sans-serif; }

/* ── FAIXA SUPERIOR PREFEITURA SP ── */
.topo-sp {
    background: #cc0000;
    color: #fff;
    padding: .35rem 1.5rem;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .04em;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* ── FUNDO GERAL ── */
.stApp { background: #f0f2f5 !important; }
[data-testid="stAppViewContainer"] > .main { background: #f0f2f5 !important; }
[data-testid="block-container"] { padding-top: 1.5rem !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #003d7a !important;
    border-right: 4px solid #cc0000 !important;
}
[data-testid="stSidebar"] * { color: #cce0f5 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size: 1rem !important;
    font-weight: 600 !important;
    padding: .4rem 0 !important;
}
[data-testid="stSidebar"] hr { border-color: #1a5c9a !important; }

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: #fff !important;
    border: 1.5px solid #b0bec5 !important;
    border-radius: 4px !important;
    color: #1a2733 !important;
    font-size: .97rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #003d7a !important;
    box-shadow: 0 0 0 3px rgba(0,61,122,.12) !important;
}

/* ── LABELS ── */
label,
.stTextInput label,
.stSelectbox label,
.stDateInput label,
.stTextArea label {
    color: #1a2733 !important;
    font-weight: 700 !important;
    font-size: .88rem !important;
    text-transform: uppercase !important;
    letter-spacing: .04em !important;
}

/* ── BOTÕES ── */
.stButton > button {
    background: #003d7a !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: .9rem 2rem !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
    box-shadow: 0 3px 10px rgba(0,61,122,.3) !important;
    transition: background .15s !important;
    width: 100% !important;
    border-bottom: 4px solid #cc0000 !important;
}
.stButton > button:hover {
    background: #002d5a !important;
    box-shadow: 0 5px 16px rgba(0,61,122,.45) !important;
}
.stButton > button:active { transform: translateY(1px) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #1a7a3d !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 700 !important;
    font-size: .97rem !important;
    padding: .8rem 1.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: .04em !important;
    border-bottom: 4px solid #0f5229 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover { background: #145e2f !important; }

/* ── MÉTRICAS ── */
[data-testid="metric-container"] {
    background: #fff !important;
    border: 1px solid #d0d7de !important;
    border-top: 4px solid #003d7a !important;
    border-radius: 4px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,.08) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #003d7a !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #546e7a !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    font-size: .78rem !important;
    letter-spacing: .06em !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: #fff !important;
    border: 1px solid #d0d7de !important;
    border-radius: 4px !important;
    padding: 2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.07) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 4px !important; border: 1px solid #d0d7de !important; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1.5px solid #b0bec5 !important;
    border-radius: 4px !important;
    color: #1a2733 !important;
}

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: .3rem .9rem;
    border-radius: 3px;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .06em;
    text-transform: uppercase;
}
.badge-aguardando { background: #fff3cd; color: #7d5a00; border-left: 3px solid #f0a500; }
.badge-confirmado { background: #d4edda; color: #155724; border-left: 3px solid #28a745; }
.badge-realizado  { background: #d1ecf1; color: #0c5460; border-left: 3px solid #17a2b8; }
.badge-cancelado  { background: #f8d7da; color: #721c24; border-left: 3px solid #dc3545; }

/* ── SECTION HEADER ── */
.section-header {
    background: #003d7a;
    color: #fff;
    border-radius: 4px;
    padding: 1.1rem 1.5rem;
    margin-bottom: 1.5rem;
    border-left: 6px solid #cc0000;
    box-shadow: 0 2px 8px rgba(0,0,0,.15);
}
.section-header h2 { margin: 0; font-size: 1.2rem; font-weight: 700; color: #fff; text-transform: uppercase; letter-spacing: .05em; }
.section-header p  { margin: .3rem 0 0; font-size: .88rem; color: #a8c8e8; }

/* ── AVISO INSTITUCIONAL ── */
.aviso {
    background: #fff8e1;
    border: 1px solid #f0c040;
    border-left: 5px solid #f0a500;
    border-radius: 4px;
    padding: .75rem 1.25rem;
    font-size: .88rem;
    color: #5a4000;
    margin-bottom: 1.25rem;
    font-weight: 600;
}

/* ── HEADINGS ── */
h1, h2, h3 { color: #003d7a !important; }
p { color: #37474f; }

/* ── DIVIDER ── */
hr { border-color: #d0d7de !important; }

/* ── ALERT ── */
[data-testid="stAlert"] { border-radius: 4px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f2f5; }
::-webkit-scrollbar-thumb { background: #90a4ae; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Faixa superior Prefeitura SP
st.markdown("""
<div class="topo-sp">
  <span>🏙️ PREFEITURA DE SÃO PAULO &nbsp;|&nbsp; SECRETARIA MUNICIPAL DE SAÚDE</span>
  <span>SMS-SP · Atenção Básica</span>
</div>
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
    <div style="text-align:center;padding:1.75rem 1rem 1.25rem;border-bottom:1px solid #1a5c9a">
      <div style="font-size:2.6rem">🏥</div>
      <div style="font-size:1.1rem;font-weight:700;color:#fff;letter-spacing:.03em;margin-top:.4rem">UBS VILA NOVA</div>
      <div style="font-size:.75rem;color:#7aaed4;margin-top:.15rem;text-transform:uppercase;letter-spacing:.06em">Unidade Básica de Saúde</div>
      <div style="font-size:.72rem;color:#5a8ab0;margin-top:.4rem">CRS Centro · SMS-SP</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    aba = st.radio("Menu", ["📋 Atendimento", "📅 Agendados", "⚙️ Gerenciar"])
    st.markdown("---")
    now = datetime.now()
    st.markdown(f"""
    <div style="font-size:.85rem;line-height:2.2;color:#7aaed4">
      📅 &nbsp;<span style="color:#fff;font-weight:700">{now.strftime('%d/%m/%Y')}</span><br>
      🕐 &nbsp;<span style="color:#fff;font-weight:700">{now.strftime('%H:%M')}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:.8rem;color:#4caf82;font-weight:700">● Sistema SIGA — Online</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.72rem;color:#5a8ab0;margin-top:.5rem">v2.1 · Atenção Básica SP</div>', unsafe_allow_html=True)


df = load_db()


# ════════════════════════════════════════
# ABA 1 — ATENDIMENTO
# ════════════════════════════════════════
if aba == "📋 Atendimento":
    st.markdown("""
    <div class="section-header">
      <h2>📋 Registro de Paciente</h2>
      <p>Preencha os dados do cidadão para iniciar o atendimento na unidade.</p>
    </div>
    <div class="aviso">
      ⚠️ &nbsp;Documento de identidade com foto obrigatório. Cartão SUS facilita o atendimento.
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
      <h2>📅 Agenda do Dia — UBS Vila Nova</h2>
      <p>Consulte e gerencie os atendimentos agendados na unidade.</p>
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
            html_rows += f"""<tr style="border-bottom:1px solid #e8edf2;transition:background .12s" onmouseover="this.style.background='#eef3fa'" onmouseout="this.style.background='transparent'">
              <td style="padding:.85rem 1rem;color:#003d7a;font-weight:700;font-size:.9rem">{row['ID']}</td>
              <td style="padding:.85rem 1rem;color:#1a2733;font-weight:600">{row['Nome']}</td>
              <td style="padding:.85rem 1rem;color:#546e7a;font-size:.85rem">{row['CPF']}</td>
              <td style="padding:.85rem 1rem;color:#1a2733;font-weight:700">{row['Hora']}</td>
              <td style="padding:.85rem 1rem;color:#37474f">{row['Especialidade']}</td>
              <td style="padding:.85rem 1rem;color:#37474f">{row['Convenio']}</td>
              <td style="padding:.85rem 1rem">{badge}</td>
            </tr>"""

        headers = ["ID", "Nome", "CPF", "Horário", "Especialidade", "Convênio", "Status"]
        header_html = "".join(
            f'<th style="text-align:left;padding:.8rem 1rem;font-size:.73rem;text-transform:uppercase;'
            f'letter-spacing:.07em;color:#546e7a;border-bottom:2px solid #003d7a;font-weight:700">{h}</th>'
            for h in headers
        )
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:4px;
                      overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.1);border:1px solid #d0d7de">
          <thead style="background:#f0f4f8"><tr>{header_html}</tr></thead>
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
      <p>Atualize o status do cidadão pelo número de protocolo.</p>
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
