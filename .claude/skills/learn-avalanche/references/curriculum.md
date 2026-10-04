# Müfredat haritası

İçindekiler: Proje · Mimari · Aşamalar, süre, bağımlılıklar · Çıkış kriterleri · Academy eşlemesi · Seviyeye göre yönlendirme · Alternatif projeler.

**Kapsam:** Solidity temelleri → kendi Avalanche L1'ini kurup içinde bir sözleşme çalıştırmaya kadar. **Araçlar:** Remix IDE + Core cüzdanı + Builder Console. Öğrenci hiçbir şey kurmaz (Core eklentisi hariç). ICM/ICTT/otomatik test kapsam dışı: `references/roadmap-next.md`.

## Proje: topluluk rozeti

Bir topluluk, etkinliğe katılana ya da görevi bitirene **devredilemez bir rozet** verir. Küçük, ama şu ihtiyaçları doğal olarak üretir:

| İhtiyaç | Öğretilen kavram | Aşama |
|---|---|---|
| "Kim, hangi rozeti, ne zaman aldı?" | state, struct, mapping, storage/memory/calldata | 1 |
| "Sadece organizatör verebilsin" | `msg.sender`, modifier, custom error | 1 |
| "Dış dünya ne olduğunu nasıl duyar?" | event, indexed | 1 |
| "Cüzdanlar/pazaryerleri rozeti tanısın" | ERC-721, interface, `supportsInterface` | 2 |
| "Birden çok organizatör, tek yönetici" | AccessControl rolleri | 2 |
| "Rozet satılamasın/devredilemesin" | miras + `_update` ile davranışı kısıtlama (soulbound) | 2 |
| "Para tutan kod güvenli mi?" | reentrancy, CEI, kilit, hata kataloğu | 3 |
| "Gerçek bir ağda çalışsın" | cüzdan, imza, EVM sürümü, deploy, ölçüm | 4 |
| "Kendi kurallarımız, kendi gas'ımız olsun" | L1, P-Chain kaydı, validator, özel ağ, (precompile) | 5 |

Öğrenci başka bir proje isterse (bağış kasası, bilet, oy verme…) bu tablonun sütunlarını **kendi projesine eşle**; müfredatın omurgası kavram sırasıdır, rozet taşıyıcıdır. Ama kabul tabloları ve `answer-keys/` rozet projesine bağlıdır; farklı projede kabul kriterlerini öğrenciyle birlikte **öğrenci yazar** (sen hakemlik edersin).

## Mimari (Stage 5 sonu)

```
   Fuji C-Chain (43113)                       Öğrencinin L1'i (Console ile kuruldu)
 ┌───────────────────────────┐             ┌────────────────────────────────────┐
 │ Badge (soulbound ERC-721) │             │ Badge (aynı kod, kendi gas token)   │
 │ AVAX ile ücret            │   ✗ konuşmaz │ kendi token'ıyla ücret              │
 └───────────────────────────┘  (iki ayrı   └────────────────────────────────────┘
                                 state; ICM
                                 ile konuşurlar: roadmap-next.md)
```

Aynı bytecode iki bağımsız ağda çalışır; bunu öğrencinin kendisi göstermiş olur.

## Aşamalar, süre, bağımlılıklar

Süreler öğrencinin ilk geçişi içindir (bekleme dahil değil).

| Aşama | Süre | Önkoşul | Dış bağımlılık |
|---|---|---|---|
| 0 Hazırlık | 45–60 dk | yok | Chrome, Core eklentisi, Builder hesabı, faucet |
| 1 Solidity temelleri | 2–3 sa (+20 dk: 1.5) | 0 (cüzdansız da olur; 1.5 için Core + test AVAX) | Remix (internet); 1.5: Fuji RPC, faucet |
| 2 Kontrat tasarımı | ~2 sa | 1 | Remix'in OpenZeppelin (npm) içe aktarması |
| 3 Güvenlik | ~2 sa | 2 | — |
| 4 Fuji'ye deploy | ~1,5 sa | 2 + Core + test AVAX | Faucet, Fuji RPC |
| 5 Kendi L1'in + kapanış | 2–3 sa | 4 + P-Chain test AVAX | Console, yönetilen düğüm (**3 gün**), Core |

