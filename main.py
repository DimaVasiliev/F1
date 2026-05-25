import json
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

# Имя файла для сохранения истории и задач
DATA_FILE = "tasks_data.json"

# Предопределенный список задач по категориям
DEFAULT_DATA = {
    "tasks": [
        {"text": "Прочитать научную статью", "category": "Учёба"},
        {"text": "Выучить 5 новых иностранных слов", "category": "Учёба"},
        {"text": "Сделать 20 приседаний", "category": "Спорт"},
        {"text": "Пробежка или интенсивная растяжка", "category": "Спорт"},
        {"text": "Разобрать электронную почту", "category": "Работа"},
        {"text": "Составить план задач на завтра", "category": "Работа"},
    ],
    "history": [],
}


class RandomTaskApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("550x600")

        self.load_data()
        self.create_widgets()
        self.update_history_listbox()

    def load_data(self):
        """Загрузка данных из JSON или создание дефолтных"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = DEFAULT_DATA.copy()
        else:
            self.data = DEFAULT_DATA.copy()

    def save_data(self):
        """Сохранение данных в JSON"""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def create_widgets(self):
        # --- СЕКЦИЯ 1: ГЕНЕРАЦИЯ ---
        gen_frame = tk.LabelFrame(self.root, text="Генератор", padding=10)
        gen_frame.pack(fill="x", padx=10, top=10)

        self.btn_generate = tk.Button(
            gen_frame,
            text="Сгенерировать задачу",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.generate_task,
        )
        self.btn_generate.pack(fill="x", pady=5)

        self.lbl_result = tk.Label(
            gen_frame,
            text="Нажмите кнопку для выбора задачи",
            font=("Arial", 12, "italic"),
            wraplength=500,
            fg="#333",
        )
        self.lbl_result.pack(pady=10)

        # --- СЕКЦИЯ 2: ДОБАВЛЕНИЕ НОВОЙ ЗАДАЧИ ---
        add_frame = tk.LabelFrame(self.root, text="Добавить свою задачу", padding=10)
        add_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(add_frame, text="Текст задачи:").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.entry_task = tk.Entry(add_frame, width=30)
        self.entry_task.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Категория:").grid(
            row=1, column=0, sticky="w", padx=5
        )
        self.combo_category = ttk.Combobox(
            add_frame, values=["Учёба", "Спорт", "Работа"], state="readonly"
        )
        self.combo_category.current(0)
        self.combo_category.grid(row=1, column=1, padx=5, pady=5)

        btn_add = tk.Button(
            add_frame, text="Добавить", bg="#2196F3", fg="white", command=self.add_task
        )
        btn_add.grid(row=0, column=2, rowspan=2, padx=10, sticky="nsew")

        # --- СЕКЦИЯ 3: ИСТОРИЯ И ФИЛЬТР ---
        history_frame = tk.LabelFrame(self.root, text="История задач", padding=10)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Фильтр
        filter_frame = tk.Frame(history_frame)
        filter_frame.pack(fill="x", pady=5)

        tk.Label(filter_frame, text="Фильтр по типу:").pack(side="left", padx=5)
        self.combo_filter = ttk.Combobox(
            filter_frame,
            values=["Все", "Учёба", "Спорт", "Работа"],
            state="readonly",
            width=15,
        )
        self.combo_filter.current(0)
        self.combo_filter.pack(side="left", padx=5)
        self.combo_filter.bind("<<ComboboxSelected>>", lambda e: self.update_history_listbox())

        # Список с прокруткой
        list_frame = tk.Frame(history_frame)
        list_frame.pack(fill="both", expand=True, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox_history = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set, font=("Arial", 10)
        )
        self.listbox_history.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=self.listbox_history.yview)

        # Кнопка очистки истории
        btn_clear = tk.Button(
            history_frame,
            text="Очистить историю",
            bg="#f44336",
            fg="white",
            command=self.clear_history,
        )
        btn_clear.pack(anchor="e", pady=5)

    def generate_task(self):
        """Выбор случайной задачи и добавление в историю"""
        available_tasks = self.data.get("tasks", [])

        if not available_tasks:
            messagebox.showwarning("Внимание", "Список задач пуст! Добавьте новые задачи.")
            return

        selected = random.choice(available_tasks)
        task_text = selected["text"]
        task_cat = selected["category"]

        # Отображаем на экране
        self.lbl_result.config(text=f"[{task_cat}] {task_text}", fg="black")

        # Добавляем в историю
        self.data["history"].append(selected)
        self.save_data()
        self.update_history_listbox()

    def add_task(self):
        """Добавление кастомной задачи с валидацией"""
        text = self.entry_task.get().strip()
        category = self.combo_category.get()

        # Валидация: проверка на пустую строку
        if not text:
            messagebox.showwarning("Ошибка ввода", "Поле задачи не может быть пустым!")
            return

        new_task = {"text": text, "category": category}
        self.data["tasks"].append(new_task)
        self.save_data()

        self.entry_task.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача успешно добавлена в категорию '{category}'!")

    def update_history_listbox(self):
        """Обновление списка истории с учетом выбранного фильтра"""
        self.listbox_history.delete(0, tk.END)
        filter_val = self.combo_filter.get()

        for item in reversed(self.data.get("history", [])):
            if filter_val == "Все" or item["category"] == filter_val:
                self.listbox_history.insert(
                    tk.END, f" [{item['category']}] {item['text']}"
                )

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.data["history"] = []
            self.save_data()
            self.update_history_listbox()
            self.lbl_result.config(
                text="Нажмите кнопку для выбора задачи", fg="#333"
            )


if __name__ == "__main__":
    root = tk.Tk()
    # Поддержка padding в ttk.LabelFrame для старых версий Python
    from tkinter import messagebox, ttk

    app = RandomTaskApp(root)
    root.mainloop()