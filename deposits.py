from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import connect_database
from tkinter import messagebox
from datetime import datetime

def add_expenses (date, supplier, amount, deposits_treeview):
    if (date=='' or supplier==''  or amount=='' ):
        messagebox.showerror('Error','All feilds are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS payments_data (date VARCHAR(50), supplier VARCHAR(100), amount INT(50))')
            cursor.execute('INSERT INTO payments_data (date, supplier, amount) VALUES (%s, %s, %s)', (date, supplier, amount))
            connection.commit()
            messagebox.showinfo('Success', 'Expenses added successfully')
            treeview_expense(deposits_treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_expense(deposits_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM payments_data')
        customer_records = cursor.fetchall()
        deposits_treeview.delete(*deposits_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            deposits_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear_expenses(date_entry, supplier_entry, Amount_entry):
    date_entry.delete(0, END)
    supplier_entry.delete(0, END)
    Amount_entry.delete(0, END)
    messagebox.showinfo('Cleared', 'All entries have been cleared')


def delete_expenses(deposits_treeview):
    selected = deposits_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the entry to delete')
        return
    result = messagebox.askyesno('Confirm', 'Do you want to delete this record?')
    if not result:
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        item = deposits_treeview.item(selected[0])
        values = item['values']
        if len(values) < 3:
            messagebox.showerror('Error', 'Selected entry is invalid.')
            return
        cursor.execute('DELETE FROM payments_data WHERE date=%s AND supplier=%s AND amount=%s', (values[0], values[1], values[2]))
        connection.commit()
        messagebox.showinfo('Success', 'Expenses deleted successfully')
        treeview_expense(deposits_treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def ubdate_expenses(date, supplier, amount, deposits_treeview):
    selected = deposits_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the record to update')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        item = deposits_treeview.item(selected[0])
        values = item['values']
        if len(values) < 3:
            messagebox.showerror('Error', 'Selected entry is invalid.')
            return
        old_date, old_supplier, old_amount = values[0], values[1], values[2]
        # Check if any changes were made
        if str(date).strip() == str(old_date).strip() and str(supplier).strip() == str(old_supplier).strip() and str(amount).strip() == str(old_amount).strip():
            messagebox.showerror('Error', 'No changes made to update')
            return
        cursor.execute('UPDATE payments_data SET date=%s, supplier=%s, amount=%s WHERE date=%s AND supplier=%s AND amount=%s',
                       (date, supplier, amount, old_date, old_supplier, old_amount))
        connection.commit()
        treeview_expense(deposits_treeview)
        messagebox.showinfo('Success', 'Expense data updated successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()



def seleted_expense(event, deposits_treeview, date_entry, supplier_entry, Amount_entry):
    selected = deposits_treeview.selection()
    if not selected:
        return
    item = deposits_treeview.item(selected[0])
    values = item['values']
    if len(values) < 3:
        return
    date_entry.delete(0, END)
    date_entry.insert(0, values[0])
    supplier_entry.delete(0, END)
    supplier_entry.insert(0, values[1])
    Amount_entry.delete(0, END)
    Amount_entry.insert(0, values[2])

def view_day_expenses(date_entry, deposits_treeview, balance):
    selected_date = date_entry.get()
    if not selected_date:
        messagebox.showerror('Error', 'Please select a date')
        return
    try:
        # Convert selected date to datetime object
        selected_dt = datetime.strptime(selected_date, "%m/%d/%y")
    except Exception as e:
        messagebox.showerror('Error', f'Invalid date format: {e}')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        cursor.execute('SELECT * FROM payments_data')
        records = cursor.fetchall()
        filtered = []
        total = 0

        for record in records:
            try:
                record_date = datetime.strptime(str(record[0]), "%m/%d/%y")
                if record_date.date() == selected_dt.date():  # Compare exact date
                    filtered.append(record)
                    try:
                        total += float(record[2])
                    except Exception:
                        pass
            except Exception:
                continue

        # Clear and insert filtered records
        deposits_treeview.delete(*deposits_treeview.get_children())
        for record in filtered:
            deposits_treeview.insert('', END, values=record)

        balance.delete(0, END)
        balance.insert(0, str(round(total, 2)))

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def fetch_supplier(supplier_combobox):
    supplier_options = []

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        cursor.execute('SELECT DISTINCT supplier_Name FROM supplier_data')
        suppliers = cursor.fetchall()

        if suppliers:
            supplier_combobox.set('Select')
            for row in suppliers:
                supplier_options.append(row[0])
            supplier_combobox.config(values=supplier_options)

    except Exception as e:
        messagebox.showerror('Error', f'Error fetching suppliers: {e}')
    finally:
        cursor.close()
        connection.close()




def managedeposits(window):
    
    expenses_frame = Toplevel(window)
    expenses_frame.title("Manage Deposits")
    expenses_frame.geometry("1500x780+330+175")
    expenses_frame.configure(bg="white")
    expenses_frame.resizable(True, True)

    #the title label
    title_label=Label(expenses_frame,text="Supplier Payments ",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(expenses_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    deposits_treeview=ttk.Treeview(treeview_frame,columns=("Date","Supplier_Name","Amount"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=deposits_treeview.yview)
    scrollx.config(command=deposits_treeview.xview)
    deposits_treeview.heading("Date",text="Date")
    deposits_treeview.heading("Supplier_Name",text="Supplier Name")
    deposits_treeview.heading("Amount",text="Amount")

    deposits_treeview.column("Date",width=150)
    deposits_treeview.column("Supplier_Name",width=100)
    deposits_treeview.column("Amount",width=150)
    treeview_expense(deposits_treeview)

    deposits_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(expenses_frame,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    cashDate_label =Label(entry_frame,text="Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    cashDate_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    date_entry = DateEntry(entry_frame, font=("times New roman", 15), width=15, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    supplier =Label(entry_frame,text="Supplier",font=("times New roman",15,"bold"),bg="white",fg="black")
    supplier.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    supplier=ttk.Combobox(entry_frame,font=("times New roman",15,"bold"),values=["empty","empty2"],width=13,state="readonly")
    supplier.grid(row=1,column=1,pady=10,padx=10,sticky="w")
    supplier.set("Select")
    fetch_supplier(supplier)

    balance =Label(entry_frame,text="Total Deposits",font=("times new roman",15,"bold"),bg="white",fg="black")
    balance.grid(row=0,column=2,pady=10,padx=10,sticky="w")
    balance=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    balance.grid(row=0,column=3,pady=10,padx=10,sticky="w")


    Amount_label =Label(entry_frame,text="Amount",font=("times new roman",15,"bold"),bg="white",fg="black")
    Amount_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    Amount_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    Amount_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

                      
    add_button=Button(entry_frame,text="Add",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_expenses(date_entry.get(), supplier.get(), Amount_entry.get(), deposits_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(entry_frame,text="Clear",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_expenses(date_entry, supplier, Amount_entry))
    clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_expenses(deposits_treeview))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:ubdate_expenses(date_entry.get(), supplier.get(), Amount_entry.get(), deposits_treeview))
    update_button.grid(row=5,column=5,pady=10,padx=10,sticky="w")

    view_button=Button(entry_frame,text="View",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: view_day_expenses(date_entry, deposits_treeview,balance))
    view_button.grid(row=0,column=4,pady=10,padx=10,sticky="w")




    deposits_treeview.bind('<ButtonRelease-1>', lambda event: seleted_expense(event, deposits_treeview, date_entry, supplier, Amount_entry))







    