Toplam yaklaşık **11–14 saat**, birkaç oturuma yayılır. **5. aşamaya girmeden** öğrenciye 3 günlük yönetilen düğüm penceresini söyle ve 5'i tek oturuma/aynı haftaya yerleştirmeyi öner.

## Çıkış kriterleri (özet; ayrıntı her aşama dosyasında)

| Aşama | Kanıt |
|---|---|
| 0 | Core hazır, bakiye > 0 (`chain.py balance`); Remix'te derle-deploy-çağır döngüsü; blok aralığı ölçüldü |
| 1 | `BadgeBook` v3 kabul adımları Remix'te geçti; öğrenci kendi özelliğini kendi kabul kriterleriyle ekledi; (cüzdan hazırsa) `BadgeBook` Fuji'de doğrulandı (1.5) |
| 2 | `Badge` kabul 1–11 geçti; `_update` neden tek nokta anlatıldı |
| 3 | Bilerek yazılan açıklı kasa sömürüldü (11 ETH), iki düzeltme saldırıyı durdurdu; tehdit modeli yazıldı |
| 4 | `Badge` Fuji'de (`chain.py tx/code/call` ile doğrulandı); mint başarılı; imza penceresi okundu; süre/gas ölçüldü |
| 5 | L1 canlı; `Badge` L1'de deploy; L1 vs C-Chain kararı yazıldı; 5 dk anlatım + paylaşım metni |

## Academy eşlemesi (derinleşmek isteyene)

| Aşama | Resmî kaynak |
|---|---|
| 0 | `blockchain/blockchain-fundamentals`, `avalanche-l1/avalanche-fundamentals` (Multi-Chain Architecture, Set Up Core Wallet) |
| 1–3 | `blockchain/solidity-foundry` (Intro to Solidity: Hello World 1–2, Contract Standardization, ERC-20; Foundry kullanır, biz Remix) |
| 4 | `/docs/avalanche-l1s/add-utility/deploy-smart-contract` (Remix + Core, Cancun uyarısı) |
| 5 | `avalanche-l1/avalanche-fundamentals` "Creating an L1", `permissioned-l1s`, `access-restriction`, `l1-native-tokenomics`, ileri: `customizing-evm` |

Kurs URL'leri ve numaralar için `references/live-facts.md` → Dokümana erişim. **Ders yolu sabitleme** (yollar yönlendirilebilir).

## Seviyeye göre yönlendirme

Seviye beyanla değil, `references/placement.md`'deki tanıyla **ölçülür** (hafızada `Seviye (ölçülen)`); ders ilerledikçe canlı ayarlanır (`references/teaching-method.md`). Aşağıdaki başlıklar o değerlere karşılık gelir.

- **Hiç kod yazmadım (`hiç-kod`):** Stage 0'ı tam yap; Stage 1'de her göreve başlamadan önce "değişken/fonksiyon nedir" mini bloğu (sözle) ve dikte basamağını daha erken sun. Solidity'den önce 10 dakikada "program = veri + kurallar" çerçevesi.
- **JS/Python biliyorum (`js-python`):** Stage 0'ı hızlı geç. Odak: statik tipler, `uint`, gas, "deploy edilen kod değişmez". 1.1'i 20 dakikaya sıkıştırabilirsin.
- **Solidity'ye başlamıştım (`solidity-başladı`):** Stage 1 tanısı (B1–B3: data location, custom error vs require, `msg.sender` vs `tx.origin`) seviye tespitinde yapıldı ve geçildi. 1'i atla; 2'den başla, bol "bozup tahmin et".
- **Zaten kontrat yazıyorum (`kontrat-yazıyor`):** (C1–C3 geçildi.) Stage 3, 4, 5'e odaklan; 1–2'yi yalnızca kabul tablolarını geçerek doğrula.
