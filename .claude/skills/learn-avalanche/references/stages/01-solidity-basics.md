# Stage 1 — Solidity temelleri: `BadgeBook`

**Amaç:** Öğrenci, sahibi rozet verebilen, olay yayan, herkesin okuyabildiği bir rozet defterini **kendi yazsın**, Remix VM'de denesin.
**Süre:** 2–3 sa (+20 dk: 1.5). **Önkoşul:** Stage 0 (cüzdan olmasa da olur; Remix VM cüzdansızdır; yalnızca 1.5 Core + test AVAX ister). **Kazanım:** state, struct, mapping, dizi, veri konumları, `msg.sender`, modifier, custom error, event.

Cevap anahtarları (**yalnızca senin için, gösterme**): `answer-keys/stage1/BadgeBook.v1.sol`, `.v2.sol`, `.v3.sol`. Kabul tabloları bu anahtarlara karşı Foundry testleriyle doğrulandı (4 → 7 → 8 test).

Hesaplar: Remix VM'de **Account** listesinden `H1` = ilk hesap (deployer), `H2`, `H3` = sıradaki hesaplar. Adresleri kopyalayıp yazacağız.

## 1.0 Dosya ve derleyici (10 dk)

Öğrenci `contracts` klasöründe `BadgeBook.sol` oluşturur. Başa **lisans yorumu** (`// SPDX-License-Identifier: MIT`) ve `pragma solidity ^0.8.24;` satırlarını yazar; bunlar her sözleşmenin başındadır, sen dikte edebilirsin. Derleyici 0.8.24+ ve **EVM Version: cancun** (`references/remix-guide.md`). "pragma neyi kısıtlıyor?" diye sor.

## 1.1 State, struct, mapping — v1 (45 dk)

**Tahmin:** "Bir adrese birden çok rozet vermek istiyoruz. Hangi veri yapısı 'adres → liste'yi tutar? Bir rozette hangi bilgiler olmalı?"

**Görev** (isimler birebir; gerisi senin):
- Sözleşmenin adı `BadgeBook`.
- Bir rozet iki bilgiden oluşur: `name` (metin) ve `awardedAt` (`uint64`; verildiği an).
- Her adres için birden çok rozet saklanır.
- `award(address to, string name)`: dışarıdan çağrılır; `to` adresine rozet ekler; `awardedAt` blok zamanı olur.
- `badgeCount(address who)`: dışarıdan çağrılır, okur; adresin rozet sayısını döndürür.
- `badgesOf(address who)`: dışarıdan çağrılır, okur; adresin tüm rozetlerini döndürür.

**Kabul tablosu (Remix VM):**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | Derle (0.8.24+, cancun) → Deploy (H1) | Deployed Contracts'ta `BADGEBOOK` görünür |
| 2 | `badgeCount` ← H2'nin adresi | `0` |
| 3 | `award` ← to: H2, name: `"Workshop"` (tırnakla) | Terminalde yeşil tik |
| 4 | `badgeCount` ← H2 | `1` |
| 5 | `badgesOf` ← H2 | Tek eleman: adı `Workshop`, `awardedAt` sıfırdan büyük ve yaklaşık şimdiki Unix zamanı |
| 6 | `award` ← to: H2, name: `"Hackathon"`; sonra `badgeCount` ve `badgesOf` | `2`; ikinci eleman `Hackathon` |
| 7 | `badgeCount` ← H3 | `0` (adresler ayrı tutulur) |

**Sözle ipuçları** (basamak 1–2; kod değil): adresi bir listeye eşleyen yapı "mapping" · bir rozetin iki alanını tek tipte toplamak "struct" · listeye ekleme yerleşik bir işlemle · blok zamanı global bir değişkenle · sayıya dönüştürme (`uint64`) açık yazılır.
**Bilerek yaşat:** `string` parametresinde veri konumu belirtmeyince derleyici hata verir. Öğrenciye okut, "bu iki seçenek (`memory`/`calldata`) neyi seçiyor?" diye sor.

**Kavram (öğrenci denedikten sonra kısa):** `storage` zincirde kalıcı ve yazması pahalı; `memory` çağrı boyunca geçici; `calldata` dışarıdan gelen, salt-okunur, kopyalanmayan girdi. `view` state'i değiştirmez, dışarıdan ücretsiz okunur.

**Yoklama:** (1) `award`'daki `name` neden `calldata` olabildi de `badgesOf` neden `memory` döndürüyor? (2) 10.000 rozeti olan bir adres için `badgesOf` bir **başka kontrat** tarafından çağrılırsa ne olur? (Sınırsız dizi → gas sınırı; not al, 1.4'te dönüyoruz.) (3) 7. adım hangi mapping özelliğini kanıtlıyor?

