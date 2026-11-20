# Documentação do projeto — Gracie Barra São Mateus

Este diretório (`.docs/`) contém o plano, decisões e guias técnicos do site institucional da **Gracie Barra São Mateus (Guriri – ES)**. Foi criado para permitir que **múltiplos agentes de múltiplos providers** atuem de forma independente, com contexto compartilhado e consistente.

## Índice

| Arquivo | Conteúdo |
|---|---|
| [`PLAN.md`](./PLAN.md) | Plano completo de criação do site |
| [`DECISIONS.md`](./DECISIONS.md) | Decisões de projeto resolvidas e pendentes |
| [`STRUCTURE.md`](./STRUCTURE.md) | Estrutura de diretórios e convenções |
| [`ASSETS.md`](./ASSETS.md) | Mapeamento e otimização de assets |
| [`CONVERSION.md`](./CONVERSION.md) | Conversão do design (HTML/CSS/JS) |
| [`DEPLOY.md`](./DEPLOY.md) | Deploy em HostGator (shared hosting) |
| [`TESTING.md`](./TESTING.md) | Testes e validação |
| [`TASKS.md`](./TASKS.md) | Checklist de tarefas com status |
| [`AGENTS.md`](./AGENTS.md) | Guia para agentes colaboradores |

## Como usar (agentes)

1. Leia `AGENTS.md` e `PLAN.md` antes de qualquer alteração.
2. Consulte `TASKS.md` para saber o que já foi feito e o que falta.
3. Ao concluir uma tarefa, marque-a em `TASKS.md` (checkbox + data/agente).
4. Registre decisões novas em `DECISIONS.md`.
5. Mantenha a estrutura definida em `STRUCTURE.md`; não crie arquivos fora dela sem documentar.

## Fontes de design (raiz do projeto)

- `Gracie Barra São Mateus.html` — design exportado (fonte principal).
- `Gracie Barra São Mateus (1).pdf` — renderização/print de referência.
- `Home — site institucional.png` — screenshot de referência.

## Status geral

- **Fase atual:** Planejamento concluído → pronto para implementação.
- **Stack:** HTML5 + CSS3 + JS vanilla (sem backend/banco).
- **Hospedagem:** HostGator shared (frontend estático).