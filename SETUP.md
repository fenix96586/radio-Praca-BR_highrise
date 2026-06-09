# 🎙️ Rádio Jeffão - Deploy e Teste

## ✅ Estrutura Completa Criada

```
✅ Backend Express.js - servidor/api
✅ Frontend HTML/CSS/JS - interface 5 blocos  
✅ Storage MP3 - biblioteca local
✅ Proteção de código - CODEOWNERS
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/fenix96586/radio-Praca-BR_highrise.git
cd radio-Praca-BR_highrise
```

### 2. Instalar dependências
```bash
npm install
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Editar .env se necessário
```

### 4. Executar o servidor
```bash
npm start
```

Ou em desenvolvimento:
```bash
npm run dev
```

---

## 🌐 URLs para Testar

### Web Rádio (Interface)
```
http://localhost:3000
```

### API de Streaming
```
http://localhost:3000/api/stream
```

### Endpoints da API

**Player atual:**
```
GET http://localhost:3000/api/player/current
```

**Biblioteca:**
```
GET http://localhost:3000/api/library?page=1&limit=20
```

**Buscar:**
```
GET http://localhost:3000/api/library/search?q=musica
```

**Upload:**
```
POST http://localhost:3000/api/upload
(multipart/form-data com files)
```

**Comando de player:**
```
POST http://localhost:3000/api/player/command
{
  "command": "play-track",
  "trackId": "id-da-musica"
}
```

---

## 📋 Funcionalidades Implementadas

### Bloco 1: URL de Stream ✅
- Link HTTPS para copiar
- Botão "Copiar" com feedback

### Bloco 2: Player ✅
- Display da música tocando
- Botões Play/Pause
- Informações em tempo real

### Bloco 3: YouTube Download ✅
- Converter vídeo/playlist para MP3
- Adicionar na biblioteca

### Bloco 4: Upload de Arquivos ✅
- Até 50 arquivos MP3
- Drag & drop
- Salvamento automático

### Bloco 5: Biblioteca ✅
- Lista de 500 músicas
- Busca e filtro
- Paginação (20 por página)

---

## 🔐 Proteção do Código

- ✅ CODEOWNERS criado
- ✅ Apenas você (@fenix96586) pode fazer merge
- ✅ Editar via VS Code sem problemas
- ✅ GitHub protege a main branch

---

## 🤖 Bot do Highrise (Temporário)

Quando tiver o `main.py` e `emotes.py`:

1. Crie pasta `bot/` 
2. Coloque os arquivos lá
3. Será sincronizado com a web rádio

---

## 📝 Próximos Passos

1. **Fazer upload de MP3s na pasta `storage/music/`**
2. **Testar interface em `http://localhost:3000`**
3. **Copiar URL do stream e adicionar no Highrise**
4. **Enviar main.py e emotes.py do bot**

---

## 🧪 Teste Rápido

1. Abra seu navegador
2. Vá para `http://localhost:3000`
3. Clique em "Copiar" no Bloco 1 (URL do stream)
4. A URL está pronta para colar no Highrise

---

## 📞 Suporte

Qualquer dúvida ou erro, me mande:
- Screenshots dos erros
- Seu main.py e emotes.py
- Que funcionalidade não tá funcionando

---

**Sua Rádio Jeffão está PRONTA! 🎙️**

