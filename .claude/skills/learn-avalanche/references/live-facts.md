# Canlı gerçekler (Avalanche)

**Doğrulama tarihi: 2026-09-30.** Kaynaklar: build.avax.network dokümanları ve Academy, Remix dokümanı, Fuji C-Chain'e karşı canlı çağrılar (`scripts/chain.py`, ayrıca Foundry `cast` ile çapraz kontrol). Bu tablo eskir: bir komut/adres/URL öğretmeden önce "Yeniden doğrula" notundaki kontrolü yap, özellikle tarihten haftalar geçtiyse. Bir gerçek değiştiyse burayı güncelle. Beş temel kontrolü tek komutla koşmak için: `python3 scripts/verify-facts.py` (DEĞİŞMİŞ = bu konudan öğretme; ERİŞİLEMEDİ = ağ yok, sonuç hakkında bir şey söylemez). "Ekosistem programları" bölümü bu betikte yok; onu sayfadan elle oku.

İçindekiler: Ağlar · Cüzdan, hesap, faucet · Zincire özgü sabitler · EVM sürümü · Araçlar · L1 oluşturma · Precompile'lar · ICM (sonraki) · Yükseltmeler · Ekosistem programları · Dokümana erişim · Terimler · Bilinen tuzaklar.

## Ağlar

| | C-Chain Mainnet | C-Chain Fuji (testnet) |
|---|---|---|
| Chain ID | 43114 (0xA86A) | **43113** (0xA869) |
| RPC | `https://api.avax.network/ext/bc/C/rpc` | `https://api.avax-test.network/ext/bc/C/rpc` |
| Explorer (HTTP 200, 2026-09-30) | `https://explorer.avax.network/c-chain` | `https://explorer-test.avax.network/c-chain` |

P-Chain: `…/ext/bc/P`; X-Chain: `…/ext/bc/X`. Bu kurs yalnızca **Fuji** ve **öğrencinin L1'i** ile çalışır.

**Yeniden doğrula:** `python3 scripts/chain.py chain-id` → 43113.

## Cüzdan, hesap, faucet

