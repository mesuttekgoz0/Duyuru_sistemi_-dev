from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from campus_announcement_system.domain.interfaces import IObserver

class UserBase(BaseModel):
    """
    Sistemdeki kullanıcılar (Öğrenci ve Öğretmen) için ortak taban veri modelidir.
    """
    id: int
    name: str
    email: str
    role: str
    phone: str = Field(default="555-0000", description="Bildirim kanalı olarak kullanılacak telefon numarası")
    notification_preference: str = Field(default="email", description="Tercih edilen bildirim kanalı: 'email', 'sms' veya 'both'")

class Student(UserBase, IObserver):
    """
    Öğrenci veri modelidir. Aynı zamanda IObserver arayüzünü uygulayarak
    yeni duyurulardan bildirim alabilir.
    """
    role: str = Field(default="student")

    def update(self, announcement: Announcement) -> None:
        """
        Öğrenciye yeni duyuru ulaştığında tetiklenen metottur.
        Domain katmanında iş mantığı barındırılmaması gerektiğinden, gerçek bildirim
        gönderim ve loglama işlemleri üst katmanlarda yönetilecektir. Burası sadece
        Observer kontratını tamamlar.
        """
        pass

class Teacher(UserBase, IObserver):
    """
    Öğretmen veri modelidir. Duyuru yapabilmelerinin yanı sıra kendileri de
    diğer duyurulardan haberdar olmak için IObserver arayüzünü uygularlar.
    """
    role: str = Field(default="teacher")

    def update(self, announcement: Announcement) -> None:
        """
        Öğretmene yeni duyuru ulaştığında tetiklenen metottur.
        Observer kontratını tamamlar.
        """
        pass

class Announcement(BaseModel):
    """
    Kampüs içi duyuru veri modelidir.
    """
    id: int
    title: str
    content: str
    author: str  # Duyuruyu oluşturan öğretmenin adı
    type: str    # "genel", "akademik", "acil" vb.
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GeneralAnnouncement(Announcement):
    """
    Genel duyuru tipi. Varsayılan olarak tipi 'genel'dir.
    """
    type: str = Field(default="genel")

class AcademicAnnouncement(Announcement):
    """
    Akademik duyuru tipi. Varsayılan olarak tipi 'akademik'dir.
    """
    type: str = Field(default="akademik")

class UrgentAnnouncement(Announcement):
    """
    Acil duyuru tipi. Varsayılan olarak tipi 'acil'dir.
    """
    type: str = Field(default="acil")

