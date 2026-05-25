[25.05.2026 21:23] F1: import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# -----------------------------
# Данные
# -----------------------------

books = []
BOOKS_FILE = "books.json"

# -----------------------------
# Сохранение книг
# -----------------------------

def save_books():
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)

# -----------------------------
# Загрузка книг
# -----------------------------

def load_books():
    if os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

            for book in data:
                books.append(book)

                tree.insert(
                    "",
                    tk.END,
                    values=(
                        book["title"],
                        book["author"],
                        book["genre"],
                        book["pages"]
                    )
                )

# -----------------------------
# Добавление книги
# -----------------------------

def add_book():
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()

    # Проверка пустых полей

    if not title or not author or not genre or not pages:
        messagebox.showerror(
            "Ошибка",
            "Все поля должны быть заполнены"
        )
        return

    # Проверка количества страниц

    if not pages.isdigit():
        messagebox.showerror(
            "Ошибка",
            "Количество страниц должно быть числом"
        )
        return

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }

    books.append(book)

    tree.insert(
        "",
        tk.END,
        values=(
            title,
            author,
            genre,
            pages
        )
    )

    save_books()

    clear_entries()

    messagebox.showinfo(
        "Успех",
        "Книга добавлена"
    )

# -----------------------------
# Очистка полей
# -----------------------------

def clear_entries():
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

# -----------------------------
# Фильтрация
# -----------------------------

def filter_books():
    genre_filter = genre_filter_var.get().strip().lower()
    pages_filter = pages_filter_var.get().strip()

    # Очистка таблицы

    for item in tree.get_children():
        tree.delete(item)

    # Вывод подходящих книг

    for book in books:

        # Фильтр по жанру

        genre_match = True

        if genre_filter:
            genre_match = (
                genre_filter in book["genre"].lower()
            )

        # Фильтр по страницам

        pages_match = True

        if pages_filter:
            if pages_filter.isdigit():
                pages_match = (
                    book["pages"] > int(pages_filter)
                )

        if genre_match and pages_match:
            tree.insert(
                "",
                tk.END,
                values=(
                    book["title"],
                    book["author"],
                    book["genre"],
                    book["pages"]
                )
            )

# -----------------------------
# GUI
# -----------------------------

root = tk.Tk()
root.title("Book Tracker")
root.geometry("850x600")

title_label = tk.Label(
    root,
    text="Трекер прочитанных книг",
    font=("Arial", 18)
)

title_label.pack(pady=10)

# -----------------------------
# Форма
# -----------------------------

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

# Название

tk.Label(form_frame, text="Название книги").grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

title_entry = tk.Entry(form_frame, width=30)
title_entry.grid(row=0, column=1)

# Автор

tk.Label(form_frame, text="Автор").grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

author_entry = tk.
[25.05.2026 21:23] F1: Entry(form_frame, width=30)
author_entry.grid(row=1, column=1)

# Жанр

tk.Label(form_frame, text="Жанр").grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

genre_entry = tk.Entry(form_frame, width=30)
genre_entry.grid(row=2, column=1)

# Страницы

tk.Label(form_frame, text="Количество страниц").grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)

pages_entry = tk.Entry(form_frame, width=30)
pages_entry.grid(row=3, column=1)

# -----------------------------
# Кнопка добавления
# -----------------------------

add_button = tk.Button(
    root,
    text="Добавить книгу",
    command=add_book
)

add_button.pack(pady=10)

# -----------------------------
# Фильтрация
# -----------------------------

filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Жанр").grid(
    row=0,
    column=0,
    padx=5
)

genre_filter_var = tk.StringVar()

genre_filter_entry = tk.Entry(
    filter_frame,
    textvariable=genre_filter_var
)

genre_filter_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="Страниц больше").grid(
    row=0,
    column=2,
    padx=5
)

pages_filter_var = tk.StringVar()

pages_filter_entry = tk.Entry(
    filter_frame,
    textvariable=pages_filter_var
)

pages_filter_entry.grid(row=0, column=3)

filter_button = tk.Button(
    filter_frame,
    text="Фильтровать",
    command=filter_books
)

filter_button.grid(row=0, column=4, padx=10)

# -----------------------------
# Таблица
# -----------------------------

columns = (
    "title",
    "author",
    "genre",
    "pages"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

tree.heading("title", text="Название")
tree.heading("author", text="Автор")
tree.heading("genre", text="Жанр")
tree.heading("pages", text="Страницы")

tree.column("title", width=250)
tree.column("author", width=180)
tree.column("genre", width=150)
tree.column("pages", width=100)

tree.pack(pady=10)

# -----------------------------
# Загрузка данных
# -----------------------------

load_books()

root.mainloop()