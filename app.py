import streamlit as st
import pandas as pd
import os
import re
import io
from datetime import datetime, date
from openpyxl import load_workbook, Workbook

st.set_page_config(
    page_title="Telemedicina",
    page_icon="✚",
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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Inter:wght@300;400;500&display=swap');

section[data-testid="stSidebar"] { background: #0a0a0a !important; }
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] button {
    background: transparent !important;
    border: 1px solid #333 !important;
    color: #ccc !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
    border-radius: 0 !important;
}
section[data-testid="stSidebar"] button:hover { border-color: #fff !important; color: #fff !important; }

.brand {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.6rem;
    font-weight: 300;
    letter-spacing: 0.25em;
    text-align: center;
    color: #0a0a0a;
    text-transform: uppercase;
    margin: 0.5rem 0 0.2rem;
}
.brand-sub {
    text-align: center;
    font-size: 0.7rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 1.5rem;
}
.nav-bar {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    border-top: 1px solid #e0e0e0;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.75rem 0;
    margin-bottom: 2rem;
}
.nav-bar a {
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0a0a0a;
    text-decoration: none;
    font-weight: 500;
}
.hero-banner {
    background: #0a0a0a;
    color: #fff;
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        45deg, transparent, transparent 40px,
        rgba(255,255,255,0.015) 40px, rgba(255,255,255,0.015) 80px
    );
}
.hero-banner h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3rem;
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-banner p { font-size: 0.88rem; letter-spacing: 0.1em; color: #aaa; margin-bottom: 1.5rem; }
.hero-btn {
    display: inline-block;
    background: #fff;
    color: #0a0a0a;
    padding: 0.75rem 2.5rem;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 500;
    border: none;
    cursor: pointer;
    text-decoration: none;
}
.pill-row {
    display: flex;
    justify-content: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.pill {
    background: #f5f5f5;
    color: #0a0a0a;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 6px 18px;
    border: 1px solid #e0e0e0;
}
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 0.25rem;
}
.section-heading {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.8rem;
    font-weight: 300;
    color: #0a0a0a;
    margin-bottom: 1.5rem;
    letter-spacing: 0.05em;
}
.service-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1px;
    background: #e0e0e0;
    border: 1px solid #e0e0e0;
    margin-bottom: 2.5rem;
}
.service-card {
    background: #fff;
    padding: 2rem 1.25rem;
    text-align: center;
}
.service-card .sicon { font-size: 2rem; margin-bottom: 1rem; display: block; }
.service-card h4 {
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #0a0a0a;
    margin-bottom: 0.5rem;
    font-weight: 500;
}
.service-card p { font-size: 0.78rem; color: #888; line-height: 1.6; margin: 0; }
.contact-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1px;
    background: #e0e0e0;
    border: 1px solid #e0e0e0;
    margin-bottom: 2rem;
}
.contact-block {
    background: #fafafa;
    padding: 1.25rem 1rem;
}
.contact-block h5 {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #999;
    margin: 0 0 0.4rem;
    font-weight: 400;
}
.contact-block p { font-size: 0.82rem; color: #0a0a0a; margin: 0; line-height: 1.6; }
.divider {
    border: none;
    border-top: 1px solid #e8e8e8;
    margin: 2.5rem 0;
}
.footer-strip {
    border-top: 1px solid #e0e0e0;
    padding: 1.25rem 0;
    text-align: center;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #aaa;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "site"
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## ✚ TELEMEDICINA")
    st.markdown("---")
    if st.button("INÍCIO", use_container_width=True):
        st.session_state.pagina = "site"
        st.rerun()
    if st.button("AGENDAR CONSULTA", use_container_width=True):
        st.session_state.pagina = "agendar"
        st.rerun()
    if st.button("CONTATO", use_container_width=True):
        st.session_state.pagina = "contato"
        st.rerun()
    st.markdown("---")
    if st.button("ÁREA ADMINISTRATIVA", use_container_width=True):
        st.session_state.pagina = "admin"
        st.rerun()

if st.session_state.pagina == "site":

    st.markdown('<div class="brand">Telemedicina</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Saúde & Bem-estar · Beverly Hills</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-banner">
      <h2>Cuidado de excelência,<br>onde você estiver</h2>
      <p>Consultas médicas presenciais e online — 24 horas por dia, 7 dias por semana</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="pill-row">
      <span class="pill">24/7 Disponível</span>
      <span class="pill">Beverly Hills, CA</span>
      <span class="pill">Teleconsulta</span>
      <span class="pill">Primeira consulta</span>
    </div>
    """, unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("AGENDAR MINHA CONSULTA", use_container_width=True):
            st.session_state.pagina = "agendar"
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<p class="section-label">Nossos serviços</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">O que oferecemos</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="service-grid">
      <div class="service-card">
        <span class="sicon">🩺</span>
        <h4>Clínica Geral</h4>
        <p>Consultas e check-ups completos para todas as idades</p>
      </div>
      <div class="service-card">
        <span class="sicon">📋</span>
        <h4>Exames & Laudos</h4>
        <p>Solicitação e análise detalhada de resultados</p>
      </div>
      <div class="service-card">
        <span class="sicon">💻</span>
        <h4>Teleconsulta</h4>
        <p>Atendimento online pelo conforto de qualquer lugar</p>
      </div>
      <div class="service-card">
        <span class="sicon">❤️</span>
        <h4>Acompanhamento</h4>
        <p>Retornos e monitoramento contínuo da sua saúde</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Fale conosco</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Contato rápido</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-strip">
      <div class="contact-block"><h5>Telefone</h5><p>(11) 93307-537</p></div>
      <div class="contact-block"><h5>WhatsApp</h5><p>(11) 93307-537<br>Disponível 24/7</p></div>
      <div class="contact-block"><h5>E-mail</h5><p>contato@telemedicina.com</p></div>
      <div class="contact-block"><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="footer-strip">© 2026 Telemedicina · Beverly Hills · Todos os direitos reservados</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "agendar":
    st.markdown('<div class="brand">Telemedicina</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Agendamento</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Agendar consulta</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:0.85rem;color:#888;margin-bottom:1.5rem;">Preencha os dados abaixo. Entraremos em contato para confirmar seu horário.</p>', unsafe_allow_html=True)

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
        obs = st.text_area("Motivo da consulta / Observações", placeholder="Descreva brevemente o motivo ou informações importantes para o médico...")

        enviado = st.form_submit_button("ENVIAR AGENDAMENTO", use_container_width=True)

        if enviado:
            if not nome or not telefone or tipo == "Selecione...":
                st.error("Preencha os campos obrigatórios: Nome, Telefone e Tipo de consulta.")
            elif not validar_cpf(cpf):
                st.error("CPF inválido. Digite os 11 dígitos.")
            else:
                dados = {
                    "Nome": nome, "CPF": formatar_cpf(cpf), "Telefone": telefone,
                    "Email": email if email else "—", "Data": data_pref.strftime("%d/%m/%Y"),
                    "Horario": horario, "Tipo": tipo, "Observacoes": obs if obs else "—",
                }
                novo_id = salvar_agendamento(dados)
                st.success(f"Agendamento #{novo_id} enviado com sucesso! Entraremos em contato em breve.")
                st.balloons()

elif st.session_state.pagina == "contato":
    st.markdown('<div class="brand">Telemedicina</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Fale conosco</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Contato</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-strip">
      <div class="contact-block"><h5>Telefone</h5><p>(11) 93307-537</p></div>
      <div class="contact-block"><h5>WhatsApp</h5><p>(11) 93307-537<br>Disponível 24/7</p></div>
      <div class="contact-block"><h5>E-mail</h5><p>contato@telemedicina.com</p></div>
      <div class="contact-block"><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<p class="section-label">Mensagem</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-heading">Enviar mensagem</p>', unsafe_allow_html=True)

    with st.form("form_contato", clear_on_submit=True):
        nome_c = st.text_input("Nome", placeholder="Seu nome completo")
        email_c = st.text_input("E-mail ou telefone", placeholder="Para retorno de contato")
        msg = st.text_area("Mensagem", placeholder="Como podemos te ajudar?", height=120)
        enviar_c = st.form_submit_button("ENVIAR MENSAGEM", use_container_width=True)
        if enviar_c:
            if not nome_c or not msg:
                st.error("Por favor, preencha nome e mensagem.")
            else:
                st.success("Mensagem enviada! Entraremos em contato em breve.")

elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.markdown('<div class="brand">Telemedicina</div>', unsafe_allow_html=True)
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Restrito</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-heading">Área administrativa</p>', unsafe_allow_html=True)
        col_l = st.columns([1, 2, 1])
        with col_l[1]:
            senha = st.text_input("Senha", type="password")
            if st.button("ENTRAR", use_container_width=True):
                if senha == ADMIN_PASSWORD:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        st.markdown('<p class="section-label">Painel</p>', unsafe_allow_html=True)
        st.markdown('<p class="section-heading">Agendamentos</p>', unsafe_allow_html=True)

        if st.button("SAIR"):
            st.session_state.admin_logado = False
            st.session_state.pagina = "site"
            st.rerun()

        df = carregar_dados()

        if df.empty:
            st.info("Nenhum agendamento registrado ainda.")
        else:
            total = len(df)
            aguardando = len(df[df["Status"] == "Aguardando confirmação"]) if "Status" in df.columns else 0

            c1, c2, c3 = st.columns(3)
            c1.metric("Total", total)
            c2.metric("Aguardando", aguardando)
            c3.metric("Confirmados", total - aguardando)

            st.markdown("---")
            status_filtro = st.selectbox("Filtrar por status", ["Todos", "Aguardando confirmação", "Confirmado", "Cancelado"])
            df_view = df if status_filtro == "Todos" else df[df["Status"] == status_filtro]
            st.dataframe(df_view, use_container_width=True, hide_index=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                id_sel = st.number_input("ID do agendamento", min_value=1, step=1)
            with col_b:
                novo_status = st.selectbox("Novo status", ["Aguardando confirmação", "Confirmado", "Cancelado"])
            if st.button("ATUALIZAR STATUS"):
                df_full = carregar_dados()
                if id_sel in df_full["ID"].values:
                    df_full.loc[df_full["ID"] == id_sel, "Status"] = novo_status
                    df_full.to_excel(DATA_FILE, index=False)
                    st.success(f"Agendamento #{int(id_sel)} atualizado para {novo_status}.")
                    st.rerun()
                else:
                    st.error("ID não encontrado.")

            st.markdown("---")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.download_button("EXPORTAR AGENDAMENTOS (.xlsx)", buffer.getvalue(), "agendamentos.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
