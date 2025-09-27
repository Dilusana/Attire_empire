from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import connect_database
from tkinter import messagebox
from datetime import datetime



def add_fardar(date, invoice_no, payment_method, customer_name, delivery_date, amount,fardar_ID, fardar_treeview):
    if (date=='' or invoice_no==''  or payment_method=='' or customer_name=='' or delivery_date=='' or amount=='' or fardar_ID==''):
        messagebox.showerror('Error','All feilds are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS fardar_data (Date VARCHAR(50), Invoice_No VARCHAR(100), fardar_ID VARCHAR(150), Customer_Name VARCHAR(100), Delivery_Date VARCHAR(50), total_amount INT(50),payment VARCHAR(100))')
            cursor.execute('INSERT INTO fardar_data (Date, Invoice_No, fardar_ID, Customer_Name, Delivery_Date, total_amount,payment) VALUES (%s, %s, %s, %s, %s, %s, %s)', (date, invoice_no, fardar_ID, customer_name, delivery_date, amount, payment_method))
            connection.commit()
            messagebox.showinfo('Success', 'Fardar payment added successfully')
            treeview_fardar(fardar_treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_fardar(fardar_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM fardar_data')
        customer_records = cursor.fetchall()
        fardar_treeview.delete(*fardar_treeview.get_children())
        for record in customer_records:  # here is the important not to view all the data in treeview you must use the code
            fardar_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear_entries(date_entry, Invoice_No_entry, payment_combobox, Customer_Name, Delivery_date, Amount):
    date_entry.delete(0, END)
    Invoice_No_entry.delete(0, END)
    payment_combobox.set("Select States")
    Customer_Name.delete(0, END)
    Delivery_date.delete(0, END)
    Amount.delete(0, END)
    messagebox.showinfo('Cleared', 'All entries have been cleared')

def select_fardar_entry(event, fardar_treeview, date_entry, Invoice_No_entry, payment_combobox, Customer_Name,fardar_ID,Delivery_date, Amount):
    selected = fardar_treeview.selection()
    if not selected:
        return
    item = fardar_treeview.item(selected[0])
    values = item['values']
    if len(values) < 6:
        return
    # Populate the entry fields with the selected row's data
    date_entry.delete(0, END)
    date_entry.insert(0, values[0])
    Invoice_No_entry.delete(0, END)
    Invoice_No_entry.insert(0, values[1])
    payment_combobox.set(values[2])
    Customer_Name.delete(0, END)
    Customer_Name.insert(0, values[3])
    Delivery_date.delete(0, END)
    Delivery_date.insert(0, values[4])
    Amount.delete(0, END)
    Amount.insert(0, values[5])
    fardar_ID.delete(0, END)
    fardar_ID.insert(0, values[6])


def delete_expenses(fardar_treeview):
    selected = fardar_treeview.selection()
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
        item = fardar_treeview.item(selected[0])
        values = item['values']
        if len(values) < 2:
            messagebox.showerror('Error', 'Selected entry is invalid.')
            return
        cursor.execute('DELETE FROM fardar_data WHERE Date=%s AND Invoice_No=%s', (values[0], values[1]))
        connection.commit()
        messagebox.showinfo('Success', 'Fardar payment deleted successfully')
        treeview_fardar(fardar_treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()








def Farder(window):
        fardar_frame = Toplevel(window)
        fardar_frame.title("Manage Fardar Payments")
        fardar_frame.geometry("1500x780+330+175")
        fardar_frame.configure(bg="white")
        fardar_frame.resizable(True, True)

        #the title label
        title_label=Label(fardar_frame,text="Fardar Payments",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
        title_label.pack(side=TOP,fill=X)

        #the treeview frame 

        treeview_frame = Frame(fardar_frame,bg="white",bd=3,relief=GROOVE)
        treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


        scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
        scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
        fardar_treeview=ttk.Treeview(treeview_frame,columns=("Ordered_Date","Invoice_No","fardar_ID","Customer_Name","Delivery_Date","Amount","Payment_Method"),show="headings")
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=fardar_treeview.yview)
        scrollx.config(command=fardar_treeview.xview)
        fardar_treeview.heading("Ordered_Date",text="Ordered Date")
        fardar_treeview.heading("Invoice_No",text="Invoice No")
        fardar_treeview.heading("fardar_ID", text="Fardar ID")
        fardar_treeview.heading("Customer_Name",text="Customer_Name")
        fardar_treeview.heading("Delivery_Date",text="Delivery_Date")
        fardar_treeview.heading("Amount",text="Amount")#combo boxx
        fardar_treeview.heading("Payment_Method",text="Payment Method")

        fardar_treeview.column("Ordered_Date",width=150)
        fardar_treeview.column("Invoice_No",width=150)
        fardar_treeview.column("fardar_ID",width=100)
        fardar_treeview.column("Customer_Name",width=100)
        fardar_treeview.column("Delivery_Date",width=100)
        fardar_treeview.column("Amount",width=50)
        fardar_treeview.column("Payment_Method", width=100)

        treeview_fardar(fardar_treeview)

        fardar_treeview.pack(fill=BOTH,expand=1)

        #entry frame 
        entry_frame = Frame(fardar_frame,width=1050,height=330,bg="white")
        entry_frame.pack(side=TOP,fill=X,pady=10)


        Date_label =Label(entry_frame,text="Ordered Date",font=("times New roman",15,"bold"),bg="white",fg="black")
        Date_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
        date_entry = DateEntry(entry_frame, font=("times New roman", 15), width=15, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        Delivery_date =Label(entry_frame,text="Delivery Date",font=("times New roman",15,"bold"),bg="white",fg="black")
        Delivery_date.grid(row=1,column=0,pady=10,padx=10,sticky="w")
        Delivery_date=DateEntry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=15)
        Delivery_date.grid(row=1,column=1,pady=10,padx=10,sticky="w")
                
        payment_label =Label(entry_frame,text="Payment Method",font=("times New roman",15,"bold"),bg="white",fg="black")
        payment_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
        payment_combobox=ttk.Combobox(entry_frame,font=("times New roman",15,"bold"),state="readonly",values=["Cash","COD","Bank Transfer","Credit"],width=15)
        payment_combobox.grid(row=2,column=1,pady=10,padx=10,sticky="w")
        payment_combobox.set("Select Method")

        Invoice_No_label =Label(entry_frame,text="Invoice No",font=("times New roman",15,"bold"),bg="white",fg="black")
        Invoice_No_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
        Invoice_No_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
        Invoice_No_entry.grid(row=3,column=1,pady=10,padx=10,sticky="w")

        Customer_Name =Label(entry_frame,text="Customer Name",font=("times New roman",15,"bold"),bg="white",fg="black")
        Customer_Name.grid(row=4,column=0,pady=10,padx=10,sticky="w")
        Customer_Name=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
        Customer_Name.grid(row=4,column=1,pady=10,padx=10,sticky="w")
        
        Amount =Label(entry_frame,text="Amount",font=("times New roman",15,"bold"),bg="white",fg="black")
        Amount.grid(row=5,column=0,pady=10,padx=10,sticky="w")
        Amount=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
        Amount.grid(row=5,column=1,pady=10,padx=10,sticky="w")

        fardar_ID_label = Label(entry_frame, text="Fardar ID", font=("times new roman", 15, "bold"), bg="white", fg="black")
        fardar_ID_label.grid(row=0, column=2, pady=10, padx=10, sticky="w")
        fardar_ID = Entry(entry_frame, font=("times new roman", 15), bd=2, relief=RIDGE, width=17)
        fardar_ID.grid(row=0, column=3, pady=10, padx=10, sticky="w")





        add_button=Button(entry_frame,text="Add",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_fardar(date_entry.get(), Invoice_No_entry.get(), payment_combobox.get(), Customer_Name.get(), Delivery_date.get(), Amount.get(),fardar_ID.get() ,fardar_treeview))
        add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

        clear_button=Button(entry_frame,text="Clear",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_entries(date_entry, Invoice_No_entry, payment_combobox, Customer_Name, Delivery_date, Amount))
        clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

        delete_button=Button(entry_frame,text="Delete",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_expenses(fardar_treeview)) 
        delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")
        

        fardar_treeview.bind('<ButtonRelease-1>', lambda event: select_fardar_entry(event, fardar_treeview, date_entry, Invoice_No_entry, payment_combobox, Customer_Name,fardar_ID,Delivery_date, Amount))










        





