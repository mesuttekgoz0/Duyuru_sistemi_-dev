# Proje Kuralları (Campus Announcement System)

Bu dosya, yapay zeka asistanının projeye kod üretirken kesinlikle uyması gereken kuralları içerir.

## 1. İletişim ve Çıktı Kuralları
* **Bağlam Sağlama, Zincirleme Düşünce Kullan:** Uzun ve teorik metinler yazmaktan kaçın. Kodu üretmeden önce, yapacağın işlemin mantığını ve neden o tasarım desenini seçtiğini "Zincirleme Düşünce" (Chain of Thought) adımlarıyla kısa ve net bir şekilde açıkla. Ardından doğrudan kodu ver.
* Kod bloklarında her zaman type hinting (örneğin: `name: str`) kullan.

## 2. Mimari Kurallar
Proje kesinlikle **Katmanlı Mimari (Layered Architecture)** standartlarına uymalıdır. Katmanlar arası bağımlılıklar tek yönlü olmalıdır (Presentation -> Application -> Domain).
* `domain/`: Sadece interface'ler (ABC) ve temel veri modelleri (Pydantic/Dataclass) yer almalıdır. İş mantığı içermemelidir.
* `infrastructure/`: Dış dünya simülasyonları, loglama ve nesne üretim fabrikaları burada yer almalıdır.
* `application/`: Sadece iş akışı (use cases) ve Observer pattern'in abonelik/bildirim süreçleri yönetilmelidir.
* `presentation/`: Sadece FastAPI router ve endpoint'lerini içermelidir. İş mantığı burada yazılmamalıdır.

## 3. Tasarım Desenleri (Design Patterns)
Aşağıdaki 3 desenin kullanımı zorunludur ve doğru katmanlarda uygulanmalıdır:
* **Singleton Pattern:** `infrastructure/logger.py` içinde sistem loglarını konsola yazdırmak için kullanılacaktır.
* **Factory Pattern:** `infrastructure/factory.py` içinde `AnnouncementFactory` ve `NotificationFactory` olarak, nesne yaratım süreçlerini soyutlamak için kullanılacaktır.
* **Observer Pattern:** `application/announcement_service.py` içinde `AnnouncementPublisher` sınıfı ile kullanılacak, öğrenci ve öğretmen nesneleri (`IObserver` uygulayan) bu yapıya abone edilecektir.