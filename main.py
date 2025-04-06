import os
import tkinter as tk
from tkinter import messagebox

try:
    from gui import RSASignatureApp
    from file_utils import create_default_directories
except ImportError as e:
    messagebox.showerror("Lỗi khi import", f"Không thể import các module cần thiết: {str(e)}")
    exit(1)

def main():
    """Hàm chính để khởi chạy ứng dụng"""
    # Tạo các thư mục mặc định
    try:
        create_default_directories()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo thư mục: {str(e)}")
    
    # Khởi tạo cửa sổ Tkinter
    root = tk.Tk()
    root.title("Ứng dụng Chữ ký số RSA")
    
    # Xác định kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Tính toán kích thước và vị trí cửa sổ
    window_width = 900
    window_height = 600
    position_x = (screen_width - window_width) // 2
    position_y = (screen_height - window_height) // 2
    
    # Đặt kích thước và vị trí cửa sổ
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    try:
        # Sử dụng icon ứng dụng nếu có
        if os.path.exists("keys/public_key_icon.png"):
            icon = tk.PhotoImage(file="keys/public_key_icon.png")
            root.iconphoto(True, icon)
    except Exception:
        pass
    
    # Khởi tạo ứng dụng
    app = RSASignatureApp(root)
    
    # Chạy vòng lặp chính
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        messagebox.showerror("Lỗi không xác định", f"Đã xảy ra lỗi không mong muốn: {str(e)}")
        exit(1) 