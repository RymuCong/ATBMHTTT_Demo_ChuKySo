# Ứng dụng Chữ ký số RSA

Đây là ứng dụng minh họa việc sử dụng chữ ký số RSA để đảm bảo tính toàn vẹn dữ liệu khi truyền tải giữa các bên. Ứng dụng có thể tạo chữ ký số cho cả văn bản và hình ảnh, đồng thời cung cấp khả năng xác thực tính toàn vẹn của dữ liệu.

## Tính năng

- Tạo cặp khóa RSA (khóa riêng tư và khóa công khai)
- Ký số cho dữ liệu văn bản
- Ký số cho file (hình ảnh, văn bản, ...)
- Xác thực tính toàn vẹn của dữ liệu bằng chữ ký số
- Giao diện đồ họa trực quan, dễ sử dụng
- Đo lường hiệu suất của quá trình ký và xác thực với các loại dữ liệu khác nhau

## Cài đặt

### Yêu cầu

- Python 3.8 trở lên
- Các thư viện Python: cryptography, Pillow, tkinter, matplotlib, psutil

### Cài đặt các thư viện cần thiết

```bash
pip install cryptography Pillow
```

### Các thư viện bổ sung

```bash
pip install matplotlib psutil
```

Hoặc cài đặt tất cả thư viện cần thiết với một lệnh:

```bash
pip install -r requirements.txt
```

### Tkinter

Tkinter thường được cài đặt mặc định với Python. Nếu chưa có, bạn có thể cài đặt:

- Windows: Thường được cài sẵn với Python
- Linux (Ubuntu/Debian): `sudo apt-get install python3-tk`
- macOS: Thường được cài sẵn với Python từ python.org

## Cách sử dụng

1. Chạy ứng dụng:
   ```bash
   python main.py
   ```

2. Ứng dụng sẽ hiển thị với 3 tab chức năng:

### Tab 1: Tạo Khóa
- Chọn kích thước khóa (1024, 2048, 3072, 4096 bit)
- Nhấn "Tạo cặp khóa mới" để tạo cặp khóa RSA
- Khóa được tự động lưu vào thư mục "keys"
- Có thể tải khóa có sẵn bằng cách chọn file và nhấn "Tải khóa"

### Tab 2: Tạo Chữ Ký
- Nhập văn bản hoặc chọn file để ký
- Nhấn "Ký dữ liệu" để tạo chữ ký
- Nhấn "Lưu chữ ký" để lưu chữ ký vào file
- Chữ ký được lưu trong thư mục "signatures"

### Tab 3: Xác Thực Chữ Ký
- Nhập văn bản hoặc chọn file cần xác thực
- Chọn file chữ ký
- Nhấn "Xác thực" để kiểm tra tính toàn vẹn
- Kết quả xác thực sẽ hiển thị (hợp lệ hoặc không hợp lệ)

## Mô hình hoạt động

1. **Bên gửi (A)**:
   - Tạo cặp khóa RSA (khóa riêng tư và khóa công khai)
   - Sử dụng khóa riêng tư để ký dữ liệu (văn bản hoặc file)
   - Gửi dữ liệu và chữ ký cho bên nhận
   - Chia sẻ khóa công khai cho bên nhận

2. **Bên nhận (B)**:
   - Nhận dữ liệu và chữ ký từ bên gửi
   - Sử dụng khóa công khai để xác thực chữ ký
   - Kiểm tra tính toàn vẹn của dữ liệu

## Lưu ý về an toàn

Đây là ứng dụng minh họa cho mục đích học tập và nghiên cứu. Trong môi trường thực tế, cần áp dụng thêm nhiều biện pháp bảo mật khác nhau:

- Bảo vệ khóa riêng tư an toàn
- Sử dụng cơ chế chứng thực khóa công khai (PKI)
- Mã hóa kênh truyền dữ liệu
- Sử dụng các tiêu chuẩn và thư viện bảo mật đã được kiểm chứng

## Thư mục

Ứng dụng tạo ra các thư mục sau:
- `keys/`: Lưu trữ các khóa RSA
- `signatures/`: Lưu trữ các chữ ký số
- `temp/`: Thư mục tạm thời cho xử lý dữ liệu 

## Đo lường hiệu suất

Ứng dụng bao gồm một tính năng đo lường hiệu suất cho phép so sánh thời gian xử lý trong các trường hợp khác nhau:

1. Chạy chương trình đo lường:
   ```bash
   python performance_test.py
   ```

2. Chương trình sẽ thực hiện các phép đo:
   - **Đo hiệu suất với dữ liệu văn bản**: Đo thời gian ký và xác thực với các văn bản có kích thước khác nhau (1KB đến 1000KB)
   - **Đo hiệu suất với dữ liệu hình ảnh**: Đo thời gian ký và xác thực các file ảnh có kích thước khác nhau
   - **Đo hiệu suất với các kích thước khóa khác nhau**: So sánh thời gian tạo khóa, ký và xác thực với các khóa có độ dài 1024, 2048, 3072 và 4096 bit

3. Kết quả được hiển thị dưới dạng:
   - Biểu đồ so sánh (lưu dưới dạng PNG)
   - Dữ liệu thời gian chi tiết in ra màn hình
   - Thông tin về cấu hình hệ thống đo lường

Thư mục `test_images/` chứa các hình ảnh mẫu được sử dụng trong quá trình đo lường. 