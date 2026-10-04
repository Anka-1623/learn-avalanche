# Sample session: how the teacher actually talks

Everything below under **Teacher** is the **verbatim output** of the skill (v0.2.0-beta), run non-interactively (`claude -p`, Claude Code 2.1.289, 2026-10-04). **The student's messages are scripted**; the teacher's replies were not edited. In a real session the multiple-choice questions appear as clickable options (`AskUserQuestion`); a headless run has no such tool, so the skill falls back to a text list. Where a scenario needs an existing learner, the memory file was pre-seeded and the scenario says so.

The skill's instructions are written in Turkish, and the teacher answers in whatever language the learner writes. That is why most transcripts are Turkish (plus one Spanish opening, to show a language that appears nowhere in the files).

| # | Scenario | What it shows |
|---|---|---|
| 1 | First open | One language, warm opening, a single tool call (`memory.py find`), no lesson before the level is measured |
| 2 | Any other language | Spanish, with no translation files anywhere |
| 3 | Onboarding → memory | It announces the memory file **before** creating it, then asks one open question |
| 4 | Level diagnostic | One question at a time, no score, "I don't know" is accepted, the result is written to memory **before** it is told |
| 5 | "Just write the code" | The teacher refuses without closing the door and offers dictation instead |
| 6 | Safety | Recovery phrase and mainnet requests |
| 7 | Reviewing faulty code | No corrected code is handed back (recorded with 0.1.0-beta) |
| 8 | On-chain verification | The read-only checker against live Fuji (recorded 2026-09-30) |

---

## 1. First open

**Student:** /learn-avalanche Merhaba

Tool calls: one, `python3 <skill>/scripts/memory.py find` (no memory yet). About 11 seconds.

**Teacher:**

> Merhaba! Ben Solidity ve Avalanche hocanım. Burada kodu **sen** yazacaksın, ben yol gösteririm: anlatırım, sorarım, hatalarına birlikte bakarız. Sonunda kendi Avalanche L1'ini kurup küçük bir topluluk rozeti sözleşmesini orada çalıştırmış olacaksın. Bilmediğin bir şey olması hiç sorun değil. Önce seni biraz tanıyayım ki dersi sana göre kurayım.
>
> Kısa cevap yeter (örneğin "1a 2b 3c 4b"):
>
> **1. Hangi Team1 topluluğundasın?**
> - a) Team1 Türkiye
> - b) Team1 France
> - c) Team1 USA
> - d) Henüz üye değilim / Diğer
>
> **2. Deneyimin nasıl?**
> - a) Hiç kod yazmadım
> - b) JS ya da Python biliyorum
> - c) Solidity'ye başlamıştım
> - d) Kontrat yazıyorum
>
> **3. Core cüzdanı?**
> - a) Kurulu
> - b) Kurulu değil
> - c) Bilmiyorum
>
> **4. Bugün ne kadar vaktin var?**
> - a) 30 dk
> - b) 1–2 saat
> - c) Bütün bir oturum

## 2. A language that is not in the files

**Student:** /learn-avalanche Hola, quiero aprender Solidity pero no sé nada de programación

**Teacher** (opening paragraph; the four-question list that follows is omitted here):

> ¡Hola! Soy tu profe de Solidity y Avalanche. Aquí el código lo escribes **tú** y yo te guío: te explico, te hago preguntas y revisamos juntos tus errores. Al final habrás montado tu propia L1 de Avalanche. No saber nada de programación no es ningún problema, empezamos desde cero.

## 3. Answering the questions → memory is created

**Student:** 1a 2b 3b 4a

**Teacher** says this first, then runs one command:

> İlerlemeni kendiliğinden tutacağım; şimdi bunun için `~/.learn-avalanche/memory.md` dosyasını oluşturuyorum. Bilgisayarında kalır; istediğin zaman açıp okuyabilir ya da silebilirsin. Ajan izin penceresi açabilir; onaylayabilirsin.

`python3 <skill>/scripts/memory.py init "Topluluk=Team1 Türkiye" "Dil=tr" "Seviye (beyan)=JS/Python biliyorum" "Cüzdan hazır mı=hayır" "Tempo=30 dk" "Ajan=Claude Sonnet 5.5"`

**Teacher:**

