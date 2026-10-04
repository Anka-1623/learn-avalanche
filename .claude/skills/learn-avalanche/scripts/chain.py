#!/usr/bin/env python3
"""Read-only Avalanche chain checker for the tutor agent. No dependencies, no keys, no signing.

The learner deploys and sends every transaction from Remix + their own wallet. This tool lets the
tutor verify the RESULT on-chain ("is there code at that address? what does owner() return?")
without ever holding a private key. It cannot send a transaction: there is no code path for it.

Usage:
  chain.py [--network fuji | --rpc URL] <command> [args]

Commands:
  chain-id                         eth_chainId (decimal)
  block                            latest block: number, time, tx count
  block-times [N=10]               measure real block spacing from the last N blocks
  balance ADDR                     native balance in whole tokens
  code ADDR                        is there contract code? (size in bytes)
  call ADDR "sig(in)(out)" [args]  read-only call, cast-style signature; e.g.
                                     call 0xABC... "ownerOf(uint256)(address)" 0
  tx HASH                          receipt: status, block, gas used, contract created
  keccak TEXT                      keccak256 of TEXT; and 4-byte selector if TEXT looks like a signature

Networks: fuji = Avalanche C-Chain testnet (43113). For your own L1 pass its RPC: --rpc https://.../rpc
Supported ABI types for call: address, bool, uintN, bytesN, string, bytes.
"""
import argparse
import json
import re
import sys
import time
import urllib.request

FUJI_RPC = "https://api.avax-test.network/ext/bc/C/rpc"
M64 = 0xFFFFFFFFFFFFFFFF

# ---------------------------------------------------------------- keccak-256 (Ethereum flavour, not SHA3)
_RC = [0x0000000000000001, 0x0000000000008082, 0x800000000000808A, 0x8000000080008000, 0x000000000000808B,
       0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088,
       0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089,
       0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A,
       0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]
_ROT = [[0, 36, 3, 41, 18], [1, 44, 10, 45, 2], [62, 6, 43, 15, 61], [28, 55, 25, 21, 56], [27, 20, 39, 8, 14]]


def _rol(x: int, n: int) -> int:
    n %= 64
    return ((x << n) | (x >> (64 - n))) & M64 if n else x


