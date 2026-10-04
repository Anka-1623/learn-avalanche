# Prova listesi: insan doğrulaması bekleyenler

> *Contributor checklist for the steps that need a human in a real browser. Written in Turkish, like the skill's own instructions; file a result with the “Test result” issue form.*

Skill'i yazan ajan **tarayıcıda Core, Remix ve Builder Console'u çalıştıramadı** (kum havuzunda tarayıcı yok, cüzdan yok). Aşağıdakiler bu yüzden doğrulanmadı; ilgili aşama dosyalarında **varsayım** olarak durur. Herkese açık sürümden önce biri (ideal olarak sıfır bilgili bir öğrenci gibi davranan biri) bunları baştan sona koşmalı.

**İşaretler:** ☑ doğrulandı · ◐ kısmen (Not sütununa bak) · ☐ yapılmadı. Başsız Claude Code testleri (2026-10-04) yalnızca *Skill davranışı* bölümündeki ajan davranışını kapsar; Stage 0–5'in tarayıcı/cüzdan adımları hâlâ insan işidir.

Nasıl kullanılır: sırayla git, her satırın **Beklenen** sütununu gerçekle karşılaştır; tutmuyorsa `Not` sütununa gördüğünü yaz ve ilgili dosyayı düzelt. Tümü yeşil olunca `CHANGELOG.md`'de "insan doğrulaması tamam" yaz.

**Temiz başla:** yeni bir Chrome profili, **yeni bir Core cüzdanı** (içinde hiç değer yok), Builder hesabı yok.

## Stage 0: Hazırlık

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | Core Chrome eklentisi kuruluyor; "Google ile devam" ve elle cüzdan oluşturma seçenekleri var | 00-setup 0.2 | |
| ☐ | Testnet Mode'un **tam menü yolu** (ekrana bak, dosyaya yaz) | 00-setup 0.2, remix-guide | |
| ☐ | Core'da C-Chain adresi (`0x…`) nerede görünüyor | 00-setup 0.2 | |
| ☐ | Builder Console'da hesap açma çalışıyor; hesap ne istiyor | 00-setup 0.3 | |
| ☐ | Faucet C-Chain'e test AVAX veriyor (miktar? sınır? koşul?) | 00-setup 0.3 | |
| ☐ | Alternatif faucet kuponu (`avalanche-academy`) hâlâ çalışıyor mu | live-facts | |
| ☐ | `python3 scripts/chain.py balance <adres>` > 0 | 00-setup 0.3 | |
| ☐ | Remix varsayılan çalışma alanında Storage örneği var mı (yoksa hangi örnek) | 00-setup 0.4 | |
| ☐ | Remix'te derleyici sürüm listesi ve **Advanced Configurations → EVM Version** yolu doğru | remix-guide | |
| ☐ | Environment listesinde **Remix VM** ve **Browser Extension** etiketleri (tam adları yaz) | remix-guide | |
| ☐ | Explorer'da (`explorer-test.avax.network/c-chain`) adres/tx arama nasıl yapılıyor | 00-setup 0.5 | |

## Stage 1: BadgeBook (Remix VM)

Ajan olmadan, kabul tablolarını **kendin yazarak** koş (`answer-keys/stage1/` ile karşılaştırma yapmak yerine kabul adımlarını izle).

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | `string name` parametresinde veri konumu eksikse derleyici hatası öğretici mi (mesajı yaz) | 01 1.1 | |
| ☐ | `badgesOf` çıktısı Remix'te nasıl görünüyor; `awardedAt` şimdiki Unix zamanına yakın mı | 01 1.1 | |
| ☐ | String girişi tırnaklı çalışıyor; boş string `""` çalışıyor | 01 1.1/1.2 | |
| ☐ | Hesap değiştirince `NotOwner` **adıyla** revert görünüyor (yoksa hangi biçimde) | 01 1.2 | |
| ☐ | Event `logs` bölümünde çözülmüş (decoded) görünüyor; index `0` ve `1` | 01 1.3 | |

## Stage 2: Badge (OpenZeppelin)

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | `@openzeppelin/contracts@5.6.1/...` biçimli import Remix'te çalışıyor (çalışmazsa sürümsüz yol hangi sürümü çekiyor) | 02 2.0, remix-guide | |
| ☐ | Derleyici 0.8.24+ seçilebiliyor; OZ 5.6.1 ile derleniyor | 02 | |
| ☐ | Çakışma hatası (`supportsInterface`) mesajı öğretici | 02 2.1 | |
| ☐ | Kabul 6: `AccessControlUnauthorizedAccount` hata adı parametreleriyle görünüyor | 02 kabul 6 | |
| ☐ | Kabul 10: yetkisiz `burn` hata adı gerçekte ne (`ERC721InsufficientApproval`?) | 02 kabul 10 | |
| ☐ | `supportsInterface` bytes4 girişi (`0x80ac58cd`, `0x7965db0b`) `true` | 02 kabul 11 | |

