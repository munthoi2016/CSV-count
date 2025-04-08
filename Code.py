import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from collections import defaultdict

def get_csv_file():
    """Mở hộp thoại chọn file CSV và trả về đường dẫn."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    return file_path if file_path else None

def process_csv_data(file_path):
    """Đọc dữ liệu từ file CSV và xử lý."""
    try:
        df = pd.read_csv(file_path)
        if df.empty or df.shape[1] < 2:
            messagebox.showerror("Lỗi", "File CSV không hợp lệ hoặc không có dữ liệu.")
            return None
        
        component_counts = defaultdict(int)
        for _, row in df.iterrows():
            components = str(row[0]).strip()
            qty = int(row[1]) if pd.notna(row[1]) else 0
            for component in map(str.strip, components.split(",")):
                component_counts[component] += qty
        
        return component_counts
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xử lý file CSV: {e}")
        return None

def display_results(component_counts):
    """Hiển thị kết quả trong bảng có thể copy dữ liệu."""
    result_window = tk.Toplevel(root)
    result_window.title("Kết quả")
    result_window.geometry("400x300")
    
    tree = ttk.Treeview(result_window, columns=("Thành phần", "Tổng số lượng"), show="headings")
    tree.heading("Thành phần", text="Thành phần")
    tree.heading("Tổng số lượng", text="Tổng số lượng")
    tree.pack(fill=tk.BOTH, expand=True)
    
    for component, count in sorted(component_counts.items(), key=lambda x: x[1], reverse=True):
        tree.insert("", tk.END, values=(component, count))
    
    def copy_to_clipboard():
        text = "Thành phần\tTổng số lượng\n" + "\n".join(f"{comp}\t{cnt}" for comp, cnt in component_counts.items())
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        messagebox.showinfo("Thông báo", "Dữ liệu đã được sao chép vào clipboard.")
    
    copy_btn = tk.Button(result_window, text="Copy", command=copy_to_clipboard)
    copy_btn.pack(pady=10)

def process_csv_file():
    """Xử lý file CSV và hiển thị kết quả."""
    file_path = get_csv_file()
    if file_path:
        component_counts = process_csv_data(file_path)
        if component_counts:
            display_results(component_counts)

# Tạo giao diện
root = tk.Tk()
root.title("Xử lý Linh Kiện từ CSV")
root.geometry("300x150")

btn_select = tk.Button(root, text="Chọn CSV", command=process_csv_file)
btn_select.pack(pady=20)

root.mainloop()
