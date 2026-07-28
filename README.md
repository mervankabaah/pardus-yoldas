# Pardus Yoldaş

**Pardus Yoldaş**, Pardus ve Debian tabanlı Linux dağıtımlarında komut yazmayı kolaylaştıran, terminal içinde çalışan akıllı öneri uygulamasıdır. Bir komutun başını yazdığınızda, devamını soluk (hayalet) metin olarak önerir. Öneriyi tamamlayabilir, alternatiflerine geçebilir veya komutu doğrudan çalıştırabilirsiniz.

Uygulama, `komutlar.json` dosyasındaki **4.006 komutluk** havuzu kullanır. Eşleşen öneriler önce kullanım sıklığına göre sıralanır: daha sık kullanılan komutlar önce, daha az kullanılanlar sonra gösterilir.

> Dikkat: Pardus Yoldaş girilen komutları Bash ile gerçekten çalıştırır. Bir önerinin görünmesi onun güvenli, sisteminizde kurulu veya her durumda uygun olduğu anlamına gelmez. `sudo`, dosya silme ve disk işlemleri gibi komutları çalıştırmadan önce mutlaka kontrol edin.

## Neler yapar?

- 4.006 komuttan otomatik tamamlama önerisi üretir.
- Önerileri kullanım sıklığına göre sıralar.
- `Tab` ile görünür öneriyi komut satırına tamamlar.
- `Shift+Tab` ile daha sonraki, genellikle daha az sık kullanılan uygun öneriye geçer.
- `Enter` ile yazılı komutu Bash üzerinde çalıştırır.
- `cd`, `cd -` ve `cd klasor` komutlarıyla dizin değişikliğini uygulama oturumu boyunca korur.
- `source venv/bin/activate` ile Python sanal ortamını uygulama içinden etkinleştirebilir.
- `deactivate`, `exit` ve `quit` komutlarını destekler.

## Gereksinimler

- Pardus veya başka bir Debian tabanlı Linux dağıtımı
- İnternet bağlantısı (ilk kurulum için)
- Terminal erişimi
- `git`, Python 3, `venv` ve `pip`

## Kurulum

Aşağıdaki komutları sırayla terminalde çalıştırın. Her adımın altında ne yaptığı açıklanmıştır.

### 1. Paket listesini güncelleyin

```bash
sudo apt update
```

Bu komut, Pardus'un paket listelerini yeniler. `sudo` sizden kullanıcı parolanızı isteyebilir; parola yazılırken ekranda karakter görünmemesi normaldir.

### 2. Git ve Python araçlarını kurun

```bash
sudo apt install -y git python3 python3-venv python3-pip unzip
```

Bu paketlerin görevleri şunlardır:

- `git`: Projeyi GitHub'dan indirmek (klonlamak) için kullanılır.
- `python3`: Uygulamayı çalıştırır.
- `python3-venv`: İzole Python ortamı oluşturur.
- `python3-pip`: Python kütüphanelerini kurar.
- `unzip`: GitHub'dan ZIP indirme yolunu tercih edenler için arşivi çıkarır.

### 3. Projeyi GitHub'dan klonlayın

Ev dizininizde çalışmak için önce oraya geçin ve projeyi indirin:

```bash
cd ~
git clone https://github.com/mervankabaah/pardus-yoldas.git
```