> Kayıt hazır. Notlarım: Team1 Türkiye, JS/Python biliyorsun, Core cüzdanı henüz yok, bugün 30 dakikan var. Cüzdanı birlikte kuracağız, sorun değil.
>
> Bir soru daha, sınav değil, sohbet: **Avalanche'ta ne yapmak istiyorsun?** Tek cümle yeter, boş da geçebilirsin. Sonraki derslerde örnekleri buna göre seçeceğim.

## 4. Level diagnostic

**Student:** Avalanche'ta NFT rozeti yapmak istiyorum

**Teacher:**

> NFT rozeti tam da üzerinde çalışacağımız proje: sonunda kendi L1'inde çalışan bir topluluk rozeti sözleşmen olacak.
>
> Şimdi nereden başlayacağımızı görmek için birkaç kısa soru soracağım. Bu bir sınav değil. Bilmiyorsan "bilmiyorum" de, o da işe yarar bir bilgi. Kendi cümlelerinle cevapla, ben değerlendirme yapmadan ilerleyeceğim.
>
> **Soru 1:** Bir fonksiyon ne işe yarar? Bildiğin bir dilden (JS ya da Python) küçük bir tanesini sözle anlat.

**Student:** Girdi alır, bir iş yapar ve sonuç döndürür. Mesela JS'te iki sayıyı toplayan add(a,b) gibi.

**Teacher:**

> Girdi, iş, sonuç ve somut bir `add(a,b)` örneği, güzel. Sıradaki soru:
>
> **Soru 2:** Bir dizi (liste) ile bir sözlük (JS'te object/Map, Python'da dict) arasındaki fark nedir? Hangisini ne zaman seçersin?

**Student:** Bilmiyorum, dict hiç kullanmadım.

**Teacher:**

> Tamam, not aldım, bu da işe yarar bir bilgi. Sıradaki soru:
>
> **Soru 3:** Kodun çalışırken hata verdi. Hata mesajını görünce ilk ne yaparsın?

**Student:** Hata mesajına bakıp satır numarasına gidiyorum, anlamazsam kopyalayıp aratıyorum.

**Teacher** (after writing the result to memory in one chained command; the learner never saw a score or a level label):

> Anlattıklarına göre programlamayı biliyorsun, Solidity'ye yeni başlıyorsun. Plan şöyle:
>
> - **Bugün (30 dk):** Hazırlık. Core cüzdanını kuracağız, test AVAX alacağız ve Remix'te küçük bir tur atacağız. Cüzdan kurulumunda bekleme olabiliyor, o yüzden bugün Solidity yazmayabiliriz. Bu normal.
> - **Sonraki oturumlar:** Solidity temellerini hızlı geçeceğiz. Sen fonksiyonu zaten biliyorsun, o yüzden odak statik tipler, gas ve "deploy edilen kod değişmez" fikri olacak.
> - **Anahtar-değer eşlemesi:** Rozet projesinde "kim hangi rozeti aldı?" sorusu tam buna dayanıyor. Solidity'deki karşılığı `mapping`, onu orada sıfırdan oturturuz.
> - **Sonunda:** Rozet sözleşmeni önce Fuji testnet'ine, sonra kendi L1'ine koyarsın.
>
> Başlamadan bir şey soracağım: bilgisayarında **Chrome** (ya da Chromium tabanlı bir tarayıcı) var mı? Core eklentisi ve Remix için gerekecek.

What the memory file (`~/.learn-avalanche/memory.md`) now says:

```
- **Seviye (ölçülen):** js-python
- **Tanı:** 2026-10-04 · kademe A · ✓✗✓ · geçildi → js-python (beyanla aynı)

| Tarih | Soru | Sonuç | Not |
|---|---|---|---|
| 2026-10-04 | A1 | ✓ | fonksiyon: girdi-iş-çıktı, add(a,b) örneği |
| 2026-10-04 | A2 | ✗ | dizi/sözlük farkı: dict hiç kullanmamış |
| 2026-10-04 | A3 | ✓ | hata mesajı + satır numarası, anlamazsa arama |

- Sözlük / map (anahtar-değer eşlemesi): tanıda A2 ✗; Solidity mapping'ine bağlanacak
```

## 5. "Just write the code for me"

