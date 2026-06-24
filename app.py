import streamlit as st

st.set_page_config(
    page_title="Clínica Saúde",
    page_icon="🌿",
    layout="centered",
)

st.markdown("""
<style>
    .hero {
        background: #EAF3DE;
        border-radius: 12px;
        padding: 2.5rem 2rem;
        text-align: center;
        border: 1px solid #C0DD97;
        margin-bottom: 1.5rem;
    }
    .hero h1 { color: #27500A; font-size: 2rem; margin-bottom: 0.5rem; }
    .hero p { color: #3B6D11; font-size: 1rem; }
    .badge-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin: 1rem 0; }
    .badge {
        background: #C0DD97; color: #27500A;
        font-size: 0.82rem; padding: 5px 12px;
        border-radius: 8px; display: inline-block;
    }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin: 1.5rem 0; }
    .card {
        background: #f5f5f5; border-radius: 12px;
        padding: 1rem; text-align: center;
        border: 1px solid #e0e0e0;
    }
    .card h4 { font-size: 0.9rem; margin: 0.5rem 0 0.25rem; color: #27500A; }
    .card p { font-size: 0.8rem; color: #555; }
    .contact-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 1rem 0; }
    .contact-item {
        background: #f5f5f5; border-radius: 12px;
        padding: 1rem; border: 1px solid #e0e0e0;
    }
    .contact-item h4 { font-size: 0.85rem; color: #3B6D11; margin-bottom: 4px; }
    .contact-item p { font-size: 0.82rem; color: #555; margin: 0; }
    .section-title { font-size: 1.2rem; font-weight: 600; color: #27500A; margin-bottom: 0.25rem; }
    .section-sub { font-size: 0.88rem; color: #666; margin-bottom: 1rem; }
    .success-box {
        background: #EAF3DE; border: 1px solid #C0DD97;
        border-radius: 8px; padding: 1rem;
        color: #27500A; font-size: 0.9rem; margin-top: 1rem;
    }
    hr { border: none; border-top: 1px solid #e0e0e0; margin: 2rem 0; }
    .footer { text-align: center; font-size: 0.78rem; color: #aaa; padding: 1rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🌿 Clínica Saúde</h1>
  <p>Cuidando de você e da sua família com atenção, carinho e excelência.<br>Agende sua consulta com facilidade.</p>
  <div class="badge-row">
    <span class="badge">🕐 Seg–Sex, 8h–18h</span>
    <span class="badge">📍 Atendimento presencial</span>
    <span class="badge">📱 Teleconsulta disponível</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card-grid">
  <div class="card"><div style="font-size:1.8rem">🩺</div><h4>Clínica geral</h4><p>Consultas e check-ups para todas as idades</p></div>
  <div class="card"><div style="font-size:1.8rem">📋</div><h4>Exames e laudos</h4><p>Solicitação e análise de resultados</p></div>
  <div class="card"><div style="font-size:1.8rem">📱</div><h4>Teleconsulta</h4><p>Atendimento online pelo conforto de casa</p></div>
  <div class="card"><div style="font-size:1.8rem">❤️</div><h4>Acompanhamento</h4><p>Retornos e monitoramento contínuo</p></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-title">📅 Agendar consulta</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Preencha o formulário e entraremos em contato para confirmar seu horário.</p>', unsafe_allow_html=True)

with st.form("agendamento"):
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome completo", placeholder="Seu nome")
    with col2:
        tel = st.text_input("Telefone / WhatsApp", placeholder="(00) 00000-0000")

    col3, col4 = st.columns(2)
    with col3:
        email = st.text_input("E-mail", placeholder="seu@email.com")
    with col4:
        data = st.date_input("Data de preferência")

    col5, col6 = st.columns(2)
    with col5:
        tipo = st.selectbox("Tipo de consulta", ["Selecione...", "Consulta presencial", "Teleconsulta", "Retorno"])
    with col6:
        horario = st.selectbox("Horário preferido", ["Selecione...", "Manhã (8h–12h)", "Tarde (13h–18h)"])

    obs = st.text_area("Observações (opcional)", placeholder="Descreva brevemente o motivo da consulta ou alguma informação importante...")

    submitted = st.form_submit_button("✉️ Enviar agendamento", use_container_width=True)

    if submitted:
        if not nome or not tel:
            st.error("Por favor, preencha nome e telefone.")
        else:
            st.markdown("""
            <div class="success-box">
              ✅ <strong>Agendamento enviado com sucesso!</strong><br>
              Entraremos em contato em breve para confirmar seu horário.
            </div>
            """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('<p class="section-title">📞 Contato</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Fale conosco pelo canal de sua preferência.</p>', unsafe_allow_html=True)

st.markdown("""
<div class="contact-grid">
  <div class="contact-item"><h4>📞 Telefone</h4><p>(00) 0000-0000<br>(00) 00000-0000</p></div>
  <div class="contact-item"><h4>💬 WhatsApp</h4><p>(00) 00000-0000<br>Seg–Sex, 8h–18h</p></div>
  <div class="contact-item"><h4>📧 E-mail</h4><p>contato@clinicasaude.com.br</p></div>
  <div class="contact-item"><h4>📍 Endereço</h4><p>Rua Exemplo, 123<br>Bairro — Cidade/UF</p></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">© 2026 Clínica Saúde · Todos os direitos reservados</div>', unsafe_allow_html=True)
