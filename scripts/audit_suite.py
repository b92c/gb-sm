#!/usr/bin/env python3
"""
Audit & Testing Suite — Gracie Barra São Mateus
Validates all items from .docs/TESTING.md, .docs/PLAN.md, and project requirements.
"""

import os
import sys
import re
import subprocess
import html.parser
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

class HTMLValidator(html.parser.HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.stack = []
        self.void_elements = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }
        self.errors = []
        self.ids = set()
        self.links = []
        self.images = []
        self.pictures = []
        self.current_picture = None
        self.headings = []
        self.current_heading = None
        self.current_heading_text = []
        self.svgs = []
        self.buttons = []
        self.metas = []
        self.link_tags = []
        self.scripts = []
        self.data_filters = []
        self.data_kinds = []
        self.data_binds = []
        self.classes = set()

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        pos = self.getpos()

        # Check tag stack
        if tag.lower() not in self.void_elements:
            self.stack.append((tag.lower(), pos))

        # Collect classes
        if 'class' in attr_dict:
            for c in attr_dict['class'].split():
                self.classes.add(c)

        # Collect IDs
        if 'id' in attr_dict:
            if attr_dict['id'] in self.ids:
                self.errors.append(f"Duplicate ID '{attr_dict['id']}' at line {pos[0]}")
            self.ids.add(attr_dict['id'])

        # Collect links
        if tag == 'a':
            self.links.append((attr_dict, pos))

        # Collect images & picture
        if tag == 'picture':
            self.current_picture = {'sources': [], 'img': None, 'pos': pos}
        elif tag == 'source' and self.current_picture is not None:
            self.current_picture['sources'].append((attr_dict, pos))
        elif tag == 'img':
            self.images.append((attr_dict, pos))
            if self.current_picture is not None:
                self.current_picture['img'] = (attr_dict, pos)

        # Collect headings
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self.current_heading = (tag, pos)
            self.current_heading_text = []

        # Collect SVGs
        if tag == 'svg':
            self.svgs.append((attr_dict, pos))

        # Collect buttons
        if tag == 'button':
            self.buttons.append((attr_dict, pos))

        # Collect meta & link tags
        if tag == 'meta':
            self.metas.append((attr_dict, pos))
        if tag == 'link':
            self.link_tags.append((attr_dict, pos))

        # Collect scripts
        if tag == 'script':
            self.scripts.append((attr_dict, pos))

        # Interactive attributes
        if 'data-filter' in attr_dict:
            self.data_filters.append((tag, attr_dict, pos))
        if 'data-kind' in attr_dict:
            self.data_kinds.append((tag, attr_dict, pos))
        if 'data-bind' in attr_dict:
            self.data_binds.append((tag, attr_dict, pos))

    def handle_data(self, data):
        if self.current_heading:
            self.current_heading_text.append(data.strip())

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag == 'picture' and self.current_picture is not None:
            self.pictures.append(self.current_picture)
            self.current_picture = None

        if self.current_heading and tag == self.current_heading[0]:
            h_text = ' '.join([t for t in self.current_heading_text if t])
            self.headings.append((self.current_heading[0], h_text, self.current_heading[1]))
            self.current_heading = None
            self.current_heading_text = []

        if tag_lower in self.void_elements:
            self.errors.append(f"End tag for void element <{tag}> at line {self.getpos()[0]}")
            return

        if not self.stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]} (empty stack)")
            return

        last_tag, pos = self.stack[-1]
        if last_tag == tag_lower:
            self.stack.pop()
        else:
            stack_tags = [t[0] for t in self.stack]
            if tag_lower in stack_tags:
                idx = len(self.stack) - 1 - stack_tags[::-1].index(tag_lower)
                unclosed = self.stack[idx+1:]
                for ut, up in unclosed:
                    self.errors.append(f"Unclosed tag <{ut}> opened at line {up[0]} before </{tag}> at line {self.getpos()[0]}")
                self.stack = self.stack[:idx]
            else:
                self.errors.append(f"Mismatched closing tag </{tag}> at line {self.getpos()[0]} (expected </{last_tag}> from line {pos[0]})")

    def validate(self):
        with open(self.filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for unreplaced template tokens
        curly_matches = re.findall(r'\{\{[^}]*\}\}', content)
        if curly_matches:
            self.errors.append(f"Found unreplaced tokens {curly_matches[:5]} in {self.filename}")

        sc_matches = re.findall(r'\bsc-[a-zA-Z0-9_-]+', content)
        if sc_matches:
            self.errors.append(f"Found proprietary sc-* attributes {sc_matches[:5]} in {self.filename}")

        self.feed(content)

        for tag, pos in self.stack:
            self.errors.append(f"Unclosed tag <{tag}> opened at line {pos[0]}")

        return self.errors


def run_audit():
    print("=" * 70)
    print("GRACIE BARRA SÃO MATEUS — RELATÓRIO DE AUDITORIA & TESTES (QA)")
    print("=" * 70)

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    def test(name, condition, error_detail=""):
        nonlocal total_tests, passed_tests, failed_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name}")
        else:
            failed_tests.append((name, error_detail))
            print(f"  [FAIL] {name} => {error_detail}")

    # =========================================================================
    # SEÇÃO 1: VALIDAÇÃO TÉCNICA
    # =========================================================================
    print("\n--- 1. VALIDAÇÃO TÉCNICA ---")

    # 1.1 index.html syntax & tags
    idx_parser = HTMLValidator('index.html')
    idx_errs = idx_parser.validate()
    test("index.html: Sintaxe HTML e balanceamento de tags", len(idx_errs) == 0, "; ".join(idx_errs))

    with open('index.html', 'r', encoding='utf-8') as f:
        idx_content = f.read()
    test("index.html: DOCTYPE html5 presente", idx_content.startswith('<!DOCTYPE html>'))
    test("index.html: <html lang=\"pt-BR\"> configurado", '<html lang="pt-BR">' in idx_content)
    test("index.html: Sem tokens {{...}} restantes", len(re.findall(r'\{\{[^}]*\}\}', idx_content)) == 0)
    test("index.html: Sem atributos sc-* restantes", len(re.findall(r'\bsc-[a-zA-Z0-9_-]+', idx_content)) == 0)

    # 1.2 404.html syntax & tags
    p404_parser = HTMLValidator('404.html')
    p404_errs = p404_parser.validate()
    test("404.html: Sintaxe HTML e balanceamento de tags", len(p404_errs) == 0, "; ".join(p404_errs))

    with open('404.html', 'r', encoding='utf-8') as f:
        p404_content = f.read()
    test("404.html: DOCTYPE html5 presente", p404_content.startswith('<!DOCTYPE html>'))
    test("404.html: Sem tokens {{...}} restantes", len(re.findall(r'\{\{[^}]*\}\}', p404_content)) == 0)
    test("404.html: Sem atributos sc-* restantes", len(re.findall(r'\bsc-[a-zA-Z0-9_-]+', p404_content)) == 0)

    # 1.3 CSS styles.css syntax & custom properties
    with open('assets/css/styles.css', 'r', encoding='utf-8') as f:
        css_content = f.read()
    css_open = css_content.count('{')
    css_close = css_content.count('}')
    test("styles.css: Chaves balanceadas", css_open == css_close, f"open={css_open}, close={css_close}")

    declared_vars = set(re.findall(r'(--[a-zA-Z0-9_-]+)\s*:', css_content))
    used_vars_css = set(re.findall(r'var\((--[a-zA-Z0-9_-]+)\)', css_content))
    used_vars_html = set(re.findall(r'var\((--[a-zA-Z0-9_-]+)\)', idx_content))
    all_used_vars = used_vars_css | used_vars_html
    undeclared = all_used_vars - declared_vars
    test("styles.css: Todas as variáveis CSS (var(--*)) declaradas em :root", len(undeclared) == 0, f"Undeclared: {undeclared}")

    test("styles.css: Container query @container gb (max-width: 920px) presente", '@container gb (max-width: 920px)' in css_content)
    test("styles.css: Media query fallback @media (max-width: 920px) presente", '@media (max-width: 920px)' in css_content)
    test("styles.css: Classe .is-dimmed configurada com opacity 0.25", '.is-dimmed' in css_content and 'opacity: 0.25' in css_content)
    test("styles.css: Regra :focus-visible para acessibilidade de teclado", ':focus-visible' in css_content)

    # 1.4 JS syntax & node execution
    res_syntax = subprocess.run(["node", "-c", "assets/js/config.js", "assets/js/app.js"], capture_output=True, text=True)
    test("JS: Sintaxe de config.js e app.js válida no Node.js", res_syntax.returncode == 0, res_syntax.stderr)

    res_test = subprocess.run(["node", "scripts/test_app.js"], capture_output=True, text=True)
    test("JS: Suíte de testes interativos do app.js executa sem erros de runtime", res_test.returncode == 0, res_test.stderr)

    # =========================================================================
    # SEÇÃO 2: VALIDAÇÃO FUNCIONAL E DE INTEGRIDADE
    # =========================================================================
    print("\n--- 2. VALIDAÇÃO FUNCIONAL E DE INTEGRIDADE ---")

    # 2.1 Anchor links
    required_anchors = ['#inicio', '#sobre', '#modalidades', '#horarios', '#professor', '#contato']
    all_anchor_hrefs = [l[0].get('href') for l in idx_parser.links if l[0].get('href', '').startswith('#')]
    missing_targets = []
    for href in set(all_anchor_hrefs):
        target_id = href[1:]
        if target_id and target_id not in idx_parser.ids:
            missing_targets.append(href)
    test("Âncoras internas: Todos os links # possuem IDs correspondentes", len(missing_targets) == 0, f"Missing: {missing_targets}")
    for req in required_anchors:
        test(f"Âncora interna: Elemento com id='{req[1:]}' existe no DOM", req[1:] in idx_parser.ids)

    # 2.2 Schedule filter
    filters = {b[1].get('data-filter'): b[1] for b in idx_parser.data_filters}
    test("Filtro de horários: Botões 'todos', 'gi' e 'nogi' presentes", set(filters.keys()) == {'todos', 'gi', 'nogi'})
    test("Filtro de horários: Botão 'todos' inicia com aria-pressed='true'", filters.get('todos', {}).get('aria-pressed') == 'true')
    test("Filtro de horários: Botão 'gi' inicia com aria-pressed='false'", filters.get('gi', {}).get('aria-pressed') == 'false')
    test("Filtro de horários: Botão 'nogi' inicia com aria-pressed='false'", filters.get('nogi', {}).get('aria-pressed') == 'false')

    kinds = [c[1].get('data-kind') for c in idx_parser.data_kinds]
    test("Grade de horários: 10 aulas cadastradas (8 Gi + 2 No-Gi)", len(kinds) == 10 and kinds.count('gi') == 8 and kinds.count('nogi') == 2)

    # 2.3 Mobile menu
    menu_btns = [b for b in idx_parser.buttons if 'gb-menu-btn' in b[0].get('class', '').split() or b[0].get('id') == 'gb-menu-toggle']
    test("Menu Mobile: Botão .gb-menu-btn presente", len(menu_btns) > 0)
    if menu_btns:
        btn = menu_btns[0][0]
        test("Menu Mobile: Botão tem aria-expanded='false'", btn.get('aria-expanded') == 'false')
        test("Menu Mobile: Botão tem aria-controls='mobile-menu'", btn.get('aria-controls') == 'mobile-menu')
        test("Menu Mobile: Botão tem aria-label='Abrir menu'", btn.get('aria-label') == 'Abrir menu')

    panel = [el for el in idx_parser.links if el[0].get('id') == 'mobile-menu'] or [p for p in idx_parser.classes if p == 'gb-mobile-panel']
    test("Menu Mobile: Painel .gb-mobile-panel presente", 'gb-mobile-panel' in idx_parser.classes)
    test("Menu Mobile: Elemento com id='mobile-menu' presente", 'mobile-menu' in idx_parser.ids)

    # 2.4 External links (WhatsApp, Instagram, Google Maps)
    external_links = []
    for attrs, pos in idx_parser.links:
        href = attrs.get('href', '')
        if href.startswith('http://') or href.startswith('https://'):
            external_links.append((attrs, pos))

    test("Links externos: 15 links externos encontrados em index.html", len(external_links) == 15, f"Found {len(external_links)}")
    invalid_targets = [l[0].get('href') for l in external_links if l[0].get('target') != '_blank']
    test("Links externos: Todos possuem target='_blank'", len(invalid_targets) == 0, f"Invalid: {invalid_targets}")

    invalid_rels = [l[0].get('href') for l in external_links if l[0].get('rel') != 'noopener noreferrer']
    test("Links externos: Todos possuem rel='noopener noreferrer'", len(invalid_rels) == 0, f"Invalid: {invalid_rels}")

    # Fallback URLs
    wa_links = [l[0].get('href') for l in external_links if 'wa.me' in l[0].get('href', '')]
    ig_links = [l[0].get('href') for l in external_links if 'instagram.com' in l[0].get('href', '')]
    maps_links = [l[0].get('href') for l in external_links if 'share.google' in l[0].get('href', '') or 'maps' in l[0].get('href', '')]

    test("Links WhatsApp: Fallbacks contêm telefone 5527999494456 e mensagem de aula experimental",
         len(wa_links) > 0 and all('5527999494456' in w and 'aula%20experimental' in w.lower() for w in wa_links))
    test("Links Instagram: Fallbacks apontam para @gbsaomateus_prof_mucio_maia",
         len(ig_links) > 0 and all('gbsaomateus_prof_mucio_maia' in i for i in ig_links))
    test("Links Google Maps: Fallbacks apontam para https://share.google/cw5yoKluPTkqPXMPN",
         len(maps_links) > 0 and all('cw5yoKluPTkqPXMPN' in m for m in maps_links))

    # 2.5 Asset existence
    missing_assets = []
    # Collect assets from index.html and 404.html
    for parser in [idx_parser, p404_parser]:
        for attrs, pos in parser.images:
            src = attrs.get('src')
            if src and not os.path.exists(src):
                missing_assets.append(f"{parser.filename} img src: {src}")
        for pic in parser.pictures:
            for s_attrs, s_pos in pic['sources']:
                srcset = s_attrs.get('srcset')
                if srcset and not os.path.exists(srcset):
                    missing_assets.append(f"{parser.filename} picture srcset: {srcset}")
        for l_attrs, l_pos in parser.link_tags:
            if l_attrs.get('rel') in ('icon', 'shortcut icon', 'apple-touch-icon', 'stylesheet'):
                href = l_attrs.get('href')
                if href and not href.startswith('http') and not os.path.exists(href):
                    missing_assets.append(f"{parser.filename} link href: {href}")
        for m_attrs, m_pos in parser.metas:
            if m_attrs.get('property') == 'og:image' or m_attrs.get('name') == 'twitter:image':
                content = m_attrs.get('content')
                if content and not content.startswith('http') and not os.path.exists(content):
                    missing_assets.append(f"{parser.filename} meta img: {content}")

    test("Integridade de assets: Todas as imagens e ícones referenciados existem no disco", len(missing_assets) == 0, "; ".join(missing_assets))

    # Favicons & Touch Icons
    fav_files = ['favicon.ico', 'favicon.png', 'favicon-16x16.png', 'favicon-32x32.png', 'apple-touch-icon.png']
    missing_favs = [f for f in fav_files if not os.path.exists(f) or not os.path.exists(os.path.join('assets/img', f))]
    test("Favicons: Todos os tamanhos padrão existem na raiz e em assets/img/", len(missing_favs) == 0, f"Missing: {missing_favs}")

    # =========================================================================
    # SEÇÃO 3: VALIDAÇÃO DE SEO, ACESSIBILIDADE E PERFORMANCE
    # =========================================================================
    print("\n--- 3. SEO, ACESSIBILIDADE & PERFORMANCE ---")

    # 3.1 Heading hierarchy
    h1_count = len([h for h in idx_parser.headings if h[0] == 'h1'])
    test("SEO/A11y: index.html possui exatamente 1 elemento <h1>", h1_count == 1, f"Found {h1_count}")

    heading_sequence = [int(h[0][1]) for h in idx_parser.headings]
    skipped_levels = []
    for i in range(1, len(heading_sequence)):
        diff = heading_sequence[i] - heading_sequence[i-1]
        if diff > 1:
            skipped_levels.append(f"Level jump from h{heading_sequence[i-1]} to h{heading_sequence[i]} at '{idx_parser.headings[i][1]}'")
    test("SEO/A11y: Hierarquia de headings estrita sem saltos de nível (h1 -> h2 -> h3)", len(skipped_levels) == 0, "; ".join(skipped_levels))

    # 3.2 Images Alt & CLS attributes
    images_missing_alt = [img for img in idx_parser.images if not img[0].get('alt')]
    test("Acessibilidade: Todas as <img> possuem atributo alt preenchido", len(images_missing_alt) == 0, f"Missing alt: {images_missing_alt}")

    images_missing_dims = [img for img in idx_parser.images if not img[0].get('width') or not img[0].get('height')]
    test("Performance (CLS): Todas as <img> possuem width e height definidos", len(images_missing_dims) == 0, f"Missing dimensions: {images_missing_dims}")

    # 3.3 Decorative SVGs aria-hidden
    svgs_not_hidden = [svg for svg in idx_parser.svgs if svg[0].get('aria-hidden') != 'true']
    test("Acessibilidade: Todos os 20 SVGs decorativos possuem aria-hidden='true'", len(svgs_not_hidden) == 0, f"Not hidden: {svgs_not_hidden}")

    # 3.4 Meta tags in index.html
    meta_names = {m[0].get('name'): m[0].get('content') for m in idx_parser.metas if 'name' in m[0]}
    meta_props = {m[0].get('property'): m[0].get('content') for m in idx_parser.metas if 'property' in m[0]}
    has_charset = any('charset' in m[0] for m in idx_parser.metas)

    test("Meta: Charset UTF-8 declarado", has_charset)
    test("Meta: Viewport responsivo width=device-width configurado", 'width=device-width' in (meta_names.get('viewport') or ''))
    test("Meta: Description presente com >50 caracteres", len(meta_names.get('description', '')) > 50)
    test("Meta: Theme-color configurada para #0D0F14", meta_names.get('theme-color') == '#0D0F14')
    test("Meta: Canonical link presente", any(l[0].get('rel') == 'canonical' for l in idx_parser.link_tags))
    test("Open Graph: og:title, og:description, og:image, og:type, og:locale presentes",
         all(p in meta_props for p in ['og:title', 'og:description', 'og:image', 'og:type', 'og:locale']))
    test("Open Graph: Dimensões da imagem (og:image:width=1200, og:image:height=630)",
         meta_props.get('og:image:width') == '1200' and meta_props.get('og:image:height') == '630')
    test("Twitter Card: twitter:card='summary_large_image', twitter:title, twitter:image presentes",
         meta_names.get('twitter:card') == 'summary_large_image' and 'twitter:title' in meta_names and 'twitter:image' in meta_names)

    # 3.5 Server & Crawling configuration (.htaccess, robots.txt, sitemap.xml)
    test("DevOps: Arquivo .htaccess existe", os.path.exists('.htaccess'))
    with open('.htaccess', 'r', encoding='utf-8') as f:
        ht_content = f.read()
    test("DevOps: .htaccess possui compressão mod_deflate", 'mod_deflate' in ht_content)
    test("DevOps: .htaccess possui políticas de cache mod_expires", 'mod_expires' in ht_content)
    test("DevOps: .htaccess possui redirecionamento HTTPS mod_rewrite", 'RewriteCond %{HTTPS} off' in ht_content)
    test("DevOps: .htaccess define ErrorDocument 404 /404.html", 'ErrorDocument 404 /404.html' in ht_content)
    test("DevOps: .htaccess inclui cabeçalhos de segurança (X-Content-Type-Options, X-Frame-Options)",
         'X-Content-Type-Options' in ht_content and 'X-Frame-Options' in ht_content)

    test("SEO: Arquivo robots.txt existe", os.path.exists('robots.txt'))
    with open('robots.txt', 'r', encoding='utf-8') as f:
        rb_content = f.read()
    test("SEO: robots.txt permite rastreamento público (Allow: /) e aponta sitemap",
         'Allow: /' in rb_content and 'Sitemap:' in rb_content)

    test("SEO: Arquivo sitemap.xml existe", os.path.exists('sitemap.xml'))
    try:
        tree = ET.parse('sitemap.xml')
        root = tree.getroot()
        test("SEO: sitemap.xml é um XML válido com schema urlset", 'urlset' in root.tag)
    except Exception as e:
        test("SEO: sitemap.xml é um XML válido", False, str(e))

    # =========================================================================
    # RESUMO FINAL
    # =========================================================================
    print("\n" + "=" * 70)
    print(f"RESULTADO: {passed_tests} / {total_tests} TESTES PASSARAM ({passed_tests/total_tests*100:.1f}%)")
    if failed_tests:
        print("FALHAS ENCONTRADAS:")
        for name, err in failed_tests:
            print(f"  - {name}: {err}")
        print("=" * 70)
        sys.exit(1)
    else:
        print("STATUS: TODAS AS VALIDAÇÕES FORAM BEM-SUCEDIDAS COM 100% DE APROVAÇÃO!")
        print("=" * 70)
        sys.exit(0)

if __name__ == '__main__':
    run_audit()
