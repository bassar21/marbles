# -*- coding: utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- AYARLAR ---
# Buraya hedef kanalın linkini yapıştır
KANAL_LINKI = "https://kick.com/dantesofficial" 

# Opera GX'in bilgisayarındaki yolu. 
# NOT: Kısayol (.lnk) yerine doğrudan .exe dosyasını göstermelisin. 
# Kullanıcı adın "Deniz D" olduğu için yolu buna göre düzenledim.
OPERA_PATH = r"C:\Users\Deniz D\AppData\Local\Programs\Opera GX\launcher.exe"
# ----------------

def run_bot():
    print("Bot baslatiliyor... Lutfen bekleyin.")
    
    options = Options()
    # Opera GX'in yerini belirtiyoruz
    options.binary_location = OPERA_PATH
    
    # Opera, Chrome altyapısını kullandığı için Chrome ayarlarıyla çalışır
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Pencerenin görünmesini istemiyorsan aşağıdaki satırın başındaki '#' işaretini kaldır:
    # options.add_argument("--headless") 

    try:
        # Opera için uygun olan ChromeDriver'ı otomatik yükler
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        print(f"Baglaniliyor: {KANAL_LINKI}")
        driver.get(KANAL_LINKI)
        
        # Sayfanın yüklenmesi için bekleme
        time.sleep(5)
        
        print("Kanal acildi. Islemler yapiliyor...")
        
        # Sayfayı aşağı kaydır (Örnek işlem)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        
        print("Islem tamamlandi. Tarayici 10 saniye icinde kapatilacak.")
        time.sleep(10)
        driver.quit()
        print("Bot basariyla durduruldu.")

    except Exception as e:
        print(f"\nHata Olustu: {e}")
        if "cannot find Chrome binary" in str(e) or "binary" in str(e):
            print("\nUYARI: Opera GX belirtilen yolda bulunamadi!")
            print(f"Lutfen su yolu kontrol et: {OPERA_PATH}")
            print("Eger Opera GX farkli bir klasordeyse OPERA_PATH kısmını güncellemelisin.")

if __name__ == "__main__":
    # Dosya yolunun varlığını kontrol et
    if not os.path.exists(OPERA_PATH):
        print(f"HATA: Opera GX belirtilen yolda bulunamadi!\nAranan yol: {OPERA_PATH}")
        print("\nİpucu: Opera GX genellikle şu yoldadır:")
        print(r"C:\Users\KULLANICI_ADIN\AppData\Local\Programs\Opera GX\launcher.exe")
    else:
        run_bot()