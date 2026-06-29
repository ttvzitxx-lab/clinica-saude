import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import io

DB_FILE = "atendimentos.xlsx"
ADMIN_SENHA = "Vitaclinica"

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
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Source Sans 3', Arial, sans-serif; }

/* ── FUNDO ── */
.stApp { background: #f0f2f5 !important; }
[data-testid="stAppViewContainer"] > .main { background: #f0f2f5 !important; }
[data-testid="block-container"] { padding-top: 1.5rem !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #002d5c !important;
    border-right: 5px solid #1a6fbd !important;
    min-width: 270px !important;
}
[data-testid="stSidebar"] * { color: #cce0f5 !important; }
[data-testid="stSidebar"] hr { border-color: #1a4d80 !important; }

/* Menu items como botões */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: .55rem !important;
    flex-direction: column !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    background: rgba(255,255,255,.07) !important;
    border: 1.5px solid rgba(255,255,255,.12) !important;
    border-radius: 10px !important;
    padding: .9rem 1.2rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    cursor: pointer !important;
    transition: all .18s !important;
    color: #a8d0f0 !important;
    text-transform: none !important;
    letter-spacing: .01em !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.14) !important;
    border-color: rgba(255,255,255,.28) !important;
    color: #fff !important;
    transform: translateX(4px) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
    background: #1a6fbd !important;
    border-color: #1a6fbd !important;
    color: #fff !important;
    box-shadow: 0 4px 16px rgba(26,111,189,.5) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display:none !important; }
[data-testid="stSidebar"] .stRadio > label { display:none !important; }

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: #fff !important;
    border: 1.5px solid #b0bec5 !important;
    border-radius: 6px !important;
    color: #1a2733 !important;
    font-size: .97rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #1a6fbd !important;
    box-shadow: 0 0 0 3px rgba(26,111,189,.13) !important;
}

/* ── LABELS ── */
label,
.stTextInput label,
.stSelectbox label,
.stDateInput label,
.stTextArea label {
    color: #1a2733 !important;
    font-weight: 700 !important;
    font-size: .85rem !important;
    text-transform: uppercase !important;
    letter-spacing: .04em !important;
}

/* ── BOTÕES ── */
.stButton > button {
    background: #1a6fbd !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
    font-size: 1.1rem !important;
    padding: 1rem 2rem !important;
    letter-spacing: .05em !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(26,111,189,.35), inset 0 1px 0 rgba(255,255,255,.15) !important;
    transition: all .18s !important;
    width: 100% !important;
    border-bottom: 4px solid #0d4f8c !important;
}
.stButton > button:hover {
    background: #155da0 !important;
    box-shadow: 0 8px 26px rgba(26,111,189,.5), inset 0 1px 0 rgba(255,255,255,.15) !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
    border-bottom-width: 2px !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #1a7a3d !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: .85rem 1.5rem !important;
    text-transform: uppercase !important;
    letter-spacing: .04em !important;
    border-bottom: 4px solid #0f5229 !important;
    width: 100% !important;
    box-shadow: 0 3px 12px rgba(26,122,61,.3) !important;
}
.stDownloadButton > button:hover {
    background: #145e2f !important;
    transform: translateY(-1px) !important;
}

/* ── MÉTRICAS ── */
[data-testid="metric-container"] {
    background: #fff !important;
    border: 1px solid #d0d7de !important;
    border-top: 4px solid #1a6fbd !important;
    border-radius: 8px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.08) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1a6fbd !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    color: #546e7a !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    font-size: .75rem !important;
    letter-spacing: .07em !important;
}

/* ── FORM ── */
[data-testid="stForm"] {
    background: #fff !important;
    border: 1px solid #d0d7de !important;
    border-radius: 8px !important;
    padding: 2rem !important;
    box-shadow: 0 2px 14px rgba(0,0,0,.07) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border-radius: 8px !important; border: 1px solid #d0d7de !important; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #fff !important;
    border: 1.5px solid #b0bec5 !important;
    border-radius: 6px !important;
    color: #1a2733 !important;
}

