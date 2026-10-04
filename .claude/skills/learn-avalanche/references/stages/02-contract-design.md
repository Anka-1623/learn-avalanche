# Stage 2 — Kontrat tasarımı: `Badge` (ERC-721, roller, soulbound)

**Amaç:** Sıfırdan yazmak yerine denetlenmiş yapı taşlarını (OpenZeppelin) *birleştirmeyi* ve bir standardı (ERC-721) doğru uygulamayı öğren.
**Süre:** ~2 sa. **Önkoşul:** Stage 1. **Kazanım:** miras, `override`, interface, `supportsInterface`, AccessControl, `_update` ile davranışı kısıtlama.

Cevap anahtarı (**yalnızca senin için, gösterme**): `answer-keys/stage2/Badge.sol`. Kabul tablosu bu anahtara karşı 8 Foundry testiyle doğrulandı ("soulbound kontrolünü sil" mutasyonu 2 testi kırıyor). OpenZeppelin **5.6.1** (npm) ile test edildi.

Hesaplar (Remix VM): `H1` = admin, `H2` = minter, `H3` = Alice (rozet sahibi), `H4` = Bob.

## 2.0 OpenZeppelin (10 dk)

Amaç "kütüphaneyi kullan" değil, **okuyarak kullan**. Öğrenciye: OpenZeppelin'in ERC-721 dokümantasyon sayfasını aç, `ERC721` sözleşmesinin Remix'te nasıl içe aktarıldığına bak, import yolunu **kendin yaz** (`references/remix-guide.md` → OpenZeppelin: sürümü yola yaz, **5.6.1**). Sonra Remix'te içe aktarılan `ERC721.sol`'u aç ve `_update` fonksiyonunu bul: **"Bir rozet mint edilirken, devredilirken ve yakılırken bakiyeler tam olarak nerede değişiyor? Tahmin et, sonra oku."** Sürüm bilgisi: v4 öğreticilerindeki `_beforeTokenTransfer` v5'te **yok**; öğrenci eski bir örnek yapıştırırsa nedeni budur.

## 2.1 Miras ve çakışma (30 dk)

**Tahmin:** "`ERC721` ve `AccessControl`'ü birlikte miras alırsak, ikisinde de bulunan bir fonksiyon (ERC-165 `supportsInterface`) ne olur?" Öğrenci sözleşmeyi iki mirasla yazar; **derleyicinin** çakışma hatasını okur ve çözer (hatayı önceden söyleme). Kavram: `is` (miras), `override`, `virtual`, `super`; interface vs abstract; ERC-165: bir cüzdan/pazaryeri sözleşmenin ERC-721 konuşup konuşmadığını böyle sorar.

## 2.2 (isteğe bağlı) ERC-20'yi oku (20 dk)

Zamanı olan öğrenci OpenZeppelin `ERC20`'de bakiye mapping'ini ve `_update`'i bulup "transfer'de bakiye nerede değişir?" sorusunu cevaplar; sonra sen "ERC-20 (eşdeğer) ile ERC-721 (benzersiz) neden ayrı standartlar? Rozet hangisi olmalı?" diye sorarsın. Kod yazdırma; okuma egzersizi.

## 2.3 `Badge` — soulbound ERC-721 + roller (60 dk)

**Tahmin (yazmadan önce):**
1. "Devredilemezliği nasıl sağlardın?" Öğrenciler genelde `transferFrom`'u ezmeyi önerir. Yönlendir: "`safeTransferFrom`'un iki imzası, `approve` + `transferFrom` yolu da var. Hepsini mi ezeceksin? Ortak noktaları ne?" → hepsi `_update`'ten geçer (2.0'da bulduğu fonksiyon).
2. "Stage 1'deki `owner` yerine neden roller?" (Birden çok organizatör; yetki verme/alma yönetici tarafından; tek anahtara bağımlılık yok.)

