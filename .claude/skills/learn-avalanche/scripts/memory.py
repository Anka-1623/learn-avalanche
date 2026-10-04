#!/usr/bin/env python3
"""learn-avalanche hafıza dosyası (memory.md) için tek-komut yardımcı. Yalnızca standart kütüphane.

Amaç: ajanın hafızayı aramak, okumak ve güncellemek için art arda araç çağırmasını önlemek
(her çağrı yavaş modellerde saniyeler/dakikalar tutar). Her komut TEK çağrıdır ve dosyayı kendisi okuyup yazar.

  find                            hafızayı ara, bulursa içeriğini yazdır
  init K=V [K=V ...]              şablondan yeni hafıza oluştur (Topluluk, Dil, Seviye (beyan), Cüzdan hazır mı, Tempo, Hedef, Ajan)
  set  K=V [K=V ...]              üst bilgi alanlarını güncelle (Seviye (ölçülen), Tanı, Son yazan ajan...)
  append "<bölüm>" "<satır>"      bir bölümün sonuna satır ekle (tablo ise satır olarak, değilse madde olarak)
                                  bölüm = başlığın başı: "Kavram defteri", "Zayıf noktalar", "Oturum günlüğü",
                                  "Tanı sonuçları", "Seviye geçmişi", "Zincir üstü kayıtlar", "Ölçümler", "Fikir kartı"
  path                            yalnızca konumu yazdır

Konum: $LEARN_AVALANCHE_HOME verilmişse YALNIZCA $LEARN_AVALANCHE_HOME/memory.md (başka klasöre düşmez);
verilmemişse ~/.learn-avalanche/memory.md -> ./.learn-avalanche/memory.md (ilk bulunan / ilk yazılabilir)
Her yazmada `Son oturum` bugüne, `Son yazan ajan` AJAN ortam değişkeni ya da --agent değerine ayarlanır.
Gizli bilgi (recovery phrase, özel anahtar, parola) YAZMA: bu betik içeriği denetlemez, kural ajandadır.
"""
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "memory.template.md")


def candidates():
    # LEARN_AVALANCHE_HOME açıkça verilmişse TEK konumdur: boşsa "hafıza yok" demektir, başka
    # klasördeki hafızaya düşmez (aksi halde ikinci bir öğrenci/demo ilkinin hafızasını sürdürür).
    env = os.environ.get("LEARN_AVALANCHE_HOME")
    if env:
        return [os.path.join(os.path.expanduser(env), "memory.md")]
    return [
        os.path.join(os.path.expanduser("~"), ".learn-avalanche", "memory.md"),
        os.path.join(os.getcwd(), ".learn-avalanche", "memory.md"),
    ]


def legacy_candidates():
    env = os.environ.get("LEARN_AVALANCHE_HOME")
    if env:
        return [os.path.join(os.path.expanduser(env), "progress.md")]
    return [
        os.path.join(os.getcwd(), ".learn-avalanche", "progress.md"),
        os.path.join(os.getcwd(), "avalanche-lab", ".learn-avalanche", "progress.md"),
        os.path.join(os.path.expanduser("~"), ".learn-avalanche", "progress.md"),
    ]


def existing():
    for p in candidates():
        if os.path.isfile(p):
            return p
    return None


def writable_target():
    for p in candidates():
        d = os.path.dirname(p)
        try:
            os.makedirs(d, exist_ok=True)
            probe = os.path.join(d, ".w")
            with open(probe, "w") as f:
                f.write("")
            os.remove(probe)
            return p
        except OSError:
            continue
    return None


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def write(p, s):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(s)
    os.replace(tmp, p)


def parse_kv(args):
    kv = {}
    for a in args:
        if "=" not in a:
            sys.exit(f"HATA: 'Alan=değer' biçimi bekleniyordu: {a!r}")
        k, v = a.split("=", 1)
        kv[k.strip()] = v.strip()
    return kv


def set_field(text, key, value):
    # "- **Alan:** değer  <!-- yorum -->" -> yalnızca değeri değiştir, yorumu koru
    pat = re.compile(r"^(- \*\*" + re.escape(key) + r":\*\* )(.*?)(\s+<!--.*-->)?\s*$", re.M)
    if not pat.search(text):
        return text, False
    return pat.sub(lambda m: m.group(1) + value + (m.group(3) or ""), text, count=1), True


def touch(text, agent):
    text, _ = set_field(text, "Son oturum", datetime.date.today().isoformat())
    if agent:
        text, _ = set_field(text, "Son yazan ajan", agent)
    return text


