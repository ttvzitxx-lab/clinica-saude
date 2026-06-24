# 🌿 Clínica Saúde — Sistema de Agendamentos

App completo para clínicas médicas com agendamento online e painel administrativo, construído com **Streamlit**.

## Funcionalidades

### Área do paciente
- Página inicial com apresentação da clínica e serviços
- Formulário de agendamento com captura completa de dados
- Seção de contato com formulário de mensagem

### Área administrativa (`🔒 Área administrativa`)
- Login com senha
- Painel com métricas de agendamentos
- Tabela de todos os pacientes e consultas
- Filtro por status (Aguardando / Confirmado / Cancelado)
- Atualização de status por ID
- Exportação dos dados em `.csv`

**Senha padrão do admin:** `clinica2024`
> Altere a variável `ADMIN_PASSWORD` no arquivo `app.py` antes de publicar.

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como publicar no Streamlit Cloud (link público gratuito)

1. Suba este repositório no GitHub (público ou privado)
2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com o GitHub
3. Clique em **"New app"** → selecione o repositório → entry point: `app.py`
4. Clique em **Deploy** — o link público é gerado automaticamente

## Estrutura

```
.
├── app.py               # Aplicação principal
├── requirements.txt     # Dependências
├── agendamentos.csv     # Criado automaticamente ao primeiro agendamento
└── README.md
```

## Personalização

Edite `app.py` para alterar:
- `ADMIN_PASSWORD` — senha do painel admin
- Nome, endereço, telefone e e-mail da clínica
- Serviços oferecidos
- Horários de atendimento
