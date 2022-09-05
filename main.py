# library management system using OOP, sqlite3 and tkinter
import sqlite3
from tkinter import *
from tkinter import messagebox

# TODO list
# TODO: confirmations  -  DONE
# TODO: reset id
# TODO: add cancel/close buttons  -  DONE
# TODO: fix bugs
# TODO: GUI  -  DONE
# TODO: prettier data display from db (make a table not just display in multiline)  -  DONE
# TODO: more, better comments (is this even doable?)


# classes
class User:
    def __init__(self, name, age, books_lend):
        self.name = name
        self.age = age
        self.books_lend = books_lend

    def add_to_db(self):
        query = f"INSERT INTO users(name, age, books_lend) VALUES('{self.name}', {self.age}, {self.books_lend})"
        try:
            decision = messagebox.askyesno("Are you sure?", f"Do you want to add {self.name} age {self.age}?")
            if decision is True:
                cursor.execute(query)
            else:
                return
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error!", f"Inserting user has been unsuccessful! \n {e}")
        else:
            con.commit()  # committing changes
            messagebox.showinfo("Success!", "Inserting user has been successful!")


class Book:
    def __init__(self, title, author, publish_date):
        self.title = title
        self.author = author
        self.publish_date = publish_date

    def add_to_db(self):
        query = f"INSERT INTO books(title, author, publish_date) " \
                f"VALUES('{self.title}', '{self.author}', '{self.publish_date}')"
        try:
            decision = messagebox.askyesno("Are you sure?", f"Do you want to add {self.title} published by {self.author} on {self.publish_date}?")
            if decision is True:
                cursor.execute(query)
            else:
                return
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error!", f"Inserting book has been unsuccessful! \n {e}")
        else:
            con.commit()  # committing changes
            messagebox.showinfo("Success!", "Inserting book has been successful!")


class LendingData:
    def __init__(self, name, title):
        self.name = name
        self.title = title

    def add_to_db(self):
        query = f"INSERT INTO lending_data(user_name, book_title) VALUES('{self.name}', '{self.title}')"
        update_books_lend = f"UPDATE users SET books_lend = books_lend + 1 WHERE name = '{self.name}'"
        try:
            decision = messagebox.askyesno("Are you sure?", f"Do you want to add {self.name} who lent {self.title}?")
            if decision is True:
                cursor.execute(query)
                cursor.execute(update_books_lend)
            else:
                return
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error!", f"Inserting lending data has been unsuccessful! \n {e}")
        else:
            con.commit()  # committing changes
            messagebox.showinfo("Success!", "Inserting lending data has been successful!")


# normal static functions
# adding to database
def add_record_to_db(name_of_table):
    global name_entry
    global age_entry
    global title_entry
    global author_entry
    global publish_date_entry
    global lending_name_entry
    global lending_book_entry
    global adding_to_db_window

    adding_to_db_window = Toplevel()
    adding_to_db_window.title(f"Add a record to the {name_of_table} table")

    if name_of_table == "users":
        adding_to_db_window.geometry("250x130")
        # labels
        name_label = Label(adding_to_db_window, text="Name: ")
        name_label.grid(row=0, column=0)

        age_label = Label(adding_to_db_window, text="Age: ")
        age_label.grid(row=1, column=0)

        # entries
        name_entry = Entry(adding_to_db_window)
        name_entry.grid(row=0, column=1)

        age_entry = Entry(adding_to_db_window)
        age_entry.grid(row=1, column=1)

    if name_of_table == "books":
        adding_to_db_window.geometry("300x170")
        # labels
        title_label = Label(adding_to_db_window, text="Title: ")
        title_label.grid(row=0, column=0)

        author_label = Label(adding_to_db_window, text="Author: ")
        author_label.grid(row=1, column=0)

        publish_date_label = Label(adding_to_db_window, text="Publish date: \n (DD/MM/YYYY)")
        publish_date_label.grid(row=2, column=0)

        # entries
        title_entry = Entry(adding_to_db_window)
        title_entry.grid(row=0, column=1)

        author_entry = Entry(adding_to_db_window)
        author_entry.grid(row=1, column=1)

        publish_date_entry = Entry(adding_to_db_window)
        publish_date_entry.grid(row=2, column=1)

    if name_of_table == "lending_data":
        adding_to_db_window.geometry("250x130")
        # labels
        lending_name_label = Label(adding_to_db_window, text="Name: ")
        lending_name_label.grid(row=0, column=0)

        lending_book_label = Label(adding_to_db_window, text="Book: ")
        lending_book_label.grid(row=1, column=0)

        # entries
        lending_name_entry = Entry(adding_to_db_window)
        lending_name_entry.grid(row=0, column=1)

        lending_book_entry = Entry(adding_to_db_window)
        lending_book_entry.grid(row=1, column=1)

    # button
    add_button = Button(adding_to_db_window, text="Add to database", command=lambda: adding(name_of_table))
    add_button.grid(row=3, column=0, columnspan=2)

    # cancel button
    cancel_button = Button(adding_to_db_window, text="Cancel", command=adding_to_db_window.destroy)
    cancel_button.grid(row=4, column=0, columnspan=2)


def adding(name_of_table):
    if name_of_table == "users":
        new_record = User(name_entry.get(), age_entry.get(), 0)
        new_record.add_to_db()

    if name_of_table == "books":
        new_record = Book(title_entry.get(), author_entry.get(), publish_date_entry.get())
        new_record.add_to_db()

    if name_of_table == "lending_data":
        if check_if_exist(lending_name_entry.get(), lending_book_entry.get()) is False:
            messagebox.showerror("Error!", "There is no such a data in a database!")
            return

        new_record = LendingData(lending_name_entry.get(), lending_book_entry.get())
        new_record.add_to_db()

    adding_to_db_window.destroy()


