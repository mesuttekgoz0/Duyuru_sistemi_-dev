# 🎓 Kampüs Duyuru Sistemi (Campus Announcement System)

Bu proje, modern yazılım mimarisi prensiplerine (SOLID, OOP, Clean Code) ve **Katmanlı Mimari (Layered Architecture)** standartlarına uygun olarak tasarlanmış, FastAPI tabanlı dinamik bir kampüs duyuru yönetimi ve gerçek zamanlı bildirim simülasyon sistemidir.

Projede **Singleton**, **Factory** ve **Observer** olmak üzere 3 temel GoF (Gang of Four) Tasarım Deseni uçtan uca uygulanmış ve etkileşimli bir **Glassmorphic Ön Yüz Kontrol Paneli (Dashboard)** ile taçlandırılmıştır.

---

## 🏗️ Mimari Tasarım (Layered Architecture)

Proje, katmanlar arası bağımlılıkların kesinlikle tek yönlü (`Presentation -> Application -> Domain`) olduğu katı bir katmanlı mimari yapısına sahiptir:

1. **`domain/` (Domain Katmanı):**
   * Sistemin en iç katmanıdır; dış katmanlardan tamamen izoledir.
   * Soyut kontratları/arayüzleri (`interfaces.py`) ve temel veri modellerini (`models.py`) barındırır.
   * Kesinlikle iş mantığı (business logic) veya dış dünyaya (veri tabanı, loglama vb.) ait kod içermez.

2. **`infrastructure/` (Altyapı Katmanı):**
   * Dış dünya ile iletişim, simülasyonlar (SMS/E-posta gönderimi), nesne üretim fabrikaları ve loglama sistemini barındırır.
   * `logger.py`, `factory.py` ve `notifications.py` bu katmanda yer alır.

3. **`application/` (Uygulama Katmanı):**
   * Sistemin iş akışlarını (use cases) ve orkestrasyonunu üstlenir.
   * Gözlemcilerin abonelik yönetimini ve duyuru yayınlandığında tetiklenen çok kanallı Observer orkestrasyonunu yönetir.

4. **`presentation/` (Sunum Katmanı):**
   * İstemci isteklerini karşılayan, girdi doğrulamalarını (Pydantic şemaları) üstlenen FastAPI APIRouter uç noktalarını barındırır.

---

## 🎨 Tasarım Desenleri (Design Patterns)

### 1. Singleton Pattern (Sistem Günlükçüsü / Logger)
* **Konum:** `infrastructure/logger.py`
* **Amaç:** Sistem genelinde sadece tek bir aktif logger nesnesinin olmasını garanti eder.
* **Tasarım:** Çoklu iş parçacığı (multithreading) ortamlarında güvenli çalışabilmesi için `threading.Lock()` ile çift kontrollü kilitleme (**thread-safe double-checked locking**) uygulanmıştır. Ayrıca ön yüzde canlı sistem akışını izleyebilmek için son 100 logu in-memory saklar.

### 2. Factory Pattern (Duyuru ve Bildirim Nesnesi Üretimi)
* **Konum:** `infrastructure/factory.py`
* **Duyuru Fabrikası (`AnnouncementFactory`):** İstemcinin seçtiği tipe göre (`genel`, `akademik`, `acil`) domain katmanındaki somut alt sınıfları (`GeneralAnnouncement`, `AcademicAnnouncement`, `UrgentAnnouncement`) dinamik olarak türetir.
* **Bildirim Fabrikası (`NotificationFactory`):** Belirlenen kanala göre (`email` veya `sms`) somut bildirim sınıflarını (`EmailNotification`, `SMSNotification`) polimorfik olarak örnekler.

### 3. Observer Pattern (Abonelik ve Bildirim Dağıtımı)
* **Konum:** `application/announcement_service.py` & `domain/interfaces.py`
* **Açıklama:** Öğrenciler (`Student`) ve Öğretmenler (`Teacher`), `IObserver` soyut sınıfını uygulayarak sisteme kayıt olurlar. `AnnouncementPublisher` (`IPublisher` uygulayan) yeni bir duyuru yayınladığında, tüm aboneleri sırasıyla bilgilendirir.
* **Akıllı Bildirim Tercihi:** Her abone kendi bildirim kanalını (`Sadece E-posta`, `Sadece SMS`, `Her İkisi`) özgürce seçebilir. Acil durumlarda (`acil` duyurular) ise sistem, güvenlik gereği abonenin tercihi ne olursa olsun SMS bildirimini zorunlu kılar.

