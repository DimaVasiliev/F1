[25.05.2026 21:13] F1: import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# ----------------------------
# Предопределённые задачи
# ----------------------------

tasks = [
    {"task": "Прочитать статью", "type": "Учёба"},
    {"task": "Сделать зарядку", "type": "Спорт"},
    {"task": "Написать отчёт", "type": "Работа"},
    {"task": "Изучить Python", "type": "Учёба"},
    {"task": "Пробежать 2 км", "type": "Спорт"},
]

history = []

TASKS_FILE = "tasks.json"
HISTORY_FILE = "history.json"

# ----------------------------
# Загрузка данных
# ----------------------------

def load_tasks():
    global tasks

    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)

def load_history():
    global history

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

            for item in history:
                history_listbox.insert(tk.END, item)

# ----------------------------
# Сохранение данных
# ----------------------------

def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)

def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# ----------------------------
# Генерация задачи
# ----------------------------

def generate_task():
    selected_type = filter_var.get()

    filtered_tasks = tasks

    if selected_type != "Все":
        filtered_tasks = [
            task for task in tasks
            if task["type"] == selected_type
        ]

    if not filtered_tasks:
        messagebox.showwarning("Ошибка", "Нет задач данного типа")
        return

    task = random.choice(filtered_tasks)

    result_label.config(
        text=f'{task["task"]} ({task["type"]})'
    )

    history_entry = f'{task["task"]} ({task["type"]})'

    history.append(history_entry)
    history_listbox.insert(tk.END, history_entry)

    save_history()

# ----------------------------
# Добавление новой задачи
# ----------------------------

def add_task():
    task_text = task_entry.get().strip()
    task_type = type_var.get()

    if task_text == "":
        messagebox.showerror(
            "Ошибка",
            "Задача не может быть пустой"
        )
        return

    new_task = {
        "task": task_text,
        "type": task_type
    }

    tasks.append(new_task)

    save_tasks()

    messagebox.showinfo(
        "Успех",
        "Задача добавлена"
    )

    task_entry.delete(0, tk.END)

# ----------------------------
# GUI
# ----------------------------

root = tk.Tk()
root.title("Random Task Generator")
root.geometry("500x500")

title_label = tk.Label(
    root,
    text="Генератор случайных задач",
    font=("Arial", 16)
)

title_label.pack(pady=10)

# Фильтр

filter_var = tk.StringVar(value="Все")

filter_label = tk.Label(root, text="Фильтр:")
filter_label.pack()

filter_menu = tk.OptionMenu(
    root,
    filter_var,
    "Все",
    "Учёба",
    "Спорт",
    "Работа"
)

filter_menu.pack()

# Кнопка генерации

generate_button = tk.Button(
    root,
    text="Сгенерировать задачу",
    command=generate_task
)

generate_button.pack(pady=10)

# Результат

result_label = tk.Label(
    root,
    text="Нажмите кнопку",
    font=("Arial", 14)
)

result_label.pack(pady=10)

# История

history_label = tk.Label(root, text="История:")
history_label.pack()

history_listbox = tk.Listbox(root, width=50, height=10)
history_listbox.pack(pady=5)

# Добавление новой задачи

add_label = tk.Label(root, text="Добавить новую задачу")
add_label.pack(pady=10)

task_entry = tk.Entry(root, width=40)
task_entry.pack()

type_var = tk.StringVar(value="Учёба")

type_menu = tk.OptionMenu(
    root,
    type_var,
    "Учёба",
    "Спорт",
    "Работа"
)

type_menu.pack(pady=5)

add_button = tk.Button(
    root,
    text="Добавить задачу",
    command=add_task
)

add_button.pack()

# Загрузка данных

load_tasks()
[25.05.2026 21:13] F1: load_history()

root.mainloop()