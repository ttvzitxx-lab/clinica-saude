# ClinícaVita — Central de Atendimento Médico

Sistema web de atendimento médico moderno, sem dependências externas — HTML, CSS e JavaScript puro.

## Projetos

| Arquivo | Descrição |
|---|---|
| `atendimento-medico.html` | Central de atendimento com registro de pacientes e agenda do dia |
| `declabsai.html` | Portal institucional de saúde (versão anterior) |

## atendimento-medico.html

### Funcionalidades

**Aba Atendimento**
- Registro de paciente com nome, CPF, RG, data de nascimento e sexo
- Contato: telefone/WhatsApp e e-mail
- Seleção de especialidade e convênio
- Campo de queixa principal / observações
- Máscaras automáticas em CPF, RG e telefone
- Validação de campos obrigatórios

**Aba Agendados**
- Cards de resumo: total do dia, confirmados e aguardando
- Tabela com avatar, nome, CPF, horário, especialidade, convênio e status
- Busca em tempo real por nome ou CPF
- Botão "Chamar" para atualizar status do paciente
- Novos registros aparecem automaticamente na lista

### Design

Paleta equilibrada — nem fria nem quente:
- **Verde-salva** `#3d7f6e` como cor primária
- **Âmbar** `#c8a96e` como cor de destaque
- Fundo `#f4f6f5`, superfícies brancas, sombras suaves
- Badges de status coloridos (confirmado, aguardando, realizado, cancelado)
- Relógio em tempo real e indicador de sistema online no header

### Como usar

Abra o arquivo diretamente no navegador — nenhuma instalação necessária.

```
atendimento-medico.html  →  abrir no navegador
```
