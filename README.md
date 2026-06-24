# 🌿 Clínica Saúde

Site de agendamentos médicos construído com **Streamlit**.

## Funcionalidades

- Página inicial com apresentação da clínica
- Cards de serviços (clínica geral, exames, teleconsulta, acompanhamento)
- Formulário de agendamento de consultas
- Seção de contato com telefone, WhatsApp, e-mail e endereço

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como publicar no Streamlit Cloud

1. Faça o fork ou push deste repositório para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte seu repositório GitHub
4. Selecione o arquivo `app.py` como entry point
5. Clique em **Deploy** — o link público será gerado automaticamente

## Estrutura

```
.
├── app.py            # Aplicação principal
├── requirements.txt  # Dependências
└── README.md
```

## Personalização

Edite o arquivo `app.py` para alterar:
- Nome da clínica
- Serviços oferecidos
- Informações de contato (telefone, endereço, e-mail)
- Horários de atendimento
