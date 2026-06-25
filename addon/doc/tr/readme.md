# NVDA için Renk Kontrast Denetleyicisi

Dijital erişilebilirlik test uzmanlarının, renk kontrastı oranlarının Web İçeriği Erişilebilirlik Kılavuzu (WCAG) tarafından tanımlanan eşiklerin içinde kaldığından düzenli olarak emin olmaları gerekir. Ancak görme engelli test uzmanlarının bunu, gören meslektaşlarına veya otomatik çözümlere güvenmeden yapması tarihsel olarak zor olmuştur. WAVE ve axe DevTools dahil piyasadaki çoğu otomatik çözüm, kontrast sorunlarını yalnızca "öneri" olarak filtreler, bazı şeyleri gözden kaçırır ve odak göstergesini incelemez.

Bu eklenti, odaklanmış öğenin kontrastını NVDA+F ile, inceleme imlecinin altındaki öğeyi NVDA+Shift+F ile, odak göstergesini NVDA+Shift+C ile kontrol etmenize ve tüm metin kontrastı hataları için NVDA+Shift+Ctrl+F ile sayfa genelinde bir denetim çalıştırmanıza olanak tanır.

| Görev | Komut | Kapsam |
| --- | --- | --- |
| Odaklanmış metnin kontrastını kontrol et | **NVDA+F** | Odaklanmış öğenin, kontrast oranı dahil biçimlendirme bilgileri |
| İnceleme imlecindeki metnin kontrastını kontrol et | **NVDA+Shift+F** | İnceleme imleci konumundaki, kontrast oranı dahil biçimlendirme bilgileri |
| Odak göstergesinin kontrastını kontrol et | **NVDA+Shift+C** | Çevreleyen arka plana karşı odak halkası |
| Sayfa genelinde metin denetimi çalıştır | **NVDA+Shift+Ctrl+F** | Geçerli sayfadaki, WCAG kontrast eşiğine göre gruplanmış görünür metin |

## Metin kontrastı

Bu eklenti, NVDA'nın mevcut biçimlendirme bilgisi komutlarını genişletir. Kontrast oranı dahil biçimlendirme bilgilerini duymak için herhangi bir metnin üzerinde **NVDA+F** tuşlarına basın. Örnek:

- Source Sans 3 ExtraLight
- 10.5pt
- beyaz üzerinde siyah
- sola hizalı
- `#FFFFFF üzerinde #000000, kontrast 21.0:1`

Gözatılabilir bir iletişim kutusu için hızlıca iki kez basın. **NVDA+Shift+F**, sistem düzeltme imleci yerine inceleme imleci konumunu kullanır.

WCAG AA, normal metin için 4.5:1, büyük metin için 3:1 gerektirir. WCAG AAA ise 7:1 gerektirir.

## Odak göstergesi kontrastı

Odak halkası ile çevreleyen arka plan arasındaki kontrastı duymak için herhangi bir odaklanmış öğenin üzerinde **NVDA+Shift+C** tuşlarına basın:

> `Odak göstergesi: #FFFFFF üzerinde #000000, kontrast 21.0:1`

WCAG, odak göstergelerini ilgili gereksinimler aracılığıyla değerlendirir. Metin dışı kontrast, görsel odak göstergesinin bitişik renklere karşı en az 3:1 kontrasta sahip olmasını gerektirir; WCAG 2.2 odak görünümü ise değişimin kontrastı ve göstergenin boyutu konusunda gereksinimler ekler. Bu eklenti kontrast ölçümünü bildirir; test uzmanları yine de tam odak görünümü gereksinimini değerlendirmelidir.

## Sayfa genelinde kontrast denetimi

Geçerli sayfadaki her metin parçasını tek seferde taramak için **NVDA+Shift+Ctrl+F** tuşlarına basın. Sonuçlar, ciddiyete göre gruplanmış olarak gözatılabilir bir iletişim kutusunda açılır:

- 3:1'in altında (büyük metin)
- 4.5:1'in altında (normal veya küçük metin)
- 7:1'in altında (AAA metin kontrastı)

7:1 veya daha iyisini karşılayan metin, tüm WCAG eşiklerini geçer ve atlanır. Hiçbir şey başarısız olmazsa, NVDA iletişim kutusunu açmak yerine bunu bildirir.

Lütfen bu komutun yalnızca sayfanın geçerli durumunda görünen metni kontrol ettiğini unutmayın. Odak, üzerine gelme, genişletilmiş veya daraltılmış içerik, geç yüklenen içerik ve özel olarak işlenmiş veya görsele dayalı metin gibi diğer durumları yine de göstermeniz ve test etmeniz gerekir. Odak halkası kontrastı, **NVDA+Shift+C** ile ayrıca kontrol edilir.

## Kurulum

1. En son sürümü [bu bağlantıdan](https://github.com/cartertemm/contrast-checker-nvda/releases/latest/) indirin.
2. NVDA çalışırken .nvda-addon dosyasını açın. NVDA sizden kurmanızı isteyecektir.

## Deneyin

`tests/test_contrast.html` dosyasını yerel olarak veya [işlenmiş test sayfasını](https://ctemm.me/files/test_contrast.html) NVDA çalışırken bir tarayıcıda açın.
Metin kontrastı, bilinen oranlardaki odak halkaları, eksik halkalar, box-shadow halkaları, beyaz olmayan arka planlar ve farklı öğe türleri gibi çeşitli yaygın senaryoları kapsar.

## Kaynaktan derleme

Git, Python ve SCons gerektirir.

```
git clone https://github.com/cartertemm/contrast-checker-nvda/
cd contrast-checker-nvda
pip install scons
scons
```

Derlenen `.nvda-addon` dosyası proje kök dizininde görünür.

## Lisans

GPL 2.0
