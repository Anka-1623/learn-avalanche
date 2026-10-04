# Remix rehberi (ajan için)

İçindekiler: Neden Remix + Core · Doğrulanmış temel bilgiler · Kurulum akışı · Derleyici ayarı (EVM sürümü!) · Deploy & Run paneli · Çıktıları okuma · OpenZeppelin içe aktarma · Sık takılmalar · Emin olmadığın yerler.

**Uyarı:** Remix arayüzü sık güncellenir. Aşağıdakilerin bir kısmı resmî dokümandan doğrulandı (işaretli), kalanı bilinen kullanımdır. Bir etiket öğrencinin ekranında yoksa tartışma, **ekran görüntüsü iste** ve ekrandakine güven. Doğrulanmayan yerleri repo `docs/verification-checklist.md` dosyasında bir insan gerçek tarayıcıda kontrol etmek için listelendi.

## Neden Remix + Core

- Remix tarayıcıda çalışır: kurulum yok, kod öğrenci ekranındadır, sen dosya yazamazsın. Bu "kodu öğrenci yazar" kuralıyla birebir uyumludur.
- **Core cüzdanı zorunlu:** P-Chain işlemi (L1 oluşturma) yapabilen tek cüzdan Core'dur; MetaMask/Rabby yapamaz (Academy, "Install Core Wallet"). Bu yüzden Remix'te de aynı cüzdanı kullanırız: tek cüzdan, tek kimlik. Core'un Chrome eklentisi vardır; tarayıcı olarak Chrome kullandır.
- Avalanche'ın kendi öğreticisi de bu akışı izler: Remix → Deploy sekmesi → Environment: *Injected Web3* (Core yüklüyken) → Compile → Deploy → Core penceresinde onay (`/docs/avalanche-l1s/add-utility/deploy-smart-contract`).

## Doğrulanmış temel bilgiler

- **Environment seçenekleri (Remix dokümanı, 2026-09-30):** `Remix VM` (tarayıcıda sahte zincir, cüzdan gerekmez) · `Browser Extension` (eskiden *Injected Provider*; Avalanche dokümanı hâlâ "Injected Web3" der: aynı şey, cüzdan eklentisini kullanır) · `WalletConnect` · `Hardhat Provider` · `Foundry Provider` · `External HTTP Provider` · `Forked State`. Öğrenciye: "Environment açılırken içinde 'Browser Extension' ya da 'Injected Provider' benzeri bir seçenek var; onu seç."
- **Unit test eklentisi (Remix dokümanı):** `remix_tests.sol` ve `remix_accounts.sol` ile, dosya adı `_test.sol` ile biter, `Assert.equal(...)`. Beta'da kullanılmıyor (öğrenci testi elle Remix arayüzünden yapıyor); `references/roadmap-next.md`'ye bak.
- **EVM sürümü (Avalanche dokümanı):** Remix → Solidity Compiler paneli → *Advanced Configurations* → **EVM Version = cancun.** Avalanche C-Chain ve Subnet-EVM Cancun'u destekler, Pectra'yı henüz değil (`references/live-facts.md`).
- **Cüzdan ağı ekleme (Avalanche dokümanı):** Network Name, RPC URL, Chain ID, Symbol, Explorer alanları.

## Kurulum akışı (özet; ayrıntı `references/stages/00-setup.md`)

1. Chrome'da `remix.ethereum.org` aç → varsayılan workspace.
2. Core eklentisini kur → **yeni** bir cüzdan oluştur (bu kurs için) → Testnet Mode (ayarlarda; menü adı sürüme göre değişebilir) → Fuji.
3. Remix'te sol menüden sırayla: **File explorer** (dosyalar), **Solidity compiler**, **Deploy & run transactions**. Alt tarafta **terminal/konsol**: işlem çıktıları burada.

## Derleyici ayarı (her egzersizde)

1. Solidity compiler sekmesi → **Compiler** açılır listesinden `0.8.24` veya üstü bir sürüm (öneri: `0.8.28` ya da listedeki yakın bir kararlı sürüm; OpenZeppelin 5.x `^0.8.24` ister). Dosyadaki `pragma solidity ^0.8.24;` ile uyumlu olmalı.
2. **Advanced Configurations** → **EVM Version: cancun.** Bunu Stage 1'de bile yaptır; alışkanlık olsun, Stage 4'te Avalanche'a giderken unutulmasın.
3. Compile düğmesi (ya da *Auto compile*). Yeşil tik = derlendi. Sarı uyarılar (warning) normalde durdurmaz; kırmızı hatalar durdurur.

## Deploy & Run paneli

