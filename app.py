import streamlit as st
import pandas as pd
import os
from datetime import datetime, date

st.set_page_config(
    page_title="Clínica Saúde",
    page_icon="🌿",
    layout="centered",
)

DATA_FILE = "agendamentos.csv"
ADMIN_PASSWORD = "clinica2024"

COLUNAS = ["ID", "Nome", "Telefone", "Email", "Data", "Horario", "Tipo", "Observacoes", "Recebido_em", "Status"]

def carregar_dados():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=COLUNAS)

def salvar_agendamento(dados):
    df = carregar_dados()
    novo_id = len(df) + 1
    dados["ID"] = novo_id
    dados["Recebido_em"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    dados["Status"] = "Aguardando confirmação"
    nova_linha = pd.DataFrame([dados])
    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return novo_id

st.markdown("""
<style>
.hero {
    background: #EAF3DE;
    border-radius: 14px;
    padding: 2.5rem 2rem;
    text-align: center;
    border: 1px solid #C0DD97;
    margin-bottom: 1.5rem;
}
.hero h1 { color: #27500A; font-size: 2rem; margin-bottom: 0.4rem; }
.hero p { color: #3B6D11; font-size: 1rem; line-height: 1.6; }
.badge-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 1rem 0; }
.badge { background: #C0DD97; color: #27500A; font-size: 0.82rem; padding: 5px 12px; border-radius: 8px; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin: 1.5rem 0; }
.card { background: #f8f9fa; border-radius: 12px; padding: 1.1rem; text-align: center; border: 1px solid #e8ecdf; }
.card .icon { font-size: 1.9rem; }
.card h4 { font-size: 0.88rem; margin: 0.4rem 0 0.2rem; color: #27500A; font-weight: 600; }
.card p { font-size: 0.78rem; color: #666; margin: 0; }
.contact-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 1rem 0; }
.contact-item { background: #f8f9fa; border-radius: 12px; padding: 1rem; border: 1px solid #e8ecdf; }
.contact-item h4 { font-size: 0.85rem; color: #3B6D11; margin: 0 0 4px; font-weight: 600; }
.contact-item p { font-size: 0.82rem; color: #555; margin: 0; line-height: 1.5; }
.sec-title { font-size: 1.15rem; font-weight: 700; color: #27500A; margin-bottom: 0.2rem; }
.sec-sub { font-size: 0.87rem; color: #777; margin-bottom: 1rem; }
hr { border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
.footer { text-align: center; font-size: 0.78rem; color: #aaa; padding: 1.5rem 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

if "pagina" not in st.session_state:
    st.session_state.pagina = "site"
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

with st.sidebar:
    st.markdown("### 🌿 Clínica Saúde")
    st.markdown("---")
    if st.button("🏠 Início", use_container_width=True):
        st.session_state.pagina = "site"
        st.rerun()
    if st.button("📅 Agendar consulta", use_container_width=True):
        st.session_state.pagina = "agendar"
        st.rerun()
    if st.button("📞 Contato", use_container_width=True):
        st.session_state.pagina = "contato"
        st.rerun()
    st.markdown("---")
    if st.button("🔒 Área administrativa", use_container_width=True):
        st.session_state.pagina = "admin"
        st.rerun()

if st.session_state.pagina == "site":
    st.markdown("""
    <div class="hero">
      <h1>🌿 Clínica Saúde</h1>
      <p>Cuidando de você e da sua família com atenção, carinho e excelência.<br>
      Agende sua consulta de forma rápida e fácil.</p>
      <div class="badge-row">
        <span class="badge">🕐 Seg–Sex, 8h–18h</span>
        <span class="badge">📍 Atendimento presencial</span>
        <span class="badge">📱 Teleconsulta disponível</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card-grid">
      <div class="card"><div class="icon">🩺</div><h4>Clínica geral</h4><p>Consultas e check-ups para todas as idades</p></div>
      <div class="card"><div class="icon">📋</div><h4>Exames e laudos</h4><p>Solicitação e análise de resultados</p></div>
      <div class="card"><div class="icon">📱</div><h4>Teleconsulta</h4><p>Atendimento online pelo conforto de casa</p></div>
      <div class="card"><div class="icon">❤️</div><h4>Acompanhamento</h4><p>Retornos e monitoramento contínuo</p></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📅 Agendar minha consulta", use_container_width=True):
            st.session_state.pagina = "agendar"
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📞 Contato rápido</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="contact-grid">
      <div class="contact-item"><h4>📞 Telefone</h4><p>(00) 0000-0000<br>(00) 00000-0000</p></div>
      <div class="contact-item"><h4>💬 WhatsApp</h4><p>(00) 00000-0000<br>Seg–Sex, 8h–18h</p></div>
      <div class="contact-item"><h4>📧 E-mail</h4><p>contato@clinicasaude.com.br</p></div>
      <div class="contact-item"><h4>📍 Endereço</h4><p>Rua Exemplo, 123<br>Bairro — Cidade/UF</p></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Clínica Saúde · Todos os direitos reservados</div>', unsafe_allow_html=True)

elif st.session_state.pagina == "agendar":
    st.markdown('<p class="sec-title">📅 Agendar consulta</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Preencha os dados abaixo e entraremos em contato para confirmar seu horário.</p>', unsafe_allow_html=True)

    with st.form("form_agendamento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome completo *", placeholder="Seu nome completo")
        with col2:
            telefone = st.text_input("Telefone / WhatsApp *", placeholder="(00) 00000-0000")

        col3, col4 = st.columns(2)
        with col3:
            email = st.text_input("E-mail", placeholder="seu@email.com")
        with col4:
            data_pref = st.date_input("Data de preferência", min_value=date.today())

        col5, col6 = st.columns(2)
        with col5:
            tipo = st.selectbox("Tipo de consulta *", ["Selecione...", "Consulta presencial", "Teleconsulta", "Retorno", "Check-up"])
        with col6:
            horario = st.selectbox("Horário preferido", ["Sem preferência", "Manhã (8h–12h)", "Tarde (13h–18h)"])

        obs = st.text_area("Motivo da consulta / Observações", placeholder="Descreva brevemente o motivo da consulta ou informações importantes para o médico...")

        enviado = st.form_submit_button("✉️ Enviar agendamento", use_container_width=True)

        if enviado:
            if not nome or not telefone or tipo == "Selecione...":
                st.error("⚠️ Preencha os campos obrigatórios: Nome, Telefone e Tipo de consulta.")
            else:
                dados = {
                    "Nome": nome,
                    "Telefone": telefone,
                    "Email": email if email else "—",
                    "Data": data_pref.strftime("%d/%m/%Y"),
                    "Horario": horario,
                    "Tipo": tipo,
                    "Observacoes": obs if obs else "—",
                }
                novo_id = salvar_agendamento(dados)
                st.success(f"✅ **Agendamento #{novo_id} enviado com sucesso!**\n\nEntraremos em contato em breve para confirmar seu horário. Guarde o número do seu agendamento: **#{novo_id}**")
                st.balloons()

elif st.session_state.pagina == "contato":
    st.markdown('<p class="sec-title">📞 Fale conosco</p>', unsafe_allow_html=True)
    st.markdown('<p class="sec-sub">Estamos à disposição para atender você.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-grid">
      <div class="contact-item"><h4>📞 Telefone</h4><p>(00) 0000-0000<br>(00) 00000-0000</p></div>
      <div class="contact-item"><h4>💬 WhatsApp</h4><p>(00) 00000-0000<br>Seg–Sex, 8h–18h</p></div>
      <div class="contact-item"><h4>📧 E-mail</h4><p>contato@clinicasaude.com.br</p></div>
      <div class="contact-item"><h4>📍 Endereço</h4><p>Rua Exemplo, 123<br>Bairro — Cidade/UF</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p class="sec-title">✉️ Enviar mensagem</p>', unsafe_allow_html=True)
    with st.form("form_contato", clear_on_submit=True):
        nome_c = st.text_input("Seu nome", placeholder="Nome completo")
        email_c = st.text_input("E-mail ou telefone", placeholder="Para retorno de contato")
        msg = st.text_area("Mensagem", placeholder="Como podemos te ajudar?", height=120)
        enviar_c = st.form_submit_button("Enviar mensagem", use_container_width=True)
        if enviar_c:
            if not nome_c or not msg:
                st.error("Por favor, preencha nome e mensagem.")
            else:
                st.success("✅ Mensagem enviada! Entraremos em contato em breve.")

elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.markdown('<p class="sec-title">🔒 Área administrativa</p>', unsafe_allow_html=True)
        st.markdown("Acesso restrito à equipe da clínica.")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if senha == ADMIN_PASSWORD:
                st.session_state.admin_logado = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    else:
        st.markdown('<p class="sec-title">🗂️ Painel administrativo</p>', unsafe_allow_html=True)

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

            c1, c2, c3 = st.columns(3)
            c1.metric("Total de agendamentos", total)
            c2.metric("Aguardando confirmação", aguardando)
            c3.metric("Confirmados", total - aguardando)

            st.markdown("---")
            st.markdown("#### Agendamentos")

            status_filtro = st.selectbox("Filtrar por status", ["Todos", "Aguardando confirmação", "Confirmado", "Cancelado"])
            if status_filtro != "Todos":
                df_view = df[df["Status"] == status_filtro]
            else:
                df_view = df

            st.dataframe(df_view, use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("#### Atualizar status de um agendamento")
            col_a, col_b = st.columns(2)
            with col_a:
                id_sel = st.number_input("ID do agendamento", min_value=1, step=1)
            with col_b:
                novo_status = st.selectbox("Novo status", ["Aguardando confirmação", "Confirmado", "Cancelado"])
            if st.button("Atualizar status"):
                df_full = carregar_dados()
                if id_sel in df_full["ID"].values:
                    df_full.loc[df_full["ID"] == id_sel, "Status"] = novo_status
                    df_full.to_csv(DATA_FILE, index=False)
                    st.success(f"Status do agendamento #{int(id_sel)} atualizado para **{novo_status}**.")
                    st.rerun()
                else:
                    st.error("ID não encontrado.")

            st.markdown("---")
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Exportar todos os agendamentos (.csv)", csv, "agendamentos.csv", "text/csv", use_container_width=True)
