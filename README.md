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
- `git` ve temel sistem araçları

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

### 2. Python Kurun

Pardus/Debian sistemlerde önce paket listesini güncelleyin:

```bash
sudo apt update
```

Python 3 kurulu değilse kurun:

```bash
sudo apt install -y python3
```

Kurulumu kontrol edin:

```bash
python3 --version
```

### 3. Venv ve Pip Paketlerini Kurun

Sanal ortam oluşturabilmek ve Python paketlerini kurabilmek için gerekli sistem paketlerini yükleyin:

```bash
sudo apt install -y python3-venv python3-pip
```

### 4. Sanal Ortam Oluşturun

Proje klasörü içinde `venv` adlı sanal ortamı oluşturun:

```bash
python3 -m venv venv
```

Sanal ortamı etkinleştirin:

```bash
source venv/bin/activate
```

Terminal satırının başında `(venv)` görüyorsanız sanal ortam aktiftir.

### 5. Gerekli Sistem Paketlerini Kurun

Uygulama temel olarak Python ile çalışır. Komut önerileri içinde geçen yaygın araçları denemek istiyorsanız aşağıdaki paketleri kurabilirsiniz:

```bash
sudo apt install -y curl wget git nano vim htop tree net-tools openssh-client openssh-server ufw rsync unzip zip tar grep sed gawk coreutils
```

Docker komutlarını da kullanacaksanız:

```bash
sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

Docker grup değişikliğinin aktif olması için oturumu kapatıp açmanız gerekebilir.

### 6. Python Kütüphanelerini Kurun

Sanal ortam aktifken Python bağımlılıklarını `requirements.txt` dosyasından kurun:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Kurulan paketleri kontrol etmek için:

```bash
pip list
```

### 7. Komut Havuzunu Kontrol Edin

`komutlar.json` dosyası proje kök dizininde bulunmalıdır. JSON dosyasının geçerli olduğunu kontrol etmek için:

```bash
python3 -m json.tool komutlar.json
```

Komut sayısını kontrol etmek için:

```bash
python3 -c "import json; print(len(json.load(open('komutlar.json', encoding='utf-8'))))"
```

Çıktı `1000` olmalıdır.

## Çalıştırma

Sanal ortam aktifken uygulamayı başlatın:

```bash
python3 app.py
```

Başarılı çalıştığında şuna benzer bir ekran görürsünüz:

```text
--- Pardus Akıllı Terminal (1000 komut yüklendi) ---
pardus@akilli:~$
```

## Kullanım

Komut yazmaya başladığınızda uygulama `komutlar.json` içindeki ilk uygun komutu hayalet metin olarak önerir.

Örnek:

```text
pardus@akilli:~$ sudo apt up
```

Bu giriş için öneri olarak `sudo apt update` veya listedeki benzer bir komut görüntülenebilir.

Öneriyi kabul etmek için sağ ok gibi terminal tamamlama tuşlarını kullanabilir veya komutu yazmaya devam edebilirsiniz. `Enter` tuşu satırda gerçekten yazılı olan komutu çalıştırır.

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
