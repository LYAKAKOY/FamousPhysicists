import io
import tkinter as tk
import sqlite3 as sq
from tkinter import ttk, messagebox, filedialog

DB_NAME = "Russian's_Physicists.db"
image_physicist = None
image_physicist_refactor = None


def show_modal_window(self):
    modal_window = tk.Toplevel(name='modal_window')
    self.pack_window(modal_window)
    modal_window.resizable(False, False)
    modal_window.title("О программе")
    # image = Image.open('!.jpeg')
    # image = image.resize((40, 40))
    # picture = ImageTk.PhotoImage(image)
    image_label = tk.Label(modal_window, font=("Arial", 40), padx=10, pady=10, image=picture)
    image_label.grid(row=0, column=0, padx=5, pady=5)
    label_text = tk.Label(modal_window, text="База данных 'Знаменитые физики России'\n"
                                             "(c) Gusenkov S.A., Russia, 2023\n", padx=10, pady=10)
    label_text.grid(row=0, column=1, padx=5, pady=5)

    close_button = ttk.Button(modal_window, text="Ок", style="Close.TButton", command=modal_window.destroy)
    close_button.grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)

    modal_window.transient(master=self.root)
    modal_window.grab_set()
    modal_window.focus_set()
    self.root.wait_window(modal_window)


def help_window(self):
    window = tk.Toplevel(name='help_window')
    window.title("Справка")
    window.geometry(f"400x200")
    self.pack_window(window)
    window.resizable(False, False)

    text = "База данных 'Известные физики России'\n" \
           "Позволяет: добавлять/ изменять/ удалять информацию.\n" \
           "Клавиши программы:\n" \
           "F1-вызов справки по программе,\n" \
           "F2-добавить в базу данных,\n" \
           "F3-удалить из базы данных,\n" \
           "F4-изменить запись в базе данных,\n" \
           "F10-меню программы"

    label = tk.Label(window, text=text, font=("Arial", 10))
    label.pack(padx=20, pady=10)

    close_button = ttk.Button(window, text="Закрыть", style="Close.TButton", command=window.destroy)
    close_button.pack(side=tk.RIGHT, padx=20, pady=0)


def on_select(event):
    try:
        widget = event.widget
        selection = widget.curselection()
        fio = widget.get(selection)
        with sq.connect(DB_NAME) as connection:
            cur = connection.cursor()
            image_url, description = cur.execute("SELECT picture, description FROM physicists WHERE fio = ?",
                                                 (fio,)).fetchone()

    except tk.TclError as e:
        print(e)
    else:
        photo = io.BytesIO(image_url)
        picture = tk.PhotoImage(data=photo.getvalue())
        picture = picture.subsample(3)
        image_field.configure(image=picture)
        image_field.image = picture
        text_field.configure(state="normal")
        text_field.delete(1.0, tk.END)
        text_field.insert(tk.END, description)
        text_field.configure(state="disabled")


def get_list_of_physicists():
    try:
        with sq.connect(DB_NAME) as connection:
            cur = connection.cursor()
            data = cur.execute("SELECT fio FROM physicists ORDER BY fio").fetchall()
            list_of_physicists = [physicist[0] for physicist in data]
            return list_of_physicists

    except sq.OperationalError:
        tk.messagebox.showerror('Ошибка', 'Нет подключения к базе данных')
        root.destroy()


def check_image(type_image):
    global image_physicist, image_physicist_refactor
    if type_image:
        image_url = image_physicist
    else:
        image_url = image_physicist_refactor
    if image_url is not None:
        with open(image_url, 'rb') as image_file:
            image_data = image_file.read()
    else:
        with open('default.png', 'rb') as image_file:
            image_data = image_file.read()
    return image_data


def update_list_box():
    list_box.delete(0, tk.END)
    list_of_physicists = get_list_of_physicists()
    for el in list_of_physicists:
        list_box.insert(tk.END, el)