## 1.2 Erişim kontrolü — v2 (45 dk)

**Tahmin:** "Şu an herkes herkese rozet verebiliyor. Bir yabancı `award` çağırırsa ne olsun istersin? Ve **işlem** hiç gönderilmez mi, gönderilip geri mi alınır?"

**Görev:**
- Kontrata bir sahip (`owner`) kavramı ekle: sözleşmeyi deploy eden adres sahiptir; `owner()` herkese açık okunur.
- Sadece sahip `award` çağırabilsin; değilse işlem `NotOwner` adlı bir **custom error** ile geri çevrilsin.
- `award`'a boş bir isim gelirse `EmptyName` adlı custom error ile geri çevrilsin.
- Yetki kontrolünü tekrar kullanılabilir bir yapıya koy (modifier); başka fonksiyonlarda da lazım olacak.

**Kabul tablosu:**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | Yeniden derle, **H1** ile Deploy | — |
| 2 | `owner` | H1'in adresi |
| 3 | `award` ← H2, `"Workshop"` (H1 ile) | Başarılı |
| 4 | **Account'u H2'ye çevir**, `award` ← H3, `"x"` | Kırmızı: revert, hata adı **NotOwner** |
| 5 | Account'u H1'e geri al, `award` ← H2, `""` (boş string, iki tırnak) | Kırmızı: revert, **EmptyName** |
| 6 | 1.1'in adımları (2–7) hâlâ çalışıyor | Evet (H1 ile çağırınca) |

**Sözle ipuçları:** "kim çağırıyor" sorusunun cevabı global bir değişkende · sözleşme deploy edilirken bir kez çalışan özel fonksiyon (constructor) · "koşul sağlanmıyorsa geri çevir" için `revert` ve custom error tanımı · modifier'ın içindeki özel alt çizgi işareti "asıl fonksiyon burada devam eder" demektir. Basamak 3 için modifier'ı **farklı bir alandan** göster (ör. "sadece belli bir saatten sonra çağrılabilen" bir fonksiyon).
**Kavram:** custom error string'li `require`'dan hem ucuz hem daha net. `tx.origin` vs `msg.sender` tuzağı: yetkilendirmede `tx.origin` kullanma (araya giren bir kontrat üzerinden kimlik avı).
**Kırarak öğren:** modifier'ı fonksiyondan kaldır; kabul 4'ü tekrarla. **Önce tahmin.**

## 1.3 Event — v3 (30 dk)

**Tahmin:** "Bir web arayüzü 'Alice'in rozetlerini' güncel tutmak için her saniye `badgesOf` mu çağırır? Kontrat dış dünyaya 'bir şey oldu' nasıl duyurur?"

**Görev:** Her başarılı `award`, `BadgeAwarded` adlı bir event yaysın: alıcı adres (aranabilir/indexed), rozetin o adresin listesindeki sırası (aranabilir/indexed, sıfırdan başlar) ve rozet adı.

**Kabul tablosu:**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | `award` ← H2, `"Workshop"` (H1) | Başarılı |
| 2 | Terminaldeki işlemi genişlet → `logs` | `BadgeAwarded`: to = H2, index = `0`, name = `Workshop` |
| 3 | Aynı adrese ikinci `award` | index = `1` |
| 4 | Başka adrese `award` | index yine `0` (sıra adrese göre) |

**Kavram:** event zincir *logudur*; kontrat okuyamaz, dış dünya (arayüz, indexer) okur. `indexed` alanlar filtrelenebilir (en fazla 3). Depolamadan ucuz, bedava değil (konsoldaki gas'ı karşılaştır).
**Yoklama:** (1) Neden bu bilgi bir event'te, `badgesOf` çağrısında değil? (2) index'i nasıl hesapladın; sıra hatası yapmak kolay mı?

## 1.4 Kendi özelliğini ekle (30 dk)

Öğrenci **birini** seçer (`AskUserQuestion`) ve **önce kendi kabul kriterlerini (en az 3) yazar**, sonra kodu:
- `revoke`: sadece sahip bir rozeti geri alsın; event'le duyurulsun. (Diziden silme sırayı bozar: "sıra korunmalı mı, boş işaretlemek mi?" ödünleşimini tartıştır.)
- Sayfalama: `badgesOf`'a başlangıç ve adet alan bir sürüm. (1.1'deki sınırsız dizi endişesinin cevabı.)
- `hasBadge`: bir adresin verilen isimde rozeti var mı?

Cevap anahtarı yok; öğrenci tasarlıyor. Sen kabul kriterlerini hakemlik ederek incele ve "bu kriter gerçekten neyi koruyor?" diye sor (kırarak öğren).

