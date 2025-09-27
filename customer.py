from tkinter import *
from tkinter import ttk
from manageProducts import connect_database
from tkinter import messagebox




def add_customer(customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, customer_treeview):
    if (customer_ID == '' or customer_Name == '' or customer_address == '' or Contact_Number == '' or Remark == '' or Sizes == '' or balance == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS customer_data (customer_ID VARCHAR(50) PRIMARY KEY, customer_Name VARCHAR(100), customer_address VARCHAR(200), Contact_Number VARCHAR(15), Remark TEXT, Sizes VARCHAR(50), balance DECIMAL(10, 2))')
            cursor.execute('SELECT * FROM customer_data WHERE customer_ID=%s', (customer_ID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'customer_ID already exists')
                return
            cursor.execute('INSERT INTO customer_data VALUES(%s,%s,%s,%s,%s,%s,%s)', (customer_ID, customer_Name,
                           customer_address, Contact_Number, Remark, Sizes, balance))
            connection.commit()
            treeview_data(customer_treeview)
            messagebox.showinfo('Success', 'Customer  added successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_data(customer_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM customer_data')
        customer_records = cursor.fetchall()
        customer_treeview.delete(*customer_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            customer_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event,customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, customer_treeview):
    index= customer_treeview.selection()
    content=customer_treeview.item(index)
    actual_content =content['values']

    customer_ID.delete(0,END)
    customer_Name.delete(0,END)
    customer_address.delete(0,END)
    Contact_Number.delete(0,END)
    Remark.delete(0,END)
    Sizes.delete(0,END)
    balance.delete(0,END)

    customer_ID.insert(0,actual_content[0])
    customer_Name.insert(0,actual_content[1])
    customer_address.insert(0,actual_content[2])
    Contact_Number.insert(0,actual_content[3])
    Remark.insert(0,actual_content[4])
    Sizes.insert(0,actual_content[5])
    balance.insert(0,actual_content[6])








def clear_feilds(customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance,payment, customer_treeview,check):
    customer_ID.delete(0, END)
    customer_Name.delete(0, END)
    customer_address.delete(0, END)
    Contact_Number.delete(0, END)
    Remark.delete(0,END)
    Sizes.delete(0, END)
    balance.delete(0, END)
    payment.delete(0, END)
   
    if check:
        # to deselect the selected data in the treeview
        customer_treeview.selection_remove(customer_treeview.selection())

def delete_customer(customer_ID, customer_treeview):
    selected = customer_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the record to delete ')
    else:
        result = messagebox.askyesno('Confirm', 'Do you want to delete this record?')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE attire_empire')
                # Get the customer_ID from the selected item in the treeview
                item = customer_treeview.item(selected[0])
                selected_customer_ID = item['values'][0]
                cursor.execute('DELETE FROM customer_data WHERE customer_ID=%s', (selected_customer_ID,))
                connection.commit()
                treeview_data(customer_treeview)
                messagebox.showinfo('Success', 'Customer deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()





def update_customer(customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, payment, customer_treeview):
    selected = customer_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select a record to update')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE attire_empire')

        # Fetch current data for the selected customer_ID
        cursor.execute('SELECT * FROM customer_data WHERE customer_ID = %s', (customer_ID,))
        current_data = cursor.fetchone()

        if current_data is None:
            messagebox.showerror('Error', 'Customer not found for update')
            return

        # Assume current_data order: (customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance)
        existing_data = current_data[1:-1]  # exclude customer_ID and balance
        existing_balance = float(current_data[-1])  # last field is balance

        Sizes = Sizes.strip()

        # Convert input values to string for comparison (except balance)
        new_data = (customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, payment )

        if tuple(str(x) for x in existing_data) == tuple(str(x) for x in new_data) and float(balance) == existing_balance:
            messagebox.showerror('Error', 'No changes detected to update')
            return

        # Safely convert payment and balance
        try:
            balance = float(balance)
            payment = float(payment)
        except ValueError:
            messagebox.showerror("Input Error", "Balance and Payment must be numeric values.")
            return

        # Adjust balance
        updated_balance = balance - payment

        # Perform the update
        cursor.execute(
            '''UPDATE customer_data 
               SET customer_Name = %s, customer_address = %s, Contact_Number = %s, 
                   Remark = %s, Sizes = %s, balance = %s 
               WHERE customer_ID = %s''',
            (customer_Name, customer_address, Contact_Number, Remark, Sizes, updated_balance, customer_ID)
        )

        connection.commit()
        treeview_data(customer_treeview)
        messagebox.showinfo('Success', 'Customer data updated successfully')

    except Exception as e:
        messagebox.showerror('Error', f'Error occurred: {e}')
    finally:
        cursor.close()
        connection.close()


def show_customer_data(customer_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        cursor.execute("SELECT * FROM customer_data")
        rows = cursor.fetchall()

        # Clear previous data in treeview
        for item in customer_treeview.get_children():
            customer_treeview.delete(item)

        # Insert new data into the treeview
        for row in rows:
            customer_treeview.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load customer data: {e}")
    finally:
        cursor.close()
        connection.close()


def search_customer(customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, customer_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE attire_empire')
    try:
        query = 'SELECT * FROM customer_data WHERE 1=1'
        params = []

        if customer_ID:
            query += ' AND customer_ID LIKE %s'
            params.append(f'%{customer_ID}%')
        if customer_Name:
            query += ' AND customer_Name LIKE %s'
            params.append(f'%{customer_Name}%')
        if customer_address:
            query += ' AND customer_address LIKE %s'
            params.append(f'%{customer_address}%')
        if Contact_Number:
            query += ' AND Contact_Number LIKE %s'
            params.append(f'%{Contact_Number}%')
        if Remark:
            query += ' AND Remark LIKE %s'
            params.append(f'%{Remark}%')
        if Sizes:
            query += ' AND Sizes LIKE %s'
            params.append(f'%{Sizes}%')
        if balance:
            query += ' AND balance LIKE %s'
            params.append(f'%{balance}%')

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        customer_treeview.delete(*customer_treeview.get_children())
        for record in records:
            customer_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

    

def showall(customer_ID,customer_Name,customer_address, Contact_Number, Remark, Sizes, balance,customer_treeview):
    treeview_data(customer_treeview)
    customer_ID.delete(0, END)
    customer_Name.delete(0, END)
    customer_address.delete(0, END)
    Contact_Number.delete(0, END)
    Remark.delete(0,END)
    Sizes.delete(0, END)
    balance.delete(0, END)
    

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM customer_data')
        customer_records = cursor.fetchall()
        customer_treeview.delete(*customer_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            customer_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()






def customer_form(window):
    customer_frame = Toplevel(window)
    customer_frame.title("Customer Details")
    customer_frame.geometry("1225x960+500+10")
    customer_frame.configure(bg="white")
    customer_frame.resizable(False, False)

    close_image = PhotoImage(file='assests/close.png')
    close_button = Button(customer_frame, image=close_image, bg="white", bd=0, command=customer_frame.destroy)
    close_button.image = close_image
    close_button.place(x=880, y=10)
    #------------------------------------------------------------------------------------------------------------------------

    heading_label=Label(customer_frame,text="Customer Details",font=("Times new roman",25,"bold"),fg="black",anchor="w",bg="white")
    heading_label.pack(fill=X,pady=10)



    #the treeview frame------------------------------------------------------------------------------------------
    customer_treeview_frame = Frame(customer_frame,bg="white")
    customer_treeview_frame.pack(fill=BOTH,expand=1,pady=10)

    scrolly = Scrollbar(customer_treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(customer_treeview_frame, orient=HORIZONTAL)
    customer_treeview=ttk.Treeview(customer_treeview_frame,columns=("Cus_ID","Cus_Name","Cus_address","Cus_Number","Remark","Sizes","Balance"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=customer_treeview.yview)
    scrollx.config(command=customer_treeview.xview)
    customer_treeview.heading("Cus_ID",text="Customer ID")
    customer_treeview.heading("Cus_Name",text="Customer Name")
    customer_treeview.heading("Cus_address",text="Customer Address")
    customer_treeview.heading("Cus_Number",text="Contact Number")
    customer_treeview.heading("Remark",text="Remark")
    customer_treeview.heading("Sizes",text="Sizes")
    customer_treeview.heading("Balance",text="Balance")


    customer_treeview.column("Cus_ID",width=50)
    customer_treeview.column("Cus_Name",width=150)
    customer_treeview.column("Cus_address",width=100)
    customer_treeview.column("Cus_Number",width=100)
    customer_treeview.column("Remark",width=130)
    customer_treeview.column("Sizes",width=100)
    customer_treeview.column("Balance",width=90)
    show_customer_data(customer_treeview)

    customer_treeview.pack(fill=BOTH,expand=1)
    #-------------------------------------------------------------------------------------------------------------------
    #customers details 
    details_frame = Frame(customer_frame,width=910,height=280,bg="white")
    details_frame.pack(fill=BOTH,expand=1,pady=10)

    customerID_label =Label(details_frame,text="Customer ID",font=("times New roman",11,"bold"),bg="white",fg="black")
    customerID_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    customerID_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    customerID_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    customerName_label =Label(details_frame,text="Customer Name",font=("times New roman",11,"bold"),bg="white",fg="black")
    customerName_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    customerName_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    customerName_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    customerAddress_label =Label(details_frame,text="Customer Address",font=("times New roman",11,"bold"),bg="white",fg="black")
    customerAddress_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    customerAddress_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    customerAddress_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    contact_num_label =Label(details_frame,text="Contact Number",font=("times New roman",11,"bold"),bg="white",fg="black")
    contact_num_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    contact_num_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    contact_num_entry.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    balance_label =Label(details_frame,text="Due Payment",font=("times New roman",11,"bold"),bg="white",fg="black")
    balance_label.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    balance_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    balance_entry.grid(row=4,column=1,pady=10,padx=10,sticky="w")

    size_label =Label(details_frame,text="Sizes",font=("times New roman",11,"bold"),bg="white",fg="black")
    size_label.grid(row=0,column=2,pady=10,padx=10,sticky="w")
    size_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    size_entry.grid(row=0,column=3,pady=10,padx=10,sticky="w")

    remark_label =Label(details_frame,text="Remark",font=("times New roman",11,"bold"),bg="white",fg="black")
    remark_label.grid(row=1,column=2,pady=10,padx=10,sticky="w")
    remark_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    remark_entry.grid(row=1,column=3,pady=10,padx=10,sticky="w")

    payment_label =Label(details_frame,text="Now Paying",font=("times New roman",11,"bold"),bg="white",fg="black")
    payment_label.grid(row=2,column=2,pady=10,padx=10,sticky="w")
    payment_entry=Entry(details_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    payment_entry.grid(row=2,column=3,pady=10,padx=10,sticky="w")


    add_button=Button(details_frame,text="Add",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_customer(customerID_entry.get(), customerName_entry.get(), customerAddress_entry.get(), contact_num_entry.get(), remark_entry.get(), size_entry.get(), balance_entry.get(), customer_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(details_frame,text="Clear",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_feilds(customerID_entry, customerName_entry, customerAddress_entry, contact_num_entry, remark_entry, size_entry, balance_entry,payment_entry,customer_treeview,False))
    clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    delete_button=Button(details_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_customer(customerID_entry.get(),customer_treeview))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")

    Update_button=Button(details_frame,text="Update",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:update_customer(customerID_entry.get(), customerName_entry.get(), customerAddress_entry.get(), contact_num_entry.get(), remark_entry.get(), size_entry.get(), balance_entry.get(),payment_entry.get(), customer_treeview))
    Update_button.grid(row=5,column=5,pady=10,padx=10,sticky="w")

    
    search_button=Button(details_frame,text="Search",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: search_customer(customerID_entry.get(), customerName_entry.get(), customerAddress_entry.get(), contact_num_entry.get(), remark_entry.get(), size_entry.get(), balance_entry.get(), customer_treeview))
    search_button.grid(row=1,column=4,pady=10,padx=10,sticky="w")

    showall_button=Button(details_frame,text="Show All",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: showall(customerID_entry, customerName_entry, customerAddress_entry, contact_num_entry, remark_entry, size_entry, balance_entry,customer_treeview))
    showall_button.grid(row=1,column=5,pady=10,padx=10,sticky="w")

    customer_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, customerID_entry, customerName_entry, customerAddress_entry, contact_num_entry, remark_entry, size_entry, balance_entry, customer_treeview))




























