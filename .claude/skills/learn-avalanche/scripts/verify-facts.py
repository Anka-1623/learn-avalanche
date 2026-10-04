#!/usr/bin/env python3
"""live-facts.md'deki "Yeniden doğrula" kontrollerini sırayla koşar. SALT-OKUNUR: anahtar tutmaz, işlem göndermez.

Kullanım:
    python3 scripts/verify-facts.py              # hepsi
    python3 scripts/verify-facts.py --only chain # yalnızca zincir kontrolleri (chain | doc)

Sonuç satırları:
    OK            kontrol beklenen sonucu verdi
    DEĞİŞMİŞ      kaynak yönlendirildi / 404 / beklenen metin yok: bu konudan ÖĞRETME, live-facts.md'yi güncelle
    ERİŞİLEMEDİ   ağ ya da RPC'ye ulaşılamadı (sonuç hakkında bir şey söylemez)

Çıkış kodu: 0 hepsi OK · 1 en az bir DEĞİŞMİŞ · 3 DEĞİŞMİŞ yok ama ERİŞİLEMEDİ var.
Yeni bir "Yeniden doğrula" komutu eklersen CHECKS listesine bir satır ekle.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

OK, CHANGED, UNREACHABLE = "OK", "DEĞİŞMİŞ", "ERİŞİLEMEDİ"

# (ad, tür, betik argümanları, stdout'ta aranacak desen ya da None)
CHECKS = [
    ("Fuji chain ID 43113", "chain", ["chain.py", "chain-id"], r"43113"),
    ("ICM Teleporter hâlâ kontrat (Fuji)", "chain",
     ["chain.py", "code", "0x253b2784c75e510dD0fF1da844684a1aC0aa5fcf"], r"CONTRACT"),
    ("Academy: Core bağlama dersi", "doc",
     ["fetch-doc.py", "/academy/avalanche-l1/avalanche-fundamentals/04-creating-an-l1/02-connect-core"], None),
    ("Academy: test token alma dersi", "doc",
     ["fetch-doc.py", "/academy/avalanche-l1/avalanche-fundamentals/04-creating-an-l1/02a-claim-testnet-tokens"], None),
    ("Remix + Core dokümanı: EVM sürümü uyarısı", "doc",
     ["fetch-doc.py", "/docs/avalanche-l1s/add-utility/deploy-smart-contract", "--grep", "(?i)cancun|pectra"],
     r"(?i)cancun"),
]


def classify(returncode, stdout, stderr, pattern):
    """Bir kontrolün çıktısını OK / DEĞİŞMİŞ / ERİŞİLEMEDİ olarak sınıflar."""
    if returncode == 2:  # fetch-doc.py: site başka bir sayfaya yönlendirdi
        return CHANGED, "yönlendirildi (yol eskimiş)"
    if returncode != 0:
        if "404" in stderr:
            return CHANGED, "404"
        return UNREACHABLE, (stderr.strip().splitlines() or ["hata"])[-1][:120]
    if pattern and (not re.search(pattern, stdout) or "(no match)" in stdout):
        return CHANGED, f"beklenen metin yok: {pattern}"
    return OK, ""


def run(args):
    try:
        p = subprocess.run([sys.executable, os.path.join(HERE, args[0])] + args[1:],
                           capture_output=True, text=True, timeout=45)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "zaman aşımı"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", choices=["chain", "doc"])
    only = ap.parse_args().only

    results = []
    for name, kind, args, pattern in CHECKS:
        if only and kind != only:
            continue
        status, note = classify(*run(args), pattern)
        results.append(status)
        print(f"{status:<12} {name}" + (f"  ({note})" if note else ""))

    changed, unreachable = results.count(CHANGED), results.count(UNREACHABLE)
    print(f"\n{results.count(OK)} OK · {changed} DEĞİŞMİŞ · {unreachable} ERİŞİLEMEDİ")
    if changed:
        return 1
    return 3 if unreachable else 0


if __name__ == "__main__":
    sys.exit(main())
