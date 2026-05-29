from campus_announcement_system.domain.interfaces import INotification
from campus_announcement_system.infrastructure.logger import Logger

class EmailNotification(INotification):
    """
    E-posta bildirim gönderimini simüle eden sınıftır.
    """
    def __init__(self, recipient: str, subject: str, body: str) -> None:
        self.recipient: str = recipient
        self.subject: str = subject
        self.body: str = body
        self._logger: Logger = Logger()

    def send(self) -> None:
        """
        E-posta gönderme işlemini simüle eder ve loglar.
        """
        self._logger.info(
            f"Email Gönderildi -> Alıcı: {self.recipient} | Konu: {self.subject} | İçerik: {self.body[:40]}..."
        )

class SMSNotification(INotification):
    """
    SMS bildirim gönderimini simüle eden sınıftır.
    """
    def __init__(self, phone_number: str, message: str) -> None:
        self.phone_number: str = phone_number
        self.message: str = message
        self._logger: Logger = Logger()

    def send(self) -> None:
        """
        SMS gönderme işlemini simüle eder ve loglar.
        """
        self._logger.info(
            f"SMS Gönderildi -> Telefon: {self.phone_number} | Mesaj: {self.message[:40]}..."
        )
