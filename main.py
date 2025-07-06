import subprocess
import threading
import customtkinter as ctk
from tkinter import ttk
import random
import json
from datetime import datetime

COLUMNS = ["Type", "IP", "MAC", "Port", "Protocol", "IPV4", "IPV6", "Location"]

COLOR_MAP = {
    "IP": "#4FC3F7",
    "MAC": "#81C784",
    "Port": "#FFD54F",
    "Protocol": "#FF8A65",
    "Type": "#BA68C8",
}

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x640")
        self.root.title("NetProbe")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.frame = ctk.CTkFrame(self.root, fg_color="#181A1B", corner_radius=16)
        self.frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1E1E1E",
                        foreground="white",
                        fieldbackground="#1E1E1E",
                        rowheight=36,
                        font=("Segoe UI", 13),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background="#292B2C",
                        foreground="#4FC3F7",
                        font=("Segoe UI", 14, "bold"),
                        borderwidth=0)
        style.map("Treeview", background=[("selected", "#333")])

        self.tree = ttk.Treeview(self.frame, columns=COLUMNS, show="headings", selectmode="browse")
        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(fill="both", expand=True, side="left", padx=(0, 5), pady=10)

        scrollbar = ctk.CTkScrollbar(self.frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", pady=10)

        for tag, color in COLOR_MAP.items():
            self.tree.tag_configure(tag, foreground=color)

        self.status_label = ctk.CTkLabel(self.root, text="", text_color="gray", font=("Segoe UI", 12, "italic"))
        self.status_label.pack(pady=(0, 4))

        self.scan_btn = ctk.CTkButton(self.root,
                                      text="🔍 Scan Network",
                                      command=self.start_scan_thread,
                                      fg_color="#4FC3F7",
                                      hover_color="#2196F3",
                                      text_color="black",
                                      font=("Segoe UI", 15, "bold"),
                                      corner_radius=16,
                                      height=46,
                                      width=220)
        self.scan_btn.pack(pady=(0, 20))

        self.save_btn = ctk.CTkButton(self.root,
                                      text="💾 Save to JSON",
                                      command=self.save_to_json,
                                      fg_color="#81C784",
                                      hover_color="#388E3C",
                                      text_color="black",
                                      font=("Segoe UI", 14, "bold"),
                                      corner_radius=14,
                                      height=40,
                                      width=180)
        self.save_btn.pack(pady=(0, 10))

        self.devices_data = []

    def start_scan_thread(self):
        self.status_label.configure(text="⏳ Scanning network...")
        self.scan_btn.configure(state="disabled")
        threading.Thread(target=self.scan_network, daemon=True).start()

    def scan_network(self):
        try:
            result = subprocess.run(['ruby', 'lib/opmized.rb'], capture_output=True, text=True)
            lines = result.stdout.strip().splitlines()
            if not lines or len(lines) < 2:
                self.status_label.configure(text="⚠️ No data or script error.")
                return

            self.tree.delete(*self.tree.get_children())
            self.devices_data = []

            for row in lines[1:]:
                device_type = random.choice(["Router", "Hotspot", "Bluetooth"])
                values = [device_type] + row.split(",")
                device_info = dict(zip(COLUMNS, values))
                self.devices_data.append(device_info)
                tags = [col for col in COLUMNS if col in COLOR_MAP]
                self.tree.insert("", "end", values=values, tags=tags)

            self.status_label.configure(text="✅ Scan complete.")
        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)}")
        finally:
            self.scan_btn.configure(state="normal")

    def save_to_json(self):
        try:
            filename = f"scan_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(self.devices_data, f, indent=4)
            self.status_label.configure(text=f"✅ Saved to {filename}")
        except Exception as e:
            self.status_label.configure(text=f"❌ Save failed: {str(e)}")

if __name__ == "__main__":
    app = ctk.CTk()
    MainApp(app)
    app.mainloop()
# File: lib/opmized.rb
