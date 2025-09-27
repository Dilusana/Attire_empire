from datetime import date
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from customer import customer_form
from sale import sales_form
from calculator import calculator_form
from manageProducts import connect_database
from tkinter import messagebox
import pymysql
from fpdf import FPDF
import tempfile
import os
from manageProducts import treeview_data
import random
from pathlib import Path
import inspect
import time
import pywhatkit
import datetime
import pyautogui
import pyperclip
import webbrowser
import time
from tkinter import messagebox
import datetime

import webbrowser
from tkinter import messagebox
from urllib.parse import quote

def open_billing():
    window = Tk()
    window.title("Billing System")
    window.geometry("1350x730+0+0")
    window.configure(bg="white")
    window.resizable(True, True)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    for i in range(3):
        window.grid_rowconfigure(i, weight=1)
    for i in range(3):
        window.grid_columnconfigure(i, weight=1)

    #############################################################Funtions###########################

    def clear_fields(name_combobox, address_entry, contactNumber_entry, ordered_date_entry, delivery_date_entry, payment_combobox):
        name_combobox.set("Select Customer")
        address_entry.delete(0, END)
        contactNumber_entry.delete(0, END)
        ordered_date_entry.set_date(date.today())
        delivery_date_entry.set_date(date.today())
        payment_combobox.set("Select Method")
        
    def print_details(name_combobox,contact_number,address,total_amount,fardar_entry):
        if name_combobox == "Select Name" or contact_number=='' or address=='':
            messagebox.showerror("Error", "Please Enter Customer Details.")
        else:
            print_window=Toplevel(window)
            print_window.title("Print Customer Address Details")
            print_window.geometry("800x600+500+200")
            print_window.configure(bg="white")
            print_window.resizable(False, False)


            customer_details_frame= Frame(print_window, bg="white")
            customer_details_frame.place(x=30, y=45, width=750, height=300)
            # Get the customer name from the main form
            
        

            name_label = Label(customer_details_frame, text=f"Name: {name_combobox}", font=("times new roman", 15, "bold"), bg="white", fg="black")
            name_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

            contactnumber_label = Label(customer_details_frame, text=f"Contact Number:{contact_number}", font=("times new roman", 15, "bold"), bg="white", fg="black")
            contactnumber_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

            address_label = Label(customer_details_frame, text=f"Address : {address}", font=("times new roman", 15, "bold"), bg="white", fg="black")
            address_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")

            total_label = Label(customer_details_frame, text=f"Amount : {total_amount}", font=("times new roman", 15, "bold"), bg="white", fg="black")
            total_label.grid(row=3, column=0, pady=10, padx=10, sticky="w")
            
            fardar_label = Label(customer_details_frame, text=f"Fardar ID : {fardar_entry}", font=("times new roman", 15, "bold"), bg="white", fg="black")  
            fardar_label.grid(row=4, column=0, pady=10, padx=10, sticky="w")    




            business_details_frame= Frame(print_window, bg="white")
            business_details_frame.place(x=500, y=350, width=230, height=150)

            name_label = Label(business_details_frame, text="Attire Empire", font=("times new roman", 20, "bold"), bg="white", fg="black")
            name_label.pack(pady=0)
            owner_name = Label(business_details_frame, text="Lakshiya", font=("times new roman", 20), bg="white", fg="black")
            owner_name.pack(pady=0)
            contact_label = Label(business_details_frame, text="0742217332", font=("times new roman", 20, "bold"), bg="white", fg="black")
            contact_label.pack(pady=0)

            print_pdf=Button(print_window,text="Print Pdf",font=("times new roman",17,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:print_pdf())
            print_pdf.place(x=340,y=500,width=150,height=40)

            def print_pdf():
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=16)
                pdf.cell(200, 10, txt="Customer Address Details", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, txt=f"Name: {name_combobox}", ln=True)
                pdf.cell(0, 10, txt=f"Address: {address}", ln=True)
                pdf.cell(0, 10, txt=f"Contact Number: {contact_number}", ln=True)
                pdf.set_font("Arial", size=20)
                pdf.cell(0, 10, txt=f"Amount: {total_amount}", ln=True)
                pdf.ln(20)
                pdf.set_font("Arial", size=14)
                # Add business details to the top right corner
                pdf.set_xy(150, 10)
                pdf.set_font("Arial", size=12)
                pdf.ln(90)
                pdf.set_x(150)
                pdf.cell(0, 10, txt="Attire Empire", ln=True, align='R')
                pdf.set_x(150)
                pdf.cell(0, 10, txt="Lakshiya", ln=True, align='R')
                pdf.set_x(150)
                pdf.cell(0, 10, txt="0742217332", ln=True, align='R')

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
                    pdf.output(tmpfile.name)
                    os.startfile(tmpfile.name, "open")

        




    def fetch_customername(name_combobox):
        name_option = []

        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE attire_empire')
            cursor.execute('SELECT DISTINCT customer_Name FROM customer_data')
            categories = cursor.fetchall()
            if categories:
                name_combobox.set('Select Name')
                for category in categories:
                    name_option.append(category[0])
                name_combobox.config(values=name_option)
        except Exception as e:
            messagebox.showerror('Error', f'Error fetching Names: {e}')
        finally:
            cursor.close()
            connection.close()

    def addtocart(productID, productname, price, quantity, discount,delivery_charge,TotalAmount_entry,fardar_entry, cart_treeview):

            price = float(price) if price else 0.0
            quantity = int(quantity) if quantity else 0
            discount = float(discount) if discount else 0.0
            delivery_charge = float(delivery_charge) if delivery_charge else 0.0


            net_price = price - discount
            total_amount = (net_price * quantity) + delivery_charge

            TotalAmount_entry.delete(0, END)
            TotalAmount_entry.insert(0, str(total_amount))
            
            try:

                price = float(price) if price else 0.0
                quantity = int(quantity) if quantity else 0
                discount = float(discount) if discount else 0.0
                delivery_charge = float(delivery_charge) if delivery_charge else 0.0
                

                net_price = price - discount
                amount = (net_price * quantity) + delivery_charge



                cart_treeview.insert('', 'end', values=(
                productID,
                productname,
                quantity,
                price,
                discount,
                net_price,
                delivery_charge,
                amount,
                fardar_entry
                ))
                
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add to cart: {e}")

    def clear(cart_treeview):
        for item in cart_treeview.get_children():
            cart_treeview.delete(item)




    def billing(product_name, address, contact_number, productname, quantity, price, size, gram, delivery_charge, discount, total_amount, payment_method, ordered_date, delivery_date,fardar_ID, cart_treeview):
        global invoice_number,total_cart_amount
        if not product_name or not address or not contact_number or not productname or not quantity or not price or not size or not gram  or not total_amount or not payment_method :
            messagebox.showerror("Error", "Please fill all fields.")
            return

        billing_text.delete(1.0, END)
        billing_text.tag_configure("header", font=("Times New Roman", 16, "bold"))
        billing_text.insert(END, "********** Welcome To Attire Empire **********\n", "header")

        billing_text.tag_configure("subheader", font=("Times New Roman", 11))
        billing_text.insert(END, "\nThank you For Participating with Attire Empire. Please Find your Bill Enclosed\n", "subheader")
        billing_text.insert(END, "\nFor future orders or inquiries, you can Contact us via:", "subheader")
        billing_text.insert(END, "\n\tCall/Whatsapp: 074-221 7332(Lakshiya)", "subheader")
        billing_text.insert(END, "\n\tInstagram: fashion_fizz_6 / attire_empire_saree_sj ", "subheader")
        billing_text.insert(END, "\n\tFacebook: Attire Empire / Attire Empire Saree S&J", "subheader")


        billing_text.insert(END, f"\n\nCustomer Name: {product_name}","subheader")
        billing_text.insert(END, f"\nAddress: {address}","subheader")
        billing_text.insert(END, f"\nContact Number: {contact_number}","subheader")
        invoice_number = random.randint(10000, 99999)
        billing_text.insert(END, f"\nInvoice Number: {invoice_number}\n", "subheader")
        billing_text.insert(END, f"\nFardar ID: {fardar_ID}\n", "subheader")

        billing_text.tag_configure("itamheader", font=("Times New Roman", 12, "bold"))

        billing_text.insert(END, f"\n\n\nProduct Name\t\t\tQuantity\t\tPrice\t\tSize\t\tGram\t\tDelivery Charge\t\tDiscount\t\tTotal Amount\n", "itamheader")
        billing_text.tag_configure("iteams", font=("Times New Roman", 11))

        for item in cart_treeview.get_children():
            values = cart_treeview.item(item, 'values')
            # values: (ID, Name, Quantity, Price, Discount, Net Price, Delivery_charge, Amount)
            billing_text.insert(
                END,
                f"{values[1]}\t\t\t{values[2]}\t\t{values[3]}\t\t{size}\t\t{gram}\t\t{values[6]}\t\t{values[4]}\t\t{values[7]}\n","iteams"
            )

        # Count the number of items in the cart
        # Calculate the total amount for all items in the cart
        num_items = len(cart_treeview.get_children())
        total_cart_amount = 0.0
        for item in cart_treeview.get_children():
            values = cart_treeview.item(item, 'values')
            try:
                amount = float(values[7])  # Amount is at index 7
            except (IndexError, ValueError):
                amount = 0.0
            total_cart_amount += amount


        billing_text.insert(END, f"\n\nTotal Amount: {total_cart_amount}\n", "itamheader")

        billing_text.insert(END, f"\n\nPayment Method: {payment_method}\n", "subheader")
        billing_text.insert(END, f"Ordered Date: {ordered_date}\n", "subheader")
        billing_text.insert(END, "\n\n********** Thank You For Shopping With Us **********\n", "subheader")







    def clear_bill(billing_text):
        billing_text.delete(1.0, END)

    def autofill_customer_details(event=None):
        customer_name = name_combobox.get().strip()

        if not customer_name:
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            messagebox.showerror("Error", "Database connection failed.")
            return

        try:
            cursor.execute("USE attire_empire")
            cursor.execute("""
                SELECT customer_address, Contact_Number 
                FROM customer_data 
                WHERE customer_Name = %s
            """, (customer_name,))
            result = cursor.fetchone()

            if result:
                address, contact = result
                address_entry.delete(0, END)
                address_entry.insert(0, address)

                contactNumber_entry.delete(0, END)
                contactNumber_entry.insert(0, contact)
            else:
                # If no match found, clear the fields
                address_entry.delete(0, END)
                contactNumber_entry.delete(0, END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch customer details: {e}")
        finally:
            cursor.close()
            connection.close()

        
    def save_bill(ordered_date, delivery_date, productID, productname, quantity, delivery_charge,
                discount, remark, size, gram, name, address, payment , contact_number ,fardarID):
        global invoice_number, total_cart_amount

        bill_content = billing_text.get(1.0, END).strip()
        if not bill_content:
            messagebox.showerror("Error", "No bill content to save.")
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            messagebox.showerror("Error", "Database connection failed.")
            return

        try:
            cursor.execute('USE attire_empire')

        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales_data (
                    invoice_number VARCHAR(255),
                    ordered_date DATE,
                    delivery_date DATE,
                    productID VARCHAR(50),
                    productname VARCHAR(255),
                    quantity INT,
                    delivery_charge DECIMAL(10,2),
                    discount DECIMAL(10,2),
                    remark TEXT,
                    size VARCHAR(50),
                    gram VARCHAR(50),
                    name VARCHAR(255),
                    address VARCHAR(255),
                    payment VARCHAR(100),
                    total_amount DECIMAL(10,2),
                    contact_number VARCHAR(150),
                    fardar_ID VARCHAR(150)
                )
            """)
            gram = float(gram)
            quantity = float(quantity)

            updated_stock = gram - quantity



            cursor.execute("""
                UPDATE product_data
                SET gram = %s
                WHERE Product_ID = %s
            """, (updated_stock, productID))







            cursor.execute("""
                INSERT INTO sales_data (
                    invoice_number, ordered_date, delivery_date, productID, productname, quantity, delivery_charge,
                    discount, remark, size, gram, name, address, payment, total_amount, contact_number, fardar_ID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                invoice_number, ordered_date, delivery_date, productID, productname, quantity,
                delivery_charge, discount, remark, size, gram, name, address,
                payment, total_cart_amount, contact_number, fardarID
            ))
            if payment.lower() == "credit":  # now both are lowercase
                cursor.execute("SELECT balance FROM customer_data WHERE customer_Name = %s", (name,))
                result = cursor.fetchone()

                if result:
                    current_balance = result[0] or 0
                    new_balance = current_balance + total_cart_amount
                    cursor.execute("""
                        UPDATE customer_data 
                        SET balance = %s 
                        WHERE customer_Name = %s
                    """, (new_balance, name))
                else:
                    cursor.execute("""
                        INSERT INTO customer_data (customer_Name, balance)
                        VALUES (%s, %s)
                    """, (name, total_cart_amount))

                connection.commit()

            # Normalize the payment method
            normalized_payment = payment.strip().lower()
            print(f"Normalized payment: '{normalized_payment}'")  # Optional debug

            # Only insert if it's COD or Bank Transfer
            if normalized_payment in ["cod", "bank"]:
                cursor.execute("""
                    INSERT INTO fardar_data (
                        Date, Invoice_No, fardar_ID, Customer_Name, Delivery_Date, total_amount, payment
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    ordered_date,
                    invoice_number,
                    fardarID,
                    name,
                    delivery_date,
                    total_cart_amount,
                    normalized_payment
                ))


            connection.commit()
            messagebox.showinfo("Success", "Bill saved successfully.")

                


            # Ask user if they want to save PDF
            result = messagebox.askyesno("Save Bill", "Do you want to save the bill as PDF?")
            if result:
                desktop = Path.home() / "Desktop"
                bills_folder = desktop / "Bills"
                bills_folder.mkdir(exist_ok=True)
                pdf_file_path = bills_folder / f"{invoice_number}.pdf"

                # Create PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)

                # Header
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="********** Welcome To Attire Empire **********", ln=True, align='C')
                pdf.ln(10)

                pdf.set_font("Arial", size=11)
                pdf.cell(0, 10, txt="Thank you For Participating with Attire Empire. Please Find your Bill Enclosed", ln=True)
                pdf.cell(0, 10, txt="For future orders or inquiries, you can Contact us via:", ln=True)
                pdf.cell(0, 10, txt="Call/Whatsapp: 074-221 7332 (Lakshiya)", ln=True)
                pdf.cell(0, 10, txt="Instagram: fashion_fizz_6 / attire_empires_saree / attire_jewellary", ln=True)
                pdf.cell(0, 10, txt="Facebook: Attire Empire", ln=True)
                pdf.ln(10)

                # Customer Info
                pdf.cell(0, 10, txt=f"Customer Name: {name}", ln=True)
                pdf.cell(0, 10, txt=f"Address: {address}", ln=True)
                pdf.cell(0, 10, txt=f"Contact Number: {contact_number}", ln=True)
                pdf.cell(0, 10, txt=f"Invoice Number: {invoice_number}", ln=True)
                pdf.cell(0, 10, txt=f"Fardar ID: {fardarID}", ln=True)
                pdf.ln(10)

                # Table Headers
                pdf.set_font("Arial", "B", size=10)
                col_widths = [35, 15, 20, 15, 15, 25, 20, 25]
                headers = ["Product", "Qty", "Price", "Size", "Gram", "Delivery", "Discount", "Total"]
                for i in range(len(headers)):
                    pdf.cell(col_widths[i], 10, headers[i], border=1, align='C')
                pdf.ln()

                # Table Rows
                pdf.set_font("Arial", size=10)
                for item in cart_treeview.get_children():
                    values = cart_treeview.item(item, 'values')
                    pdf.cell(col_widths[0], 10, str(values[1]), border=1)
                    pdf.cell(col_widths[1], 10, str(values[2]), border=1, align='C')
                    pdf.cell(col_widths[2], 10, str(values[3]), border=1, align='C')
                    pdf.cell(col_widths[3], 10, str(size), border=1, align='C')
                    pdf.cell(col_widths[4], 10, str(gram), border=1, align='C')
                    pdf.cell(col_widths[5], 10, str(values[6]), border=1, align='C')
                    pdf.cell(col_widths[6], 10, str(values[4]), border=1, align='C')
                    pdf.cell(col_widths[7], 10, str(values[7]), border=1, align='C')
                    pdf.ln()

                # Summary
                pdf.ln(5)
                pdf.set_font("Arial", size=11)
                pdf.cell(0, 10, txt=f"Total Amount: {total_cart_amount}", ln=True)
                pdf.cell(0, 10, txt=f"Payment Method: {payment}", ln=True)
                pdf.cell(0, 10, txt=f"Ordered Date: {ordered_date}", ln=True)
                pdf.cell(0, 10, txt=f"Delivery Date: {delivery_date}", ln=True)
                pdf.ln(10)

                # Footer
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, txt="********** Thank You For Shopping With Us **********", ln=True, align='C')
                pdf.ln(5)
                pdf.set_font("Arial", size=11)

                pdf.output(str(pdf_file_path))
                messagebox.showinfo("Success", f"Bill saved as PDF:\n{pdf_file_path}")
            else:
                messagebox.showinfo("Info", "Bill was not saved as PDF.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill: {e}")
        finally:
            if cursor: cursor.close()
            if connection: connection.close()
                                    



    def open_send_bill_window(main_billing_text):
        send_window = Toplevel()
        send_window.title("Send Bill via WhatsApp")
        send_window.geometry("600x600")
        send_window.grab_set()

        Label(send_window, text="Customer WhatsApp Number (Ex: 94771234567)").pack(pady=5)
        number_entry = Entry(send_window, width=30)
        number_entry.pack(pady=5)

        Label(send_window, text="Bill Content").pack(pady=5)
        send_billing_text = Text(send_window, width=45, height=10)
        send_billing_text.pack(pady=5)

        # Load content from billing text area
        bill_content = main_billing_text.get("1.0", END).strip()
        send_billing_text.insert(END, bill_content)

        def send_bill():
            number = number_entry.get().strip()
            message = send_billing_text.get("1.0", END).strip()

            if not number or not message:
                messagebox.showerror("Error", "Please enter both the number and the bill content.")
                return

            if not number.isdigit():
                messagebox.showerror("Error", "Enter number as digits only (e.g., 9477xxxxxxx)")
                return

            # Encode message for URL
            encoded_msg = quote(message)
            url = f"https://wa.me/{number}?text={encoded_msg}"

            # Open WhatsApp Web in browser
            webbrowser.open(url)

            send_window.destroy()

        Button(send_window, text="Send Bill", command=send_bill).pack(pady=10)


    #############################################################################################################################################################
    ##########################################################GUI##########################################################################################
    #icon frmae-------------------------------------
    icon_frame = Frame(window, bg="black", width=100)
    icon_frame.grid(row=0, column=0, rowspan=5, sticky="ns")  # Removed 'e' and 'w' so it doesn't expand
    icon_frame.grid_propagate(False)  # Prevent auto-expanding to fit content



    homeimage=PhotoImage(file="assests/home.png")
    home_button = Button(icon_frame, image=homeimage, bg="white", bd=0,width=75,height=75)
    home_button.grid(row=0,column=0,pady=20,padx=5)

    searchimage=PhotoImage(file="assests/search.png")
    search_button = Button(icon_frame, image=searchimage, bg="white", bd=0,width=75,height=75,command=lambda:search_form(window))
    search_button.grid(row=1,column=0,pady=20,padx=5)

    customerimage=PhotoImage(file="assests/customer.png")
    customer_button = Button(icon_frame, image=customerimage, bg="white", bd=0,width=75,height=75,command=lambda:customer_form(window))
    customer_button.grid(row=2,column=0,pady=20,padx=5)

    saleimage=PhotoImage(file="assests/sale.png")
    sale_button = Button(icon_frame, image=saleimage, bg="white", bd=0,width=75,height=75,command=lambda:sales_form(window))
    sale_button.grid(row=4,column=0,pady=20,padx=5)

    calculatorimage=PhotoImage(file="assests/calculator.png")
    calculator_button = Button(icon_frame, image=calculatorimage, bg="white", bd=0,width=75,height=75,command=lambda:calculator_form(window))
    calculator_button.grid(row=5,column=0,pady=20,padx=5)

    logoutimage=PhotoImage(file="assests/logout.png")
    logout_button = Button(icon_frame, image=logoutimage, bg="white", bd=0,width=75,height=75,command=lambda:exit_app())
    logout_button.grid(row=6,column=0,pady=20,padx=5)

    #-------------------------------------------------------------------------------------------------------------

    #heading frame------------------------------------------------------------------------------------------------
    heading_frame = Frame(window, bg="white")
    heading_frame.grid(row=0, column=1, sticky="nsew")

    # Configure heading_frame to allow flexible layout
    heading_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
    heading_frame.grid_columnconfigure(0, weight=3)  # For Title
    heading_frame.grid_columnconfigure(1, weight=2)  # For Subtitle
    heading_frame.grid_rowconfigure(0, weight=1)

    # Main title
    Title_label = Label(heading_frame, text=" @ Attire Empire",
                        font=("Times new roman", 30, "bold"),
                        fg="black", anchor="w", bg="white")
    Title_label.grid(row=0, column=0, sticky="nsew")

    # Subtitle
    subtitle_label = Label(heading_frame, text="Welcome\t\tTime: 00:00:00\tDate: 15th June 2025",
                        font=("Times new roman", 15, "bold"),
                        fg="black", anchor="e", bg="white")
    subtitle_label.grid(row=0, column=1, sticky="nsew")

    #-------------------------------------------------------------------------------------------------------------

    # Configure columns
    for col in range(3):
        window.grid_columnconfigure(col, weight=1)

    # Configure row (optional)
    window.grid_rowconfigure(1, weight=0)



    # Place the label spanning all columns so it fills the width
    Title2_label = Label(heading_frame, text="Customer Details",
                        font=("Times new roman", 20, "bold"),
                        fg="white", bg="#0D0D50")
    Title2_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)


    #the details frame--------------------------------------------------------------------------------------------
    details_frame = Frame(heading_frame, bg="white")
    details_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

    name_label =Label(details_frame,text="Name",font=("times New roman",15,"bold"),bg="white",fg="black")
    name_label.grid(row=0,column=0,pady=10,padx=10,sticky="w")
    name_combobox=ttk.Combobox(details_frame,font=("times New roman",15,"bold"),values=["Dilushana","krishna","Ganesh"],width=15)
    name_combobox.grid(row=0,column=1,pady=10,padx=10,sticky="w")
    name_combobox.set("Select Customer")
    fetch_customername(name_combobox)
    name_combobox.bind("<FocusOut>", autofill_customer_details)  # On focus out

    address_label =Label(details_frame,text="Address",font=("times New roman",15,"bold"),bg="white",fg="black")
    address_label.grid(row=0,column=2,pady=10,padx=10,sticky="w")
    address_entry=Entry(details_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    address_entry.grid(row=0,column=3,pady=10,padx=10,sticky="w")
    
    contactNumber_label =Label(details_frame,text="Contact Number",font=("times New roman",15,"bold"),bg="white",fg="black")
    contactNumber_label.grid(row=0,column=4,pady=10,padx=10,sticky="w")
    contactNumber_entry=Entry(details_frame,font=("times new roman",15),bd=2,relief=RIDGE,width=17)
    contactNumber_entry.grid(row=0,column=5,pady=10,padx=10,sticky="w")

    # or
    # customer_name_entry.bind("<Return>", autofill_customer_details)  # On pressing Enter

    ordered_date_label =Label(details_frame,text="Ordered Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    ordered_date_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    ordered_date_entry = DateEntry(details_frame, width=15, state='readonly',date_pattern='dd-mm-yyyy', font=('times new roman', 15, 'bold'))
    ordered_date_entry.grid(row=1, column=1, pady=10, padx=10, sticky='w')

    ordered_date_label =Label(details_frame,text="Ordered Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    ordered_date_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    ordered_date_entry = DateEntry(details_frame, width=15, state='readonly',date_pattern='dd-mm-yyyy', font=('times new roman', 15, 'bold'))
    ordered_date_entry.grid(row=1, column=1, pady=10, padx=10, sticky='w')

    delivery_date_label =Label(details_frame,text="Delivery Date",font=("times New roman",15,"bold"),bg="white",fg="black")
    delivery_date_label.grid(row=1,column=2,pady=10,padx=10,sticky="w")
    delivery_date_entry = DateEntry(details_frame, width=15, state='readonly',date_pattern='dd-mm-yyyy', font=('times new roman', 15, 'bold'))
    delivery_date_entry.grid(row=1, column=3, pady=10, padx=10, sticky='w')

    payment_label =Label(details_frame,text="Payment Method",font=("times New roman",15,"bold"),bg="white",fg="black")
    payment_label.grid(row=1,column=4,pady=10,padx=10,sticky="w")
    payment_combobox=ttk.Combobox(details_frame,font=("times New roman",15,"bold"),state="readonly",values=["Cash","COD","Bank","Credit"],width=15)
    payment_combobox.grid(row=1,column=5,pady=10,padx=10,sticky="w")
    payment_combobox.set("Select Method")

    clear_button=Button(details_frame,text="Clear",font=("times new roman",17,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_fields(name_combobox,address_entry,contactNumber_entry,ordered_date_entry,delivery_date_entry,payment_combobox))
    clear_button.grid(row=0,column=6,pady=10,padx=10,sticky="w")
    #this buttton need to open a small window and it should print the customer details 
    print_customer_button=Button(details_frame,text="Print Details",font=("times new roman",17,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:print_details(name_combobox.get(),contactNumber_entry.get(),address_entry.get(),TotalAmount_entry.get(),fardar_entry.get()))
    print_customer_button.grid(row=1,column=6,pady=10,padx=10,sticky="w")


    #--------------------------------------------------------------------------------------------------------------------
    Title3_label=Label(window,text="Product Details",font=("Times new roman",20,"bold"),fg="white",bg="#0D0D50")
    Title3_label.grid(row=1,column=1,sticky="nsew")
    #product frame-------------------------------------------------------------------------------------------------------
    product_frame = Frame(window, bg="white")
    product_frame.grid(row=2, column=1, sticky="nsew")

    
    
    productID_label =Label(product_frame,text="Product ID",font=("times New roman",13,"bold"),bg="white",fg="black")
    productID_label.grid(row=0,column=0,padx=10,sticky="w")
    productID_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    productID_entry.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    productname_label =Label(product_frame,text="Product Name",font=("times New roman",13,"bold"),bg="white",fg="black")
    productname_label.grid(row=1,column=0,pady=10,padx=10,sticky="w")
    productname_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    productname_entry.grid(row=1,column=1,pady=10,padx=10,sticky="w")

    price_label =Label(product_frame,text="Price",font=("times New roman",13,"bold"),bg="white",fg="black")
    price_label.grid(row=2,column=0,pady=10,padx=10,sticky="w")
    price_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    price_entry.grid(row=2,column=1,pady=10,padx=10,sticky="w")

    quantity_label =Label(product_frame,text="Quantity",font=("times New roman",13,"bold"),bg="white",fg="black")
    quantity_label.grid(row=3,column=0,pady=10,padx=10,sticky="w")
    quantity_entry=Spinbox(product_frame,from_=0,to=100,font=("times new roman",13),bd=2,relief=RIDGE,width=15)
    quantity_entry.grid(row=3,column=1,pady=10,padx=10,sticky="w")

    delivery_charge_label =Label(product_frame,text="Delivery Charge",font=("times New roman",13,"bold"),bg="white",fg="black")
    delivery_charge_label.grid(row=4,column=0,pady=10,padx=10,sticky="w")
    delivery_charge_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    delivery_charge_entry.grid(row=4,column=1,pady=10,padx=10,sticky="w")

    discount_label =Label(product_frame,text="Discount",font=("times New roman",13,"bold"),bg="white",fg="black")
    discount_label.grid(row=5,column=0,pady=10,padx=10,sticky="w")
    discount_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    discount_entry.grid(row=5,column=1,pady=10,padx=10,sticky="w")

    remark_label =Label(product_frame,text="Remark",font=("times New roman",13,"bold"),bg="white",fg="black")
    remark_label.grid(row=6,column=0,pady=10,padx=10,sticky="w")
    remark_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    remark_entry.grid(row=6,column=1,pady=10,padx=10,sticky="w")

    size_label =Label(product_frame,text="Size",font=("times New roman",13,"bold"),bg="white",fg="black")
    size_label.grid(row=7,column=0,pady=10,padx=10,sticky="w")
    size_combobox=ttk.Combobox(product_frame,font=("times New roman",13,"bold"),values=["S","M","L","XL","XLL","XLL","XXXL"],width=13)
    size_combobox.grid(row=7,column=1,pady=10,padx=10,sticky="w")
    size_combobox.set("Select Size")

    gram_label =Label(product_frame,text="Stock",font=("times New roman",13,"bold"),bg="white",fg="black")
    gram_label.grid(row=8,column=0,pady=10,padx=10,sticky="w")
    gram_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    gram_entry.grid(row=8,column=1,pady=10,padx=10,sticky="w")

    TotalAmount_label =Label(product_frame,text="Total Amount",font=("times New roman",13,"bold"),bg="white",fg="black")
    TotalAmount_label.grid(row=9,column=0,pady=10,padx=10,sticky="w")
    TotalAmount_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    TotalAmount_entry.grid(row=9,column=1,pady=10,padx=10,sticky="w")

    fardar_label =Label(product_frame,text="Fardar ID",font=("times New roman",13,"bold"),bg="white",fg="black")
    fardar_label.grid(row=10,column=0,pady=10,padx=10,sticky="w")
    fardar_entry=Entry(product_frame,font=("times new roman",13),bd=2,relief=RIDGE,width=17)
    fardar_entry.grid(row=10,column=1,pady=10,padx=10,sticky="w")



    add_cart_button=Button(product_frame,text="Add To Cart",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:addtocart(productID_entry.get(),productname_entry.get(),price_entry.get(),quantity_entry.get(),discount_entry.get(),delivery_charge_entry.get(),TotalAmount_entry,fardar_entry.get(),cart_treeview))
    add_cart_button.grid(row=11,column=0,pady=10,padx=10,sticky="w")
    # Clear Cart button below the Treeview frame
    clear_cart_button = Button(product_frame, text="Clear", font=("Times New Roman", 15, "bold"),
                            bg="#4267B2", fg="white", width=10, bd=1, relief=RIDGE,
                            command=lambda: clear(cart_treeview))
    clear_cart_button.grid(row=11, column=1, sticky="w",pady=10,padx=10)


    # Assuming 'product_frame' is already defined
    cart_treeview_frame = Frame(product_frame, bg="white")
    cart_treeview_frame.grid(row=0, column=2, rowspan=11, sticky="nsew", padx=10, pady=10)
    cart_treeview_frame.grid_propagate(False)

    # Scrollbars
    scrolly = Scrollbar(cart_treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(cart_treeview_frame, orient=HORIZONTAL)

    # Treeview
    cart_treeview = ttk.Treeview(
        cart_treeview_frame,
        columns=("ID", "Name", "Quantity", "Price", "Discount", "Net Price", "Delivery_charge", "Amount"),
        show="headings",
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )

    # Pack scrollbars
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)

    # Attach scrollbars to treeview
    scrolly.config(command=cart_treeview.yview)
    scrollx.config(command=cart_treeview.xview)

    # Headings
    cart_treeview.heading("ID", text="ID")
    cart_treeview.heading("Name", text="Name")
    cart_treeview.heading("Quantity", text="Quantity")
    cart_treeview.heading("Price", text="Price")
    cart_treeview.heading("Discount", text="Discount")
    cart_treeview.heading("Net Price", text="Net Price")
    cart_treeview.heading("Delivery_charge", text="Delivery")
    cart_treeview.heading("Amount", text="Amount")

    # Column widths
    cart_treeview.column("ID", width=20)
    cart_treeview.column("Name", width=100)
    cart_treeview.column("Quantity", width=50)
    cart_treeview.column("Price", width=50)
    cart_treeview.column("Discount", width=50)
    cart_treeview.column("Net Price", width=80)
    cart_treeview.column("Delivery_charge", width=80)
    cart_treeview.column("Amount", width=80)

    # Pack the Treeview last so it adjusts to the scrollbars
    cart_treeview.pack(fill=BOTH, expand=1)

    #--------------------------------------------------------------------------------------------------------------------
    Title3_label=Label(window,text="Product Details",font=("Times new roman",20,"bold"),fg="white",bg="#0D0D50")
    Title3_label.grid(row=1,column=1,sticky="nsew")
    Title4_label=Label(window,text="View Bill",font=("Times new roman",20,"bold"),fg="white",bg="#0D0D50")
    Title4_label.grid(row=1,column=2,sticky="nsew")
    #View bill frame-------------------------------------------------------------------------------------------------------
    billing_frame = Frame(window, bg="white")
    billing_frame.grid(row=2, column=2, sticky="nsew")


    scrolly = Scrollbar(billing_frame, orient=VERTICAL)
    scrollx = Scrollbar(billing_frame, orient=HORIZONTAL)
    billing_text = Text(billing_frame, wrap=NONE, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    billing_text.pack(fill=BOTH, expand=1)
    scrolly.config(command=billing_text.yview)
    scrollx.config(command=billing_text.xview)

    button_frame = Frame(window, bg="white")
    button_frame.grid(row=3, column=2, sticky="nsew")
    window.grid_rowconfigure(3, weight=0)  # Optional: don't allow too much expansion


    Bill__button=Button(button_frame,text="Bill",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:billing(name_combobox.get(),address_entry.get(),contactNumber_entry.get(),productname_entry.get(),quantity_entry.get(),price_entry.get(),size_combobox.get(),gram_entry.get(),delivery_charge_entry.get(),discount_entry.get(),TotalAmount_entry.get(),payment_combobox.get(),ordered_date_entry.get_date(),delivery_date_entry.get_date(),fardar_entry.get(),cart_treeview))
    Bill__button.grid(row=0,column=1,pady=10,padx=10,sticky="w")

    send_whatsapp_button = Button(button_frame, text="Send Bill", font=("times new roman", 15, "bold"), bg="#4267B2", fg="white", width=10, bd=1, relief=RIDGE, command=lambda: open_send_bill_window(billing_text))
    send_whatsapp_button.grid(row=0,column=2,pady=10,padx=10,sticky="w")

    clear_button=Button(button_frame,text="Clear",font=("times new roman",15,"bold"),bg="#4267B2",fg="white",width=10,bd=1,relief=RIDGE,command=lambda:clear_bill(billing_text))
    clear_button.grid(row=0,column=3,pady=10,padx=10,sticky="w")

    Save_button = Button(button_frame, text="Save", font=("times new roman", 15, "bold"), bg="#4267B2", fg="white", width=10, bd=1, relief=RIDGE, command=lambda: save_bill( ordered_date_entry.get_date(), delivery_date_entry.get_date(), productID_entry.get(), productname_entry.get(), quantity_entry.get(), delivery_charge_entry.get(), discount_entry.get(), remark_entry.get(), size_combobox.get(), gram_entry.get(), name_combobox.get(), address_entry.get(),payment_combobox.get(), contactNumber_entry.get(),fardar_entry.get()))
    Save_button.grid(row=0, column=4, pady=10, padx=10, sticky="w")







    ####################################################################################################################################################################
    ####################################################################################################################################################################
    #SEARCH PRODUCT#####







    def search_form(window):






        def select_data(event,productID_entry, productname_entry, price_entry, remark_entry,size_combobox,gram_entry, product_treeview ):
            
            selected = product_treeview.selection()
            if not selected:
                return
            content = product_treeview.item(selected[0])
            row = content['values']
            if len(row) < 12:
                return
            productID_entry.delete(0, END)
            productname_entry.delete(0, END)
            price_entry.delete(0, END)
            remark_entry.delete(0, END)
            size_combobox.set('Select size')
            gram_entry.delete(0, END)

            
            productID_entry.insert(0, row[0])
            productname_entry.insert(0, row[1])
            price_entry.insert(0, row[6])
            remark_entry.insert(0, row[7])
            size_combobox.set(row[8])
            gram_entry.insert(0, row[9])

        def search_product(productID, productname, product_treeview):
            
            cursor, connection = connect_database()
            if not cursor or not connection:
                return

            cursor.execute('USE attire_empire')
            try:
                query = 'SELECT * FROM product_data WHERE 1=1'
                params = []

                if productID:
                    query += ' AND Product_ID = %s'
                    params.append(productID)
                if productname:
                    query += ' AND Product_Name LIKE %s'
                    params.append(f'%{productname}%')
                
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
            

        def show_product(product_treeview):
            cursor, connection = connect_database()
            if not cursor or not connection:
                return

            cursor.execute('USE attire_empire')
            try:
                cursor.execute('SELECT * FROM product_data')
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


        
        # Create a Toplevel window instead of a Frame
        search_window = Toplevel(window)
        search_window.title("Search Products")
        search_window.geometry("1225x960+500+10")
        search_window.configure(bg="white")
        search_window.resizable(False, False)

        close_image = PhotoImage(file='assests/close.png')
        close_button = Button(search_window, image=close_image, bg="white", bd=0, command=search_window.destroy)
        close_button.image = close_image
        close_button.place(x=880, y=10)

        heading_label = Label(search_window, text="Search Products", font=("Times new roman", 25, "bold"), fg="black", anchor="w", bg="white")
        heading_label.pack(side=TOP, fill=X, padx=10, pady=10)


        search_product_frame = Frame(search_window, bg="white")
        search_product_frame.pack(side=TOP, fill=X, padx=10, pady=10)

        ID_label = Label(search_product_frame, text="Product ID", font=("times New roman", 15, "bold"), bg="white", fg="black")
        ID_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        ID_entry = Entry(search_product_frame, font=("times new roman", 15), bd=2, relief=RIDGE, width=17)
        ID_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        name_label = Label(search_product_frame, text="Product Name", font=("times New roman", 15, "bold"), bg="white", fg="black")
        name_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        name_entry = Entry(search_product_frame, font=("times new roman", 15), bd=2, relief=RIDGE, width=17)
        name_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        search_button = Button(search_product_frame, text="Search", font=("times new roman", 15, "bold"), bg="#4267B2", fg="white", width=10, bd=1, relief=RIDGE,command=lambda: search_product(ID_entry.get(), name_entry.get(), product_treeview))
        search_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        showall_button = Button(search_product_frame, text="Show All", font=("times new roman", 15, "bold"), bg="#4267B2", fg="white", width=10, bd=1, relief=RIDGE,command=lambda: show_product(product_treeview))
        showall_button.grid(row=0, column=3, pady=10, padx=10, sticky="w")
        #----------------------------------------------------------------------------------------------------------------
        #the treeview frame------------------------------------------------------------------------------------------
        product_treeview_frame = Frame(search_window, bg="white")
        product_treeview_frame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)

        scrolly = Scrollbar(product_treeview_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_treeview_frame, orient=HORIZONTAL)
        product_treeview = ttk.Treeview(product_treeview_frame, columns=("ID", "Name", "INR Price ₹", "Duety Charge", "Cost", "Profit", "Selling Price", "Remark", "Size", "Gram", "Category", "Supplier"), show="headings")
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=product_treeview.yview)
        scrollx.config(command=product_treeview.xview)
        product_treeview.heading("ID", text="ID")
        product_treeview.heading("Name", text="Name")
        product_treeview.heading("INR Price ₹", text="INR Price ₹")
        product_treeview.heading("Duety Charge", text="Duety Charge")
        product_treeview.heading("Cost", text="Cost")
        product_treeview.heading("Profit", text="Profit")
        product_treeview.heading("Selling Price", text="Selling Price")
        product_treeview.heading("Remark", text="Remark")
        product_treeview.heading("Size", text="Size")
        product_treeview.heading("Gram", text="Gram")
        product_treeview.heading("Category", text="Category")
        product_treeview.heading("Supplier", text="Supplier")

        product_treeview.column("ID", width=50)
        product_treeview.column("Name", width=150)
        product_treeview.column("INR Price ₹", width=100)
        product_treeview.column("Duety Charge", width=100)
        product_treeview.column("Cost", width=100)
        product_treeview.column("Profit", width=130)
        product_treeview.column("Selling Price", width=90)
        product_treeview.column("Remark", width=100)
        product_treeview.column("Size", width=100)
        product_treeview.column("Gram", width=100)
        product_treeview.column("Category", width=100)
        product_treeview.column("Supplier", width=100)
        product_treeview.pack(fill=BOTH, expand=1)
        product_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, productID_entry, productname_entry, price_entry, remark_entry,size_combobox,gram_entry, product_treeview))
        treeview_data(product_treeview)





    def exit_app():
        window.destroy()


    def update():

        date_time=time.strftime('%I:%M:%S %p on %A,%B %d,%Y')
        subtitle_label.config(text=f'{date_time}')
        subtitle_label.after(1000,update)
        
    update()





    window.mainloop()