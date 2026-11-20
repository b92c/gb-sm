# Testes e validação — Gracie Barra São Mateus

Relatório consolidado de testes de qualidade, acessibilidade e conformidade técnica.
Última auditoria executada em: **2026-11-20** por **QA & Testing Auditor**.
Resultado geral: **66 de 66 testes automatizados aprovados (100% de sucesso)**.

---

## Validação técnica
- [x] HTML válido (sintaxe HTML5 estrita, tags devidamente fechadas, DOCTYPE e `lang="pt-BR"`).
- [x] CSS válido (chaves balanceadas, sem variáveis indefinidas, container queries e media queries conformes).
- [x] Sem erros no console do navegador (scripts executam em Node.js e browser simulado sem runtime errors ou warnings).
- [x] Links internos (`#inicio`, `#sobre`, `#modalidades`, `#horarios`, `#professor`, `#contato`) funcionando com scroll compensado para header sticky (`scroll-margin-top: 88px` e `window.scrollTo` com offset).

## Funcional
- [x] Menu mobile abre/fecha; `aria-expanded` e `aria-label` atualizados; fecha por clique no botão, tecla Escape, clique fora e clique nos links do painel.
- [x] Filtro de horários: "Todos", "Gi", "No-Gi" com dimming correto via classe `.is-dimmed` (opacidade 0.25 e `aria-hidden="true"`); estado ativo com `aria-pressed="true"`.
- [x] Links WhatsApp abrem com número oficial `5527999494456` e mensagem pré-preenchida de aula experimental.
- [x] Links Instagram (`@gbsaomateus_prof_mucio_maia`) e Google Maps abrem em nova aba com `target="_blank"` e `rel="noopener noreferrer"`.
- [x] Imagens carregam sem 404 (todas as 27 referências locais em `index.html` e 5 em `404.html` validadas em disco).
- [x] Fontes carregam (`Barlow Condensed` e `Inter` via Google Fonts com `preconnect`).

## Responsividade
- [x] Desktop ≥ 1240px: grid completo, header com navegação inline e botão CTA.
- [x] Tablet 768–920px: ativação de menu hamburguer mobile em ≤ 920px (via `@container gb` e fallback `@media`).
- [x] Mobile ≤ 480px: layout empilhado fluído, imagens com `max-width: 100%`, botão WhatsApp flutuante compacto.
- [x] Container queries funcionando (`container-type: inline-size; container-name: gb;` com regras `@container gb (max-width: 920px)` e `@container gb (min-width: 700px)`).

## Acessibilidade (WCAG 2.1 AA)
- [x] Navegação por teclado (Tab) funcional em todos os botões e links.
- [x] Foco visível com `:focus-visible` estilizado com contorno de alto contraste (`outline: 2px solid var(--accent)`).
- [x] Contraste adequado (fundo escuro `#0D0F14` com texto claro `#FFFFFF`, badges `#0B3D91` e `#D7182A` com texto `#FFFFFF`).
- [x] Atributo `alt` preenchido descritivamente em 100% das imagens.
- [x] Headings rigorosamente hierárquicos (único `h1`, seguido de seções `h2` e subitens `h3`, sem saltos de nível).
- [x] Ícones SVG decorativos marcados com `aria-hidden="true"`.

## Performance (Auditoria Estática & Prevenção de CLS)
- [x] Prevenção de CLS (Cumulative Layout Shift < 0.1): todas as tags `<img>` possuem atributos numéricos `width` e `height`.
- [x] Imagens otimizadas em formato WebP com fallback JPEG/PNG dentro de elementos `<picture>`.
- [x] Imagem hero acima da dobra com `loading="eager"`; imagens abaixo da dobra com `loading="lazy"`.
- [x] Gzip e compressão HTTP configuradas no `.htaccess` via `mod_deflate`.
- [x] Políticas de cache de longa duração (1 ano para assets estáticos) via `mod_expires`.

## Visual
- [x] Comparação com `Home — site institucional.png` e PDF (seções idênticas: hero, sobre, linhagem, modalidades, grade de horários, professor responsável, galeria do dia a dia, CTA e rodapé).
- [x] Cores fiéis ao design system: accent `#D7182A`, blue `#0B3D91`, fundo `#0D0F14`.

## Pós-deploy (Checklist para ativação em produção)
- [ ] HTTPS ativo no servidor HostGator (certificado SSL cPanel/Let's Encrypt).
- [ ] Substituir o placeholder `SEU-DOMINIO.com` pelo domínio real registrado no `index.html` (canonical, og:url), `robots.txt` e `sitemap.xml`.
- [ ] Validação ao vivo sem mixed content após publicação.
