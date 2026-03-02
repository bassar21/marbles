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

# Opera GX'in bilgisayarındaki yolu (Genellikle bu yoldadır, değilse değiştirin)
OPERA_PATH = os.path.expanduser(r"~\AppData\Local\Programs\Opera GX\launcher.exe")
# ----------------

def run_bot():
    print("Bot baslatiliyor... Lutfen bekleyin.")
    
    options = Options()
    # Opera GX'in yerini belirtiyoruz
    options.binary_location = OPERA_PATH
    
    # Opera, Chrome altyapısını kullandığı için Chrome ayarlarıyla çalışır
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Arka planda çalışmasını istersen aşağıdaki satırı aktif edebilirsin:
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
        
        # Burada yapmak istediğin işlemleri (scroll, tıklama vb.) koda ekleyebilirsin
        # Örnek: Sayfayı aşağı kaydır
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

if __name__ == "__main__":
    if not os.path.exists(OPERA_PATH):
        print(f"HATA: Opera GX yuklu degil veya yol yanlis!\nAranan yol: {OPERA_PATH}")
    else:
        run_bot()