# Stage 0 — Hazırlık

**Amaç:** Cüzdan ve test AVAX hazır olsun; öğrenci Remix'i tanısın; "zincir nedir"i doğru bir modelle görsün ve canlı bir Avalanche ağına **ölçerek** dokunsun.
**Süre:** 45–60 dk (Core kuruluysa ~30). **Önkoşul:** yok. **Kazanım:** cüzdan, adres, gas, blok, EOA vs kontrat kavramlarını kendi ölçümüyle söyleyebilir.

Onboarding cevaplarına göre uzunluğu ayarla: Core kuruluysa 0.2'yi atla; deneyimliyse 0.1'i 3 soruya indir.

## 0.1 Zihinsel model (10 dk, konuşma + çizim)

Tahminle aç: **"Bir arkadaşına AVAX gönderdiğinde, işlemi 'gönder'e bastığın an ile 'para gitti' arasında neler oluyor? Aklına gelen adımları sırala."** Sonra şemayı öğrenciyle birlikte tamamla:

```
cüzdan ── imzalı işlem ──► düğüm (RPC) ──► bekleme havuzu ──► blok içinde sıralanır
                                                 │
                       EVM işlemi çalıştırır: hesap bakiyeleri / sözleşme depoları (state) değişir
                                                 │
                       validator'lar blok üzerinde anlaşır (konsensüs) ──► nihai
```

Avalanche katmanı (bu kadarı yeter; gerisi sonraki aşamalarda): **Primary Network** üç zincirdir: **P** (validator/L1 yönetimi), **X** (varlık), **C** (EVM; Solidity burada çalışır). **L1** = kendi validator seti, kendi kuralları, kendi gas token'ı olan bağımsız zincir (Stage 5). Öğrenciye bir soru bırak; cevabı 0.5'te *ölçerek* bulacak: **"Avalanche'ta yaklaşık her kaç saniyede bir blok üretiliyor?"** (Rakamı sen söyleme.)

## 0.2 Core cüzdanı (10 dk)

Neden Core: **P-Chain işlemi yapabilen tek cüzdan** (L1 kurmak için şart; MetaMask/Rabby yapamaz). Bu kursta Remix'te de aynı cüzdanı kullanacağız.

1. **Chrome** ile Core eklentisini kur (Core'un resmî sitesinden ya da Chrome Web Store'dan). Bağlantıyı öğrenciye ver, sen açmazsın.
2. **Yeni bir cüzdan oluştur, yalnızca bu kurs için.** ("Google ile devam" ya da elle oluşturma seçenekleri var; elle oluşturmak seed'in ne olduğunu göstermesi açısından öğreticidir ama ikisi de kabul.)
3. **Recovery phrase kuralı** (öğrenciye açıkça söyle, çünkü bu kursun en önemli alışkanlığı): kağıda yaz; ekran görüntüsü alma; kimseye gösterme; **bana (ajana) asla yazma.** "İçinde gerçek para olan bir cüzdanı bu kurs için kullanma."
4. Core'da **Testnet Mode**'u aç (ayarlarda; menü adı sürüme göre değişebilir, ekran görüntüsü iste).
5. Core'daki **C-Chain adresini** (`0x…`) kopyalat. Bu adres herkese açıktır, paylaşmak güvenli.

**Kanıt:** öğrenci adresi yapıştırır; sen `python3 scripts/chain.py code <adres>` çalıştırırsın → "no code (EOA or empty)". Sor: "Bu adreste kod yok. Cüzdan adresinin kod içermemesi ne demek?" (EOA = anahtarla kontrol edilen hesap.)

## 0.3 Builder hesabı ve test AVAX (10 dk)

**Builder Console** (`https://build.avax.network/console`) üzerinden bir **Builder Account** aç (Academy önerir): faucet'i kupon ya da mainnet bakiyesi olmadan kullandırır ve **ücretsiz yönetilen testnet düğümü + ICM relayer** verir (Stage 5'te lazım). Ardından Console'da **Testnet Faucet**: Core'u bağla, C-Chain için test AVAX iste. (P-Chain AVAX'ı Stage 5'te isteyeceğiz.)

Alternatif (Builder hesabı istemeyen ya da faucet takılırsa): Academy'nin anlattığı harici Avalanche Faucet + kupon kodu (`references/live-facts.md` → Faucet). Kupon ve arayüz değişebilir: sayfayı öğrenciyle birlikte oku.

