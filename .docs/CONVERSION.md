# Conversão do design para HTML/CSS/JS — Gracie Barra São Mateus

## Fonte
`Gracie Barra São Mateus.html` → extrair o conteúdo do `<script type="__bundler/template">` (JSON string). Resultado salvo como HTML de referência (ex.: `/tmp/scratchpad/template.html`).

## Passos de conversão

### 1. Extrair markup
Parsear o script `__bundler/template` e decodificar a string JSON. O resultado é o HTML do design com estilos inline.

### 2. Limpar atributos proprietários (Design Canvas)
| Atributo proprietário | Conversão |
|---|---|
| `sc-camel-view-box="0 0 24 24"` | `viewBox="0 0 24 24"` |
| `sc-camel-on-click="{{fn}}"` | `onclick="fn()"` ou listener em `app.js` (preferir JS) |
| `sc-if value="{{cond}}"` | Renderizar condicionalmente no HTML final (expandir) |
| `sc-for list="{{arr}}" as="x"` | Expandir o loop no HTML final (renderizar N itens) |
| `sc-camel-*` (outros) | remover/normalizar conforme padrão HTML |

### 3. Substituir tokens `{{...}}`
| Token | Valor |
|---|---|
| `{{red}}` | `var(--accent)` / `#D7182A` |
| `{{blue}}` | `var(--blue)` / `#0B3D91` |
| `{{wa}}` | `https://wa.me/5527999494456?text=...` |
| `{{ig}}` | `https://www.instagram.com/gbsaomateus_prof_mucio_maia/` |
| `{{maps}}` | `https://share.google/cw5yoKluPTkqPXMPN` |
| `{{filter}}`, `{{days}}`, `{{f.*}}`, `{{d.*}}`, `{{c.*}}` | Renderizar via JS a partir de `config.js` ou expandir estático |

Recomendação: renderizar a grade de horários estaticamente no HTML (para SEO) e usar JS apenas para o filtro (dimming). Links dinâmicos via `data-bind` + `config.js`.

### 4. Migrar estilos inline
- Padrões repetidos (botões, links, cards) → classes em `styles.css`.
- Estilos únicos podem permanecer inline.
- Mover `@font-face` do design para uso de Google Fonts (remover base64 de fontes).
- Manter container queries e auto-fit grids.

### 5. HTML semântico
- Adicionar `<!DOCTYPE html>`, `<html lang="pt-BR">`, `<head>` com meta tags.
- Estruturar com `header/main/section/article/figure/footer`.
- Preservar IDs de seção e `aria-*`.

### 6. Imagens
- Substituir src UUID por caminhos `assets/img/...`.
- Adicionar `width`, `height`, `alt`, `loading="lazy"` (exceto hero).

### 7. Interatividade
Implementar em `app.js`:
- Menu mobile (toggle).
- Filtro de horários (dimming por `data-kind`).
- Aplicação de links dinâmicos (`data-bind`).
- Smooth scroll (CSS).

### 8. Validação
Comparar visualmente com PNG/PDF; rodar Lighthouse; validar HTML/CSS. Ver `TESTING.md`.