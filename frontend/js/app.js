class RadioApp {
    constructor() {
        this.apiBase = '/api';
        this.currentTrack = null;
        this.isPlaying = false;
        this.libraryPage = 1;
        this.libraryTotal = 0;
        this.init();
    }

    async init() {
        console.log('🎙️ Iniciando Radio Jeffao...');
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEvents());
        } else {
            this.setupEvents();
        }
        await this.loadLibraryStats();
        await this.loadCurrentTrack();
    }

    setupEvents() {
        document.getElementById('btnCopyStream')?.addEventListener('click', () => this.copyUrl());
        document.getElementById('btnPlayPause')?.addEventListener('click', () => this.togglePlay());
        document.getElementById('btnDownload')?.addEventListener('click', () => this.downloadYT());
        document.getElementById('youtubeUrl')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.downloadYT();
        });
        
        const uploadBox = document.getElementById('uploadBox');
        uploadBox?.addEventListener('click', () => document.getElementById('fileUpload').click());
        uploadBox?.addEventListener('dragover', (e) => e.preventDefault());
        uploadBox?.addEventListener('drop', (e) => this.handleDrop(e));
        document.getElementById('fileUpload')?.addEventListener('change', (e) => this.uploadFiles(e));
        
        document.getElementById('searchMusic')?.addEventListener('input', (e) => this.search(e.target.value));
        document.getElementById('btnPrevPage')?.addEventListener('click', () => this.prevPage());
        document.getElementById('btnNextPage')?.addEventListener('click', () => this.nextPage());
    }

    async copyUrl() {
        const url = document.getElementById('streamUrl').textContent;
        try {
            await navigator.clipboard.writeText(url);
            const feedback = document.getElementById('copyFeedback');
            feedback.textContent = '✅ Copiado!';
            feedback.style.display = 'block';
            setTimeout(() => feedback.style.display = 'none', 2000);
        } catch (err) {
            alert('Erro ao copiar');
        }
    }

    togglePlay() {
        this.isPlaying ? this.pause() : this.play();
    }

    async play() {
        if (!this.currentTrack) return;
        this.isPlaying = true;
        await this.sendCommand('play');
        this.updateUI();
    }

    async pause() {
        this.isPlaying = false;
        await this.sendCommand('pause');
        this.updateUI();
    }

    updateUI() {
        const btn = document.getElementById('btnPlayPause');
        btn.textContent = this.isPlaying ? '⏸️' : '⏯️';
    }

    async downloadYT() {
        const url = document.getElementById('youtubeUrl').value.trim();
        if (!url) {
            alert('Cole um link do YouTube!');
            return;
        }

        const progress = document.getElementById('downloadProgress');
        progress.style.display = 'block';

        try {
            const response = await fetch(`${this.apiBase}/youtube/download`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            if (response.ok) {
                document.getElementById('youtubeUrl').value = '';
                await this.loadLibraryStats();
            } else {
                alert('Erro ao processar YouTube');
            }
        } catch (err) {
            alert('Erro: ' + err.message);
        } finally {
            progress.style.display = 'none';
        }
    }

    handleDrop(event) {
        event.preventDefault();
        const files = event.dataTransfer.files;
        this.uploadFiles({ target: { files } });
    }

    async uploadFiles(event) {
        const files = Array.from(event.target.files);
        if (files.length > 50) {
            alert('Máximo 50 arquivos!');
            return;
        }

        const formData = new FormData();
        files.forEach(f => formData.append('files', f));

        try {
            const response = await fetch(`${this.apiBase}/upload`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                await this.loadLibraryStats();
            }
        } catch (err) {
            alert('Erro no upload');
        }
    }

    async loadLibrary(page = 1) {
        try {
            const response = await fetch(`${this.apiBase}/library?page=${page}&limit=20`);
            const data = await response.json();
            
            this.libraryTotal = data.total;
            this.libraryPage = page;
            this.renderLibrary(data.items);
            this.updatePagination();
        } catch (err) {
            console.error('Erro biblioteca:', err);
        }
    }

    renderLibrary(items) {
        const list = document.getElementById('libraryList');
        
        if (items.length === 0) {
            list.innerHTML = '<div style="text-align: center; padding: 20px; color: #a0a0a0;">Sem músicas</div>';
            return;
        }

        list.innerHTML = items.map(m => `
            <div class="music-item ${this.currentTrack?.id === m.id ? 'playing' : ''}" data-id="${m.id}">
                <div>🎵</div>
                <div class="music-info">
                    <div class="music-title">${m.title}</div>
                    <div class="music-meta">${m.artist}</div>
                </div>
                <button class="btn-control" onclick="radioApp.playTrack('${m.id}')">▶️</button>
            </div>
        `).join('');
    }

    async playTrack(id) {
        await this.sendCommand('play-track', { trackId: id });
        await this.loadCurrentTrack();
    }

    async search(query) {
        try {
            const response = await fetch(`${this.apiBase}/library/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.renderLibrary(data.items);
            this.libraryTotal = data.total;
        } catch (err) {
            console.error('Erro busca:', err);
        }
    }

    nextPage() {
        const maxPage = Math.ceil(this.libraryTotal / 20);
        if (this.libraryPage < maxPage) {
            this.loadLibrary(this.libraryPage + 1);
        }
    }

    prevPage() {
        if (this.libraryPage > 1) {
            this.loadLibrary(this.libraryPage - 1);
        }
    }

    updatePagination() {
        const maxPage = Math.ceil(this.libraryTotal / 20);
        document.getElementById('pageInfo').textContent = `Pág ${this.libraryPage} de ${maxPage}`;
        document.getElementById('btnPrevPage').disabled = this.libraryPage === 1;
        document.getElementById('btnNextPage').disabled = this.libraryPage === maxPage;
    }

    async loadCurrentTrack() {
        try {
            const response = await fetch(`${this.apiBase}/player/current`);
            const data = await response.json();
            
            this.currentTrack = data.track;
            this.isPlaying = data.isPlaying;
            
            if (this.currentTrack) {
                document.getElementById('currentSongTitle').textContent = this.currentTrack.title || 'Desconhecido';
                document.getElementById('currentArtist').textContent = this.currentTrack.artist || 'Artista desconhecido';
            }
            
            this.updateUI();
        } catch (err) {
            console.error('Erro track:', err);
        }
    }

    async loadLibraryStats() {
        try {
            const response = await fetch(`${this.apiBase}/library/stats`);
            const data = await response.json();
            
            document.getElementById('musicCount').textContent = `${data.total} músicas`;
            document.getElementById('storageUsage').textContent = `${(data.totalSize / 1024 / 1024).toFixed(2)} MB`;
            
            await this.loadLibrary(1);
        } catch (err) {
            console.error('Erro stats:', err);
        }
    }

    async sendCommand(command, data = {}) {
        try {
            await fetch(`${this.apiBase}/player/command`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ command, ...data })
            });
        } catch (err) {
            console.error('Erro comando:', err);
        }
    }
}

const radioApp = new RadioApp();
