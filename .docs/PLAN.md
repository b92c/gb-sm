# Plano de criação do site institucional — Gracie Barra São Mateus

## 1. Resumo
Criar um site estático (HTML/CSS/JS puro) para a **Gracie Barra São Mateus (Guriri – ES)**, reproduzindo fielmente o design fornecido (`Gracie Barra São Mateus.html` + print/PDF), hospedável em servidor compartilhado HostGator, sem backend/banco de dados, com contato exclusivo via WhatsApp. Arquitetura pensada para facilitar ajustes futuros (textos, horários, cores, contatos) por pessoas não-desenvolvedoras.

## 2. Análise dos arquivos base
| Arquivo | Uso |
|---|---|
| `Gracie Barra São Mateus.html` | Design exportado do "Design Canvas" (React/DCLogic). Contém todo o markup, estilos inline, imagens em base64 (manifest), e a lógica de interação (filtros de horários, menu mobile). **Fonte principal de design.** |
| `Gracie Barra São Mateus (1).pdf` | Renderização/print do mesmo design (5 páginas). Serve como referência visual e checklist de conteúdo. |
| `Home — site institucional.png` | Screenshot da home. Referência visual para validação final. |

**Conteúdo extraído do design:** hero "Jiu-Jitsu para todos", destaques, "Nossa linhagem" (timeline 1986/1995/hoje), 4 modalidades (Gi, No-Gi, Kids, Feminina), grade semanal de horários, professor Mestre Múcio Maia + conquistas, galeria, CTA "aula experimental", contato (WhatsApp, Instagram, endereço placeholder, aulas), footer.

**Dados-chave:** WhatsApp `(27) 99949-4456` · Instagram `@gbsaomateus_prof_mucio_maia` · Maps link disponível · Cores: accent `#D7182A`, blue `#0B3D91`, fundo `#0D0F14`. Fontes: Barlow Condensed + Inter (Google Fonts).

**Placeholders a resolver:** endereço `[Rua e número]`; foto da turma feminina (hoje placeholder).

## 3. Objetivos e requisitos
- Reproduzir o design pixel-a-pixel (responsivo, container queries já presentes).
- Zero backend: site 100% estático.
- Contato via WhatsApp (link `wa.me` com mensagem pré-preenchida).
- Fácil ajuste/atualização: centralizar dados variáveis; documentar onde editar.
- Deploy simples em HostGator (upload de arquivos).
- SEO básico, acessibilidade, performance (imagens otimizadas).

## 4. Arquitetura e tecnologias
- **HTML5** semântico (`header`, `nav`, `main`, `section`, `article`, `figure`, `footer`).
- **CSS3** (arquivo `assets/css/styles.css`) com **CSS custom properties** para cores/spacing; manter os estilos inline do design migrados para classes quando repetidos, ou manter inline quando pontuais. Container queries (`@container`) preservadas.
- **JavaScript vanilla** (`assets/js/app.js`) para: menu mobile, filtro de horários, aplicação de dados do `config.js` (contatos/links), smooth scroll.
- **Google Fonts** (Barlow Condensed 600/700/800, Inter 400/500/600/700) via `<link>` (sem base64 de fontes).
- **Sem build tools / bundler** → editar e publicar direto; ideal para HostGator.
- Opcional: Tailwind CDN (não recomendado — CSS puro dá mais controle e menos dependência).
- Imagens em `assets/img/` (extraídas do manifest; renomeadas para nomes semânticos).

## 5. Estrutura de diretórios
Ver `STRUCTURE.md` para detalhes. Resumo:
```
gb-sm/
├── index.html
├── 404.html
├── assets/{css,js,img}/
├── .htaccess
├── robots.txt
├── sitemap.xml
└── README.md
```

## 6. Mapeamento de assets
Ver `ASSETS.md`. UUIDs do manifest → nomes semânticos.

## 7. Conversão do design (HTML/CSS/JS)
Ver `CONVERSION.md`. Inclui limpeza de atributos proprietários (`sc-camel-*`, `sc-if`, `sc-for`), substituição de tokens `{{...}}`, migração de estilos inline, CSS variables, imagens otimizadas.

## 8. Interatividade (app.js)
- **Menu mobile:** toggle classe `.is-open` no header; CSS controla exibição do painel; `aria-expanded` atualizado.
- **Filtro de horários:** botões `data-filter="todos|gi|nogi"`; ao clicar, aplicar classe `.is-dimmed` (opacity .25) nas aulas cujo `data-kind` não corresponde; atualizar `aria-pressed` e estilos do botão ativo.
- **Links dinâmicos:** `config.js` fornece WhatsApp/Instagram/Maps; `app.js` aplica a elementos `[data-bind="wa|ig|maps"]` no `DOMContentLoaded`.
- **Smooth scroll** via CSS `scroll-behavior: smooth`; `scroll-margin-top` para header sticky.

## 9. Dados centralizados (config.js)
Objeto `SITE` com: `brand`, `theme`, `contact` (whatsapp number + mensagem, instagram, address, mapsUrl), `schedule` (days/classes), `content` (textos editáveis). Textos longos (sobre, professor) permanecem no HTML (SEO + edição simples); apenas dados repetidos/variáveis no config.

## 10. SEO, acessibilidade e performance
- `<title>`, meta description, Open Graph (imagem 1200×630), Twitter Card.
- `lang="pt-BR"`, headings hierárquicos, `aria-label`/`aria-pressed`, foco visível.
- Favicon (a partir do logo).
- Compressão de imagens (hero ≤ 200KB), formatos modernos (WebP com fallback JPEG).
- `.htaccess`: `mod_deflate`, cache de assets (1 ano para img/css/js), redirect HTTP→HTTPS, www opcional, página 404.
- `robots.txt` + `sitemap.xml`.

## 11. Deploy HostGator
Ver `DEPLOY.md`.

## 12. Testes e validação
Ver `TESTING.md`.

## 13. Cronograma (estimativa)
| Etapa | Duração |
|---|---|
| 1. Extração/limpeza do markup + assets | 0.5 dia |
| 2. HTML semântico + CSS (design) | 1.5 dias |
| 3. JS (interações) + config.js | 0.5 dia |
| 4. SEO/a11y/performance | 0.5 dia |
| 5. Testes + ajustes | 0.5 dia |
| 6. Deploy HostGator + validação | 0.5 dia |
| **Total** | **~4 dias** |

## 14. Decisões (resumo)
Ver `DECISIONS.md`. Resolvidas: endereço completo; WhatsApp confirmado; sem GA/Pixel; sem LGPD; SPA; foto feminina como incremento final; domínio em aberto.

## 15. Próximos passos
Implementar conforme `TASKS.md`, começando pela extração/limpeza e criação da estrutura. Ao concluir, validar com `TESTING.md` e publicar conforme `DEPLOY.md`.