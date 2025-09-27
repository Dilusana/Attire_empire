from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import connect_database
from tkinter import messagebox
from datetime import datetime


def add_douty_charge(date, description, payment_state, amount,douty_charge_treeview):
    if date == '' or description == '' or payment_state == '' or amount == '':
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS douty_charge_data (Date VARCHAR(50), Description VARCHAR(255), Payment_States VARCHAR(50), Amount INT(50))')
            cursor.execute('INSERT INTO douty_charge_data (Date, Description, Payment_States, Amount) VALUES (%s, %s, %s, %s)', (date, description, payment_state, amount))
            connection.commit()
            messagebox.showinfo('Success', 'Douty charge added successfully')
            treeview_douty_charge(douty_charge_treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_douty_charge(douty_charge_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM douty_charge_data')
        customer_records = cursor.fetchall()
        douty_charge_treeview.delete(*douty_charge_treeview.get_children())
        for record in customer_records:
            douty_charge_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def select_fardar_entry(event, treeview, date_entry, description_entry, payment_state_combobox, amount_entry):
    selected_item = treeview.focus()
    if selected_item:
        values = treeview.item(selected_item, 'values')
        if values:
            date_entry.delete(0, END)
            date_entry.insert(0, values[0])
            description_entry.delete(0, END)
            description_entry.insert(0, values[1])
            payment_state_combobox.set(values[2])
            amount_entry.delete(0, END)
            amount_entry.insert(0, values[3])

def delete_douty_charge(douty_charge_treeview):
    selected_item = douty_charge_treeview.focus()
    if selected_item:
        values = douty_charge_treeview.item(selected_item, 'values')
        if values:
            date = values[0]
            description = values[1]
            payment_state = values[2]
            amount = values[3]
            try:
                amount_int = int(amount)
            except ValueError:
                messagebox.showerror('Error', 'Amount value is invalid and cannot be deleted.')
                return
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE attire_empire')
                cursor.execute('DELETE FROM douty_charge_data WHERE Date=%s AND Description=%s AND Payment_States=%s AND Amount=%s', (date, description, payment_state, amount_int))
                connection.commit()
                messagebox.showinfo('Success', 'Douty charge deleted successfully')
                treeview_douty_charge(douty_charge_treeview)
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()
    
def clear_entries(date_entry, description_entry, payment_state_combobox, amount_entry):
    date_entry.delete(0, END)
    description_entry.delete(0, END)
    payment_state_combobox.set('Select')
    amount_entry.delete(0, END)

def update_douty_charge(date, description, payment_state, amount, douty_charge_treeview):
    selected = douty_charge_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the entry to update')
        return
    item = douty_charge_treeview.item(selected[0])
    values = item['values']
    if len(values) < 4:
        messagebox.showerror('Error', 'Selected entry is invalid.')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        cursor.execute(
            'UPDATE douty_charge_data SET Date=%s, Description=%s, Payment_States=%s, Amount=%s WHERE Date=%s AND Description=%s AND Payment_States=%s AND Amount=%s',
            (date, description, payment_state, amount, values[0], values[1], values[2], values[3])
        )
        connection.commit()
        messagebox.showinfo('Success', 'Douty charge updated successfully')
        treeview_douty_charge(douty_charge_treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def view_month_deposits(date_entry, douty_charge_treeview, balance):
    selected_date = date_entry.get()
    if not selected_date:
        messagebox.showerror('Error', 'Please select a date')
        return
    try:
        # Extract year and month from the selected date
        dt = datetime.strptime(selected_date, "%m/%d/%y")
        year = dt.year
        month = dt.month
    except Exception as e:
        messagebox.showerror('Error', f'Invalid date format: {e}')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        cursor.execute('SELECT * FROM douty_charge_data')
        records = cursor.fetchall()
        filtered = []
        total = 0
        for record in records:
            try:
                rec_date = datetime.strptime(str(record[0]), "%m/%d/%y")
                if rec_date.year == year and rec_date.month == month:
                    filtered.append(record)
                    try:
                        total += float(record[3])
                    except Exception:
                        pass
            except Exception:
                continue
        douty_charge_treeview.delete(*douty_charge_treeview.get_children())
        for record in filtered:
            douty_charge_treeview.insert('', END, values=record)
        balance.delete(0, END)
        balance.insert(0, str(total))

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def manageDouty_charges(window):
    
    douty_frame = Toplevel(window)
    douty_frame.title("Manage Duty Charges")
    douty_frame.geometry("1500x780+330+175")
    douty_frame.configure(bg="white")
    douty_frame.resizable(True, True)

    #the title label
    title_label=Label(douty_frame,text="Duty Charge",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(douty_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    douty_charge_treeview=ttk.Treeview(treeview_frame,columns=("Date","Description","Payment_States","Amount"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=douty_charge_treeview.yview)
    scrollx.config(command=douty_charge_treeview.xview)
    douty_charge_treeview.heading("Date",text="Date")
    douty_charge_treeview.heading("Description",text="Description")
    douty_charge_treeview.heading("Payment_States",text="Payment_States")
    douty_charge_treeview.heading("Amount",text="Amount")

    douty_charge_treeview.column("Date",width=150)
    douty_charge_treeview.column("Description",width=100)
    douty_charge_treeview.column("Payment_States",width=150)
    douty_charge_treeview.column("Amount",width=150)
    treeview_douty_charge(douty_charge_treeview)

    douty_charge_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(douty_frame,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    cashDate_label =Label(entry_frame,text="Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    cashDate_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    date_entry = DateEntry(entry_frame, font=("times New roman", 15), width=15, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    description =Label(entry_frame,text="Description",font=("times new roman",15,"bold"),bg="white",fg="black")
    description.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    description=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    description.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    Amount_label =Label(entry_frame,text="Amount",font=("times new roman",15,"bold"),bg="white",fg="black")
    Amount_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    Amount_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    Amount_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    Payment_States_label =Label(entry_frame,text="Payment States",font=("times New roman",15,"bold"),bg="white",fg="black")
    Payment_States_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    Payment_States_combobox=ttk.Combobox(entry_frame,font=("times New roman",15,"bold"),state="readonly",values=["Paid","Not Paid"],width=15)
    Payment_States_combobox.grid(row=3,column=1,pady=10,padx=10,sticky="w")
    Payment_States_combobox.set("Select")

    balance_label = Label(entry_frame, text="Total Deposits", font=("times new roman", 15, "bold"), bg="white", fg="black")
    balance_label.grid(row=0, column=2, pady=10, padx=10, sticky="w")
    balance = Entry(entry_frame, font=("times new roman", 15), bd=2, relief=RIDGE, width=17)
    balance.grid(row=0, column=3, pady=10, padx=10, sticky="w")


    view_button=Button(entry_frame,text="View",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: view_month_deposits(date_entry,douty_charge_treeview,balance))
    view_button.grid(row=0,column=4,pady=10,padx=10,sticky="w")

                      
    add_button=Button(entry_frame,text="Add",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: add_douty_charge(date_entry.get(),description.get(),Payment_States_combobox.get(),Amount_entry.get(),douty_charge_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(entry_frame,text="Clear",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_entries(date_entry, description, Payment_States_combobox, Amount_entry))
    clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: delete_douty_charge(douty_charge_treeview))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: update_douty_charge(date_entry.get(), description.get(), Payment_States_combobox.get(), Amount_entry.get(), douty_charge_treeview))
    update_button.grid(row=5,column=5,pady=10,padx=10,sticky="w")

    douty_charge_treeview.bind("<ButtonRelease-1>", lambda event: select_fardar_entry(event, douty_charge_treeview, date_entry, description, Payment_States_combobox, Amount_entry))





    