---

## 💻 Canlı Kontrol Paneli (Interactive Dashboard)

Uygulamanın kök dizininde (`/`) sunulan modern ve göz kamaştırıcı ön yüz kontrol paneli, tamamen asenkron (AJAX - Fetch API) olarak çalışır:
* **Yeni Abone Girişi (Observer):** Rol (Öğrenci/Öğretmen), Telefon, E-Posta ve Kişisel Bildirim kanalı tercihiyle anlık abone ekleme.
* **Duyuru Yayınlama (Factory & Publisher):** 3 farklı tipte duyuru oluşturma ve Observer tetikleme.
* **Gözlemci Listesi:** Aktif abonelerin, profil kartları ve kişisel tercihleriyle birlikte canlı listelenmesi; tek tıkla abonelikten çıkarma (`Detach`).
* **Canlı Sistem Konsolu:** Singleton Logger'ın arka planda ürettiği simüle edilmiş E-Posta ve SMS gönderim çıktılarını 1.5 saniyede bir poll ederek ekrana yansıtan canlı terminal paneli.

---

## 🚀 Adım Adım Kurulum ve Çalıştırma

Sistemi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla takip ediniz:

### 1. Adım: Proje Dizinine Giriş
Komut satırınızı (Terminal, PowerShell veya CMD) açın ve projenin kök dizinine gidin:
```bash
cd "c:\Users\mesut\OneDrive\Desktop\Duyuru_sistemi_ödev"
```

### 2. Adım: Gerekli Kütüphanelerin Yüklenmesi
FastAPI ve sunucu bağımlılıklarını Python ortamınıza yükleyin:
```bash
python -m pip install fastapi uvicorn pydantic
```

### 3. Adım: Uygulamayı Başlatma
Projenin sahip olduğu dahili çalıştırıcı sayesinde sunucuyu tek bir komutla başlatabilirsiniz:
```bash
python campus_announcement_system/main.py
```
*(Alternatif olarak `python -m uvicorn campus_announcement_system.main:app --reload` komutu ile de başlatabilirsiniz).*

### 4. Adım: Dashboard'a Giriş Yapma
Sunucunuz başarıyla ayağa kalktığında terminalinizde `SİSTEM AKTİF` loglarını göreceksiniz. Tarayıcınızı açın ve kontrol paneline gidin:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Örnek Test Senaryosu (Observer & Factory Akışı)

Tasarım desenlerinin gücünü gözlemlemek için tarayıcınızda açtığınız Dashboard üzerinde şu adımları deneyin:

1. **Abone Ekleme:**
   * **Öğrenci 1:** Ahmet Yılmaz, `ahmet@edu.tr`, `555-101-2020`, Bildirim Tercihi: `Sadece E-Posta`
   * **Öğrenci 2:** Zeynep Kaya, `zeynep@edu.tr`, `555-303-4040`, Bildirim Tercihi: `Sadece SMS`
   * **Öğretmen 1:** Canan Çelik, `canan@edu.tr`, `555-808-9090`, Bildirim Tercihi: `Her İkisi de`

2. **Genel Duyuru Yayınlama:**
   * Başlık: *Kütüphane Çalışma Saatleri*
   * Yazar: *Kütüphane Daire Başkanlığı*
   * Tip: **Genel Duyuru** seçin.
   * *Canlı terminalde Ahmet'e E-posta, Zeynep'e SMS ve Canan Hoca'ya hem E-posta hem SMS gönderildiğini anlık olarak izleyin.*

3. **Acil Duyuru Yayınlama:**
   * Başlık: *Hava Durumu Uyarısı*
   * Yazar: *Rektörlük*
   * Tip: **Acil Duyuru (SMS Bildirimli 🚨)** seçin.
   * *Zeynep zaten SMS seçtiği için sadece SMS alır. Ahmet sadece E-posta seçmiş olmasına rağmen acil durum politikası gereği hem SMS hem E-posta alır. Canan Hoca her iki kanaldan da uyarılır.*
