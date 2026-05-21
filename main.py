import tkinter as tk
from tkinter import ttk, messagebox
from generator import generate_password
from storage import load_history, save_history
from validation import validate_settings
from datetime import datetime


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("700x500")

        self.history = load_history()

        self.length_var = tk.IntVar(value=12)

        self.letters_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        self.create_widgets()
        self.load_table()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="Генератор случайных паролей",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Длина пароля").grid(row=0, column=0)

        self.scale = tk.Scale(
            frame,
            from_=4,
            to=64,
            orient=tk.HORIZONTAL,
            variable=self.length_var
        )
        self.scale.grid(row=0, column=1)

        tk.Checkbutton(
            frame,
            text="Буквы",
            variable=self.letters_var
        ).grid(row=1, column=0, sticky="w")

        tk.Checkbutton(
            frame,
            text="Цифры",
            variable=self.digits_var
        ).grid(row=2, column=0, sticky="w")

        tk.Checkbutton(
            frame,
            text="Специальные символы",
            variable=self.symbols_var
        ).grid(row=3, column=0, sticky="w")

        generate_btn = tk.Button(
            self.root,
            text="Создать пароль",
            command=self.generate
        )
        generate_btn.pack(pady=10)

        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 14),
            justify="center",
            width=40
        )
        self.password_entry.pack(pady=10)

        copy_btn = tk.Button(
            self.root,
            text="Скопировать пароль",
            command=self.copy_password
        )
        copy_btn.pack()

        columns = ("password", "length", "date")

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=10
        )

        self.tree.heading("password", text="Password")
        self.tree.heading("length", text="Length")
        self.tree.heading("date", text="Created At")

        self.tree.pack(fill="both", expand=True, pady=10)

        clear_btn = tk.Button(
            self.root,
            text="Очистить историю",
            command=self.clear_history
        )
        clear_btn.pack(pady=5)

    def generate(self):
        length = self.length_var.get()

        letters = self.letters_var.get()
        digits = self.digits_var.get()
        symbols = self.symbols_var.get()

        try:
            validate_settings(length, letters, digits, symbols)

            password = generate_password(
                length,
                letters,
                digits,
                symbols
            )

            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            record = {
                "password": password,
                "length": length,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            self.history.append(record)

            save_history(self.history)

            self.tree.insert(
                "",
                tk.END,
                values=(
                    record["password"],
                    record["length"],
                    record["created_at"]
                )
            )

        except ValueError as error:
            messagebox.showerror("Validation Error", str(error))

    def copy_password(self):
        password = self.password_entry.get()

        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)

            messagebox.showinfo(
                "Скопировано",
                "Пароль скопирован в буфер обмена"
            )

    def load_table(self):
        for item in self.history:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    item["password"],
                    item["length"],
                    item["created_at"]
                )
            )

    def clear_history(self):
        self.history = []

        save_history(self.history)

        for item in self.tree.get_children():
            self.tree.delete(item)


root = tk.Tk()
app = PasswordGeneratorApp(root)
root.mainloop()