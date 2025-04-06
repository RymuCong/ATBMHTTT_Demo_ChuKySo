import os
import base64
import json
from datetime import datetime

def save_signature(signature, output_path):
    """Lưu chữ ký vào file"""
    with open(output_path, 'wb') as f:
        f.write(signature)

def load_signature(signature_path):
    """Đọc chữ ký từ file"""
    with open(signature_path, 'rb') as f:
        return f.read()

def save_signature_info(file_path, signature_path, output_path, creator=""):
    """Lưu thông tin chữ ký vào file JSON"""
    # Lấy tên file gốc
    original_filename = os.path.basename(file_path)
    
    # Tạo thông tin chữ ký
    signature_info = {
        "original_file": original_filename,
        "signature_file": os.path.basename(signature_path),
        "creation_time": datetime.now().isoformat(),
        "creator": creator
    }
    
    # Lưu thông tin chữ ký vào file JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(signature_info, f, ensure_ascii=False, indent=4)

def load_signature_info(info_path):
    """Đọc thông tin chữ ký từ file JSON"""
    with open(info_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_text_to_file(text, file_path):
    """Lưu văn bản vào file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def read_text_from_file(file_path):
    """Đọc văn bản từ file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def ensure_directory_exists(directory):
    """Đảm bảo thư mục tồn tại"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_default_directories():
    """Tạo các thư mục mặc định cho ứng dụng"""
    directories = ['keys', 'signatures', 'temp']
    for directory in directories:
        ensure_directory_exists(directory)
    return directories 