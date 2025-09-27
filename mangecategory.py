from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from manageProducts import connect_database



###THE FUNCTIONS#####

def add_category(category_ID, category_Name, description,category_treeview):
    if (category_ID == '' or category_Name == '' or description == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('CREATE TABLE IF NOT EXISTS category_data (category_ID VARCHAR(50) PRIMARY KEY, category_Name VARCHAR(100), description VARCHAR (500) )')
            cursor.execute('SELECT * FROM category_data WHERE category_ID=%s', (category_ID,))
            if cursor.fetchone():
                messagebox.showerror('Error', 'category_ID already exists')
                return
            cursor.execute('INSERT INTO category_data VALUES(%s,%s,%s)', (category_ID, category_Name, description))
            connection.commit()
            treeview_data(category_treeview)
            messagebox.showinfo('Success', 'Category added successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def treeview_data(category_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM category_data')
        customer_records = cursor.fetchall()
        category_treeview.delete(*category_treeview.get_children())
        for record in customer_records:  # here  is the important not to view the all the data in treeeview you must use the code
            category_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def select_data(category_ID, category_Name, description, category_treeview):
    index = category_treeview.selection()
    if not index:
        return
    content = category_treeview.item(index[0])
    actual_content = content['values']

    category_ID.delete(0, END)
    category_Name.delete(0, END)
    description.delete('1.0', END)

    if len(actual_content) > 0:
        category_ID.insert(0, actual_content[0])
    if len(actual_content) > 1:
        category_Name.insert(0, actual_content[1])
    if len(actual_content) > 2:
        description.insert('1.0', actual_content[2])







def clear_feilds(category_ID, category_Name, description,category_treeview,check):
    category_ID.delete(0, END)
    category_Name.delete(0, END)
    description.delete('1.0', END)

   
    if check:
        # to deselect the selected data in the treeview
        category_treeview.selection_remove(category_treeview.selection())

def delete_customer(category_ID, category_treeview):
    selected = category_treeview.selection()
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
                # Get the category_ID from the selected item in the treeview
                item = category_treeview.item(selected[0])
                selected_category_ID = item['values'][0]
                cursor.execute('DELETE FROM category_data WHERE category_ID=%s', (selected_category_ID,))
                connection.commit()
                treeview_data(category_treeview)
                messagebox.showinfo('Success', 'Category deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()

def ubdate_category(category_ID, category_Name, description, category_treeview):
    selected = category_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the record to update')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT * FROM category_data WHERE category_ID=%s', (category_ID,))
            current_data = cursor.fetchone()
            if current_data is None:
                messagebox.showerror('Error', 'Category not found for update')
                return
            # Get the current values for comparison
            current_data = current_data[1:]  # (category_Name, description)
            new_data = (category_Name, description)
            # Convert both tuples to strings for comparison
            if tuple(str(x).strip() for x in current_data) == tuple(str(x).strip() for x in new_data):
                messagebox.showerror('Error', 'No changes made to update')
                return

            cursor.execute('UPDATE category_data SET category_Name=%s, description=%s WHERE category_ID=%s',
                           (category_Name, description, category_ID))
            connection.commit()
            treeview_data(category_treeview)
            messagebox.showinfo('Success', 'Category data updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def search_category(category_ID, category_Name, category_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE attire_empire')
    try:
        query = 'SELECT * FROM category_data WHERE 1=1'
        params = []

        if category_ID:
            query += ' AND category_ID = %s'
            params.append(category_ID)
        if category_Name:
            query += ' AND category_Name LIKE %s'
            params.append(f'%{category_Name}%')

        cursor.execute(query, tuple(params))
        records = cursor.fetchall()

        category_treeview.delete(*category_treeview.get_children())
        for record in records:
            category_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()
    

    

def showall(category_ID, category_Name, category_treeview):
    treeview_data(category_treeview)
    category_ID.delete(0, END)
    category_Name.delete(0, END)

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE attire_empire')
    try:
        cursor.execute('SELECT * FROM category_data')
        customer_records = cursor.fetchall()
        category_treeview.delete(*category_treeview.get_children())
        for record in customer_records:
            category_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()













def managecat(window):
    
    cate_frame = Toplevel(window)
    cate_frame.title("Manage Category")
    cate_frame.geometry("1500x780+330+175")
    cate_frame.configure(bg="white")
    cate_frame.resizable(True, True)

    #the title label
    title_label=Label(cate_frame,text="Manage Category",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=BOTH,expand=1)

    #the treeview frame 

    treeview_frame = Frame(cate_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    category_treeview=ttk.Treeview(treeview_frame,columns=("Category_ID","Category_Name","Description"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=category_treeview.yview)
    scrollx.config(command=category_treeview.xview)
    category_treeview.heading("Category_ID",text="Category ID")
    category_treeview.heading("Category_Name",text="Category Name")
    category_treeview.heading("Description",text="Description")

    category_treeview.column("Category_ID",width=150)
    category_treeview.column("Category_Name",width=150)
    category_treeview.column("Description",width=100)
    treeview_data(category_treeview)  # Load initial data into the treeview
    category_treeview.pack(fill=BOTH,expand=1)

    #entry frame 
    entry_frame = Frame(cate_frame,width=1050,height=330,bg="white")
    entry_frame.pack(side=TOP,fill=BOTH,expand=1)

    CategoryID_label =Label(entry_frame,text="Category ID",font=("times new roman",15,"bold"),bg="white",fg="black")
    CategoryID_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    CategoryID_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    CategoryID_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    CategoryName_label =Label(entry_frame,text="Category Name",font=("times new roman",15,"bold"),bg="white",fg="black")
    CategoryName_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    CategoryName_entry=Entry(entry_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    CategoryName_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    description_label = Label(entry_frame, text="Description", font=("times new roman", 15, "bold"), bg="white", fg="black")
    description_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
    description = Text(entry_frame, font=("times new roman", 11), bd=2, relief=RIDGE, width=17, height=3)
    description.grid(row=2, column=1, pady=10, padx=10, sticky="w")


    add_button=Button(entry_frame,text="Add",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:add_category(CategoryID_entry.get(),CategoryName_entry.get(),description.get("1.0", END).strip(),category_treeview))
    add_button.grid(row=5,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(entry_frame,text="Clear",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_feilds(CategoryID_entry, CategoryName_entry, description, category_treeview, True))
    clear_button.grid(row=5,column=3,pady=10,padx=10,sticky="w")

    delete_button=Button(entry_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_customer(CategoryID_entry.get(), category_treeview))
    delete_button.grid(row=5,column=4,pady=10,padx=10,sticky="w")

    update_button=Button(entry_frame,text="Update",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:ubdate_category(CategoryID_entry.get(), CategoryName_entry.get(), description.get("1.0", END).strip(), category_treeview))
    update_button.grid(row=5,column=5,pady=10,padx=10,sticky="w")

    search_button=Button(entry_frame,text="Search",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: search_category(CategoryID_entry.get(), CategoryName_entry.get(),category_treeview))
    search_button.grid(row=0,column=2,pady=10,padx=10,sticky="w")

    showall_button=Button(entry_frame,text="Show All",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: showall(CategoryID_entry, CategoryName_entry, category_treeview))
    showall_button.grid(row=0,column=3,pady=10,padx=10,sticky="w")
    
    category_treeview.bind('<ButtonRelease-1>', lambda event: select_data(CategoryID_entry, CategoryName_entry, description, category_treeview))






#to do 23 june 2025
#the texting in the category and correct the error 
#euoghr data base setting 


    





