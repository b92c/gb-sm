# Deploy — HostGator (shared hosting) — Gracie Barra São Mateus

## Pré-requisitos
- Conta HostGator com domínio (ou subdomínio) apontado.
- Acesso ao cPanel ou FTP.
- Site validado localmente (ver `TESTING.md`).

## Passos

### 1. Preparar arquivos
- Garantir estrutura conforme `STRUCTURE.md`.
- Comprimir imagens (ver `ASSETS.md`).
- Atualizar `sitemap.xml` e canonical/OG com o domínio real (quando definido).
- Verificar `.htaccess`.

### 2. Upload
Opção A — cPanel File Manager:
1. Compactar projeto em `.zip`.
2. Upload para `public_html/`.
3. Extrair.
4. Remover o `.zip`.

Opção B — FTP (FileZilla):
1. Conectar com credenciais FTP do cPanel.
2. Enviar conteúdo da raiz do projeto para `public_html/`.

### 3. Permissões
- Arquivos: `644`.
- Pastas: `755`.

### 4. SSL/HTTPS
- cPanel → SSL/TLS Status → Run AutoSSL (Let's Encrypt).
- Confirmar redirect HTTP→HTTPS via `.htaccess`.

### 5. Domínio
- Se domínio novo: apontar DNS (A record) para IP do servidor.
- Aguardar propagação (até 24h).

### 6. Validação pós-deploy
- Abrir site no domínio real (desktop + mobile).
- Testar links WhatsApp, Instagram, Maps.
- Testar menu mobile e filtro de horários.
- Verificar console do navegador (sem erros).
- Testar Lighthouse no domínio real.

### 7. Backup
- Manter zip do deploy + repositório Git.
- Antes de cada atualização, baixar backup do `public_html/`.

## .htaccess (referência)
```
# HTTPS redirect
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Compressão
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>

# Cache
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>

# 404
ErrorDocument 404 /404.html
```