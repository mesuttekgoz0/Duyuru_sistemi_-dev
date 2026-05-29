from __future__ import annotations
from typing import List
from campus_announcement_system.domain.interfaces import IPublisher, IObserver
from campus_announcement_system.domain.models import Announcement
from campus_announcement_system.infrastructure.logger import Logger
from campus_announcement_system.infrastructure.factory import AnnouncementFactory, NotificationFactory

class AnnouncementPublisher(IPublisher):
    """
    Observer tasarım deseninin somut Publisher (Subject) sınıfıdır.
    Abonelik işlemlerini yönetir ve yeni duyuruları tüm abonelere bildirir.
    """
    def __init__(self) -> None:
        self._observers: List[IObserver] = []
        self._announcements: List[Announcement] = []
        self._logger: Logger = Logger()

    def attach(self, observer: IObserver) -> None:
        """
        Sisteme yeni bir kullanıcı (öğrenci/öğretmen) abone eder.
        """
        if observer not in self._observers:
            self._observers.append(observer)
            self._logger.info(f"Yeni abone eklendi: {observer.name} ({observer.role.upper()})")

    def detach(self, observer: IObserver) -> None:
        """
        Kullanıcıyı abonelikten çıkarır.
        """
        if observer in self._observers:
            self._observers.remove(observer)
            self._logger.info(f"Abone sistemden ayrıldı: {observer.name}")

    def notify(self, announcement: Announcement) -> None:
        """
        Kayıtlı tüm aboneleri yeni duyurudan haberdar eder.
        Duyuru tipine ve abonenin kişisel bildirim tercihlerine göre (E-posta, SMS veya Her İkisi) bildirim gönderilir.
        """
        self._logger.info(f"Tüm abonelere bildirim gönderiliyor: '{announcement.title}' (Tip: {announcement.type.upper()})")
        for observer in self._observers:
            # Domain katmanındaki soyut güncellemeyi tetikle
            observer.update(announcement)
            
            # Abonenin kişisel bildirim tercihini al
            pref = getattr(observer, "notification_preference", "email").lower()
            
            # Gönderilecek kanalları belirle
            channels = []
            if announcement.type == "acil":
                # Acil duyurularda SMS her koşulda gönderilir. Kullanıcı e-posta da istiyorsa o da eklenir.
                channels.append("sms")
                if pref in ("email", "both"):
                    channels.append("email")
            else:
                # Normal duyurularda kullanıcının tercihine saygı duyulur
                if pref == "both":
                    channels.extend(["email", "sms"])
                else:
                    channels.append(pref)
            
            # Belirlenen tüm kanallardan bildirimi gönder (tekilleştirerek)
            for channel in set(channels):
                recipient = getattr(observer, "phone", "555-0000") if channel == "sms" else getattr(observer, "email", "")
                try:
                    notification = NotificationFactory.create_notification(
                        notification_type=channel,
                        recipient=recipient,
                        content=announcement.content,
                        title=f"Duyuru ({announcement.type.upper()}): {announcement.title}"
                    )
                    notification.send()
                except Exception as e:
                    self._logger.error(f"{observer.name} için {channel.upper()} bildirimi gönderilemedi: {str(e)}")

    def publish_announcement(self, announcement_type: str, title: str, content: str, author: str) -> Announcement:
        """
        Yeni bir duyuru oluşturur, listeye kaydeder ve tüm abonelere duyurur.
        
        Args:
            announcement_type (str): Duyurunun tipi ("genel", "akademik", "acil").
            title (str): Duyuru başlığı.
            content (str): Duyuru içeriği.
            author (str): Duyuruyu hazırlayan öğretmenin adı.
            
        Returns:
            Announcement: Üretilen somut duyuru nesnesi.
        """
        self._logger.info(f"Yeni duyuru oluşturuluyor -> Tip: {announcement_type}, Yazar: {author}, Başlık: {title}")
        
        # Factory kullanarak duyuru nesnesini üret
        announcement = AnnouncementFactory.create_announcement(
            announcement_type=announcement_type,
            title=title,
            content=content,
            author=author
        )
        
        self._announcements.append(announcement)
        self._logger.info(f"Duyuru başarıyla kaydedildi (ID: {announcement.id})")
        
        # Observer deseni ile aboneleri bilgilendir
        self.notify(announcement)
        
        return announcement

    def get_announcements(self) -> List[Announcement]:
        """
        Yayınlanan tüm duyuruların listesini döner.
        """
        return self._announcements
