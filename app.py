import streamlit as st
import pandas as pd
import os
import re
import io
from datetime import datetime, date
from openpyxl import Workbook

st.set_page_config(
    page_title="Telemedicina — Portal de Saúde",
    page_icon="🏥",
    layout="wide",
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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1a3a2a !important;
    border-right: 3px solid #f5c400 !important;
}
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] .stMarkdown p {
    color: #a8c5b5 !important;
    font-size: 0.78rem;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}
section[data-testid="stSidebar"] button {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e8f5ee !important;
    border-radius: 4px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    margin-bottom: 3px !important;
    text-align: left !important;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(245,196,0,0.15) !important;
    border-color: #f5c400 !important;
    color: #f5c400 !important;
}

/* Gov top bar */
.gov-topbar {
    background: #1a3a2a;
    padding: 0.4rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
}
.gov-topbar span {
    font-size: 0.72rem;
    color: #a8c5b5;
    letter-spacing: 0.03em;
}
.gov-topbar .gov-badge {
    background: #f5c400;
    color: #1a3a2a;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 3px;
    letter-spacing: 0.06em;
}

/* Header institucional */
.inst-header {
    background: #fff;
    border-bottom: 4px solid #f5c400;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0;
}
.inst-logo {
    width: 52px; height: 52px;
    background: #1a6b4a;
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    flex-shrink: 0;
}
.inst-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1a3a2a;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.inst-sub {
    font-size: 0.72rem;
    color: #666;
    margin-top: 2px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.inst-right {
    margin-left: auto;
    text-align: right;
}
.inst-right .date-info {
    font-size: 0.72rem;
    color: #888;
}
.inst-right .status-online {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #e8f5ee;
    border: 1px solid #b2dfcc;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.7rem;
    color: #1a6b4a;
    font-weight: 600;
    margin-top: 4px;
}
.status-dot {
    width: 7px; height: 7px;
    background: #1a6b4a;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Alerta amarelo */
.alert-bar {
    background: #fff8d6;
    border-left: 5px solid #f5c400;
    border-bottom: 1px solid #f0dc80;
    padding: 0.7rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.82rem;
    color: #5a4a00;
    margin-bottom: 1.5rem;
}

/* Breadcrumb */
.breadcrumb {
    font-size: 0.74rem;
    color: #888;
    margin-bottom: 1.25rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #eee;
}
.breadcrumb span { color: #1a6b4a; font-weight: 500; }

/* Painel de boas vindas */
.welcome-panel {
    background: linear-gradient(135deg, #1a6b4a 0%, #1a3a2a 100%);
    border-radius: 8px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    border: 2px solid #f5c400;
    position: relative;
    overflow: hidden;
}
.welcome-panel::before {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 200px; height: 100%;
    background: repeating-linear-gradient(
        -45deg,
        transparent, transparent 8px,
        rgba(245,196,0,0.07) 8px, rgba(245,196,0,0.07) 16px
    );
}
.welcome-panel h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.4rem;
    letter-spacing: -0.02em;
}
.welcome-panel p { font-size: 0.88rem; color: #a8c5b5; line-height: 1.6; margin-bottom: 1rem; }
.welcome-pills { display: flex; gap: 8px; flex-wrap: wrap; }
.pill-green {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 3px;
    font-weight: 500;
}
.pill-yellow {
    background: #f5c400;
    color: #1a3a2a;
    font-size: 0.72rem;
    padding: 4px 12px;
    border-radius: 3px;
    font-weight: 700;
}
.welcome-nums {
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 180px;
}
.num-box {
    background: rgba(245,196,0,0.12);
    border: 1px solid rgba(245,196,0,0.35);
    border-radius: 6px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.num-box .nb { font-size: 1.5rem; font-weight: 700; color: #f5c400; }
.num-box .nl { font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 2px; }

/* Cards de serviço */
.serv-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 14px;
    margin-bottom: 2rem;
}
.serv-card {
    background: #fff;
    border: 1px solid #dde8e2;
    border-radius: 6px;
    padding: 1.25rem;
    border-top: 3px solid #1a6b4a;
}
.serv-card:nth-child(2) { border-top-color: #f5c400; }
.serv-card:nth-child(4) { border-top-color: #f5c400; }
.serv-card .sic { font-size: 1.8rem; margin-bottom: 0.6rem; display: block; }
.serv-card h4 {
    font-size: 0.88rem;
    font-weight: 600;
    color: #1a3a2a;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.serv-card p { font-size: 0.78rem; color: #666; line-height: 1.6; margin: 0; }

/* Seção título gov */
.gov-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #1a6b4a;
}
.gov-section h3 {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1a3a2a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0;
}
.gov-section .gov-tag {
    background: #f5c400;
    color: #1a3a2a;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 2px;
    letter-spacing: 0.06em;
}

/* Contato */
.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    margin-bottom: 1.5rem;
}
.contact-card {
    background: #fff;
    border: 1px solid #dde8e2;
    border-radius: 6px;
    padding: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.cc-icon {
    width: 36px; height: 36px;
    background: #e8f5ee;
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; flex-shrink: 0;
    border: 1px solid #b2dfcc;
}
.contact-card h5 {
    font-size: 0.65rem;
    color: #1a6b4a;
    font-weight: 700;
    margin: 0 0 3px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.contact-card p { font-size: 0.82rem; color: #333; margin: 0; line-height: 1.5; }

/* Footer gov */
.gov-footer {
    background: #1a3a2a;
    border-top: 3px solid #f5c400;
    border-radius: 6px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 2rem;
}
.gov-footer p { color: #a8c5b5; font-size: 0.75rem; margin: 0; }
.gov-footer strong { color: #f5c400; }

.divider { border: none; border-top: 1px solid #e8eee8; margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "site"
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🏥 TELEMEDICINA")
    st.markdown("Portal de Saúde · Beverly Hills")
    st.markdown("---")
    if st.button("🏠  Página inicial", use_container_width=True):
        st.session_state.pagina = "site"
        st.rerun()
    if st.button("📅  Agendar consulta", use_container_width=True):
        st.session_state.pagina = "agendar"
        st.rerun()
    if st.button("📞  Fale conosco", use_container_width=True):
        st.session_state.pagina = "contato"
        st.rerun()
    st.markdown("---")
    if st.button("🔒  Área restrita", use_container_width=True):
        st.session_state.pagina = "admin"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(245,196,0,0.1);border:1px solid rgba(245,196,0,0.3);border-radius:6px;padding:12px;font-size:0.78rem;color:#a8c5b5;line-height:1.7;'>
    📍 8701 Charleville Blvd<br>Beverly Hills, CA 90211<br><br>
    📞 (11) 93307-537<br>
    💬 WhatsApp 24/7<br>
    📧 contato@telemedicina.com
    </div>
    """, unsafe_allow_html=True)

hoje = datetime.now().strftime("%d/%m/%Y — %H:%M")

if st.session_state.pagina == "site":

    st.markdown(f"""
    <div class="gov-topbar">
      <span>🏥 Portal Oficial de Saúde · Telemedicina</span>
      <span class="gov-badge">ATENDIMENTO 24/7</span>
    </div>
    <div class="inst-header">
      <div class="inst-logo">🏥</div>
      <div>
        <div class="inst-name">Telemedicina</div>
        <div class="inst-sub">Portal de Agendamento e Atendimento Médico Online</div>
      </div>
      <div class="inst-right">
        <div class="date-info">{hoje}</div>
        <div class="status-online"><span class="status-dot"></span> Sistema online</div>
      </div>
    </div>
    <div class="alert-bar">
      ⚠️ <strong>Atenção:</strong> Para agendar sua consulta, tenha em mãos seu CPF e número de telefone. Atendimento 24h disponível.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="breadcrumb">Início › Portal de Saúde › <span>Página Inicial</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-panel">
      <div>
        <h2>Sua saúde é nossa prioridade.</h2>
        <p>Agende sua consulta médica presencial ou online de forma<br>rápida, segura e sem burocracia. Disponível 24 horas por dia.</p>
        <div class="welcome-pills">
          <span class="pill-yellow">✚ Atendimento 24/7</span>
          <span class="pill-green">💻 Teleconsulta disponível</span>
          <span class="pill-green">📍 Beverly Hills, CA</span>
          <span class="pill-green">🔒 Dados protegidos</span>
        </div>
      </div>
      <div class="welcome-nums">
        <div class="num-box"><div class="nb">24/7</div><div class="nl">Horas de atendimento</div></div>
        <div class="num-box"><div class="nb">100%</div><div class="nl">Online & Presencial</div></div>
        <div class="num-box"><div class="nb">🏅</div><div class="nl">Profissionais certificados</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gov-section">
      <h3>Serviços disponíveis</h3>
      <span class="gov-tag">ACESSO PÚBLICO</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="serv-grid">
      <div class="serv-card"><span class="sic">🩺</span><h4>Clínica Geral</h4><p>Consultas e check-ups completos para toda a família</p></div>
      <div class="serv-card"><span class="sic">📋</span><h4>Exames & Laudos</h4><p>Solicitação e análise detalhada de resultados</p></div>
      <div class="serv-card"><span class="sic">💻</span><h4>Teleconsulta</h4><p>Atendimento médico online, onde você estiver</p></div>
      <div class="serv-card"><span class="sic">❤️‍🩹</span><h4>Acompanhamento</h4><p>Retornos e monitoramento contínuo da saúde</p></div>
    </div>
    """, unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("📅  AGENDAR MINHA CONSULTA", use_container_width=True):
            st.session_state.pagina = "agendar"
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="gov-section">
      <h3>Informações de contato</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="contact-card"><div class="cc-icon">📞</div><div><h5>Telefone</h5><p>(11) 93307-537</p></div></div>
      <div class="contact-card"><div class="cc-icon">💬</div><div><h5>WhatsApp</h5><p>(11) 93307-537 · 24/7</p></div></div>
      <div class="contact-card"><div class="cc-icon">📧</div><div><h5>E-mail</h5><p>contato@telemedicina.com</p></div></div>
      <div class="contact-card"><div class="cc-icon">📍</div><div><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gov-footer">
      <p><strong>✚ TELEMEDICINA</strong> · Portal Oficial de Saúde · Beverly Hills, CA</p>
      <p>© 2026 · Todos os direitos reservados · Atendimento 24/7</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "agendar":
    st.markdown(f"""
    <div class="gov-topbar">
      <span>🏥 Portal Oficial de Saúde · Telemedicina</span>
      <span class="gov-badge">ATENDIMENTO 24/7</span>
    </div>
    <div class="inst-header">
      <div class="inst-logo">🏥</div>
      <div>
        <div class="inst-name">Telemedicina</div>
        <div class="inst-sub">Portal de Agendamento e Atendimento Médico Online</div>
      </div>
      <div class="inst-right">
        <div class="date-info">{hoje}</div>
        <div class="status-online"><span class="status-dot"></span> Sistema online</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="breadcrumb">Início › <span>Agendar Consulta</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="gov-section">
      <h3>Formulário de agendamento</h3>
      <span class="gov-tag">CAMPOS * OBRIGATÓRIOS</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.83rem;color:#666;margin-bottom:1.25rem;">Preencha os dados abaixo com atenção. Nossa equipe entrará em contato para confirmar o horário.</p>', unsafe_allow_html=True)

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
        obs = st.text_area("Motivo da consulta / Observações", placeholder="Descreva brevemente o motivo da consulta ou informações importantes para o médico...")

        enviado = st.form_submit_button("✅  CONFIRMAR AGENDAMENTO", use_container_width=True)

        if enviado:
            if not nome or not telefone or tipo == "Selecione...":
                st.error("⚠️ Preencha os campos obrigatórios: Nome, Telefone e Tipo de consulta.")
            elif not validar_cpf(cpf):
                st.error("⚠️ CPF inválido. Digite os 11 dígitos.")
            else:
                dados = {
                    "Nome": nome, "CPF": formatar_cpf(cpf), "Telefone": telefone,
                    "Email": email if email else "—", "Data": data_pref.strftime("%d/%m/%Y"),
                    "Horario": horario, "Tipo": tipo, "Observacoes": obs if obs else "—",
                }
                novo_id = salvar_agendamento(dados)
                st.success(f"✅ **Protocolo #{novo_id:04d} gerado com sucesso!** Guarde este número. Nossa equipe entrará em contato em breve para confirmar.")
                st.balloons()

elif st.session_state.pagina == "contato":
    st.markdown(f"""
    <div class="gov-topbar">
      <span>🏥 Portal Oficial de Saúde · Telemedicina</span>
      <span class="gov-badge">ATENDIMENTO 24/7</span>
    </div>
    <div class="inst-header">
      <div class="inst-logo">🏥</div>
      <div>
        <div class="inst-name">Telemedicina</div>
        <div class="inst-sub">Portal de Agendamento e Atendimento Médico Online</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="breadcrumb">Início › <span>Fale Conosco</span></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="gov-section"><h3>Canais de atendimento</h3></div>
    <div class="contact-grid">
      <div class="contact-card"><div class="cc-icon">📞</div><div><h5>Telefone</h5><p>(11) 93307-537</p></div></div>
      <div class="contact-card"><div class="cc-icon">💬</div><div><h5>WhatsApp</h5><p>(11) 93307-537 · 24/7</p></div></div>
      <div class="contact-card"><div class="cc-icon">📧</div><div><h5>E-mail</h5><p>contato@telemedicina.com</p></div></div>
      <div class="contact-card"><div class="cc-icon">📍</div><div><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("""<div class="gov-section"><h3>Enviar mensagem</h3></div>""", unsafe_allow_html=True)

    with st.form("form_contato", clear_on_submit=True):
        nome_c = st.text_input("Nome completo", placeholder="Seu nome")
        email_c = st.text_input("E-mail ou telefone", placeholder="Para retorno de contato")
        msg = st.text_area("Mensagem", placeholder="Como podemos te ajudar?", height=120)
        enviar_c = st.form_submit_button("✅  ENVIAR MENSAGEM", use_container_width=True)
        if enviar_c:
            if not nome_c or not msg:
                st.error("Preencha nome e mensagem.")
            else:
                st.success("✅ Mensagem enviada com sucesso! Entraremos em contato em breve.")

elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.markdown("""
        <div class="gov-topbar"><span>🔒 Área Restrita · Telemedicina</span></div>
        <div class="inst-header">
          <div class="inst-logo">🔒</div>
          <div>
            <div class="inst-name">Área Administrativa</div>
            <div class="inst-sub">Acesso restrito à equipe autorizada</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        col_l = st.columns([1, 2, 1])
        with col_l[1]:
            st.markdown('<br>', unsafe_allow_html=True)
            senha = st.text_input("Senha de acesso", type="password")
            if st.button("🔓  ACESSAR PAINEL", use_container_width=True):
                if senha == ADMIN_PASSWORD:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta. Acesso negado.")
    else:
        st.markdown("""
        <div class="gov-topbar"><span>🗂️ Painel Administrativo · Telemedicina</span><span class="gov-badge">ÁREA RESTRITA</span></div>
        """, unsafe_allow_html=True)
        st.markdown("""<div class="gov-section"><h3>Painel de agendamentos</h3><span class="gov-tag">RESTRITO</span></div>""", unsafe_allow_html=True)

        if st.button("🚪  Encerrar sessão"):
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
            c1.metric("📋 Total", total)
            c2.metric("⏳ Aguardando", aguardando)
            c3.metric("✅ Confirmados", confirmados)
            c4.metric("❌ Cancelados", cancelados)

            st.markdown("---")
            st.markdown("""<div class="gov-section"><h3>Lista de agendamentos</h3></div>""", unsafe_allow_html=True)
            status_filtro = st.selectbox("Filtrar por status", ["Todos", "Aguardando confirmação", "Confirmado", "Cancelado"])
            df_view = df if status_filtro == "Todos" else df[df["Status"] == status_filtro]
            st.dataframe(df_view, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("""<div class="gov-section"><h3>Atualizar status</h3></div>""", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                id_sel = st.number_input("Número do protocolo (ID)", min_value=1, step=1)
            with col_b:
                novo_status = st.selectbox("Novo status", ["Aguardando confirmação", "Confirmado", "Cancelado"])
            if st.button("✅  ATUALIZAR STATUS", use_container_width=True):
                df_full = carregar_dados()
                if id_sel in df_full["ID"].values:
                    df_full.loc[df_full["ID"] == id_sel, "Status"] = novo_status
                    df_full.to_excel(DATA_FILE, index=False)
                    st.success(f"Protocolo #{int(id_sel):04d} atualizado para **{novo_status}**.")
                    st.rerun()
                else:
                    st.error("Protocolo não encontrado.")

            st.markdown("---")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.download_button("⬇️  EXPORTAR PLANILHA DE AGENDAMENTOS (.xlsx)", buffer.getvalue(),
                "agendamentos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)
