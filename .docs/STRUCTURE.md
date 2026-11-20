# Estrutura de diretórios e convenções — Gracie Barra São Mateus

## Árvore final

```
gb-sm/
├── index.html                 # página principal (SPA)
├── 404.html                   # página de erro
├── assets/
│   ├── css/
│   │   └── styles.css         # estilos globais + componentes
│   ├── js/
│   │   ├── config.js          # dados centralizados (SITE)
│   │   └── app.js             # interações
│   └── img/
│       ├── logo.png
│       ├── hero-academia.jpg
│       ├── modalidade-gi.jpg
│       ├── modalidade-nogi.jpg
│       ├── modalidade-kids.jpg
│       ├── modalidade-feminina.jpg   # placeholder (incremento final)
│       ├── professor-mucio.jpg
│       └── sede-guriri.jpg
├── .htaccess
├── robots.txt
├── sitemap.xml
└── README.md
```

## Convenções

### Nomes de arquivo
- Minúsculos, kebab-case, sem acentos (`modalidade-gi.jpg`).
- Sem UUIDs no nome final.
- Imagens: `jpg` para fotos, `png` para logo/ícones com transparência.

### CSS
- Arquivo único `assets/css/styles.css`.
- CSS custom properties em `:root` para tema:
  - `--accent: #D7182A; --blue: #0B3D91;`
  - `--bg: #0D0F14; --surface: #151925; --card: #FFFFFF;`
  - `--text: #11141B; --muted: #3A4150; --muted-light: #A9B0BE;`
  - `--border: #222838; --border-light: #E1E4EA;`
- Classes reutilizáveis do design: `.gb-root`, `.gb-link`, `.gb-btn`, `.gb-nav`, `.gb-menu-btn`, `.gb-mobile-panel`, `.gb-span2`.
- Container queries preservadas (`@container gb (max-width: 920px)` etc.).
- Evitar `!important` exceto overrides de responsividade já no design.

### JavaScript
- `config.js` define `window.SITE = {...}` (sem módulos ES, para compatibilidade ampla).
- `app.js` consome `window.SITE` e manipula DOM no `DOMContentLoaded`.
- Sem dependências externas.

### HTML
- Semântico, `lang="pt-BR"`.
- IDs de seção: `#inicio`, `#sobre`, `#modalidades`, `#horarios`, `#professor`, `#contato`.
- Header sticky com `scroll-margin-top: 88px` nos alvos.

### Imagens
- `loading="lazy"` exceto hero (eager).
- Sempre `width`/`height` + `alt` descritivo.
- Formato WebP opcional com `<picture>` (fallback JPEG).

### Arquivos de configuração (HostGator)
- `.htaccess` na raiz de `public_html`.
- `robots.txt` e `sitemap.xml` na raiz.