/* ── BADGES ── */
.badge {
    display: inline-block;
    padding: .3rem .9rem;
    border-radius: 4px;
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
    background: #1a6fbd;
    color: #fff;
    border-radius: 8px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 3px 14px rgba(26,111,189,.3);
}
.section-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #fff; letter-spacing: .03em; }
.section-header p  { margin: .3rem 0 0; font-size: .88rem; color: #c2dff7; }

/* ── ADMIN HEADER ── */
.admin-header {
    background: linear-gradient(135deg, #1a2d4a 0%, #0d1f36 100%);
    border-left: 6px solid #f0a500;
    color: #fff;
    border-radius: 8px;
    padding: 1.25rem 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 3px 14px rgba(0,0,0,.2);
}
.admin-header h2 { margin: 0; font-size: 1.25rem; font-weight: 800; color: #fff; }
.admin-header p  { margin: .3rem 0 0; font-size: .88rem; color: #a0b8d0; }

/* ── HEADINGS ── */
h1, h2, h3 { color: #1a2d4a !important; }
p { color: #37474f; }

/* ── DIVIDER ── */
hr { border-color: #d0d7de !important; }

/* ── ALERT ── */
[data-testid="stAlert"] { border-radius: 8px !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f0f2f5; }
::-webkit-scrollbar-thumb { background: #90a4ae; border-radius: 3px; }
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
    last = df["ID"].str.replace("#", "", regex=False).astype(int).max()
    return f"#{last + 1:04d}"


def status_badge(s: str) -> str:
    return f'<span class="badge badge-{s}">{s.capitalize()}</span>'


# ── SIDEBAR ──
with st.sidebar:
    now = datetime.now()
    dia_semana = now.strftime('%A') \
        .replace('Monday','Segunda').replace('Tuesday','Terça') \
        .replace('Wednesday','Quarta').replace('Thursday','Quinta') \
        .replace('Friday','Sexta').replace('Saturday','Sábado').replace('Sunday','Domingo')

    st.markdown(f"""
    <div style="background:rgba(0,0,0,.28);margin:-1rem -1rem 1.5rem -1rem;padding:1.75rem 1.5rem 1.5rem;border-bottom:1px solid rgba(255,255,255,.08)">
      <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:1.1rem">
        <div style="background:#1a6fbd;border-radius:12px;width:46px;height:46px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;flex-shrink:0;box-shadow:0 3px 12px rgba(26,111,189,.4)">🩺</div>
        <div>
          <div style="font-size:1.1rem;font-weight:800;color:#fff;line-height:1.2;letter-spacing:.02em">ClinícaVita</div>
          <div style="font-size:.7rem;color:#7aaed4;text-transform:uppercase;letter-spacing:.07em;margin-top:.1rem">Sistema de Atendimento</div>
        </div>
      </div>
      <div style="background:rgba(255,255,255,.07);border-radius:8px;padding:.7rem 1rem;display:flex;justify-content:space-between;align-items:center">
        <div>
          <div style="font-size:.65rem;color:#7aaed4;text-transform:uppercase;letter-spacing:.07em">{dia_semana}</div>
          <div style="font-size:.95rem;color:#fff;font-weight:700;margin-top:.05rem">{now.strftime('%d/%m/%Y')}</div>
        </div>
        <div style="text-align:right">
          <div style="font-size:.65rem;color:#7aaed4;text-transform:uppercase;letter-spacing:.07em">Horário</div>
          <div style="font-size:.95rem;color:#fff;font-weight:700;margin-top:.05rem">{now.strftime('%H:%M')}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#5a8ab0;font-weight:700;margin-bottom:.6rem;padding-left:.2rem">Menu</div>', unsafe_allow_html=True)

    aba = st.radio(
        "Menu",
        ["📋 Atendimento", "📅 Agendados", "⚙️ Gerenciar", "🔐 Administrador"],
        label_visibility="collapsed",
    )

    st.markdown(f"""
    <div style="margin-top:1.5rem;padding:.85rem 1rem;background:rgba(255,255,255,.05);border-radius:8px;border:1px solid rgba(255,255,255,.08)">
      <div style="display:flex;align-items:center;gap:.45rem;margin-bottom:.45rem">
        <span style="width:7px;height:7px;background:#4caf82;border-radius:50%;display:inline-block;flex-shrink:0"></span>
        <span style="font-size:.78rem;color:#4caf82;font-weight:700">Sistema online</span>
      </div>
      <div style="font-size:.7rem;color:#5a8ab0;line-height:1.7">
        Atendimento · v2.2
      </div>
    </div>
    """, unsafe_allow_html=True)


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
                "ID":            next_id(df),
                "Nome":          nome.strip(),
                "CPF":           cpf.strip(),
                "RG":            rg.strip(),
                "Nascimento":    nascimento.strftime("%d/%m/%Y") if nascimento else "",
                "Sexo":          sexo,
                "Telefone":      telefone.strip(),
                "Email":         email.strip(),
                "Especialidade": especialidade,
                "Convenio":      convenio,
                "Queixa":        queixa.strip(),
                "Data":          date.today().strftime("%d/%m/%Y"),
                "Hora":          datetime.now().strftime("%H:%M"),
                "Status":        "aguardando",
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
      <p>Consulte e gerencie os atendimentos agendados para hoje.</p>
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
            html_rows += f"""<tr style="border-bottom:1px solid #e8edf2;transition:background .12s" onmouseover="this.style.background='#eef4fb'" onmouseout="this.style.background='transparent'">
              <td style="padding:.85rem 1rem;color:#1a6fbd;font-weight:700;font-size:.9rem">{row['ID']}</td>
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
            f'letter-spacing:.07em;color:#546e7a;border-bottom:2px solid #1a6fbd;font-weight:700">{h}</th>'
            for h in headers
        )
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;
                      overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.1);border:1px solid #d0d7de">
          <thead style="background:#f0f4f8"><tr>{header_html}</tr></thead>
          <tbody>{html_rows}</tbody>
        </table><br>
        """, unsafe_allow_html=True)

    if not df.empty:
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
      <p>Atualize o status de um paciente pelo número de protocolo.</p>
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


# ════════════════════════════════════════
# ABA 4 — ADMINISTRADOR
# ════════════════════════════════════════
elif aba == "🔐 Administrador":
    st.markdown("""
    <div class="admin-header">
      <h2>🔐 Painel Administrativo</h2>
      <p>Acesso restrito — visualize, edite e exporte todos os dados de pacientes.</p>
    </div>
    """, unsafe_allow_html=True)

    if "admin_logado" not in st.session_state:
        st.session_state.admin_logado = False

    if not st.session_state.admin_logado:
        st.markdown("""
        <div style="max-width:400px;margin:2rem auto;background:#fff;border:1px solid #d0d7de;
                    border-radius:12px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.1)">
          <div style="text-align:center;margin-bottom:1.5rem">
            <div style="font-size:2.5rem">🔒</div>
            <div style="font-size:1.1rem;font-weight:700;color:#1a2d4a;margin-top:.5rem">Acesso Restrito</div>
            <div style="font-size:.85rem;color:#546e7a;margin-top:.25rem">Digite a senha de administrador</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_c, col_m, col_d = st.columns([1, 2, 1])
        with col_m:
            senha = st.text_input("Senha de administrador", type="password", label_visibility="collapsed",
                                  placeholder="Digite a senha...")
            if st.button("🔓 Entrar"):
                if senha == ADMIN_SENHA:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        # ── PAINEL ADMIN ──
        col_sair, _ = st.columns([1, 5])
        with col_sair:
            if st.button("🚪 Sair"):
                st.session_state.admin_logado = False
                st.rerun()

        st.markdown("---")

        # Métricas globais
        total_g   = len(df)
        agua_g    = len(df[df["Status"] == "aguardando"])  if not df.empty else 0
        conf_g    = len(df[df["Status"] == "confirmado"])  if not df.empty else 0
        realiz_g  = len(df[df["Status"] == "realizado"])   if not df.empty else 0
        cancel_g  = len(df[df["Status"] == "cancelado"])   if not df.empty else 0
        hoje_g    = len(df[df["Data"] == date.today().strftime("%d/%m/%Y")]) if not df.empty else 0

        st.markdown("#### 📊 Visão Geral — Todos os Registros")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Total",       total_g)
        m2.metric("Hoje",        hoje_g)
        m3.metric("Aguardando",  agua_g)
        m4.metric("Confirmados", conf_g)
        m5.metric("Realizados",  realiz_g)
        m6.metric("Cancelados",  cancel_g)

        st.markdown("---")

        if df.empty:
            st.info("Nenhum paciente registrado ainda.")
        else:
            # ── FILTROS ──
            st.markdown("#### 🔍 Filtros e Busca")
            fa, fb, fc, fd = st.columns([3, 1, 1, 1])
            busca_adm  = fa.text_input("Buscar por nome, CPF ou RG", placeholder="Digite para filtrar...")
            fil_status = fb.selectbox("Status", ["Todos"] + STATUS_OPTS)
            fil_espec  = fc.selectbox("Especialidade", ["Todas"] + ESPECIALIDADES)
            fil_data   = fd.text_input("Data (dd/mm/aaaa)", placeholder="dd/mm/aaaa")

            exibir = df.copy()
            if busca_adm:
                exibir = exibir[
                    exibir["Nome"].str.contains(busca_adm, case=False, na=False) |
                    exibir["CPF"].str.contains(busca_adm, na=False) |
                    exibir["RG"].str.contains(busca_adm, na=False)
                ]
            if fil_status != "Todos":
                exibir = exibir[exibir["Status"] == fil_status]
            if fil_espec != "Todas":
                exibir = exibir[exibir["Especialidade"] == fil_espec]
            if fil_data.strip():
                exibir = exibir[exibir["Data"] == fil_data.strip()]

            st.markdown(f"**{len(exibir)} registro(s) encontrado(s)**")
            st.markdown("---")

            # ── TABELA COMPLETA ──
            st.markdown("#### 📋 Todos os Pacientes")
            cols_adm = ["ID", "Nome", "CPF", "RG", "Nascimento", "Sexo", "Telefone",
                        "Email", "Especialidade", "Convenio", "Data", "Hora", "Status"]
            html_rows = ""
            for _, row in exibir[cols_adm].iterrows():
                badge = status_badge(str(row["Status"]))
                html_rows += f"""<tr style="border-bottom:1px solid #e8edf2;transition:background .12s"
                    onmouseover="this.style.background='#eef4fb'" onmouseout="this.style.background='transparent'">
                  <td style="padding:.75rem .9rem;color:#1a6fbd;font-weight:700;font-size:.85rem;white-space:nowrap">{row['ID']}</td>
                  <td style="padding:.75rem .9rem;color:#1a2733;font-weight:600;white-space:nowrap">{row['Nome']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem">{row['CPF']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem">{row['RG']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem">{row['Nascimento']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem">{row['Sexo']}</td>
                  <td style="padding:.75rem .9rem;color:#37474f;font-size:.82rem;white-space:nowrap">{row['Telefone']}</td>
                  <td style="padding:.75rem .9rem;color:#37474f;font-size:.82rem">{row['Email']}</td>
                  <td style="padding:.75rem .9rem;color:#37474f">{row['Especialidade']}</td>
                  <td style="padding:.75rem .9rem;color:#37474f">{row['Convenio']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem;white-space:nowrap">{row['Data']}</td>
                  <td style="padding:.75rem .9rem;color:#546e7a;font-size:.82rem">{row['Hora']}</td>
                  <td style="padding:.75rem .9rem">{badge}</td>
                </tr>"""

            headers_adm = ["ID", "Nome", "CPF", "RG", "Nascimento", "Sexo",
                           "Telefone", "E-mail", "Especialidade", "Convênio", "Data", "Hora", "Status"]
            header_html = "".join(
                f'<th style="text-align:left;padding:.75rem .9rem;font-size:.7rem;text-transform:uppercase;'
                f'letter-spacing:.07em;color:#546e7a;border-bottom:2px solid #1a6fbd;font-weight:700;white-space:nowrap">{h}</th>'
                for h in headers_adm
            )
            st.markdown(f"""
            <div style="overflow-x:auto">
            <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:8px;
                          overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.1);border:1px solid #d0d7de;min-width:1100px">
              <thead style="background:#f0f4f8"><tr>{header_html}</tr></thead>
              <tbody>{html_rows}</tbody>
            </table>
            </div><br>
            """, unsafe_allow_html=True)

            # ── EDIÇÃO DE STATUS ──
            st.markdown("---")
            st.markdown("#### ✏️ Editar Registro")
            ea, eb, ec = st.columns([2, 1, 1])
            proto_edit  = ea.selectbox("Protocolo", df["ID"].tolist(), key="proto_edit")
            stat_edit   = eb.selectbox("Novo status", STATUS_OPTS, key="stat_edit")
            esp_edit    = ec.selectbox("Nova especialidade", ESPECIALIDADES, key="esp_edit")

            row_edit = df[df["ID"] == proto_edit].iloc[0]
            st.markdown(
                f"**Paciente:** {row_edit['Nome']} &nbsp;·&nbsp; "
                f"**CPF:** {row_edit['CPF']} &nbsp;·&nbsp; "
                f"**Telefone:** {row_edit['Telefone']} &nbsp;·&nbsp; "
                f"**Status atual:** {status_badge(str(row_edit['Status']))}",
                unsafe_allow_html=True,
            )

            if st.button("💾 Salvar alterações"):
                df.loc[df["ID"] == proto_edit, "Status"]        = stat_edit
                df.loc[df["ID"] == proto_edit, "Especialidade"] = esp_edit
                save_db(df)
                st.success(f"Registro **{proto_edit}** atualizado.")
                st.rerun()

            # ── EXCLUIR ──
            st.markdown("---")
            st.markdown("#### 🗑️ Excluir Registro")
            col_del, col_conf = st.columns([2, 1])
            proto_del = col_del.selectbox("Protocolo a excluir", df["ID"].tolist(), key="proto_del")
            confirmar = col_conf.checkbox("Confirmar exclusão")

            if st.button("🗑️ Excluir paciente"):
                if confirmar:
                    df = df[df["ID"] != proto_del].reset_index(drop=True)
                    save_db(df)
                    st.success(f"Registro **{proto_del}** excluído com sucesso.")
                    st.rerun()
                else:
                    st.warning("Marque a caixa de confirmação antes de excluir.")

            # ── EXPORTAÇÃO ──
            st.markdown("---")
            st.markdown("#### ⬇️ Exportar Dados")
            ex1, ex2 = st.columns(2)
            with ex1:
                buf = io.BytesIO()
                df.to_excel(buf, index=False)
                st.download_button(
                    "📥 Exportar todos (.xlsx)",
                    buf.getvalue(),
                    file_name=f"pacientes_{date.today().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            with ex2:
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📄 Exportar todos (.csv)",
                    csv,
                    file_name=f"pacientes_{date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )
