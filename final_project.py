import tkinter as tk
from tkinter import ttk
import sqlite3

# Главное окно 
class Main(tk.Frame):
    def __init__(self, root) -> None:
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        # Инструменты
        toolbar = tk.Frame(bg='#7d7d7d', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления сотрудника
        self.add_img = tk.PhotoImage(file='./add.png')
        btn_add = tk.Button(toolbar, bg='#7d7d7d',bd=0,
                            image=self.add_img,
                            command=self.open_dialog)
        btn_add.pack(side=tk.LEFT)

        # Создание кнопки изменения сотрудника
        self.edit_img = tk.PhotoImage(file='./update.png')
        btn_edit = tk.Button(toolbar, bg='#7d7d7d',bd=0,
                            image=self.edit_img,
                            command=self.open_edit)
        btn_edit.pack(side=tk.LEFT)

        # Создание кнопки удаления сотрудника
        self.del_img = tk.PhotoImage(file='./delete.png')
        btn_del = tk.Button(toolbar, bg='#7d7d7d',bd=0,
                            image=self.del_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        # Создание кнопки поиска сотрудника
        self.search_img = tk.PhotoImage(file='./search.png')
        btn_search = tk.Button(toolbar, bg='#7d7d7d',bd=0,
                            image=self.search_img,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Создание кнопки обновления таблицы
        self.refresh_img = tk.PhotoImage(file='./refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#7d7d7d',bd=0,
                            image=self.refresh_img,
                            command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создание таблицы
        self.tree = ttk.Treeview(root,
                                  columns=('id', 'name', 'tel', 'email', 'salary'),
                                  height= 45,
                                  show='headings')
        
        # Добавление параметров столбца
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=225, anchor=tk.CENTER)
        self.tree.column('tel', width=125, anchor=tk.CENTER)
        self.tree.column('email', width=125, anchor=tk.CENTER)
        self.tree.column('salary', width=125, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Заработная плата')
        self.tree.pack(side=tk.LEFT)

        # Полоса прокрутки
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Метод редактирования
    def edit_record(self, name, tel, email, salary):
        ind = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE staff SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?               
        ''', (name, tel, email, salary, ind))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления записей
    def delete_records(self):
        # Проходим циклом по всем выделенным строкам в таблице
        for i in self.tree.selection():
            # Берем id каждой строки
            id = self.tree.set(i, '#1')
            #Удаляем по id
            self.db.cur.execute('''
                DELETE FROM staff
                WHERE id = ?
            ''', (id, ))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска записей
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM staff WHERE name LIKE ?',
                            ('%' + name + '%', ))
        [self.tree.insert('', 'end', values=i)for i in self.db.cur.fetchall()]

    # Вызов дочернего окна
    def open_dialog(self):
        Child()

    # Вызов окна редактирования
    def open_edit(self):
        Update()

    def open_search(self):
        Search()

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM staff')
        [self.tree.insert('', 'end', values=i)for i in self.db.cur.fetchall()]


# Класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        # Запрет на изменение размеров
        self.resizable(False, False)
        # Перехватаваем все события приложения
        self.grab_set()
        # Захватываем фокус
        self.focus_set()

        # Создание формы
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=20)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50, y=50)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=80)
        label_salary = tk.Label(self, text='Заработная плата')
        label_salary.place(x=50, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=20)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200, y=50)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=110)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev:
                     self.view.records(
                         self.entry_name.get(),
                         self.entry_tel.get(),
                         self.entry_email.get(),
                         self.entry_salary.get()))
        self.btn_ok.place(x=300, y=160)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=220, y=160)
        
class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_edit()
        self.load_data()

    def init_edit(self):
        self.title('Редактирование информации о сотруднике')
        # убрать кнопку добавления
        self.btn_ok.destroy()

        # Кнопка отредактировать
        self.btn_ok = tk.Button(self, text='Отредактировать')
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.view.edit_record(
                             self.entry_name.get(),
                             self.entry_tel.get(),
                             self.entry_email.get(),
                             self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=300, y=160)

    # Автозаполнение формы старыми данными
    def load_data(self):
        self.db.cur.execute('''SELECT * FROM staff WHERE id = ?''',
                    self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# Класс окна поиска сотрудника
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        # Запрет на изменение размеров
        self.resizable(False, False)
        # Перехватаваем все события приложения
        self.grab_set()
        # Захватываем фокус
        self.focus_set()

        # Создание формы
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150, y=30)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=230, y=70)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=160, y=70)

# Класс Базы данных 
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('staff_info.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS staff (
                         id INTEGER PRIMARY KEY,
                         name TEXT,
                         phone TEXT,
                         email TEXT,
                         salary TEXT
                )''')
        
    # Добавить в бд
    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''
                INSERT INTO staff (name, phone, email, salary)
                VALUES (?, ?, ?, ?)''', (name, tel, email, salary))
        self.conn.commit()


# Действия при запуске
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title('Список сотрудников компании')
    root.geometry('665x400')
    # Запрет на изменение размеров
    root.resizable(False, False)
    root.mainloop()