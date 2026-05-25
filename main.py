grid(row=0, column=1)

to_menu = ttk.Combobox(
    frame,
    textvariable=to_var,
    values=currencies,
    state="readonly",
    width=10
)

to_menu.grid(row=0, column=2, padx=10)

# -----------------------------
# Кнопка
# -----------------------------

convert_button = tk.Button(
    root,
    text="Конвертировать",
    command=convert_currency
)

convert_button.pack(pady=10)

# -----------------------------
# Результат
# -----------------------------

result_label = tk.Label(
    root,
    text="Введите данные",
    font=("Arial", 14)
)

result_label.pack(pady=10)

# -----------------------------
# История
# -----------------------------

history_label = tk.Label(
    root,
    text="История конвертаций",
    font=("Arial", 12)
)

history_label.pack(pady=5)

columns = ("time", "from", "to", "amount", "result")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=10
)

tree.heading("time", text="Время")
tree.heading("from", text="Из")
tree.heading("to", text="В")
tree.heading("amount", text="Сумма")
tree.heading("result", text="Результат")

tree.column("time", width=180)
tree.column("from", width=80)
tree.column("to", width=80)
tree.column("amount", width=100)
tree.column("result", width=120)

tree.pack(pady=10)

# -----------------------------
# Загрузка истории
# -----------------------------

load_history()

root.mainloop()