import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';
import multer from 'multer';
import { v4 as uuidv4 } from 'uuid';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;
const STORAGE_PATH = join(__dirname, '..', 'storage', 'music');
const UPLOAD_PATH = join(__dirname, '..', 'uploads');

app.use(cors());
app.use(express.json());
app.use(express.static(join(__dirname, '..', 'frontend')));

if (!fs.existsSync(STORAGE_PATH)) fs.mkdirSync(STORAGE_PATH, { recursive: true });
if (!fs.existsSync(UPLOAD_PATH)) fs.mkdirSync(UPLOAD_PATH, { recursive: true });

const storage = multer.diskStorage({
    destination: UPLOAD_PATH,
    filename: (req, file, cb) => {
        const uniqueName = `${uuidv4()}-${file.originalname}`;
        cb(null, uniqueName);
    }
});

const upload = multer({
    storage,
    fileFilter: (req, file, cb) => {
        if (file.mimetype === 'audio/mpeg' || file.originalname.endsWith('.mp3')) {
            cb(null, true);
        } else {
            cb(new Error('Apenas MP3'));
        }
    },
    limits: { fileSize: 100 * 1024 * 1024 }
});

let playerState = {
    currentTrack: null,
    isPlaying: false,
    position: 0,
    queue: [],
    library: []
};

function loadLibrary() {
    const files = fs.readdirSync(STORAGE_PATH);
    playerState.library = files
        .filter(f => f.endsWith('.mp3'))
        .map(f => ({
            id: uuidv4(),
            title: f.replace('.mp3', ''),
            artist: 'Desconhecido',
            duration: 0,
            filename: f,
            path: join(STORAGE_PATH, f),
            size: fs.statSync(join(STORAGE_PATH, f)).size
        }));
    return playerState.library;
}

app.get('/api/info', (req, res) => {
    res.json({ name: 'Radio Jeffao', status: 'online' });
});

app.get('/api/player/current', (req, res) => {
    res.json({
        track: playerState.currentTrack,
        isPlaying: playerState.isPlaying,
        position: playerState.position
    });
});

app.post('/api/player/command', (req, res) => {
    const { command, trackId } = req.body;
    const track = playerState.library.find(t => t.id === trackId);
    
    if (command === 'play-track' && track) {
        playerState.currentTrack = track;
        playerState.isPlaying = true;
    } else if (command === 'play') {
        playerState.isPlaying = true;
    } else if (command === 'pause') {
        playerState.isPlaying = false;
    }
    
    res.json({ success: true, state: playerState });
});

app.post('/api/upload', upload.array('files', 50), (req, res) => {
    if (!req.files) return res.status(400).json({ error: 'Sem arquivos' });
    
    req.files.forEach(file => {
        const dest = join(STORAGE_PATH, file.filename);
        fs.copyFileSync(file.path, dest);
        fs.unlinkSync(file.path);
    });
    
    loadLibrary();
    res.json({ success: true, uploaded: req.files.length });
});

app.get('/api/library', (req, res) => {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const start = (page - 1) * limit;
    const items = playerState.library.slice(start, start + limit);
    
    res.json({
        total: playerState.library.length,
        page,
        limit,
        items
    });
});

app.get('/api/library/stats', (req, res) => {
    const totalSize = playerState.library.reduce((sum, t) => sum + t.size, 0);
    res.json({ total: playerState.library.length, totalSize });
});

app.get('/api/library/search', (req, res) => {
    const query = req.query.q?.toLowerCase() || '';
    const results = playerState.library.filter(t =>
        t.title.toLowerCase().includes(query)
    );
    res.json({ total: results.length, items: results });
});

app.get('/api/stream', (req, res) => {
    if (!playerState.currentTrack) {
        return res.status(404).json({ error: 'Sem musica' });
    }
    
    const filepath = playerState.currentTrack.path;
    if (!fs.existsSync(filepath)) {
        return res.status(404).json({ error: 'Arquivo nao encontrado' });
    }
    
    const stat = fs.statSync(filepath);
    const fileSize = stat.size;
    const range = req.headers.range;
    
    if (range) {
        const parts = range.replace(/bytes=/, '').split('-');
        const start = parseInt(parts[0], 10);
        const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
        
        res.writeHead(206, {
            'Content-Range': `bytes ${start}-${end}/${fileSize}`,
            'Accept-Ranges': 'bytes',
            'Content-Length': end - start + 1,
            'Content-Type': 'audio/mpeg'
        });
        fs.createReadStream(filepath, { start, end }).pipe(res);
    } else {
        res.writeHead(200, {
            'Content-Length': fileSize,
            'Content-Type': 'audio/mpeg'
        });
        fs.createReadStream(filepath).pipe(res);
    }
});

loadLibrary();

app.listen(PORT, () => {
    console.log(`🎙️ Radio Jeffao em http://localhost:${PORT}`);
    console.log(`📁 Biblioteca: ${STORAGE_PATH}`);
    console.log(`🎵 Stream: http://localhost:${PORT}/api/stream`);
});