def last_writer(text):
    m = re.search(r"^- \*\*Son yazan ajan:\*\* (.*?)(\s+<!--.*-->)?\s*$", text, re.M)
    return m.group(1).strip() if m else ""


def agent_name(kv):
    return kv.pop("Ajan", None) or os.environ.get("AJAN") or ""


def cmd_find():
    p = existing()
    if p:
        print(f"FOUND {p}\n")
        print(read(p))
        return 0
    for lp in legacy_candidates():
        if os.path.isfile(lp):
            print(f"LEGACY {lp}\n")
            print(read(lp))
            print("\n(Eski sürüm dosyası: içeriği memory.md'ye taşı, 'Seviye (ölçülen)' boş kalsın, eskiyi progress.md.migrated yap.)")
            return 0
    t = writable_target()
    print(f"NONE {t or '(yazılabilir konum yok: hafıza bloğu yedeğine geç)'}")
    return 0


def cmd_init(args):
    if existing():
        print(f"VAR {existing()} (init atlandı; güncellemek için 'set' kullan)")
        return 0
    kv = parse_kv(args)
    agent = agent_name(kv)
    target = writable_target()
    if not target:
        print("HATA: yazılabilir konum yok; hafıza bloğu yedeğine geç")
        return 1
    text = read(TEMPLATE)
    today = datetime.date.today().isoformat()
    kv.setdefault("Başlangıç", today)
    for k, v in kv.items():
        text, ok = set_field(text, k, v)
        if not ok:
            print(f"UYARI: alan bulunamadı: {k}", file=sys.stderr)
    text = touch(text, agent)
    write(target, text)
    print(f"OLUŞTU {target}")
    return 0


def cmd_set(args):
    p = existing()
    if not p:
        print("HATA: hafıza yok; önce 'init'")
        return 1
    kv = parse_kv(args)
    agent = agent_name(kv)
    text = read(p)
    for k, v in kv.items():
        text, ok = set_field(text, k, v)
        if not ok:
            print(f"UYARI: alan bulunamadı: {k}", file=sys.stderr)
    write(p, touch(text, agent))
    print(f"GÜNCELLENDİ {p}")
    return 0


def cmd_append(args):
    if len(args) < 2:
        sys.exit('Kullanım: memory.py append "<bölüm>" "<satır>" [--agent ad]')
    section, line = args[0], args[1]
    agent = ""
    if "--agent" in args:
        agent = args[args.index("--agent") + 1]
    agent = agent or os.environ.get("AJAN") or ""
    p = existing()
    if not p:
        print("HATA: hafıza yok; önce 'init'")
        return 1
    lines = read(p).split("\n")
    start = None
    for i, l in enumerate(lines):
        if l.startswith("## ") and l[3:].strip().lower().startswith(section.strip().lower()):
            start = i
            break
    if start is None:
        print(f"HATA: bölüm bulunamadı: {section}")
        return 1
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    body = range(start + 1, end)
    table_rows = [i for i in body if lines[i].startswith("|")]
    if table_rows and not line.startswith("|"):
        # eksik sütunları tamamla (ajan sık sık son "Ajan" sütununu atlıyor); "Ajan" sütununa yazan ajanı koy
        head = [c.strip() for c in lines[table_rows[0]].strip().strip("|").split("|")]
        cells = [c.strip() for c in line.split("|")]
        who = agent or last_writer("\n".join(lines))
        while len(cells) < len(head):
            cells.append(who if head[len(cells)].lower() == "ajan" else "")
        new = "| " + " | ".join(cells) + " |"
    else:
        new = line
    if table_rows:
        # tabloya satır olarak ekle; boş yer-tutucu satırı (| | | |) ilk eklemede değiştir
        last = table_rows[-1]
        if re.fullmatch(r"\|(\s*\|)+", lines[last].strip()):
            lines[last] = new
        else:
            lines.insert(last + 1, new)
    else:
        i = end - 1
        while i > start and lines[i].strip() == "":
            i -= 1
        lines.insert(i + 1, line if line.startswith("- ") else "- " + line)
    write(p, touch("\n".join(lines), agent))
    print(f"EKLENDİ [{section}] {p}")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "find":
        return cmd_find()
    if cmd == "init":
        return cmd_init(args)
    if cmd == "set":
        return cmd_set(args)
    if cmd == "append":
        return cmd_append(args)
    if cmd == "path":
        print(existing() or "")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
