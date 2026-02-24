import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- AYARLAR ---
KICK_CHANNEL_URL = "https://kick.com/dantesofficial/chatroom" # Chat linkinizi buraya yazın
OUTPUT_FILE = "marbles_list.txt"
COMMAND = "!play"

def start_bot():
    # Tarayıcı ayarları
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Arka planda çalışsın isterseniz bu satırı aktif edin
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(KICK_CHANNEL_URL)
    
    print(f"Sistem başlatıldı. {KICK_CHANNEL_URL} adresi izleniyor...")
    print("Durdurmak için terminalde Ctrl+C yapabilirsiniz.")

    players = set() # İsimleri benzersiz tutmak için 'set' kullanıyoruz

    try:
        while True:
            try:
                # Chat mesajlarını bul (Kick'in güncel HTML yapısına göre)
                messages = driver.find_elements(By.CSS_SELECTOR, ".chat-entry")
                
                for msg in messages:
                    try:
                        text_content = msg.text.lower()
                        
                        # Eğer mesaj "!play" içeriyorsa
                        if COMMAND in text_content:
                            # Kullanıcı adını çek (Genellikle mesajın içindeki ilk kelime veya belirli bir class içindedir)
                            # Kick yapısında kullanıcı adı genellikle 'chat-entry-username' class'ındadır
                            username_element = msg.find_element(By.CSS_SELECTOR, ".chat-entry-username")
                            username = username_element.text.strip()

                            if username not in players:
                                players.add(username)
                                print(f"Yeni oyuncu eklendi: {username}")
                                
                                # Dosyayı anlık güncelle (Marbles'a aktarmaya hazır formatta)
                                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                                    for player in sorted(players):
                                        f.write(f"{player}\n")
                    except:
                        continue
                
                time.sleep(2) # İşlemciyi yormamak için kısa bekleme
                
            except Exception as e:
                print(f"Bir hata oluştu: {e}")
                time.sleep(5)
                
    except KeyboardInterrupt:
        print(f"\nİşlem durduruldu. Toplam {len(players)} kişi kaydedildi.")
        print(f"Dosya hazır: {os.path.abspath(OUTPUT_FILE)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_bot()