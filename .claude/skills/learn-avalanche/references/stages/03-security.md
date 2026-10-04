# Stage 3 — Güvenlik: bir açığı kendin yaz, kendin sömür, kendin kapat

**Amaç:** Öğrenci reentrancy açığını **bilerek yazsın**, bir saldırgan sözleşmeyle sömürsün, sonra düzeltsin. Açığı ellerinle yazınca bir daha unutmazsın.
**Süre:** 2 sa. **Önkoşul:** Stage 2. **Kazanım:** reentrancy, Checks-Effects-Interactions (CEI), `ReentrancyGuard`, klasik hata kataloğu, tehdit modeli düşüncesi.

Cevap anahtarı (**yalnızca senin için, gösterme**): `answer-keys/stage3/Vault.sol`. Doğrulandı: sömürü çalışıyor (saldırgan 1 ETH ile girip 11 ETH ile çıkıyor), CEI **tek başına** ve `nonReentrant` **tek başına** sömürüyü durduruyor. Kabul tablosu bu sonuçlardan türedi.

Hesaplar (Remix VM, her birinde bol sahte ETH var): `H1` = deployer, `H2` = kurban, `H3` = saldırgan.

## 3.0 Neden bu aşama ayrı bir dünya (5 dk)

Tahmin: **"Bir banka uygulamasında kodda hata olsa müşteri şubeye gidip düzelttirir. Zincirde kod değişmez ve para kodun içindedir. Bu ne demek?"** Kodun değişmezliği + herkese açık olması + para tutması = hatanın doğrudan para kaybı olması.

## 3.1 Açıklı kasa: bilerek yanlış yaz (25 dk)

**Tahmin:** "Bir kasa sözleşmesi düşün: herkes AVAX yatırır, sonra kendi bakiyesini çeker. Çekme fonksiyonunda üç şey olur: bakiyeyi oku, parayı gönder, bakiyeyi sıfırla. Sıra önemli mi? Hangi sıra tehlikeli?"

**Görev** (isimler birebir; `Vault.sol` dosyası):
- `VulnerableVault`: adres başına bakiye tutan bir mapping (`balanceOf`, herkese açık).
- `deposit()`: gönderilen AVAX'ı gönderenin bakiyesine ekler (payable).
- `withdraw()`: gönderenin bakiyesini okur; sıfırsa geri çevirir; **parayı gönderenin adresine düşük seviyeli çağrıyla (`call`, değer ile) gönderir; gönderme başarısızsa geri çevirir; EN SON bakiyeyi sıfırlar.** (Sırayı bilerek böyle yaz: bu bir hata ve amaç bu.)

**Kabul (Remix VM):**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | H1 ile `VulnerableVault` Deploy | — |
| 2 | Account H2, **Value: 10 Ether**, `deposit` | Kasa örneğinin yanındaki bakiye **10 ETH** |
| 3 | `balanceOf` ← H2 | `10000000000000000000` (10 ETH, wei cinsinden) |
| 4 | Account H2, Value 0, `withdraw` | Başarılı; kasa bakiyesi 0; H2'nin bakiyesi ~10 ETH artar (gas hariç) |

