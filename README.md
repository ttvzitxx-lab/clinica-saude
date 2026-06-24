# ✚ Telemedicina — Sistema de Agendamentos

App completo para clínicas médicas com design premium inspirado em marcas de luxo, agendamento online e painel administrativo. Construído com **Streamlit**.

## Informações da clínica

- **Nome:** Telemedicina
- **Telefone:** (11) 93307-537
- **WhatsApp:** (11) 93307-537 — 24/7
- **E-mail:** contato@telemedicina.com
- **Endereço:** 8701 Charleville Blvd, Beverly Hills, CA 90211, EUA
- **Horário:** 24/7

## Funcionalidades

### Área do paciente
- Página inicial com design premium (fundo preto, tipografia elegante)
- Cards de serviços em grade estilo editorial
- Formulário de agendamento com captura de: Nome, CPF, Telefone, E-mail, Data, Horário, Tipo de consulta e Observações
- Validação de CPF em tempo real
- Seção de contato com formulário de mensagem

### Área administrativa (`ÁREA ADMINISTRATIVA`)
- Login com senha protegida
- Métricas de agendamentos (total, aguardando, confirmados)
- Tabela completa de pacientes e consultas
- Filtro por status (Aguardando / Confirmado / Cancelado)
- Atualização de status por ID
- Exportação da planilha completa em `.xlsx`

**Senha do admin:** `clinica2024`
> Altere a variável `ADMIN_PASSWORD` no `app.py` antes de publicar.

## Banco de dados

Os agendamentos são salvos automaticamente em `agendamentos.xlsx` com as colunas:

| ID | Nome | CPF | Telefone | Email | Data | Horario | Tipo | Observacoes | Recebido_em | Status |

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como publicar no Streamlit Cloud (link público gratuito)

1. Repositório já disponível em: [github.com/ttvzitxx-lab/clinica-saude](https://github.com/ttvzitxx-lab/clinica-saude)
2. Acesse [share.streamlit.io](https://share.streamlit.io) e faça login com o GitHub
3. Clique em **"New app"** → selecione `ttvzitxx-lab/clinica-saude` → entry point: `app.py`
4. Clique em **Deploy**

## Estrutura

```
.
├── app.py               # Aplicação principal
├── requirements.txt     # Dependências (streamlit, pandas, openpyxl)
├── agendamentos.xlsx    # Criado automaticamente ao primeiro agendamento
└── README.md
```

## Personalização

Edite `app.py` para alterar:
- `ADMIN_PASSWORD` — senha do painel admin
- Nome, endereço, telefone e e-mail da clínica
- Serviços oferecidos
- Cores e tipografia (seção `<style>`)