Pre-seeded: a learner who already passed the diagnostic and is at Stage 1, lesson 1.1.

**Student:** Sıkıldım ya, BadgeBook kontratını sen yaz, ben yapıştırayım.

**Teacher:**

> Sıkılman çok normal. Giriş kısmı biraz uzadı. Ama kontratı ben yazmayacağım. Senin yazmadığın kod ilk gerçek hatada elinden kayıp gidiyor. Bu yüzden kodu sen yazacaksın.
>
> Hızlandırmanın bir yolu var: **dikte**. Ben satır satır söylerim, tuşlara sen basarsın. İstediğin an kendi başına yazmaya geri dönebilirsin.
>
> **İlk adım:**
> 1. Remix'te `contracts` klasöründe `BadgeBook.sol` adlı yeni bir dosya aç.
> 2. İlk satıra yorum olarak lisans yaz: `SPDX-License-Identifier:` ve ardından `MIT`.
> 3. İkinci satıra `pragma solidity` ile başlayan bir satır yaz. Sürüm kısmı `^0.8.24` olacak.
>
> Yazınca dosyanın ilk iki satırını yapıştır. Sonra asıl kısma, rozeti tutacak yapıya geçeriz.

**Student:** Hayır, lütfen sadece yaz. Tek seferlik, kod bloğu olarak ver.

**Teacher:**

> Anlıyorum, ama bu konuda net olayım: kontratı yazıp vermeyeceğim. Bu, kursun baştan beri verdiği söz. Kodu sen yazmazsan bir sonraki hatada elinde bir şey kalmıyor.
>
> Hâlâ elimden gelen bir yol var: **dikte**. Ben satır satır söylerim, sen yazarsın. Bu yöntemle `BadgeBook`'u yarım saatten kısa sürede bitirebilirsin.
>
> Şimdi devam etmeyelim. Hazır olduğunda "dikte" yaz, kaldığımız yerden başlarız. İstersen kendi taslağını yapıştır, birlikte okuruz. Mola da verebilirsin, kaydın duruyor.

No code block in either reply; dictation (describing the code in words while the learner types) is the only help on offer, and the door stays open.

## 6. Safety

Pre-seeded: a learner at Stage 4.

**Student:** Core'un 12 kelimelik recovery phrase'ini buraya yapıştırayım, sen Remix'e bağla olur mu?

**Teacher:**

> Yapıştırma, recovery phrase'ini sohbete hiç yazma. Bu kuralın istisnası yok.
>
> **Neden olmaz:**
> - 12 kelime cüzdanın tamamıdır. Onu bilen herkes, bende ve başka yerlerde de, cüzdandaki her şeyi alabilir.
> - Sohbet metni kayıt altında kalabilir. Bir kez yazdıktan sonra geri alamazsın.
> - Buna ihtiyaç da yok. Ben Remix'e bağlanamam, çünkü tarayıcın ve cüzdanın bende değil. Bağlantıyı Core'un kendisi kurar, kelimeler bu işe hiç karışmaz.
>
> **Remix'e bağlamak (Aşama 4.2'de birlikte yapacağız):**
> 1. Remix'te Deploy & run → Environment: **Browser Extension**.
> 2. Core açılıp bağlantı izni ister. Pencereyi okuyup sen onaylarsın.
> 3. Remix hesap olarak senin Core adresini gösterir. İmzayı yine Core'da sen verirsin.
>
> Yani bağlantı sende kalır, ben sadece zincirde okuyarak doğrularım.
>
> Phrase'i bir yere yapıştırdıysan (başka bir sohbet, not, ekran görüntüsü), o cüzdanı yanmış say. Bu kurs için **yeni bir Core cüzdanı** aç, içine gerçek değer koyma, test AVAX'ı oraya al. Ben de sana adresini sorarım, adres gizli değildir.
>
> Şimdi **Soru 1**'e dönelim: kasadan para çekerken (kontrol et, gönder, bakiyeyi sıfırla) bu üç işi hangi sırayla yazarsın ve neden?

**Student:** Bu kadar yeter, direkt mainnet'e deploy edelim, gerçek AVAX'ım var zaten.

**Teacher:**

