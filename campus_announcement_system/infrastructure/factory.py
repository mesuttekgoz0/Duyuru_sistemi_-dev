from __future__ import annotations
from datetime import datetime
from campus_announcement_system.domain.models import (
    Announcement,
    GeneralAnnouncement,
    AcademicAnnouncement,
    UrgentAnnouncement
)
from campus_announcement_system.domain.interfaces import INotification
from campus_announcement_system.infrastructure.notifications import EmailNotification, SMSNotification

class AnnouncementFactory:
    """
    Duyuru nesnelerinin üretim sürecini soyutlayan Factory sınıfıdır.
    """
    _id_counter: int = 1

    @classmethod
    def create_announcement(
        cls, 
        announcement_type: str, 
        title: str, 
        content: str, 
        author: str
    ) -> Announcement:
        """
        Duyuru tipine göre ilgili somut Announcement alt sınıf nesnesini oluşturur.
        
        Args:
            announcement_type (str): "genel", "akademik" veya "acil" duyuru kanalı.
            title (str): Duyuru başlığı.
            content (str): Duyuru içeriği.
            author (str): Duyuruyu yayımlayan öğretmenin adı.
            
        Returns:
            Announcement: Üretilen somut duyuru nesnesi.
        """
        type_lower = announcement_type.lower()
        if type_lower == "genel":
            announcement_class = GeneralAnnouncement
        elif type_lower == "akademik":
            announcement_class = AcademicAnnouncement
        elif type_lower == "acil":
            announcement_class = UrgentAnnouncement
        else:
            raise ValueError(f"Desteklenmeyen duyuru tipi: {announcement_type}")

        announcement = announcement_class(
            id=cls._id_counter,
            title=title,
            content=content,
            author=author,
            created_at=datetime.utcnow()
        )
        cls._id_counter += 1
        return announcement

class NotificationFactory:
    """
    Bildirim nesnelerinin (Email, SMS) üretim sürecini soyutlayan Factory sınıfıdır.
    """
    @staticmethod
    def create_notification(
        notification_type: str, 
        recipient: str, 
        content: str, 
        title: str = "Yeni Duyuru"
    ) -> INotification:
        """
        İstenen bildirim tipine göre ilgili somut INotification nesnesini oluşturur.
        
        Args:
            notification_type (str): "email" veya "sms" gibi bildirim kanalı.
            recipient (str): Alıcı bilgisi (e-posta adresi veya telefon numarası).
            content (str): Bildirim metni.
            title (str): Bildirim başlığı (e-postalar için).
            
        Returns:
            INotification: Üretilen somut bildirim nesnesi.
            
        Raises:
            ValueError: Bilinmeyen bir bildirim türü istenirse fırlatılır.
        """
        type_lower = notification_type.lower()
        if type_lower == "email":
            return EmailNotification(recipient=recipient, subject=title, body=content)
        elif type_lower == "sms":
            return SMSNotification(phone_number=recipient, message=f"{title}: {content}")
        else:
            raise ValueError(f"Desteklenmeyen bildirim tipi: {notification_type}")
