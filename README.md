# Pardus Akıllı Terminal

Pardus, Debian ve Debian tabanlı Linux sistemleri için geliştirilmiş basit bir akıllı terminal denemesidir. Uygulama `prompt_toolkit` kullanarak yazılan komuta göre `komutlar.json` içindeki yaygın terminal komutlarını hayalet metin olarak önerir.

## Özellikler

- Pardus/Debian odaklı komut tamamlama
- `apt`, `systemctl`, `journalctl`, `ls`, `cd`, `rm`, `cp`, `mv`, `tar`, `chmod`, `chown`, `grep`, `awk`, `sed`, `docker`, `git`, `ssh`, `ufw`, `nano`, `vim` gibi araçlar için hazır komut havuzu
- `komutlar.json` içinde 1000 adet gerçekçi terminal komutu
- `cd` komutunu oturum içinde çalıştırma
- `exit` veya `quit` ile çıkış

## Gereksinimler

- Pardus veya Debian tabanlı bir Linux dağıtımı
- Python 3
- Python sanal ortam desteği
- `pip`
- GitHub üzerinden klonlama yapılacaksa `git`

## Kurulum

### 1. Projeyi İndirin

GitHub deposunu bilgisayarınıza klonlayın:

```bash
git clone https://github.com/kullanici/pardus-akilli-terminal.git
cd pardus-akilli-terminal
```

Depoyu ZIP olarak indirdiyseniz klasöre terminalden girin:

```bash
cd pardus-akilli-terminal
```

### 2. Python ve Venv Paketlerini Kurun

Pardus/Debian sistemlerde önce paket listesini güncelleyin:

```bash
sudo apt update
```

Uygulamanın çalışması için gereken sistem paketlerini kurun:

```bash
sudo apt install -y python3 python3-venv python3-pip
```

Projeyi GitHub üzerinden klonlayacaksanız ayrıca `git` gerekir:

```bash
sudo apt install -y git
```

Kurulumu kontrol edin:

```bash
python3 --version
```

### 3. Sanal Ortam Oluşturun

Proje klasörü içinde `venv` adlı sanal ortamı oluşturun:

```bash
python3 -m venv venv
```

Sanal ortamı etkinleştirin:

```bash
source venv/bin/activate
```

Terminal satırının başında `(venv)` görüyorsanız sanal ortam aktiftir.

### 4. Python Kütüphanelerini Kurun

Sanal ortam aktifken Python bağımlılıklarını `requirements.txt` dosyasından kurun:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Kurulan paketleri kontrol etmek için:

```bash
pip list
```

### 5. Komut Havuzunu Kontrol Edin

`komutlar.json` dosyası proje kök dizininde bulunmalıdır. JSON dosyasının geçerli olduğunu kontrol etmek için:

```bash
python3 -m json.tool komutlar.json
```

Komut sayısını kontrol etmek için:

```bash
python3 -c "import json; print(len(json.load(open('komutlar.json', encoding='utf-8'))))"
```

Çıktı `1000` olmalıdır.

`komutlar.json` içinde `docker`, `nginx`, `ufw`, `ssh` gibi farklı araçlara ait örnek komutlar bulunabilir. Bunlar sadece autocomplete önerileridir; uygulamanın çalışması için bu araçların kurulması zorunlu değildir.

## Çalıştırma

Sanal ortam aktifken uygulamayı başlatın:

```bash
python3 app.py
```

Başarılı çalıştığında şuna benzer bir ekran görürsünüz:

```text
--- Pardus Akıllı Terminal (1000 komut yüklendi) ---
mervan@pardusyoldaş:$
```

Uygulama açıldığında otomatik olarak kullanıcının ana dizininde başlar. Yani `app.py` hangi klasörden çalıştırılırsa çalıştırılsın komutlar varsayılan olarak `$HOME` dizininde çalışır.

## Kullanım

