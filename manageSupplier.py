from tkinter import *
from tkinter import ttk
from manageProducts import connect_database
from tkinter import messagebox

# function to manage supplier 

def add_supplier(invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, supplier_treeview):
    if ( invoice_no== '' or supplier_ID == '' or supplier_Name == '' or supplier_address == '' or Contact_Number == '' or Description == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data (invoice_no VARCHAR(50) PRIMARY KEY, supplier_ID INT (100), supplier_Name VARCHAR(200), supplier_address VARCHAR(15), Contact_Number INT(100),Description TEXT)')
            cursor.execute('SELECT * FROM supplier_data WHERE invoice_no=%s', (invoice_no,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Invoice Number  already exists')
                return
            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s,%s,%s)', (invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description))
            connection.commit()
            treeview_data(supplier_treeview)
            messagebox.showinfo('Success', 'Supplier added successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_data(supplier_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM supplier_data')
        customer_records = cursor.fetchall()
        supplier_treeview.delete(*supplier_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            supplier_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, supplier_treeview):
    index= supplier_treeview.selection()
    content=supplier_treeview.item(index)
    actual_content =content['values']

    invoice_no.delete(0,END)
    supplier_ID.delete(0,END)
    supplier_Name.delete(0,END)
    supplier_address.delete(0,END)
    Contact_Number.delete(0,END)
    Description.delete(0,END)

    invoice_no.insert(0,actual_content[0])
    supplier_ID.insert(0,actual_content[1])
    supplier_Name.insert(0,actual_content[2])
    supplier_address.insert(0,actual_content[3])
    Contact_Number.insert(0,actual_content[4])
    Description.insert(0,actual_content[5])


def clear_feilds(invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, supplier_treeview,check):
    invoice_no.delete(0, END)
    supplier_ID.delete(0, END)
    supplier_Name.delete(0, END)
    supplier_address.delete(0, END)
    Contact_Number.delete(0,END)
    Description.delete(0, END)
   
    if check:
        # to deselect the selected data in the treeview
        supplier_treeview.selection_remove(supplier_treeview.selection())

def delete_supplier(invoice_no, supplier_treeview):
    selected = supplier_treeview.selection()
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
                item = supplier_treeview.item(selected[0])
                selected_customer_ID = item['values'][0]
                cursor.execute('DELETE FROM supplier_data WHERE invoice_no=%s', (selected_customer_ID,))
                connection.commit()
                treeview_data(supplier_treeview)
                messagebox.showinfo('Success', 'Invoice deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()




def ubdate_supplier(invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, supplier_treeview):
    selected= supplier_treeview.selection()
    if not selected:
        messagebox.showerror('Error','Please select the record to update')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT * FROM supplier_data WHERE invoice_no=%s',(invoice_no,))
            current_data = cursor.fetchone()
            if current_data is None:
                messagebox.showerror('Error', 'Product not found for update')
                return
            current_data = current_data[1:] # get the current value of the data 
            new_data = (invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description)
            # Convert both tuples to strings for comparison
            if tuple(str(x) for x in current_data) == tuple(str(x) for x in new_data):
                messagebox.showerror('Error','No changes made to update')
                return

            cursor.execute('UPDATE supplier_data SET supplier_ID=%s,supplier_Name=%s,supplier_address=%s,Contact_Number=%s,Description=%s WHERE invoice_no = %s',
                        (supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, invoice_no))
            connection.commit()
            treeview_data(supplier_treeview)
            messagebox.showinfo('Success', 'Product data updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def search_supplier(invoice_no,supplier_ID, supplier_Name, supplier_address, Contact_Number, Description, supplier_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE attire_empire')
    try:
        query = 'SELECT * FROM supplier_data WHERE 1=1'
        params = []

        if invoice_no:
            query += ' AND invoice_no = %s'
            params.append(invoice_no)
        if supplier_ID:
            query += ' AND supplier_ID = %s'
            params.append(supplier_ID)
        if supplier_Name:
            query += ' AND supplier_Name LIKE %s'
            params.append(f'%{supplier_Name}%')
        if supplier_address:
            query += ' AND supplier_address = %s'
            params.append(supplier_address)
        if Contact_Number:
            query += ' AND Contact_Number = %s'
            params.append(Contact_Number)
        if Description:
            query += ' AND Description LIKE %s'
            params.append(f'%{Description}%')

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        supplier_treeview.delete(*supplier_treeview.get_children())
        for record in records:
            supplier_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()
    

def showall(Invoice_NO_entry, SupplierID_entry, SupplierName_entry, Supplier_Address, Contact_Number, Description_entry, supplier_treeview):
    treeview_data(supplier_treeview)
    Invoice_NO_entry.delete(0, END)
    SupplierID_entry.delete(0, END)
    SupplierName_entry.delete(0, END)
    Supplier_Address.delete(0,END)
    Contact_Number.delete(0, END)
    Description_entry.delete(0, END)
    

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM supplier_data')
        customer_records = cursor.fetchall()
        supplier_treeview.delete(*supplier_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            supplier_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()



#gui######
def manageSup(window):
    
    supplier_frame = Toplevel(window)
    supplier_frame.title("Manage Supplier")
    supplier_frame.geometry("1500x780+330+175")
    supplier_frame.configure(bg="white")
    supplier_frame.resizable(True, True)
    #the title label
    title_label=Label(supplier_frame,text="Manage Supplier",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(supplier_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    supplier_treeview=ttk.Treeview(treeview_frame,columns=("Invoice_No","Supplier_ID","Supplier_Name","Supplier_Address","Contact_Number","Description"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=supplier_treeview.yview)
    scrollx.config(command=supplier_treeview.xview)
    supplier_treeview.heading("Invoice_No",text="Invoice No")
    supplier_treeview.heading("Supplier_ID",text="Supplier ID")
    supplier_treeview.heading("Supplier_Name",text="Supplier Name")
    supplier_treeview.heading("Supplier_Address",text="Supplier Address")
    supplier_treeview.heading("Contact_Number",text="Contact Number")
    supplier_treeview.heading("Description",text="Description")

    supplier_treeview.column("Invoice_No",width=150)
    supplier_treeview.column("Supplier_ID",width=150)
    supplier_treeview.column("Supplier_Name",width=100)
    supplier_treeview.column("Supplier_Address",width=100)
    supplier_treeview.column("Contact_Number",width=100)
    supplier_treeview.column("Description",width=100)
    treeview_data(supplier_treeview)  # Load initial data into the treeview
    supplier_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(supplier_frame,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    Invoice_NO_label =Label(entry_frame,text="Invoice NO",font=("times New roman",11,"bold"),bg="white",fg="black")
    Invoice_NO_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    Invoice_NO_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Invoice_NO_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")
    
    SupplierID_label =Label(entry_frame,text="Supplier ID",font=("times New roman",11,"bold"),bg="white",fg="black")
    SupplierID_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    SupplierID_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    SupplierID_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    SupplierName_label =Label(entry_frame,text="Supplier Name",font=("times New roman",11,"bold"),bg="white",fg="black")
    SupplierName_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    SupplierName_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    SupplierName_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    Supplier_Address =Label(entry_frame,text="Supplier Address",font=("times New roman",11,"bold"),bg="white",fg="black")
    Supplier_Address.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    Supplier_Address=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Supplier_Address.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    Contact_Number =Label(entry_frame,text="Contact Number",font=("times New roman",11,"bold"),bg="white",fg="black")
    Contact_Number.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    Contact_Number=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Contact_Number.grid(row=4,column=1,pady=10,padx=10,sticky="w")

    Description_label =Label(entry_frame,text="Description",font=("times New roman",11,"bold"),bg="white",fg="black")
    Description_label.grid(row=5,column=0,pady=10,padx=10,sticky="w")
    Description_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Description_entry.grid(row=5,column=1,pady=10,padx=10,sticky="w",columnspan=2)

    add_button=Button(entry_frame,text="Add",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_supplier(Invoice_NO_entry.get(),SupplierID_entry.get(),SupplierName_entry.get(),Supplier_Address.get(),Contact_Number.get(),Description_entry.get(),supplier_treeview))
    add_button.grid(row=6,column=0,pady=10,padx=10,sticky="w")

    clear_button=Button(entry_frame,text="Clear",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_feilds(Invoice_NO_entry, SupplierID_entry, SupplierName_entry, Supplier_Address, Contact_Number, Description_entry, supplier_treeview, True))
    clear_button.grid(row=6,column=1,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_supplier(Invoice_NO_entry.get(), supplier_treeview))
    delete_button.grid(row=6,column=2,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:ubdate_supplier(Invoice_NO_entry.get(),SupplierID_entry.get(),SupplierName_entry.get(),Supplier_Address.get(),Contact_Number.get(),Description_entry.get(),supplier_treeview))
    update_button.grid(row=6,column=3,pady=10,padx=10,sticky="w")

    search_button=Button(entry_frame,text="Search",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:search_supplier(Invoice_NO_entry.get(),SupplierID_entry.get(), SupplierName_entry.get(), Supplier_Address.get(), Contact_Number.get(), Description_entry.get(), supplier_treeview))
    search_button.grid(row=0,column=2,pady=10,padx=10,sticky="w")

    showall_button=Button(entry_frame,text="Show All",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:showall(Invoice_NO_entry, SupplierID_entry, SupplierName_entry, Supplier_Address, Contact_Number, Description_entry, supplier_treeview))
    showall_button.grid(row=0,column=3,pady=10,padx=10,sticky="w")
    
    supplier_treeview.bind('<ButtonRelease-1>', lambda event: select_data(Invoice_NO_entry, SupplierID_entry, SupplierName_entry, Supplier_Address, Contact_Number, Description_entry, supplier_treeview))












    





