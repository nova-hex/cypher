# cryptotoolbox

Small, original Python package (educational) with:
- Wallet demo utilities (deterministic demo keys)
- Vesting schedule simulator
- CLI interface

**Not production-ready for real funds.** Use for learning and prototyping.

Usage:
```bash
python -m cryptotoolbox.cli create-wallet
python -m cryptotoolbox.cli derive "<seed phrase>" --index 1
python -m cryptotoolbox.cli vesting --amount 10000
