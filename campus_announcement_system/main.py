import sys
from pathlib import Path

# Projenin kök dizinini sys.path'e ekleyerek doğrudan dosya çalıştırma desteği sağlarız
sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from contextlib import asynccontextmanager
from campus_announcement_system.presentation.api import router
from campus_announcement_system.infrastructure.logger import Logger

# Singleton Logger örneğini oluştur
logger = Logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI uygulamasının yaşam döngüsü (lifespan) yönetimini sağlar.
    Uygulama ayağa kalkarken ve kapanırken Singleton Logger ile durumları günlüğe kaydeder.
    """
    logger.info("Kampüs Duyuru Sistemi API başlatılıyor...")
    yield
    logger.info("Kampüs Duyuru Sistemi API durduruluyor...")

app = FastAPI(
    title="Kampüs Duyuru Sistemi API",
    description="Katmanlı Mimari (Layered Architecture) ve Tasarım Desenleri (Observer, Factory, Singleton) kullanılarak geliştirilmiş Kampüs Duyuru Sistemi.",
    version="1.0.0",
    lifespan=lifespan
)

# API yönlendiricisini sisteme dahil et
app.include_router(router, prefix="/api")

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root() -> HTMLResponse:
    """
    Kampüs Duyuru Sistemi için görsel ve etkileşimli bir Canlı Dashboard arayüzü sunar.
    """
    html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kampüs Duyuru Sistemi Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #0a0b12;
            --bg-card: rgba(17, 20, 36, 0.75);
            --border-glow: rgba(124, 58, 237, 0.2);
            --primary: #7c3aed;
            --secondary: #06b6d4;
            --accent-red: #ef4444;
            --accent-green: #10b981;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-dark);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(124, 58, 237, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.08) 0%, transparent 40%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }
        
        header {
            padding: 1.5rem 2rem;
            max-width: 1400px;
            width: 100%;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .header-title h1 {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a78bfa 0%, #22d3ee 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .header-title p {
            color: var(--text-muted);
            font-size: 0.9rem;
        }
        
        .badge-live {
            background: rgba(16, 185, 129, 0.1);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 0.4rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .badge-live::before {
            content: '';
            display: block;
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(0.9); opacity: 0.6; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.9); opacity: 0.6; }
        }
        
        main {
            flex: 1;
            max-width: 1400px;
            width: 100%;
            margin: 1.5rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1.25fr 1.75fr;
            gap: 2rem;
        }
        
        @media (max-width: 1024px) {
            main {
                grid-template-columns: 1fr;
            }
        }
        
        .glass-card {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            border-color: var(--border-glow);
            box-shadow: 0 10px 40px rgba(124, 58, 237, 0.1);
        }
        
        .card-title {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 0.75rem;
            color: #fff;
        }

        .card-title svg {
            width: 20px;
            height: 20px;
            fill: none;
            stroke: currentColor;
            stroke-width: 2;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .form-group {
            margin-bottom: 1rem;
        }
        
        label {
            display: block;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        input, select, textarea {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 0.65rem 0.85rem;
            color: var(--text-main);
            font-family: inherit;
            font-size: 0.9rem;
            transition: all 0.2s;
        }
        
        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(124, 58, 237, 0.2);
            background: rgba(0, 0, 0, 0.5);
        }
        
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn {
            width: 100%;
            border: none;
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            font-size: 0.9rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, #a78bfa 100%);
            color: #fff;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, var(--secondary) 0%, #22d3ee 100%);
            color: #050508;
            font-weight: 700;
        }
        
        .btn-secondary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
        }
        
        .btn-icon-danger {
            background: rgba(239, 68, 68, 0.1);
            color: var(--accent-red);
            border: 1px solid rgba(239, 68, 68, 0.2);
            padding: 0.35rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-icon-danger:hover {
            background: var(--accent-red);
            color: #fff;
            border-color: var(--accent-red);
        }
        
        .badge {
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-student {
            background: rgba(6, 182, 212, 0.1);
            color: var(--secondary);
            border: 1px solid rgba(6, 182, 212, 0.25);
        }
        
        .badge-teacher {
            background: rgba(124, 58, 237, 0.1);
            color: #a78bfa;
            border: 1px solid rgba(124, 58, 237, 0.25);
        }

        .badge-danger {
            background: rgba(239, 68, 68, 0.1);
            color: var(--accent-red);
            border: 1px solid rgba(239, 68, 68, 0.25);
        }
        
        .subscribers-list, .announcements-list {
            max-height: 250px;
            overflow-y: auto;
            padding-right: 0.25rem;
        }
        
        .subscribers-list::-webkit-scrollbar, 
        .announcements-list::-webkit-scrollbar,
        .terminal-box::-webkit-scrollbar {
            width: 4px;
        }
        
        .subscribers-list::-webkit-scrollbar-thumb, 
        .announcements-list::-webkit-scrollbar-thumb,
        .terminal-box::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        
        .subscriber-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 10px;
            margin-bottom: 0.6rem;
            transition: all 0.2s;
        }
        
        .subscriber-row:hover {
            background: rgba(255, 255, 255, 0.035);
            border-color: rgba(255, 255, 255, 0.06);
        }
        
        .sub-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        
        .sub-avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.85rem;
            color: #fff;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        .sub-details h4 {
            font-size: 0.85rem;
            font-weight: 600;
            color: #fff;
        }
        
        .sub-details p {
            font-size: 0.75rem;
            color: var(--text-muted);
        }
        
        .sub-actions {
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }
        
        .announcement-card {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            transition: all 0.2s;
        }
        
        .announcement-card:hover {
            border-color: rgba(6, 182, 212, 0.15);
            background: rgba(255, 255, 255, 0.035);
        }
        
        .ann-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .ann-header h3 {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--secondary);
        }
        
        .ann-meta {
            font-size: 0.75rem;
            color: var(--text-muted);
            display: flex;
            gap: 0.75rem;
        }
        
        .ann-body {
            font-size: 0.85rem;
            line-height: 1.4;
            color: var(--text-main);
        }
        
        .terminal-box {
            background: #040508;
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            font-family: 'Fira Code', monospace;
            font-size: 0.75rem;
            padding: 0.85rem;
            height: 200px;
            overflow-y: auto;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.8);
        }
        
        .log-entry {
            margin-bottom: 0.35rem;
            line-height: 1.3;
        }
        
        .log-time {
            color: #4b5563;
        }
        
        .log-level-info {
            color: var(--accent-green);
        }
        
        .log-level-warning {
            color: #fbbf24;
        }
        
        .log-level-error {
            color: var(--accent-red);
        }
        
        .log-msg {
            color: #9ca3af;
        }
        
        .empty-state {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-muted);
            font-size: 0.8rem;
        }
        
        .grid-right {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        
        .toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: rgba(10, 11, 18, 0.95);
            border: 1px solid var(--primary);
            border-radius: 10px;
            padding: 0.85rem 1.25rem;
            color: #fff;
            font-size: 0.85rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transform: translateY(150%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .toast.show {
            transform: translateY(0);
        }
        
        .toast-icon {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.7rem;
        }
        
        .toast-success {
            border-color: var(--accent-green);
        }
        
        .toast-success .toast-icon {
            background: var(--accent-green);
            color: #000;
        }
        
        .toast-error {
            border-color: var(--accent-red);
        }
        
        .toast-error .toast-icon {
            background: var(--accent-red);
            color: #fff;
        }
    </style>
</head>
<body>

    <header>
        <div class="header-title">
            <h1>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#gradient)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#a78bfa"/>
                            <stop offset="100%" stop-color="#22d3ee"/>
                        </linearGradient>
                    </defs>
                    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
                    <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
                </svg>
                Kampüs Duyuru Sistemi
            </h1>
            <p>Katmanlı Mimari (Layered Architecture) &amp; Nesne Yönelimli Tasarım Desenleri Canlı Kontrol Paneli</p>
        </div>
        <div class="badge-live">SİSTEM AKTİF</div>
    </header>

    <main>
        <!-- SOL PANEL: Girdiler ve Formlar -->
        <section>
            <!-- Form 1: Abone Ekle -->
            <div class="glass-card">
                <h2 class="card-title">
                    <svg viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2m11-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm8 2h6m-3-3v6" stroke-linecap="round"/></svg>
                    Yeni Abone Kaydı (Observer)
                </h2>
                <form id="form-subscribe">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="sub-id">Kullanıcı ID</label>
                            <input type="number" id="sub-id" placeholder="Örn: 101" required>
                        </div>
                        <div class="form-group">
                            <label for="sub-role">Rol / Tip</label>
                            <select id="sub-role" required>
                                <option value="student">Öğrenci</option>
                                <option value="teacher">Öğretmen</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="sub-name">Ad Soyad</label>
                        <input type="text" id="sub-name" placeholder="Örn: Ahmet Yılmaz" required>
                    </div>
                    <div class="form-group">
                        <label for="sub-email">E-Posta Adresi</label>
                        <input type="email" id="sub-email" placeholder="Örn: ahmet@universite.edu.tr" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="sub-phone">Telefon No (SMS)</label>
                            <input type="text" id="sub-phone" placeholder="Örn: 555-123-4567" required>
                        </div>
                        <div class="form-group">
                            <label for="sub-pref">Bildirim Tercihi</label>
                            <select id="sub-pref" required>
                                <option value="email">Sadece E-Posta</option>
                                <option value="sms">Sadece SMS</option>
                                <option value="both">Her İkisi de (E-Posta &amp; SMS)</option>
                            </select>
                        </div>
                    </div>
                    <button type="submit" class="btn btn-secondary">Abone Et (Attach)</button>
                </form>
            </div>

            <!-- Form 2: Duyuru Yayınla -->
            <div class="glass-card">
                <h2 class="card-title">
                    <svg viewBox="0 0 24 24"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zm-1-15h2v6h-2zm0 8h2v2h-2z" stroke-linecap="round"/></svg>
                    Duyuru Yayınla (Factory &amp; Publisher)
                </h2>
                <form id="form-publish">
                    <div class="form-group">
                        <label for="ann-title">Duyuru Başlığı</label>
                        <input type="text" id="ann-title" placeholder="Örn: Final Sınavları Hakkında" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="ann-author">Yazar (Öğretmen)</label>
                            <input type="text" id="ann-author" placeholder="Örn: Prof. Dr. Canan Kaya" required>
                        </div>
                        <div class="form-group">
                            <label for="ann-type">Duyuru Tipi (Factory)</label>
                            <select id="ann-type" required>
                                <option value="genel">Genel Duyuru (E-Posta)</option>
                                <option value="akademik">Akademik Duyuru (E-Posta)</option>
                                <option value="acil">Acil Duyuru (SMS Bildirimli 🚨)</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="ann-content">Duyuru İçeriği</label>
                        <textarea id="ann-content" placeholder="Kampüse iletilecek mesajı giriniz..." required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Yayınla ve Bildir (Publish)</button>
                </form>
            </div>
        </section>

        <!-- SAĞ PANEL: Canlı Listeler ve Terminal -->
        <section class="grid-right">
            <!-- Aktif Aboneler Listesi -->
            <div class="glass-card">
                <h2 class="card-title">
                    <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2m11-10a4 4 0 1 0 0-8 4 4 0 0 0 0 8z" stroke-linecap="round"/></svg>
                    Aktif Aboneler / Dinleyiciler
                </h2>
                <div class="subscribers-list" id="subscribers-container">
                    <div class="empty-state">Henüz kayıtlı bir abone (Observer) yok.</div>
                </div>
            </div>

            <!-- Son Duyurular -->
            <div class="glass-card">
                <h2 class="card-title">
                    <svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zM22 6l-10 7L2 6" stroke-linecap="round"/></svg>
                    Kampüs Duyuru Akışı
                </h2>
                <div class="announcements-list" id="announcements-container">
                    <div class="empty-state">Henüz yayınlanmış bir duyuru bulunmuyor.</div>
                </div>
            </div>

            <!-- Canlı Sistem Terminali (Loglayıcı) -->
            <div class="glass-card">
                <h2 class="card-title" style="color: var(--accent-green);">
                    <svg viewBox="0 0 24 24" style="stroke: var(--accent-green);"><path d="M4 17l6-6-6-6m8 14h8" stroke-linecap="round"/></svg>
                    Canlı Sistem Konsolu (Singleton Logger)
                </h2>
                <div class="terminal-box" id="terminal-container">
                    <div class="log-entry"><span class="log-time">[Canlı]</span> <span class="log-level-info">[SİSTEM]</span> <span class="log-msg">Konsol dinleme bağlantısı kuruldu.</span></div>
                </div>
            </div>
        </section>
    </main>

    <!-- Bildirim Balonu (Toast) -->
    <div id="toast" class="toast">
        <div class="toast-icon">✓</div>
        <div id="toast-text">İşlem başarıyla gerçekleştirildi.</div>
    </div>

    <!-- JavaScript Dinamik Arayüz Orkestrasyonu -->
    <script>
        const API_BASE = '/api';
        
        // Yardımcı Fonksiyon: Toast Göster
        function showToast(message, isSuccess = true) {
            const toast = document.getElementById('toast');
            const toastText = document.getElementById('toast-text');
            const toastIcon = toast.querySelector('.toast-icon');
            
            toastText.textContent = message;
            toast.className = 'toast ' + (isSuccess ? 'toast-success' : 'toast-error');
            toastIcon.textContent = isSuccess ? '✓' : '✗';
            
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        // 1. Veri Çekme: Aktif Aboneler
        async function loadSubscribers() {
            try {
                const res = await fetch(`${API_BASE}/subscribers`);
                const data = await res.json();
                const container = document.getElementById('subscribers-container');
                
                if (data.length === 0) {
                    container.innerHTML = '<div class="empty-state">Henüz kayıtlı bir abone (Observer) yok.</div>';
                    return;
                }
                
                container.innerHTML = data.map(sub => `
                    <div class="subscriber-row">
                        <div class="sub-info">
                            <div class="sub-avatar">${sub.name.charAt(0).toUpperCase()}</div>
                            <div class="sub-details">
                                <h4>${sub.name} (ID: ${sub.id})</h4>
                                <p>${sub.email} | 📱 ${sub.phone || 'Yok'}</p>
                                <p style="font-size: 0.72rem; color: #a78bfa; margin-top: 0.15rem; font-weight: 500;">
                                    Tercih: ${sub.notification_preference === 'both' ? 'E-POSTA & SMS' : sub.notification_preference.toUpperCase()}
                                </p>
                            </div>
                        </div>
                        <div class="sub-actions">
                            <span class="badge badge-${sub.role}">${sub.role === 'student' ? 'Öğrenci' : 'Öğretmen'}</span>
                            <button onclick="unsubscribeUser('${sub.email}')" class="btn-icon-danger" title="Aboneliği Sonlandır (Detach)">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="3 6 5 6 21 6"></polyline>
                                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                                    <line x1="10" y1="11" x2="10" y2="17"></line>
                                    <line x1="14" y1="11" x2="14" y2="17"></line>
                                </svg>
                            </button>
                        </div>
                    </div>
                `).join('');
            } catch (err) {
                console.error("Aboneler yüklenirken hata oluştu:", err);
            }
        }

        // 2. Veri Çekme: Duyurular
        async function loadAnnouncements() {
            try {
                const res = await fetch(`${API_BASE}/announcements`);
                const data = await res.json();
                const container = document.getElementById('announcements-container');
                
                if (data.length === 0) {
                    container.innerHTML = '<div class="empty-state">Henüz yayınlanmış bir duyuru bulunmuyor.</div>';
                    return;
                }
                
                container.innerHTML = data.map(ann => {
                    const date = new Date(ann.created_at).toLocaleTimeString('tr-TR', {hour: '2-digit', minute:'2-digit'});
                    
                    let typeBadgeClass = 'badge-student';
                    let typeLabel = 'Genel';
                    if (ann.type === 'akademik') {
                        typeBadgeClass = 'badge-teacher';
                        typeLabel = 'Akademik';
                    } else if (ann.type === 'acil') {
                        typeBadgeClass = 'badge-danger';
                        typeLabel = 'Acil 🚨';
                    }
                    
                    return `
                        <div class="announcement-card">
                            <div class="ann-header">
                                <h3>${ann.title}</h3>
                                <span class="badge ${typeBadgeClass}">${typeLabel}</span>
                            </div>
                            <div class="ann-body">${ann.content}</div>
                            <div class="ann-meta" style="margin-top: 0.75rem;">
                                <span>✍ Yazar: <b>${ann.author}</b></span>
                                <span>🕒 Saat: ${date}</span>
                            </div>
                        </div>
                    `;
                }).join('');
            } catch (err) {
                console.error("Duyurular yüklenirken hata oluştu:", err);
            }
        }

        // 3. Veri Çekme: Canlı Log Terminali (Singleton Logger)
        let lastLogCount = 0;
        async function loadLogs() {
            try {
                const res = await fetch(`${API_BASE}/logs`);
                const data = await res.json();
                const container = document.getElementById('terminal-container');
                
                container.innerHTML = data.map(log => {
                    let levelClass = 'log-level-info';
                    if (log.level === 'WARNING') levelClass = 'log-level-warning';
                    if (log.level === 'ERROR') levelClass = 'log-level-error';
                    
                    return `
                        <div class="log-entry">
                            <span class="log-time">[${log.timestamp}]</span>
                            <span class="${levelClass}">[${log.level}]</span>
                            <span class="log-msg">${log.message}</span>
                        </div>
                    `;
                }).join('');
                
                // Yeni log geldiyse aşağıya otomatik kaydır
                if (data.length > lastLogCount) {
                    container.scrollTop = container.scrollHeight;
                    lastLogCount = data.length;
                }
            } catch (err) {
                console.error("Loglar yüklenirken hata:", err);
            }
        }

        // 4. İşlem: Abone Ol (Attach)
        document.getElementById('form-subscribe').addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = parseInt(document.getElementById('sub-id').value);
            const role = document.getElementById('sub-role').value;
            const name = document.getElementById('sub-name').value;
            const email = document.getElementById('sub-email').value;
            const phone = document.getElementById('sub-phone').value;
            const notification_preference = document.getElementById('sub-pref').value;
            
            try {
                const res = await fetch(`${API_BASE}/subscribe`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ id, role, name, email, phone, notification_preference })
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    showToast(data.message, true);
                    document.getElementById('form-subscribe').reset();
                    loadSubscribers();
                    loadLogs();
                } else {
                    showToast(data.detail || "Kayıt eklenemedi.", false);
                }
            } catch (err) {
                showToast("Sunucu bağlantı hatası.", false);
            }
        });

        // 5. İşlem: Duyuru Yayınla (Publish)
        document.getElementById('form-publish').addEventListener('submit', async (e) => {
            e.preventDefault();
            const title = document.getElementById('ann-title').value;
            const author = document.getElementById('ann-author').value;
            const content = document.getElementById('ann-content').value;
            const announcement_type = document.getElementById('ann-type').value;
            
            try {
                const res = await fetch(`${API_BASE}/announcements`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ announcement_type, title, author, content })
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    showToast("Duyuru başarıyla yayınlandı!", true);
                    document.getElementById('form-publish').reset();
                    loadAnnouncements();
                    loadLogs();
                } else {
                    showToast(data.detail || "Duyuru yayınlanamadı.", false);
                }
            } catch (err) {
                showToast("Sunucu bağlantı hatası.", false);
            }
        });

        // 6. İşlem: Abonelikten Çıkar (Detach)
        async function unsubscribeUser(email) {
            if (!confirm(`E-posta adresi '${email}' olan aboneyi çıkarmak istediğinize emin misiniz?`)) return;
            
            try {
                const res = await fetch(`${API_BASE}/unsubscribe?email=${encodeURIComponent(email)}`, {
                    method: 'POST'
                });
                
                const data = await res.json();
                
                if (res.ok) {
                    showToast(data.message, true);
                    loadSubscribers();
                    loadLogs();
                } else {
                    showToast(data.detail || "Abonelikten çıkarılamadı.", false);
                }
            } catch (err) {
                showToast("Sunucu bağlantı hatası.", false);
            }
        }

        // Sayfa ilk yüklendiğinde ve periyodik olarak güncelle
        window.addEventListener('DOMContentLoaded', () => {
            loadSubscribers();
            loadAnnouncements();
            loadLogs();
            
            // Periyodik güncelleme zamanlayıcıları
            setInterval(loadLogs, 1500);         // Konsol hızlı güncellensin
            setInterval(loadSubscribers, 3000);  // Aboneler orta hızda güncellensin
            setInterval(loadAnnouncements, 3000); // Duyurular orta hızda güncellensin
        });
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    # Doğrudan python komutuyla çalıştırıldığında uvicorn sunucusunu başlatır
    uvicorn.run("campus_announcement_system.main:app", host="127.0.0.1", port=8000, reload=True)

