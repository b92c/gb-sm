# Mapeamento e otimização de assets — Gracie Barra São Mateus

## Mapeamento UUID → nome semântico

| UUID (manifest) | Novo nome | Uso |
|---|---|---|
| `ca0e79d0-250d-48b7-ac8d-94211e49405c` | `assets/img/logo.png` | Logo navbar/footer |
| `473c675b-69f4-4686-a453-5e14c1da3e84` | `assets/img/hero-academia.jpg` | Hero (1206×500) |
| `1c8ca2e8-5479-47d7-a1bb-27933d69289c` | `assets/img/modalidade-gi.jpg` | Card Gi |
| `40b24039-ea10-477d-b9bf-834de45e5710` | `assets/img/modalidade-nogi.jpg` | Card No-Gi + galeria |
| `452ae0e7-488c-4011-9bb8-85f97dddac56` | `assets/img/modalidade-kids.jpg` | Card Kids + galeria |
| (placeholder) | `assets/img/modalidade-feminina.jpg` | Card Feminina (incremento final) |
| `1c788475-760a-41fc-9e9f-3f5e7c208376` | `assets/img/professor-mucio.jpg` | Seção professor (3:5) |
| `ae6d6375-130e-4b37-b9f8-02c760660532` | `assets/img/sede-guriri.jpg` | Contato (fachada) |

As imagens já foram extraídas do manifest para `assets/img/` com os nomes UUID; renomear conforme tabela.

## Fontes
- Barlow Condensed (600/700/800) e Inter (400/500/600/700) via Google Fonts (`<link>`), não base64.
- URL: `https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap`.

## Otimização (antes do deploy)
- Comprimir JPEGs (hero ≤ 200KB; cards ≤ 120KB; professor ≤ 150KB).
- Gerar WebP com fallback JPEG via `<picture>` (opcional, recomendado).
- Favicon 32×32 e 180×180 (apple-touch-icon) a partir do logo.
- Imagem OG 1200×630 (pode reusar hero recortado/branding).
- Lazy loading em todas exceto hero.

## Localização no design
- Logo: navbar (48×48) e footer (56×56).
- Hero: `aspect-ratio: 1206/500`, `object-fit: cover`, `object-position: 30% 50%`.
- Cards modalidades: `aspect-ratio: 4/3`.
- Professor: `aspect-ratio: 3/5`, `object-position: 50% 0%`.
- Sede: `object-fit: cover`, `object-position: 50% 30%`.

## Tabela final de assets gerados e otimizados (Status: 100% Concluído)

| Arquivo | Dimensões | Formato | Tamanho (Bytes) | Tamanho (KB) | Meta / Limite | Status |
|---|---|---|---|---|---|---|
| `assets/img/logo.png` | 256×256 | PNG (RGBA) | 87.706 B | 85.7 KB | Navbar / Footer | OK |
| `assets/img/logo.webp` | 256×256 | WebP (Lossless) | 67.296 B | 65.7 KB | Next-gen `<picture>` | OK |
| `assets/img/hero-academia.jpg` | 1206×500 | JPEG | 118.428 B | 115.7 KB | ≤ 200 KB | OK |
| `assets/img/hero-academia.webp` | 1206×500 | WebP | 81.068 B | 79.2 KB | ≤ 100 KB | OK |
| `assets/img/modalidade-gi.jpg` | 600×450 | JPEG | 59.642 B | 58.2 KB | ≤ 120 KB | OK |
| `assets/img/modalidade-gi.webp` | 600×450 | WebP | 43.818 B | 42.8 KB | ≤ 60 KB | OK |
| `assets/img/modalidade-nogi.jpg` | 1316×765 | JPEG | 84.840 B | 82.9 KB | ≤ 120 KB | OK |
| `assets/img/modalidade-nogi.webp` | 1316×765 | WebP | 43.176 B | 42.2 KB | ≤ 60 KB | OK |
| `assets/img/modalidade-kids.jpg` | 720×480 | JPEG | 64.376 B | 62.9 KB | ≤ 120 KB | OK (otimizado de 263KB) |
| `assets/img/modalidade-kids.webp` | 720×480 | WebP | 57.480 B | 56.1 KB | ≤ 60 KB | OK |
| `assets/img/modalidade-feminina.jpg` | 800×600 | JPEG | 60.146 B | 58.7 KB | ≤ 120 KB | OK (placeholder institucional) |
| `assets/img/modalidade-feminina.webp` | 800×600 | WebP | 22.112 B | 21.6 KB | ≤ 40 KB | OK |
| `assets/img/professor-mucio.jpg` | 454×1090 | JPEG | 84.419 B | 82.4 KB | ≤ 150 KB | OK |
| `assets/img/professor-mucio.webp` | 454×1090 | WebP | 44.196 B | 43.2 KB | ≤ 80 KB | OK |
| `assets/img/sede-guriri.jpg` | 880×495 | JPEG | 104.714 B | 102.3 KB | ≤ 120 KB | OK |
| `assets/img/sede-guriri.webp` | 880×495 | WebP | 68.406 B | 66.8 KB | ≤ 80 KB | OK |
| `assets/img/og-image.jpg` | 1200×630 | JPEG | 134.423 B | 131.3 KB | ≤ 200 KB | OK (Hero + Branding) |
| `assets/img/og-image.webp` | 1200×630 | WebP | 56.018 B | 54.7 KB | ≤ 80 KB | OK |
| `favicon.png` / `assets/img/favicon.png` | 32×32 | PNG | 2.708 B | 2.6 KB | Raiz + assets/img/ | OK |
| `apple-touch-icon.png` / `assets/img/apple-touch-icon.png` | 180×180 | PNG | 52.036 B | 50.8 KB | Raiz + assets/img/ | OK |
| `favicon.ico` / `assets/img/favicon.ico` | 32×32 | ICO | 4.414 B | 4.3 KB | Raiz + assets/img/ | OK |
| `favicon-16x16.png` / `assets/img/favicon-16x16.png` | 16×16 | PNG | 1.001 B | 1.0 KB | Raiz + assets/img/ | OK |
| `favicon-32x32.png` / `assets/img/favicon-32x32.png` | 32×32 | PNG | 2.708 B | 2.6 KB | Raiz + assets/img/ | OK |
