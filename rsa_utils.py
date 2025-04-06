import os
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

def generate_key_pair(key_size=2048):
    """Tạo cặp khóa RSA (khóa riêng tư và khóa công khai)"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    
    return private_key, public_key

def save_private_key(private_key, path, password=None):
    """Lưu khóa riêng tư vào file"""
    encryption_algorithm = serialization.NoEncryption()
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
    
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )
    
    with open(path, 'wb') as f:
        f.write(pem)

def save_public_key(public_key, path):
    """Lưu khóa công khai vào file"""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open(path, 'wb') as f:
        f.write(pem)

def load_private_key(path, password=None):
    """Đọc khóa riêng tư từ file"""
    with open(path, 'rb') as f:
        private_key_data = f.read()
    
    if password:
        return serialization.load_pem_private_key(
            private_key_data,
            password=password.encode()
        )
    return serialization.load_pem_private_key(
        private_key_data,
        password=None
    )

def load_public_key(path):
    """Đọc khóa công khai từ file"""
    with open(path, 'rb') as f:
        public_key_data = f.read()
    
    return serialization.load_pem_public_key(public_key_data)

def calculate_file_hash(file_path):
    """Tính giá trị hash của file"""
    hash_obj = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_obj.update(chunk)
    
    return hash_obj.digest()

def calculate_data_hash(data):
    """Tính giá trị hash của dữ liệu"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    hash_obj = hashlib.sha256()
    hash_obj.update(data)
    return hash_obj.digest()

def sign_data(private_key, data):
    """Tạo chữ ký số cho dữ liệu"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    return signature

def sign_file(private_key, file_path):
    """Tạo chữ ký số cho file"""
    file_hash = calculate_file_hash(file_path)
    return sign_data(private_key, file_hash)

def verify_signature(public_key, data, signature):
    """Xác thực chữ ký số cho dữ liệu"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False

def verify_file_signature(public_key, file_path, signature):
    """Xác thực chữ ký số cho file"""
    file_hash = calculate_file_hash(file_path)
    return verify_signature(public_key, file_hash, signature) 