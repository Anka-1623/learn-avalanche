# Avalanche Öğrenme Hafızası

<!-- Bu dosya /learn-avalanche skill'ine aittir; ajan kendiliğinden günceller, öğrencinin "kaydet" demesi gerekmez. -->
<!-- Öğrenci elle de düzenleyebilir; ajan yazmadan önce dosyayı okur ve yalnızca ilgili bölümü günceller. -->
<!-- Gizli bilgi YAZMA: recovery phrase, özel anahtar, parola. Adresler ve işlem hash'leri gizli değildir. -->
<!-- Silme: `/learn-avalanche sıfırla` önce .bak alır. -->

- **Topluluk:** {{Team1 Türkiye | Team1 France | Team1 USA | Diğer}}
- **Dil:** {{öğrencinin dilinin adı, örn. Türkçe}}  <!-- öğrencinin yazdığı dil; topluluktan türetilmez -->
- **Hedef:** {{öğrencinin kendi sözleriyle, boş olabilir}}
- **Seviye (beyan):** {{hiç-kod | js-python | solidity-başladı | kontrat-yazıyor}}
- **Seviye (ölçülen):** {{hiç-kod | js-python | solidity-başladı | kontrat-yazıyor}}  <!-- BOŞSA Seviye kapısı çalışır: ders başlamadan tanı yapılır -->
- **Tanı:** {{YYYY-MM-DD · kademeler ve sonuç, örn. "B ✓◐✓ → solidity-başladı"}}
- **Cüzdan hazır mı:** {{evet | hayır}}
- **Tempo:** {{30 dk | 1–2 saat | bütün oturum}}
- **Başlangıç:** {{YYYY-MM-DD}}
- **Son oturum:** {{YYYY-MM-DD}}
- **Son yazan ajan:** {{Claude Code | Codex | Antigravity | OpenCode | …}}
- **Skill sürümü:** 0.2.0-beta
- **Format sürümü:** 1

## Şimdi

- **Aşama / ders:** {{0 / 0.1}}
- **Durum:** {{başlanmadı | devam | çıkış-kriteri-bekliyor}}
- **Sonraki ilk adım:** {{...}}

## Aşamalar

| # | Aşama | Durum | Bitiş | Not |
|---|---|---|---|---|
| 0 | Hazırlık | ☐ | | |
| 1 | Solidity temelleri | ☐ | | |
| 2 | Kontrat tasarımı | ☐ | | |
| 3 | Güvenlik | ☐ | | |
| 4 | Fuji'ye deploy | ☐ | | |
| 5 | Kendi L1'in + kapanış | ☐ | | |

Durum: ☐ başlanmadı · ◐ devam · ☑ tamam · ⤼ atlandı

## Tanı sonuçları

<!-- Soru kodları references/placement.md'de. ✓ tam · ◐ kısmen · ✗ yok/yanlış/"bilmiyorum". Yeniden ölçmede satır ekle, silme. -->

| Tarih | Soru | Sonuç | Not |
|---|---|---|---|
| | | | |

## Seviye geçmişi

<!-- Her seviye değişikliği bir satır: tanıdan mı, ders sinyalinden mi (references/teaching-method.md → Seviyeyi canlı ayarla). -->

| Tarih | Ölçülen seviye | Neden | Ajan |
|---|---|---|---|
| | | | |

## Kavram defteri (öğrencinin kendi cümleleriyle kanıtladıkları)

<!-- Örn: "reentrancy: para gönderdikten SONRA bakiyeyi sıfırlarsan, alıcı receive() içinden geri girip aynı bakiyeyi tekrar çekebilir." -->

## Zayıf noktalar (bir sonraki oturumda tekrar sorulacak)

<!-- İpucu merdiveninde 3–4. basamak kullanıldıysa ya da öğrenci iki kez yanlış tahmin ettiyse yaz. Tekrar sorusu, dikte olmadan doğru yazılınca sil. -->

## Ölçümler (öğrencinin kendi verileri)

| Ne | Değer | Nerede/nasıl |
|---|---|---|
| Blok aralığı (Fuji) | | `chain.py block-times` |
| İlk faucet işlemi ücreti | | explorer |
| Deploy gas / mint gas | | `chain.py tx` |
| Kesinleşme süresi (kronometre) | | Remix |

## Zincir üstü kayıtlar

| Sözleşme | Ağ | Adres | Deploy tx | Tarih |
|---|---|---|---|---|
| | | | | |

**Cüzdan (C-Chain) adresi:** {{0x… (gizli değil)}}

**L1 bilgileri (Stage 5'te doldurulur):** ad · chain ID · blockchain ID (32 bayt) · RPC · token sembolü · **yönetilen düğüm kapanış tarihi (oluşturma + 3 gün)**

## Fikir kartı (Stage 5 kapanışında öğrenci yazar; fikir yoksa "yok")

<!-- Öğrencinin kendi cümleleriyle, 5 satır: kim için hangi problem · neden zincir üstünde · C-Chain mi L1 mi, neden · en küçük demo · önümüzdeki 7 günde tek adım. Ajan yalnızca sorar, kartı yazmaz. -->

## Oturum günlüğü

<!-- YYYY-MM-DD · ajan — ne yapıldı, ne kanıtlandı, en zor an, sonraki adım. Oturum bitmeden, adım adım eklenir. -->