`git clone` komutu, [mervankabaah/pardus-yoldas](https://github.com/mervankabaah/pardus-yoldas) deposunu bilgisayarınıza `pardus-yoldas` adlı klasör olarak indirir.

### 4. Proje klasörüne girin

```bash
cd ~/pardus-yoldas
```

Bu noktadan sonraki komutlar proje klasörü içinde çalıştırılmalıdır.

### ZIP ile indirdiyseniz: arşivi çıkarın

`git clone` kullandıysanız bu adımı **atlayın**: Git projeyi zaten dosyalar hâlinde indirir, çıkarılacak ZIP oluşturmaz.

GitHub sayfasındaki **Code → Download ZIP** seçeneğiyle bir ZIP dosyası indirdiyseniz, klonlama yerine aşağıdaki yolu kullanın:

```bash
cd ~/İndirilenler
unzip pardus-yoldas-main.zip
cd pardus-yoldas-main
```

İndirilen dosyanın adı farklıysa, `pardus-yoldas-main.zip` yerine kendi dosya adınızı yazın. `ls` komutuyla bulunduğunuz klasördeki dosyaları görebilirsiniz.

### 5. Python sanal ortamını oluşturun

Git ile kurulumda proje klasöründeyken şu komutu çalıştırın:

```bash
python3 -m venv venv
```

Bu komut, proje içinde `venv` adlı ayrı bir Python ortamı oluşturur. Böylece uygulamanın ihtiyaç duyduğu kütüphaneler sistemdeki diğer Python programlarından bağımsız tutulur.

### 6. Sanal ortamı etkinleştirin

```bash
source venv/bin/activate
```

Başarılı olduğunda terminal satırınızın başında `(venv)` görünür. Bu, sonraki `python` ve `pip` komutlarının bu proje için oluşturulan ortamı kullanacağı anlamına gelir.

### 7. Gerekli Python kütüphanesini kurun

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

İlk komut `pip` paket yöneticisini günceller. İkinci komut, `requirements.txt` dosyasında yazan gerekli kütüphaneleri (özellikle `prompt_toolkit`) kurar.

## Uygulamayı çalıştırma

Sanal ortam etkin durumdayken proje klasöründe aşağıdaki komutu çalıştırın:

```bash
python app.py
```

Başlangıçta buna benzer bir mesaj görürsünüz:

```text
--- Pardus Akıllı Terminal (4006 komut yüklendi) ---
kullanici@pardusyoldaş:$
```

Sonraki kullanımlarda yeni bir terminal açtıysanız önce proje klasörüne girip sanal ortamı yeniden etkinleştirin:

```bash
cd ~/pardus-yoldas
source venv/bin/activate
python app.py
```

ZIP yoluyla kurduysanız proje klasör adı `pardus-yoldas-main` olabilir; ilk `cd` komutunu buna göre değiştirin.

## Kullanım

Komutun ilk kısmını yazmaya başlayın. Eşleşen bir komut varsa, devamı hayalet metin olarak görünür. Örneğin `sudo apt` yazdığınızda uygulama buna uygun komutlardan birini önerebilir.

| Tuş / komut | Ne yapar? |
| --- | --- |
| `Tab` | Görünen hayalet öneriyi satıra ekler. Komutu henüz çalıştırmaz. |
| `Shift+Tab` | Bir sonraki uygun öneriye geçer. Öneriler kullanım sıklığına göre sıralandığından bu genellikle daha az sık kullanılan bir öneridir. Tekrar basarak diğer eşleşmeleri dolaşabilirsiniz. |
| `Enter` | Satırdaki komutu çalıştırır. Önce öneriyi `Tab` ile tamamlamak zorunda değilsiniz. |
| `Ctrl+C` | O anda yazdığınız satırı iptal eder ve yeni bir isteme döner. |
| `Ctrl+D` | Girdi sonunu bildirir ve uygulamadan çıkar. |
| `exit` veya `quit` | Uygulamayı kapatır. |

Örnek akış:

1. `git sta` yazın.
2. Hayalet olarak `tus` devamı görünürse `Tab` tuşuna basın; satır `git status` olur.
3. Başka bir olası komutu görmek isterseniz `Shift+Tab` tuşuna basın.
4. Çalıştırmak için `Enter` tuşuna basın.
5. Vazgeçerseniz `Ctrl+C` tuşuna basın.

## Dizinler arasında gezinme

Pardus Yoldaş içindeki `cd` komutu, çalıştığınız dizini oturum boyunca değiştirir:

```bash
cd ~/Masaüstü
cd proje-klasoru
cd ..
cd -
```

- `cd`: Ana dizine (`~`) döner.
- `cd klasor`: Verilen klasöre geçer.
- `cd ..`: Bir üst klasöre çıkar.
- `cd -`: Bir önceki klasöre döner.

## Sanal ortamı uygulama içinden kullanma

Pardus Yoldaş çalışırken bir Python projesinin sanal ortamını etkinleştirmek için önce projenin dizinine gidin, sonra etkinleştirme komutunu yazın:

```bash
cd ~/pardus-yoldas
source venv/bin/activate
```

İstem satırında `(venv)` görünür. Sanal ortamdan çıkmak için şunu yazın:

```bash
deactivate
```

`source /venv/bin/activate` yanlış bir yoldur; baştaki `/` kök dizini ifade eder. Proje içindeki ortam için `source venv/bin/activate` kullanın.

## Sorun giderme

### `python3-venv` veya `pip` bulunamadı

Sistem paketlerini yeniden kurun:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

### `ModuleNotFoundError: No module named 'prompt_toolkit'`

Sanal ortamı etkinleştirip bağımlılıkları kurun:

```bash
cd ~/pardus-yoldas
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Komut önerileri görünmüyor

Uygulamayı proje klasöründen çalıştırdığınızdan ve `komutlar.json` dosyasının bulunduğundan emin olun:

```bash
cd ~/pardus-yoldas
ls komutlar.json
python app.py
```

## Proje dosyaları

```text
pardus-yoldas/
├── app.py             # Terminal uygulaması
├── komutlar.json      # 4.006 komutluk öneri havuzu
├── requirements.txt   # Python bağımlılıkları
├── LICENSE            # GNU GPL v3 lisansı
└── README.md          # Bu kılavuz
```

## Lisans

Bu proje [GNU General Public License v3.0](LICENSE) ile lisanslanmıştır.