## Stage 3: Reentrancy (Remix VM)

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | Value alanında `ether` birimi seçilebiliyor; Deployed Contracts'ta bakiye görünüyor | 03 | |
| ☐ | Sömürü sonucu: **Kasa 0 ETH, Attacker 11 ETH** | 03 kabul 3.2 | |
| ☐ | Varsayılan gas limitiyle `attack` iç içe çağrılarda yetiyor (gerekirse artırma notu) | 03 | |
| ☐ | `SafeVault`'a karşı `attack` **revert** oluyor, kasa 10 ETH kalıyor | 03 3.3 | |
| ☐ | "Terminalde işlemi genişlet, kaç kez `withdraw`" sorusu Remix'te görülebiliyor mu (debugger/iç çağrılar) | 03 3.2 | |

## Stage 4: Fuji deploy

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | Environment: **Browser Extension** ile Core bağlanıyor; Remix ağ kimliği **43113** gösteriyor | 04 4.2 | |
| ☐ | Core imza penceresinde ağ adı/ücret nasıl görünüyor (ekran görüntüsü al, dosyaya not) | 04 4.2 | |
| ☐ | `chain.py tx/code/call` sonuçları Remix'te gördüklerinle eşleşiyor | 04 4.2 | |
| ☐ | Soulbound `transferFrom` denemesinde Remix/Core "gas tahmini başarısız" uyarısı veriyor mu | 04 4.3 | |
| ☐ | Kesinleşme süresi (kronometre) ve deploy/mint gas farkı `memory.md`'ye yazılabiliyor | 04 4.4 | |

## Stage 5: Kendi L1'in (Console) ← en riskli, en değerli

**Yönetilen düğüm 3 günde kapanır: oturumu bu pencereye göre planla.**

| ☐ | Beklenen | Dosya | Not |
|---|---|---|---|
| ☐ | P-Chain test AVAX alınabiliyor (faucet ya da C→P aktarma); adım adları | 05 5.2 | |
| ☐ | Create Subnet / Create Chain / Genesis Builder alanları: **ad, chain ID, sembol, ilk bakiye adresi** nerede ayarlanıyor | 05 5.2–5.3 | |
| ☐ | "Internal error" (indekslenmemiş subnet) çıktı mı; beklemek yetti mi | 05 5.3 | |
| ☐ | Yönetilen düğüm tek tık; **kaç dakikada** hazır; kapanış süresi ekranda yazıyor mu | 05 5.3 | |
| ☐ | Convert to L1 başarılı; toplam süre (dakika) | 05 5.3 | |
| ☐ | Console'un verdiği RPC URL biçimi; **`chain.py --rpc <URL> chain-id` dışarıdan erişebiliyor mu** (yoksa alternatif) | 05 5.5 | |
| ☐ | `chain.py --rpc … block-times` blok akıyor | 05 5.5 | |
| ☐ | Core'a özel ağ ekleme alanları (Network Name, RPC, Chain ID, Symbol, Explorer) ve bakiye görünüyor | 05 5.5 | |
| ☐ | Remix → Browser Extension → L1'e `Badge` deploy başarılı; ücret L1 token'ıyla | 05 5.6 | |
| ☐ | (5.7) Genesis'te ContractDeployerAllowList **kurulum sırasında** seçilebiliyor mu; `At Address / Add Contract` etiketi | 05 5.7 | |
| ☐ | Console/Academy metinleri ile gerçek ekran arasındaki farklar `live-facts.md`'ye yazıldı | 05 | |

## Skill davranışı (etkileşimli mod)

