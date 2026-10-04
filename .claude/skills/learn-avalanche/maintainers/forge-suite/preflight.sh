#!/usr/bin/env bash
# learn-avalanche preflight — Stage 0 ortam kontrolü. Salt-okunur: hiçbir şey kurmaz/değiştirmez.
#
# Çıktı satırları makine-okunur (ajan için): "<DURUM> <araç> <ayrıntı>"
#   OK        araç var ve doğru
#   MISSING   araç yok
#   CONFLICT  aynı isimde ama FARKLI bir program var (ör. Foundry olmayan bir `forge`)
#   WARN      çalışır ama dikkat
# Sonunda: "FOUNDRY_BIN=<dizin>" (gerçek Foundry'nin bulunduğu yer) ve "SUMMARY ready|not-ready".
#
# Neden CONFLICT kontrolü? Bazı Linux dağıtımlarında /usr/bin/forge başka bir araca aittir.
# `forge --version` "forge Version: X" DEĞİL de hata veriyorsa, öğrenci "forge çalışmıyor"
# sanıp yanlış yere sapar. Burada bunu baştan yakalıyoruz.

FUJI_RPC="https://api.avax-test.network/ext/bc/C/rpc"
ready=1

is_real_foundry() { # $1 = forge yolu
  "$1" --version 2>&1 | head -1 | grep -qE '^forge( Version:| [0-9])'
}

# 1) Gerçek Foundry'yi bul: önce ~/.foundry/bin (foundryup'ın varsayılan yeri), sonra PATH'teki tüm adaylar.
FOUNDRY_BIN=""
candidates=()
[ -x "$HOME/.foundry/bin/forge" ] && candidates+=("$HOME/.foundry/bin/forge")
while IFS= read -r p; do candidates+=("$p"); done < <(type -aP forge 2>/dev/null | awk '!seen[$0]++')

for c in "${candidates[@]}"; do
  if is_real_foundry "$c"; then FOUNDRY_BIN="$(dirname "$c")"; break; fi
done

if [ -n "$FOUNDRY_BIN" ]; then
  ver="$("$FOUNDRY_BIN/forge" --version 2>&1 | head -1)"
  echo "OK forge $ver ($FOUNDRY_BIN/forge)"
  first_on_path="$(command -v forge 2>/dev/null)"
  if [ -n "$first_on_path" ] && [ "$(dirname "$first_on_path")" != "$FOUNDRY_BIN" ]; then
    echo "CONFLICT forge PATH'te ilk sıradaki '$first_on_path' Foundry değil; komutlardan önce: export PATH=\"$FOUNDRY_BIN:\$PATH\""
  fi
  for t in cast anvil; do
    if [ -x "$FOUNDRY_BIN/$t" ]; then echo "OK $t ($("$FOUNDRY_BIN/$t" --version 2>&1 | head -1))"
    else echo "MISSING $t ($FOUNDRY_BIN içinde yok — foundryup çalıştır)"; ready=0; fi
  done
else
  if [ "${#candidates[@]}" -gt 0 ]; then
    echo "CONFLICT forge PATH'te '${candidates[0]}' var ama Foundry değil (--version: $("${candidates[0]}" --version 2>&1 | head -1))"
  else
    echo "MISSING forge"
  fi
  echo "MISSING cast"; echo "MISSING anvil"
  echo "INSTALL curl -L https://getfoundry.sh/install | bash   # sonra yeni terminalde: foundryup"
  ready=0
fi

# 2) Genel araçlar
if command -v git >/dev/null 2>&1; then echo "OK git $(git --version | awk '{print $3}')"; else echo "MISSING git"; ready=0; fi
if command -v python3 >/dev/null 2>&1; then echo "OK python3 (scripts/fetch-doc.py için)"; else echo "WARN python3 yok — canlı doküman çekmek için WebFetch kullan"; fi
if command -v node >/dev/null 2>&1; then echo "OK node $(node --version) (Stage 7 frontend için; şimdilik opsiyonel)"; else echo "WARN node yok (opsiyonel)"; fi

# 3) Git deposu içinde miyiz? forge init'i etkiler.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "WARN cwd zaten bir git deposunun içinde ($(git rev-parse --show-toplevel)) — 'forge init' yerine 'forge init --no-git' kullan, yoksa üst deponun .gitmodules'ü değişir"
fi

# 4) Ağ: Fuji'ye ulaşabiliyor muyuz? (salt-okunur çağrı, anahtar gerekmez)
if [ -n "$FOUNDRY_BIN" ]; then
  cid="$("$FOUNDRY_BIN/cast" chain-id --rpc-url "$FUJI_RPC" 2>/dev/null)"
  if [ "$cid" = "43113" ]; then echo "OK fuji-rpc chain-id=43113"
  else echo "WARN fuji-rpc ulaşılamadı veya beklenmeyen yanıt ('$cid') — internet/proxy kontrol et"; fi
fi

# 5) Anahtar hijyeni: gitignore + env sızıntısı
if [ -f .gitignore ]; then
  grep -qE '^\.env' .gitignore && echo "OK .gitignore .env'yi kapsıyor" || echo "WARN .gitignore .env'yi kapsamıyor — anahtar dosyası commit'lenebilir"
fi
[ -n "${PRIVATE_KEY:-}" ] && echo "WARN ortamda PRIVATE_KEY tanımlı — bu oturumda gerçek/mainnet anahtar kullanma; testnet keystore kullan"

echo "FOUNDRY_BIN=${FOUNDRY_BIN}"
[ "$ready" = 1 ] && echo "SUMMARY ready" || echo "SUMMARY not-ready"
[ "$ready" = 1 ]
