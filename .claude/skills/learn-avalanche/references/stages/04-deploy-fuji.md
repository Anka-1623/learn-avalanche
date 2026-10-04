# Stage 4 — Fuji testnet'e deploy

**Amaç:** `Badge`'i gerçek bir Avalanche ağına (Fuji C-Chain) Remix + Core ile göndermek, zincir üstünde etkileşime girmek ve sonucu **ölçmek.**
**Süre:** ~1,5 sa. **Önkoşul:** Stage 2 (Stage 3 önerilir); Stage 0'dan Core + test AVAX. **Kazanım:** ağ seçimi, `evm_version`, imza penceresi okuma, gerçek deploy, explorer, zincirde doğrulama, gas ve süre ölçümü.

## Kim ne yapar (güvenlik böleni)

| Ajan (sen) | Öğrenci |
|---|---|
| Ne yapacağını, hangi ağda, neyi imzaladığını açıklar | Remix'te yazar, derler, deploy eder; **Core'da her imzayı bilerek onaylar** |
| Zincirde **salt-okunur** doğrular (`scripts/chain.py`) | Adres ve işlem hash'ini paylaşır (gizli değildir) |
| Adresleri `memory.md`'ye yazar | Recovery phrase / anahtar hiçbir yerde paylaşılmaz |

## 4.1 Ağ ve derleyici hazırlığı (15 dk)