- **Core zorunludur.** Academy: "Core is the only wallet that supporting issuing P-Chain transactions, so it is not possible to use other wallets such as MetaMask or Rabby." L1 oluşturmak P-Chain işlemi gerektirir; bu yüzden tüm kurs boyunca tek cüzdan Core. Core eklentisi **Chrome** içindir (Academy "Download the Core Extension for Chrome"). Cüzdan oluştururken "Google ile devam" ya da elle yeni cüzdan seçeneği vardır.
- **Builder Account** (Builder Hub hesabı; Console'dan açılır). Academy'ye göre: (1) faucet'ten **kuponsuz ve mainnet bakiyesi olmadan** C-Chain ve P-Chain test AVAX, (2) **ücretsiz yönetilen testnet düğümü ve ICM relayer**. Hesapsız da kurs tamamlanabilir ama daha zor.
- **Faucet:** Console → Testnet Faucet (`https://build.avax.network/console/primary-network/faucet`). Builder hesabıyla token'lar otomatik ya da düğmeyle gelir. **Alternatif (hesapsız):** harici Avalanche Faucet (`https://core.app/tools/testnet-faucet/`, HTTP 200) + Academy'nin verdiği kupon kodu (`avalanche-academy` ya da `avalanche-academy25`, C-Chain'e 2 AVAX). Sonra C→P aktarma aracıyla P-Chain'e. Kuponlar ve arayüz değişebilir; sayfayı öğrenciyle birlikte oku.
- **Testnet Mode** Core'da ayarlardan açılır (menü adı sürüme göre değişebilir; ekran görüntüsü iste).

**Yeniden doğrula:** `python3 scripts/fetch-doc.py /academy/avalanche-l1/avalanche-fundamentals/04-creating-an-l1/02-connect-core` ve `…/02a-claim-testnet-tokens` (yönlendirme uyarısı yoksa yol geçerli).

## Zincire özgü sabitler (Fuji C-Chain)

- C-Chain **blockchain ID** (32 bayt): `0x7fc93d85c6d62c5b2ac0b519c87010ea5294012d1e407030d6acd0021cac10d5` (Warp precompile `getBlockchainID()` ve Teleporter `blockchainID()` aynı değeri döndürdü). **Chain ID (43113) ile karıştırma.**
- Blok aralığı ve gas fiyatı: **rakam öğretme, öğrenci ölçsün** (`chain.py block-times 20`; doğrulama günü 10 blokta ortalama ~1,7 sn, zaman damgası tam saniye olduğundan kaba). Ücret mekanizması yükseltmelerle değişti (ACP-125, ACP-176/226).

## EVM sürümü: `cancun` (en sık düşülen tuzak)

Avalanche **C-Chain ve Subnet-EVM (L1'ler)** Ethereum'un **Cancun** sürümünü destekler; Pectra ve sonrasını henüz desteklemez. Solidity **0.8.30+** varsayılan hedefi Pectra'ya çevirdi; açık belirtmezsen üretilen bytecode zincirin desteklemediği şeyler içerebilir. **Remix'te:** Solidity Compiler → *Advanced Configurations* → **EVM Version = cancun** (`/docs/avalanche-l1s/add-utility/deploy-smart-contract`).

Sayfadaki gizli not: bu uyarı, Avalanche **Pectra desteğini eklediğinde kaldırılacak** ("after Continuous Execution implementation", ACP-194 sonrası; son gözden geçirme Aralık 2025). Yani zincir yükseldiğinde bu kural değişir; önce sayfayı kontrol et.

**Yeniden doğrula:** `python3 scripts/fetch-doc.py /docs/avalanche-l1s/add-utility/deploy-smart-contract --grep '(?i)cancun|pectra'`.

## Araçlar: neyi kullan, neyi kullanma

| Araç | Durum (2026-09-30) | Not |
|---|---|---|
| **Remix IDE** (`remix.ethereum.org`) + **Core** | **Bu kursun ana yolu** | Avalanche'ın kendi öğreticisi de bunu kullanır. Environment adları için `references/remix-guide.md`. |
| **Builder Console** (`build.avax.network/console`) | L1 oluşturma, faucet, düğüm, ICM/ICTT kurulumu için **resmî yol** | Tarayıcı + Core ister; ajan tıklayamaz, öğrenciyi yönlendirir. Menü: Create L1, My L1 Dashboard, Testnet Faucet, Testnet Nodes, ICM Relayer, ICM Setup, ICTT Setup… |
| **Platform CLI** | P-Chain işlemleri için (staking, subnet/L1 validator, anahtar) | Solidity deploy etmez, yerel ağ çalıştırmaz. Beta'da kullanılmaz. |
| **Avalanche CLI** (`avalanche blockchain create …`) | **Artık aktif bakımda değil.** Doküman: P-Chain için Platform CLI, gerisi için Builder Console. | Starter kit ve eski dersler hâlâ bunu öğretir. Öğretme; öğrenci eski bir kaynakta görürse "emekli, Console kullanıyoruz" de. |
| **Foundry** (`forge`, `cast`, `anvil`) | Beta'da öğrenciye **gerekmez** | Yalnızca bakımcılar için: `maintainers/forge-suite/`. ⚠ Bazı sistemlerde `/usr/bin/forge` Foundry değildir (`forge --version` → `ZOE ERROR … zoeParseOptions`); `preflight.sh` bunu CONFLICT diye bildirir. |
| **Hardhat** | Geçerli alternatif | Bu kurs Remix'e odaklı. |

## L1 oluşturma (Academy "Avalanche Fundamentals" → Creating an L1)

Akış: Builder hesabı → Core → test AVAX → **CreateSubnetTx** → **CreateChainTx** (Genesis Builder; ad, VM=Subnet EVM, genesis) → **validator düğümü** → **ConvertSubnetToL1Tx** (ilk validator seti + Validator Manager adresi; genesis'e önceden konmuş bir `TransparentUpgradeableProxy` başlangıç adresi olur; dönüşümden sonra subnet sahibi yetkisini kaybeder) → **test et** → düğümü kaldır.

- **Ücretsiz yönetilen testnet düğümü** (Builder hesabıyla, Console'da tek tık, Docker gerekmez) **3 gün sonra otomatik kapanır.** Tek validator'lü L1'de düğüm kapanınca zincir durur. Stage 5'i 72 saat içinde bitirmeyi planla; kapanış tarihini `memory.md`'ye yaz.
- Self-host seçeneği Docker: ~4 vCPU / 8 GB RAM, portlar 9651 (P2P) ve 9650 (RPC); üretim için 5+ validator önerilir.
- L1 validator'ları (ACP-77) **sürekli ücret** öder (ön yüklemeli bakiyeden; bakiye biterse validator pasifleşir).
- Create Chain'de "internal error" görülürse Academy: subnet henüz indekslenmemiş olabilir, 1 dakika bekle.
- Özel ağı Core'a eklemek için alanlar (Avalanche dokümanı): Network Name, RPC URL (`…/ext/bc/<blockchainID>/rpc` biçimi), Chain ID, Symbol, Explorer (N/A).
- C-Chain mi L1 mi? `/docs/avalanche-l1s` ("Advantages") ve `/blog/l1-economics`. Eski `/docs/dapps/*` bölümü kaldırıldı (yönlendirilir).

## Precompile adresleri (resmî Subnet-EVM/Coreth dokümanı)

| Adres | Precompile |
|---|---|
| `0x0200000000000000000000000000000000000000` | ContractDeployerAllowList |
| `…0001` | NativeMinter |
| `…0002` | TxAllowList |
| `…0003` | FeeManager |
| `…0004` | RewardManager |
| `…0005` | Warp (C-Chain'de kod boyutu 1: aktif) |

Allowlist arayüzü (dokümandan): `readAllowList(address) → uint256` (`0 = None`, `1 = Enabled`, `2 = Admin`), `setAdmin`, `setEnabled`, `setManager`, `setNone`. Bir L1'de precompile yalnızca genesis'te etkinleştirildiyse vardır (`chain.py --rpc <L1> code <adres>`).

## ICM (Interchain Messaging / Teleporter): beta dışı, referans

| Ne | Değer (Fuji C-Chain'de doğrulandı) |
|---|---|
| `TeleporterMessenger` | `0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf` (dokümana göre tüm zincirlerde aynı; ICM major sürümüne göre değişir; `chain.py code` ile 13.013 bayt) |
| `TeleporterRegistry` (Fuji C-Chain) | `0xF86Cb19Ad8405AEFa7d09C778215D2Cb6eBfB228` (`getLatestTeleporter()` messenger'ı döndürdü) |
| `sendCrossChainMessage(...)` selector | `0x62448850` (canlı bytecode'da bulundu) |

Ayrıntı ve güvenlik notları: `references/roadmap-next.md`.

## Yükseltmeler (bağlam; tarih ezberletme)

Etna (mainnet 16 Aralık 2024): ACP-77 (L1'ler), ACP-125 (min base fee düşürüldü). Granite (Fuji 29 Ekim 2025): P-Chain epoched views for ICM, secp256r1, dinamik minimum blok süreleri (ACP-226). Ayrıca ACP-194 (Continuous Execution). Güncel liste: `/docs/nodes/releases`.

## Ekosistem programları (hibe, kuluçka, yarışma)

**Bu bölümün doğrulama tarihi: 2026-10-03** (resmî sayfalar canlı okundu). Açık/kapalı durumu hızla değişir. **Öğrenciye "açık" deme; tutar, koşul ya da tarih söyleme.** "Şu sayfaya bak, durum orada yazıyor" de ve sayfayı birlikte oku. Aşağıdakiler yalnızca sayfaların o gün söylediğidir.

| Program | Sayfaya göre ne | Kaynak | Durum notu (2026-10-03) |
|---|---|---|---|
| **Team1 Builder Grants** (sayfada "Team1 Mini Grants") | Avalanche üzerinde akıllı kontrat yazan, uygulama yapan ya da ekosisteme katkı veren geliştiriciler için hızlı, odaklı hibe; bir Team1 programı | `https://docs.avax.network/grants/team1-mini-grants`, `https://team1.network/grants` | Sayfa uygunluk koşulu, tutar ve son tarih **vermiyor**; "Apply Now" düğmesi var |
| **Codebase** (kuluçka) | 10 haftalık kuluçka + hoş geldin haftası; erken aşama kurucular. Sayfaya göre şirket 500.000 doların altında fon toplamış olmalı ve 24 ay Avalanche üzerinde inşa etmeyi taahhüt etmeli | `https://codebase.avax.network/` | Sayfa **Season 4**'ü gösteriyor ve başvurular **kapalı** (kayıt 4 Mayıs–6 Haziran; yatırımcı sunum günü 9 Aralık; sayfada yıl yazmıyor). Sonraki dönem için `build.avax.network`'te posta listesi |
| **Build Games** | Altı haftalık küresel çevrimiçi yarışma, 1 milyon dolarlık ödül havuzu | duyuru: `https://www.avalanche.com/about/blog/avalanche-launches-1m-competition-build-games` (20 Ocak 2026); başvuru: `https://build.avax.network/build-games` | 20 Ocak 2026'da başladı; **güncel turun durumu doğrulanmadı** |
| **Blizzard Fund** | Avalanche projelerine yatırım yapan fon (sayfada "$200M+") | `https://www.blizzard.fund/` | Proje ekipleri için; öğrenci aşamasına uygun değil |
| **Güvenlik denetimi** | Ava Labs'ın onaylı denetçilerinden teklif; sayfaya göre %75'e kadar sübvansiyonlu | `https://docs.avax.network/audits` | Mainnet'e çıkacak proje için |
| Diğerleri | Geliştirici kredileri (Space & Time), Game Accelerator (Helika), akademik araştırma teklifleri, güvenlik bug bounty'si | `https://docs.avax.network/grants` | Listede; ayrıntı ilgili sayfada |
| **Retro9000** | Blogda dört kohort duyurusu var | `avax.network` blogu | `docs.avax.network/grants` listesinde **görünmüyor**; güncel durumu doğrulanmadı |

**Yeniden doğrula:** `https://docs.avax.network/grants` sayfasını aç; liste ve durum satırları orada. `verify-facts.py` bunu kapsamaz.

## Dokümana erişim (ajan için)

1. **Resmî Avalanche MCP sunucusu** (salt-okunur): `https://build.avax.network/api/mcp`. Araçlar: `docs_search`, `docs_fetch`, `docs_list_sections`, `cli_lookup_command`, `rpc_lookup_method`, `acp_lookup`, `github_search_code`, `blockchain_get_native_balance`… Kurulum: `claude mcp add avalanche-mcp --transport http https://build.avax.network/api/mcp`. Bağlıysa ilk tercih; değilse öğrenciye öner, kendin ekleme.
2. **`scripts/fetch-doc.py <yol>`**: `.md` uçlarını dener, HTML gelirse metne çevirir, `--grep REGEX` ile süzer.
3. **`scripts/chain.py`**: salt-okunur zincir kontrolü (`chain-id`, `block`, `block-times`, `balance`, `code`, `call`, `tx`, `keccak`). `--rpc URL` ile öğrencinin L1'i. Anahtar tutmaz, işlem gönderemez.
4. **`https://build.avax.network/llms.txt`**: bölümlere ayrılmış dizin. `llms-full.txt` ~4 MB; bağlamına yükleme, `grep` ile ara.
5. **Kaldırılmış yollar 404 vermez, başka bir sayfaya yönlendirilir.** Eski `/docs/dapps/toolchains/foundry` bir Academy dersine, `/docs/dapps/c-chain-or-avalanche-l1` genel "Primary Network" sayfasına gider. `fetch-doc.py` son URL'yi istenenle karşılaştırır: yönlendirme varsa `WARNING: REDIRECTED …` yazar ve **çıkış kodu 2** döner (geçerli 0, gerçek 404 ise 1). Uyarı varsa o sayfadan öğretme; doğru yolu `llms-full.txt`'te başlıkla ara ya da MCP `docs_search` ile bul.
6. `…/docs/<sayfa>.md` gerçek Markdown döndürür; Academy **ders** sayfalarında `.md` bazen HTML kabuğu döndürür (script halleder). Academy ders yolları ve numaraları değişebilir: **ders URL'si sabitleme, kurs + başlık kullan.**

Academy kursları (kurs düzeyi, 2026-09-30):
`/academy/avalanche-l1/` → `avalanche-fundamentals`, `customizing-evm`, `interchain-messaging`, `erc20-bridge`, `permissioned-l1s`, `l1-native-tokenomics`, `permissionless-l1s`, `native-token-bridge`, `access-restriction`.
`/academy/blockchain/` → `blockchain-fundamentals`, `solidity-foundry` (Intro to Solidity), `nft-deployment`, `encrypted-erc`, `x402-payment-infrastructure`.
`/academy/entrepreneur/` → `foundations-web3-venture`, `fundraising-finance`, `go-to-market`, `web3-community-architect`.

## Terim sözlüğü

| Eski / gayri resmi | Güncel |
|---|---|
| Subnet | **Avalanche L1** (subnet, L1'e dönüşmeden önceki P-Chain nesnesini anlatır) |
| Teleporter | **ICM** (Interchain Messaging); kontrat adları hâlâ `Teleporter*` |
| AWM | **Avalanche Warp Messaging** |
| Avalanche CLI | emekli → Platform CLI + Builder Console |
| Injected Provider / Injected Web3 | Remix'te güncel etiket **Browser Extension** (aynı iş) |

## Bilinen tuzaklar (öğrenci bunlara düşer)

1. Remix'te **EVM Version = cancun** seçilmedi (yukarıda).
2. MetaMask ile L1 kurmaya çalışmak: P-Chain işlemi yalnızca Core'da.
3. Remix VM durumu geçicidir; sayfa yenilenince deploy edilen örnekler silinir.
4. Constructor'a `admin` adresini yanlış yazmak: kimse mint edemez; yeniden deploy. Adresleri kopyala, elle yazma.
5. OpenZeppelin v5'te `_beforeTokenTransfer` yok; mint/transfer/burn hepsi `_update`'ten geçer. v4 öğreticileri v5'te derlenmez. Sürümü import yoluna yaz (5.6.1).
6. Yönetilen L1 düğümü 3 günde kapanır; zincir durur.
7. Genesis'teki ilk bakiye yanlış adrese verilirse L1'de deploy edilemez; yeniden kurmak dışında ucuz çözüm yoktur.
8. Kaldırılmış doküman yolları başka sayfaya yönlendirilir (yukarıda).
