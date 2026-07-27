import json
import os
from pathlib import Path
import getpass
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.key_binding import KeyBindings

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
UYGULAMA_DIZINI = Path(__file__).resolve().parent
ANA_DIZIN = Path.home()
JSON_DOSYASI = UYGULAMA_DIZINI / "komutlar.json"
KOMUTLAR = komutlari_yukle(JSON_DOSYASI)
SON_DIZIN = None

# Hayalet Yazı Motoru
class AkilliTahmin(AutoSuggest):
    def __init__(self):
        self.yazilan = None
        self.secili_index = 0

    def eslesen_komutlar(self, yazilan):
        if not yazilan:
            return []

        return [
            komut
            for komut in KOMUTLAR
            if komut.startswith(yazilan) and len(komut) > len(yazilan)
        ]

    def get_suggestion(self, buffer, document):
        yazilan = document.text
        eslesenler = self.eslesen_komutlar(yazilan)

        if not eslesenler:
            self.yazilan = yazilan
            self.secili_index = 0
            return None

        if self.yazilan != yazilan:
            self.yazilan = yazilan
            self.secili_index = 0

        self.secili_index %= len(eslesenler)
        return Suggestion(eslesenler[self.secili_index][len(yazilan):])

    def sonraki_tahmin(self, yazilan):
        eslesenler = self.eslesen_komutlar(yazilan)

        if not eslesenler:
            self.yazilan = yazilan
            self.secili_index = 0
            return None

        if self.yazilan != yazilan:
            self.yazilan = yazilan
            self.secili_index = 0
        else:
            self.secili_index = (self.secili_index + 1) % len(eslesenler)

        return Suggestion(eslesenler[self.secili_index][len(yazilan):])

def tus_kisayollari_olustur(tahmin_motoru):
    kb = KeyBindings()

    @kb.add('tab')
    def _(event):
        buffer = event.current_buffer
        if buffer.suggestion:
            buffer.insert_text(buffer.suggestion.text)

    @kb.add('s-tab')
    def _(event):
        buffer = event.current_buffer
        buffer.suggestion = tahmin_motoru.sonraki_tahmin(buffer.document.text)
        event.app.invalidate()

    return kb

def dizin_metni():
    mevcut_dizin = Path.cwd()

    if mevcut_dizin == ANA_DIZIN:
        return ""

    try:
        return "~/" + str(mevcut_dizin.relative_to(ANA_DIZIN))
    except ValueError:
        return str(mevcut_dizin)

def prompt_metni():
    kullanici = getpass.getuser()
    dizin = dizin_metni()

    if dizin:
        return [
            ("ansigreen", f"{kullanici}@pardusyoldaş"),
            ("", ":"),
            ("ansiblue", dizin),
            ("", "$ "),
        ]

    return [
        ("ansigreen", f"{kullanici}@pardusyoldaş"),
        ("", ":$ "),
    ]

def dizin_degistir(girdi):
    global SON_DIZIN

    try:
        parcalar = shlex.split(girdi)
    except ValueError as hata:
        print(f"Hata: {hata}")
        return

    if len(parcalar) == 1:
        hedef = ""
    elif len(parcalar) == 2:
        hedef = parcalar[1]
    else:
        print("Hata: cd komutu tek hedef dizin alır")
        return

    mevcut_dizin = Path.cwd()

    if not hedef:
        yeni_dizin = ANA_DIZIN
    elif hedef == "-":
        if SON_DIZIN is None:
            print("Hata: Önceki dizin yok")
            return
        yeni_dizin = SON_DIZIN
    else:
        yeni_dizin = Path(os.path.expandvars(os.path.expanduser(hedef)))
        if not yeni_dizin.is_absolute():
            yeni_dizin = mevcut_dizin / yeni_dizin

    try:
        os.chdir(yeni_dizin)
        SON_DIZIN = mevcut_dizin
        if hedef == "-":
            print(Path.cwd())
    except FileNotFoundError:
        print("Hata: Dizin bulunamadı")
    except NotADirectoryError:
        print("Hata: Bu bir dizin değil")
    except PermissionError:
        print("Hata: Bu dizine erişim izni yok")

def main():
    if not KOMUTLAR:
        print("Terminal başlatılamadı çünkü komut havuzu boş!")
        return

    os.chdir(ANA_DIZIN)

    tahmin_motoru = AkilliTahmin()
    session = PromptSession(key_bindings=tus_kisayollari_olustur(tahmin_motoru))
    print(f"\033[92m--- Pardus Akıllı Terminal ({len(KOMUTLAR)} komut yüklendi) ---\033[0m")

    while True:
        try:
            girdi = session.prompt(prompt_metni(), auto_suggest=tahmin_motoru)
            
            if girdi.lower() in ['exit', 'quit']:
                break
            if not girdi.strip():
                continue

            # cd komutunu Python içinde yönetiyoruz
            if girdi == "cd" or girdi.startswith("cd "):
                dizin_degistir(girdi)
                continue

            # Komutu sisteme gönder
            os.system(girdi)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    main()