**Kanıt:** `python3 scripts/chain.py balance <adres>` → sıfırdan büyük. Sor: "Bu AVAX'ın gerçek para değeri var mı? O zaman neden cüzdanı yine de özenle yönetiyoruz?" (Alışkanlık; hesap ele geçirilirse kimlik çalınır; aynı kalıp mainnet'te para kaybettirir.)

Faucet çalışmazsa: dur, ekran görüntüsü iste, sayfadaki koşulu birlikte oku; başka kaynak uydurma. Cüzdan sorunu Solidity'yi geciktirmesin: 1. aşamaya (Remix VM, cüzdansız) geç, cüzdanı sonra çöz.

## 0.4 Remix turu (15 dk)

`https://remix.ethereum.org` aç. Amaç: kendi kodumuzdan önce **derle → deploy → çağır** döngüsünü Remix'in kendi örneğiyle görmek. (Kodu sen yazmıyorsun; Remix'in hazır örneği.)

1. Sol menüden **File explorer** → varsayılan çalışma alanındaki Storage örneğini aç (yoksa Remix'in verdiği herhangi bir örnek).
2. **Solidity compiler** → derle. Derleyici sürümünü ve **Advanced Configurations → EVM Version**'ı göster; **cancun** seç (`references/remix-guide.md`; nedeni Stage 4'te).
3. **Deploy & run transactions** → Environment: **Remix VM** → Deploy. "Sahte bir zincir tarayıcının içinde; gerçek AVAX yok, cüzdan yok."
4. Deployed Contracts'ta örneğin fonksiyonlarını çağır; mavi (okuma) ve turuncu (yazma) düğmelerin farkını sor. Terminalde işlem satırını genişlet.
5. Account listesini göster: "Hesabı değiştirmek çağıranı değiştirir. Bunu yetki testlerinde kullanacağız."

**Yoklama:** (1) Mavi düğmeye basınca neden işlem/gas yok, turuncuda var? (2) Sayfayı yenilersek deploy edilen sözleşmeye ne olur?

## 0.5 Canlı zincire ölçerek bak (10 dk) ← dersin kalbi

Sen çalıştırırsın, öğrenci önce **tahmin eder**:

| Tahmin sorusu | Sen çalıştır | Ne öğretir |
|---|---|---|
| "Fuji'nin chain ID'si kaç?" | `python3 scripts/chain.py chain-id` | Ağın kimliği (43113) |
| "Avalanche'ta blok kaç saniyede bir geliyor?" (0.1'deki soru) | `python3 scripts/chain.py block-times 20` | **Gerçek ölçüm**; öğrencinin tahmini ile karşılaştır |
| "Bu adres bir cüzdan mı, kontrat mı?" (`0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf`) | `python3 scripts/chain.py code 0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf` | Kontrat = kodu var (bu: ICM'in Teleporter'ı; Stage 5 sonrası merak edersen) |
| "Bir işlemin maliyeti ne kadar?" | Öğrencinin faucet işlemini explorer'da bul (`https://explorer-test.avax.network/c-chain`), gas ve ücreti birlikte oku | gas × fiyat |

Öğrenci kendi faucet işlemini explorer'da arasın (adresini ya da işlem hash'ini yapıştırarak); arayüz etiketleri değişirse ekran görüntüsü iste. Rakamları `memory.md` "Ölçümler" bölümüne yaz (blok aralığı, ilk işlem ücreti); Stage 4'te karşılaştıracağız.

## Çıkış kriterleri

- [ ] Core kurulu, yeni cüzdan, Testnet Mode açık, C-Chain adresi biliniyor ve bakiye > 0 (`chain.py balance` ile doğrulandı)
- [ ] Öğrenci recovery phrase kuralını kendi cümleleriyle söyledi
- [ ] Remix'te derle → Remix VM'e deploy → fonksiyon çağır döngüsü yapıldı, EVM Version cancun seçildi
- [ ] Blok aralığı ölçüldü ve öğrencinin tahminiyle karşılaştırıldı
- [ ] EOA ile kontrat farkını `code` çıktısıyla açıkladı
- [ ] `memory.md`: Stage 0 ☑, cüzdan adresi, ölçümler, kavram defterine ≥ 3 cümle

**Sonraki:** `references/stages/01-solidity-basics.md`.