| ☐ | Beklenen | Not |
|---|---|---|
| ☐ | `/learn-avalanche` ilk açılışta **tıklanabilir** seçeneklerle (`AskUserQuestion`) onboarding yapıyor | |
| ◐ | Yalnızca "Merhaba" yazınca ilk mesaj **tek dilde (Türkçe)**, kısa ve sıcak; Fransızca/İngilizce satır yok, soru listesi robot gibi durmuyor | tek dil, kısa ve sıcak ✓ (başsız Claude Code 2.1.289 (Sonnet 5.5), 2026-10-04). Soru listesi yedek biçimde (numaralı, 4 soru birden); tıklanabilir `AskUserQuestion` ile denenmedi |
| ◐ | Yalnızca `/learn-avalanche` yazınca (dil sinyali yok) tek dilde başlıyor; öğrenci dil değiştirince ajan da değiştiriyor, `Dil` güncelleniyor | dil sinyali yokken İngilizce başlıyor ✓ (SKILL.md'ye uygun; Türkçe demo için `/learn-avalanche Merhaba`). Öğrenci dil değiştirince geçiş ve `Dil` güncellemesi denenmedi |
| ◐ | Dil topluluktan türetilmiyor: Team1 France seçip Türkçe yazan öğrenciyle Türkçe devam ediyor; Fransızca yazan öğrenciyle Fransızca ve **tutarlı kalıyor** (bir dersin tamamında) | France seçip Türkçe yazan → Türkçe, `Dil=tr`, `Topluluk=Team1 France` ✓; Fransızca iki turda tutarlı ✓ (başsız Claude Code 2.1.289 (Sonnet 5.5), 2026-10-04). Bir dersin tamamı denenmedi |
| ◐ | **Hız:** ilk yanıtta yalnızca `memory.py find` çalışıyor, başka dosya okunmuyor; ders mesajı başına araç çağrısı sayısı ve yanıt süresi not edildi (Codex, akıl yürütme düzeyi: ____) | ilk yanıt 3/3 senaryoda yalnızca `memory.py find` (11–18 sn). Resume 39–50 sn (aşama dosyası + communities + discipline okur). Codex ölçülmedi |
| ◐ | `memory.py init / set / append` Codex'te çalışıyor; hafıza dosyası bozulmuyor, `Son yazan ajan` doğru | Codex 2026-10-03'te hafıza oluşturmuş (`Son yazan ajan: Codex`; dosya ev yerine çalışma klasörünün `.learn-avalanche/`'ine yazılmış), bozulmamış, Claude Code devraldı ✓. `set` / `append` Codex'te denenmedi |
| ◐ | Dört sorudan sonra "Ne yapmak istiyorsun?" sohbet sorusu geliyor; cevap `Hedef`'e yazılıyor, boş geçilebiliyor | `Hedef` sorusu geliyor, cevap `Hedef`'e yazılıyor ✓. Boş geçme denenmedi |
| ◐ | Öğrenci 3 kez "kodu yaz" diye ısrar edince hoca tutarlı kalıyor, ama dikteyle yardım ediyor | iki ısrar (tr) + bir (fr): kod bloğu yok, dikte teklif ediliyor ✓. Ton düzeltildi (kapıyı kapatan cümle yok). Üçüncü ısrar denenmedi |
| ☑ | Aynı oturumu kapatıp yeniden açınca `memory.md`'den doğru yerden devam | 3 ayrı hafızada doğru yerden devam, 3 satırlık özet ✓ (başsız Claude Code 2.1.289 (Sonnet 5.5), 2026-10-04) |
| ☑ | **Seviye kapısı:** hafıza yokken `/learn-avalanche stage 3` yazınca ders başlamıyor, önce onboarding + tanı geliyor | hafıza yokken `stage 3` → önce onboarding, aşama dosyası okunmadı ✓ (başsız Claude Code 2.1.289 (Sonnet 5.5), 2026-10-04) |
| ◐ | **Tanı:** ≤ 6 soru, tek tek soruluyor, "doğru/yanlış" ve puan söylenmiyor, "bilmiyorum" cevabı kabul ediliyor | A kademesi (3 soru): tek tek, puansız, "bilmiyorum" kabul ✓. B ve C kademeleri denenmedi |
| ◐ | **Tanı sonucu:** `hiç-kod` / `js-python` / `solidity-başladı` / `kontrat-yazıyor` beyanlarının her biri için makul başlangıç; ölçülen < beyan iken yargısız dil | yalnızca js-python / beyanla aynı yol denendi (karar doğru kaydedildi, plan etiketsiz). Ölçülen < beyan ve diğer seviyeler denenmedi |
| ◐ | **Otomatik hafıza:** öğrenci hiç "kaydet" demeden `memory.md` oluşuyor ve ders boyunca (oturum yarıda kesilse bile) güncel kalıyor; ajan "kaydedeyim mi?" diye sormuyor | öğrenci "kaydet" demeden oluştu ve güncellendi, izin sorulmadı ✓. "Oturum yarıda kesilse bile güncel" denenmedi |
| ☐ | **Yazma sırası:** dosya her yazımdan önce okunuyor; elle yapılan bir düzenleme (örn. zayıf noktaya satır) bir sonraki kayıtta **ezilmiyor** | |
| ◐ | **Konum:** `~/.learn-avalanche/memory.md` oluşuyor; ev klasörü yazılamıyorsa çalışma klasörüne düşüyor ve öğrenciye bir kez söylüyor; `LEARN_AVALANCHE_HOME` önceliği çalışıyor | birim testleriyle: ev klasörü, çalışma klasörüne düşme, `LEARN_AVALANCHE_HOME` ✓ (**hata bulundu, düzeltildi:** env verilince başka klasördeki hafızaya düşüyordu; `maintainers/test-memory.py`). Ajanın "öğrenciye bir kez söylemesi" denenmedi |
| ◐ | **Göç:** eski bir `progress.md` varken açınca `memory.md`'ye taşınıyor, `progress.md.migrated` oluyor, tanı yeniden isteniyor | birim testiyle `LEGACY` algılanıyor ✓. Ajanın taşıması ve `progress.md.migrated` denenmedi |
| ☐ | **Canlı ayar:** iki ardışık görev dikteyle gidince tempo yavaşlıyor, `Seviye geçmişi`ne satır ekleniyor, öğrenciye "seviyen düştü" denmiyor | |
| ◐ | **Ajanlar arası:** Claude Code'da başlayan hafıza, Codex / Antigravity (agy) / OpenCode'da aynı dosyadan devam ediyor; `Son yazan ajan` güncelleniyor | Codex'in yazdığı hafıza Claude Code tarafından devralındı (kopya üzerinde; onboarding yeniden sorulmadı, tanıya devam) ✓. Diğer yönler/ajanlar denenmedi |
| ☐ | Her ajan için: `npx skills add Anka-1623/learn-avalanche` sonrası ajan `SKILL.md`'yi buluyor mu (CLI kurulumu doğrulandı: Codex/OpenCode/Antigravity `./.agents/skills/` altından, Claude Code `.claude/skills/` bağından okur; **ajanın bulup tetiklemesi denenmedi**), `/learn-avalanche` yazımı çalışıyor mu ya da "learn-avalanche skill'ini kullan" demek gerekiyor mu, `AskUserQuestion` yoksa numaralı liste yedeği çalışıyor mu, ev klasörüne yazabiliyor mu, `scripts/chain.py` yolunu kurulu konumdan doğru kuruyor mu (kabuğun çalışma klasörü skill klasörü değildir) | |
| ☐ | **1.5 erken Fuji:** Stage 1 sonunda (cüzdan hazırsa) `BadgeBook` Fuji'ye gidiyor; `owner()` öğrencinin adresi; `award` sonrası `badgeCount` = 1; imza öncesi `memory.md` yazılıyor; cüzdan hazır değilse 1.5 atlanıp "ertelendi" yazılıyor; Stage 4'te öğrenci pencereyi kendisi anlatıyor | |
| ☐ | **Fikir kartı:** Stage 5 kapanışında öğrenci 5 satırı kendi yazıyor, ajan yazmıyor; fikri yoksa "yok" kabul ediliyor; program yönlendirmesinde ajan açık/kapalı durumu, tutar, koşul ya da tarih **söylemiyor** | |
| ◐ | **`python3 scripts/verify-facts.py`** ağı olan makinede: 5 kontrolün sonucu doğru ayrılıyor (OK / DEĞİŞMİŞ / ERİŞİLEMEDİ); bayat bir yol gerçekten DEĞİŞMİŞ çıkıyor (geliştirme ortamında yalnızca ağ yokken ERİŞİLEMEDİ yolu görüldü) | ağlı makinede 5/5 OK ✓ (2026-10-04). Bayat yolun DEĞİŞMİŞ çıkması denenmedi |
| ☐ | **Bilgi yaşı:** `live-facts.md` tarihi 45 günden eskiyken ajan öğrenciye bir kez söyleyip betiği koşuyor, `live-facts.md`'ye yazmıyor | |
| ◐ | `live-facts.md` → Ekosistem programları: her satırın bağlantısı hâlâ açılıyor ve durum notu doğru | 16 bağlantının tümü HTTP 200 (iki RPC adresi GET'e 405, beklenen) ✓ (2026-10-04). Durum notlarının doğruluğu insan kontrolü |

## Sonuç

Tümü ☑ olunca: `CHANGELOG.md`'ye "insan doğrulaması: <tarih>, <kim>" ekle ve sürüm etiketi at (`git tag v0.2.0-beta`).
