from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from campus_announcement_system.domain.models import Student, Teacher
from campus_announcement_system.application.announcement_service import AnnouncementPublisher

router = APIRouter()

# Uygulama genelinde durumu (aboneleri ve duyuruları) yöneten tekil Publisher örneği
publisher = AnnouncementPublisher()

class SubscribeRequest(BaseModel):
    """
    Kullanıcı abonelik isteği veri şeması.
    """
    id: int = Field(..., description="Kullanıcının benzersiz ID'si")
    name: str = Field(..., description="Kullanıcının adı")
    email: str = Field(..., description="Kullanıcının e-posta adresi")
    role: str = Field(..., description="Kullanıcı rolü: 'student' veya 'teacher'")
    phone: str = Field(default="555-0000", description="Telefon numarası (SMS bildirimleri için)")
    notification_preference: str = Field(default="email", description="Tercih edilen bildirim kanalı: 'email', 'sms' veya 'both'")

class PublishAnnouncementRequest(BaseModel):
    """
    Duyuru yayınlama isteği veri şeması.
    """
    announcement_type: str = Field(..., description="Duyuru tipi: 'genel', 'akademik', 'acil'")
    title: str = Field(..., description="Duyuru başlığı")
    content: str = Field(..., description="Duyuru içeriği")
    author: str = Field(..., description="Duyuruyu yayınlayan öğretmenin adı")

@router.post("/subscribe", status_code=201)
def subscribe(request: SubscribeRequest) -> Dict[str, str]:
    """
    Sisteme yeni bir gözlemci (Öğrenci veya Öğretmen) kaydeder.
    """
    role_lower = request.role.lower()
    
    if role_lower == "student":
        # Domain modelini oluştur
        observer = Student(
            id=request.id, 
            name=request.name, 
            email=request.email, 
            phone=request.phone,
            notification_preference=request.notification_preference
        )
    elif role_lower == "teacher":
        # Domain modelini oluştur
        observer = Teacher(
            id=request.id, 
            name=request.name, 
            email=request.email, 
            phone=request.phone,
            notification_preference=request.notification_preference
        )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Geçersiz rol tanımlandı. Sadece 'student' veya 'teacher' kabul edilir."
        )

    # Abone ekleme işlemini gerçekleştir
    publisher.attach(observer)
    return {"message": f"{request.name} ({request.role.upper()}) sisteme başarıyla abone oldu."}

@router.post("/unsubscribe", status_code=200)
def unsubscribe(email: str) -> Dict[str, str]:
    """
    E-posta adresine göre aboneyi sistemden çıkarır.
    """
    target_observer = None
    for observer in publisher._observers:
        # Pydantic modelinden email alanını kontrol et
        if getattr(observer, "email", None) == email:
            target_observer = observer
            break

    if not target_observer:
        raise HTTPException(
            status_code=404, 
            detail="Belirtilen e-posta adresine sahip aktif bir abone bulunamadı."
        )

    publisher.detach(target_observer)
    return {"message": f"{target_observer.name} abonelikten başarıyla ayrıldı."}

@router.post("/announcements", status_code=201)
def publish_announcement(request: PublishAnnouncementRequest) -> Dict[str, Any]:
    """
    Yeni bir duyuru yayınlar ve kayıtlı tüm abonelere bildirim gönderir.
    """
    announcement = publisher.publish_announcement(
        announcement_type=request.announcement_type,
        title=request.title,
        content=request.content,
        author=request.author
    )
    return {
        "message": "Duyuru başarıyla yayınlandı ve tüm abonelere bildirim gönderildi.",
        "announcement": announcement
    }

@router.get("/announcements", response_model=List[Any])
def get_announcements() -> List[Any]:
    """
    Yayınlanan tüm duyuruların geçmişini listeler.
    """
    return publisher.get_announcements()

@router.get("/subscribers", response_model=List[Dict[str, Any]])
def get_subscribers() -> List[Dict[str, Any]]:
    """
    Sisteme kayıtlı aktif tüm aboneleri listeler.
    """
    return [
        {
            "id": getattr(obs, "id", None),
            "name": getattr(obs, "name", None),
            "email": getattr(obs, "email", None),
            "role": getattr(obs, "role", None),
            "phone": getattr(obs, "phone", None),
            "notification_preference": getattr(obs, "notification_preference", None)
        }
        for obs in publisher._observers
    ]

@router.get("/logs", response_model=List[Dict[str, str]])
def get_logs() -> List[Dict[str, str]]:
    """
    Sistem loglarının son 100 kaydını döner.
    """
    from campus_announcement_system.infrastructure.logger import Logger
    return Logger().logs_history