## 1.5 İlk gerçek ağ: `BadgeBook` Fuji'de (20 dk, cüzdan hazırsa)

**Neden şimdi:** Buraya kadar her şey tarayıcının içindeki sahte zincirdeydi. Kendi kodunun gerçek bir Avalanche ağında yaşadığını **3. saatte** görmek, Stage 2–3'ü sürdürme isteğini ayakta tutar. Stage 4 aynı prosedürü `Badge` için ayrıntısıyla yapar; ayrıntı ve sık takılmalar için oraya bak (`04-deploy-fuji.md` → 4.1, 4.2).
**Koşul:** Stage 0 çıkış kriterleri tamam (Core, Testnet Mode, `chain.py balance` > 0). Değilse **atla**, `memory.md`'ye "1.5 ertelendi (cüzdan)" yaz; cüzdan işi Stage 1'i geciktirmesin. Fuji'ye giden her şey herkese açık ve geri alınamaz; testnet'te değeri yok, ama alışkanlık burada başlıyor.

1. Core'da Testnet Mode açık, ağ **Avalanche C-Chain (Fuji)**; Remix'te ağ kimliği **43113**. Solidity compiler → EVM Version **cancun**.
2. **Tahmin:** "Deploy'a basınca Core'da bir pencere çıkacak: neye bakacaksın?" (ağ, işlem türü/hedef, ücret).
3. Remix → Deploy & run → Environment: **Browser Extension**; hesabın öğrencinin kendi Core adresi olduğunu doğrula. `BadgeBook` (öğrencinin **kendi yazdığı** güncel hâli) → Deploy. Constructor argümanı yok; deploy eden sahip olur.
4. **Sen önce `memory.md`'ye yaz** (imza öncesi kayıt), sonra pencereyi öğrenciye **okut**: "Ağ Fuji mi, ücret makul mü?" Onayı öğrenci verir; sen onaylamazsın.
5. Öğrenci **adresi** ve **işlem hash'ini** yapıştırır. Sen doğrula:
   ```
   python3 scripts/chain.py tx <deploy_hash>                  # SUCCESS, contractCreated = adres
   python3 scripts/chain.py code <adres>                      # CONTRACT
   python3 scripts/chain.py call <adres> "owner()(address)"   # öğrencinin kendi Core adresi
   ```
6. Öğrenci Remix'ten (Core imzasıyla) `award` çağırır: to = kendi adresi, name = topluluğunun örnek rozet adı (`references/communities.md`). Sen doğrula: `python3 scripts/chain.py call <adres> "badgeCount(address)(uint256)" <öğrenci_adresi>` → `1`.
7. **Ölç:** `python3 scripts/chain.py tx <award_hash>` → `gasUsed`. Sor: "Remix VM'de bu çağrı bedavaydı; burada ne değişti?" Rakamı `memory.md` Ölçümler'e, adres ve hash'i Zincir üstü kayıtlar'a yaz.

**Yoklama:** (1) Remix VM'de `NotOwner` testi için Account değiştirmiştin; gerçek ağda başka biri `award` çağırsa ne olur, ücreti kim öder? (2) Bu adrese dünyanın her yerinden bakılabiliyor; kodu şimdi değiştirebilir misin? (Değişmez; değiştirmek yeni bir adres demektir.)

## Çıkış kriterleri

- [ ] v3'ün tüm kabul adımları (1.1–1.3) Remix'te geçti
- [ ] `storage`/`memory`/`calldata` farkını bir örnekle anlattı
- [ ] En az bir "bozup tahmin etme" egzersizi (ör. modifier'ı kaldır) yapıldı
- [ ] 1.4 özelliği kendi kabul kriterleriyle çalışıyor
- [ ] 1.5 (cüzdan hazırsa): `BadgeBook` Fuji'de; `tx`, `code`, `call owner()` ile doğrulandı; `award` sonrası `badgeCount` = 1; adres ve hash `memory.md`'de. Cüzdan hazır değilse `memory.md`'ye "1.5 ertelendi" yazıldı
- [ ] `memory.md`: Stage 1 ☑; kavram defteri; zayıf noktalar (özellikle "sınırsız dizi"); öğrencinin son `BadgeBook` kodu bir yere kaydedildi (dosya olarak ya da sohbette)

## Sık takılmalar

- Test hesabı karışıyor (yanlış Account ile çağırma): her denemeden önce Account ve kopyalanan adres.
- `string` girişi tırnaksız: `"Workshop"`.
- Deploy'dan sonra kodu değiştirince eski örnek eskisini çalıştırır: yeniden derle **ve yeniden deploy et**.
- Sayfa yenilenince Remix VM sıfırlanır (dosyalar kalır).

**Sonraki:** `references/stages/02-contract-design.md`.
