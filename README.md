# ClinícaVita — Central de Atendimento Médico

Sistema web de atendimento médico moderno com interface Streamlit e versão HTML standalone.

## 🚀 Acesso ao sistema

**👉 [https://clinica-saude.streamlit.app](https://clinica-saude.streamlit.app)**

> Deploy via [Streamlit Community Cloud](https://share.streamlit.io) — repositório: `ttvzitxx-lab/clinica-saude`

---

## Projetos

| Arquivo | Descrição |
|---|---|
| `app.py` | Interface Streamlit — atendimento, agenda e gerenciamento |
| `atendimento-medico.html` | Versão HTML standalone (sem dependências) |

---

## app.py — Interface Streamlit

### Abas

**📋 Atendimento**
- Registro de paciente: nome, CPF, RG, data de nascimento, sexo
- Contato: telefone/WhatsApp e e-mail
- Especialidade e convênio
- Campo de queixa / observações
- Geração automática de protocolo (`#0001`, `#0002`...)
- Validação de campos obrigatórios

**📅 Agendados**
- Métricas do dia: total, confirmados, aguardando, realizados
- Tabela com badges de status coloridos
- Busca em tempo real por nome ou CPF
- Filtro por status
- Exportação em `.xlsx`

**⚙️ Gerenciar**
- Atualização de status por protocolo
- Visualização completa de todos os registros

### Banco de dados

Salvo automaticamente em `atendimentos.xlsx`:

| ID | Nome | CPF | RG | Nascimento | Sexo | Telefone | Email | Especialidade | Convenio | Queixa | Data | Hora | Status |

### Design

- Sidebar escura `#1e2d28` com navegação lateral
- Verde-salva `#3d7f6e` como cor primária
- Badges de status: aguardando (âmbar), confirmado (verde), realizado (azul), cancelado (vermelho)

---

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Login com GitHub → **New app**
3. Repositório: `ttvzitxx-lab/clinica-saude` → arquivo: `app.py`
4. Clique em **Deploy**

## Estrutura

```
.
├── app.py                   # Interface Streamlit principal
├── atendimento-medico.html  # Versão HTML standalone
├── requirements.txt         # streamlit, pandas, openpyxl
├── atendimentos.xlsx        # Banco de dados (gerado automaticamente)
└── README.md
```
