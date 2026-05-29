from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from campus_announcement_system.domain.models import Announcement

class IObserver(ABC):
    """
    Observer tasarım deseninin dinleyici (Subscriber) arayüzüdür.
    Sistemde duyuru yapıldığında bildirim alacak sınıflar (Öğrenci, Öğretmen) bu arayüzü uygular.
    """
    @abstractmethod
    def update(self, announcement: Announcement) -> None:
        """
        Yeni bir duyuru yayınlandığında tetiklenecek olan güncelleme metodudur.
        
        Args:
            announcement (Announcement): Yayınlanan duyuru nesnesi.
        """
        pass

class IPublisher(ABC):
    """
    Observer tasarım deseninin yayıncı (Subject/Publisher) arayüzüdür.
    Duyuruların yönetimini ve abonelerin (observers) bilgilendirilmesini sağlar.
    """
    @abstractmethod
    def attach(self, observer: IObserver) -> None:
        """
        Sisteme yeni bir abone ekler.
        
        Args:
            observer (IObserver): Abone olacak gözlemci nesne.
        """
        pass

    @abstractmethod
    def detach(self, observer: IObserver) -> None:
        """
        Sistemden bir aboneyi çıkarır.
        
        Args:
            observer (IObserver): Abonelikten çıkacak gözlemci nesne.
        """
        pass

    @abstractmethod
    def notify(self, announcement: Announcement) -> None:
        """
        Kayıtlı tüm abonelere yeni duyuruyu bildirir.
        
        Args:
            announcement (Announcement): Yayınlanan duyuru nesnesi.
        """
        pass

class INotification(ABC):
    """
    Notification nesneleri için soyut arayüzdür.
    Factory deseni ile üretilecek farklı bildirim kanallarının (Email, SMS vb.)
    ortak bir arayüze sahip olmasını sağlar.
    """
    @abstractmethod
    def send(self) -> None:
        """
        Bildirimi ilgili alıcıya iletir.
        """
        pass
