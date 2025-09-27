from tkinter import *
from tkinter import ttk
from manageProducts import connect_database
from tkinter import messagebox
from fpdf import FPDF
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

def show_customer_data(sales_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        cursor.execute("SELECT * FROM sales_data")
        rows = cursor.fetchall()

        # Clear previous data in treeview
        for item in sales_treeview.get_children():
            sales_treeview.delete(item)

        # Insert new data into the treeview
        for row in rows:
            sales_treeview.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load customer data: {e}")
    finally:
        cursor.close()
        connection.close()
        
def search_customer_data(invoice_no, customer_name, payment_method, month, product_name, product_id, sales_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        query = "SELECT * FROM sales_data WHERE 1=1"
        params = []

        if invoice_no:
            query += " AND Invoice_number LIKE %s"
            params.append(f"%{invoice_no}%")

        if customer_name:
            query += " AND name LIKE %s"
            params.append(f"%{customer_name}%")

        if payment_method and payment_method != "Select":
            query += " AND payment = %s"
            params.append(payment_method)

        if month and month != "Select Month":
            query += " AND MONTHNAME(ordered_date) = %s"
            params.append(month)

        if product_name:
            query += " AND productname LIKE %s"
            params.append(f"%{product_name}%")

        if product_id:
            query += " AND productID LIKE %s"
            params.append(f"%{product_id}%")

        # Debugging tip (optional): print query and params
        # print("QUERY:", query)
        # print("PARAMS:", params)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        # Clear existing rows in treeview
        sales_treeview.delete(*sales_treeview.get_children())

        # Insert new search results
        for row in rows:
            sales_treeview.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to search customer data: {e}")
    finally:
        cursor.close()
        connection.close()

def show_customer_data(sales_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        cursor.execute("SELECT * FROM sales_data")
        rows = cursor.fetchall()

        # Clear previous data in treeview
        for item in sales_treeview.get_children():
            sales_treeview.delete(item)

        # Insert new data into the treeview
        for row in rows:
            sales_treeview.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load customer data: {e}")
    finally:
        cursor.close()
        connection.close()

def clear(invoiceNO_entry, name_entry, payment_combobox, month_combobox, Product_name_entry, Product_ID_entry,sales_treeview):
    invoiceNO_entry.delete(0, END)
    name_entry.delete(0, END)
    payment_combobox.set("Select")
    month_combobox.set("Select Month")
    Product_name_entry.delete(0, END)
    Product_ID_entry.delete(0, END)

    # Clear the treeview
    for item in sales_treeview.get_children():
        sales_treeview.delete(item)
    
    # Optionally, you can also show all data again
    show_customer_data(sales_treeview)

def print_sales_report(sales_treeview):
    try:
        # Get the data from the treeview
        data = []
        headers = []

        # Get column headings from Treeview
        for col in sales_treeview["columns"]:
            headers.append(col)

        for item in sales_treeview.get_children():
            data.append(sales_treeview.item(item)['values'])

        if not data:
            messagebox.showinfo("Info", "No data to print.")
            return

        # Ask user where to save the PDF
        file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return

        # Initialize PDF
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=5)

        # Set column width (adjust based on your needs)
        col_width = 270 / len(headers)
        row_height = 8

        # Add table header
        pdf.set_fill_color(200, 220, 255)
        for header in headers:
            pdf.cell(col_width, row_height, txt=str(header), border=1, ln=0, align='C', fill=True)
        pdf.ln(row_height)

        # Add table data
        for row in data:
            for item in row:
                pdf.cell(col_width, row_height, txt=str(item), border=1, ln=0, align='C')
            pdf.ln(row_height)

        # Save the PDF
        pdf.output(file_path)
        messagebox.showinfo("Success", f"PDF saved successfully at:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export sales report: {e}")



def sales_form(window):

    sale_frame = Toplevel(window)
    sale_frame.title("Sales Overview")
    sale_frame.geometry("1225x960+500+10")
    sale_frame.configure(bg="white")
    sale_frame.resizable(False, False)

    close_image = PhotoImage(file='assests/close.png')
    close_button = Button(sale_frame, image=close_image, bg="white", bd=0, command=sale_frame.destroy)
    close_button.image = close_image
    close_button.place(x=880, y=10)


    heading_label=Label(sale_frame,text="Sale",font=("Times new roman",20,"bold"),fg="black",anchor="w",bg="white")
    heading_label.pack(side=TOP,fill=X,pady=10)    
    
    
    #search frame-------------------------------------------------------------------------------------------------------------

    search_frame=Frame(sale_frame,bg="white")
    search_frame.pack(side=TOP,fill=X,pady=10)

    invoiceNO_label =Label(search_frame,text="Invoice Number",font=("times New roman",11,"bold"),bg="white",fg="black")
    invoiceNO_label.grid(row=0,column=0,pady=10,padx=5,sticky="w")
    invoiceNO_entry=Entry(search_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    invoiceNO_entry.grid(row=0,column=1,pady=10,padx=5,sticky="w")

    name_label =Label(search_frame,text="Customer Name ",font=("times New roman",11,"bold"),bg="white",fg="black")
    name_label.grid(row=0,column=2,pady=10,padx=5,sticky="w")
    name_entry=Entry(search_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    name_entry.grid(row=0,column=3,pady=10,padx=5,sticky="w")

    payment_label =Label(search_frame,text="Payment Method",font=("times New roman",11,"bold"),bg="white",fg="black")
    payment_label.grid(row=0,column=4,pady=10,padx=5,sticky="w")
    payment_combobox=ttk.Combobox(search_frame,font=("times New roman",11,"bold"),state="readonly",values=["Cash","COD","Bank","Credit"],width=10)
    payment_combobox.grid(row=0,column=5,pady=10,padx=5,sticky="w")
    payment_combobox.set("Select")

    month_label =Label(search_frame,text="View Sales Report ",font=("times New roman",11,"bold"),bg="white",fg="black")
    month_label.grid(row=1,column=0,pady=10,padx=5,sticky="w")
    month_combobox=ttk.Combobox(search_frame,font=("times New roman",11,"bold"),values=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],width=11)
    month_combobox.grid(row=1,column=1,pady=10,padx=5,sticky="w")
    month_combobox.set("Select Month")

    Product_name_label =Label(search_frame,text="Product Name",font=("times New roman",11,"bold"),bg="white",fg="black")
    Product_name_label.grid(row=1,column=2,pady=10,padx=5,sticky="w")
    Product_name_entry=Entry(search_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=17)
    Product_name_entry.grid(row=1,column=3,pady=10,padx=5,sticky="w")

    Product_ID_label =Label(search_frame,text="Product ID",font=("times New roman",11,"bold"),bg="white",fg="black")
    Product_ID_label.grid(row=1,column=4,pady=10,padx=5,sticky="w")
    Product_ID_entry=Entry(search_frame,font=("times new roman",11),bd=2,relief=RIDGE,width=15)
    Product_ID_entry.grid(row=1,column=5,pady=10,padx=5,sticky="w")
#buttons
    search_button=Button(search_frame,text="Search",font=("times new roman",10,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: search_customer_data(invoiceNO_entry.get(),name_entry.get(),payment_combobox.get(),month_combobox.get(),Product_name_entry.get(),Product_ID_entry.get(),sales_treeview))
    search_button.grid(row=0,column=6,pady=10,padx=5,sticky="w")
    
    showall_button=Button(search_frame,text="Show All",font=("times new roman",10,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda: show_customer_data(sales_treeview))
    showall_button.grid(row=0,column=7,pady=10,padx=5,sticky="w")

    Print_button=Button(search_frame,text="Print",font=("times new roman",10,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:print_sales_report(sales_treeview))
    Print_button.grid(row=1,column=6,pady=10,padx=5,sticky="w")

    Clear_button=Button(search_frame,text="Clear",font=("times new roman",10,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear(invoiceNO_entry,name_entry,payment_combobox,month_combobox,Product_name_entry,Product_ID_entry, sales_treeview))
    Clear_button.grid(row=1,column=7,pady=10,padx=5,sticky="w")
#-----------------------------------------------------------------------------------------------------------------------------------
#treeframe--------------------------------------------------------------------------------------------------------------------------
    treeview_frame=Frame(sale_frame,bg="white")
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1,pady=10)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    sales_treeview=ttk.Treeview(treeview_frame,columns=("Invoice_number","Ordered_Date","Delivery_date","Product_ID","Product_Name","Quantity","Delivery_charge","Discount","Remark","Size","Gram","Customer_Name","Customer_address","Payment_method","Amount","Customer_number","Fardar_ID"),show="headings")
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=sales_treeview.yview)
    scrollx.config(command=sales_treeview.xview)
    sales_treeview.heading("Invoice_number",text="Invoice number")
    sales_treeview.heading("Ordered_Date",text="Ordered Date")
    sales_treeview.heading("Delivery_date",text="Delivery Date")
    sales_treeview.heading("Product_ID",text="Product ID")
    sales_treeview.heading("Product_Name",text="Product Name")
    sales_treeview.heading("Quantity",text="Quantity")
    sales_treeview.heading("Delivery_charge",text="Delivery charge")
    sales_treeview.heading("Discount",text="Discount")
    sales_treeview.heading("Remark",text="Remark")
    sales_treeview.heading("Size",text="Size")
    sales_treeview.heading("Gram",text="Gram")
    sales_treeview.heading("Customer_Name",text="Customer Name")
    sales_treeview.heading("Customer_address",text="Customer Address")
    sales_treeview.heading("Payment_method",text="Payment Method")
    sales_treeview.heading("Amount",text="Amount")
    sales_treeview.heading("Customer_number",text="Contact Number")
    sales_treeview.heading("Fardar_ID",text="Fardar ID")


    sales_treeview.column("Invoice_number",width=100)
    sales_treeview.column("Ordered_Date",width=100)
    sales_treeview.column("Delivery_date",width=100)
    sales_treeview.column("Product_ID",width=100)
    sales_treeview.column("Product_Name",width=150)
    sales_treeview.column("Quantity",width=100)
    sales_treeview.column("Delivery_charge",width=100)
    sales_treeview.column("Discount",width=100)
    sales_treeview.column("Remark",width=100)
    sales_treeview.column("Size",width=100)
    sales_treeview.column("Gram",width=100)
    sales_treeview.column("Customer_Name",width=100)
    sales_treeview.column("Customer_address",width=100)
    sales_treeview.column("Payment_method",width=100)
    sales_treeview.column("Amount",width=100)
    sales_treeview.column("Customer_number",width=100)
    sales_treeview.column("Fardar_ID",width=100)
    show_customer_data(sales_treeview)
    sales_treeview.pack(fill=BOTH,expand=1)





 

 
  








