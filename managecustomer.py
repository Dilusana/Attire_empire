from tkinter import *
from tkinter import ttk
import pymysql
from manageProducts import connect_database
from tkinter import messagebox
import os
import inspect


###THE FUNCTIONS#####

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








def clear_feilds(customer_ID, customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, customer_treeview,check):
    customer_ID.delete(0, END)
    customer_Name.delete(0, END)
    customer_address.delete(0, END)
    Contact_Number.delete(0, END)
    Remark.delete(0,END)
    Sizes.delete(0, END)
    balance.delete(0, END)
   
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





def ubdate_customer(customer_ID,customer_Name,customer_address, Contact_Number, Remark, Sizes, balance,customer_treeview):
    selected= customer_treeview.selection()
    if not selected:
        messagebox.showerror('Error','Please select the record to update')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT * FROM customer_data WHERE customer_ID=%s',(customer_ID,))
            current_data = cursor.fetchone()
            if current_data is None:
                messagebox.showerror('Error', 'Product not found for update')
                return
            current_data = current_data[1:] # get the current value of the data 
            Sizes = Sizes.strip()
            new_data = (customer_Name, customer_address, Contact_Number, Remark, Sizes, balance)
            # Convert both tuples to strings for comparison
            if tuple(str(x) for x in current_data) == tuple(str(x) for x in new_data):
                messagebox.showerror('Error','No changes made to update')
                return

            cursor.execute('UPDATE customer_data SET customer_Name=%s,customer_address=%s,Contact_Number=%s,Remark=%s,Sizes=%s,balance=%s WHERE customer_ID = %s',
                        (customer_Name, customer_address, Contact_Number, Remark, Sizes, balance, customer_ID))
            connection.commit()
            treeview_data(customer_treeview)
            messagebox.showinfo('Success', 'Product data updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
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







######GUI######
def managecust(window):
    
    customer_window = Toplevel(window)
    customer_window.title("Manage Customer")
    customer_window.geometry("1500x780+330+175")
    customer_window.configure(bg="white")
    customer_window.resizable(True, True)


    #the title label
    title_label=Label(customer_window,text="Manage Customer",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(customer_window,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    customer_treeview=ttk.Treeview(treeview_frame,columns=("Customer_ID","Customer_Name","Customer_Address","Contact_Number","Remark","Sizes","Balance"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=customer_treeview.yview)
    scrollx.config(command=customer_treeview.xview)
    customer_treeview.heading("Customer_ID",text="Customer ID")
    customer_treeview.heading("Customer_Name",text="Customer Name")
    customer_treeview.heading("Customer_Address",text="Customer Address")
    customer_treeview.heading("Contact_Number",text="Contact Number")
    customer_treeview.heading("Remark",text="Remark")
    customer_treeview.heading("Sizes",text="Sizes")#combo boxx
    customer_treeview.heading("Balance",text="Balance")#combo box

    customer_treeview.column("Customer_ID",width=150)
    customer_treeview.column("Customer_Name",width=150)
    customer_treeview.column("Customer_Address",width=100)
    customer_treeview.column("Contact_Number",width=100)
    customer_treeview.column("Remark",width=100)
    customer_treeview.column("Sizes",width=50)
    customer_treeview.column("Balance",width=50)
    treeview_data(customer_treeview)
    customer_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(customer_window,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    CustomerID_label =Label(entry_frame,text="Customer ID",font=("times New roman",11,"bold"),bg="white",fg="black")
    CustomerID_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    CustomerID_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    CustomerID_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    CustomerName_label =Label(entry_frame,text="Customer Name",font=("times New roman",11,"bold"),bg="white",fg="black")
    CustomerName_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    CustomerName_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    CustomerName_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    Customer_Address =Label(entry_frame,text="Customer Address",font=("times New roman",11,"bold"),bg="white",fg="black")
    Customer_Address.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    Customer_Address=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Customer_Address.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    Contact_Number =Label(entry_frame,text="Contact Number",font=("times New roman",11,"bold"),bg="white",fg="black")
    Contact_Number.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    Contact_Number=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Contact_Number.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    Remark =Label(entry_frame,text="Remark",font=("times New roman",11,"bold"),bg="white",fg="black")
    Remark.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    Remark=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Remark.grid(row=4,column=1,pady=10,padx=10,sticky="w")

    sizes_label =Label(entry_frame,text="sizes",font=("times New roman",11,"bold"),bg="white",fg="black")
    sizes_label.grid(row=5,column=0,pady=10,padx=10,sticky="w")
    sizes_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    sizes_entry.grid(row=5,column=1,pady=10,padx=10,sticky="w")


    balance_label =Label(entry_frame,text="Balance",font=("times New roman",20,"bold"),bg="white",fg="black")
    balance_label.grid(row=1,column=2,pady=10,padx=10,sticky="w")
    balance_entry=Entry(entry_frame,font=("times new roman",20),bd=2,relief=RIDGE,width=17)
    balance_entry.grid(row=1,column=3,pady=10,padx=10,sticky="w",columnspan=2)

    add_button=Button(entry_frame,text="Add",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: add_customer(CustomerID_entry.get(),CustomerName_entry.get(),Customer_Address.get(),Contact_Number.get(),Remark.get(),sizes_entry.get(),balance_entry.get(),customer_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(entry_frame,text="Clear",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_feilds(CustomerID_entry,CustomerName_entry,Customer_Address,Contact_Number,Remark,sizes_entry,balance_entry,customer_treeview,False))
    clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_customer(CustomerID_entry.get(),customer_treeview))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:ubdate_customer(CustomerID_entry.get(),CustomerName_entry.get(),Customer_Address.get(),Contact_Number.get(),Remark.get(),sizes_entry.get(),balance_entry.get(),customer_treeview))
    update_button.grid(row=5,column=5,pady=10,padx=10,sticky="w")

    search_button=Button(entry_frame,text="Search",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: search_customer(CustomerID_entry.get(),CustomerName_entry.get(),Customer_Address.get(),Contact_Number.get(),Remark.get(),sizes_entry.get(),balance_entry.get(),customer_treeview))
    search_button.grid(row=0,column=2,pady=10,padx=10,sticky="w")

    showall_button=Button(entry_frame,text="Show All",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: showall(CustomerID_entry,CustomerName_entry,Customer_Address,Contact_Number,Remark,sizes_entry,balance_entry,customer_treeview))
    showall_button.grid(row=0,column=3,pady=10,padx=10,sticky="w")

    customer_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, CustomerID_entry, CustomerName_entry, Customer_Address, Contact_Number, Remark, sizes_entry, balance_entry, customer_treeview))








    