def open_file_dialog(master, field):
    global image_physicist, image_physicist_refactor
    file_path = filedialog.askopenfilename(parent=master, filetypes=[("Image files", "*.png")])
    if file_path:
        if field.winfo_name() == 'image_save':
            image_physicist = file_path
        else:
            image_physicist_refactor = file_path
        picture = tk.PhotoImage(file=file_path)
        picture = picture.subsample(6)
        field.configure(image=picture)
        field.image = picture


def delete_picture_of_physicist(field):
    global image_physicist, image_physicist_refactor
    if field.winfo_name() == 'image_save':
        image_physicist = None
    else:
        image_physicist_refactor = None
    photo = tk.PhotoImage(file='default.png')
    photo = photo.subsample(8)
    field.configure(image=photo)
    field.image = photo


def hide_text_info(field, text_info):
    if field.get() == text_info:
        field.delete(0, 'end')
        field.configure(foreground='black')


def set_text_info(field, text_info):
    if not field.get():
        field.insert(0, text_info)
        field.configure(foreground="#999")


def clear_entry_text(event):
    field = event.widget
    if field.get(0.1, tk.END).strip() == "Введите информацию о физике...":
        field.delete(1.0, tk.END)
        field.configure(foreground='black')


def set_hint_text(event):
    field = event.widget
    if not field.get(1.0, tk.END).strip():
        field.insert(0.1, "Введите информацию о физике...")
        field.configure(foreground="#999")


def refactor_physicist():
    def update_data():
        global image_physicist_refactor
        name_of_physicist = physicist_name_entry_refactor.get()
        if combo_box.current() == 0:
            return
        else:
            name_update = list_of_physicists[combo_box.current() - 1]
        if name_of_physicist in ('', "Введите фио физика..."):
            tk.messagebox.showerror("Ошибка", "Обязательное поле: фио физика")
        else:
            try:
                with sq.connect(DB_NAME) as con:
                    cur = con.cursor()

                    text_about_physicist = text_field_about_physicist_refactor.get(1.0, tk.END)
                    if text_about_physicist.strip() == 'Введите информацию о физике...':
                        text_about_physicist = 'Нет информации'
                    if image_physicist_refactor is None or image_physicist_refactor == 'default.png':
                        cur.execute("UPDATE physicists SET fio = ?, description = ? WHERE fio = ? ",
                                    (name_of_physicist,
                                     text_about_physicist, name_update))
                    else:
                        image_data = check_image(0)
                        cur.execute("UPDATE physicists SET fio = ?, picture = ?, description = ? WHERE fio = ? ",
                                    (name_of_physicist, image_data,
                                     text_about_physicist, name_update))
            except sq.OperationalError:
                tk.messagebox.showerror('Ошибка', 'Нет подключения к базе данных')
                refactor_form.focus_set()
            except sq.IntegrityError:
                tk.messagebox.showerror('Ошибка', f'Физик с фио {name_of_physicist} уже существует в базе данных')
                refactor_form.focus_set()
            else:
                update_list_box()
                messagebox.showinfo('Результат', 'Изменения успешно применены')
                refactor_form.destroy()

    def selected(event):
        if combo_box.current() == 0:
            return
        box = event.widget
        name = box.get()
        try:
            with sq.connect(DB_NAME) as connection:
                cur = connection.cursor()
                image_url, description = cur.execute("SELECT picture, description FROM physicists WHERE name = ?",
                                                     (name,)).fetchone()
        except sq.OperationalError:
            tk.messagebox.showerror('Ошибка', 'Нет подключения к базе данных')
        else:
            photo = io.BytesIO(image_url)
            picture = tk.PhotoImage(data=photo.getvalue())
            picture = picture.subsample(8)
            refactor_file_button.configure(image=picture)
            refactor_file_button.image = picture
            physicist_name_entry_refactor.delete(0, tk.END)
            physicist_name_entry_refactor.insert(0, name)
            physicist_name_entry_refactor.configure(foreground='black')
            text_field_about_physicist_refactor.delete(1.0, tk.END)
            text_field_about_physicist_refactor.insert(tk.END, description)
            text_field_about_physicist_refactor.configure(foreground='black')

    refactor_form = tk.Toplevel(name='refactor_window')
    refactor_form.title("Ввод информации о физике")
    refactor_form.resizable(False, False)

    photo = tk.PhotoImage(file='default.png')
    photo = photo.subsample(8)

    refactor_file_button = ttk.Button(refactor_form, text="Обзор...",
                                      command=lambda: open_file_dialog(refactor_form, refactor_file_button),
                                      image=photo,
                                      name='image_refactor')
    refactor_file_button.image = photo
    refactor_file_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    delete_picture = ttk.Button(refactor_form, text="\u2715",
                                command=lambda: delete_picture_of_physicist(refactor_file_button),
                                width=2)
    delete_picture.grid(row=0, column=1, padx=50, pady=10, sticky=tk.NW)

    combo_box = ttk.Combobox(refactor_form, values=['Выберите физика'] + list_of_physicists, state="readonly",
                             width=10,
                             foreground='gray')
    combo_box.current(0)
    combo_box.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)
    combo_box.bind("<<ComboboxSelected>>", selected)

    physicist_name_entry_refactor = ttk.Entry(refactor_form, width=20)
    physicist_name_entry_refactor.configure(foreground="#999")
    physicist_name_entry_refactor.insert(0, "Введите фио физика...")
    physicist_name_entry_refactor.bind("<FocusIn>", lambda event: hide_text_info(event.widget, "Введите фио "
                                                                                               "физика..."))
    physicist_name_entry_refactor.bind('<FocusOut>', lambda event: set_text_info(event.widget, "Введите фио "
                                                                                               "физика..."))
    physicist_name_entry_refactor.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

    text_field_about_physicist_refactor = tk.Text(refactor_form, width=45, height=5)
    text_field_about_physicist_refactor.configure(foreground='#999')
    text_field_about_physicist_refactor.insert(0.1, "Введите информацию о физике...")
    text_field_about_physicist_refactor.bind("<Control-c>", lambda event: text_field.event_generate("<<Copy>>"))
    text_field_about_physicist_refactor.bind("<FocusIn>", clear_entry_text)
    text_field_about_physicist_refactor.bind('<FocusOut>', set_hint_text)
    text_field_about_physicist_refactor.grid(row=2, column=0, columnspan=2, sticky=tk.S)

    save_button = ttk.Button(refactor_form, text="Сохранить", command=update_data, width=25)
    save_button.grid(row=4, column=0, pady=10)

    cancel_button = ttk.Button(refactor_form, text="Отмена", command=refactor_form.destroy, width=25)
    cancel_button.grid(row=4, column=1, pady=10)


