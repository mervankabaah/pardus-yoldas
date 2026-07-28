import json
import os
from pathlib import Path
import getpass
import shlex
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.key_binding import KeyBindings

# JSON dosyasından komutları çeken fonksiyon
def komutlari_yukle(dosya_yolu):
    try:
        # "utf-8-sig", UTF-8 dosyalarını ve bazı editörlerin eklediği BOM'u destekler.
        with open(dosya_yolu, 'r', encoding='utf-8-sig') as f:
            # JSON dosyasindaki komutlari normalize etmek icin oku
            ham_komutlar = json.load(f)
    except FileNotFoundError:
        print(f"\033[91mHata: '{dosya_yolu}' bulunamadı. Lütfen JSON dosyasını oluşturun.\033[0m")
        return []
    except json.JSONDecodeError:
        print(f"\033[91mHata: '{dosya_yolu}' geçerli bir JSON formatında değil.\033[0m")
        return []

    komutlar = []
    for sira, kayit in enumerate(ham_komutlar):
        if isinstance(kayit, str):
            komut = kayit
            kullanim_sikligi = 0
        elif isinstance(kayit, dict):
            komut = kayit.get("komut") or kayit.get("command")
            kullanim_sikligi = (
                kayit.get("kullanim_sikligi")
                or kayit.get("usage_frequency")
                or 0
            )
        else:
            continue

        if not isinstance(komut, str) or not komut:
            continue

        try:
            kullanim_sikligi = int(kullanim_sikligi)
        except (TypeError, ValueError):
            kullanim_sikligi = 0

        komutlar.append({
            "komut": komut,
            "kullanim_sikligi": kullanim_sikligi,
            "sira": sira,
        })

    return komutlar

# Komutları global bir listeye alıyoruz
UYGULAMA_DIZINI = Path(__file__).resolve().parent
ANA_DIZIN = Path.home()
JSON_DOSYASI = UYGULAMA_DIZINI / "komutlar.json"
KOMUTLAR = komutlari_yukle(JSON_DOSYASI)
SON_DIZIN = None
AKTIF_VENV = None
VENV_ORTAM_YEDEGI = None

# Hayalet Yazı Motoru
class AkilliTahmin(AutoSuggest):
    def __init__(self):
        self.yazilan = None
        self.secili_index = 0

    def eslesen_komutlar(self, yazilan):
        if not yazilan:
            return []

        eslesenler = [
            kayit
            for kayit in KOMUTLAR
            if kayit["komut"].startswith(yazilan) and len(kayit["komut"]) > len(yazilan)
        ]
        eslesenler.sort(key=lambda kayit: (-kayit["kullanim_sikligi"], kayit["sira"]))
        return [kayit["komut"] for kayit in eslesenler]

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
    venv_eki = []

    if AKTIF_VENV is not None:
        venv_eki = [("ansiyellow", f"({AKTIF_VENV.name}) ")]

    if dizin:
        return venv_eki + [
            ("ansigreen", f"{kullanici}@pardusyoldaş"),
            ("", ":"),
            ("ansiblue", dizin),
            ("", "$ "),
        ]

    return venv_eki + [
        ("ansigreen", f"{kullanici}@pardusyoldaş"),
        ("", ":$ "),
    ]

def venv_aktivasyon_yolu(girdi):
    """`source venv/bin/activate` komutundan venv kökünü döndürür."""
    try:
        parcalar = shlex.split(girdi)
    except ValueError:
        return None

    if len(parcalar) != 2 or parcalar[0] not in ("source", "."):
        return None

    aktivasyon_dosyasi = Path(os.path.expanduser(parcalar[1]))
    if not aktivasyon_dosyasi.is_absolute():
        aktivasyon_dosyasi = Path.cwd() / aktivasyon_dosyasi
    aktivasyon_dosyasi = aktivasyon_dosyasi.resolve()

    if (
        aktivasyon_dosyasi.name != "activate"
        or aktivasyon_dosyasi.parent.name != "bin"
        or not aktivasyon_dosyasi.is_file()
    ):
        return None

    venv_yolu = aktivasyon_dosyasi.parent.parent
    if not (venv_yolu / "bin" / "python").is_file():
        return None
    return venv_yolu

def venv_ortamini_geri_yukle():
    global AKTIF_VENV, VENV_ORTAM_YEDEGI

    if VENV_ORTAM_YEDEGI is None:
        return False

    for anahtar, deger in VENV_ORTAM_YEDEGI.items():
        if deger is None:
            os.environ.pop(anahtar, None)
        else:
            os.environ[anahtar] = deger

    AKTIF_VENV = None
    VENV_ORTAM_YEDEGI = None
    return True

def venv_aktive_et(venv_yolu):
    global AKTIF_VENV, VENV_ORTAM_YEDEGI

    # Zaten etkin bir ortam varsa önce asıl PATH'i geri getir.
    venv_ortamini_geri_yukle()
    VENV_ORTAM_YEDEGI = {
        anahtar: os.environ.get(anahtar)
        for anahtar in ("PATH", "VIRTUAL_ENV", "VIRTUAL_ENV_PROMPT")
    }
    os.environ["VIRTUAL_ENV"] = str(venv_yolu)
    os.environ["VIRTUAL_ENV_PROMPT"] = f"({venv_yolu.name}) "
    os.environ["PATH"] = str(venv_yolu / "bin") + os.pathsep + os.environ["PATH"]
    AKTIF_VENV = venv_yolu
    print(f"Sanal ortam etkinleştirildi: {venv_yolu}")

def venv_devre_disi_birak():
    if venv_ortamini_geri_yukle():
        print("Sanal ortam devre dışı bırakıldı")
    else:
        print("Etkin bir sanal ortam yok")

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

            if girdi.strip() == "deactivate":
                venv_devre_disi_birak()
                continue

            venv_yolu = venv_aktivasyon_yolu(girdi)
            if venv_yolu is not None:
                venv_aktive_et(venv_yolu)
                continue

            # Bash sözdizimini destekle. Ortam değişkenleri, aktif venv varsa
            # bu süreçten çalıştırılan her komuta aktarılır.
            subprocess.run(girdi, shell=True, executable="/bin/bash", env=os.environ)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == '__main__':
    main()
