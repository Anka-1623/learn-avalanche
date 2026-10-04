# Topluluklar: örneklere ve kapanışa göre yol

Öğrenci Onboarding'de hangi Team1 topluluğuna katıldığını (ya da katılmayı düşündüğünü) söyler. Bu dosya, o cevaba göre **neyin değiştiğini** tanımlar. Buradaki tablo bakımcının düzenleyeceği tek yerdir: yeni bir topluluk eklemek için bir satır yeterli.

## Ne değişir, ne değişmez

| | Değişir (topluluğa göre) | Değişmez |
|---|---|---|
| Öğretim dili | — (öğrencinin yazdığı dil; topluluktan **türetilmez**) | Müfredat, aşamalar, kabul kriterleri |
| Örnek adlar | Rozet adı, sembol, örnek rozet isimleri | Kontratın yapısı ve fonksiyon adları (kabul tabloları buna bağlı) |
| Kapanış | Paylaşım önerisi, hangi kitleye sunulacağı | Doğrulama, güvenlik kuralları |

**Fonksiyon adları hiçbir zaman çevrilmez** (`award`, `badgeCount`, `owner`…): kabul tabloları ve doğrulama araçları bu adlara bağlıdır. Çevrilen şey **açıklamalar** ve **rozetin insana görünen adıdır** (`ERC721` constructor'ındaki ad/sembol ve örnek rozet isimleri).

## Topluluk tablosu

Tablo **tek kaynak dilde** tutulur; öğrencinin diline çeviri çalışma anında senin işindir (dil başına satır, sütun ya da örnek **yok**). Ad ve örnek isimleri öğrencinin diline uyarla ("Workshop" → Türkçe öğrenciyle "Atölye", Fransızcayla "Atelier"); sembol dil taşımaz, olduğu gibi kalır.

| Seçenek | Rozet adı önerisi (ERC-721 adı / sembol) | Örnek rozet isimleri (`award` içinde) |
|---|---|---|
| **Team1 Türkiye** | `Team1 Türkiye Badge` / `T1TR` | Workshop, Hackathon, Meetup |
| **Team1 France** | `Team1 France Badge` / `T1FR` | Workshop, Hackathon, Meetup |
| **Team1 USA** | `Team1 USA Badge` / `T1US` | Workshop, Hackathon, Meetup |
| **Henüz üye değilim / Other** | `Community Badge` / `BADGE` | Workshop, Hackathon, Meetup |

Not: "Team1 USA" seçeneği, bakımcının "USD" dediği topluluk olarak yorumlandı (README → Varsayımlar). "Diğer" seçeneği, listede olmayan bir topluluğa ya da henüz üye olmayanlara açıktır.

Öneri, **öneridir**: öğrenci kendi ad/sembolünü seçebilir. Rozet adını **öğrenci yazar**; sen sadece "topluluğunun adını taşısın istersen" diye önerirsin.

## Açılış cümleleri

Açılış mesajının sesi `SKILL.md` → Onboarding'deki tek örnektir; onu öğrencinin diline sen çevirirsin, dil başına ayrı örnek tutulmaz.

## Kapanış: topluluğa göre

Stage 5'in sonunda (`references/stages/05-own-l1.md` → Kapanış) öğrencinin elinde çalışan bir L1, bir sözleşme adresi ve kendi yazdığı kod olur. Ona sor: **"Bunu topluluğunda kime, nasıl göstereceksin?"** Sonra:

1. Öğrenci 3–4 cümlelik bir paylaşım metnini **kendisi** yazar (ne yaptı, ne öğrendi, hangi sayıyı ölçtü); sen sadece dil ve netlik için soru sorarsın, metni yazmazsın.
2. Paylaşım yeri: kendi topluluğunun kanalı. **Kanal bağlantısı verme**; bakımcı doğrulamadığı sürece uydurma. "Topluluğunun kendi duyuru/sohbet kanalı" de ve öğrenciye sor.
3. Team1 Network'ün genel kaynakları (arama ile doğrulandı, 2026-09-30): `https://team1.network` (katılım/başvuru bilgisi), `https://x.com/AvaxTeam1`, `https://www.team1.blog`, `https://github.com/AvalancheTeam1`.
4. Team1 görev panosu (`go.team1.network`): 2026-08-30 tarihli bir notta "Developer" kategorisi ("bir proje inşa et", "GitHub PR") vardı. Öğrenci sorarsa **"panoyu ve kategori adını kendin kontrol et, değişmiş olabilir"** de; bir görevin ödülünü, koşulunu ya da teslim yöntemini uydurma.

## Bakımcı notu

- Topluluğa özel bir ödev, bağlantı ya da kural eklemek istiyorsan (ör. "France'a katılanlar şu formu doldurur") bu dosyaya, ilgili topluluk satırının altına yaz. Yalnızca doğrulanmış olanı yaz; doğrulanmamış bağlantı öğrenciye yanlış yol gösterir.
- Yeni bir topluluk eklemek için tabloya satır yeter. Dil için bir şey eklemek gerekmez: ajan öğrencinin yazdığı dilde konuşur (hangi dil olursa); müfredat dosyalarını ya da bu tabloyu çevirmek gerekmez.
