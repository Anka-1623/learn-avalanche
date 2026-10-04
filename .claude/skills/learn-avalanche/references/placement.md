# Seviye tespiti

İçindekiler: Neden · Seviyeler · Akış · Sorular (A, B, C) · Puanlama · Sonucu söyleme · Hafızaya yazma · Yeniden ölçme.

## Neden

Beyan güvenilir bir ölçü değil. Kendini olduğundan ileri görenler Stage 1'i atlayıp üçüncü derste çöker; kendini geri görenler sıkılıp bırakır. 3–6 soruluk bir tanı ikisini de önler. **Beyan başlangıç noktasıdır, ölçü karar verir.** Tanı bir sınav değildir ve sonucu öğrenciye puan olarak söylenmez.

## Seviyeler (hafızadaki değerler)

| Değer | Anlamı | Yönlendirme |
|---|---|---|
| `hiç-kod` | Programlamaya yeni | `references/curriculum.md` → Seviyeye göre yönlendirme |
| `js-python` | Programlama biliyor, Solidity bilmiyor | aynı |
| `solidity-başladı` | Solidity temelini biliyor | aynı |
| `kontrat-yazıyor` | Kontrat yazıyor, güvenlik ve dağıtım bilgisi var | aynı |

## Akış

1. **Beyan:** Onboarding'deki "Deneyim" cevabı → hafızada `Seviye (beyan)`.
2. **Başlangıç kademesi:** `hiç-kod` → tanı yok: ölçülen = `hiç-kod` yaz, `Tanı` satırına "beyan; tanı yapılmadı" notunu düş, 5'e geç (A'yı sormak öğrenciyi küçültür; yanlış beyanı canlı ayar yakalar) · `js-python` → **A** · `solidity-başladı` → **B** · `kontrat-yazıyor` → **C**.
3. **Soruları tek tek sor.** Başlarken söyle: "Bu bir sınav değil; nereden başlayacağımızı görmek için. Bilmiyorsan 'bilmiyorum' de, o da işe yarar bir bilgi." Öğrenci kendi cümleleriyle cevaplar; çoktan seçmeli kullanma. İpucu verme, doğru/yanlış deme; ama robot gibi de durma. Her cevaba kısa, **içerikli** ve **değerlendirmesiz** bir karşılık ver, öğrencinin kendi kullandığı bir kelimeyi geri yansıt ("storage'ı 'kalıcı' diye anlattın, tamam; sıradaki…"), aynı kalıbı üst üste kullanma. Soruları art arda sıralama; her biri tek mesaj, aralarda tek cümlelik bağ. Soruları öğrencinin dilinde sor; kod terimleri İngilizce kalır.
4. **Kademe geçildi mi** (Puanlama): geçildiyse dur. Geçilmediyse bir alt kademeye in (C→B→A) ve onu sor. A de geçilmezse seviye `hiç-kod`. **Toplam en fazla 6 soru** (≈5–8 dk).
5. **Karar:** ölçülen seviye = geçilen en yüksek kademe: A → `js-python`, B → `solidity-başladı`, C → `kontrat-yazıyor`, hiçbiri → `hiç-kod`.
6. **Hafızaya yaz** (aşağıda), sonra sonucu söyle.

## Sorular

Her sorunun altında "yeterli cevap" notu var; kelimesi kelimesine aranmaz, fikir aranır.

### Kademe A: programlama temeli

| Kod | Soru | Yeterli cevap |
|---|---|---|
| A1 | "Bir fonksiyon ne işe yarar? Bildiğin bir dilden küçük bir tanesini sözle anlat." | Girdi alır, iş yapar, çıktı verir; aynı işi tekrar yazmamak için. Somut bir örnek verirse ✓. |
| A2 | "Bir dizi (liste) ile bir sözlük (dict / object / map) arasındaki fark nedir? Hangisini ne zaman seçersin?" | Dizi sıra/numara ile, sözlük anahtar ile erişir; "isimle bulmak" istendiğinde sözlük. |
| A3 | "Kodun hata verdi. Hata mesajını görünce ilk ne yaparsın?" | Mesajı okur, satır numarasına ve ne beklediğine bakar, sorunu küçültüp yeniden dener. "Kopyalayıp aratırım" tek başına ◐. |

### Kademe B: Solidity temeli

