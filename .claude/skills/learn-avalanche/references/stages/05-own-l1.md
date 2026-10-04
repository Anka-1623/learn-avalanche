# Stage 5 — Kendi Avalanche L1'in ve kapanış

**Amaç:** Öğrenci Fuji üzerinde **kendi L1'ini** kursun, kendi gas token'ıyla çalışan bu zincire Cüzdan'ından bağlansın ve `Badge`'i **orada** deploy etsin. Sonra yolculuğu kapatsın: ne öğrendi, ne kurdu, nereye götürecek.
**Süre:** 2–3 sa (+ bekleme). **Önkoşul:** Stage 4. **Kazanım:** L1 vs C-Chain kararı, P-Chain kaydı ile düğümün farkı, validator/düğüm fikri, cüzdana özel ağ ekleme, aynı bytecode'un iki bağımsız ağda çalışması, (isteğe bağlı) precompile ile kural değiştirme.

⏱ **3 günlük pencere:** Builder hesabıyla gelen ücretsiz yönetilen testnet düğümü **3 gün sonra otomatik kapanır**; tek validator'lü bir L1'de düğüm kapanınca zincir durur. Aşamaya girmeden öğrenciye söyle; L1'in oluşturulma ve kapanış tarihini `memory.md`'ye yaz. Kapanırsa yeniden kurmak bir hata değil, dersin konusudur: "validator kaybı = zincir kaybı."

**Bu aşamada sen tarayıcıda tıklayamazsın.** Öğrenci Console'da (`https://build.avax.network/console`) ve Core'da çalışır. Sen (a) kararları hazırlar, (b) Console adımlarını **canlı okuyarak** tarif eder, (c) her adımın sonucunu `scripts/chain.py --rpc <L1 RPC>` ile doğrularsın. Console arayüzü değişir: adımları ezberden değil, aşağıdaki Academy derslerinden oku (`references/live-facts.md` → Dokümana erişim; ders yolu bayat olabilir, `fetch-doc.py` uyarısına bak):

- `avalanche-l1/avalanche-fundamentals`, "Creating an L1" modülü: Create Builder Account → Install Core Wallet → Claim Testnet Tokens → Network Architecture → **Create a Blockchain** → **Set up Validator Nodes** → **Convert a Subnet to an L1** → **Test your L1** → Remove Node.
- (isteğe bağlı 5.7) `avalanche-l1/access-restriction`, `avalanche-l1/customizing-evm`.

## 5.1 Karar: neden L1? (20 dk, konuşma)

`/docs/avalanche-l1s` ("Advantages") ve `/blog/l1-economics` sayfalarını `fetch-doc.py` ile oku. Sonra öğrenciyle şu tabloyu **kendi projesi için** doldur:

| Soru | C-Chain | Kendi L1'i |
|---|---|---|
| Gas token'ı kim belirler? | AVAX | Sen |
| Kimler kontrat deploy/işlem yapabilir? | Herkes | İstersen izinli |
| Validator'ları kim seçer? | Primary Network | Sen (Validator Manager) |
| Altyapı yükü ve maliyeti | Yok | Var (düğüm, sürekli validator ücreti) |
| Güvenlik | Geniş validator seti | Senin validator setin kadar |