# deleting from the database
def delete_from_db(name_of_table, id_column):
    global id_entry
    global remove_from_db

    remove_from_db = Toplevel()
    remove_from_db.title(f"Remove item from the {name_of_table} table")
    remove_from_db.geometry("220x70")

    id_label = Label(remove_from_db, text="Id: ")
    id_label.grid(row=0, column=0)

    id_entry = Entry(remove_from_db)
    id_entry.grid(row=0, column=1)

    # remove button
    remove_btn = Button(remove_from_db, text="Delete a record", command=lambda: removing(name_of_table, id_column))
    remove_btn.grid(row=3, column=0, columnspan=2)

    # cancel button
    cancel_button = Button(remove_from_db, text="Cancel", command=remove_from_db.destroy)
    cancel_button.grid(row=4, column=0, columnspan=2)


def removing(name_of_table, id_column):
    query = f"DELETE FROM {name_of_table} WHERE {id_column} = {id_entry.get()}"
    try:
        decision = messagebox.askyesno("Are you sure?", f"Do you want to remove an id of '{id_entry.get()}' from the '{name_of_table}' table?")
        if decision is True:
            cursor.execute(query)
        else:
            return
    except sqlite3.OperationalError as e:
        messagebox.showerror("Error!", f"Removing record has been unsuccessful! \n {e}")
    else:
        con.commit()  # committing changes
        messagebox.showinfo("Success!", "Removing record has been successful!")
        remove_from_db.destroy()


# displaying data from the table
def show_from_db(name_of_table):
    view_window = Toplevel()
    view_window.title(f"View the contents of {name_of_table} table")
    view_window.geometry("600x200")

    # getting data from database
    query = f"SELECT * FROM {name_of_table}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # checking if table has any records
    if len(rows) == 0:
        messagebox.showerror("Error!", "There is no data in a table!")
        view_window.destroy()
        return

    # creating a table made of the data set from database
    for row in range(len(rows)):
        for record in range(len(rows[0])):
            e = Entry(view_window, width=16)
            e.grid(row=row, column=record)
            e.insert(END, rows[row][record])
            e.config(state=DISABLED)

    # close
    close_button = Button(view_window, text="Close", command=view_window.destroy)
    close_button.grid(row=row+1, column=0, sticky=S+W)


# checking if entered name and book title exists in database
def check_if_exist(name, title):
    user_query = f"SELECT count(name) FROM users WHERE name = '{name}'"
    title_query = f"SELECT count(title) FROM books WHERE title = '{title}'"

    cursor.execute(user_query)
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        return False

    cursor.execute(title_query)
    title_count = cursor.fetchone()[0]

    if title_count == 0:
        return False

    return True


# creating database and tables
con = sqlite3.connect("library.db")  # creating/connecting to a database

cursor = con.cursor()

# creating tables
# users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id integer PRIMARY KEY AUTOINCREMENT,
        name text,
        age integer,
        books_lend integer
    )
""")

# books table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        book_id integer PRIMARY KEY AUTOINCREMENT,
        title text,
        author text,
        publish_date text
    )
""")

# lending data table
cursor.execute("""
    CREATE TABLE  IF NOT EXISTS lending_data(
        lending_id integer PRIMARY KEY AUTOINCREMENT,
        user_name text,
        book_title text,
        FOREIGN KEY("user_name") REFERENCES "users"("name"),
        FOREIGN KEY("book_title") REFERENCES "books"("title")
    )
""")

con.commit()  # committing changes

# main hub
root = Tk()
root.title("Library management system")
root.geometry("420x200")
root.option_add("*Font", "arial")
root.option_add("*Label.Font", "arial 12")

# main title label
title_label = Label(root, text="Welcome to the library management system", font=("arial", 16))
title_label.grid(row=0, column=0, columnspan=3)

# title labels (user, book, lending data)
user_label = Label(root, text="User:")
user_label.grid(row=1, column=0)

book_label = Label(root, text="Book:")
book_label.grid(row=1, column=1)

lending_data_label = Label(root, text="Lending data:")
lending_data_label.grid(row=1, column=2)

# 'add' buttons
add_user_btn = Button(root, text="ADD", padx=18, command=lambda: add_record_to_db("users"))
add_user_btn.grid(row=2, column=0)

add_book_btn = Button(root, text="ADD", padx=18, command=lambda: add_record_to_db("books"))
add_book_btn.grid(row=2, column=1)

add_lending_data_btn = Button(root, text="ADD", padx=18, command=lambda: add_record_to_db("lending_data"))
add_lending_data_btn.grid(row=2, column=2)

# "remove' buttons
remove_user_btn = Button(root, text="REMOVE", command=lambda: delete_from_db("users", "user_id"))
remove_user_btn.grid(row=3, column=0)

remove_book_btn = Button(root, text="REMOVE", command=lambda: delete_from_db("books", "book_id"))
remove_book_btn.grid(row=3, column=1)

remove_lending_data_btn = Button(root, text="REMOVE", command=lambda: delete_from_db("lending_data", "lending_id"))
remove_lending_data_btn.grid(row=3, column=2)

# 'view' buttons
view_user_btn = Button(root, text="VIEW", padx=15,  command=lambda: show_from_db("users"))
view_user_btn.grid(row=4, column=0)

view_book_btn = Button(root, text="VIEW", padx=15, command=lambda: show_from_db("books"))
view_book_btn.grid(row=4, column=1)

view_lending_data_btn = Button(root, text="VIEW", padx=15, command=lambda: show_from_db("lending_data"))
view_lending_data_btn.grid(row=4, column=2)

root.mainloop()

con.close()