| Alan | Ne işe yarar / bilinmesi gereken |
|---|---|
| **Environment** | `Remix VM` = sahte zincir. `Browser Extension` = Core, gerçek (test) ağ. |
| **Account** | Remix VM'de birkaç hazır hesap (sahte bakiyeli). **Hesabı değiştirmek `msg.sender`'ı değiştirir**: yetki testlerinin anahtarı. Adresi kopyalamak için yanındaki kopyala simgesi. |
| **Gas limit** | Varsayılan genellikle yeter. Deploy "out of gas" ile dönerse artır. |
| **Value** | Payable fonksiyona/constructor'a gönderilen miktar. Yanındaki birim seçiciden `wei / gwei / ether`. Stage 3'te `ether` seç. |
| **Contract** | Derlenmiş sözleşmeler; aynı dosyada birden çok sözleşme varsa doğru olanı seç. |
| **Deploy** | Constructor parametresi varsa düğmenin yanındaki kutuya yazılır. **String değerler tırnak içinde**: `"Workshop"`. Adresler `0x…` olarak. Boş string: `""`. |
| **Deployed Contracts** | Deploy edilen örnek(ler). Yanında **bakiye** görünür (Stage 3'te reentrancy kanıtı). Fonksiyon düğmeleri: **mavi** = sadece okur (`view`/`pure`, ücretsiz), **turuncu** = state değiştirir, **kırmızı** = `payable`. |
| **At Address / Add Contract** | Zaten deploy edilmiş bir sözleşmeye adresle bağlanır (Stage 5'te precompile için). Derlenmiş ABI gerektirir. |

## Çıktıları okuma

- **Terminal/konsol:** her işlem bir satır: yeşil tik = başarılı, kırmızı = geri alındı (revert). Satırı aç → `status`, `logs` (event'ler), `transaction cost` (gas). Sonuç kanıtları burada.
- **Custom error'lar:** ABI bilindiği için Remix çoğunlukla hata adını gösterir (ör. `NotOwner`, parametrelerle). Görünmüyorsa 4 baytlık selector görünür; `python3 scripts/chain.py keccak "NotOwner()"` ile eşleştirebilirsin.
- **Event'ler:** işlemi genişlet → `logs` bölümünde çözülmüş (decoded) argümanlar.
- **Debug:** işlem satırındaki *Debug* düğmesi adım adım çalıştırmayı gösterir (ileri seviye, isteğe bağlı).
- **Remix VM durumu geçicidir**: sayfayı yenilemek/çalışma alanını sıfırlamak deploy edilmiş örnekleri siler. Dosyalar kalır. Öğrenciye söyle.

## OpenZeppelin'i içe aktarma

Remix, `@openzeppelin/contracts/...` yollarını npm'den otomatik çeker. **Sürümü yola yazarak sabitle**, çünkü "en son sürüm" zamanla değişir ve cevap anahtarımız v5 API'sine (`_update`) dayanır. Doğrulanmış sürüm: **5.6.1** (npm `latest`, 2026-09-30; anahtarlar bu paketle test edildi). Yolun biçimi: `@openzeppelin/contracts@5.6.1/…` (Remix bunu destekler; çalışmazsa sürümsüz yolu dene ve derlenen sürümü kontrol et). Öğrencinin tam yolu bulması egzersizin parçasıdır: OpenZeppelin dokümanındaki ilgili sayfayı okuyup yolu kendisi yazar.

## Sık takılmalar

| Belirti | Olası neden | Nasıl yönlendirirsin |
|---|---|---|
| Kırmızı: `ParserError` / `Expected ';'` | Noktalı virgül/parantez | Satır numarasını okut; "hangi satırdan sonra?" |
| `Data location must be "memory" or "calldata"` | String/dizi parametresinde veri konumu yok | Bilerek yaşat (Stage 1.1). "Bu iki kelime neyi seçiyor?" |
| `DeclarationError: Identifier not found` | Yazım hatası ya da import yok | Büyük/küçük harf, import satırı |
| `TypeError: Overriding function is missing "override"` | Miras alınan fonksiyonu ezme | Stage 2: derleyicinin dediğini oku |
| `Stack too deep` | Çok yerel değişken | Fonksiyonu böl (nadiren) |
| Deploy: `gas estimation failed` / `revert` | Constructor'da geri alma ya da yanlış argüman | Argümanları (özellikle adres/tırnak) kontrol; konsolu oku |
| İşlem geri alındı ama sebep görünmüyor | Hata adı çözülmedi | Konsolu genişlet; selector'ı `chain.py keccak` ile eşle |
| `Browser Extension` seçeneği yok / Core görünmüyor | Eklenti yüklü değil ya da başka sekmede | Chrome, sayfa yenile, eklenti açık mı |
| Core'da yanlış ağ | Testnet Mode kapalı ya da farklı ağ seçili | Core'da ağı kontrol et; Remix'in gösterdiği chain ID ile karşılaştır (Fuji: 43113) |
| `insufficient funds` | Test AVAX yok/az | Stage 0 faucet; bakiyeyi `chain.py balance` ile doğrula |
| String argümanı kabul etmiyor | Tırnak yok | `"Workshop"` biçimi |

## Emin olmadığın yerler (beta)

Aşağıdakileri **kesin dille söyleme**; öğrenci ekranını sor: Core'da *Testnet Mode*'un tam menü yolu · Remix'te `Browser Extension` etiketinin o anki adı · `@5.6.1` sürüm sabitleme sözdiziminin Remix'in o günkü sürümündeki davranışı · Console ekranlarındaki düğme adları. Bunlar `docs/verification-checklist.md`'de "insan doğrulaması bekliyor" olarak işaretli.
