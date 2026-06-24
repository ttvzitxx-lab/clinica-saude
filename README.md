# 🏥 Telemedicina — Sistema de Agendamentos Médicos

Plataforma completa de agendamentos médicos com design moderno voltado para saúde e bem-estar. Interface verde profissional, painel administrativo e banco de dados em Excel. Construído com **Streamlit**.

## Informações da clínica

| Campo | Informação |
|---|---|
| **Nome** | Telemedicina |
| **Telefone** | (11) 93307-537 |
| **WhatsApp** | (11) 93307-537 — 24/7 |
| **E-mail** | contato@telemedicina.com |
| **Endereço** | 8701 Charleville Blvd, Beverly Hills, CA 90211 |
| **Horário** | 24/7 |

## Funcionalidades

### Área do paciente
- **Página inicial** com hero verde, cards de serviços e faixa de diferenciais
- **Serviços:** Clínica Geral, Exames & Laudos, Teleconsulta, Acompanhamento
- **Formulário de agendamento** com: Nome, CPF (validado), Telefone, E-mail, Data, Horário, Tipo de consulta e Observações
- **Página de contato** com formulário de mensagem

### Área administrativa (`🔒 Área administrativa`)
- Login com senha
- Métricas: Total, Aguardando, Confirmados, Cancelados
- Tabela completa de pacientes
- Filtro por status
- Atualização de status por ID
- Exportação em `.xlsx`

**Senha do admin:** `clinica2024`
> Altere `ADMIN_PASSWORD` no `app.py` antes de publicar.

## Banco de dados

Salvo automaticamente em `agendamentos.xlsx`:

| ID | Nome | CPF | Telefone | Email | Data | Horario | Tipo | Observacoes | Recebido_em | Status |

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Repositório: [github.com/ttvzitxx-lab/clinica-saude](https://github.com/ttvzitxx-lab/clinica-saude)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Login com GitHub → **New app** → `ttvzitxx-lab/clinica-saude` → `app.py` → **Deploy**

## Estrutura

```
.
├── app.py               # Aplicação principal
├── requirements.txt     # streamlit, pandas, openpyxl
├── agendamentos.xlsx    # Banco de dados (gerado automaticamente)
└── README.md
```
