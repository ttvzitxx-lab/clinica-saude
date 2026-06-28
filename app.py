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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] { background: #1e2d28 !important; }
[data-testid="stSidebar"] * { color: #d4e8e1 !important; }

[data-testid="metric-container"] {
    background: #fff;
    border: 1px solid #dde3e0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
}

.stButton > button {
    background: #3d7f6e !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: .55rem 1.6rem !important;
}
.stButton > button:hover { background: #2e6358 !important; }

.badge {
    display:inline-block;
    padding:.25rem .75rem;
    border-radius:20px;
    font-size:.78rem;
    font-weight:700;
}
.badge-aguardando { background:#fdf3e1; color:#9c6f1c; }
.badge-confirmado { background:#e8f5ec; color:#2e7d55; }
.badge-realizado  { background:#edf2ff; color:#3956c5; }
.badge-cancelado  { background:#fdecea; color:#c0392b; }

.section-header {
    background: linear-gradient(135deg, #3d7f6e 0%, #2e6358 100%);
    color: #fff;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1.5rem;
}
.section-header h2 { margin:0; font-size:1.3rem; }
.section-header p  { margin:.25rem 0 0; font-size:.88rem; opacity:.8; }
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
    st.markdown("## 🩺 ClinícaVita")
    st.markdown("---")
    aba = st.radio("Navegação", ["📋 Atendimento", "📅 Agendados", "⚙️ Gerenciar"])
    st.markdown("---")
    now = datetime.now()
    st.markdown(f"**Data:** {now.strftime('%d/%m/%Y')}")
    st.markdown(f"**Hora:** {now.strftime('%H:%M')}")
    st.markdown("---")
    st.markdown("<small>Sistema online ✅</small>", unsafe_allow_html=True)


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
            html_rows += f"""<tr style="border-bottom:1px solid #dde3e0">
              <td style="padding:.85rem 1rem">{row['ID']}</td>
              <td style="padding:.85rem 1rem"><strong>{row['Nome']}</strong></td>
              <td style="padding:.85rem 1rem;color:#6b8278;font-size:.85rem">{row['CPF']}</td>
              <td style="padding:.85rem 1rem"><strong>{row['Hora']}</strong></td>
              <td style="padding:.85rem 1rem">{row['Especialidade']}</td>
              <td style="padding:.85rem 1rem">{row['Convenio']}</td>
              <td style="padding:.85rem 1rem">{badge}</td>
            </tr>"""

        headers = ["ID", "Nome", "CPF", "Horário", "Especialidade", "Convênio", "Status"]
        header_html = "".join(
            f'<th style="text-align:left;padding:.75rem 1rem;font-size:.78rem;text-transform:uppercase;'
            f'letter-spacing:.05em;color:#6b8278;border-bottom:1px solid #dde3e0">{h}</th>'
            for h in headers
        )
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:#fff;border-radius:12px;
                      overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.07)">
          <thead style="background:#f4f6f5"><tr>{header_html}</tr></thead>
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
