# Guia para agentes colaboradores — Gracie Barra São Mateus

Este projeto pode ser atuado por **múltiplos agentes de múltiplos providers**. Siga estas regras para manter consistência e evitar conflitos.

## Antes de começar
1. Leia `.docs/README.md`, `.docs/PLAN.md` e `.docs/AGENTS.md`.
2. Consulte `.docs/TASKS.md` para identificar tarefas pendentes.
3. Consulte `.docs/DECISIONS.md` para decisões já tomadas — não reverter sem registrar nova decisão.

## Regras de colaboração
- **Não modifique arquivos fora da estrutura** definida em `STRUCTURE.md` sem documentar.
- **Não altere decisões resolvidas** sem registrar em `DECISIONS.md`.
- **Marque tarefas concluídas** em `TASKS.md` (checkbox + data + agente/provider).
- **Mantenha o design original**: reproduzir fielmente o design fornecido; não inventar novas seções.
- **Sem backend/banco**: apenas frontend estático.
- **Contato apenas via WhatsApp**: não adicionar formulários ou outros canais.
- **Fácil ajuste**: manter dados variáveis em `config.js`; não hardcode valores repetidos.

## Convenções de código
- Indentação: 2 espaços (HTML/CSS/JS).
- Idioma do conteúdo: português (pt-BR).
- Commits (se aplicável): mensagens em português, descritivas.
- Não introduzir dependências/build tools.

## Comunicação entre agentes
- Atualize `TASKS.md` ao concluir.
- Registre decisões novas em `DECISIONS.md`.
- Se encontrar bloqueio (ex.: falta de asset), anote em `TASKS.md` como pendente e siga.

## Checklist rápido antes de finalizar uma alteração
- [ ] Estrutura respeitada
- [ ] Sem erros de console
- [ ] Responsivo (mobile/tablet/desktop)
- [ ] Links e imagens funcionando
- [ ] `TASKS.md` atualizado