from mauth import CRYPT_PWD

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Padding for the input data to make sure it's a multiple of 16 bytes
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[: -ord(s[len(s) - 1 :])]


def derive_key(salt: bytes) -> bytes:
    """Derive a 256-bit (32-byte) key from the given password using PBKDF2-HMAC."""
    return hashlib.pbkdf2_hmac("sha256", CRYPT_PWD.encode(), salt, 100000, dklen=32)


def encrypt(plaintext: str) -> str:
    """Encrypt the plaintext using the given password."""
    salt = get_random_bytes(16)
    key = derive_key(salt)
    iv = get_random_bytes(16)  # Initialization vector for AES
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(plaintext).encode())

    # Combine the salt, iv, and encrypted message for storage
    combined = base64.b64encode(salt + iv + encrypted).decode("utf-8")
    return combined


def decrypt(encrypted: str) -> str:
    """Decrypt the encrypted text using the given password."""
    encrypted_data = base64.b64decode(encrypted)
    salt = encrypted_data[:16]  # The first 16 bytes are the salt
    iv = encrypted_data[16:32]  # The next 16 bytes are the initialization vector
    ciphertext = encrypted_data[32:]  # The rest is the ciphertext
    key = derive_key(salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext)).decode("utf-8")
    return plaintext
