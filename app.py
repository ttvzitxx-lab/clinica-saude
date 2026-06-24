import streamlit as st
import pandas as pd
import os
import re
import io
from datetime import datetime, date
from openpyxl import Workbook

st.set_page_config(
    page_title="Telemedicina",
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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c6e5c 0%, #085046 100%) !important;
}
section[data-testid="stSidebar"] * { color: #fff !important; }
section[data-testid="stSidebar"] .stMarkdown p { color: #b2dfdb !important; font-size: 0.78rem; }
section[data-testid="stSidebar"] button {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    margin-bottom: 4px !important;
    transition: background 0.2s;
}
section[data-testid="stSidebar"] button:hover {
    background: rgba(255,255,255,0.18) !important;
}

.topbar {
    background: #fff;
    border-bottom: 2px solid #0c6e5c;
    padding: 1rem 2rem;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0;
}
.topbar-cross {
    width: 42px; height: 42px;
    background: #0c6e5c;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; color: #fff; font-weight: 700; flex-shrink: 0;
}
.topbar-title { font-size: 1.4rem; font-weight: 700; color: #0c6e5c; letter-spacing: -0.02em; }
.topbar-sub { font-size: 0.75rem; color: #888; margin-top: 1px; }

.hero {
    background: linear-gradient(135deg, #0c6e5c 0%, #0a8f73 50%, #07b89a 100%);
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 2rem;
    border-radius: 16px;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '✚';
    position: absolute;
    right: -20px; top: -30px;
    font-size: 12rem;
    color: rgba(255,255,255,0.06);
    font-weight: 700;
}
.hero-text h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: #fff;
    line-height: 1.2;
    margin-bottom: 0.75rem;
    letter-spacing: -0.03em;
}
.hero-text p { font-size: 1rem; color: rgba(255,255,255,0.82); line-height: 1.7; margin-bottom: 1.5rem; }
.hero-pills { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-pill {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    color: #fff;
    font-size: 0.76rem;
    padding: 5px 14px;
    border-radius: 20px;
    font-weight: 500;
}
.hero-stats {
    display: flex;
    flex-direction: column;
    gap: 12px;
    min-width: 200px;
}
.stat-box {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    text-align: center;
    color: #fff;
}
.stat-box .num { font-size: 1.6rem; font-weight: 700; }
.stat-box .lbl { font-size: 0.72rem; color: rgba(255,255,255,0.75); margin-top: 2px; }

.section-tag {
    display: inline-flex; align-items: center; gap: 6px;
    background: #e8f5f0;
    color: #0c6e5c;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 0.6rem;
    letter-spacing: 0.04em;
}
.section-h { font-size: 1.6rem; font-weight: 700; color: #111; margin-bottom: 1.5rem; letter-spacing: -0.02em; }

.service-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 2.5rem;
}
.service-card {
    background: #fff;
    border: 1px solid #e8f5f0;
    border-radius: 14px;
    padding: 1.5rem 1.25rem;
    border-top: 4px solid #0c6e5c;
    transition: box-shadow 0.2s;
}
.service-card:hover { box-shadow: 0 4px 20px rgba(12,110,92,0.12); }
.service-card .sicon { font-size: 2rem; margin-bottom: 0.75rem; display: block; }
.service-card h4 { font-size: 0.92rem; font-weight: 600; color: #111; margin-bottom: 0.4rem; }
.service-card p { font-size: 0.8rem; color: #666; line-height: 1.6; margin: 0; }

.trust-strip {
    background: #f0faf7;
    border: 1px solid #c8ede4;
    border-radius: 14px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 0;
    margin-bottom: 2.5rem;
    overflow: hidden;
}
.trust-item {
    padding: 1.25rem 1rem;
    text-align: center;
    border-right: 1px solid #c8ede4;
}
.trust-item:last-child { border-right: none; }
.trust-item .tnum { font-size: 1.5rem; font-weight: 700; color: #0c6e5c; }
.trust-item .tlbl { font-size: 0.75rem; color: #555; margin-top: 2px; }

.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-bottom: 2rem;
}
.contact-card {
    background: #fff;
    border: 1px solid #e8f5f0;
    border-radius: 12px;
    padding: 1.25rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
}
.contact-card .cicon {
    width: 38px; height: 38px;
    background: #e8f5f0;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.contact-card h5 { font-size: 0.72rem; color: #0c6e5c; font-weight: 600; margin: 0 0 3px; text-transform: uppercase; letter-spacing: 0.06em; }
.contact-card p { font-size: 0.82rem; color: #333; margin: 0; line-height: 1.5; }

.divider { border: none; border-top: 1px solid #eef5f3; margin: 2.5rem 0; }

.footer {
    background: #0c6e5c;
    border-radius: 12px;
    padding: 1.25rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.5rem;
}
.footer p { color: rgba(255,255,255,0.75); font-size: 0.78rem; margin: 0; }
.footer strong { color: #fff; }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "site"
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## 🏥 Telemedicina")
    st.markdown("Beverly Hills, CA · 24/7")
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
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(255,255,255,0.1);border-radius:10px;padding:12px;font-size:0.78rem;color:rgba(255,255,255,0.8);'>
    📍 8701 Charleville Blvd<br>Beverly Hills, CA 90211<br><br>
    📞 (11) 93307-537<br>
    💬 WhatsApp 24/7
    </div>
    """, unsafe_allow_html=True)

if st.session_state.pagina == "site":

    st.markdown("""
    <div class="topbar">
      <div class="topbar-cross">✚</div>
      <div>
        <div class="topbar-title">Telemedicina</div>
        <div class="topbar-sub">Saúde & Bem-estar · Beverly Hills, CA</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
      <div class="hero-text">
        <h1>Sua saúde em<br>boas mãos, sempre.</h1>
        <p>Atendimento médico de excelência, presencial ou online.<br>
        Disponível 24 horas por dia, 7 dias por semana.</p>
        <div class="hero-pills">
          <span class="hero-pill">🕐 24/7 Disponível</span>
          <span class="hero-pill">💻 Teleconsulta</span>
          <span class="hero-pill">📍 Beverly Hills</span>
          <span class="hero-pill">✅ Agendamento fácil</span>
        </div>
      </div>
      <div class="hero-stats">
        <div class="stat-box"><div class="num">24/7</div><div class="lbl">Disponibilidade</div></div>
        <div class="stat-box"><div class="num">100%</div><div class="lbl">Online & Presencial</div></div>
        <div class="stat-box"><div class="num">🏥</div><div class="lbl">Beverly Hills, CA</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="trust-strip">
      <div class="trust-item"><div class="tnum">24/7</div><div class="tlbl">Atendimento</div></div>
      <div class="trust-item"><div class="tnum">100%</div><div class="tlbl">Online disponível</div></div>
      <div class="trust-item"><div class="tnum">🏅</div><div class="tlbl">Profissionais certificados</div></div>
      <div class="trust-item"><div class="tnum">🔒</div><div class="tlbl">Dados protegidos</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-tag">🩺 Serviços</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">O que oferecemos</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="service-grid">
      <div class="service-card">
        <span class="sicon">🩺</span>
        <h4>Clínica Geral</h4>
        <p>Consultas e check-ups completos para toda a família, de todas as idades</p>
      </div>
      <div class="service-card">
        <span class="sicon">📋</span>
        <h4>Exames & Laudos</h4>
        <p>Solicitação, análise e interpretação detalhada dos seus resultados</p>
      </div>
      <div class="service-card">
        <span class="sicon">💻</span>
        <h4>Teleconsulta</h4>
        <p>Atendimento médico online, onde você estiver, com total segurança</p>
      </div>
      <div class="service-card">
        <span class="sicon">❤️‍🩹</span>
        <h4>Acompanhamento</h4>
        <p>Retornos e monitoramento contínuo da sua saúde e bem-estar</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])
    with col_btn[1]:
        if st.button("📅 Agendar minha consulta agora", use_container_width=True):
            st.session_state.pagina = "agendar"
            st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">📞 Contato</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Fale conosco</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="contact-card"><div class="cicon">📞</div><div><h5>Telefone</h5><p>(11) 93307-537</p></div></div>
      <div class="contact-card"><div class="cicon">💬</div><div><h5>WhatsApp</h5><p>(11) 93307-537<br>Disponível 24/7</p></div></div>
      <div class="contact-card"><div class="cicon">📧</div><div><h5>E-mail</h5><p>contato@telemedicina.com</p></div></div>
      <div class="contact-card"><div class="cicon">📍</div><div><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
      <p><strong>✚ Telemedicina</strong> · Beverly Hills, CA</p>
      <p>© 2026 · Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.pagina == "agendar":
    st.markdown('<div class="section-tag">📅 Agendamento</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Agendar consulta</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#666;font-size:0.88rem;margin-bottom:1.5rem;">Preencha os dados abaixo. Nossa equipe entrará em contato para confirmar seu horário.</p>', unsafe_allow_html=True)

    with st.form("form_agendamento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("👤 Nome completo *", placeholder="Seu nome completo")
        with col2:
            telefone = st.text_input("📞 Telefone / WhatsApp *", placeholder="(00) 00000-0000")

        col3, col4 = st.columns(2)
        with col3:
            cpf = st.text_input("🪪 CPF *", placeholder="000.000.000-00")
        with col4:
            email = st.text_input("📧 E-mail", placeholder="seu@email.com")

        col5, col6 = st.columns(2)
        with col5:
            data_pref = st.date_input("📆 Data de preferência", min_value=date.today())
        with col6:
            horario = st.selectbox("🕐 Horário preferido", ["Sem preferência", "Manhã (8h–12h)", "Tarde (13h–18h)"])

        tipo = st.selectbox("🩺 Tipo de consulta *", ["Selecione...", "Consulta presencial", "Teleconsulta", "Retorno", "Check-up"])
        obs = st.text_area("📝 Motivo da consulta / Observações", placeholder="Descreva brevemente o motivo da consulta ou informações importantes para o médico...")

        enviado = st.form_submit_button("✅ Enviar agendamento", use_container_width=True)

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
                st.success(f"✅ **Agendamento #{novo_id} enviado com sucesso!** Nossa equipe entrará em contato em breve para confirmar.")
                st.balloons()

elif st.session_state.pagina == "contato":
    st.markdown('<div class="section-tag">📞 Contato</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Fale conosco</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="contact-card"><div class="cicon">📞</div><div><h5>Telefone</h5><p>(11) 93307-537</p></div></div>
      <div class="contact-card"><div class="cicon">💬</div><div><h5>WhatsApp</h5><p>(11) 93307-537<br>Disponível 24/7</p></div></div>
      <div class="contact-card"><div class="cicon">📧</div><div><h5>E-mail</h5><p>contato@telemedicina.com</p></div></div>
      <div class="contact-card"><div class="cicon">📍</div><div><h5>Endereço</h5><p>8701 Charleville Blvd<br>Beverly Hills, CA 90211</p></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">✉️ Mensagem</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h">Enviar mensagem</div>', unsafe_allow_html=True)

    with st.form("form_contato", clear_on_submit=True):
        nome_c = st.text_input("👤 Nome", placeholder="Seu nome completo")
        email_c = st.text_input("📧 E-mail ou telefone", placeholder="Para retorno de contato")
        msg = st.text_area("💬 Mensagem", placeholder="Como podemos te ajudar?", height=120)
        enviar_c = st.form_submit_button("✅ Enviar mensagem", use_container_width=True)
        if enviar_c:
            if not nome_c or not msg:
                st.error("Por favor, preencha nome e mensagem.")
            else:
                st.success("✅ Mensagem enviada! Entraremos em contato em breve.")

elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.markdown('<div class="section-tag">🔒 Restrito</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-h">Área administrativa</div>', unsafe_allow_html=True)
        col_l = st.columns([1, 2, 1])
        with col_l[1]:
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if senha == ADMIN_PASSWORD:
                    st.session_state.admin_logado = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
    else:
        st.markdown('<div class="section-tag">🗂️ Painel</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-h">Agendamentos</div>', unsafe_allow_html=True)

        if st.button("🚪 Sair"):
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

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total de agendamentos", total)
            c2.metric("Aguardando confirmação", aguardando)
            c3.metric("Confirmados", confirmados)
            c4.metric("Cancelados", total - aguardando - confirmados)

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
            if st.button("✅ Atualizar status", use_container_width=True):
                df_full = carregar_dados()
                if id_sel in df_full["ID"].values:
                    df_full.loc[df_full["ID"] == id_sel, "Status"] = novo_status
                    df_full.to_excel(DATA_FILE, index=False)
                    st.success(f"Agendamento #{int(id_sel)} atualizado para **{novo_status}**.")
                    st.rerun()
                else:
                    st.error("ID não encontrado.")

            st.markdown("---")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            st.download_button("⬇️ Exportar agendamentos (.xlsx)", buffer.getvalue(), "agendamentos.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
