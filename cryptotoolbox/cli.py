"""Small CLI to demo wallet and vesting functions"""
import argparse
import json
import time
from .wallet import Wallet
from .vesting import VestingSchedule

def main():
    p = argparse.ArgumentParser(prog="cryptotoolbox")
    sub = p.add_subparsers(dest="cmd")

    mk = sub.add_parser("create-wallet")
    mk.add_argument("--passphrase", default="")

    derive = sub.add_parser("derive")
    derive.add_argument("seed")
    derive.add_argument("--index", type=int, default=0)

    vest = sub.add_parser("vesting")
    vest.add_argument("--amount", type=float, default=1000.0)
    vest.add_argument("--start", type=int, default=int(time.time()))
    vest.add_argument("--cliff", type=int, default=60*60*24*30)  # 30 days
    vest.add_argument("--duration", type=int, default=60*60*24*365)  # 1 year
    vest.add_argument("--when", type=int, default=int(time.time()))

    args = p.parse_args()

    if args.cmd == "create-wallet":
        w = Wallet()
        print("seed_phrase:", w.seed_phrase)
        print("exported json:")
        print(w.export_json(args.passphrase))
    elif args.cmd == "derive":
        w = Wallet(seed_phrase=args.seed)
        print(w.derive_key(index=args.index))
    elif args.cmd == "vesting":
        s = VestingSchedule(total_amount=args.amount, start_time=args.start, cliff_seconds=args.cliff, duration_seconds=args.duration)
        print(json.dumps({
            "vested": s.vested_at(args.when),
            "locked": s.locked_at(args.when),
            "when": args.when
        }, indent=2))
    else:
        p.print_help()

if __name__ == "__main__":
    main()
