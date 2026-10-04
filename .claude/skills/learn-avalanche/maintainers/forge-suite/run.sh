#!/usr/bin/env bash
# Cevap anahtarlarını (../../answer-keys) Foundry ile yeniden doğrular. SKILL KULLANICILARI İÇİN DEĞİL:
# skill'i düzenleyen bakımcılar içindir. Öğrenci yolu Remix'tir; Foundry gerekmez.
#
#   bash maintainers/forge-suite/run.sh            # hepsini çalıştırır
#   OZ_VERSION=5.6.1 bash .../run.sh               # OpenZeppelin sürümünü sabitler (Remix'in çekeceği npm sürümü)
#   FOUNDRY_BIN=/yol/foundry/bin bash .../run.sh   # forge/cast dizinini elle ver
#
# Ne yapar: geçici bir Foundry projesi kurar, OpenZeppelin'i npm'den (Remix'in çözdüğü paketle aynı) alır,
# her aşamanın anahtarını kendi test setine karşı çalıştırır, sonra 4 "mutasyon" dener: bilerek bozulmuş
# kod testlerce YAKALANMALI. Yakalanmıyorsa test zayıftır. Çıkış kodu 0 = hepsi tamam.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
KEYS="$HERE/../../answer-keys"
OZ_VERSION="${OZ_VERSION:-5.6.1}"
fail=0

FB="${FOUNDRY_BIN:-$(bash "$HERE/preflight.sh" 2>/dev/null | sed -n 's/^FOUNDRY_BIN=//p')}"
if [ -z "$FB" ]; then
  echo "Gerçek Foundry bulunamadı. Kur: curl -L https://getfoundry.sh/install | bash  (sonra: foundryup)"
  echo "Not: bazı sistemlerde /usr/bin/forge Foundry değildir; preflight.sh bunu CONFLICT diye bildirir."
  exit 2
fi
export PATH="$FB:$PATH"
echo "Foundry: $(forge --version | head -1)   |   OpenZeppelin (npm): $OZ_VERSION"

W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
( cd "$W" && forge init p --no-git >/dev/null 2>&1 ) || { echo "forge init başarısız"; exit 2; }
P="$W/p"; rm -f "$P/src/Counter.sol" "$P/test/Counter.t.sol" "$P/script/Counter.s.sol"
mkdir -p "$W/oz" && ( cd "$W" && npm pack "@openzeppelin/contracts@$OZ_VERSION" --silent >/dev/null 2>&1 \
  && tar xzf "openzeppelin-contracts-$OZ_VERSION.tgz" -C oz --strip-components=1 ) || { echo "OpenZeppelin $OZ_VERSION alınamadı (npm/ağ?)"; exit 2; }
printf '@openzeppelin/contracts/=%s/oz/\n' "$W" > "$P/remappings.txt"
cp "$HERE/foundry.toml" "$P/foundry.toml"

# $1 = etiket, $2 = beklenen: pass|fail, geri kalan: forge test argümanları
check() {
  local label="$1" expect="$2"; shift 2
  local out; out="$( cd "$P" && forge test "$@" 2>&1 )"; local rc=$?
  local summary; summary="$(echo "$out" | grep -E "tests passed|test suites" | tail -1)"
  if { [ "$expect" = pass ] && [ $rc -eq 0 ]; } || { [ "$expect" = fail ] && [ $rc -ne 0 ]; }; then
    printf "  ok    %-52s %s\n" "$label" "${summary:-}"
  else
    printf "  FAIL  %-52s (beklenen: %s)\n" "$label" "$expect"; echo "$out" | tail -12 | sed 's/^/        /'; fail=1
  fi
}
reset() { rm -f "$P"/src/*.sol "$P"/test/*.sol; }

echo "== Stage 1: BadgeBook v1..v3 (her sürüm kendi testine karşı)"
for n in 1 2 3; do
  reset; cp "$KEYS/stage1/BadgeBook.v$n.sol" "$P/src/BadgeBook.sol"; cp "$HERE/test/BadgeBook.L$n.t.sol" "$P/test/BadgeBook.t.sol"
  check "BadgeBook.v$n  x  L$n testleri" pass
done

echo "== Stage 2: Badge (soulbound ERC-721 + roller)"
reset; cp "$KEYS/stage2/Badge.sol" "$P/src/"; cp "$HERE/test/Badge.t.sol" "$P/test/"
check "Badge  x  Badge.t.sol" pass

echo "== Stage 3: Vault (sömürü + düzeltme + fuzz + invariant)"
reset; cp "$KEYS/stage3/Vault.sol" "$P/src/"; cp "$HERE/test/Attacker.sol" "$HERE/test/Vault.t.sol" "$P/test/"
check "Vault/SafeVault  x  Vault.t.sol" pass

echo "== Sonraki (beta dışı): ICM iskeleti"
reset; cp "$KEYS/next-icm/"*.sol "$P/src/"; cp "$HERE/test/Interchain.t.sol" "$P/test/"
check "BadgeAnnouncer/BadgeMirror  x  Interchain.t.sol" pass

echo "== Mutasyonlar: bozuk kod YAKALANMALI (test kırılırsa 'ok')"
reset; sed 's/external onlyOwner {/external {/' "$KEYS/stage1/BadgeBook.v3.sol" > "$P/src/BadgeBook.sol"; cp "$HERE/test/BadgeBook.L3.t.sol" "$P/test/BadgeBook.t.sol"
check "M1  onlyOwner silindi" fail
reset; grep -v "emit BadgeAwarded" "$KEYS/stage1/BadgeBook.v3.sol" > "$P/src/BadgeBook.sol"; cp "$HERE/test/BadgeBook.L3.t.sol" "$P/test/BadgeBook.t.sol"
check "M2  event yayınlanmıyor" fail
reset; sed 's/if (from != address(0) \&\& to != address(0)) revert Soulbound();//' "$KEYS/stage2/Badge.sol" > "$P/src/Badge.sol"; cp "$HERE/test/Badge.t.sol" "$P/test/"
check "M3  soulbound kontrolü silindi" fail
reset; python3 - "$KEYS/stage3/Vault.sol" "$P/src/Vault.sol" <<'EOF'
import sys
s=open(sys.argv[1]).read(); i=s.index("contract SafeVault"); head,tail=s[:i],s[i:]
tail=tail.replace("withdraw() external nonReentrant","withdraw() external")
tail=tail.replace('balanceOf[msg.sender] = 0; // effect\n        (bool ok,) = msg.sender.call{value: amount}(""); // interaction\n        if (!ok) revert TransferFailed();','(bool ok,) = msg.sender.call{value: amount}("");\n        if (!ok) revert TransferFailed();\n        balanceOf[msg.sender] = 0;')
open(sys.argv[2],"w").write(head+tail)
EOF
cp "$HERE/test/Attacker.sol" "$HERE/test/Vault.t.sol" "$P/test/"
check "M4  SafeVault yeniden savunmasız" fail

echo
if [ $fail -eq 0 ]; then echo "TÜMÜ TAMAM: cevap anahtarları ve testler tutarlı."; else echo "BAŞARISIZ: yukarıdaki FAIL satırlarına bak."; fi
exit $fail