**Görev** (isimler birebir):
- Sözleşmenin adı `Badge`; OpenZeppelin'in `ERC721` ve `AccessControl`'ünden miras alır.
- Constructor bir `admin` adresi alır; o adres `DEFAULT_ADMIN_ROLE` sahibi olur. NFT adı/sembolü topluluğunun tablosundan (`references/communities.md`); öğrenci seçer.
- Herkese açık `MINTER_ROLE` sabiti: değeri `"MINTER_ROLE"` metninin keccak256 özeti.
- `mint(address to, string name)`: sadece `MINTER_ROLE`; kimlik numaraları 0'dan başlayıp sırayla artar; rozet adı `badgeName(id)` ile herkese açık okunur; alıcıya güvenli mint edilir; yeni id'yi döndürür.
- `burn(uint256 id)`: rozetin sahibi kendi rozetini yakabilir, başkası yakamaz.
- **Devredilemez (soulbound):** mint ve burn serbest; sahipten sahibe her devir `Soulbound` adlı custom error ile geri çevrilir.
- `supportsInterface` çakışmasını çöz.

**Kabul tablosu (Remix VM):**

| # | Remix'te yap | Beklenen |
|---|---|---|
| 1 | Derle → Deploy, constructor `admin` = H1 | Deployed Contracts'ta `BADGE` |
| 2 | `MINTER_ROLE` (mavi) → değeri kopyala | 32 baytlık `0x…` |
| 3 | H1 ile `grantRole` ← rol: kopyaladığın değer, hesap: H2 | Başarılı |
| 4 | Account H2: `mint` ← to: H3, name: `"Workshop"` | Başarılı |
| 5 | `ownerOf` ← `0`; `balanceOf` ← H3; `badgeName` ← `0` | H3; `1`; `Workshop` |
| 6 | Account H3 (minter değil): `mint` ← H3, `"x"` | Revert: **AccessControlUnauthorizedAccount** (hesap ve rol parametreleriyle) |
| 7 | Account H3: `transferFrom` ← from: H3, to: H4, id: `0` | Revert: **Soulbound** |
| 8 | Account H3: `approve` ← H4, `0`; sonra Account H4: `transferFrom` ← H3, H4, `0` | Revert: **Soulbound** (izin devri kurtarmaz) |
| 9 | Account H3: `burn` ← `0`; `balanceOf` ← H3 | Başarılı; `0` |
| 10 | Yeni bir rozet mint et (H2). Account H4: `burn` ← o id | Revert (yetkisiz; hata adı `ERC721InsufficientApproval` benzeri) |
| 11 | `supportsInterface` ← `0x80ac58cd`; sonra `0x7965db0b` | İkisi de `true` (ERC-721 ve AccessControl) |

**Sözle ipuçları:** rol sabitini "metnin özeti" biçiminde tanımlamak bir kalıptır (OpenZeppelin `AccessControl` belgesinde görürsün) · "yalnızca şu role sahipse" için OpenZeppelin'in hazır kısıtlayıcısı var (adı `only...` ile başlar; dokümandan bul) · güvenli mint alıcıya bir "aldım" çağrısı yapar (**dış çağrı**; Stage 3'e not) · `_update`'in imzasını 2.0'da okumuştun: "kim → kime" bilgisini oradan nasıl öğrenirsin? Mint'te "kimden" adresi sıfırdır, burn'de "kime" adresi sıfırdır.
**Bilerek yaşat:** çakışma hatası (2.1), `override` unutma, parametreli custom error'ın Remix'te gösterimi.

**Yoklama:** (1) `DEFAULT_ADMIN_ROLE` ile `MINTER_ROLE` arasındaki fark? (2) Yanlış adrese soulbound rozet verildi; çözüm ne olmalı? (Organizatör iptal edemiyor → tasarım ödünleşimi; öğrenci karar versin: `REVOKER_ROLE` mü, sadece sahibin yakması mı?) (3) `id = _nextId++` sırasında neden mint'ten **önce** artırıyoruz? (state güncelle, sonra dış çağrı: Stage 3'ün habercisi.)
**Kırarak öğren:** soulbound satırını sil, kabul 7 ve 8'i tekrarla. Hangi **iki** adım kırılır? Önce tahmin.

## Çıkış kriterleri

- [ ] Kabul 1–11 Remix'te geçti
- [ ] Öğrenci `_update`'in neden tek nokta olduğunu anlattı
- [ ] Rol ile `owner` farkını bir senaryoyla açıkladı
- [ ] `supportsInterface` override'ının nedenini söyledi
- [ ] `memory.md`: Stage 2 ☑; "güvenli mint dış çağrıdır" notu Stage 3 için zayıf noktalara eklendi

**Sonraki:** `references/stages/03-security.md`.
