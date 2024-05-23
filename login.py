import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector

import mysql.connector


def authenticate():
    username = username_entry.get()
    password = password_entry.get()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'flowershop',
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Verify administrator
    admin_query = "SELECT * FROM admins WHERE username = %s AND password = %s"
    cursor.execute(admin_query, (username, password))
    admin_result = cursor.fetchone()

    # Verify user
    user_query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(user_query, (username, password))
    user_result = cursor.fetchone()


    cursor.close()
    cnx.close()

    if admin_result:
        messagebox.showinfo("Login Successful", f"Welcome Admin {username}!")
        open_admin_panel()
    elif user_result:
        messagebox.showinfo("Login Successful", f"Welcome User {username}!")
        open_user_panel()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password, please try again.")


def register():
    new_username = username_entry.get()
    new_password = password_entry.get()

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'flowershop',
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (new_username, new_password))
        cnx.commit()
        messagebox.showinfo("Registration Successful", f"User {new_username} has been registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Registration Failed", "Username already exists. Please choose a different username.")

    cursor.close()
    cnx.close()

def fetch_flowers():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'flowershop',
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM flowers")
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return results

def buy_flower():
    selected_item = flower_treeview.focus()
    if not selected_item:
        messagebox.showerror("Error", "Please select a flower first.")
        return

    flower = flower_treeview.item(selected_item)
    flower_id = flower["values"][0]
    available_stock = flower["values"][4]

    quantity = tk.simpledialog.askinteger("Purchase Quantity", "Please enter the quantity you want to purchase:", minvalue=1, maxvalue=available_stock)

    if not quantity:
        return

    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'flowershop',
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    update_query = "UPDATE flowers SET stock = stock - %s WHERE id = %s"
    cursor.execute(update_query, (quantity, flower_id))
    cnx.commit()
    cursor.close()
    cnx.close()

    messagebox.showinfo("Purchase Successful", f"You have successfully purchased {quantity} {flower['values'][1]}.")

    # Update the flower list
    flower_treeview.delete(*flower_treeview.get_children())
    for flower in fetch_flowers():
        flower_treeview.insert('', 'end', values=flower)


