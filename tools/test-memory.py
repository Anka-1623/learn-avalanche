#!/usr/bin/env python3
"""scripts/memory.py regresyon testi. Yalnızca standart kütüphane; gerçek ~/.learn-avalanche'a dokunmaz.

Koşu:  python3 tools/test-memory.py
"""
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join(HERE, "..", ".claude", "skills", "learn-avalanche", "scripts", "memory.py")


def slurp(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def run(args, home, cwd, env_home=None):
    env = {k: v for k, v in os.environ.items() if k not in ("LEARN_AVALANCHE_HOME", "AJAN")}
    env["HOME"] = home
    if env_home:
        env["LEARN_AVALANCHE_HOME"] = env_home
    r = subprocess.run([sys.executable, MP, *args], cwd=cwd, env=env, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        self.cwd = os.path.join(self.tmp.name, "cwd")
        os.makedirs(self.home)
        os.makedirs(self.cwd)

    def tearDown(self):
        self.tmp.cleanup()

    def mem(self):
        return os.path.join(self.home, ".learn-avalanche", "memory.md")

    def test_find_none_then_init_find(self):
        rc, out, _ = run(["find"], self.home, self.cwd)
        self.assertTrue(out.startswith("NONE "), out)
        rc, out, _ = run(["init", "Topluluk=Team1 Türkiye", "Dil=tr", "Ajan=t"], self.home, self.cwd)
        self.assertTrue(out.startswith("OLUŞTU "), out)
        rc, out, _ = run(["find"], self.home, self.cwd)
        self.assertTrue(out.startswith("FOUND "), out)
        self.assertIn("Team1 Türkiye", out)

    def test_init_twice_is_skipped(self):
        run(["init", "Topluluk=A"], self.home, self.cwd)
        rc, out, _ = run(["init", "Topluluk=B"], self.home, self.cwd)
        self.assertTrue(out.startswith("VAR "), out)
        self.assertIn("**Topluluk:** A", slurp(self.mem()))

    def test_env_home_is_exclusive(self):
        # hata: LEARN_AVALANCHE_HOME boşken ev klasöründeki hafızaya düşüyordu (demo/ikinci öğrenci ilkini sürdürürdü)
        run(["init", "Topluluk=Team1 Türkiye", "Dil=tr"], self.home, self.cwd)
        other = os.path.join(self.tmp.name, "fr")
        rc, out, _ = run(["find"], self.home, self.cwd, env_home=other)
        self.assertTrue(out.startswith("NONE "), out)
        self.assertIn(other, out)
        rc, out, _ = run(["init", "Topluluk=Team1 France", "Dil=fr"], self.home, self.cwd, env_home=other)
        self.assertTrue(out.startswith("OLUŞTU "), out)
        self.assertIn("**Topluluk:** Team1 France", slurp(os.path.join(other, "memory.md")))
        self.assertIn("**Topluluk:** Team1 Türkiye", slurp(self.mem()))

    def test_set_and_append(self):
        run(["init", "Topluluk=X", "Ajan=claude"], self.home, self.cwd)
        run(["set", "Seviye (ölçülen)=js-python", "Hedef=NFT rozeti"], self.home, self.cwd)
        run(["append", "Tanı sonuçları", "2026-10-04 | A1 | ✓ | not"], self.home, self.cwd)
        run(["append", "Tanı sonuçları", "2026-10-04 | A2 | ✗ | not"], self.home, self.cwd)
        run(["append", "Zayıf noktalar", "mapping vs array karışıyor"], self.home, self.cwd)
        t = slurp(self.mem())
        self.assertIn("**Seviye (ölçülen):** js-python", t)
        self.assertIn("**Hedef:** NFT rozeti", t)
        self.assertIn("**Son yazan ajan:** claude", t)
        self.assertIn("| 2026-10-04 | A1 | ✓ | not |", t)
        self.assertLess(t.index("| A1 |"), t.index("| A2 |"))
        self.assertIn("- mapping vs array karışıyor", t)
        self.assertNotRegex(t, r"(?m)^\|\s*\|\s*\|\s*\|\s*\|\s*$\n\|\s*2026")  # boş yer-tutucu satır kalmamalı

    def test_append_pads_missing_agent_column(self):
        run(["init", "Topluluk=X", "Ajan=Codex"], self.home, self.cwd)
        run(["append", "Seviye geçmişi", "2026-10-04 | js-python | tanı"], self.home, self.cwd)
        run(["append", "Seviye geçmişi", "2026-10-05 | hiç-kod | canlı ayar", "--agent", "Claude"], self.home, self.cwd)
        t = slurp(self.mem())
        self.assertIn("| 2026-10-04 | js-python | tanı | Codex |", t)
        self.assertIn("| 2026-10-05 | hiç-kod | canlı ayar | Claude |", t)

    def test_set_updates_simdi_fields(self):
        run(["init", "Topluluk=X"], self.home, self.cwd)
        run(["set", "Aşama / ders=1 / 1.1", "Durum=devam", "Sonraki ilk adım=struct"], self.home, self.cwd)
        t = slurp(self.mem())
        self.assertIn("**Aşama / ders:** 1 / 1.1", t)
        self.assertIn("**Durum:** devam", t)
        self.assertNotIn("{{0 / 0.1}}", t)

    def test_append_unknown_section_fails(self):
        run(["init", "Topluluk=X"], self.home, self.cwd)
        rc, out, _ = run(["append", "Olmayan bölüm", "x"], self.home, self.cwd)
        self.assertEqual(rc, 1)

    def test_falls_back_to_cwd_when_home_unwritable(self):
        rc, out, _ = run(["init", "Topluluk=X"], "/proc/nonexistent-home", self.cwd)
        self.assertTrue(out.startswith("OLUŞTU "), out)
        self.assertTrue(os.path.isfile(os.path.join(self.cwd, ".learn-avalanche", "memory.md")))

    def test_legacy_progress_detected(self):
        d = os.path.join(self.cwd, ".learn-avalanche")
        os.makedirs(d)
        with open(os.path.join(d, "progress.md"), "w", encoding="utf-8") as f:
            f.write("# eski\n")
        rc, out, _ = run(["find"], self.home, self.cwd)
        self.assertTrue(out.startswith("LEGACY "), out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