1. Core'da **Testnet Mode açık** ve **Avalanche C-Chain (Fuji)** seçili olmalı. Remix'in göstereceği ağ kimliğini birlikte doğrula: **43113**.
2. Bakiyeyi doğrula: `python3 scripts/chain.py balance <öğrencinin C-Chain adresi>` > 0.
3. **EVM sürümünü şimdi göster:** Solidity compiler → Advanced Configurations → **EVM Version = cancun.** Tahmin: "Bu satırı boş bıraksak derleme başarılı olurdu. Öyleyse neden bu kadar önemli?" (Avalanche şu an Cancun EVM'ini çalıştırıyor; Solidity 0.8.30+ varsayılanı daha yeni olduğundan, bytecode zincirin desteklemediği şeyler içerebilir. `references/live-facts.md` → EVM sürümü.) Kanıt: derleme sonrası artifact/metadata'da hedef sürüm okunabilir (isteğe bağlı).
4. Deploy edilecek sözleşme: Stage 2'deki `Badge`. Öğrenci dosyayı açar; kod değişmeden aynı sözleşme iki farklı ağda çalışacak: bunu vurgula.
5. **1.5'te `BadgeBook`'u Fuji'ye gönderdiyse:** ağ doğrulamasını ve imza penceresini bu sefer **öğrenci anlatsın**, sen yalnızca zincirde doğrula; rehberliği azalt. 4.4'te gas'ı 1.5'teki `award` ölçümüyle karşılaştır. **Göndermediyse** ilk Fuji deneyimi bu aşamadır: adımları tam anlat.

## 4.2 Deploy: önce oku, sonra imzala (25 dk)

**Tahmin:** "Deploy'a basınca Core'da bir pencere çıkacak. O pencerede neye bakmalıyız?" (Ağ adı/kimliği, işlem türü/hedef, ücret. **Hepsi doğruysa** onaylanır. Beklenmedik bir şey varsa reddedilir.)

Adımlar:
1. Remix → Deploy & run → Environment: **Browser Extension** (eski adı *Injected Provider*; Avalanche dokümanı "Injected Web3" der). Core'un bağlandığını ve hesabın kendi Core adresi olduğunu doğrula.
2. Contract: `Badge`. Constructor `admin` = **öğrencinin kendi Core adresi**. (Yanlış adres yazarsan kimse mint edemez ve admin rolü kaybolur; kontratı yeniden deploy etmekten başka çare yok. Öğrenci adresi yazarken **iki kez** kontrol etsin.)
3. Deploy → Core penceresi → öğrenci **okur**, sen "ağ Fuji mi, ücret makul mü?" diye sorarsın → onay.
4. Bekle; Remix terminalinde işlem yeşil, Deployed Contracts'ta `BADGE`. Öğrenci **adresi** ve **işlem hash'ini** yapıştırır.

**Sen zincirde doğrula:**
```
python3 scripts/chain.py tx <deploy_hash>                  # status SUCCESS, contractCreated = adres
python3 scripts/chain.py code <adres>                      # CONTRACT
python3 scripts/chain.py call <adres> "name()(string)"     # öğrencinin seçtiği NFT adı
python3 scripts/chain.py call <adres> "hasRole(bytes32,address)(bool)" 0x0000000000000000000000000000000000000000000000000000000000000000 <öğrenci_adresi>   # true
```
Sonuçları öğrenciye göster: "Kodu senin tarayıcında yazdın; şimdi dünyanın herhangi bir yerinden bu adrese bakılabiliyor." Adresleri `memory.md` "Zincir üstü kayıtlar" tablosuna yaz. Explorer'da kontratı birlikte aç (`https://explorer-test.avax.network/c-chain`; adresi arat).

**Hata ayıklama:** deploy başarısızsa terminal + Core penceresi + ağ kimliğini sırayla oku; `references/remix-guide.md` → Sık takılmalar. Bakiye/ücret sorunu → 0.3.

## 4.3 Zincir üstünde etkileşim (25 dk)

Öğrenci Remix'ten (Core imzasıyla) yapar:
1. `MINTER_ROLE` değerini oku → kendine `grantRole` ile ver (admin olduğu için).
2. `mint` ← to: kendi adresi, name: (topluluğunun örnek rozet adı; `references/communities.md`).
3. **Sen doğrula:**
   ```
   python3 scripts/chain.py call <adres> "ownerOf(uint256)(address)" 0
   python3 scripts/chain.py call <adres> "badgeName(uint256)(string)" 0
   python3 scripts/chain.py tx <mint_hash>
   ```
4. **Soulbound'u zincirde dene:** öğrenci başka bir adrese `transferFrom` yapmayı dener. Remix/Core büyük olasılıkla göndermeden **önce** "gas tahmini başarısız / işlem başarısız olabilir" der. Sor: "Bu uyarı neden çıktı? İşlemi göndermeden önce zincir bile sonucu biliyor." Öğrenci **göndermemeyi** seçer (ya da göndererek başarısız işlemin ücretini görür; kendi kararı). Revert selector'ünü `python3 scripts/chain.py keccak "Soulbound()"` ile eşleştir (`0xa4420a95`).

## 4.4 Ölç (15 dk)

| Ölçüm | Nasıl | Karşılaştır |
|---|---|---|
| Kesinleşme süresi | Öğrenci "deploy/mint"e bastığı an ile Remix'te yeşil tiki gördüğü an arasını sayar (kronometre) | Stage 0'daki blok aralığı ölçümü (`chain.py block-times 20`) ve tahmini |
| İşlem maliyeti | `chain.py tx <hash>` → `gasUsed`; explorer'da ücret | Stage 0'daki faucet işlemi; mint ile deploy'un gas farkı ve nedeni |

Rakamları `memory.md` "Ölçümler"e yaz. Sor: "Deploy neden mint'ten çok daha fazla gas harcadı?" (Bytecode'un zincire yazılması.)

## Çıkış kriterleri

- [ ] `Badge` Fuji'de; `tx`, `code`, `call` ile doğrulandı
- [ ] Öğrenci Core imza penceresinde neye baktığını anlattı
- [ ] En az bir `mint` başarılı; devir denemesi başarısızlık uyarısı verdi ve nedeni açıklandı
- [ ] Öğrenci `EVM Version = cancun` neden gerekli anlattı
- [ ] Süre ve gas ölçümleri öğrencinin kendi verileriyle `memory.md`'de
- [ ] Adresler ve hash'ler `memory.md` tablosunda

## Sık takılmalar

- `Browser Extension` seçeneği yok → Chrome'da Core yüklü mü, sayfa yenilendi mi; ekran görüntüsü iste.
- Core farklı ağda → Testnet Mode + Fuji; Remix'te ağ kimliği 43113 olmalı.
- `insufficient funds` → 0.3'ü tekrarla.
- Admin adresi yanlış yazıldı → çözüm yok, yeniden deploy (ders: adresleri kopyala, elle yazma).
- Aynı sözleşmeyi tekrar deploy etmek yeni bir adres üretir; eski kalır. Hangisinin güncel olduğunu `memory.md`'de işaretle.

**Sonraki:** `references/stages/05-own-l1.md`. Geçmeden önce **3 günlük yönetilen düğüm penceresini** öğrenciye söyle (`references/curriculum.md`).
