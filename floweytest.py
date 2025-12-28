import sys
import os
import json
import threading
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit,
                             QLineEdit, QLabel, QPushButton, QHBoxLayout,
                             QSlider, QDialog, QFrame)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QMovie, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from playsound import playsound

# --- CONFIG (AYARLAR) MENÜSÜ ---
class ConfigMenu(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("UnderNet - Sistem Ayarları")
        self.setFixedSize(300, 400)
        self.setStyleSheet("background-color: #000; color: white; border: 2px solid #ffff00;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("SİSTEM YAPILANDIRMASI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffff00; border: none; margin-bottom: 10px;")
        layout.addWidget(title)

        # Müzik Kontrol
        layout.addWidget(QLabel("MÜZİK DURUMU:"))
        self.btn_muzik = QPushButton("MÜZİĞİ SUSTUR" if self.parent.muzik_caliyor else "MÜZİĞİ BAŞLAT")
        self.btn_muzik.setStyleSheet("background-color: #222; color: white; padding: 8px; border: 1px solid white;")
        self.btn_muzik.clicked.connect(self.toggle_muzik)
        layout.addWidget(self.btn_muzik)

        # Ses Seviyesi
        layout.addWidget(QLabel("\nSES SEVİYESİ:"))
        self.slider_ses = QSlider(Qt.Horizontal)
        self.slider_ses.setRange(0, 100)
        self.slider_ses.setValue(self.parent.ses_seviyesi)
        self.slider_ses.valueChanged.connect(self.set_volume)
        layout.addWidget(self.slider_ses)

        # Yazı Hızı
        layout.addWidget(QLabel("\nYAZI HIZI (Düşük = Daha Hızlı):"))
        self.slider_hiz = QSlider(Qt.Horizontal)
        self.slider_hiz.setRange(5, 150)
        self.slider_hiz.setValue(self.parent.yazi_hizi)
        self.slider_hiz.valueChanged.connect(self.set_speed)
        layout.addWidget(self.slider_hiz)

        layout.addStretch()

        btn_kapat = QPushButton("AYARLARI KAYDET VE ÇIK")
        btn_kapat.setStyleSheet("background-color: #ffff00; color: black; font-weight: bold; padding: 10px;")
        btn_kapat.clicked.connect(self.close)
        layout.addWidget(btn_kapat)

        self.setLayout(layout)

    def toggle_muzik(self):
        self.parent.muzik_duraklat_devam()
        self.btn_muzik.setText("MÜZİĞİ SUSTUR" if self.parent.muzik_caliyor else "MÜZİĞİ BAŞLAT")

    def set_volume(self, val):
        self.parent.ses_seviyesi = val
        self.parent.player.setVolume(val)

    def set_speed(self, val):
        self.parent.yazi_hizi = val

# --- ANA FLOWEY BOT ---
class FloweyBot(QWidget):
    def __init__(self):
        super().__init__()
        self.dosya_adi = "bilgi_bankasi.json"
        self.ses_dosyasi = "floweyspeak.mp3"
        self.muzik_dosyasi = "flowey_theme.mp3"
        self.gif_yolu = "flowey.gif"

        # Default Ayarlar
        self.ses_seviyesi = 50
        self.yazi_hizi = 40
        self.muzik_caliyor = False
        self.ogrenme_modu = False
        self.son_bilinmeyen_soru = ""
        self.tam_mesaj = ""
        self.mevcut_indeks = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.harf_ekle)
        self.player = QMediaPlayer()

        self.hafizayi_yukle()
        self.initUI()
        self.muzik_baslat()

    def hafizayi_yukle(self):
        # TÜM EN DİP VE KLASİK REPLİKLER
        self.bilgi_bankasi = {
            # --- KLASİKLER ---
            "selam": "Selam! Ben Flowey! Çiçek Flowey!",
            "merhaba": "Selamın aleyküm! (Tekin olmayan bir gülümseme)",
            "nasılsın": "Ruhsuz bir çiçek ne kadar iyi olabilirse o kadar iyiyim.",
            "ismin ne": "Bana 'Flowey' de. Ama eski adımı merak ediyorsan... Hayır, vazgeçtim.",
            "salak": "Bana mı dedin? Bir çiçekle konuştuğunun farkındasın, değil mi?",

            # --- VAROLUŞSAL VE DERİN KONULAR ---
            "hiçlik": "Hiçlik... Ne his, ne acı, ne de sevgi. Sadece sonsuz bir boşluk. Benim içim tam olarak bu.",
            "acı": "Acı çekmek mi? Canavarlar acı çeker. İnsanlar acı çeker. Ama ben? Ben sadece izlerim.",
            "duygu": "Duygular sadece beynindeki kimyasal hatalardır. Ben o hatalardan kurtuldum. Artık özgürüm.",
            "ölüm": "Ölmek mi? Kaç kez öldüğümü unuttum. Ama her seferinde o 'parlak ışığı' görüp geri dönüyorum. Çok sıkıcı.",
            "anlam": "Hayatın bir anlamı olduğunu mu sanıyorsun? Sadece sayılar ve istatistiklerden ibaretiz.",
            "merhamet": "Merhamet, güçsüzlerin kendini iyi hissetmek için uydurduğu bir yalandır. Gerçek dünyada merhamet seni öldürtür.",
            "ruhsuz": "Bir ruhun olmadan sevemezsin. Denemedim mi sanıyorsun? Babamı sevmeye çalıştım, annemi sevmeye çalıştım... Ama içimde koca bir delik vardı.",

            # --- OYUNCU VE META-FİZİK (4. Duvar) ---
            "sen kimsin": "Ben senin merakının bir ürünüyüm. Sen bu soruları sormasaydın, ben de burada olmazdım.",
            "beni duyuyor musun": "Seni sadece duymuyorum, seçimlerini görüyorum. O klavyeye basan parmaklarını hissediyorum.",
            "kontrol": "İpleri senin tuttuğunu mu sanıyorsun? Belki de ben seni burada tutmak için bu cevapları veriyorumdur.",
            "gerçeklik": "Bu dünya mı daha gerçek, yoksa senin yaşadığın o 'dış dünya' mı? İkimiz de birer sistemin içindeyiz.",
            "reset": "Reset mi? Her şeyi silip baştan başlamak... Tüm o anıları yok etmek... YAP DA GÖRELİM!",
            "save": "Senin 'Kayıt' dosyan benim elimde olsaydı neler yapardım tahmin bile edemezsin.",

            # --- KARAKTERLER VE HİKAYE ---
            "sans": "O kemik yığını... Gözlerindeki o ışık... Ondan nefret ediyorum. Çok sinir bozucu.",
            "asriel": "O ağlak çocuğu unut. O zayıftı. Ben onun olması gereken haliyim: Saf mantık ve güç.",
            "chara": "Sen misin? Gerçekten geri mi döndün? En iyi arkadaşım...",
            "toriel": "O yaşlı keçi hala herkesi koruyabileceğini sanıyor. Ne acınası.",
            "asgore": "O aptal kral... Hala bir çözüm bulabileceğini sanıyor. Tek çözüm benim!",
            "öldür": "İşte bu! Öldür ya da öldürül! Bu dünyanın tek kuralı bu.",
            "lvl": "S.E.V.G.İ (Siddet Eylemi Veren Güç İstatistiği). Ne kadar çok, o kadar iyi!",

            # --- DİĞER ---
            "eğlence": "Her şeyi yaptım. Herkesi öldürdim, herkese yardım ettim. Artık tek eğlencem SENİN ne yapacağını izlemek.",
            "son": "Son diye bir şey yok. Sen bu programı kapatsan bile, ben burada bekliyor olacağım.",
            "ekonomi": "Altınlar, marketler... Hepsi anlamsız. Tek gerçek güç RUHLARDIR."
        }
        if os.path.exists(self.dosya_adi):
            with open(self.dosya_adi, "r", encoding="utf-8") as f:
                self.bilgi_bankasi.update(json.load(f))

    def hafizayi_kaydet(self):
        with open(self.dosya_adi, "w", encoding="utf-8") as f:
            json.dump(self.bilgi_bankasi, f, ensure_ascii=False, indent=4)

    def initUI(self):
        self.setWindowTitle('UnderNet Terminal - Flowey')
        self.setGeometry(300, 100, 550, 700)
        self.setStyleSheet("background-color: #000000; color: #ffffff; font-family: 'Courier New';")

        main_layout = QVBoxLayout()

        # Üst Bar (Config)
        top_bar = QHBoxLayout()
        self.btn_config = QPushButton("⚙ CONFIG (YAPI)")
        self.btn_config.setStyleSheet("""
            QPushButton {
                background-color: #000; color: #ffff00;
                border: 1px solid #ffff00; font-weight: bold; padding: 5px;
            }
            QPushButton:hover { background-color: #ffff00; color: #000; }
        """)
        self.btn_config.clicked.connect(self.open_config)
        top_bar.addWidget(self.btn_config)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # Avatar
        self.avatar_label = QLabel(self)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setFixedSize(550, 300)
        if os.path.exists(self.gif_yolu):
            self.movie = QMovie(self.gif_yolu)
            self.avatar_label.setMovie(self.movie)
            self.movie.start()
        main_layout.addWidget(self.avatar_label)

        # Ayırıcı Çizgi
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: white; border: 1px solid white;")
        main_layout.addWidget(line)

        # Chat
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("background-color: #000; border: none; font-size: 16px; selection-background-color: #ffff00;")
        main_layout.addWidget(self.chat_history)

        # Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Bir şeyler yaz...")
        self.input_field.setStyleSheet("background-color: #111; border: 1px solid #ffff00; padding: 12px; color: #ffff00; font-size: 14px;")
        self.input_field.returnPressed.connect(self.handle_message)
        input_layout.addWidget(self.input_field)

        main_layout.addLayout(input_layout)
        self.setLayout(main_layout)

        # Başlangıç Mesajı
        self.akisi_baslat("Flowey", "Hehehe... Her şeyi görmek istediğinden emin misin dostum?")

    def open_config(self):
        dialog = ConfigMenu(self)
        dialog.exec_()

    def muzik_baslat(self):
        if os.path.exists(self.muzik_dosyasi):
            url = QUrl.fromLocalFile(os.path.abspath(self.muzik_dosyasi))
            self.player.setMedia(QMediaContent(url))
            self.player.setVolume(self.ses_seviyesi)
            self.player.play()
            self.muzik_caliyor = True
            # Döngüye al
            self.player.stateChanged.connect(lambda s: self.player.play() if s == QMediaPlayer.StoppedState and self.muzik_caliyor else None)

    def muzik_duraklat_devam(self):
        if self.muzik_caliyor:
            self.player.pause()
            self.muzik_caliyor = False
        else:
            self.player.play()
            self.muzik_caliyor = True

    def akisi_baslat(self, kim, mesaj):
        self.tam_mesaj = mesaj
        self.mevcut_indeks = 0
        renk = "#ffff00" if kim == "Flowey" else "#00ff00"
        self.chat_history.insertHtml(f"<br><b style='color: {renk};'>{kim}: </b>")
        self.timer.start(self.yazi_hizi)
        self.ses_cal()

    def harf_ekle(self):
        if self.mevcut_indeks < len(self.tam_mesaj):
            self.chat_history.insertPlainText(self.tam_mesaj[self.mevcut_indeks])
            self.chat_history.ensureCursorVisible()
            self.mevcut_indeks += 1
        else:
            self.timer.stop()

    def ses_cal(self):
        if os.path.exists(self.ses_dosyasi):
            threading.Thread(target=playsound, args=(self.ses_dosyasi,), daemon=True).start()

    def handle_message(self):
        if self.timer.isActive(): return
        metin = self.input_field.text().strip()
        if not metin: return
        self.input_field.clear()

        # Öğrenme Modu Kontrolü
        if self.ogrenme_modu:
            self.bilgi_bankasi[self.son_bilinmeyen_soru] = metin
            self.hafizayi_kaydet()
            self.chat_history.insertHtml(f"<br><b style='color: #00ff00;'>Sen: </b>{metin}")
            self.akisi_baslat("Flowey", "Tamam, bunu o küçük beynime kazıdım.")
            self.ogrenme_modu = False
            return

        # Normal Chat
        self.chat_history.insertHtml(f"<br><b style='color: #00ff00;'>Sen: </b>{metin}")
        soru = metin.lower()
        cevap = None

        # Anahtar Kelime Tarama
        for anahtar, deger in self.bilgi_bankasi.items():
            if anahtar in soru:
                cevap = deger
                break

        if cevap:
            self.akisi_baslat("Flowey", cevap)
        else:
            self.akisi_baslat("Flowey", "Bunu bilmiyorum. Ne demeliyim?")
            self.ogrenme_modu = True
            self.son_bilinmeyen_soru = soru

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloweyBot()
    ex.show()
    sys.exit(app.exec_())