Sor: **"Bir topluluk rozeti için L1 gerçekten gerekli mi?"** (Dürüst cevap çoğu zaman *hayır*, C-Chain yeter. Burada L1'i **öğrenmek** için kuruyoruz; gerçek bir ürün kararı olsaydı bu tabloya göre karar verirdin.) Öğrenci kararını kendi cümleleriyle yazar.

Kısa kavram haritası (çizdir): P-Chain L1'in kaydını ve validator listesini tutar → L1'in validator'ları (senin düğümün) blokları üretir → validator'lar P-Chain'e **sürekli ücret** öder (ön yüklemeli bakiyeden; bakiye biterse validator pasifleşir).

## 5.2 Hazırlık (15 dk)

1. **Builder hesabı** Stage 0.3'te açıldı mı? (Ücretsiz düğüm için gerekli.) Açılmadıysa şimdi aç.
2. Core'da **P-Chain bakiyesi** lazım (L1 kayıtları P-Chain'de ücret öder): Console faucet'inden P-Chain için test AVAX iste ya da C-Chain'den P-Chain'e aktarma aracını kullan (araç adını canlı bul). **Öğrenci sonucu Core'da görür; sen P-Chain bakiyesini `chain.py` ile göremezsin.** Ekran görüntüsü iste.
3. **Kararlar** (öğrenciyle ver, `memory.md`'ye yaz): L1 adı (topluluk adını taşıyabilir) · **benzersiz chain ID** (Console'un önerdiği ya da kullanılmayan büyük bir sayı) · gas token sembolü · ilk bakiyenin gideceği adres = **öğrencinin kendi Core C-Chain adresi** (aynı `0x…` adres L1'de de geçerli; kendine ayrılan bakiye olmazsa deploy edemez; bu yüzden **adresi iki kez kontrol ettir**).

## 5.3 L1'i kur (Console; ~45 dk)

Akışı Academy'deki sırayla, **her adımda öğrenciye "şu an P-Chain'de ne kaydedildi?" diye sorarak** yürüt:

1. **Subnet oluştur** (`CreateSubnetTx`): sadece sahibi (senin P-Chain adresin) parametre. "Dönüşümden sonra sahip yetkisini kaybedecek."
2. **Blockchain kaydı** (`CreateChainTx`): ad, VM (Subnet EVM), **genesis** (Genesis Builder aracı). Academy varsayılanları değiştirmemeyi önerir; sen ad, chain ID, sembol ve ilk bakiye adresini ayarlatırsın. Genesis'i birlikte oku (5.4). "Internal error" çıkarsa Academy: subnet henüz indekslenmemiş olabilir, 1 dk bekle.
3. **Düğüm:** yönetilen ücretsiz testnet düğümü (Builder hesabıyla, tek tık). Kapanış tarihini yaz (+3 gün).
4. **L1'e dönüştür** (`ConvertSubnetToL1Tx`): düğümü validator olarak ekler; Validator Manager adresi genesis'e önceden konmuş bir proxy'dir. Bu bir kereliktir.
5. **Çıktıları topla** ve `memory.md`'ye yaz: **RPC URL**, **chain ID**, **blockchain ID (32 bayt)**, **token sembolü**.

## 5.4 Genesis'i oku (15 dk)

Öğrencinin genesis JSON'unu (Console'da gösterilen) birlikte oku; her blok için tahmin: `chainId` · `alloc` (kimde ne kadar) · ücret ayarları · varsa etkinleştirilmiş precompile'lar. **"Bu satırı değiştirirsek ne olur?"** Genesis zincirin anayasasıdır; chain ID gibi şeyler sonradan değiştirilemez.

## 5.5 L1'i doğrula ve Core'a ekle (15 dk)

