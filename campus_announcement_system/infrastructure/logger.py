from __future__ import annotations
import threading
from datetime import datetime

class Logger:
    """
    Sistem loglarını yöneten Singleton sınıfıdır.
    Uygulama genelinde tek bir logger örneğinin bulunmasını garanti eder.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs) -> Logger:
        """
        Thread-safe (iş parçacığı güvenli) Singleton implementasyonu.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Logger, cls).__new__(cls)
                    # Canlı terminal arayüzü için log geçmişi listesini başlatıyoruz
                    cls._instance.logs_history = []
        return cls._instance

    def _log(self, level: str, message: str) -> None:
        """
        Log mesajını konsola standart bir biçimde yazdırır ve canlı terminal arayüzü için listeye ekler.
        """
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        print(log_entry)
        
        # Log nesnesini listeye ekle
        self.logs_history.append({
            "timestamp": timestamp,
            "level": level.upper(),
            "message": message
        })
        
        # Son 100 logdan fazlasını silerek bellek sızıntısını önleriz
        if len(self.logs_history) > 100:
            self.logs_history.pop(0)

    def info(self, message: str) -> None:
        """INFO düzeyinde log kaydeder."""
        self._log("INFO", message)

    def warning(self, message: str) -> None:
        """WARNING düzeyinde log kaydeder."""
        self._log("WARNING", message)

    def error(self, message: str) -> None:
        """ERROR düzeyinde log kaydeder."""
        self._log("ERROR", message)
