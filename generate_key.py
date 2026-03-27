#!/usr/bin/env python3
"""
Run this ONCE to generate your ENCRYPTION_KEY.
Store the output in your .env file — never lose it or your wallets are gone.
"""

from cryptography.fernet import Fernet

key = Fernet.generate_key().decode()
print(f"\n✅ Your encryption key (save this somewhere safe):\n")
print(f"ENCRYPTION_KEY={key}\n")
print("Add this to your .env file.\n")