| Kod | Soru | Yeterli cevap |
|---|---|---|
| B1 | "Solidity'de `storage`, `memory` ve `calldata` ne demek? Hangisi ne zaman?" | storage: zincirde kalıcı, pahalı · memory: geçici, değiştirilebilir kopya · calldata: dış çağrının salt-okunur girdisi, kopyalanmaz, en ucuz. |
| B2 | "Bir koşul sağlanmayınca işlemi geri çevirmek için `require("mesaj")` ile `revert CustomError()` arasındaki fark nedir?" | Custom error daha ucuz (metin saklanmaz), parametre taşıyabilir; `require` metin taşır, daha pahalı. |
| B3 | "`msg.sender` ile `tx.origin` arasındaki fark nedir? Hangisiyle yetki kontrolü yapmak tehlikeli ve neden?" | msg.sender: doğrudan çağıran (kontrat da olabilir) · tx.origin: işlemi başlatan hesap. tx.origin ile yetki, kullanıcıyı kötü bir kontrata çağrı yaptırıp onun adına işlem yaptırmaya açar (oltalama). |

### Kademe C: kontrat yazan

| Kod | Soru | Yeterli cevap |
|---|---|---|
| C1 | "Bir kasadan para çekerken üç iş var: bakiyeyi kontrol et, parayı gönder, bakiyeyi sıfırla. Hangi sırayla yazarsın, neden?" | Kontrol → sıfırla → gönder. Aksi hâlde alıcı kontrat gönderme sırasında geri girip (reentrancy) aynı bakiyeyi tekrar çekebilir. |
| C2 | "Solidity 0.8'de `unchecked` bloğu ne işe yarar? Ne zaman kullanırsın, ne zaman asla?" | Taşma kontrolünü kapatır (gas kazancı). Yalnızca taşmanın imkânsız olduğu kanıtlanabiliyorsa; kullanıcı girdisi üstünde asla. |
| C3 | "ERC-721'de `_safeMint` ile `_mint` farkı nedir? Güvenlik açısından neden önemli?" | `_safeMint` alıcı bir kontratsa `onERC721Received` çağırır: bu bir **dış çağrıdır** (reentrancy yüzeyi); ama token'ın kilitli kalmasını da önler. |

## Puanlama

✓ = 1, ◐ = 0,5 (doğru fikir, eksik ya da kısmen yanlış ayrıntı), ✗ = 0 ("bilmiyorum" dahil). Bir kademede toplam **≥ 2** ise kademe geçildi. Puanlamayı sessizce yap; öğrenciye sayı söyleme.

## Sonucu söyleme

Sonucu bir **plan** olarak anlat, not olarak değil: nereden başlayacağınız, hangi tempoda, neyi hızlı geçeceğiniz.

- **Ölçülen = beyan:** "Anlattıklarına göre … seviyesindesin; şuradan başlıyoruz: …"
- **Ölçülen < beyan:** yargılama, gerekçeyi iş olarak söyle: "Şu iki konuyu birlikte sağlamlaştırırsak sonraki aşamalar çok daha rahat geçer; hızlı ilerlersen seni yukarı çekerim. İstersen `seviye` ile istediğin zaman yeniden ölçeriz."
- **Ölçülen > beyan:** "Sağlam gidiyorsun; istersen şu aşamayı hızlı geçelim. Kanıtı Remix'te göstereceksin." Atlamayı öğrenciye sor.
- Öğrenci ölçülenden daha yukarıdan başlamak isterse izin ver; `Seviye geçmişi`ne "beyan üstüne geçildi" yaz. Canlı ayar (`references/teaching-method.md`) devrede kalır.
- "Kolay", "basit", "sadece" deme. "Yanlış" deme.
- Hafızadaki değerleri (`hiç-kod`, `js-python`…) öğrenciye etiket olarak söyleme; düz cümleyle anlat ("programlamayı biliyorsun, Solidity'ye yeni başlıyorsun"). Etiket dosyada kalır.

## Hafızaya yaz

Sonucu söylemeden **önce**, `memory.md`'de:

- `Seviye (ölçülen)` ve `Tanı` satırları (tarih, kademe, ✓/◐/✗ dizisi, karar);
- `Tanı sonuçları` tablosuna her soru için bir satır;
- `Seviye geçmişi` tablosuna "tanı" nedenli bir satır;
- yanlış çıkan her kavramı `Zayıf noktalar`a (öğrencinin sözüyle değil, kavram adıyla) ekle.

`Seviye (ölçülen)` dolmadan ders başlamaz. Tanı yarıda kesilirse alan boş kalır; bir sonraki çağrıda Seviye kapısı yeniden çalışır.

## Yeniden ölçme

- `/learn-avalanche seviye`: öğrenci isterse tanıyı baştan yap; eski satırları silme, yenilerini ekle.
- Ders sırasında seviye canlı ayarlanır: `references/teaching-method.md` → Seviyeyi canlı ayarla.
- Stage 3'e girmeden önce, öğrenci atlayarak geldiyse (`stage N`), o aşamanın önkoşul kavramlarından 2 soru sor (örn. Stage 3 için C1 ve B3); ✗ ise bir önceki aşamayı öner.
