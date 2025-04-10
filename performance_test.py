import time
import os
import matplotlib.pyplot as plt
import numpy as np
from rsa_utils import generate_key_pair, sign_data, verify_signature, sign_file, verify_file_signature
import psutil
import platform
from cryptography import __version__ as crypto_version

def measure_execution_time(func, *args, **kwargs):
    """
    Đo thời gian thực thi của một hàm
    
    Tham số:
        func: Hàm cần đo thời gian
        *args, **kwargs: Tham số truyền vào hàm
        
    Trả về:
        tuple: (kết quả hàm, thời gian thực thi tính bằng mili giây)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    execution_time_ms = (end_time - start_time) * 1000
    return result, execution_time_ms

def test_text_data_performance():
    """
    Thử nghiệm hiệu suất với dữ liệu văn bản (4.3.2)
    """
    print("\n=== THỬ NGHIỆM VỚI DỮ LIỆU VĂN BẢN ===")
    
    # Tạo khóa
    private_key, public_key = generate_key_pair()
    
    # Các kích thước văn bản khác nhau (tính bằng KB)
    text_sizes = [1, 10, 100, 1000]
    signing_times = []
    verification_times = []
    
    for size in text_sizes:
        # Tạo văn bản với kích thước tương ứng
        text = "A" * (size * 1024)
        
        # Đo thời gian ký
        signature, signing_time = measure_execution_time(sign_data, private_key, text)
        signing_times.append(signing_time)
        
        # Đo thời gian xác thực
        _, verification_time = measure_execution_time(verify_signature, public_key, text, signature)
        verification_times.append(verification_time)
        
        print(f"\nKích thước văn bản: {size}KB")
        print(f"Thời gian ký: {signing_time:.2f} ms")
        print(f"Thời gian xác thực: {verification_time:.2f} ms")
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(text_sizes, signing_times, 'o-', label='Thời gian ký')
    plt.plot(text_sizes, verification_times, 'o-', label='Thời gian xác thực')
    plt.xlabel('Kích thước văn bản (KB)')
    plt.ylabel('Thời gian (ms)')
    plt.title('Hiệu suất xử lý văn bản')
    plt.legend()
    plt.grid(True)
    plt.savefig('text_performance.png')
    plt.close()

def test_image_data_performance():
    """
    Thử nghiệm hiệu suất với dữ liệu hình ảnh (4.3.3)
    """
    print("\n=== THỬ NGHIỆM VỚI DỮ LIỆU HÌNH ẢNH ===")
    
    # Tạo khóa
    private_key, public_key = generate_key_pair()
    
    # Danh sách các file ảnh mẫu với kích thước khác nhau
    image_files = [
        "test_images/small.png",    # ~100KB
        "test_images/medium.png",   # ~1MB
        "test_images/large.png"     # ~5MB
    ]
    
    signing_times = []
    verification_times = []
    file_sizes = []
    
    for image_file in image_files:
        if not os.path.exists(image_file):
            print(f"File {image_file} không tồn tại")
            continue
            
        file_size = os.path.getsize(image_file) / (1024 * 1024)  # Chuyển sang MB
        file_sizes.append(file_size)
        
        # Đo thời gian ký
        signature, signing_time = measure_execution_time(sign_file, private_key, image_file)
        signing_times.append(signing_time)
        
        # Đo thời gian xác thực
        _, verification_time = measure_execution_time(verify_file_signature, public_key, image_file, signature)
        verification_times.append(verification_time)
        
        print(f"\nFile: {image_file}")
        print(f"Kích thước: {file_size:.2f} MB")
        print(f"Thời gian ký: {signing_time:.2f} ms")
        print(f"Thời gian xác thực: {verification_time:.2f} ms")
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(file_sizes, signing_times, 'o-', label='Thời gian ký')
    plt.plot(file_sizes, verification_times, 'o-', label='Thời gian xác thực')
    plt.xlabel('Kích thước file (MB)')
    plt.ylabel('Thời gian (ms)')
    plt.title('Hiệu suất xử lý hình ảnh')
    plt.legend()
    plt.grid(True)
    plt.savefig('image_performance.png')
    plt.close()

def test_key_size_performance():
    """
    Thử nghiệm hiệu suất với các kích thước khóa khác nhau (4.3.4)
    """
    print("\n=== THỬ NGHIỆM VỚI CÁC KÍCH THƯỚC KHÓA KHÁC NHAU ===")
    
    # Các kích thước khóa cần thử nghiệm
    key_sizes = [1024, 2048, 3072, 4096]
    
    key_generation_times = []
    signing_times = []
    verification_times = []
    
    # Dữ liệu mẫu để ký và xác thực
    sample_data = "Test data for key size performance" * 100
    
    for size in key_sizes:
        print(f"\nKích thước khóa: {size} bit")
        
        # Đo thời gian tạo khóa
        result, gen_time = measure_execution_time(generate_key_pair, size)
        private_key, public_key = result
        key_generation_times.append(gen_time)
        print(f"Thời gian tạo khóa: {gen_time:.2f} ms")
        
        # Đo thời gian ký
        signature, signing_time = measure_execution_time(sign_data, private_key, sample_data)
        signing_times.append(signing_time)
        print(f"Thời gian ký: {signing_time:.2f} ms")
        
        # Đo thời gian xác thực
        _, verification_time = measure_execution_time(verify_signature, public_key, sample_data, signature)
        verification_times.append(verification_time)
        print(f"Thời gian xác thực: {verification_time:.2f} ms")
    
    # Vẽ biểu đồ
    plt.figure(figsize=(10, 6))
    plt.plot(key_sizes, key_generation_times, 'o-', label='Tạo khóa')
    plt.plot(key_sizes, signing_times, 'o-', label='Ký')
    plt.plot(key_sizes, verification_times, 'o-', label='Xác thực')
    plt.xlabel('Kích thước khóa (bit)')
    plt.ylabel('Thời gian (ms)')
    plt.title('Hiệu suất theo kích thước khóa')
    plt.legend()
    plt.grid(True)
    plt.savefig('key_size_performance.png')
    plt.close()

def report_system_metrics():
    """Báo cáo thông số hệ thống cho việc đo lường"""
    print("\n=== THÔNG SỐ HỆ THỐNG ĐO LƯỜNG ===")
    print(f"Hệ điều hành: {platform.system()} {platform.release()}")
    print(f"CPU: {platform.processor()}")
    print(f"Số lõi CPU: {psutil.cpu_count(logical=False)} (Vật lý), {psutil.cpu_count()} (Logical)")
    print(f"RAM: {psutil.virtual_memory().total / (1024*1024*1024):.2f} GB")
    print(f"Phiên bản Cryptography: {crypto_version}")
    print("===============================")

if __name__ == "__main__":
    # Báo cáo thông số hệ thống
    report_system_metrics()
    
    # Chạy các thử nghiệm
    test_text_data_performance()
    test_image_data_performance()
    test_key_size_performance() 