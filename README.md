# Pardus Yoldaş

Pardus Yoldaş, Pardus ve Debian tabanlı Linux sistemleri için geliştirilmiş, terminal komutlarını yazarken hayalet metinle öneren küçük bir terminal uygulamasıdır. `prompt_toolkit` ile çalışan uygulama, önerilerini `komutlar.json` içindeki komut havuzundan alır ve komutları kullanım sıklığına göre sıralar.

> Bu uygulama gerçek komutları çalıştırır. Bir öneriyi kabul etmek, komutu güvenli hâle getirmez; çalıştırmadan önce komutu kontrol edin.

## Özellikler

- `komutlar.json` içindeki 4006 komutla otomatik öneri
- Kullanım sıklığına göre sıralama
- `Tab` ile öneriyi tamamlama, `Shift+Tab` ile alternatif öneriye geçme
- Oturum içinde çalışan `cd`, `cd -` ve `cd klasor` desteği
- Bash ile komut yürütme
- Uygulama içinden `source venv/bin/activate` ile Python sanal ortamı etkinleştirme
- `deactivate`, `exit` ve `quit` komutları

## Gereksinimler

- Pardus veya başka bir Debian tabanlı Linux dağıtımı
- Python 3 ve `venv` desteği
- `pip`
- Git ile kurulum için `git`

Gerekli sistem paketleri:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
```

## Kurulum

Depoyu klonlayın ve proje dizinine girin:

```bash
git clone https://github.com/mervankabaah/pardus-yoldas.git
cd pardus-yoldas
```

Sanal ortamı oluşturup bağımlılıkları yükleyin:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Çalıştırma

Sanal ortam etkin durumdayken uygulamayı başlatın:

```bash
python app.py
```

Örnek başlangıç ekranı:

```text
--- Pardus Akıllı Terminal (4006 komut yüklendi) ---
mervan@pardusyoldaş:$
```

Uygulama varsayılan olarak kullanıcının ana dizininde (`$HOME`) başlar. Başka bir dizinde çalışmak için `cd` kullanın:

```text
mervan@pardusyoldaş:$ cd ~/Masaüstü/yoldaş
mervan@pardusyoldaş:~/Masaüstü/yoldaş$
```

## Kullanım

Bir komutun ilk harflerini yazın. Görünen hayalet öneriyi `Tab` ile satıra ekleyin, sonra çalıştırmak için `Enter`a basın. Aynı önek için başka önerileri `Shift+Tab` ile dolaşabilirsiniz.

| Tuş / komut | Davranış |
| --- | --- |
| `Tab` | Görünen öneriyi satıra ekler. Komutu çalıştırmaz. |
| `Shift+Tab` | Bir sonraki uygun öneriyi gösterir. |
| `Enter` | Satırdaki komutu çalıştırır. |
| `Ctrl+C` | Girilen satırı iptal eder. |
| `cd` | Ana dizine geçer. |
| `cd klasor` | Belirtilen klasöre geçer. |
| `cd -` | Önceki dizine döner. |
| `exit` / `quit` | Uygulamadan çıkar. |

## Bash ve sanal ortam kullanımı

Pardus Yoldaş, girilen komutları Bash ile çalıştırır; bu nedenle `source`, `[[ ... ]]` ve Bash’e ait diğer sözdizimi özellikleri komut düzeyinde kullanılabilir.

Uygulama açıkken bir proje sanal ortamını etkinleştirmek için önce o projenin dizinine gidin:

```text
mervan@pardusyoldaş:$ cd ~/Masaüstü/yoldaş
mervan@pardusyoldaş:~/Masaüstü/yoldaş$ source venv/bin/activate
Sanal ortam etkinleştirildi: /home/kullanici/Masaüstü/yoldaş/venv
(venv) mervan@pardusyoldaş:~/Masaüstü/yoldaş$
```

Bu işlem `python` ve `pip` komutlarının ilgili sanal ortamdan çalışmasını sağlar. Ortamdan çıkmak için:

```text
(venv) mervan@pardusyoldaş:~/Masaüstü/yoldaş$ deactivate
```

`source /venv/bin/activate` yanlış bir yoldur; baştaki `/` kök dizini ifade eder. Proje içindeki ortam için `source venv/bin/activate` kullanın.

Her komut ayrı bir Bash alt sürecinde yürütüldüğünden, genel `export`, `alias` veya başka bir dosyayı `source` etme işlemlerinin kabuk durumu sonraki komuta taşınmaz. `source .../bin/activate` ve `deactivate` sanal ortam için uygulama tarafından özel olarak kalıcı biçimde desteklenir.

## Komut havuzu

Öneriler [`komutlar.json`](komutlar.json) dosyasından gelir. Her kayıt şu biçimdedir:

```json
{
  "komut": "sudo apt update",
  "kullanim_sikligi": 960
}
```

- `komut`: Önerilecek komut metni
- `kullanim_sikligi`: Büyük değer önce önerilir

Dosyayı düzenledikten sonra JSON biçimini doğrulayın:

```bash
python -c "import json; json.load(open('komutlar.json', encoding='utf-8-sig')); print('JSON geçerli')"
```

Komut havuzundaki örnekler yalnızca öneridir. Örneğin `docker`, `nmap` veya `ufw` ile ilgili bir önerinin görünmesi, bu araçların sistemde kurulu olduğu ya da kullanılmasının güvenli olduğu anlamına gelmez.

## Kontrol

Kurulum ve temel dosyaları kontrol etmek için:

```bash
python -m py_compile app.py
python -c "import json; json.load(open('komutlar.json', encoding='utf-8-sig'))"
```

`ModuleNotFoundError: No module named 'prompt_toolkit'` hatasında sanal ortamı etkinleştirip bağımlılıkları yeniden kurun:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Proje yapısı

```text
.
├── app.py             # Terminal uygulaması
├── komutlar.json      # Otomatik tamamlama komut havuzu
├── requirements.txt   # Python bağımlılıkları
├── LICENSE            # GNU GPL v3
└── README.md
```

## Lisans

Bu proje [GNU General Public License v3.0](LICENSE) ile lisanslanmıştır.
