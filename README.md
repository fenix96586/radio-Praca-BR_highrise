# 🎙️ Rádio Jeffão - Web Radio 24/7

Sistema profissional de web rádio integrado com Highrise Game.

## 📋 Especificações

- **Capacidade**: Até 25.000 ouvintes simultâneos
- **Sincronização**: Todos os usuários ouvem a mesma música simultaneamente
- **Formato**: MP3 apenas (compatível com Highrise)
- **Biblioteca**: Até 500 músicas no WebVPS
- **Streaming**: URL HTTPS segura

## 🏗️ Estrutura do Projeto

```
radio-Praca-BR_highrise/
├── frontend/                 # Interface Web
│   ├── index.html           # Página principal
│   ├── css/
│   │   └── style.css        # Estilos (tema escuro com gradiente magenta)
│   ├── js/
│   │   ├── app.js           # Lógica principal
│   │   ├── player.js        # Controle de reprodução
│   │   ├── youtube.js       # Conversão YouTube → MP3
│   │   ├── uploader.js      # Upload de arquivos
│   │   └── sync.js          # Sincronização em tempo real
│   └── assets/
│       └── icons/           # Ícones e imagens
├── backend/
│   ├── server.js            # Servidor Node.js/Express
│   ├── config/
│   │   └── env.js           # Variáveis de ambiente
│   ├── routes/
│   │   ├── stream.js        # Rota de streaming
│   │   ├── library.js       # Gerenciamento de biblioteca
│   │   ├── upload.js        # Upload de arquivos
│   │   └── youtube.js       # Processamento YouTube
│   ├── controllers/
│   │   ├── playerController.js
│   │   ├── libraryController.js
│   │   └── youtubeController.js
│   ├── middleware/
│   │   ├── auth.js          # Autenticação
│   │   └── errorHandler.js  # Tratamento de erros
│   ├── utils/
│   │   ├── converter.js     # Converter vídeo para MP3
│   │   ├── storage.js       # Gerenciamento de armazenamento
│   │   └── queue.js         # Fila de reprodução
│   └── models/
│       ├── Music.js         # Modelo de música
│       └── Queue.js         # Modelo de fila
├── bot/                     # Bot para Highrise
│   ├── bot.js              # Lógica principal do bot
│   ├── commands/
│   │   ├── play.js         # Comando play
│   │   ├── queue.js        # Comando queue
│   │   └── request.js      # Comando request (pedir música)
│   └── events/
│       ├── onReady.js      # Evento de inicialização
│       └── onMessage.js    # Evento de mensagem
├── database/
│   ├── schema.sql          # Estrutura do banco
│   └── migrations/
├── .github/
│   └── CODEOWNERS          # Proteção de código
├── .env.example            # Variáveis de ambiente
├── package.json            # Dependências
└── docs/
    ├── API.md              # Documentação da API
    ├── ARCHITECTURE.md     # Arquitetura do sistema
    └── DEPLOYMENT.md       # Guia de deploy

```

## 🔐 Segurança

- ✅ Repositório com proteção de branch
- ✅ Code owners definidos
- ✅ Validação de entrada
- ✅ Rate limiting
- ✅ Autenticação de bot

## 📦 Blocos Funcionais

### ✅ Bloco 1: Links de Streaming
- URL com HTTPS
- Botão "Copiar" com feedback visual
- Sem erros ao copiar

### ✅ Bloco 2: Player Principal
- Informações da música (Música, Artista)
- Barra de progresso
- Botões: ⏮️ ⏯️ ⏭️ 🔀
- Sincronização em tempo real

### ✅ Bloco 3: Conversor YouTube → MP3
- Detecção automática (vídeo/playlist)
- Download e conversão
- Requisição via bot

### ✅ Bloco 4: Upload de Arquivos
- Até 50 arquivos MP3 simultaneamente
- Salvamento em biblioteca

### ✅ Bloco 5: Biblioteca
- Até 500 músicas
- Seletor para reprodução instantânea
- Display de 20 arquivos por vez

## 🚀 Próximos Passos

1. Configurar variáveis de ambiente
2. Criar arquivos base HTML/CSS/JS
3. Implementar API de streaming
4. Configurar YouTube downloader
5. Integrar com bot Highrise
