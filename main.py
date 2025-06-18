import os
import json
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

CONFIG_FILE = 'user_agents.json'
VDF_FILENAME = 'shortcuts.vdf'


def load_user_agents():
    if os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror('Error', f'Invalid JSON in {CONFIG_FILE}')
    return {
        "Default": "Mozilla/5.0 (X11; Linux x86_64; SteamOS)"
    }


def detect_flatpak(browser):
    try:
        subprocess.run(['flatpak', 'info', browser], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def generate_app_id(url, title):
    import zlib
    key = f'{url}\0{title}'.encode('utf-8')
    return zlib.crc32(key) | 0x80000000


class ShortcutManager:
    def __init__(self):
        self.shortcuts = []

    def add_shortcut(self, title, url, browser, user_agent=None):
        entry = {
            'title': title,
            'url': url,
            'browser': browser,
            'user_agent': user_agent,
            'appid': generate_app_id(url, title),
        }
        self.shortcuts.append(entry)

    def remove(self, index):
        if 0 <= index < len(self.shortcuts):
            self.shortcuts.pop(index)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Steam Shortcut Automation Program')
        self.geometry('900x480')
        self.mgr = ShortcutManager()
        self.user_agents = load_user_agents()
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        self.shortcut_frame = ttk.Frame(notebook)
        self.config_frame = ttk.Frame(notebook)
        self.about_frame = ttk.Frame(notebook)

        notebook.add(self.shortcut_frame, text='Shortcuts')
        notebook.add(self.config_frame, text='Config')
        notebook.add(self.about_frame, text='About')

        self.build_shortcuts_tab()
        self.build_about_tab()

    def build_shortcuts_tab(self):
        frame = self.shortcut_frame
        self.listbox = tk.Listbox(frame, width=60)
        self.listbox.pack(side='left', fill='y', padx=5, pady=5)

        form = ttk.Frame(frame)
        form.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        ttk.Label(form, text='Title').grid(row=0, column=0, sticky='w')
        self.title_var = tk.StringVar()
        title_entry = ttk.Entry(form, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky='ew')
        ttk.Button(form, text='Paste', command=lambda: self.paste_clipboard(self.title_var)).grid(row=0, column=2, padx=2)

        ttk.Label(form, text='URL').grid(row=1, column=0, sticky='w')
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(form, textvariable=self.url_var)
        url_entry.grid(row=1, column=1, sticky='ew')
        ttk.Button(form, text='Paste', command=lambda: self.paste_clipboard(self.url_var)).grid(row=1, column=2, padx=2)

        ttk.Label(form, text='Browser').grid(row=2, column=0, sticky='w')
        self.browser_var = tk.StringVar(value='Chrome')
        ttk.Combobox(form, textvariable=self.browser_var, values=['Chrome', 'Edge', 'Firefox']).grid(row=2, column=1, sticky='ew')

        self.ua_enabled = tk.BooleanVar()
        ua_check = ttk.Checkbutton(form, text='Use User-Agent', variable=self.ua_enabled, command=self.toggle_ua)
        ua_check.grid(row=3, column=0, sticky='w')

        self.ua_var = tk.StringVar()
        self.ua_combo = ttk.Combobox(form, textvariable=self.ua_var, state='disabled', values=list(self.user_agents.keys()))
        self.ua_combo.grid(row=3, column=1, sticky='ew')

        add_btn = ttk.Button(form, text='Add Shortcut', command=self.add_shortcut)
        add_btn.grid(row=4, column=0, columnspan=3, pady=5)

        form.columnconfigure(1, weight=1)

    def build_about_tab(self):
        ttk.Label(self.about_frame, text='Steam Shortcut Automation Program').pack(pady=10)
        ttk.Label(self.about_frame, text='GitHub: https://github.com/example/steamsap').pack()

    def toggle_ua(self):
        state = 'normal' if self.ua_enabled.get() else 'disabled'
        self.ua_combo.configure(state=state)

    def paste_clipboard(self, variable):
        try:
            variable.set(self.clipboard_get())
        except tk.TclError:
            pass

    def add_shortcut(self):
        title = self.title_var.get().strip()
        url = self.url_var.get().strip()
        browser = self.browser_var.get()
        ua = self.user_agents.get(self.ua_var.get()) if self.ua_enabled.get() else None

        if not title or not url:
            messagebox.showerror('Error', 'Title and URL are required.')
            return

        self.mgr.add_shortcut(title, url, browser, ua)
        self.listbox.insert('end', f'[{browser}] "{title}" {url}')
        self.title_var.set('')
        self.url_var.set('')


if __name__ == '__main__':
    app = App()
    app.mainloop()
