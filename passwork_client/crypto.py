import os
import random
import hashlib
import binascii
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as padding_rsa
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from .base32 import base32
import secrets


__all__ = [
    "encrypt_aes",
    "decrypt_aes",
    "generate_password",
    "get_master_key",
    "get_request_headers",
    "generate_string",
    'rsa_decrypt',
    'b64encode',
    'rsa_encrypt'
]


def evp_bytes_to_key(password: str, salt: bytes, key_len: int, iv_len: int):
    """
    OpenSSL key and IV generation
    """
    dt = d = b""
    while len(dt) < key_len + iv_len:
        # hash the input to generate enough bytes for key and IV
        d = hashlib.md5(d + password.encode() + salt).digest()
        dt += d
    return dt[:key_len], dt[key_len: key_len + iv_len]


def encrypt_aes(message: str | bytes, passphrase: str, is_bytes: bool = False):
    """
    Encrypts a message using AES in CBC mode with a key derived from the passphrase
    """
    if passphrase:
        salt = os.urandom(8)
        key_len = 32
        iv_len = 16
        key, iv = evp_bytes_to_key(passphrase, salt, key_len, iv_len)

        # AES cipher in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        # pad the message
        padder = padding.PKCS7(128).padder()
        message = message if is_bytes else message.encode()
        padded_data = padder.update(message) + padder.finalize()

        # encrypt the padded message
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # add salt to ciphertext
        encrypted_data = b"Salted__" + salt + ciphertext
    else:
        encrypted_data =  message.encode()
        return b64encode(encrypted_data).decode('utf-8')

    encrypted_data_b64 = b64encode(encrypted_data)

    return base32.encode(encrypted_data_b64.decode())


def decrypt_aes(encrypted_data_b32: str, passphrase: str, is_bytes: bool = False):
    """
    Decrypts a message encrypted with AES in CBC mode using the passphrase
    """
    encrypted_data_b64 = base32.decode(encrypted_data_b32)
    encrypted_data = b64decode(encrypted_data_b64)

    # extract the salt and the ciphertext from the decoded data
    salt = encrypted_data[8:16]  # salt is after the "Salted__" marker
    ciphertext = encrypted_data[16:]

    key_len = 32
    iv_len = 16
    key, iv = evp_bytes_to_key(passphrase, salt, key_len, iv_len)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # decrypt and unpad the message
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext if is_bytes else plaintext.decode("utf-8")


def generate_string(length: int = 32):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!"
    return get_random_string(length, possible)

def generate_salt(length: int = 32):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!"
    return get_random_string(length, possible)

def generate_key():
    KEY_LENGTH = 100
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@!"
    return get_random_string(KEY_LENGTH, possible)

def generate_password(length: int = 32):
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^"
    return get_random_string(length, possible)

def generate_user_password(length: int = 32, complexity: dict = {}):
    digits = "0123456789"
    special_characters = "!@#$%^"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lowercase = "abcdefghijklmnopqrstuvwxyz"

    min_length = int(complexity["minLength"]) if complexity.get("minLength") else 0
    length = min_length if min_length and min_length > length else length

    is_digits_required = bool(complexity["isDigitsRequired"]) if complexity.get("isDigitsRequired") else False
    is_uppercase_required = bool(complexity["isUppercaseRequired"]) if complexity.get("isUppercaseRequired") else False
    is_special_characters_required = bool(complexity["isSpecialCharactersRequired"]) if complexity.get("isSpecialCharactersRequired") else False
    characters = f"{digits}{special_characters}{uppercase}{lowercase}"

    password = get_random_string(length, characters)

    if is_digits_required and not any(c in digits for c in password):
        return generate_user_password(length, complexity)

    if is_uppercase_required and not any(c in uppercase for c in password):
        return generate_user_password(length, complexity)

    if is_special_characters_required and not any(c in special_characters for c in password):
        return generate_user_password(length, complexity)

    return password

def get_random_string(length: int = 32, possible: str = ""):
    return "".join(secrets.choice(possible) for _ in range(length))

def get_master_key(mk_options: dict, master_password: str):

    salt = mk_options["salt"]
    iterations = int(mk_options["iterations"]) if mk_options.get("iterations") else 300000
    bytes_dklen = int(mk_options["bytes"]) if mk_options.get("bytes") else 64
    digest = mk_options["digest"] if mk_options.get("digest") else "sha256"


    # get pbkdf master key
    dk = hashlib.pbkdf2_hmac(digest, master_password.encode(), salt.encode(), iterations, dklen=bytes_dklen)
    result = binascii.b2a_base64(dk).decode().strip()
    return {
        "hashedString": result,
        "masterKeyOptions": ":".join(["pbkdf", digest, str(iterations), str(bytes_dklen), salt])
    }


def get_request_headers(token: str, master_key: str, use_master_password: bool):
    headers = {"Passwork-Auth": token}

    if use_master_password:
        # calculate hash
        master_key_hash = hashlib.sha256(master_key.encode()).hexdigest()
        headers["X-Master-Key-Hash"] = master_key_hash
    return headers

def get_hash(str: str, func: str | None = None):
    if not str:
        return ''

    match func:
        case "sha256":
            return hashlib.sha256(str.encode()).hexdigest()
        case "sha512":
            return hashlib.sha512(str.encode()).hexdigest()
        case _:
            return hashlib.sha256(str.encode()).hexdigest()


def rsa_decrypt(data, private_key):
    private_key = serialization.load_pem_private_key(
        private_key.encode(),  # Convert to bytes
        password=None
    )
    decrypted_data = private_key.decrypt(
        b64decode(data),
        padding_rsa.PKCS1v15()
    )
    return decrypted_data

def rsa_encrypt(data, public_key):
    public_key = serialization.load_pem_public_key(
        public_key.encode(),  # Convert to bytes
        None
    )
    decrypted_data = public_key.encrypt(
        data.encode(),
        padding_rsa.PKCS1v15()
    )
    return decrypted_data

def generate_rsa_keys(masterKey: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,  
        key_size=2048,          
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_encrypted = encrypt_aes(private_pem, masterKey, True)
    return {"public": public_pem.decode('utf-8'), "privateEncrypted": private_encrypted}