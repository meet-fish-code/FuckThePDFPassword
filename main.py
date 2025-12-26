import os
import sys
import pikepdf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Button
import threading


class PDFUnlockerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("FuckThePdfPassword「鱼见」")

        # 设置固定窗口大小
        self.root.geometry("400x220")  # 设置窗口大小为 400x300
        self.root.resizable(False, False)  # 禁止用户调整窗口大小

        # 选择文件和保存路径的超链接样式（不使用字体）
        self.files_label = tk.Label(root, text="选择PDF文件", fg="blue", cursor="hand2")
        self.files_label.grid(row=0, column=0, padx=10, pady=10)
        self.files_label.bind("<Button-1>", self.select_files)

        self.output_label = tk.Label(root, text="选择保存路径", fg="blue", cursor="hand2")
        self.output_label.grid(row=0, column=1, padx=10, pady=10)
        self.output_label.bind("<Button-1>", self.select_output)

        # 解锁按钮
        self.unlock_button = Button(root, text="解锁PDF文件", command=self.unlock_pdfs, style="Modern.TButton")
        self.unlock_button.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

        # 进度条
        self.progress = Progressbar(root, length=380, mode='determinate')
        self.progress.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        # 成功和失败提示
        self.result_label = tk.Label(root, text="")
        self.result_label.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.result_label.config(text="提示：请选择要解锁的PDF文件")
        # 初始化
        self.files = []
        self.output_folder = ""

        # 添加版权和版本信息标签（右下角）
        self.version_label = tk.Label(root, text="v0.1.1 - 鱼见工作室", font=("黑体", 8), fg="gray")
        self.version_label.grid(row=4, column=1, padx=10, pady=10, sticky="se")

    def select_files(self, event=None):
        self.files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if self.files:
            self.result_label.config(text="提示：文件已打开，请选择保存路径（不要和源文件同目录）")

    def select_output(self, event=None):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.result_label.config(text="提示：已选择保存路径，请开始解锁")

    def unlock_pdf(self, file, output_folder):
        try:
            # 尝试打开 PDF 文件
            with pikepdf.open(file, password='') as pdf:  # 尝试使用空密码
                # 如果解锁成功，保存为新的文件
                output_file_path = os.path.join(output_folder, os.path.basename(file))
                pdf.save(output_file_path)
                return True
        except pikepdf.PasswordError:
            # 如果密码错误
            print(f"解锁失败，密码错误: {file}")
            return False
        except Exception as e:
            print(f"解锁 {file} 失败: {e}")
            return False

    def unlock_pdfs(self):
        if not self.files or not self.output_folder:
            messagebox.showerror("错误", "请选择PDF文件和保存路径")
            return

        def process_unlock():
            successful = 0
            failed = 0
            total_files = len(self.files)

            for i, file in enumerate(self.files):
                result = self.unlock_pdf(file, self.output_folder)
                if result:
                    successful += 1
                else:
                    failed += 1

                # 更新进度条
                self.progress['value'] = (i + 1) / total_files * 100
                self.root.update_idletasks()

            # 显示最终结果
            self.result_label.config(text=f"提示：解锁完成: 成功 {successful} 个, 失败 {failed} 个")
            messagebox.showinfo("完成", f"解锁完成: 成功 {successful} 个, 失败 {failed} 个")

        # 在新线程中执行解锁操作，以避免阻塞UI界面
        threading.Thread(target=process_unlock, daemon=True).start()


def resource_path(relative_path):
    """获取打包后的文件路径"""
    try:
        # 如果是打包后的文件，可以通过 `sys._MEIPASS` 获取到临时路径
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 创建界面
root = tk.Tk()
# 设置图标路径
icon_path = resource_path("meetfish.ico")
root.iconbitmap(icon_path)
root.configure(bg="#f7f7f7")
app = PDFUnlockerApp(root)
root.mainloop()