def add_physicist():
    def save_data():
        name_of_physicist = physicist_name_entry.get()
        if name_of_physicist in ('', "Введите фио физика..."):
            tk.messagebox.showerror("Ошибка", "Обязательное поле: фио физика")
            return
        else:
            try:
                with sq.connect(DB_NAME) as con:
                    cur = con.cursor()
                    image_data = check_image(1)
                    text_about_physicist = text_field_about_physicist.get(1.0, tk.END)
                    if text_about_physicist.strip() == 'Введите информацию о физике...':
                        text_about_physicist = 'Нет информации'
                    cur.execute("INSERT INTO physicists (fio, picture, description) VALUES (?, ?, ?) ",
                                (name_of_physicist, image_data,
                                 text_about_physicist))
            except sq.OperationalError as e:
                print(e)
                tk.messagebox.showerror('Ошибка', 'Нет подключения к базе данных')
                add_form.focus_set()
            except sq.IntegrityError as e:
                print(e)
                tk.messagebox.showerror('Ошибка', f'Физик с фио: {name_of_physicist} уже существует в базе данных')
                add_form.focus_set()
            else:
                update_list_box()
                messagebox.showinfo('Результат', 'Физик успешно добавлен в базу')
                add_form.destroy()

    add_form = tk.Toplevel(name='add_window')
    add_form.geometry("370x350")
    add_form.title("Ввод информации о физике")
    add_form.resizable(False, False)

    photo = tk.PhotoImage(file='default.png')
    photo = photo.subsample(8)
    open_file_button = ttk.Button(add_form, text="Обзор...",
                                  command=lambda: open_file_dialog(add_form, open_file_button),
                                  image=photo,
                                  name='image_save')
    open_file_button.image = photo
    open_file_button.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    delete_image = ttk.Button(add_form, text="\u2715",
                              command=lambda: delete_picture_of_physicist(open_file_button),
                              width=2)
    delete_image.grid(row=0, column=1, padx=50, pady=10, sticky=tk.NW)

    physicist_name_entry = ttk.Entry(add_form, width=20)
    physicist_name_entry.configure(foreground="#999")
    physicist_name_entry.insert(0, "Введите фио физика...")
    physicist_name_entry.bind("<FocusIn>", lambda event: hide_text_info(event.widget, "Введите фио физика..."))
    physicist_name_entry.bind('<FocusOut>', lambda event: set_text_info(event.widget, "Введите фио физика..."))
    physicist_name_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

    text_field_about_physicist = tk.Text(add_form, width=45, height=5)
    text_field_about_physicist.configure(foreground='#999')
    text_field_about_physicist.insert(0.1, "Введите информацию о физике...")
    text_field_about_physicist.bind("<Control-c>", lambda event: text_field.event_generate("<<Copy>>"))
    text_field_about_physicist.bind("<FocusIn>", clear_entry_text)
    text_field_about_physicist.bind('<FocusOut>', set_hint_text)
    text_field_about_physicist.grid(row=2, column=0, columnspan=2, sticky=tk.S)

    save_button = ttk.Button(add_form, text="Сохранить", command=save_data, width=25)
    save_button.grid(row=4, column=0, pady=10)

    cancel_button = ttk.Button(add_form, text="Отмена", command=add_form.destroy, width=25)
    cancel_button.grid(row=4, column=1, pady=10)


