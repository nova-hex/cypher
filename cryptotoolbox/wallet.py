"""
Simple educational wallet utilities.
NOT a production-grade wallet. Uses standard Python libs for deterministic demo keys.
"""

import os
import json
import hashlib
import hmac
import secrets
from typing import Dict

def _pbkdf2(seed_phrase: str, salt: str, iterations: int = 2048, dklen: int = 32) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", seed_phrase.encode("utf-8"), salt.encode("utf-8"), iterations, dklen)

class Wallet:
    """
    Minimal deterministic wallet for demo/educational use.
    - Create wallet with mnemonic-like phrase (random if not provided)
    - Derive deterministic key material for account indexes
    - Export / import JSON (encrypted with a passphrase using simple HMAC-based integrity)
    """

    def __init__(self, seed_phrase: str = None):
        if seed_phrase is None:
            # generate a human-friendly pseudo-mnemonic (not BIP39)
            seed_phrase = " ".join(secrets.choice(_WORDLIST()) for _ in range(12))
        self.seed_phrase = seed_phrase

    def derive_key(self, index: int = 0) -> Dict[str, str]:
        """
        Derive deterministic key bytes for index -> return hex private/public stub.
        This is a deterministic construction for demos only.
        """
        salt = f"cryptotoolbox:{index}"
        key = _pbkdf2(self.seed_phrase, salt, iterations=4096, dklen=32)
        priv = key.hex()
        # make a simple "address" by hashing the public-like data
        addr = hashlib.sha256(key + b"addr").hexdigest()[:40]
        return {"index": index, "private_key": priv, "address": addr}

    def export_json(self, passphrase: str = "") -> str:
        """
        Export wallet JSON with an HMAC for integrity. Not encryption — passphrase is used for HMAC.
        """
        payload = {"seed_phrase": self.seed_phrase}
        payload_json = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        mac = hmac.new(passphrase.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256).hexdigest()
        wrapper = {"payload": payload, "mac": mac}
        return json.dumps(wrapper, indent=2)

    @staticmethod
    def import_json(json_text: str, passphrase: str = "") -> "Wallet":
        wrapper = json.loads(json_text)
        payload_json = json.dumps(wrapper["payload"], separators=(",", ":"), sort_keys=True)
        mac = hmac.new(passphrase.encode("utf-8"), payload_json.encode("utf-8"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(mac, wrapper.get("mac", "")):
            raise ValueError("MAC check failed — wrong passphrase or corrupted file")
        return Wallet(seed_phrase=wrapper["payload"]["seed_phrase"])

def _WORDLIST():
    # small safe wordlist for demo uniqueness — you can replace with a full list
    return [
        "alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel","india","juliet",
        "kilo","lima","mike","november","oscar","papa","quebec","romeo","sierra","tango",
        "uniform","victor","whiskey","xray","yankee","zulu"
                                                  ]
