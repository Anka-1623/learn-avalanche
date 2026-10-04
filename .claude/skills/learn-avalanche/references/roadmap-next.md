# Yol haritası: beta'dan sonrası

Bu dosya, beta'nın **kapsamı dışındaki** konuları özetler. Buradaki hiçbir şey beta'da uygulamalı ders olarak sunulmaz ve bu dosyaya dayanarak bir öğrenciye "bunu birlikte yapacağız" denmez; öğrenci kapanışta "sonra ne?" diye sorarsa yönlendirme kaynağıdır.

## Sıradaki sürümlerin adayları

| Konu | Neden bu sırada | Durum |
|---|---|---|
| **ICM (Interchain Messaging)**: L1'deki bir olayı Fuji C-Chain'e duyurmak | Bir L1'in asıl gücü diğer zincirlerle konuşmasıdır; ihtiyaç Stage 5'te ortaya çıkar ("iki `Badge` birbirini tanımıyor") | Doğrulanmış cevap anahtarları var: `answer-keys/next-icm/` + `maintainers/forge-suite/test/Interchain.t.sol` (6 test, mutasyonlar yakalanıyor). Canlı relayer + iki ağ adımları **denenmedi**. |
| **Otomatik test** (Remix Unit Testing; sonra Foundry fuzz/invariant) | Elle kabul tablosu ölçeklenmez | Remix eklentisi: `remix_tests.sol`, `_test.sol` dosyaları, `Assert.equal`; test sözleşmesinde parametreli fonksiyon olmaz. Anahtar testler `maintainers/forge-suite/`'te Foundry için hazır. |
| **ICTT** (token köprüleme) | ICM'den sonra doğal adım | Academy `erc20-bridge`, `native-token-bridge`; Console "ICTT Setup". |
| **Precompile'lar ve L1 ekonomisi** | Native minter, fee manager, reward manager | Academy `customizing-evm`, `l1-native-tokenomics`. |
| **Foundry'ye geçiş** | Profesyonel akış: yerel test, script, CI | Anahtar: `maintainers/forge-suite/`. Dikkat: makinede `/usr/bin/forge` Foundry olmayabilir (`preflight.sh`). |

## ICM'in iskeleti (doğrulanmış bilgiler; ders değil)

- Katmanlar: **Warp** (kaynak validator setinin BLS imzası; Warp precompile `0x0200…0005`) → **ICM/Teleporter** (mesaj protokolü; `TeleporterMessenger` her zincirde aynı adreste, ICM sürümüne göre değişir) → uygulama. Mesajı hedefe taşıyan **relayer** zincir dışı bir programdır; çalışmazsa mesaj teslim edilmez. (Builder hesabıyla Console ücretsiz yönetilen ICM relayer verir.)
- Hedef zincir **blockchain ID** (32 bayt) ile seçilir, chain ID ile değil.
- Alıcı sözleşme **üç şeyi** doğrulamalıdır: çağıran gerçekten Teleporter mı, mesaj beklenen kaynak zincirden mi, beklenen gönderici mi. Bunların hiçbiri atlanamaz (mutasyon testleri bunu gösterir).
- Adresler ve doğrulama yöntemleri: `references/live-facts.md` → ICM.

## Bakımcıya not

Bir sonraki sürüme geçmeden önce: (1) `maintainers/forge-suite/run.sh` tümüyle yeşil, (2) `docs/verification-checklist.md` bir insan tarafından gerçek tarayıcıda baştan sona koşulmuş, (3) `references/live-facts.md` tarihleri güncel.