**Sen doğrula (öğrenci RPC URL'yi verir):**
```
python3 scripts/chain.py --rpc <L1_RPC> chain-id            # öğrencinin seçtiği chain ID
python3 scripts/chain.py --rpc <L1_RPC> block-times 10      # blok akıyor mu? (akmıyorsa: düğüm/validator sorunu)
python3 scripts/chain.py --rpc <L1_RPC> balance <öğrenci_adresi>   # genesis'teki ilk bakiye
```
RPC senin makinenden erişilemiyorsa (özel/uç nokta) öğrenciden Core/Remix ekran görüntüsü iste. Blok gelmiyorsa teşhisi öğrenciye yaptır: düğüm çalışıyor mu? Validator olarak eklendi mi? (Tahmin ettir, sonra bak.)

**Öğrenci Core'a özel ağ ekler** (Avalanche dokümanı `deploy-smart-contract` Step 1): Network Name, **RPC URL**, **Chain ID**, **Symbol**, Explorer alanı boş (N/A). Core'da bakiyesi (kendi token'ı) görünmeli.

## 5.6 `Badge`'i kendi L1'ine deploy et (25 dk) ← dersin kalbi

Stage 4'ün akışını **aynen tekrarla**, bu sefer Core'da ağ = öğrencinin L1'i. Kod **değişmedi**: aynı bytecode, iki bağımsız ağ. Sor: "Aynı sözleşme Fuji'de de senin L1'inde de var. Bu iki kopya birbiriyle konuşuyor mu?" (Hayır; iki ayrı state. Konuşmaları için ICM gerekir: `references/roadmap-next.md`.)

Adımlar: Remix → Environment: Browser Extension → hesabın Core adresi, ağ = L1 → contract `Badge`, constructor `admin` = kendi adresi → Deploy → Core'da imza (**ağın L1 olduğunu ve ücretin L1 token'ıyla olduğunu göster**) → adres + hash.

**Sen zincirde doğrula:**
```
python3 scripts/chain.py --rpc <L1_RPC> tx <deploy_hash>
python3 scripts/chain.py --rpc <L1_RPC> code <adres>
python3 scripts/chain.py --rpc <L1_RPC> call <adres> "name()(string)"
```
Öğrenci `grantRole` + `mint` de yapar (Stage 4.3'ün tekrarı). Gas farkını ölç: L1'de bir işlemin ücreti Fuji'ye göre ne? (`chain.py tx` → gasUsed; fiyat L1'in genesis ayarından gelir.)

**Yoklama:** (1) L1 kapanırsa deploy ettiğin sözleşmeye ne olur? (2) Fuji'deki `Badge` ile L1'deki `Badge` aynı adreste mi? Neden? (Adres deploy eden hesap + nonce'tan çıkar; farklı ağda farklı olabilir.) (3) Bu zincirin güvenliği kime bağlı?

## 5.7 (İsteğe bağlı) Kuralları değiştir: izinli deploy

Genesis'te **ContractDeployerAllowList** precompile'ı etkinleştirilmişse (kurulumda seçilmesi gerekir; sonradan eklemek çoğu zaman yeni genesis demektir) şunu yapabilir:

1. Precompile'ın varlığını doğrula: `chain.py --rpc <L1_RPC> code 0x0200000000000000000000000000000000000000` → CONTRACT (küçük boyutlu stub normaldir; precompile EVM bytecode'u değil, düğüm içinde çalışan yerel koddur).
2. Öğrenci precompile'a Remix'ten bağlanır: **kendi küçük bir arayüzünü yazar** (`readAllowList(address)` okuma, `setEnabled(address)`, `setNone(address)` yazma; Avalanche dokümanında imzalar var), derler ve **At Address** ile `0x0200…00` adresine bağlar. Bu, ABI/interface kavramının doğrudan uygulamasıdır.
3. Roller (resmî doküman): `readAllowList` `0 = None`, `1 = Enabled`, `2 = Admin` döndürür. Öğrencinin adresi Admin olmalı: `chain.py … call 0x0200…00 "readAllowList(address)(uint256)" <adres>`.
4. **Tahmin:** "İkinci bir Core hesabı (yabancı) kontrat deploy etmeye çalışırsa ne olur, hata nerede oluşur?" İkinci hesap oluştur, biraz L1 token'ı gönder, deploy dene → reddedilir. Admin `setEnabled` çağırınca başarılı; `setNone` ile tekrar reddedilir.
5. Sor: "Bu kuralı bir *kontrat* olarak yazsaydık hangi yolları kapatamazdık?" (Precompile protokol seviyesinde; kontrat yalnızca kendi çağrılarını korur.)

## 5.8 Kapanış (30 dk)

1. **Anlat:** öğrenci projeyi 5 dakikada, gerçek ölçümleriyle anlatır (blok aralığı, gas, kesinleşme). Sen sadece "bunu bilmeyen birine nasıl söylerdin?" diye sorarsın.
2. **Denetçi sorusu (3 tane, bilerek biri cevapsız):** "Admin anahtarı çalınırsa ne olur?" · "Yanlış adrese rozet mint ettim, geri alabilir miyim?" · "L1'imin tek validator'ı çevrimdışı olursa ne olur?" (Bilinmeyeni kabul etmek de doğru cevaptır.)
3. **Paylaşım:** topluluğuna göre (`references/communities.md` → Kapanış). Öğrenci 3–4 cümlelik paylaşım metnini **kendisi yazar**; sen yazmazsın.
4. **Fikir kartı (öğrenci yazar):** "Bu projeden sonra ekosistemde ne yapmak istersin?" Öğrenci 5 satırı **kendi cümleleriyle** yazar; sen yalnızca sorarsın, kartı yazmazsın: (a) Kim için, hangi problem? (b) Neden zincir üstünde (neden sıradan bir veritabanı olmasın)? (c) C-Chain mi L1 mi, neden (yukarıdaki karar)? (d) Elindeki `Badge`/`BadgeBook` bu fikre en küçük hangi demoya dönüşür? (e) Önümüzdeki 7 günde atacağı tek adım? Kartı söylemeden `memory.md` → `Fikir kartı`na yaz. Fikri yoksa "yok" geçerli bir cevap: "Seni en çok hangi sorun rahatsız ediyor?" diye en fazla iki soru sor, zorlama.
5. **Sonraki yol:** teknik konu için `references/roadmap-next.md` (ICM, ICTT, otomatik test, Academy kursları). Fikri varsa olgunluğunu sor ("sadece merak mı, demo mu, ekip ve ürün mü?") ve `references/live-facts.md` → **Ekosistem programları**'ndan uygun olanı göster: merak → Academy kursu ve topluluğunun etkinliği · demo → Team1 Builder Grants sayfası · ekip ve ürün → Codebase / Blizzard Fund. Programın **açık mı kapalı mı olduğunu, tutarı, koşulu ve tarihi söyleme**; öğrenciyi resmî sayfaya götür ve durumu oradan okut. Hedefini seçtir (`AskUserQuestion`) ve `memory.md`'ye yaz.
6. **Temizlik (isteğe bağlı, öğrencinin kararı):** yönetilen düğüm kapanacaksa beklemek yeterli; hemen kaldırmak isterse Console'daki adım (Academy "Remove Node"). Cüzdanı kurs sonrası da kullanabilir ama içine gerçek değer koymamasını hatırlat.

## Çıkış kriterleri

- [ ] L1 canlı: `chain.py --rpc … chain-id` ve `block-times` yanıt veriyor
- [ ] Öğrenci "P-Chain'de ne kayıtlı, L1'de ne çalışıyor?" sorusunu şemayla anlattı
- [ ] `Badge` L1'de deploy; adres ve hash `memory.md`'de; `mint` başarılı
- [ ] L1 vs C-Chain kararı gerekçesiyle yazıldı
- [ ] (İsteğe bağlı) izinli deploy: yabancı reddedildi, `setEnabled` sonrası kabul edildi
- [ ] Kapanış: 5 dk anlatım + paylaşım metni + fikir kartı (öğrenci yazdı; fikir yoksa "yok" kaydı) + sonraki hedef
- [ ] `memory.md`: Stage 5 ☑; L1 bilgileri (ad, chain ID, blockchain ID, RPC, **düğüm kapanış tarihi**)

## Sık takılmalar

- Blok üretilmiyor → validator olarak eklenmedi ya da düğüm kapandı/senkron değil; Console düğüm paneli. Süre dolmuşsa yeniden kur.
- "Internal error" (Create Chain) → subnet indekslenmedi, 1 dk bekle (Academy).
- Core'da bakiye yok → ilk bakiye yanlış adrese gitti; genesis'i oku. Çözüm: yeniden kurmak (bu yüzden 5.2'de adresi iki kez doğrulattık).
- Console ile Academy uyuşmuyor → Console güncel, Academy geride kalmış olabilir; ekrandakine güven ve farkı `references/live-facts.md`'ye not düş.
- `chain.py` RPC'ye ulaşamıyor → uç nokta yalnızca öğrencinin tarayıcısından erişilebilir olabilir; ekran görüntüsüyle devam et.
