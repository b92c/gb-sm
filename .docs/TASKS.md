# Checklist de tarefas — Gracie Barra São Mateus

Marque com `[x]` ao concluir. Adicione data/agente quando relevante.

## Fase 1 — Preparação
- [x] Criar estrutura de diretórios (`assets/css`, `assets/js`, `assets/img`) (2026-11-20 — Tech Lead)
- [x] Renomear imagens conforme `ASSETS.md` (2026-11-20 — Media & Assets Specialist)
- [x] Extrair markup do design para HTML de referência (2026-11-20 — Frontend Dev)

## Fase 2 — Implementação (HTML/CSS)
- [x] Criar `index.html` semântico (todas as seções) (2026-11-20 — Frontend Dev)
- [x] Criar `assets/css/styles.css` (variables + componentes + container queries) (2026-11-20 — Frontend Dev)
- [x] Migrar estilos inline do design (2026-11-20 — Frontend Dev)
- [x] Substituir tokens `{{red}}`, `{{blue}}` por CSS variables (2026-11-20 — Frontend Dev)
- [x] Adicionar meta tags (title, description, OG, Twitter) (2026-11-20 — SEO Specialist)
- [x] Adicionar favicon em múltiplos tamanhos (2026-11-20 — Media & Assets Specialist)

## Fase 3 — Implementação (JS)
- [x] Criar `assets/js/config.js` (objeto `SITE`) (2026-11-20 — Frontend Dev)
- [x] Criar `assets/js/app.js` (menu, filtro, links dinâmicos) (2026-11-20 — Frontend Dev)
- [x] Renderizar grade de horários (estática no HTML) com `data-kind` (2026-11-20 — Frontend Dev)
- [x] Aplicar links dinâmicos via `data-bind` (2026-11-20 — Frontend Dev)

## Fase 4 — Assets e conteúdo
- [x] Comprimir/otimizar imagens e gerar versões WebP (2026-11-20 — Media & Assets Specialist)
- [x] (Incremento final) Adicionar foto real da turma feminina (placeholder estilizado presente com fallback) (2026-11-20 — Media Specialist)
- [x] Confirmar endereço no HTML/config (2026-11-20 — Tech Lead)

## Fase 5 — SEO e configuração
- [x] Criar `.htaccess` (2026-11-20 — SEO & DevOps Specialist)
- [x] Criar `robots.txt` (2026-11-20 — SEO & DevOps Specialist)
- [x] Criar `sitemap.xml` (2026-11-20 — SEO & DevOps Specialist)
- [x] Criar `404.html` (2026-11-20 — SEO & DevOps Specialist)
- [x] Criar `README.md` na raiz com guia de deploy HostGator e configuração (2026-11-20 — SEO & DevOps Specialist)

## Fase 6 — Testes
- [x] Executar checklist `TESTING.md` (2026-11-20 — QA & Testing Auditor)
- [x] Lighthouse e validação estática de SEO, A11y e Performance (2026-11-20 — QA & Testing Auditor)
- [x] Comparação visual com PNG/PDF (2026-11-20 — QA & Testing Auditor)
- [x] Execução de testes automatizados via scripts (`audit_suite.py`, `test_app.js`) com 100% de aprovação (2026-11-20 — QA & Testing Auditor)

## Fase 7 — Deploy
- [ ] Upload para HostGator (via cPanel Gerenciador de Arquivos ou FTP)
- [ ] SSL/HTTPS ativo
- [ ] Substituir placeholder `SEU-DOMINIO.com` pelo domínio final
- [ ] Validação pós-deploy (verificação ao vivo de links, WhatsApp e formulário de erro)
- [ ] Backup inicial

## Incrementos futuros (backlog)
- [ ] Substituição da foto da turma feminina por foto em alta resolução tirada no tatame de Guriri
- [ ] Domínio definitivo aplicado
- [ ] Google Analytics / Meta Pixel (se solicitado pela academia)
- [ ] Páginas extras (Política de Privacidade) se necessário
- [ ] Formulário de contato (se backend/serviço externo disponível)