def open_user_panel():
    user_panel = tk.Toplevel(root)
    user_panel.title("Purchase Interface")
    global flower_treeview

    flower_treeview = ttk.Treeview(user_panel, columns=("id", "name", "origin", "price", "stock"), show="headings")
    flower_treeview.heading("id", text="ID")
    flower_treeview.heading("name", text="Name")
    flower_treeview.heading("origin", text="Origin")
    flower_treeview.heading("price", text="Price")
    flower_treeview.heading("stock", text="Stock")
    flower_treeview.grid(row=0, column=0, padx=5, pady=5)

    scrollbar = ttk.Scrollbar(user_panel, orient="vertical", command=flower_treeview.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    flower_treeview.configure(yscrollcommand=scrollbar.set)

    buy_button = ttk.Button(user_panel, text="Buy", command=buy_flower)
    buy_button.grid(row=1, column=0, pady=5)


    for flower in fetch_flowers():
        flower_treeview.insert('', 'end', values=flower)

def open_admin_panel():
    def add_flower(admin_pane):
        def submit():
            name = name_entry.get()
            origin = origin_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())

            config = {
                'user': 'root',
                'password': 'root',
                'host': 'localhost',
                'database': 'flowershop',
            }

            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            insert_query = "INSERT INTO flowers (flower_name, origin, price, stock) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, origin, price, stock))
            cnx.commit()
            cursor.close()
            cnx.close()

            messagebox.showinfo("Add Successful", f"You have successfully added {name}.")

            # Update the flower list
            flower_treeview.delete(*flower_treeview.get_children())
            for flower in fetch_flowers():
                flower_treeview.insert('', 'end', values=flower)

            add_window.destroy()

        add_window = tk.Toplevel(admin_panel)
        add_window.title("Add Flower")

        tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Origin:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        origin_entry = tk.Entry(add_window)
        origin_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(add_window, text="Stock:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        stock_entry = tk.Entry(add_window)
        stock_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_button = tk.Button(add_window, text="Submit", command=submit)
        submit_button.grid(row=4, column=0, columnspan=2, pady=5)


    def update_flower(admin_panel):
        selected_item = flower_treeview.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a flower first.")
            return

        flower = flower_treeview.item(selected_item)
        flower_id = flower["values"][0]

        def submit():
            name = name_entry.get()
            origin = origin_entry.get()
            price = float(price_entry.get())
            stock = int(stock_entry.get())

            config = {
                'user': 'root',
                'password': 'root',
                'host': 'localhost',
                'database': 'flowershop',
            }

            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            update_query = "UPDATE flowers SET flower_name=%s, origin=%s, price=%s, stock=%s WHERE id=%s"
            cursor.execute(update_query, (name, origin, price, stock, flower_id))
            cnx.commit()
            cursor.close()
            cnx.close()

            messagebox.showinfo("Update successful", f"You have successfully updated {name}.")

            # Refresh the flower list
            flower_treeview.delete(*flower_treeview.get_children())
            for flower in fetch_flowers():
                flower_treeview.insert('', 'end', values=flower)

            update_window.destroy()

        update_window = tk.Toplevel(admin_panel)
        update_window.title("Update Flower")

        tk.Label(update_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, flower["values"][1])
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(update_window, text="Origin:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        origin_entry = tk.Entry(update_window)
        origin_entry.insert(0, flower["values"][2])
        origin_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(update_window, text="Price:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        price_entry = tk.Entry(update_window)
        price_entry.insert(0, flower["values"][3])
        price_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(update_window, text="Stock:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        stock_entry = tk.Entry(update_window)
        stock_entry.insert(0, flower["values"][4])
        stock_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_button = tk.Button(update_window, text="Submit", command=submit)
        submit_button.grid(row=4, column=0, columnspan=2, pady=5)

    def delete_flower(admin_panel):
        selected_item = flower_treeview.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a flower first.")
            return

        flower = flower_treeview.item(selected_item)
        flower_id = flower["values"][0]
        flower_name = flower["values"][1]

        result = messagebox.askyesno("Confirm deletion", f"Are you sure you want to delete {flower_name}?")
        if result:
            config = {
                'user': 'root',
                'password': 'root',
                'host': 'localhost',
                'database': 'flowershop',
            }

            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()
            delete_query = "DELETE FROM flowers WHERE id=%s"
            cursor.execute(delete_query, (flower_id,))
            cnx.commit()
            cursor.close()
            cnx.close()

            messagebox.showinfo("Deletion successful", f"You have successfully deleted {flower_name}.")

            # Refresh the flower list
            for flower in fetch_flowers():
                flower_treeview.insert('', 'end', values=flower)
            flower_treeview.delete(selected_item)

    admin_panel = tk.Toplevel(root)
    admin_panel.title("Administration Interface")

    flower_treeview = ttk.Treeview(admin_panel, columns=("id", "name", "origin", "price", "stock"), show="headings")
    flower_treeview.heading("id", text="ID")
    flower_treeview.heading("name", text="Name")
    flower_treeview.heading("origin", text="Origin")
    flower_treeview.heading("price", text="Price")
    flower_treeview.heading("stock", text="Stock")
    flower_treeview.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

    scrollbar = ttk.Scrollbar(admin_panel, orient="vertical", command=flower_treeview.yview)
    scrollbar.grid(row=0, column=3, sticky='ns')
    flower_treeview.configure(yscrollcommand=scrollbar.set)

    add_button = tk.Button(admin_panel, text="Add", command=lambda: add_flower(admin_panel))
    add_button.grid(row=1, column=0, pady=5)

    update_button = tk.Button(admin_panel, text="Update", command=lambda: update_flower(admin_panel))
    update_button.grid(row=1, column=1, pady=5)

    delete_button = tk.Button(admin_panel, text="Delete", command=lambda: delete_flower(admin_panel))
    delete_button.grid(row=1, column=2, pady=5)

    for flower in fetch_flowers():
        flower_treeview.insert('', 'end', values=flower)

root = tk.Tk()
root.title("Online Flower Shop Login")

tk.Label(root, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(root, text="Login", command=authenticate)
login_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

register_button = tk.Button(root, text="Register", command=register)
register_button.grid(row=2, column=1, padx=5, pady=5, sticky='e')

root.mainloop()