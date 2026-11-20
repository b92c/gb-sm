# Gracie Barra São Mateus — Site Institucional

[![Status](https://img.shields.io/badge/Status-Pronto%20para%20Produ%C3%A7%C3%A3o-success)](https://github.com/)
[![Plataforma](https://img.shields.io/badge/Hospedagem-HostGator%20Shared-blue)](https://www.hostgator.com.br/)
[![Stack](https://img.shields.io/badge/Stack-HTML5%20%7C%20CSS3%20%7C%20JS%20Vanilla-red)](https://developer.mozilla.org/)

Site institucional moderno, responsivo e de alta performance da **Gracie Barra São Mateus**, localizada no balneário de Guriri, São Mateus – ES, sob a liderança do **Professor Múcio** (Faixa Preta).

O projeto foi desenvolvido em arquitetura **SPA (Single Page Application)** estática, sem necessidade de banco de dados ou backend complexo, garantindo carregamento ultrarrápido, excelente pontuação de SEO (Core Web Vitals) e compatibilidade total com planos de hospedagem compartilhada da **HostGator** (Apache).

---

## 🥋 Características do Projeto

- **Identidade Visual Fiel**: Cores oficiais da Gracie Barra (`#0D0F14`, `#D7182A`, `#0B3D91`), tipografia esportiva e elementos modernos.
- **Foco em Conversão**: Botões diretos para agendamento de aula experimental no WhatsApp em pontos estratégicos.
- **Grade de Horários Interativa**: Visualização estática clara com filtros dinâmicos por categoria (Todos, Gi/Kimono, No-Gi, Kids).
- **Dados Centralizados**: Informações de contato, endereço, horários e textos organizados em `assets/js/config.js` para fácil atualização sem precisar alterar o HTML.
- **Pronto para SEO e HostGator**: Configurações de `.htaccess` (HTTPS forçado, compressão Gzip, cache de 1 ano para imagens), `robots.txt`, `sitemap.xml` e página personalizada `404.html`.

---

## 📁 Estrutura de Pastas

```
gb-sm/
├── index.html                 # Página principal (SPA institucional)
├── 404.html                   # Página de erro customizada (identidade Gracie Barra)
├── .htaccess                  # Configurações do servidor Apache (HostGator)
├── robots.txt                 # Diretrizes de rastreamento para buscadores
├── sitemap.xml                # Mapa do site para indexação no Google/Bing
├── README.md                  # Este guia do projeto e deploy
├── assets/
│   ├── css/
│   │   └── styles.css         # Variáveis de tema, layout, container queries e componentes
│   ├── js/
│   │   ├── config.js          # Objeto SITE centralizado com contatos, horários e textos
│   │   └── app.js             # Menu mobile, filtros da grade e bind dinâmico
│   └── img/
│       ├── logo.png           # Logotipo oficial (navbar, footer, 404)
│       ├── hero-academia.jpg  # Imagem de destaque do tatame
│       ├── modalidade-gi.jpg  # Jiu-Jitsu com kimono
│       ├── modalidade-nogi.jpg # Jiu-Jitsu sem kimono (No-Gi / Submission)
│       ├── modalidade-kids.jpg # Jiu-Jitsu Infantil
│       ├── modalidade-feminina.jpg # Turma Feminina
│       ├── professor-mucio.jpg # Foto oficial do Professor Múcio
│       └── sede-guriri.jpg    # Fachada / recepção da sede em Guriri
└── .docs/                     # Documentação técnica e planejamento do projeto
    ├── PLAN.md                # Planejamento estratégico
    ├── DEPLOY.md              # Especificações de hospedagem
    ├── STRUCTURE.md           # Convenções e arquitetura
    ├── ASSETS.md              # Mapeamento de imagens
    ├── DECISIONS.md           # Registro de decisões tomadas
    ├── TESTING.md             # Roteiro de testes de homologação
    └── TASKS.md               # Checklist de tarefas do projeto
```

---

## 💻 Como Executar Localmente

Como o projeto é 100% estático (HTML, CSS e JS puro), você pode testá-lo em qualquer computador sem precisar de Node.js, PHP ou banco de dados.

### Opção 1: Via Python (Recomendado)
Se tiver Python instalado, abra o terminal na pasta raiz do projeto e execute:

```bash
# Python 3
python3 -m http.server 8000

# Ou Python 2
python -m SimpleHTTPServer 8000
```
Em seguida, acesse no navegador: `http://localhost:8000`

### Opção 2: Extensão Live Server (VS Code)
1. Abra a pasta do projeto no **Visual Studio Code**.
2. Instale a extensão **Live Server** (caso não tenha).
3. Clique com o botão direito sobre o arquivo `index.html` e selecione **"Open with Live Server"**.

### Opção 3: PHP Built-in Server
```bash
php -S localhost:8000
```

---

## ⚙️ Como Atualizar Contatos, Textos e Horários

Todas as informações dinâmicas e variáveis do site estão isoladas no arquivo:
👉 `assets/js/config.js`

Ao editar esse arquivo, as alterações se refletem automaticamente em todo o site sem necessidade de caçar links pelo código HTML.

### 1. Alterar Número de WhatsApp
No arquivo `assets/js/config.js`, localize a seção `contato`:
```javascript
contato: {
  whatsapp: "(27) 99949-4456",
  whatsappRaw: "5527999494456", // Somente números com DDI (55) + DDD (27)
  mensagemPadrao: "Olá! Gostaria de agendar uma aula experimental na Gracie Barra São Mateus.",
  // ...
}
```

### 2. Atualizar Endereço
```javascript
endereco: {
  rua: "Rua Professor Amaro Nascimento Mendes (antiga Rua 7)",
  numero: "351",
  bairro: "Guriri Norte",
  cidade: "São Mateus",
  estado: "ES",
  pontoReferencia: "Próximo à pracinha de Guriri",
  mapsUrl: "https://maps.google.com/?q=..."
}
```

### 3. Ajustar Grade de Horários
A lista de turmas e horários pode ser ajustada diretamente no array `horarios` em `config.js`:
```javascript
horarios: [
  { dia: "Segunda a Sexta", hora: "07:00", turma: "Adulto Fundamentos", tipo: "gi" },
  { dia: "Segunda a Sexta", hora: "18:00", turma: "GB Kids", tipo: "kids" },
  { dia: "Segunda a Sexta", hora: "19:30", turma: "No-Gi / Submission", tipo: "nogi" },
  // ...
]
```

---

## 🚀 Guia de Deploy na HostGator (Passo a Passo)

Este guia orienta o envio dos arquivos para planos de hospedagem compartilhada da **HostGator** (Plano P, M, Business ou Turbo com cPanel).

### Passo 1: Ajustar URL nos Arquivos de SEO
Antes de subir para o ar, abra os arquivos abaixo e substitua `https://SEU-DOMINIO.com` pelo domínio real registrado:
1. **`robots.txt`**: Ajuste a linha `Sitemap: https://seu-dominio-real.com.br/sitemap.xml`.
2. **`sitemap.xml`**: Ajuste a tag `<loc>https://seu-dominio-real.com.br/</loc>`.
3. **`index.html`**: Ajuste as tags `canonical` e `og:url` se presentes.

### Passo 2: Upload dos Arquivos

#### Opção A: Pelo Gerenciador de Arquivos do cPanel (Mais Rápido)
1. Acesse o **cPanel** da sua conta HostGator (`seudominio.com.br/cpanel`).
2. Abra a ferramenta **Gerenciador de Arquivos** (*File Manager*).
3. Navegue até a pasta **`public_html`** (se for o domínio principal) ou até a pasta do subdomínio/domínio adicional correspondente.
4. Compacte todo o conteúdo do projeto em um arquivo **`.zip`** (atenção: inclua os arquivos ocultos `.htaccess`).
5. Clique em **Carregar** (*Upload*) e envie o arquivo `.zip`.
6. Após concluir, selecione o arquivo zip no cPanel e clique em **Extrair** (*Extract*).
7. Certifique-se de que o `index.html` e a pasta `assets/` estão na raiz do diretório `public_html`.
8. Remova o arquivo `.zip` temporário.

#### Opção B: Por FTP (FileZilla)
1. Abra o FileZilla ou cliente FTP de sua preferência.
2. Conecte-se usando:
   - **Host:** `ftp.seudominio.com.br` (ou IP informado no painel da HostGator)
   - **Usuário:** seu usuário FTP do cPanel
   - **Senha:** sua senha
   - **Porta:** `21`
3. No painel remoto (lado direito), abra a pasta `public_html/`.
4. No painel local (lado esquerdo), selecione todos os arquivos da pasta do projeto (`index.html`, `404.html`, `.htaccess`, `robots.txt`, `sitemap.xml`, pasta `assets/`).
5. Arraste para o painel remoto e aguarde o envio completo.

> **Importante:** Não é necessário enviar as pastas `.git/` nem `.docs/` para o servidor de produção, economizando espaço e garantindo segurança.

### Passo 3: Permissões de Arquivos e Pastas
O cPanel HostGator exige as permissões padrão do Linux para servidores web:
- **Pastas:** `755` (`drwxr-xr-x`)
- **Arquivos:** `644` (`-rw-r--r--`)

Geralmente o descompactador do cPanel já aplica essas permissões automaticamente.

### Passo 4: Ativar SSL Gratuito (HTTPS)
1. No cPanel da HostGator, vá na seção **Segurança** e clique em **Status do SSL/TLS**.
2. Clique no botão **Executar AutoSSL** (*Run AutoSSL*).
3. O certificado Let's Encrypt / Sectigo gratuito será instalado automaticamente.
4. Como o arquivo `.htaccess` já possui regras ativas de redirecionamento HTTP → HTTPS, todo visitante será automaticamente direcionado para a versão segura com cadeado verde.

### Passo 5: Testes e Homologação Pós-Deploy
Após a publicação, execute o seguinte checklist:
- [ ] O domínio abre em HTTPS com cadeado de segurança ativo.
- [ ] O clique no botão do WhatsApp abre uma conversa com o texto de agendamento no número `(27) 99949-4456`.
- [ ] O menu mobile (hambúrguer) abre e fecha perfeitamente em telas de smartphone.
- [ ] O filtro de modalidades na grade de horários funciona corretamente.
- [ ] Digite um link inexistente (ex.: `seudominio.com.br/pagina-inexistente`) e comprove que a página `404.html` estilizada é exibida.
- [ ] Abra o console do navegador (F12) e verifique se não há erros em vermelho.

---

## 🔒 Segurança e Otimizações Inclusas (`.htaccess`)

O arquivo `.htaccess` incluído já conta com:
- **Redirecionamento Forçado para HTTPS (301)**.
- **Compressão Gzip (mod_deflate)** para HTML, CSS, JavaScript, JSON e SVG, diminuindo o tráfego em até 70%.
- **Cache de Longa Duração (mod_expires)**:
  - Imagens e Fontes: 1 ano (`access plus 1 year`).
  - CSS e Scripts: 1 mês (`access plus 1 month`).
- **Página 404 Personalizada**: Aponta automaticamente para `/404.html`.
- **Proteção de Diretórios (`Options -Indexes`)**: Impede que visitantes listem o conteúdo das pastas.
- **Cabeçalhos de Segurança (mod_headers)**:
  - `X-Content-Type-Options: nosniff` (impede MIME sniffing).
  - `X-Frame-Options: SAMEORIGIN` (protege contra clickjacking).
  - `Referrer-Policy: strict-origin-when-cross-origin`.

---

## 📞 Suporte e Contato

- **Academia:** Gracie Barra São Mateus
- **Localização:** Rua Professor Amaro Nascimento Mendes, nº 351, Guriri Norte, São Mateus – ES
- **WhatsApp:** [(27) 99949-4456](https://wa.me/5527999494456)
- **Professor Responsável:** Professor Múcio (Faixa Preta)
