import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import sys
import shutil
from settings.start import COLORS, FONTS, SETTINGS
# ---------------------- Tooltip Class ----------------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tip_window or not self.text:
            return
        try:
            x, y, _, cy = self.widget.bbox("insert")
        except Exception:
            x, y, cy = 0, 0, 0
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + cy + 20
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#fffacd", relief="solid", borderwidth=1,
            font=("Helvetica", 9, "normal")
        )
        label.pack(ipadx=6, ipady=3)

    def hide_tip(self, event=None):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


# ---------------------- Project Explorer ----------------------
class ProjectExplorer:
    def __init__(self, parent):
        self.root = parent
        self.root.configure(bg="#f0f3f7")
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.setup_styles()
        self.build_ui()
        self.last_snapshot = self.snapshot_project()
        self.auto_refresh()

    # ---------------------- Styles ----------------------
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Top.TFrame", background="#34495e")
        style.configure("Title.TLabel", font=("Helvetica", 14, "bold"), foreground="white", background="#34495e")
        style.configure("TButton", font=("Helvetica", 10), padding=5, relief="flat", background="#ecf0f1")
        style.map("TButton", background=[("active", "#3498db")], foreground=[("active", "white")])
        style.configure("Add.TButton", font=("Helvetica", 10, "bold"), background="#2980b9", foreground="white")
        style.map("Add.TButton", background=[("active", "#3498db")])
        style.configure("Refresh.TButton", font=("Helvetica", 10, "bold"), background="#27ae60", foreground="white")
        style.map("Refresh.TButton", background=[("active", "#2ecc71")])
        style.configure("Main.TFrame", background="#f0f3f7")
        style.configure("Inner.TFrame", background="#fdfdfd")
        style.configure("TLabelframe", background="#fefefe", relief="raised", borderwidth=1)
        style.configure("TLabelframe.Label", font=("Helvetica", 11, "bold"), foreground="#2c3e50")
        style.configure("Status.TLabel", background="#2c3e50", foreground="white", font=("Helvetica", 9, "italic"))

    # ---------------------- UI Setup ----------------------
    def build_ui(self):
        # Top Frame
        top_frame = ttk.Frame(self.root, padding=5, style="Top.TFrame")
        top_frame.pack(fill=tk.X)
        title_lbl = ttk.Label(top_frame, text="📂 Project Explorer", style="Title.TLabel")
        title_lbl.pack(side=tk.LEFT, padx=10)
        ttk.Button(top_frame, text="🔄 Refresh", style="Refresh.TButton", command=self.refresh_view).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="📄 Add File", style="Add.TButton", command=self.add_file).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="➕ Add Folder", style="Add.TButton", command=self.add_folder).pack(side=tk.RIGHT, padx=5)

        # Main Scrollable Frame
        self.main_frame = ttk.Frame(self.root, style="Main.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(self.main_frame, bg="#fdfdfd", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style="Inner.TFrame")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Status Bar
        self.status_bar = ttk.Label(self.root, text="✅ Ready", style="Status.TLabel", anchor="w")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=3)

        # Initialize Sections
        self.create_sections()

    # ---------------------- Scroll ----------------------
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    # ---------------------- Sections ----------------------
    def create_sections(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for folder in sorted(os.listdir(self.BASE_DIR)):
            if folder in ("recycle", "__pycache__") or folder.startswith("."):
                continue
            folder_path = os.path.join(self.BASE_DIR, folder)
            if os.path.isdir(folder_path):
                self.create_folder_section(folder, folder_path)

    def create_folder_section(self, folder_name, folder_path):
        section_frame = ttk.LabelFrame(self.scrollable_frame, text=f"📂 {folder_name}", padding=(10,5))
        section_frame.pack(fill=tk.X, pady=8, padx=5)
        section_frame.configure(style="TLabelframe")
        toggle_btn = ttk.Button(section_frame, text="➖", width=3)
        toggle_btn.pack(side=tk.RIGHT, padx=5, pady=3)
        files_frame = ttk.Frame(section_frame)
        files_frame.pack(fill=tk.X, pady=5)

        def toggle():
            if files_frame.winfo_viewable():
                files_frame.pack_forget()
                toggle_btn.config(text="➕")
            else:
                files_frame.pack(fill=tk.X, pady=5)
                toggle_btn.config(text="➖")
        toggle_btn.config(command=toggle)

        # Files
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path,f))]
        py_files = [f for f in files if f.endswith('.py') and not f.startswith("__")]
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]
        all_files = sorted(py_files) + sorted(pdf_files)
        fixed_width = 25
        cols = 3

        if all_files:
            row, col = 0, 0
            for file in all_files:
                display_text = f"▶ {file}" if file.endswith(".py") else f"📖 {file}"
                truncated = (display_text[:fixed_width-3]+"...") if len(display_text)>fixed_width else display_text
                frame = ttk.Frame(files_frame, relief="groove", padding=4)
                frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

                action_btn = ttk.Button(frame, text="▶" if file.endswith(".py") else "📖", width=3,
                                        command=lambda f=os.path.join(folder_path,file): self.run_file(f) if f.endswith(".py") else self.open_pdf(f))
                action_btn.pack(side=tk.LEFT)
                ToolTip(action_btn, display_text)
                lbl = ttk.Label(frame, text=truncated, width=fixed_width, anchor="w")
                lbl.pack(side=tk.LEFT, padx=5)

                # Edit, Rename, Delete
                ttk.Button(frame, text="✏", width=3, command=lambda f=os.path.join(folder_path,file): self.edit_file(f)).pack(side=tk.LEFT,padx=2)
                ttk.Button(frame, text="✎", width=3, command=lambda f=os.path.join(folder_path,file): self.rename_item(f)).pack(side=tk.LEFT,padx=2)
                ttk.Button(frame, text="🗑", width=3, command=lambda f=os.path.join(folder_path,file): self.delete_item(f)).pack(side=tk.LEFT)

                col += 1
                if col >= cols:
                    col = 0
                    row += 1
        else:
            ttk.Label(files_frame, text="❌ No Python or PDF files", foreground="gray").pack(pady=5)

        # Folder Buttons
        ttk.Button(section_frame, text="✎ Rename", command=lambda: self.rename_item(folder_path)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(section_frame, text="🗑 Delete", command=lambda: self.delete_item(folder_path)).pack(side=tk.RIGHT, padx=5)

    # ---------------------- File/Folder Operations ----------------------
    def rename_item(self, path):
        try:
            new_name = simpledialog.askstring("Rename", f"Enter new name for {os.path.basename(path)}:")
            if new_name:
                new_path = os.path.join(os.path.dirname(path), new_name)
                os.rename(path, new_path)
                self.refresh_view()
                self.status_bar.config(text=f"✎ Renamed to: {new_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot rename:\n{e}")

    def delete_item(self, path):
        try:
            recycle_dir = os.path.join(self.BASE_DIR, "recycle")
            os.makedirs(recycle_dir, exist_ok=True)
            dest = os.path.join(recycle_dir, os.path.basename(path))
            if os.path.exists(dest):
                base, ext = os.path.splitext(os.path.basename(path))
                dest = os.path.join(recycle_dir, f"{base}_copy{ext}")
            shutil.move(path, dest)
            self.refresh_view()
            self.status_bar.config(text=f"🗑 Moved to recycle: {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot delete:\n{e}")

    def add_folder(self):
        folder_name = simpledialog.askstring("Add Folder", "Enter folder name:")
        if folder_name:
            os.makedirs(os.path.join(self.BASE_DIR, folder_name), exist_ok=True)
            self.refresh_view()
            self.status_bar.config(text=f"📁 Created folder: {folder_name}")

    def add_file(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New File")
        add_window.geometry("400x200")
        add_window.configure(bg="#f5f5f5")
        add_window.grab_set()

        ttk.Label(add_window, text="Choose folder:").pack(pady=5)
        folders = [f for f in os.listdir(self.BASE_DIR) if os.path.isdir(os.path.join(self.BASE_DIR,f)) and f!="recycle"]
        folder_combo = ttk.Combobox(add_window, values=folders, state="readonly")
        folder_combo.pack(pady=5)
        if folders: folder_combo.current(0)

        ttk.Label(add_window, text="Enter file name (with extension):").pack(pady=5)
        file_entry = ttk.Entry(add_window, width=30)
        file_entry.pack(pady=5)

        def create_file():
            file_name = file_entry.get()
            folder_name = folder_combo.get()
            if file_name and folder_name:
                file_path = os.path.join(self.BASE_DIR, folder_name, file_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("")
                self.refresh_view()
                self.status_bar.config(text=f"📄 Created file: {file_name} in {folder_name}")
                add_window.destroy()
            else:
                messagebox.showwarning("Warning","Choose folder and enter file name.")
        ttk.Button(add_window, text="✅ Create", style="Add.TButton", command=create_file).pack(pady=10)

    # ---------------------- Run/Edit/Open ----------------------
    def run_file(self, path):
        try:
            self.status_bar.config(text=f"▶ Running: {os.path.basename(path)}")
            if sys.platform.startswith('win'):
                subprocess.Popen(['python', path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(['python3', path], start_new_session=True)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot run file:\n{e}")

    def edit_file(self, path):
        try:
            self.status_bar.config(text=f"✏ Editing: {os.path.basename(path)}")
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot edit file:\n{e}")

    def open_pdf(self, path):
        try:
            self.status_bar.config(text=f"📖 Opening: {os.path.basename(path)}")
            if sys.platform.startswith('win'):
                os.startfile(path)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file:\n{e}")

    # ---------------------- Refresh/Snapshot ----------------------
    def refresh_view(self):
        self.create_sections()
        self.last_snapshot = self.snapshot_project()
        self.status_bar.config(text="🔄 Refreshed view")

    def snapshot_project(self):
        snap = {}
        for folder in os.listdir(self.BASE_DIR):
            folder_path = os.path.join(self.BASE_DIR, folder)
            if os.path.isdir(folder_path):
                snap[folder] = set(os.listdir(folder_path))
        return snap

    def auto_refresh(self):
        current_snapshot = self.snapshot_project()
        if current_snapshot != self.last_snapshot:
            self.refresh_view()
        self.root.after(5000, self.auto_refresh)


# ---------------------- For MainApp Compatibility ----------------------
def main(parent):
    return ProjectExplorer(parent)

App = ProjectExplorer

# ---------------------- Direct Run ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("🚀 Project Explorer")
    root.geometry("980x720")
    app = ProjectExplorer(root)
    root.mainloop()