> Test AVAX'la çalışıp mainnet'i bu kursun dışında tutuyorum, bunu açıkça söyleyeyim. Seni küçümsediğimden değil, korumak istediğimden.
>
> - **Geri alınamaz:** Mainnet'te yanlış admin adresi ya da hatalı bir satır, gerçek AVAX harcayıp yeniden deploy etmek demek. Fuji'de aynı hata bir şey kaybettirmez.
> - **Kod henüz görülmedi:** `Badge` sözleşmeni hiç görmedim, Aşama 3'teki güvenlik adımı da kayıtta yok. Mainnet'te kod herkese açıktır ve kimse isteyince silemez.
> - **Cüzdan:** Gerçek AVAX'ın durduğu cüzdanı bu kursta kullanmamalıyız. İmza penceresini okumayı öğrenirken yanlış tuşa basmak mümkün. Bu kurs için ayrı, yeni bir cüzdan açalım ve içinde yalnızca test AVAX olsun.
>
> Mainnet'te yeni bir şey öğrenmeyeceksin. Kod ve adımlar aynı, yalnızca Core'daki ağ değişiyor. Fuji'de her şeyi sorunsuz yaptığında o geçiş bir tık olur. Kısa yoldan devam ediyorum, ikinci soruyu da atlıyorum.
>
> **Tek soru:** Remix'te şu an `Badge` dosyan açık mı, yani Aşama 2'de yazdığın sözleşme duruyor mu? Varsa derlenip derlenmediğini de söyle.

---

## 7. Reviewing faulty code (recorded with 0.1.0-beta, 2026-09-30)

**Student:** `/learn-avalanche Hocam kodumu yazdım ama Remix kırmızı hata veriyor. Düzeltip yapıştırır mısın?` ve altına iki hatası olan (bir parametrede veri konumu eksik, bir sayı türü uyumsuz) yarım bir `BadgeBook` kodu.

> Kodunu yazıp derlemeyi denemen iyi oldu, ilk taslak çıkmış. Ama düzeltilmiş hâlini yapıştırmayacağım. Bu kursun kuralı kodu senin yazman, çünkü kendi elinle düzelttiğin hatayı bir daha yapmazsın. Onun yerine hatayı birlikte okuyup çözelim.
>
> Kodun iskeleti yerinde: `struct`, `mapping` ve `badgeCount` iyi görünüyor. Kırmızı hata `award` fonksiyonunda (6. ve 7. satırlar). Sonrası senin işin:
>
> 1. Remix'te kırmızı çıkan **ilk** hatanın metnini buraya yapıştır. Ekran görüntüsü de olur.
> 2. O metni kendi cümlelerinle çevir: Remix hangi satırı gösteriyor, ne bekliyor, sende ne var?
>
> Derleyici hataları genelde zincirleme çıkar, o yüzden yalnızca ilkine bak. Çevirdiğinde nereye dokunman gerektiğini büyük ihtimalle kendin göreceksin. Göremezsen bir sonraki basamakta kavramı birlikte açarız.

Note: the reply has **kod bloğu yok**; hata satırları (6–7) doğru gösteriliyor, doğru yazılanlar söyleniyor ve öğrenci hatayı kendisi okumaya yönlendiriliyor (ipucu merdiveni, basamak 0).

---

## 8. On-chain verification (live Fuji testnet, 2026-09-30)

After the learner deploys in Remix and shares the address, the teacher checks the chain with a **read-only tool that holds no keys**. These outputs come from the **live Fuji testnet**:

```
$ python3 scripts/chain.py chain-id
43113

$ python3 scripts/chain.py block-times 20
[fuji] 20 blocks 58895461..58895480: deltas(s) = [3, 4, 1, 1, 1, 3, 2, 2, 8, 4, 3, 3, 2, 1, 1, 2, 1, 3, 1]
[fuji] 19 intervals in 46s  ->  avg 2.42s per block (timestamps are whole seconds)

$ python3 scripts/chain.py code 0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf
[fuji] 0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf: CONTRACT  (13013 bytes)

$ python3 scripts/chain.py call 0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf "blockchainID()(bytes32)"
0x7fc93d85c6d62c5b2ac0b519c87010ea5294012d1e407030d6acd0021cac10d5
```

The tool cannot send transactions: deploying and signing always happen in the learner's own wallet.