root = tk.Tk()
style = ttk.Style()
width = 700
height = 400

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f"{width}x{height}+{x}+{y}")
root.title("Знаменитые физики России")
style.configure("Close.TButton")

list_box = tk.Listbox(root, selectmode=tk.SINGLE, font=('Arial', 12))
list_of_physicists = get_list_of_physicists()
for option in list_of_physicists:
    list_box.insert(tk.END, option)
style.configure('Search.TEntry', foreground='grey')
list_box.grid(row=0, column=0, sticky=tk.NS + tk.EW)
list_box.configure(selectbackground=list_box.cget('background'), selectforeground='gray')
list_box.bind("<<ListboxSelect>>", on_select)

# IMAGE
image = None
image_field = tk.Label(root)
image_field.grid(row=0, column=1, sticky="nsew")

# TEXT
text_field = tk.Text(root, wrap=tk.WORD)
text_field.grid(row=0, column=2, sticky=tk.NS + tk.EW)
text_field.configure(state="disabled")

root.rowconfigure(0, weight=1, uniform="row")
root.columnconfigure(0, weight=20, uniform="column")
root.columnconfigure(1, weight=55, uniform="column")
root.columnconfigure(2, weight=25, uniform="column")

# MENU1
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Фонд", menu=file_menu)
# file_menu.add_command(label="Найти...", command=search_lake)
file_menu.add_separator()
file_menu.add_command(label="Добавить F2", command=add_physicist)
root.bind("<F2>", lambda event: add_physicist())
# file_menu.add_command(label="Удалить F3", command=delete_lake_window)
# root.bind("<F3>", lambda event: delete_lake_window())
# file_menu.add_command(label="Выйти F4", command=self.root.quit)
root.bind("<F4>", lambda event: refactor_physicist())
# root.bind("<F10>", lambda event: file_menu.post(event.x_root, event.y_root))
#
# # Menu2
file_menu2 = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справка", menu=file_menu2)
file_menu2.add_command(label="Содержание", command=help_window)
root.bind("<F1>", lambda event: help_window())
file_menu2.add_separator()
file_menu2.add_command(label="О программе", command=show_modal_window)

root.config(menu=menu_bar)
root.mainloop()
