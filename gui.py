import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import io

from rsa_utils import (
    generate_key_pair, save_private_key, save_public_key,
    load_private_key, load_public_key,
    sign_data, sign_file,
    verify_signature, verify_file_signature
)
from file_utils import (
    save_signature, load_signature,
    save_signature_info, load_signature_info,
    save_text_to_file, read_text_from_file,
    ensure_directory_exists, create_default_directories
)

class RSASignatureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Chữ ký số RSA")
        self.root.geometry("900x600")
        
        # Khởi tạo các biến
        self.private_key = None
        self.public_key = None
        self.current_text = ""
        self.current_file_path = None
        self.signature = None
        self.signature_path = None
        
        # Tạo các thư mục mặc định
        self.directories = create_default_directories()
        
        # Tạo giao diện
        self.create_tabs()
        self.create_key_generation_tab()
        self.create_signature_tab()
        self.create_verification_tab()
    
    def create_tabs(self):
        """Tạo hệ thống tab cho giao diện"""
        self.tab_control = ttk.Notebook(self.root)
        
        self.key_tab = ttk.Frame(self.tab_control)
        self.signature_tab = ttk.Frame(self.tab_control)
        self.verification_tab = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.key_tab, text="Tạo Khóa")
        self.tab_control.add(self.signature_tab, text="Tạo Chữ Ký")
        self.tab_control.add(self.verification_tab, text="Xác Thực Chữ Ký")
        
        self.tab_control.pack(expand=1, fill="both")
    
    def create_key_generation_tab(self):
        """Tạo tab tạo khóa"""
        frame = ttk.LabelFrame(self.key_tab, text="Tạo và quản lý khóa RSA")
        frame.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Khung thông tin
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(info_frame, text="Kích thước khóa:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_size_var = tk.StringVar(value="2048")
        key_size_combo = ttk.Combobox(info_frame, textvariable=self.key_size_var, width=10)
        key_size_combo['values'] = ("1024", "2048", "3072", "4096")
        key_size_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Khóa riêng tư
        private_key_frame = ttk.LabelFrame(frame, text="Khóa riêng tư (Private Key)")
        private_key_frame.pack(fill="both", padx=10, pady=5, expand=1)
        
        self.private_key_path = tk.StringVar()
        ttk.Entry(private_key_frame, textvariable=self.private_key_path, width=50).pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=1)
        ttk.Button(private_key_frame, text="Chọn", command=self.load_private_key_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Khóa công khai
        public_key_frame = ttk.LabelFrame(frame, text="Khóa công khai (Public Key)")
        public_key_frame.pack(fill="both", padx=10, pady=5, expand=1)
        
        self.public_key_path = tk.StringVar()
        ttk.Entry(public_key_frame, textvariable=self.public_key_path, width=50).pack(side=tk.LEFT, padx=5, pady=5, fill="x", expand=1)
        ttk.Button(public_key_frame, text="Chọn", command=self.load_public_key_dialog).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Nút tạo khóa
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Tạo cặp khóa mới", command=self.generate_keys).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Tải khóa", command=self.load_keys).pack(side=tk.LEFT, padx=5, pady=5)
        
    def create_signature_tab(self):
        """Tạo tab ký số"""
        frame = ttk.LabelFrame(self.signature_tab, text="Tạo chữ ký số")
        frame.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Chọn dữ liệu để ký
        data_frame = ttk.LabelFrame(frame, text="Dữ liệu cần ký")
        data_frame.pack(fill="both", padx=10, pady=5, expand=1)
        
        # Tab cho văn bản và file
        data_tab = ttk.Notebook(data_frame)
        data_tab.pack(expand=1, fill="both", padx=5, pady=5)
        
        # Tab văn bản
        text_tab = ttk.Frame(data_tab)
        data_tab.add(text_tab, text="Văn bản")
        
        self.text_input = scrolledtext.ScrolledText(text_tab, height=10)
        self.text_input.pack(fill="both", expand=1, padx=5, pady=5)
        
        text_buttons = ttk.Frame(text_tab)
        text_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(text_buttons, text="Tải từ file", command=self.load_text_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(text_buttons, text="Lưu vào file", command=self.save_text_to_file).pack(side=tk.LEFT, padx=5)
        
        # Tab file
        file_tab = ttk.Frame(data_tab)
        data_tab.add(file_tab, text="File (hình ảnh/văn bản)")
        
        file_content = ttk.Frame(file_tab)
        file_content.pack(fill="both", expand=1, padx=5, pady=5)
        
        self.file_path_var = tk.StringVar()
        ttk.Entry(file_content, textvariable=self.file_path_var, width=50).pack(side=tk.LEFT, fill="x", expand=1, padx=5, pady=5)
        ttk.Button(file_content, text="Chọn file", command=self.select_file).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.file_preview = ttk.LabelFrame(file_tab, text="Xem trước")
        self.file_preview.pack(fill="both", expand=1, padx=5, pady=5)
        
        self.preview_label = ttk.Label(self.file_preview, text="Chưa có file nào được chọn")
        self.preview_label.pack(expand=1, fill="both", padx=5, pady=5)
        
        # Khung ký
        signature_frame = ttk.LabelFrame(frame, text="Tạo chữ ký")
        signature_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(signature_frame, text="Ký dữ liệu", command=self.sign_data_action).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(signature_frame, text="Lưu chữ ký", command=self.save_signature_action).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Trạng thái
        self.signature_status = ttk.Label(frame, text="")
        self.signature_status.pack(fill="x", padx=10, pady=5)
    
    def create_verification_tab(self):
        """Tạo tab xác thực chữ ký"""
        frame = ttk.LabelFrame(self.verification_tab, text="Xác thực chữ ký số")
        frame.pack(expand=1, fill="both", padx=10, pady=10)
        
        # Chọn dữ liệu để xác thực
        data_frame = ttk.LabelFrame(frame, text="Dữ liệu cần xác thực")
        data_frame.pack(fill="both", padx=10, pady=5, expand=1)
        
        # Tab cho văn bản và file
        verify_data_tab = ttk.Notebook(data_frame)
        verify_data_tab.pack(expand=1, fill="both", padx=5, pady=5)
        
        # Tab văn bản
        verify_text_tab = ttk.Frame(verify_data_tab)
        verify_data_tab.add(verify_text_tab, text="Văn bản")
        
        self.verify_text_input = scrolledtext.ScrolledText(verify_text_tab, height=10)
        self.verify_text_input.pack(fill="both", expand=1, padx=5, pady=5)
        
        verify_text_buttons = ttk.Frame(verify_text_tab)
        verify_text_buttons.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(verify_text_buttons, text="Tải từ file", command=self.load_verify_text_from_file).pack(side=tk.LEFT, padx=5)
        
        # Tab file
        verify_file_tab = ttk.Frame(verify_data_tab)
        verify_data_tab.add(verify_file_tab, text="File (hình ảnh/văn bản)")
        
        verify_file_content = ttk.Frame(verify_file_tab)
        verify_file_content.pack(fill="both", expand=1, padx=5, pady=5)
        
        self.verify_file_path_var = tk.StringVar()
        ttk.Entry(verify_file_content, textvariable=self.verify_file_path_var, width=50).pack(side=tk.LEFT, fill="x", expand=1, padx=5, pady=5)
        ttk.Button(verify_file_content, text="Chọn file", command=self.select_verify_file).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.verify_file_preview = ttk.LabelFrame(verify_file_tab, text="Xem trước")
        self.verify_file_preview.pack(fill="both", expand=1, padx=5, pady=5)
        
        self.verify_preview_label = ttk.Label(self.verify_file_preview, text="Chưa có file nào được chọn")
        self.verify_preview_label.pack(expand=1, fill="both", padx=5, pady=5)
        
        # Chọn chữ ký
        signature_frame = ttk.LabelFrame(frame, text="Chữ ký")
        signature_frame.pack(fill="x", padx=10, pady=5)
        
        self.verify_signature_path_var = tk.StringVar()
        ttk.Entry(signature_frame, textvariable=self.verify_signature_path_var, width=50).pack(side=tk.LEFT, fill="x", expand=1, padx=5, pady=5)
        ttk.Button(signature_frame, text="Chọn file chữ ký", command=self.select_signature_file).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Nút xác thực
        verify_button_frame = ttk.Frame(frame)
        verify_button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(verify_button_frame, text="Xác thực", command=self.verify_signature_action).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Kết quả xác thực
        self.verify_result = ttk.Label(frame, text="")
        self.verify_result.pack(fill="x", padx=10, pady=5)
    
    # Các phương thức xử lý sự kiện
    def generate_keys(self):
        """Tạo cặp khóa mới"""
        try:
            key_size = int(self.key_size_var.get())
            self.private_key, self.public_key = generate_key_pair(key_size)
            
            # Lưu khóa vào file
            private_key_path = os.path.join("keys", f"private_key_{key_size}.pem")
            public_key_path = os.path.join("keys", f"public_key_{key_size}.pem")
            
            save_private_key(self.private_key, private_key_path)
            save_public_key(self.public_key, public_key_path)
            
            self.private_key_path.set(private_key_path)
            self.public_key_path.set(public_key_path)
            
            messagebox.showinfo("Thành công", f"Đã tạo cặp khóa {key_size} bit thành công và lưu vào thư mục 'keys'")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tạo khóa: {str(e)}")
    
    def load_private_key_dialog(self):
        """Mở hộp thoại chọn file khóa riêng tư"""
        file_path = filedialog.askopenfilename(
            title="Chọn file khóa riêng tư",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
            initialdir="keys"
        )
        if file_path:
            self.private_key_path.set(file_path)
    
    def load_public_key_dialog(self):
        """Mở hộp thoại chọn file khóa công khai"""
        file_path = filedialog.askopenfilename(
            title="Chọn file khóa công khai",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
            initialdir="keys"
        )
        if file_path:
            self.public_key_path.set(file_path)
    
    def load_keys(self):
        """Tải khóa từ file"""
        try:
            private_key_path = self.private_key_path.get()
            public_key_path = self.public_key_path.get()
            
            if (private_key_path == "" or public_key_path == ""):
                messagebox.showerror("Lỗi", "Cần chọn file khóa riêng tư và công khai trước khi tải khóa")
                return

            if private_key_path:
                self.private_key = load_private_key(private_key_path)
            
            if public_key_path:
                self.public_key = load_public_key(public_key_path)
            
            messagebox.showinfo("Thành công", "Đã tải khóa thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải khóa: {str(e)}")
    
    def load_text_from_file(self):
        """Tải văn bản từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file văn bản",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                text = read_text_from_file(file_path)
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(tk.END, text)
                self.current_text = text
                messagebox.showinfo("Thành công", "Đã tải văn bản từ file thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải văn bản: {str(e)}")
    
    def save_text_to_file(self):
        """Lưu văn bản vào file"""
        text = self.text_input.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Không có văn bản để lưu")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Lưu văn bản",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            defaultextension=".txt"
        )
        if file_path:
            try:
                save_text_to_file(text, file_path)
                self.current_text = text
                messagebox.showinfo("Thành công", "Đã lưu văn bản vào file thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu văn bản: {str(e)}")
    
    def select_file(self):
        """Chọn file để ký"""
        file_path = filedialog.askopenfilename(
            title="Chọn file để ký",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.current_file_path = file_path
            self.show_file_preview(file_path, self.preview_label, self.file_preview)
    
    def show_file_preview(self, file_path, label_widget, frame_widget):
        """Hiển thị xem trước file"""
        if not file_path or not os.path.exists(file_path):
            label_widget.config(text="Không thể tìm thấy file")
            return
        
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            try:
                # Hiển thị hình ảnh
                image = Image.open(file_path)
                # Điều chỉnh kích thước hình ảnh
                max_width = frame_widget.winfo_width() - 20 if frame_widget.winfo_width() > 100 else 300
                max_height = 200
                image.thumbnail((max_width, max_height))
                
                photo = ImageTk.PhotoImage(image)
                
                # Xóa nội dung cũ
                for widget in frame_widget.winfo_children():
                    widget.destroy()
                
                # Hiển thị hình ảnh mới
                img_label = ttk.Label(frame_widget, image=photo)
                img_label.image = photo  # Giữ tham chiếu
                img_label.pack(padx=5, pady=5)
                
                info_label = ttk.Label(frame_widget, text=f"Hình ảnh: {os.path.basename(file_path)}")
                info_label.pack(padx=5, pady=5)
            except Exception as e:
                label_widget.config(text=f"Không thể hiển thị hình ảnh: {str(e)}")
        else:
            try:
                # Hiển thị văn bản
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read(500)  # Chỉ đọc 500 ký tự đầu
                
                # Xóa nội dung cũ
                for widget in frame_widget.winfo_children():
                    widget.destroy()
                
                text_preview = scrolledtext.ScrolledText(frame_widget, height=10, width=40)
                text_preview.insert(tk.END, text + ("..." if len(text) >= 500 else ""))
                text_preview.config(state=tk.DISABLED)
                text_preview.pack(padx=5, pady=5, fill="both", expand=1)
                
                info_label = ttk.Label(frame_widget, text=f"Văn bản: {os.path.basename(file_path)}")
                info_label.pack(padx=5, pady=5)
            except Exception as e:
                label_widget.config(text=f"Không thể hiển thị văn bản: {str(e)}")
    
    def sign_data_action(self):
        """Ký dữ liệu"""
        if not self.private_key:
            messagebox.showerror("Lỗi", "Cần tải khóa riêng tư trước khi ký")
            return
        
        try:
            current_tab = self.tab_control.index(self.tab_control.select())
            if current_tab != 1:  # Không phải tab signature
                self.tab_control.select(1)
            
            # Xác định loại dữ liệu (văn bản hoặc file)
            data_tab = self.signature_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0]
            current_data_tab = data_tab.index(data_tab.select())
            
            if current_data_tab == 0:  # Tab văn bản
                text = self.text_input.get(1.0, tk.END).strip()
                if not text:
                    messagebox.showwarning("Cảnh báo", "Không có văn bản để ký")
                    return
                
                self.signature = sign_data(self.private_key, text)
                self.signature_status.config(text="Đã ký văn bản thành công", foreground="green")
            else:  # Tab file
                file_path = self.file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    messagebox.showwarning("Cảnh báo", "Cần chọn file để ký")
                    return
                
                self.signature = sign_file(self.private_key, file_path)
                self.signature_status.config(text=f"Đã ký file '{os.path.basename(file_path)}' thành công", foreground="green")
            
            messagebox.showinfo("Thành công", "Đã tạo chữ ký thành công")
        except Exception as e:
            self.signature_status.config(text=f"Lỗi khi ký: {str(e)}", foreground="red")
            messagebox.showerror("Lỗi", f"Không thể ký dữ liệu: {str(e)}")
    
    def save_signature_action(self):
        """Lưu chữ ký vào file"""
        if not self.signature:
            messagebox.showerror("Lỗi", "Cần tạo chữ ký trước khi lưu")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Lưu chữ ký",
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")],
            defaultextension=".sig",
            initialdir="signatures"
        )
        if file_path:
            try:
                save_signature(self.signature, file_path)
                self.signature_path = file_path
                
                # Tạo file thông tin chữ ký
                info_path = file_path + ".info"
                data_source = self.current_file_path if self.current_file_path else "text_input.txt"
                save_signature_info(data_source, file_path, info_path)
                
                messagebox.showinfo("Thành công", f"Đã lưu chữ ký vào file '{os.path.basename(file_path)}'")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu chữ ký: {str(e)}")
    
    def load_verify_text_from_file(self):
        """Tải văn bản để xác thực từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn file văn bản để xác thực",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                text = read_text_from_file(file_path)
                self.verify_text_input.delete(1.0, tk.END)
                self.verify_text_input.insert(tk.END, text)
                messagebox.showinfo("Thành công", "Đã tải văn bản từ file thành công")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải văn bản: {str(e)}")
    
    def select_verify_file(self):
        """Chọn file để xác thực"""
        file_path = filedialog.askopenfilename(
            title="Chọn file để xác thực",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.verify_file_path_var.set(file_path)
            self.show_file_preview(file_path, self.verify_preview_label, self.verify_file_preview)
    
    def select_signature_file(self):
        """Chọn file chữ ký"""
        file_path = filedialog.askopenfilename(
            title="Chọn file chữ ký",
            filetypes=[("Signature files", "*.sig"), ("All files", "*.*")],
            initialdir="signatures"
        )
        if file_path:
            self.verify_signature_path_var.set(file_path)
    
    def verify_signature_action(self):
        """Xác thực chữ ký"""
        if not self.public_key:
            messagebox.showerror("Lỗi", "Cần tải khóa công khai trước khi xác thực")
            return
        
        signature_path = self.verify_signature_path_var.get()
        if not signature_path or not os.path.exists(signature_path):
            messagebox.showwarning("Cảnh báo", "Cần chọn file chữ ký để xác thực")
            return
        
        try:
            signature = load_signature(signature_path)
            
            # Xác định loại dữ liệu (văn bản hoặc file)
            verify_data_tab = self.verification_tab.winfo_children()[0].winfo_children()[0].winfo_children()[0]
            current_data_tab = verify_data_tab.index(verify_data_tab.select())
            
            if current_data_tab == 0:  # Tab văn bản
                text = self.verify_text_input.get(1.0, tk.END).strip()
                if not text:
                    messagebox.showwarning("Cảnh báo", "Không có văn bản để xác thực")
                    return
                
                is_valid = verify_signature(self.public_key, text, signature)
            else:  # Tab file
                file_path = self.verify_file_path_var.get()
                if not file_path or not os.path.exists(file_path):
                    messagebox.showwarning("Cảnh báo", "Cần chọn file để xác thực")
                    return
                
                is_valid = verify_file_signature(self.public_key, file_path, signature)
            
            if is_valid:
                self.verify_result.config(text="Chữ ký hợp lệ ✓ - Dữ liệu không bị thay đổi", foreground="green")
                messagebox.showinfo("Kết quả xác thực", "Chữ ký hợp lệ - Dữ liệu không bị thay đổi")
            else:
                self.verify_result.config(text="Chữ ký không hợp lệ ✗ - Dữ liệu có thể đã bị thay đổi", foreground="red")
                messagebox.showwarning("Kết quả xác thực", "Chữ ký không hợp lệ - Dữ liệu có thể đã bị thay đổi")
        except Exception as e:
            self.verify_result.config(text=f"Lỗi khi xác thực: {str(e)}", foreground="red")
            messagebox.showerror("Lỗi", f"Không thể xác thực chữ ký: {str(e)}") 