from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import connect_database
from tkinter import messagebox
from fpdf import FPDF
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

def search_customer_data(month_combobox,sales_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        query = "SELECT * FROM sales_data WHERE 1=1"
        params = []



        if month_combobox and month_combobox != "Select Month":
            query += " AND MONTHNAME(ordered_date) = %s"
            params.append(month_combobox)




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

def delete_sales_data(sales_treeview):
    selected_item = sales_treeview.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a sale record to delete.")
        return

    invoice_number = sales_treeview.item(selected_item, 'values')[0]  # Assuming Invoice_number is the first column

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Error", "Database connection failed.")
        return

    try:
        cursor.execute("USE attire_empire")
        cursor.execute("DELETE FROM sales_data WHERE Invoice_number = %s", (invoice_number,))
        connection.commit()
        sales_treeview.delete(selected_item)
        messagebox.showinfo("Success", "Sale record deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete sale record: {e}")
    finally:
        cursor.close()
        connection.close()

def managesales(window):
    
    sales_frame = Toplevel(window)
    sales_frame.title("Manage Sales")
    sales_frame.geometry("1500x780+330+175")
    sales_frame.configure(bg="white")
    sales_frame.resizable(True, True)

    #the title label
    title_label=Label(sales_frame,text="Sales Overview",font=("Times new roman",30,"bold"),fg="#060436",anchor="w",bg="white")
    title_label.pack(side=TOP,fill=X)


    search_frame= Frame(sales_frame,width=900,height=70,bg="white")
    search_frame.pack(side=TOP,fill=X,pady=10)

    month_label =Label(search_frame,text="View Sales Report ",font=("times New roman",15,"bold"),bg="white",fg="black")
    month_label.grid(row=0,column=0,pady=10,padx=5,sticky="w")
    month_combobox=ttk.Combobox(search_frame,font=("times New roman",11,"bold"),values=[
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],width=11)
    month_combobox.grid(row=0,column=1,pady=10,padx=5,sticky="w")
    month_combobox.set("Select Month")

    search_button=Button(search_frame,text="Search",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:search_customer_data(month_combobox.get(),sales_treeview))
    search_button.grid(row=0,column=2,pady=10,padx=10,sticky="w")

    showall_button=Button(search_frame,text="Show All",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:show_customer_data(sales_treeview))
    showall_button.grid(row=0,column=3,pady=10,padx=10,sticky="w")

    print_button=Button(search_frame,text="Print Report",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:print_sales_report(sales_treeview))
    print_button.grid(row=0,column=4,pady=10,padx=10,sticky="w")

    delete_button=Button(search_frame,text="Delete",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:delete_sales_data(sales_treeview))
    delete_button.grid(row=0,column=5,pady=10,padx=10,sticky="w")









    #the treeview frame 

    treeview_frame = Frame(sales_frame,bg="white",bd=3,relief=GROOVE)
    treeview_frame.pack(side=TOP,fill=BOTH,expand=1)


    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    sales_treeview=ttk.Treeview(treeview_frame,columns=("Invoice_number","Ordered_Date","Delivery_date","Product_ID","Product_Name","Quantity","Delivery_charge","Discount","Remark","Size","Gram","Customer_Name","Customer_address","Customer_number","Amount","Payment_method"),show="headings")
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
    sales_treeview.heading("Customer_number",text="Contact Number")
    sales_treeview.heading("Amount",text="Amount")
    sales_treeview.heading("Payment_method",text="Payment Method")


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
    sales_treeview.column("Customer_number",width=100)
    sales_treeview.column("Amount",width=100)
    sales_treeview.column("Payment_method",width=100)
    show_customer_data(sales_treeview)
    sales_treeview.pack(fill=BOTH,expand=1)



    





