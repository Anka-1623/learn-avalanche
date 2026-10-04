# Security

## What this project does and doesn't do

- The skill works with **testnet only** (Remix VM, Fuji, the student's own L1); there is no mainnet.
- The skill never asks for or stores any key, recovery phrase or password. These are not written to the memory file (`~/.learn-avalanche/memory.md`).
- `scripts/chain.py` is **read-only**: it doesn't sign and doesn't send transactions.

## Reporting a problem

If you find any of the following, **don't open a public issue**:

- a flow where the skill asks for, or writes to memory, a key or recovery phrase,
- anything in the scripts (`scripts/`) that sends transactions, sends data elsewhere, or runs unexpected commands,
- a secret accidentally left in the repo.

Instead, use **Security → Report a vulnerability** (private security advisory) on this repository. If that option isn't visible, send the repository owner a private message through their GitHub profile.

This is a beta educational tool; no response time is guaranteed, but security reports take priority.