(4'ten sonra kasayı yeniden doldur: 2. adımı tekrarla.)

## 3.2 Saldırgan sözleşme (45 dk)

**Tahmin:** "Kasa parayı bir *sözleşme* adresine gönderirse o sözleşmenin `receive()` fonksiyonu çalışır. O anda kasada bakiye henüz sıfırlanmış mı? Ben saldırgan olsam `receive()` içinde ne yapardım?"

Bu dersin en zor görevi; ipucu merdivenini kullan, küçük parçalara böl:

1. **Arayüz:** Saldırganın kasayı çağırabilmesi için kasanın iki fonksiyonunu (`deposit`, `withdraw`) tanıtan bir *interface* yaz (`IVault`). Sözle: "bir interface, sadece imzalardan oluşur, gövdesi yoktur."
2. **`Attacker` sözleşmesi:** constructor'ı kasanın adresini alır ve saklar; ayrıca gönderilen miktarı hatırlamak için bir değişkeni vardır.
3. **`attack()`** (payable): gelen değeri saklar, kasaya yatırır (`deposit`), hemen ardından `withdraw` çağırır.
4. **`receive()`** (payable, özel fonksiyon): kasada, saklanan miktardan fazla ya da eşit bakiye kaldığı sürece kasanın `withdraw`'ını **tekrar** çağırır.

**Kabul (Remix VM; kasada H2'nin 10 ETH'i yatıyor):**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | H3 ile `Attacker` Deploy, constructor: kasa adresi | — |
| 2 | Account H3, **Value: 1 Ether**, `attack` | Başarılı |
| 3 | Kasanın ve `Attacker` örneğinin bakiyelerine bak | **Kasa 0 ETH, Attacker 11 ETH** (1 kendisi + kurbanın 10'u) |
| 4 | `balanceOf` ← H2 (kurban) | Hâlâ 10 ETH yazıyor ama kasada para yok! |

**Kanıt sonrası sorular:** "Saldırgan 1 ETH yatırıp neden 11 ETH çekebildi? Terminaldeki işlemi genişlet, kaç kez `withdraw` çağrıldı? Neden döngü durdu?" (Kasa boşalınca `receive()` koşulu sağlanmaz.) Öğrenci akışı kağıda/ASCII ile çizsin: `withdraw → receive → withdraw → receive → …`.

## 3.3 Düzelt: iki bağımsız çözüm (30 dk)

**Görev:** `SafeVault` adlı yeni bir sözleşme yaz (`VulnerableVault` ile aynı iş, ama güvenli). Önce **hangi değişiklikle** düzelteceğini söylesin, sonra yazsın. İki çözüm var ve **ikisi de tek başına** sömürüyü durdurur (doğrulandı):

- **CEI:** Kontroller (Checks) → Durum değişikliği (Effects: bakiyeyi sıfırla) → Dış çağrı (Interactions: parayı gönder). Asıl çözüm; mantıkla ilgili.
- **Kilit:** OpenZeppelin `ReentrancyGuard` + `nonReentrant`. İkinci kat savunma.

**Kabul:**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | `SafeVault` Deploy; H2 10 ETH yatırır | Kasa 10 ETH |
| 2 | Yeni bir `Attacker` (constructor: **SafeVault** adresi); H3, Value 1 Ether, `attack` | **Revert** (işlem geri alınır) |
| 3 | Kasa bakiyesi | Hâlâ 10 ETH |
| 4 | Account H2, `withdraw` | 10 ETH geri gelir |

**Tartış:** "Neden ikisini birden kullanmak istersin?" (Defense in depth: CEI unutulursa kilit kurtarır, kilit atlanırsa CEI kurtarır.) Neden `transfer`/`send` (sabit gas sınırı) artık güvenli çözüm sayılmaz? (Gas maliyetleri değişir; kalıcı çözüm CEI/kilit.)

**Kırarak öğren:** `SafeVault`'ta CEI sırasını geri bozup kilidi kaldır; saldırı yeniden çalışıyor mu? Önce tahmin.

## 3.4 Kendi projene uygula (20 dk)

Stage 2'deki notu geri getir: **"Güvenli mint (`_safeMint`) alıcı bir sözleşmeyse ona bir çağrı yapar."** Sor: "`Badge.mint` içinde bu çağrı, hangi state güncellemesinden **sonra** geliyor? Kimlik numarasını artırmayı mint'ten sonraya bıraksaydın ne olabilirdi?" (Aynı desen: dış çağrı sırasında state tutarsız.)

Sonra klasik hata kataloğunu öğrenciye tablo olarak doldurt: her hata için "**kendi kodumda var mı?**"

| Hata | Bir cümle | Kendi kodunda nerede? |
|---|---|---|
| Erişim kontrolü eksik | En sık ve en pahalı hata | Stage 1'de modifier'ı kaldırmıştın |
| Reentrancy | Dış çağrı sırasında state tutarsız | `_safeMint`, `Vault` |
| `tx.origin` ile yetkilendirme | Araya kontrat girerse kimlik avı | Stage 1 tuzak sorusu |
| Sınırsız döngü / dizi (DoS) | Büyüyen dizide gas sınırı aşılır | `badgesOf` |
| Kontrol edilmeyen dönüş değeri | Düşük seviyeli çağrı başarısız olabilir | `withdraw`'daki `call` |
| Zamana bağımlılık | `block.timestamp` yaklaşık bilgidir | `awardedAt` (bilgi için, karar için değil) |
| Tam sayı taşması | 0.8+ varsayılan olarak revert eder; `unchecked` bilinçli açılır | — |

**Uygulama:** `Badge` için 5 satırlık **tehdit modeli** (Kim? Neyi korumak istiyoruz? Saldırgan ne yapabilir? Hangi kabul adımı buna karşı?) Öğrenci yazar; eksik bir kabul adımı bulursa yeni adım tasarlar.

## Çıkış kriterleri

- [ ] Öğrenci bilerek açıklı kasayı yazdı, sömürdü (kasa 0, saldırgan 11 ETH) ve işlemin iç içeliğini terminalde gösterdi
- [ ] İki düzeltmeyi de uyguladı; saldırı revert oldu, kasa 10 ETH kaldı
- [ ] CEI'yi kendi cümleleriyle anlattı; `_safeMint` dış çağrısını fark etti
- [ ] Hata kataloğu tablosu ve `Badge` tehdit modeli dolduruldu
- [ ] `memory.md`: Stage 3 ☑; kavram defterine reentrancy tanımı (öğrencinin cümlesiyle); zayıf noktalar güncel

**Notlar (sonraki):** fuzz ve invariant testi bu beta'da yok (Foundry gerekir); bkz. `references/roadmap-next.md`.

**Sonraki:** `references/stages/04-deploy-fuji.md`.
