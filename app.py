import streamlit as st
import pandas as pd
import os
import re
import io
from datetime import datetime, date

st.set_page_config(
    page_title="Telemedicina",
    page_icon="✚",
    layout="centered",
)

DATA_FILE = "agendamentos.xlsx"
ADMIN_PASSWORD = "clinica2024"
COLUNAS = ["ID", "Nome", "CPF", "Telefone", "Email", "Data", "Horario", "Tipo", "Observacoes", "Recebido_em", "Status"]

def formatar_cpf(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def validar_cpf(cpf):
    return len(re.sub(r'\D', '', cpf)) == 11

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_excel(DATA_FILE)
    return pd.DataFrame(columns=COLUNAS)

def salvar_agendamento(dados):
    df = carregar_dados()
    novo_id = len(df) + 1
    dados["ID"] = novo_id
    dados["Recebido_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados["Status"] = "Aguardando confirmação"
    df = pd.concat([df, pd.DataFrame([dados])], ignore_index=True)
    df.to_excel(DATA_FILE, index=False)
    return novo_id

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

section[data-testid="stSidebar"] { background: #111 !important; }
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] button {
    background: #1c1c1c !important;
    border: 1px solid #2e2e2e !important;
    color: #ccc !important;
    border-radius: 6px !important;
    font-size: 0.83rem !important;
    margin-bottom: 4px !important;
}
section[data-testid="stSidebar"] button:hover {
    border-color: #f0c040 !important;
    color: #f0c040 !important;
    background: #1a1a1a !important;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 0 1rem;
    border-bottom: 2px solid #111;
    margin-bottom: 2rem;
}
.header-left { display: flex; align-items: center; gap: 12px; }
.cross-badge {
    width: 40px; height: 40px;
    background: #111;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; color: #f0c040;
    font-weight: 700; flex-shrink: 0;
}
.brand-name { font-size: 1.2rem; font-weight: 700; color: #111; }
.brand-tagline { font-size: 0.72rem; color: #888; margin-top: 1px; }
.online-badge {
    background: #f0c040;
    color: #111;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 4px;
    letter-spacing: 0.05em;
}

.hero {
    background: #111;
    border-radius: 10px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
}
.hero h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.25;
    margin-bottom: 0.6rem;
    letter-spacing: -0.03em;
}
.hero h1 span { color: #f0c040; }
.hero p { font-size: 0.88rem; color: #aaa; line-height: 1.7; margin-bottom: 1.25rem; }
.hero-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.pill {
    background: #1e1e1e;
    border: 1px solid #333;
    color: #ccc;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 20px;
}
.pill.yellow { background: #f0c040; color: #111; border-color: #f0c040; font-weight: 600; }

.section-title {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #eee;
}

.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 2rem;
}
.card {
    background: #fff;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 1.25rem 1rem;
}
.card .ic { font-size: 1.6rem; margin-bottom: 0.6rem; display: block; }
.card h4 { font-size: 0.83rem; font-weight: 600; color: #111; margin-bottom: 0.3rem; }
.card p { font-size: 0.76rem; color: #777; line-height: 1.6; margin: 0; }
.card.highlight { border-top: 3px solid #f0c040; }

.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 10px;
    margin-bottom: 1.5rem;
}
.ccard {
    background: #fafafa;
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    padding: 1rem;
}
.ccard h5 { font-size: 0.65rem; font-weight: 700; color: #f0c040; margin: 0 0 4px; text-transform: uppercase; letter-spacing: 0.1em; background: #111; display: inline-block; padding: 2px 7px; border-radius: 3px; }
.ccard p { font-size: 0.82rem; color: #333; margin: 0; line-height: 1.6; }

.footer {
    background: #111;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 2rem;
}
.footer p { color: #666; font-size: 0.74rem; margin: 0; }
.footer strong { color: #f0c040; }

.divider { border: none; border-top: 1px solid #f0f0f0; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "site"
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✚ Telemedicina")
    st.markdown("Beverly Hills · 24/7")
    st.markdown("---")
    if st.button("🏠  Início", use_container_width=True):
        st.session_state.pagina = "site"
        st.rerun()
    if st.button("📅  Agendar consulta", use_container_width=True):
        st.session_state.pagina = "agendar"
        st.rerun()
    if st.button("📞  Contato", use_container_width=True):
        st.session_state.pagina = "contato"
        st.rerun()
    st.markdown("---")
    if st.button("🔒  Área administrativa", use_container_width=True):
        st.session_state.pagina = "admin"
        st.rerun()

if st.session_state.pagina == "site":

    st.markdown("""
    <div class="header">
      <div class="header-left">
        <div class="cross-badge">✚</div>
        <div>
          <div class="brand-name">Telemedicina</div>
          <div class="brand-tagline">Beverly Hills, CA · Atendimento médico online e presencial</div>
        </div>
      </div>
      <span class="online-badge">24/7 ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
      <h1>Sua saúde em<br><span>boas mãos.</span></h1>
      <p>Consultas médicas presenciais e online com profissionais certificados.<br>Agende em minutos, sem burocracia.</p>
      <div class="hero-pills">
        <span class="pill yellow">✚ Disponível 24/7</span>
        <span class="pill">💻 Teleconsulta</span>
        <span class="pill">📍 Beverly Hills</span>
        <span class="pill">🔒 Dados protegidos</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("📅  Agendar minha consulta", use_container_width=True):
            st.session_state.pagina = "agendar"
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Serviços</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card-grid">
      <div class="card highlight">
        <span class="ic">🩺</span>
        <h4>Clínica Geral</h4>
        <p>Consultas e check-ups para toda a família</p>
      </div>
      <div class="card">
        <span class="ic">📋</span>
        <h4>Exames & Laudos</h4>
        <p>Solicitação e análise de resultados</p>
      </div>
      <div class="card highlight">
        <span class="ic">💻</span>
        <h4>Teleconsulta</h4>
        <p>Atendimento online de qualquer lugar</p>
      </div>
      <div class="card">
        <span class="ic">❤️‍🩹</span>
        <h4>Acompanhamento</h4>
        <p>Retornos e monitoramento contínuo</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Contato</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="ccard"><h5>Telefone</h5><p>(11) 93307-537</p></div>
      <div class="ccard"><h5>WhatsApp</h5><p>(11) 93307-537<br>24/7</p></div>
      <div class="ccard"><h5>E-mail</h5><p>contato@telemedicina.com</p></div>
      <div class="ccard"><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      <p><strong>✚ Telemedicina</strong> · Beverly Hills, CA</p>
      <p>© 2026 · Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "agendar":
    st.markdown("""
    <div class="header">
      <div class="header-left">
        <div class="cross-badge">✚</div>
        <div>
          <div class="brand-name">Telemedicina</div>
          <div class="brand-tagline">Agendamento de consulta</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Formulário de agendamento</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.84rem;color:#666;margin-bottom:1.25rem;">Preencha os campos abaixo. Entraremos em contato para confirmar o horário.</p>', unsafe_allow_html=True)

    with st.form("form_agendamento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo *", placeholder="Seu nome completo")
        with col2:
            telefone = st.text_input("Telefone / WhatsApp *", placeholder="(00) 00000-0000")

        col3, col4 = st.columns(2)
        with col3:
            cpf = st.text_input("CPF *", placeholder="000.000.000-00")
        with col4:
            email = st.text_input("E-mail", placeholder="seu@email.com")

        col5, col6 = st.columns(2)
        with col5:
            data_pref = st.date_input("Data de preferência", min_value=date.today())
        with col6:
            horario = st.selectbox("Horário preferido", ["Sem preferência", "Manhã (8h–12h)", "Tarde (13h–18h)"])

        tipo = st.selectbox("Tipo de consulta *", ["Selecione...", "Consulta presencial", "Teleconsulta", "Retorno", "Check-up"])
        obs = st.text_area("Observações", placeholder="Motivo da consulta ou informações importantes para o médico...")

        enviado = st.form_submit_button("✅  Enviar agendamento", use_container_width=True)

        if enviado:
            if not nome or not telefone or tipo == "Selecione...":
                st.error("⚠️ Preencha: Nome, Telefone e Tipo de consulta.")
            elif not validar_cpf(cpf):
                st.error("⚠️ CPF inválido. Digite os 11 dígitos.")
            else:
                dados = {
                    "Nome": nome, "CPF": formatar_cpf(cpf), "Telefone": telefone,
                    "Email": email if email else "—", "Data": data_pref.strftime("%d/%m/%Y"),
                    "Horario": horario, "Tipo": tipo, "Observacoes": obs if obs else "—",
                }
                novo_id = salvar_agendamento(dados)
                st.success(f"✅ **Protocolo #{novo_id:04d} gerado!** Entraremos em contato em breve para confirmar.")
                st.balloons()

elif st.session_state.pagina == "contato":
    st.markdown("""
    <div class="header">
      <div class="header-left">
        <div class="cross-badge">✚</div>
        <div>
          <div class="brand-name">Telemedicina</div>
          <div class="brand-tagline">Fale conosco</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Canais de atendimento</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="contact-grid">
      <div class="ccard"><h5>Telefone</h5><p>(11) 93307-537</p></div>
      <div class="ccard"><h5>WhatsApp</h5><p>(11) 93307-537<br>24/7</p></div>
      <div class="ccard"><h5>E-mail</h5><p>contato@telemedicina.com</p></div>
      <div class="ccard"><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Enviar mensagem</div>', unsafe_allow_html=True)

    with st.form("form_contato", clear_on_submit=True):
        nome_c = st.text_input("Nome", placeholder="Seu nome completo")
        email_c = st.text_input("E-mail ou telefone", placeholder="Para retorno de contato")
        msg = st.text_area("Mensagem", placeholder="Como podemos te ajudar?", height=120)
        enviar_c = st.form_submit_button("✅  Enviar mensagem", use_container_width=True)
        if enviar_c:
            if not nome_c or not msg:
                st.error("Preencha nome e mensagem.")
            else:
                st.success("✅ Mensagem enviada! Entraremos em contato em breve.")

elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.markdown("""
        <div class="header">
          <div class="header-left">
            <div class="cross-badge">🔒</div>
            <div>
              <div class="brand-name">Área Administrativa</div>
              <div class="brand-tagline">Acesso restrito</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        col_l = st.columns([1, 2, 1])
        with col_l[1]:
            senha = st.text_input("Senha", type="password")
            if st.button("🔓  Acessar", use_container_width=True):
                if senha == ADMIN_PASSWORD:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        st.markdown('<div class="section-title">Painel de agendamentos</div>', unsafe_allow_html=True)

        if st.button("🚪  Sair"):
            st.session_state.admin_logado = False
            st.session_state.pagina = "site"
            st.rerun()

        df = carregar_dados()

        if df.empty:
            st.info("Nenhum agendamento registrado ainda.")
        else:
            total = len(df)
            aguardando = len(df[df["Status"] == "Aguardando confirmação"]) if "Status" in df.columns else 0
            confirmados = len(df[df["Status"] == "Confirmado"]) if "Status" in df.columns else 0
            cancelados = len(df[df["Status"] == "Cancelado"]) if "Status" in df.columns else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total", total)
            c2.metric("Aguardando", aguardando)
            c3.metric("Confirmados", confirmados)
            c4.metric("Cancelados", cancelados)

            st.markdown("---")
            status_filtro = st.selectbox("Filtrar", ["Todos", "Aguardando confirmação", "Confirmado", "Cancelado"])
            df_view = df if status_filtro == "Todos" else df[df["Status"] == status_filtro]
            st.dataframe(df_view, use_container_width=True, hide_index=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                id_sel = st.number_input("ID do protocolo", min_value=1, step=1)
            with col_b:
                novo_status = st.selectbox("Novo status", ["Aguardando confirmação", "Confirmado", "Cancelado"])
            if st.button("✅  Atualizar status", use_container_width=True):
                df_full = carregar_dados()
                if id_sel in df_full["ID"].values:
                    df_full.loc[df_full["ID"] == id_sel, "Status"] = novo_status
                    df_full.to_excel(DATA_FILE, index=False)
                    st.success(f"Protocolo #{int(id_sel):04d} → {novo_status}")
                    st.rerun()
                else:
                    st.error("ID não encontrado.")

            st.markdown("---")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.download_button("⬇️  Exportar agendamentos (.xlsx)", buffer.getvalue(),
                "agendamentos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)
