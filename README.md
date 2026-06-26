# 🏥 Telemedicina — Portal de Saúde

Plataforma institucional de agendamentos médicos com visual de sistema público, cores verde e amarelo, painel administrativo completo e banco de dados em Excel. Construído com **Streamlit**.

## Informações da clínica

| Campo | Informação |
|---|---|
| **Nome** | Telemedicina |
| **Telefone** | (11) 93307-537 |
| **WhatsApp** | (11) 93307-537 — 24/7 |
| **E-mail** | contato@telemedicina.com |
| **Endereço** | 8701 Charleville Blvd, Beverly Hills, CA 90211 |
| **Horário** | 24/7 |

## Design

Visual inspirado em portais institucionais públicos de saúde:
- **Barra superior** com identificação do portal e badge "24/7"
- **Header institucional** com logo, nome, data e indicador de sistema online
- **Alerta amarelo** com instruções ao paciente
- **Breadcrumb** de navegação
- **Painel hero** verde escuro com destaque amarelo
- **Sidebar verde escura** com borda amarela
- Protocolo numerado gerado ao agendar (`#0001`, `#0002`...)

## Funcionalidades

### Área do paciente
- Página inicial com painel institucional e cards de serviços
- Formulário de agendamento com CPF validado e geração de protocolo
- Página de contato com formulário de mensagem

### Área administrativa (`🔒 Área restrita`)
- Login com senha
- Métricas: Total, Aguardando, Confirmados, Cancelados
- Tabela completa de pacientes
- Filtro por status
- Atualização de status por protocolo (ID)
- Exportação em `.xlsx`

**Senha do admin:** `clinica2024`
> Altere `ADMIN_PASSWORD` no `app.py` antes de publicar.

### Gestão de Contratos (`📄 Contratos`)

Módulo completo para leitura e rastreamento de documentos contratuais, com 6 abas:

| Aba | Descrição |
|-----|-----------|
| ⏳ **Pendentes** | Contratos aguardando leitura, com alerta de urgência para prioridade Alta |
| 🔍 **Em Revisão** | Contratos em processo de análise |
| ✅ **Lidos** | Histórico de contratos lidos — registra quem leu e quando |
| 🗄️ **Arquivados** | Contratos encerrados ou arquivados |
| 📋 **Todos** | Visão geral com gráficos por status/tipo e exportação Excel |
| ➕ **Novo Contrato** | Formulário de cadastro com upload de arquivo (PDF, DOCX, etc.) |

Cada contrato possui: filtros por tipo/prioridade/busca, observações editáveis, download do arquivo, troca de status e exclusão. O contador de cada aba é atualizado em tempo real.

## Banco de dados

**Agendamentos** — salvo em `agendamentos.xlsx`:

| ID | Nome | CPF | Telefone | Email | Data | Horario | Tipo | Observacoes | Recebido_em | Status |

**Contratos** — salvo em `contratos.xlsx` + arquivos em `contratos_uploads/`:

| ID | Nome | Tipo | Parte_A | Parte_B | Status | Prioridade | Adicionado_em | Lido_em | Lido_por | Arquivo | Tags |

## Como rodar localmente

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Repositório: [github.com/ttvzitxx-lab/clinica-saude](https://github.com/ttvzitxx-lab/clinica-saude)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Login com GitHub → **New app** → `ttvzitxx-lab/clinica-saude` → `app.py` → **Deploy**

## Estrutura

```
.
├── app.py                  # Aplicação principal
├── contracts_backend.py    # Backend de gestão de contratos
├── requirements.txt        # streamlit, pandas, openpyxl
├── agendamentos.xlsx       # Banco de agendamentos (gerado automaticamente)
├── contratos.xlsx          # Banco de contratos (gerado automaticamente)
├── contratos_uploads/      # Arquivos enviados nos contratos
└── README.md
```
