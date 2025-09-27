from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from manageProducts import managingproduct
from managecustomer import managecust
from manageSupplier import manageSup
from mangecategory import managecat
from mangaesale import managesales
from cashflow import manageCash
from deposits import managedeposits
from expenses import manageExpenses
from fardarDomestic import Farder
from douty_charger import manageDouty_charges
from manageProducts import connect_database
import time
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
import matplotlib.pyplot as plt
from tkinter import messagebox





def open_dashboard():
    window = Tk()
    window.title("Dashboard")
    window.geometry("1350x690+0+0")
    window.configure(bg="white")
    window.resizable(True, True)
    





    #heading frame------------------------------------------------------------------------------------------------
    heading_frame = Frame(window,bg="white")
    heading_frame.pack(side=TOP,fill=X)

    Title_label=Label(heading_frame,text="Welcome Back",font=("Times new roman",20,"bold"),fg="black",anchor="w",bg="white")
    Title_label.pack(padx=20,pady=10,fill=X)
    line_label=Label(window,bg="#423F3F",anchor="w")
    line_label.pack(fill=X)

    subtitle_label=Label(heading_frame,text="Time: 00:00:00\tDate: 15th June 2025",font=("Times new roman",15,"bold"),fg="black",anchor="w",bg="white")
    subtitle_label.pack(padx=20,pady=5,fill=X)
    #-------------------------------------------------------------------------------------------------------------

    leftframe = Frame(window, bg="black")
    leftframe.pack(side=LEFT, fill=Y)   

    heading_label = Label(leftframe,text="@ Attire Empire",font=("fire sans",20,"bold"),fg="white",bg="black")
    heading_label.pack(padx=0,pady=10) 
    #buttons

    producticon = PhotoImage(file='assests/dress.png')
    productbutton = Button(leftframe, image=producticon, compound=LEFT, text=' Product', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda : managingproduct(window))
    productbutton.pack(fill=X)

    customericon = PhotoImage(file='assests/users.png')
    customerbutton = Button(leftframe, image=customericon, compound=LEFT, text=' Customers', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda: managecust(window))
    customerbutton.pack(fill=X)

    suppliericon = PhotoImage(file='assests/hotel-supplier.png')
    supplierbutton = Button(leftframe, image=suppliericon, compound=LEFT, text=' Supplier', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda: manageSup(window))
    supplierbutton.pack(fill=X)

    salesicon = PhotoImage(file='assests/fashion.png')
    salesbutton = Button(leftframe, image=salesicon, compound=LEFT, text=' Sales', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda:managesales(window))
    salesbutton.pack(fill=X)

    categoryicon = PhotoImage(file='assests/categorization.png')
    categorybutton = Button(leftframe, image=categoryicon, compound=LEFT, text=' Category', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda: managecat(window))
    categorybutton.pack(fill=X)

    Inverstmenticon = PhotoImage(file='assests/cash-flow.png')
    Inverstmentbutton = Button(leftframe, image=Inverstmenticon, compound=LEFT, text=' Cash Flow', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command= lambda: manageCash(window))
    Inverstmentbutton.pack(fill=X)

    depositsicon = PhotoImage(file='assests/money.png')
    depositsbutton = Button(leftframe, image=depositsicon, compound=LEFT, text='Supplier Payments', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda: managedeposits(window) )
    depositsbutton.pack(fill=X)

    expensesicon = PhotoImage(file='assests/expenses.png')
    expensesbutton = Button(leftframe, image=expensesicon, compound=LEFT, text=' Expenses', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda: manageExpenses(window))
    expensesbutton.pack(fill=X)

    fardaricon = PhotoImage(file='assests/motorbike.png')
    fardarbutton = Button(leftframe, image=fardaricon, compound=LEFT, text=' Fardar Domestic ', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command= lambda: Farder(window))
    fardarbutton.pack(fill=X)

    deliveryicon = PhotoImage(file='assests/delivery-van.png')
    deliverybutton = Button(leftframe, image=deliveryicon, compound=LEFT, text=' Duty Chargers ', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command= lambda :manageDouty_charges(window))
    deliverybutton.pack(fill=X)

    exiticon = PhotoImage(file='assests/logoutt.png')
    exitbutton = Button(leftframe, image=exiticon, compound=LEFT, text=' Exit', fg='white', bg='black', font=('Karla', 15, 'bold'), anchor='w', padx=20, bd=0, pady=10, activebackground='black',cursor='hand2',command=lambda:exit_app())
    exitbutton.pack(fill=X)


    # Main container to hold all three frames in one row
    stats_container = Frame(window, bg='white')
    stats_container.pack(side=TOP, anchor='n', pady=10)

    # Analytic Frame
    analytic_frame = Frame(stats_container, bg='black', bd=3, relief=RIDGE)
    analytic_frame.pack(side=LEFT, padx=10)

    total_sale_label = Label(analytic_frame, text='Total Sales', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_sale_label.pack(pady=10)

    sale_count_label = Button(analytic_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black', bd=2, command=lambda: sales_reveal())
    sale_count_label.pack(pady=10)

    # Expense Frame
    expense_frame = Frame(stats_container, bg='black', bd=3, relief=RIDGE)
    expense_frame.pack(side=LEFT, padx=10)

    total_expense_label = Label(expense_frame, text='Total Expense', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_expense_label.pack(pady=10)

    expense_count_label = Button(expense_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black', bd=2, command=lambda: expense_reveal())
    expense_count_label.pack(pady=10)

    # Deposits Frame
    deposits_frame = Frame(stats_container, bg='black', bd=3, relief=RIDGE)
    deposits_frame.pack(side=LEFT, padx=10)

    total_deposit_label = Label(deposits_frame, text='Total Deposits', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_deposit_label.pack(pady=10)

    deposit_count_label = Button(deposits_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black', bd=2, command=lambda: deposit_reveal())
    deposit_count_label.pack(pady=10)






    analy_frame = Frame(window, bg='black', bd=3, relief=RIDGE)
    analy_frame.pack(side=LEFT, anchor='w',  padx=10, pady=10)

    total_products_label = Label(analy_frame, text='Total Products', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_products_label.pack(pady=10)
    product_count_label = Button(analy_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black',bd=2,command=lambda: product_reveal())
    product_count_label.pack(pady=10)



    customer_frame = Frame(window, bg='black', bd=3, relief=RIDGE)
    customer_frame.pack(side=LEFT, anchor='w',  padx=10, pady=10)

    total_cus_label = Label(customer_frame, text='Total Customers', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_cus_label.pack(pady=10)
    cus_count_label = Button(customer_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black',bd=2,command=lambda: customer_reveal())
    cus_count_label.pack(pady=10)



    cashflow_frame = Frame(window, bg='black', bd=3, relief=RIDGE)
    cashflow_frame.pack(side=LEFT,anchor='w',  padx=10, pady=10)

    total_cashflow_label = Label(cashflow_frame, text='Total Cashflow', font=('Karla', 25, 'bold'), fg='white', bg='black')
    total_cashflow_label.pack(pady=10)
    cash_count_label = Button(cashflow_frame, text='Reveal', font=('Karla', 20, 'bold'), fg='white', bg='black',bd=2,command=lambda: cashflow_reveal())
    cash_count_label.pack(pady=10)



    def sales_reveal():
        # --- Update total sales label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT SUM(total_amount) FROM sales_data")
                result = cursor.fetchone()
                total_sales = result[0] if result[0] is not None else 0
                sale_count_label.config(text=f"Rs. {total_sales:,.2f}")
            except Exception as e:
                sale_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            sale_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, update)


    def expense_reveal():
        # --- Update total sales label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT SUM(amount) FROM expenses_data")
                result = cursor.fetchone()
                total_sales = result[0] if result[0] is not None else 0
                expense_count_label.config(text=f"Rs. {total_sales:,.2f}")
            except Exception as e:
                expense_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            expense_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, update)

    def deposit_reveal():
        # --- Update total sales label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT SUM(amount) FROM payments_data")
                result = cursor.fetchone()
                total_sales = result[0] if result[0] is not None else 0
                deposit_count_label.config(text=f"Rs. {total_sales:,.2f}")
            except Exception as e:
                deposit_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            deposit_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, update)

    def product_reveal():
        # --- Update product count label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT COUNT(*) FROM product_data")
                result = cursor.fetchone()
                product_count = result[0] if result[0] is not None else 0
                product_count_label.config(text=f"{product_count}")
            except Exception as e:
                product_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            product_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, product_reveal)

    def customer_reveal():
        # --- Update product count label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT COUNT(*) FROM customer_data")
                result = cursor.fetchone()
                product_count = result[0] if result[0] is not None else 0
                cus_count_label.config(text=f"{product_count}")
            except Exception as e:
                cus_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            cus_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, product_reveal)

    def cashflow_reveal():
        # --- Update total sales label ---
        cursor, connection = connect_database()
        if cursor and connection:
            try:
                cursor.execute("USE attire_empire")
                cursor.execute("SELECT SUM(Amount) FROM cash_flow")
                result = cursor.fetchone()
                total_sales = result[0] if result[0] is not None else 0
                cash_count_label.config(text=f"Rs. {total_sales:,.2f}")
            except Exception as e:
                cash_count_label.config(text="Error")
            finally:
                cursor.close()
                connection.close()
        else:
            cash_count_label.config(text="Error")

        # --- Schedule this function to run again after 1000ms (1 sec) ---
        subtitle_label.after(1000, update)

    def exit_app():
        window.destroy()


    def update():

        date_time=time.strftime('%I:%M:%S %p on %A,%B %d,%Y')
        subtitle_label.config(text=f'{date_time}')
        subtitle_label.after(1000,update)


        
    update()
    window.mainloop()  