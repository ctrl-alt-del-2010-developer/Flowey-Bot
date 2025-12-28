# Flowey-Bot
🌻 UnderNet: Flowey OS - Interaktif Chatbot

UnderNet, Undertale dünyasının en tekinsiz karakteri Flowey'i masaüstünüze getiren, Python ve PyQt5 ile geliştirilmiş interaktif bir terminal projesidir. Proje, Flowey'nin değişken ruh hallerini, öğrenme yeteneğini ve ikonik daktilo sesli konuşma stilini simüle eder.
🌟 Öne Çıkan Özellikler

    Dinamik Karakter Kişiliği: Flowey, girdiğiniz kelimelere göre "Arkadaş Canlısı" veya "Korkunç" modları arasında geçiş yapar.

    Akıllı Müzik ve Ses Yönetimi:

        QMediaPlayer ile kesintisiz arka plan müziği.

        Ruh Modu: "Ruh" kelimesi geçtiğinde müzik aniden kesilir, arayüz kırmızıya döner ve korkutucu ses efektleri (flowey_evil.mp3) devreye girer.

        Pygame Mixer sayesinde her cevap başında gecikmesiz ses tetikleme.

    Gelişmiş Hafıza Sistemi: bilgi_bankasi.json dosyası üzerinden botun bilmediği kelimeleri ona öğretebilirsiniz.

    Retro Terminal Arayüzü: Undertale estetiğine uygun fontlar, daktilo yazı efekti ve animasyonlu GIF desteği.

    Config Menüsü: Kullanıcı arayüzü üzerinden ses seviyesi ve yazı hızı gibi ayarları gerçek zamanlı değiştirme imkanı.

🛠️ Kurulum ve Gereksinimler

Projeyi çalıştırmak için aşağıdaki Python kütüphanelerinin yüklü olması gerekir:
Bash

pip install PyQt5 pygame

Klasör Yapısı

Projenin düzgün çalışması için dosyaların şu şekilde dizilmesi önerilir:
Plaintext

📂 ProjectRoot
 ├── 📄 main.py               # Ana uygulama kodu
 ├── 📄 bilgi_bankasi.json    # Botun kelime hafızası (Otomatik oluşturulur)
 ├── 🖼️ flowey.gif            # Flowey animasyonu
 ├── 🎵 flowey_theme.mp3      # Arka plan müziği
 ├── 🎵 floweyspeak.mp3       # Normal konuşma sesi
 └── 🎵 flowey_evil.mp3       # Korkunç mod ses dosyası

🎮 Nasıl Kullanılır?

    python main.py komutuyla uygulamayı başlatın.

    Alt kısımdaki giriş satırına Flowey ile konuşmak istediğiniz kelimeleri yazın.

    Özel Komutlar:

        ruh, öldür, ölüm: Flowey'nin karanlık yüzünü uyandırır ve müziği durdurur.

        reset: Hafızadaki geçici verileri kontrol eder.

        Öğretme: Bot bir kelimeyi bilmiyorsa size "Ne demeliyim?" diye sorar. Yazdığınız bir sonraki cevap hafızaya kaydedilir.

🏗️ Teknik Detaylar

    GUI: PyQt5 (QVBoxLayout, QTimer, QMovie).

    Audio: Pygame (SFX için) ve QtMultimedia (BGM için).

    Veri Yönetimi: JSON (Sözlük tabanlı veri depolama).

    Multithreading: Ses dosyalarının arayüzü dondurmaması için threading modülü kullanılmıştır.

⚠️ Lisans ve Uyarı

Bu proje bir hayran çalışmasıdır (Fan-made). Karakter tasarımları, ses efektleri ve hikaye öğeleri Toby Fox (Undertale) mülkiyetindedir. Ticari amaçla kullanılamaz.

Flowey OS hakkında başka bir dökümantasyon veya geliştirme planın var mı?