Komut yazmaya başladığınızda uygulama `komutlar.json` içindeki ilk uygun komutu hayalet metin olarak önerir.

Örnek:

```text
mervan@pardusyoldaş:$ sudo apt up
```

Bu giriş için öneri olarak `sudo apt update` veya listedeki benzer bir komut görüntülenebilir.

Öneriyi kabul etmek için `Tab` tuşuna basabilirsiniz. Bu işlem öneriyi satıra ekler ve imleci satırın sonuna taşır; komutu çalıştırmaz. Komutu çalıştırmak için ayrıca `Enter` tuşuna basmanız gerekir.

Ana dizindeyken prompt içinde dizin yazmaz. Farklı bir dizine geçtiğinizde konum bilgisi mavi renkte görünür:

```text
mervan@pardusyoldaş:~/Masaüstü$
```

## Kısayollar

| Tuş / Komut | Açıklama |
| --- | --- |
| `Tab` | Ekranda görünen tahmini satıra uygular, komutu çalıştırmaz. |
| `Shift+Tab` | Aynı yazılan metin için bir sonraki tahmine geçer. Tüm tahminleri göstermeden aynı tahmini tekrar göstermez; liste bitince ilk tahmine döner. |
| `Enter` | Satırda yazılı olan komutu çalıştırır. |
| `cd` | Ana dizine geçer. |
| `cd klasor` | Belirtilen klasöre geçer. |
| `cd -` | Bir önceki klasöre döner. |
| `Ctrl+C` | Yazılan satırı iptal eder ve yeni satıra geçer. |
| `exit` | Uygulamadan çıkar. |
| `quit` | Uygulamadan çıkar. |

Çıkmak için:

```bash
exit
```

veya:

```bash
quit
```

## Proje Yapısı

```text
.
├── app.py
├── komutlar.json
├── README.md
└── requirements.txt
```

## Dosyalar

- `app.py`: Akıllı terminal uygulamasının ana Python dosyası.
- `komutlar.json`: Autocomplete için kullanılan 1000 komutluk JSON listesi.
- `requirements.txt`: Python bağımlılıkları.
- `README.md`: Kurulum ve kullanım dokümantasyonu.

## Komut Havuzunu Güncelleme

Yeni komut eklemek için `komutlar.json` dosyasını açın ve JSON dizi formatını bozmadan yeni string ekleyin:

```json
[
  "sudo apt update",
  "sudo apt upgrade -y",
  "systemctl status ssh"
]
```

Dikkat edilmesi gerekenler:

- Dosya geçerli JSON array formatında kalmalıdır.
- Her komut string olmalıdır.
- Son elemandan sonra virgül olmamalıdır.
- Dosyayı düzenledikten sonra `python3 -m json.tool komutlar.json` ile kontrol edin.

## Güvenlik Notu

Bu uygulama girilen komutu sistem kabuğunda çalıştırır. Bu nedenle yalnızca ne yaptığını bildiğiniz komutları çalıştırın. Özellikle `sudo`, `rm`, `chmod`, `chown`, `iptables`, `ufw`, `docker`, `systemctl` ve disk işlemleri içeren komutlarda dikkatli olun.

## Sorun Giderme

`ModuleNotFoundError: No module named 'prompt_toolkit'` hatası alırsanız sanal ortamı etkinleştirip bağımlılıkları yeniden kurun:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

`komutlar.json bulunamadı` hatası alırsanız uygulamayı proje kök dizininden çalıştırdığınızdan emin olun:

```bash
pwd
ls
python3 app.py
```

JSON hatası alırsanız dosyayı doğrulayın:

```bash
python3 -m json.tool komutlar.json
```

## Lisans

Bu projeyi kendi GitHub deponuzda uygun gördüğünüz lisansla yayımlayabilirsiniz. Açık kaynak yayımlamak için `MIT`, `Apache-2.0` veya `GPL-3.0` lisanslarından birini tercih edebilirsiniz.
