import os
import tkinter as tk
from tkinter import ttk
import importlib.util
from settings.start import COLORS, FONTS, SETTINGS

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📂 Main Project Launcher")
        self.root.geometry(SETTINGS["window_size"])
        
        # إبقاء النافذة في المقدمة مؤقتاً عند البدء
        self.root.attributes('-topmost', 1)
        self.root.after(100, lambda: self.root.attributes('-topmost', 0))

        # تقسيم الواجهة: قائمة جانبية + محتوى
        self.sidebar = tk.Frame(self.root, width=200, bg=COLORS["dark"])
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self.root, bg=COLORS["light"])
        self.content.pack(side="right", fill="both", expand=True)

        # زر تحديث المشاريع
        refresh_btn = tk.Button(
            self.sidebar, text="🔄 ",
            bg=COLORS["info"], fg="white", relief="flat", padx=10, pady=10,
            font=FONTS["main"],
            command=self.refresh_projects
        )
        refresh_btn.pack(fill="x", pady=5)

        # تحميل المشاريع لأول مرة
        self.projects = self.find_projects()
        self.create_sidebar_buttons()

    def find_projects(self):
        """ البحث عن جميع المجلدات التي تحتوي ملف start.py """
        projects = {}
        base_dir = os.path.dirname(os.path.abspath(__file__))
        for item in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, item)
            if os.path.isdir(folder_path):
                start_file = os.path.join(folder_path, "start.py")
                if os.path.exists(start_file):
                    projects[item] = start_file
        return projects

    def create_sidebar_buttons(self):
        """ إنشاء أزرار في القائمة الجانبية لكل مشروع """
        # إزالة الأزرار السابقة (مع ترك زر التحديث)
        for widget in self.sidebar.winfo_children():
            if widget.cget("text") != "🔄 تحديث المشاريع":
                widget.destroy()

        for project_name, start_path in self.projects.items():
            btn = tk.Button(
                self.sidebar,
                text=project_name,
                bg=COLORS["primary"], fg="white",
                relief="flat", padx=10, pady=10,
                font=FONTS["main"],
                activebackground=COLORS["secondary"],
                command=lambda p=start_path: self.load_project(p)
            )
            btn.pack(fill="x", pady=2)

    def load_project(self, start_path):
        """ تحميل start.py وتشغيله داخل content """
        # تنظيف المحتوى الحالي
        for widget in self.content.winfo_children():
            widget.destroy()

        try:
            # تحميل الملف كـ module
            spec = importlib.util.spec_from_file_location("start_module", start_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # تمرير self.root أيضاً للتوافق مع النوافذ المنبثقة
            if hasattr(module, "main"):
                module.main(self.content, self.root)
            elif hasattr(module, "App"):
                app_instance = module.App(self.content)
                app_instance.main_window = self.root  # إضافة reference للنافذة الرئيسية
            else:
                lbl = tk.Label(
                    self.content,
                    text=f"⚠ {start_path} لا يحتوي على دالة main() أو App()",
                    fg=COLORS["danger"], bg=COLORS["light"], font=FONTS["main"]
                )
                lbl.pack(pady=20)

        except Exception as e:
            lbl = tk.Label(
                self.content,
                text=f"❌ خطأ أثناء تشغيل {start_path}\n\n{e}",
                fg=COLORS["danger"], bg=COLORS["light"], font=FONTS["main"]
            )
            lbl.pack(pady=20)

    def refresh_projects(self):
        """ إعادة تحميل المشاريع وتحديث القائمة """
        self.projects = self.find_projects()
        self.create_sidebar_buttons()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()