def _permute(a):
    for rc in _RC:
        c = [a[x][0] ^ a[x][1] ^ a[x][2] ^ a[x][3] ^ a[x][4] for x in range(5)]
        d = [c[(x - 1) % 5] ^ _rol(c[(x + 1) % 5], 1) for x in range(5)]
        a = [[a[x][y] ^ d[x] for y in range(5)] for x in range(5)]
        b = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                b[y][(2 * x + 3 * y) % 5] = _rol(a[x][y], _ROT[x][y])
        a = [[b[x][y] ^ ((~b[(x + 1) % 5][y]) & b[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        a[0][0] ^= rc
    return a


def keccak256(data: bytes) -> bytes:
    rate = 136
    data = bytearray(data) + b"\x01"
    data += b"\x00" * (-len(data) % rate)
    data[-1] |= 0x80
    a = [[0] * 5 for _ in range(5)]
    for off in range(0, len(data), rate):
        for i in range(rate // 8):
            a[i % 5][i // 5] ^= int.from_bytes(data[off + 8 * i: off + 8 * i + 8], "little")
        a = _permute(a)
    return b"".join(a[i % 5][i // 5].to_bytes(8, "little") for i in range(4))


# ---------------------------------------------------------------- minimal ABI
def _split_types(s: str) -> list:
    s = s.strip()
    return [t.strip() for t in s.split(",")] if s else []


def _enc_word(t: str, v: str) -> bytes:
    if t == "address":
        return bytes(12) + bytes.fromhex(v.lower().removeprefix("0x").rjust(40, "0"))
    if t == "bool":
        return (1 if v.lower() in ("1", "true") else 0).to_bytes(32, "big")
    if t.startswith("uint"):
        return int(v, 0).to_bytes(32, "big")
    if re.fullmatch(r"bytes\d+", t):
        raw = bytes.fromhex(v.removeprefix("0x"))
        return raw.ljust(32, b"\x00")
    raise SystemExit(f"unsupported argument type: {t}")


def encode_call(sig: str, args: list) -> str:
    m = re.fullmatch(r"\s*([A-Za-z_]\w*)\(([^)]*)\)(?:\(([^)]*)\))?\s*", sig)
    if not m:
        raise SystemExit(f'bad signature: {sig!r} (expected name(types)(returns))')
    name, ins, _ = m.groups()
    types = _split_types(ins)
    if len(types) != len(args):
        raise SystemExit(f"{name} takes {len(types)} argument(s), got {len(args)}")
    selector = keccak256(f"{name}({','.join(types)})".encode())[:4]
    head, tail = b"", b""
    for t, v in zip(types, args):
        if t in ("string", "bytes"):
            raw = v.encode() if t == "string" else bytes.fromhex(v.removeprefix("0x"))
            head += (32 * len(types) + len(tail)).to_bytes(32, "big")
            tail += len(raw).to_bytes(32, "big") + raw.ljust((len(raw) + 31) // 32 * 32, b"\x00")
        else:
            head += _enc_word(t, v)
    return "0x" + (selector + head + tail).hex()


def checksum(addr_hex: str) -> str:
    """EIP-55 mixed-case address, so it matches what Remix / wallets / explorers display."""
    a = addr_hex.lower().removeprefix("0x")
    h = keccak256(a.encode()).hex()
    return "0x" + "".join(c.upper() if int(h[i], 16) >= 8 else c for i, c in enumerate(a))


def decode_return(sig: str, data_hex: str) -> list:
    m = re.fullmatch(r"\s*[A-Za-z_]\w*\([^)]*\)(?:\(([^)]*)\))?\s*", sig)
    outs = _split_types(m.group(1) or "") if m else []
    data = bytes.fromhex(data_hex.removeprefix("0x"))
    res = []
    for i, t in enumerate(outs):
        w = data[32 * i: 32 * i + 32]
        if t == "address":
            res.append(checksum(w[12:].hex()))
        elif t == "bool":
            res.append(bool(int.from_bytes(w, "big")))
        elif t.startswith("uint"):
            res.append(int.from_bytes(w, "big"))
        elif re.fullmatch(r"bytes\d+", t):
            res.append("0x" + w[: int(t[5:])].hex())
        elif t in ("string", "bytes"):
            off = int.from_bytes(w, "big")
            ln = int.from_bytes(data[off: off + 32], "big")
            raw = data[off + 32: off + 32 + ln]
            res.append(raw.decode("utf-8", "replace") if t == "string" else "0x" + raw.hex())
        else:
            res.append("0x" + w.hex())
    return res


# ---------------------------------------------------------------- JSON-RPC
class Rpc:
    def __init__(self, url: str):
        self.url = url

    def __call__(self, method: str, params=None):
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
        req = urllib.request.Request(self.url, body, {"Content-Type": "application/json", "User-Agent": "learn-avalanche"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.load(r)
        except Exception as e:
            raise SystemExit(f"RPC unreachable ({self.url}): {e}")
        if "error" in out:
            raise SystemExit(f"RPC error from {method}: {out['error']}")
        return out["result"]


def hx(n) -> int:
    return int(n, 16)


def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only Avalanche chain checker (no keys, no signing).")
    ap.add_argument("--network", choices=["fuji"], default="fuji")
    ap.add_argument("--rpc", help="custom RPC URL, e.g. your own L1")
    ap.add_argument("cmd")
    ap.add_argument("args", nargs="*")
    a = ap.parse_args()
    rpc = Rpc(a.rpc or FUJI_RPC)
    label = a.rpc or "fuji"

    if a.cmd == "keccak":
        text = " ".join(a.args)
        print("0x" + keccak256(text.encode()).hex())
        if re.fullmatch(r"[A-Za-z_]\w*\([^)]*\)", text):
            print("selector: 0x" + keccak256(text.encode())[:4].hex())
    elif a.cmd == "chain-id":
        print(hx(rpc("eth_chainId")))
    elif a.cmd == "block":
        b = rpc("eth_getBlockByNumber", ["latest", False])
        print(f"[{label}] block {hx(b['number'])}  time {hx(b['timestamp'])}  txs {len(b['transactions'])}  gasUsed {hx(b['gasUsed'])}")
    elif a.cmd == "block-times":
        n = int(a.args[0]) if a.args else 10
        latest = hx(rpc("eth_blockNumber"))
        blocks = [rpc("eth_getBlockByNumber", [hex(latest - i), False]) for i in range(n)]
        ts = [hx(b["timestamp"]) for b in blocks][::-1]
        deltas = [y - x for x, y in zip(ts, ts[1:])]
        span = ts[-1] - ts[0]
        print(f"[{label}] {n} blocks {latest - n + 1}..{latest}: deltas(s) = {deltas}")
        print(f"[{label}] {n - 1} intervals in {span}s  ->  avg {span / (n - 1):.2f}s per block (timestamps are whole seconds)")
    elif a.cmd == "balance":
        wei = hx(rpc("eth_getBalance", [a.args[0], "latest"]))
        print(f"{wei / 1e18:.6f}  (wei: {wei})")
    elif a.cmd == "code":
        code = rpc("eth_getCode", [a.args[0], "latest"])
        size = (len(code) - 2) // 2
        print(f"[{label}] {a.args[0]}: {'CONTRACT' if size else 'no code (EOA or empty)'}  ({size} bytes)")
        return 0 if size else 3
    elif a.cmd == "call":
        addr, sig, rest = a.args[0], a.args[1], a.args[2:]
        raw = rpc("eth_call", [{"to": addr, "data": encode_call(sig, rest)}, "latest"])
        vals = decode_return(sig, raw)
        print(vals[0] if len(vals) == 1 else vals if vals else raw)
    elif a.cmd == "tx":
        r = rpc("eth_getTransactionReceipt", [a.args[0]])
        if r is None:
            print("not mined yet (or unknown hash)")
            return 4
        print(f"[{label}] status {'SUCCESS' if r['status'] == '0x1' else 'FAILED (reverted)'}  block {hx(r['blockNumber'])}  "
              f"gasUsed {hx(r['gasUsed'])}  from {r['from']}  to {r['to']}  contractCreated {r.get('contractAddress')}  logs {len(r['logs'])}")
        return 0 if r["status"] == "0x1" else 5
    else:
        ap.error(f"unknown command {a.cmd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
