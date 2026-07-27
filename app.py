import json
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

# JSON dosyasından komutları çeken fonksiyon
def komutlari_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, 'r', encoding='utf-8') as f:
            # JSON dosyasındaki listeyi doğrudan döndür
            return json.load(f)
    except FileNotFoundError:
        print(f"\033[91mHata: '{dosya_yolu}' bulunamadı. Lütfen JSON dosyasını oluşturun.\033[0m")
        return []
    except json.JSONDecodeError:
        print(f"\033[91mHata: '{dosya_yolu}' geçerli bir JSON formatında değil.\033[0m")
        return []

# Komutları global bir listeye alıyoruz
JSON_DOSYASI = "komutlar.json"
KOMUTLAR = komutlari_yukle(JSON_DOSYASI)

# Hayalet Yazı Motoru
class AkilliTahmin(AutoSuggest):
    def get_suggestion(self, buffer, document):
        yazilan = document.text
        
        if not yazilan:
            return None
            
        for komut in KOMUTLAR:
            if komut.startswith(yazilan):
                return Suggestion(komut[len(yazilan):])
        return None

def main():
    if not KOMUTLAR:
        print("Terminal başlatılamadı çünkü komut havuzu boş!")
        return

    session = PromptSession()
    print(f"\033[92m--- Pardus Akıllı Terminal ({len(KOMUTLAR)} komut yüklendi) ---\033[0m")

    while True:
        try:
            girdi = session.prompt("pardus@akilli:~$ ", auto_suggest=AkilliTahmin())
            
            if girdi.lower() in ['exit', 'quit']:
                break
            if not girdi.strip():
                continue

            # cd komutunu Python içinde yönetiyoruz
            if girdi.startswith("cd "):
                try:
                    os.chdir(girdi[3:].strip())
                except FileNotFoundError:
                    print(f"Hata: Dizin bulunamadı")
                continue

            # Komutu sisteme gönder
            os.system(girdi)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    main()