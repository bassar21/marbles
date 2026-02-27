# -*- coding: utf-8 -*-
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class MarblesBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kick Marbles Katilim Botu")
        self.root.geometry("350x450")
        self.root.configure(bg="#1e1e1e")

        self.is_recording = False
        self.players = set()
        self.output_file = "marbles_list.txt"
        self.placeholder_text = "Kanal Adi Girin"

        # Arayüz Elemanları
        tk.Label(root, text="Kick Marbles Kayit", fg="#53fc18", bg="#1e1e1e", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.channel_entry = tk.Entry(root, font=("Arial", 12), width=25, fg="gray", insertbackground="white", bg="#2b2b2b", border=0)
        self.channel_entry.insert(0, self.placeholder_text)
        self.channel_entry.bind("<FocusIn>", self.clear_placeholder)
        self.channel_entry.bind("<FocusOut>", self.add_placeholder)
        self.channel_entry.pack(pady=10, ipady=5)

        self.start_btn = tk.Button(root, text="KAYDI BASLAT", bg="green", fg="white", font=("Arial", 10, "bold"), width=20, command=self.start_thread, cursor="hand2")
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="KAYDI DURDUR", bg="red", fg="white", font=("Arial", 10, "bold"), width=20, command=self.stop_recording, cursor="hand2")
        self.stop_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="Durum: Bekleniyor...", fg="gray", bg="#1e1e1e")
        self.status_label.pack(pady=20)

        self.count_label = tk.Label(root, text="Kayitli Kisi: 0", fg="white", bg="#1e1e1e", font=("Arial", 12))
        self.count_label.pack(pady=5)

    def clear_placeholder(self, event):
        if self.channel_entry.get() == self.placeholder_text:
            self.channel_entry.delete(0, tk.END)
            self.channel_entry.config(fg="white")

    def add_placeholder(self, event):
        if not self.channel_entry.get():
            self.channel_entry.insert(0, self.placeholder_text)
            self.channel_entry.config(fg="gray")

    def start_thread(self):
        if not self.is_recording:
            channel = self.channel_entry.get().strip()
            if not channel or channel == self.placeholder_text:
                messagebox.showwarning("Uyari", "Lütfen geçerli bir kanal adi girin!")
                return
            
            self.is_recording = True
            self.players.clear()
            self.count_label.config(text="Kayitli Kisi: 0")
            self.start_btn.config(state="disabled")
            self.channel_entry.config(state="disabled")
            threading.Thread(target=self.run_bot, args=(channel,), daemon=True).start()

    def run_bot(self, channel):
        self.root.after(0, lambda: self.status_label.config(text=f"Baglaniyor: {channel}", fg="yellow"))
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(f"https://kick.com/{channel}/chatroom")
            time.sleep(8)
            self.root.after(0, lambda: self.status_label.config(text="Kayit Yapiliyor...", fg="#53fc18"))
            
            while self.is_recording:
                try:
                    messages = driver.find_elements(By.CSS_SELECTOR, ".chat-entry")
                    for msg in messages:
                        msg_text = msg.text.lower()
                        if "!katil" in msg_text:
                            user_el = msg.find_elements(By.CSS_SELECTOR, ".chat-entry-username")
                            if user_el:
                                username = user_el[0].text.strip()
                                if username and username not in self.players:
                                    self.players.add(username)
                                    with open(self.output_file, "w", encoding="utf-8") as f:
                                        for p in sorted(self.players):
                                            f.write(f"{p}\n")
                                    self.root.after(0, lambda u=len(self.players): self.count_label.config(text=f"Kayitli Kisi: {u}"))
                except Exception as inner_e:
                    print(f"Dongu Hatasi: {inner_e}")
                time.sleep(2)
            driver.quit()
        except Exception as e:
            print(f"Ana Hata: {e}")
            self.root.after(0, lambda: self.status_label.config(text="Hata: Baglanti Kesildi!", fg="red"))
            self.is_recording = False
            self.root.after(0, lambda: self.start_btn.config(state="normal"))
            self.root.after(0, lambda: self.channel_entry.config(state="normal"))

    def stop_recording(self):
        self.is_recording = False
        self.start_btn.config(state="normal")
        self.channel_entry.config(state="normal")
        self.status_label.config(text="Kayit Durduruldu.", fg="white")
        if self.players:
            messagebox.showinfo("Bitti", f"Kayit tamamlandi! {len(self.players)} kisi kaydedildi.\nDosya: marbles_list.txt")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarblesBotApp(root)
    root.mainloop()