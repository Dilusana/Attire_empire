from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
import os
import inspect


#functional Part 

def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost', user='root', password='20020615Az@')
        cursor = connection.cursor()
        # Ensure the database exists before using it
        cursor.execute('CREATE DATABASE IF NOT EXISTS attire_empire')
        cursor.execute('USE attire_empire')
    except Exception as e:
        messagebox.showerror(
            'Error', f'Database connection failed: {e}\nTry Again, Please open MySQL command line client.')
        return None, None

    return cursor, connection

def create_database_table():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('CREATE DATABASE IF NOT EXISTS attire_empire')
        cursor.execute('USE attire_empire')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_data (
                Product_ID INT PRIMARY KEY,
                Product_Name VARCHAR(200),
                INR_Price INT,
                Duety_Charge INT,
                Cost INT,
                Profit INT,
                Selling_Price INT,
                Remark VARCHAR(250),
                Size VARCHAR(150),
                Gram INT,
                Category VARCHAR(250),
                Supplier VARCHAR(100)
            )
        ''')
        connection.commit()
    except Exception as e:
        messagebox.showerror('Error', f'Error creating table: {e}')
    finally:
        cursor.close()
        connection.close()







def add_product(Product_ID,Product_Name,INR_Price,Duety_Charge,Cost,Profit,Selling_Price,Remark,Size,Gram,Category,Supplier,product_treeview):
    if (Product_ID == '' or Product_Name == '' or INR_Price == '' or Duety_Charge == '' or Cost == '' or Profit == '' or Selling_Price == '' or Remark == '' or Size == 'Select Size' or Gram == '' or Category == 'Select Category' or Supplier == 'Select'):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE attire_empire')
        try:
            
            cursor.execute(
                'SELECT * FROM product_data WHERE Product_ID=%s', (Product_ID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Product_ID already exists')
                return
            cursor.execute('INSERT INTO product_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (Product_ID, Product_Name,
                           INR_Price, Duety_Charge, Cost, Profit, Selling_Price, Remark, Size, Gram, Category, Supplier))
            connection.commit()
            treeview_data(product_treeview)
            
            messagebox.showinfo('Success', 'Product added successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_data(product_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM product_data')
        product_records = cursor.fetchall()
        product_treeview.delete(*product_treeview.get_children())
        for record in product_records:  # here  is the important not to view the all the data in treeeview you must use the code
            product_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(event, productID_entry, productName_entry, INR_entry, duety_charge_entry, cost_entry,
                Profit_entry, sellingPrice_entry, Remark_entry, size_combobox, gram_entry,
                rate_entry, 
                category_combobox, supplier_combobox, product_treeview):

    selected = product_treeview.selection()
    if not selected:
        return

    content = product_treeview.item(selected[0])
    row = content['values']

    clear_feilds(productID_entry, productName_entry, INR_entry, duety_charge_entry, cost_entry,
                 Profit_entry, sellingPrice_entry, Remark_entry, size_combobox, gram_entry,
                 rate_entry, 
                 category_combobox, supplier_combobox, product_treeview, False)

    if len(row) < 12:
        return

    productID_entry.insert(0, row[0])
    productName_entry.insert(0, row[1])
    INR_entry.insert(0, row[2])
    duety_charge_entry.insert(0, row[3])
    cost_entry.insert(0, row[4])
    Profit_entry.insert(0, row[5])
    sellingPrice_entry.insert(0, row[6])
    Remark_entry.insert(0, row[7])
    size_combobox.set(row[8])
    gram_entry.insert(0, row[9])
    category_combobox.set(row[10])
    supplier_combobox.set(row[11])



def clear_feilds(productID_entry, productName_entry, INR_entry, duety_charge_entry, cost_entry,
                 Profit_entry, sellingPrice_entry, Remark_entry, size_combobox, gram_entry,
                 rate_entry, 
                 category_combobox, supplier_combobox,
                 product_treeview, check):

    productID_entry.delete(0, END)
    productName_entry.delete(0, END)
    INR_entry.delete(0, END)
    duety_charge_entry.delete(0, END)
    cost_entry.delete(0, END)
    Profit_entry.delete(0, END)
    sellingPrice_entry.delete(0, END)
    Remark_entry.delete(0, END)
    size_combobox.set('Select Size')
    gram_entry.delete(0, END)
    rate_entry.delete(0, END)
    category_combobox.set('Select Category')
    supplier_combobox.set('Select')


    if check:
        product_treeview.selection_remove(product_treeview.selection())


def delete_product(product_ID,product_treeview):
    selected = product_treeview.selection()
    if not selected:
        messagebox.showerror('Error','Please select the record to delete ')
    else:
        result = messagebox.askyesno('Confirm','Do you want to delete this record?')
        if result:
            cursor, connection = connect_database()
            if not  cursor or not connection:
                return
            try:
                cursor.execute('USE attire_empire')
                cursor.execute('DELEte FROM product_data WHERE product_ID=%s',(product_ID,))
                connection.commit()
            
                treeview_data(product_treeview)
                messagebox.showinfo('Success', 'Product deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()





def ubdate_product(Product_ID,Product_Name,INR_Price,Duety_Charge,Cost,Profit,Selling_Price,Remark,Size,Gram,Category,Supplier,product_treeview):
    selected= product_treeview.selection()
    if not selected:
        messagebox.showerror('Error','Please select the record to update')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT * FROM product_data WHERE product_ID=%s',(Product_ID,))
            current_data = cursor.fetchone()
            if current_data is None:
                messagebox.showerror('Error', 'Product not found for update')
                return
            current_data = current_data[1:] # get the current value of the data 
            Size = Size.strip()
            new_data = (Product_Name,INR_Price,Duety_Charge,Cost,Profit,Selling_Price,Remark,Size,Gram,Category,Supplier)
            # Convert both tuples to strings for comparison
            if tuple(str(x) for x in current_data) == tuple(str(x) for x in new_data):
                messagebox.showerror('Error','No changes made to update')
                return
            cursor.execute('UPDATE product_data SET Product_Name=%s,INR_Price=%s,Duety_Charge=%s,Cost=%s,Profit=%s,Selling_Price=%s,Remark=%s,Size=%s,Gram=%s,Category=%s,Supplier=%s WHERE Product_ID = %s',(Product_Name,INR_Price,Duety_Charge,Cost,Profit,Selling_Price,Remark,Size,Gram,Category,Supplier,Product_ID))
            connection.commit()
            treeview_data(product_treeview)
            messagebox.showinfo('Success', 'Product data updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()
            
def cost_calcultion(INR_entry, duety_charge_entry, cost_entry, rate_entry, sellingPrice_entry, profit_entry):
    try:
        INR_price = float(INR_entry.get())
        duety_charge = float(duety_charge_entry.get())
        rate = float(rate_entry.get())
        profit = float(profit_entry.get())

        cost = (INR_price * rate) + duety_charge
        selling_price = cost + profit

        cost_entry.delete(0, END)
        cost_entry.insert(0, str(round(cost, 2)))

        sellingPrice_entry.delete(0, END)
        sellingPrice_entry.insert(0, str(round(selling_price, 2)))

    except ValueError:
        cost_entry.delete(0, END)
        sellingPrice_entry.delete(0, END)



        
def selling_price_calculation(cost_entry, Profit_entry, sellingPrice_entry):
    try:
        cost = float(cost_entry.get())
        profit= float(Profit_entry.get())
        selling_price=cost+profit
        sellingPrice_entry.delete(0,END)
        sellingPrice_entry.insert(0, str(selling_price))
    except ValueError:
        sellingPrice_entry.delete(0, END)






def fetch_supplier_category(catgeroy_combobox, supplier_combobox):
    category_option = []
    supplier_option = []

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE attire_empire')
        cursor.execute('SELECT DISTINCT category_Name FROM category_data')
        categories = cursor.fetchall()
        if categories:
            catgeroy_combobox.set('Select Category')
            for category in categories:
                category_option.append(category[0])
            catgeroy_combobox.config(values=category_option)

        cursor.execute('SELECT DISTINCT supplier_Name FROM supplier_data')
        suppliers = cursor.fetchall()
        if suppliers:
            supplier_combobox.set('Select')
            for supplier in suppliers:
                supplier_option.append(supplier[0])
            supplier_combobox.config(values=supplier_option)
    except Exception as e:
        messagebox.showerror('Error', f'Error fetching categories or suppliers: {e}')
    finally:
        cursor.close()
        connection.close()


def search_product(productID_entry, productName_entry,INR_entry, duety_charge_entry, cost_entry, Profit_entry, sellingPrice_entry, Remark_entry, size_combobox,gram_entry, category_combobox, supplier_combobox,product_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE attire_empire')
    try:
        query = 'SELECT * FROM product_data WHERE 1=1'
        params = []

        if productID_entry:
            query += ' AND Product_ID = %s'
            params.append(productID_entry)
        if productName_entry:
            query += ' AND Product_Name LIKE %s'
            params.append(f'%{productName_entry}%')
        if INR_entry:
            query += ' AND INR_Price = %s'
            params.append(INR_entry)
        if duety_charge_entry:
            query += ' AND Duety_Charge = %s'
            params.append(duety_charge_entry)
        if cost_entry:
            query += ' AND Cost = %s'
            params.append(cost_entry)
        if Profit_entry:
            query += ' AND Profit = %s'
            params.append(Profit_entry)
        if sellingPrice_entry:
            query += ' AND Selling_Price = %s'
            params.append(sellingPrice_entry)
        if Remark_entry:
            query += ' AND Remark LIKE %s'
            params.append(f'%{Remark_entry}%')
        if size_combobox and size_combobox != 'Select Size':
            query += ' AND Size = %s'
            params.append(size_combobox)
        if gram_entry:
            query += ' AND Gram = %s'
            params.append(gram_entry)
        if category_combobox and category_combobox != 'Select Category':
            query += ' AND Category = %s'
            params.append(category_combobox)
        if supplier_combobox and supplier_combobox != 'Select':
            query += ' AND Supplier = %s'
            params.append(supplier_combobox)

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        # Find the product_treeview from the caller's context
        frame = inspect.currentframe().f_back
        product_treeview = frame.f_locals.get('product_treeview')
        if product_treeview:
            product_treeview.delete(*product_treeview.get_children())
            for record in records:
                product_treeview.insert('', END, values=record)
        else:
            messagebox.showerror('Error', 'Treeview not found for displaying results')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()
    

    

def showall(productID_entry, productName_entry,INR_entry, duety_charge_entry, cost_entry, Profit_entry, sellingPrice_entry, Remark_entry, size_combobox,gram_entry, category_combobox, supplier_combobox,product_treeview):
    treeview_data(product_treeview)
    productID_entry.delete(0, END)
    productName_entry.delete(0, END)
    INR_entry.delete(0, END)
    duety_charge_entry.delete(0, END)
    cost_entry.delete(0,END)
    Profit_entry.delete(0, END)
    sellingPrice_entry.delete(0, END)
    Remark_entry.delete(0, END)
    size_combobox.set('Select Size')
    gram_entry.delete(0, END)
    category_combobox.set('Select Category')
    supplier_combobox.set('Select')

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM product_data')
        product_records = cursor.fetchall()
        product_treeview.delete(*product_treeview.get_children())
        for record in product_records:  # here  is the important not to view the all the data in treeeview you must use the code
            product_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()




####GUI#####

def managingproduct(window):
    
    product_window = Toplevel(window)
    product_window.title("Manage products")
    product_window.geometry("1500x780+330+175")
    product_window.configure(bg="white")
    product_window.resizable(True, True)
    #the title label
    
    title_label=Label(product_window,text="Manage Products",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)

    #the treeview frame 

    treeview_frame = Frame(product_window,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    product_treeview=ttk.Treeview(treeview_frame,columns=("Product_ID","Product_Name","INR_Price_₹","Duety_Charge","Cost","Profit","Selling_Price","Remark","Size","Stock","Category","Supplier"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=product_treeview.yview)
    scrollx.config(command=product_treeview.xview)
    product_treeview.heading("Product_ID",text="Product ID")
    product_treeview.heading("Product_Name",text="Product Name")
    product_treeview.heading("INR_Price_₹",text="INR Price ₹")
    product_treeview.heading("Duety_Charge",text="Duety Charge")
    product_treeview.heading("Cost",text="Cost")#have to calculate automatically 
    product_treeview.heading("Profit",text="Profit")
    product_treeview.heading("Selling_Price",text="Selling Price")#have to calculate automatically 
    product_treeview.heading("Remark",text="Remark")
    product_treeview.heading("Size",text="Size")#combo boxx
    product_treeview.heading("Stock",text="Stock")#combo box
    product_treeview.heading("Category",text="Category")#combo box 
    product_treeview.heading("Supplier",text="Supplier")#combo box

    product_treeview.column("Product_ID",width=150)
    product_treeview.column("Product_Name",width=150)
    product_treeview.column("INR_Price_₹",width=100)
    product_treeview.column("Duety_Charge",width=100)
    product_treeview.column("Cost",width=100)
    product_treeview.column("Profit",width=130)
    product_treeview.column("Selling_Price",width=190)
    product_treeview.column("Remark",width=100)
    product_treeview.column("Size",width=50)
    product_treeview.column("Stock",width=50)
    product_treeview.column("Category",width=100)
    product_treeview.column("Supplier",width=100)
    
    treeview_data(product_treeview)
    product_treeview.pack(fill=BOTH,expand=1)
    

    #entry frame 
    entry_frame = Frame(product_window,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=X,pady=10)

    productID_label =Label(entry_frame,text="Product ID",font=("times New roman",11,"bold"),bg="white",fg="black")
    productID_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    productID_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    productID_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    productName_label =Label(entry_frame,text="Product Name",font=("times New roman",11,"bold"),bg="white",fg="black")
    productName_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    productName_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    productName_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    INR_label =Label(entry_frame,text="INR Price ₹",font=("times New roman",11,"bold"),bg="white",fg="black")
    INR_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    INR_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    INR_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    rate_label =Label(entry_frame,text="INR Rate ",font=("times New roman",11,"bold"),bg="white",fg="black")
    rate_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    rate_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    rate_entry.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    duety_charge_label =Label(entry_frame,text="Duety Charge",font=("times New roman",11,"bold"),bg="white",fg="black")
    duety_charge_label.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    duety_charge_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    duety_charge_entry.grid(row=4,column=1,pady=10,padx=10,sticky="w")


    cost_label =Label(entry_frame,text="Cost",font=("times New roman",11,"bold"),bg="white",fg="black")
    cost_label.grid(row=5,column=0,pady=10,padx=10,sticky="w")
    cost_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    cost_entry.grid(row=5,column=1,pady=10,padx=10,sticky="w")

    Profit_label =Label(entry_frame,text="Profit",font=("times New roman",11,"bold"),bg="white",fg="black")
    Profit_label.grid(row=6,column=0,pady=10,padx=10,sticky="w")
    Profit_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Profit_entry.grid(row=6,column=1,pady=10,padx=10,sticky="w")







    Remark_label =Label(entry_frame,text="Remark",font=("times New roman",11,"bold"),bg="white",fg="black")
    Remark_label.grid(row=0,column=2,pady=10,padx=10,sticky="w")
    Remark_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Remark_entry.grid(row=0,column=3,pady=10,padx=10,sticky="w")

    size_label =Label(entry_frame,text="Size",font=("times New roman",11,"bold"),bg="white",fg="black")
    size_label.grid(row=1,column=2,pady=10,padx=10,sticky="w")
    size_combobox=ttk.Combobox(entry_frame,font=("times New roman",11,"bold"),values=["S","M","L","XL","XLL","XLL"],width=13,state="readonly")
    size_combobox.grid(row=1,column=3,pady=10,padx=10,sticky="w")
    size_combobox.set("Select Size")

    gram_label =Label(entry_frame,text="Stock",font=("times New roman",11,"bold"),bg="white",fg="black")
    gram_label.grid(row=2,column=2,pady=10,padx=10,sticky="w")
    gram_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    gram_entry.grid(row=2,column=3,pady=10,padx=10,sticky="w")

    supplier_label =Label(entry_frame,text="Supplier",font=("times New roman",11,"bold"),bg="white",fg="black")
    supplier_label.grid(row=3,column=2,pady=10,padx=10,sticky="w")
    supplier_combobox=ttk.Combobox(entry_frame,font=("times New roman",11,"bold"),values=["empty","empty2"],width=13,state="readonly")
    supplier_combobox.grid(row=3,column=3,pady=10,padx=10,sticky="w")
    supplier_combobox.set("Select")

    category_label =Label(entry_frame,text="Categories",font=("times New roman",11,"bold"),bg="white",fg="black")
    category_label.grid(row=4,column=2,pady=10,padx=10,sticky="w")
    category_combobox=ttk.Combobox(entry_frame,font=("times New roman",11,"bold"),width=13,state="readonly")
    category_combobox.grid(row=4,column=3,pady=10,padx=10,sticky="w")
    category_combobox.set("Select Category")
    
    sellingPrice_label =Label(entry_frame,text="Selling Price",font=("times New roman",15,"bold"),bg="white",fg="black")
    sellingPrice_label.grid(row=5,column=2,pady=10,padx=10,sticky="w")
    sellingPrice_entry=Entry(entry_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    sellingPrice_entry.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    # Bind cost calculation to INR and Duety Charge entry changes
    def update_cost(event=None):
        cost_calcultion(INR_entry, duety_charge_entry, cost_entry, rate_entry,sellingPrice_entry,Profit_entry)

    INR_entry.bind("<KeyRelease>", update_cost)
    duety_charge_entry.bind("<KeyRelease>", update_cost)
    rate_entry.bind("<KeyRelease>", update_cost)
    sellingPrice_entry.bind("<KeyRelease>", update_cost)
    Profit_entry.bind("<KeyRelease>", update_cost)





    # Now fetch supplier and category options after comboboxes are created
    fetch_supplier_category(category_combobox, supplier_combobox)

    add_button=Button(entry_frame,text="Add",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_product(productID_entry.get(), productName_entry.get(),INR_entry.get(), duety_charge_entry.get(), cost_entry.get(), Profit_entry.get(), sellingPrice_entry.get(), Remark_entry.get(), size_combobox.get(), gram_entry.get(), category_combobox.get(), supplier_combobox.get(),product_treeview))
    add_button.grid(row=0,column=4,pady=10,padx=10,sticky="w")
    clear_button=Button(entry_frame,text="Clear",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_feilds(productID_entry, productName_entry,INR_entry, duety_charge_entry, cost_entry, Profit_entry, sellingPrice_entry, Remark_entry, size_combobox,gram_entry, category_combobox, supplier_combobox,rate_entry,product_treeview,True))
    clear_button.grid(row=1,column=4,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_product(productID_entry.get(),product_treeview))
    delete_button.grid(row=2,column=4,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:ubdate_product(productID_entry.get(), productName_entry.get(),INR_entry.get(), duety_charge_entry.get(), cost_entry.get(), Profit_entry.get(), sellingPrice_entry.get(), Remark_entry.get(), size_combobox.get(), gram_entry.get(), category_combobox.get(), supplier_combobox.get(),product_treeview))
    update_button.grid(row=3,column=4,pady=10,padx=10,sticky="w")

    search_button=Button(entry_frame,text="Search",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:search_product(productID_entry.get(), productName_entry.get(),INR_entry.get(), duety_charge_entry.get(), cost_entry.get(), Profit_entry.get(), sellingPrice_entry.get(), Remark_entry.get(), size_combobox.get(), gram_entry.get(), category_combobox.get(), supplier_combobox.get(),product_treeview))
    search_button.grid(row=0,column=5,pady=10,padx=10,sticky="w")

    showall_button=Button(entry_frame,text="Show All",font=("times new roman",11,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:showall(productID_entry, productName_entry,INR_entry, duety_charge_entry, cost_entry, Profit_entry, sellingPrice_entry, Remark_entry, size_combobox,gram_entry, category_combobox, supplier_combobox,product_treeview))
    showall_button.grid(row=1,column=5,pady=10,padx=10,sticky="w")

    product_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, productID_entry, productName_entry, INR_entry, duety_charge_entry, cost_entry, Profit_entry, sellingPrice_entry, Remark_entry, size_combobox, gram_entry, rate_entry, category_combobox, supplier_combobox, product_treeview))

    create_database_table()







    





