import os
import base64
import hashlib

import nacl.secret
import nacl.pwhash
from Crypto.Cipher import AES

# --- Constants for file decryption (rclone crypt file format) ---
FILE_MAGIC = b'RCLONE\x00\x00'
FILE_MAGIC_SIZE = 8
FILE_NONCE_SIZE = 24
BLOCK_HEADER_SIZE = nacl.secret.SecretBox.MACBYTES
BLOCK_DATA_SIZE = 64 * 1024
BLOCK_SIZE = BLOCK_HEADER_SIZE + BLOCK_DATA_SIZE

# --- Default salt (rclone crypt default) ---
DEFAULT_SALT = bytes([
    0xA8, 0x0D, 0xF4, 0x3A, 0x8F, 0xBD, 0x03, 0x08,
    0xA7, 0xCA, 0xB8, 0x3E, 0x58, 0x1F, 0x86, 0xB1
])

# --- For deobscuring crypt remote credentials ---
CRYPT_KEY = bytes([
    0x9c, 0x93, 0x5b, 0x48, 0x73, 0x0a, 0x55, 0x4d,
    0x6b, 0xfd, 0x7c, 0x63, 0xc8, 0x86, 0xa9, 0x2b,
    0xd3, 0x90, 0x19, 0x8e, 0xb8, 0x12, 0x8a, 0xfb,
    0xf4, 0xde, 0x16, 0x2b, 0x8b, 0x95, 0xf6, 0x38,
])

def reveal(obscured_value):
    """
    Reverse rclone’s obscure function.
    The input should be a URL‑safe, unpadded base64 string produced by rclone.
    Returns the plaintext string (or a hex string if UTF‑8 decoding fails).
    """
    pad = '=' * ((4 - len(obscured_value) % 4) % 4)
    try:
        ciphertext = base64.urlsafe_b64decode(obscured_value + pad)
    except Exception as e:
        raise ValueError(f"Base64 decode error: {e}")
    if len(ciphertext) < 16:
        raise ValueError("Input too short; not a valid obscured value.")
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    ctr = int.from_bytes(iv, byteorder='big')
    cipher = AES.new(CRYPT_KEY, AES.MODE_CTR, initial_value=ctr, nonce=b'')
    plain = cipher.decrypt(ct)
    try:
        return plain.decode('utf-8')
    except UnicodeDecodeError:
        return plain.hex()

def decode_salt(salt_input):
    """
    Convert salt_input to exactly 32 bytes.
    If salt_input is 16 bytes (or decodes to 16), it is doubled.
    Otherwise, SHA-256 is used.
    """
    REQUIRED_SALT_LENGTH = 32
    if isinstance(salt_input, bytes):
        salt_bytes = salt_input
    elif isinstance(salt_input, str):
        try:
            salt_bytes = bytes.fromhex(salt_input)
        except ValueError:
            try:
                salt_bytes = base64.b64decode(salt_input)
            except Exception:
                salt_bytes = salt_input.encode('utf-8')
    else:
        raise ValueError("Salt must be provided as bytes or a string.")
    if len(salt_bytes) == REQUIRED_SALT_LENGTH:
        return salt_bytes
    elif len(salt_bytes) == REQUIRED_SALT_LENGTH // 2:
        return salt_bytes * 2
    else:
        return hashlib.sha256(salt_bytes).digest()

def make_key(password, salt=None, min_password_length=8):
    """
    Derive a 32-byte key using scrypt from a user-supplied password and salt.
    """
    if len(password) < min_password_length:
        raise ValueError(f"Password must be at least {min_password_length} characters long.")
    if salt is None:
        salt = DEFAULT_SALT
    salt = decode_salt(salt)
    key = nacl.pwhash.scrypt.kdf(
        nacl.secret.SecretBox.KEY_SIZE,
        password.encode('utf-8'),
        salt,
        opslimit=nacl.pwhash.scrypt.OPSLIMIT_INTERACTIVE,
        memlimit=nacl.pwhash.scrypt.MEMLIMIT_INTERACTIVE
    )
    return key

def decrypt_file(input_file, data_key, dest_dir=None):
    # Determine output file name: if dest_dir is provided, use that folder.
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        output_file = os.path.join(dest_dir, base_name)
    else:
        output_file = os.path.splitext(input_file)[0]
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        magic = infile.read(FILE_MAGIC_SIZE)
        if magic != FILE_MAGIC:
            print("Invalid file header in:", input_file)
            return 1
        nonce = infile.read(FILE_NONCE_SIZE)
        if len(nonce) != FILE_NONCE_SIZE:
            print("Failed to read nonce from:", input_file)
            return 1
        print("Nonce:", nonce.hex())
        i = 0
        while True:
            cipher_block = infile.read(BLOCK_SIZE)
            if len(cipher_block) == 0:
                break
            if len(cipher_block) <= nacl.secret.SecretBox.MACBYTES:
                print(f"Corrupted block {i} in:", input_file)
                return 1
            try:
                box = nacl.secret.SecretBox(data_key)
                plain_block = box.decrypt(cipher_block, nonce)
            except Exception as e:
                print("Decryption error:", e)
                return 1
            outfile.write(plain_block)
            nonce = increment_nonce(nonce)
            i += 1
    return 0

def increment_nonce(nonce):
    nonce_int = int.from_bytes(nonce, byteorder='little') + 1
    return nonce_int.to_bytes(FILE_NONCE_SIZE, byteorder='little')