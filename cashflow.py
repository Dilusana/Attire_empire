from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import connect_database
from tkinter import messagebox

def add_cashflow(date, description, states, amount, cash_treeview):
    if not date or not description or not states or not amount:
        messagebox.showerror('Error', 'All fields are required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE attire_empire')
        cursor.execute('CREATE TABLE IF NOT EXISTS cash_flow ( Date VARCHAR(50), Description VARCHAR(100), states VARCHAR(50), Amount FLOAT)')
        cursor.execute('INSERT INTO cash_flow (Date, Description, states, Amount) VALUES (%s, %s, %s, %s)', (date, description, states, float(amount)))
        connection.commit()

        # Clear the treeview
        for item in cash_treeview.get_children():
            cash_treeview.delete(item)

        # Fetch and display updated data
        cursor.execute('SELECT * FROM cash_flow')
        for row in cursor.fetchall():
            cash_treeview.insert('', 'end', values=row)

        messagebox.showinfo('Success', 'Cash flow entry added successfully')

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()




def delete_cashflow(cash_treeview, balance_entry):
    selected = cash_treeview.selection()
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
        item = cash_treeview.item(selected[0])
        values = item['values']
        if len(values) < 4:
            messagebox.showerror('Error', 'Selected entry is invalid.')
            return
        date, description, states, amount = values
        cursor.execute(
            'DELETE FROM cash_flow WHERE Date=%s AND Description=%s AND states=%s AND Amount=%s LIMIT 1',
            (date, description, states, amount)
        )
        connection.commit()

        # Remove only the selected item from the treeview
        cash_treeview.delete(selected[0])
        messagebox.showinfo('Success', 'Cash flow entry deleted successfully')

        # Update balance entry if provided
        if balance_entry is not None and hasattr(balance_entry, "delete") and hasattr(balance_entry, "insert"):
            # Recalculate balance
            total = 0.0
            cursor.execute('SELECT states, Amount FROM cash_flow')
            for state, amt in cursor.fetchall():
                if state.lower() == "debit":
                    total += float(amt)
                elif state.lower() == "credit":
                    total -= float(amt)
            balance_entry.delete(0, END)
            balance_entry.insert(0, str(total))

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def treeview_cashflow(cash_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE attire_empire')
        cursor.execute('SELECT * FROM cash_flow')

        for row in cursor.fetchall():
            cash_treeview.insert('', 'end', values=row)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()



def manageCash(window):
    
    cash_frame = Toplevel(window)
    cash_frame.title("Manage Cash Flow")
    cash_frame.geometry("1500x780+330+175")
    cash_frame.configure(bg="white")
    cash_frame.resizable(True, True)

    #the title label
    title_label=Label(cash_frame,text="Cash Flow Statement",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(cash_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    cash_treeview=ttk.Treeview(treeview_frame,columns=("Date","Description","states","Amount"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=cash_treeview.yview)
    scrollx.config(command=cash_treeview.xview)
    cash_treeview.heading("Date",text="Date")
    cash_treeview.heading("Description",text="Description")
    cash_treeview.heading("states",text="states")
    cash_treeview.heading("Amount",text="Amount")


    cash_treeview.column("Date",width=150)
    cash_treeview.column("Description",width=100)
    cash_treeview.column("states",width=150)
    cash_treeview.column("Amount",width=150)
    treeview_cashflow(cash_treeview)

    cash_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(cash_frame,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    cashDate_label =Label(entry_frame,text="Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    cashDate_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    date_entry = DateEntry(entry_frame, font=("times New roman", 15), width=15, background='darkblue', foreground='white', borderwidth=2)
    date_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    description =Label(entry_frame,text="Description",font=("times new roman",15,"bold"),bg="white",fg="black")
    description.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    description=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    description.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    states_label =Label(entry_frame,text="States",font=("times New roman",15,"bold"),bg="white",fg="black")
    states_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    states_combobox=ttk.Combobox(entry_frame,font=("times New roman",15,"bold"),state="readonly",values=["Credit","Debit"],width=15)
    states_combobox.grid(row=2,column=1,pady=10,padx=10,sticky="w")
    states_combobox.set("Select")

    Amount_label =Label(entry_frame,text="Amount",font=("times new roman",15,"bold"),bg="white",fg="black")
    Amount_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    Amount_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    Amount_entry.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    Balance_label =Label(entry_frame,text="Balance",font=("times new roman",15,"bold"),bg="white",fg="black")
    Balance_label.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    Balance_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    Balance_entry.grid(row=4,column=1,pady=10,padx=10,sticky="w")


    add_button=Button(entry_frame,text="Add",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_cashflow(date_entry.get(),description.get(),states_combobox.get(),Amount_entry.get(),cash_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")



    delete_button=Button(entry_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_cashflow(cash_treeview,Balance_entry))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")





    def calculate_total_balance():
        cursor, connection = connect_database()
        if not cursor or not connection:
            return 0.0
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT states, Amount FROM cash_flow')
            total = 0.0
            for state, amount in cursor.fetchall():
                if state.lower() == "debit":
                    total += float(amount)
                elif state.lower() == "credit":
                    total -= float(amount)
            return total
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
            return 0.0
        finally:
            cursor.close()
            connection.close()

    def update_balance_entry():
        total_balance = calculate_total_balance()
        Balance_entry.delete(0, END)
        Balance_entry.insert(0, str(total_balance))

    # Update balance on startup and after adding new entry
    update_balance_entry()

    def add_and_update_balance(*args):
        add_cashflow(date_entry.get(), description.get(), states_combobox.get(), Amount_entry.get(), cash_treeview)
        update_balance_entry()

    add_button.config(command=add_and_update_balance)




    





