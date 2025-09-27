from tkinter import *
from tkinter import ttk
import customtkinter
from tkinter import  END
from tkinter import messagebox




def calculator_form(window):
    calculator_frame = Toplevel(window)
    calculator_frame.title("Calculator")
    calculator_frame.geometry("660x660+500+10")
    calculator_frame.configure(bg="white")
    calculator_frame.resizable(False, False)



    buttons_frame = Frame(calculator_frame,width=300,height=300,bg="black",bd=3,relief=GROOVE)
    buttons_frame.pack(pady=20,padx=20)

    def clear():
        entryfeild.delete(0,END)

    def click(number):
        entryfeild.insert(END,number)

    def answer():
        expression= entryfeild.get()
        ##to evaluvate the the expresssion 
        try:
            result=eval(expression)
            answer=(round (result,1))
            entryfeild.delete(0,END)
            entryfeild.insert(0,answer)
        except SyntaxError:
            messagebox.showerror("Error","invalid Expression")
        except ZeroDivisionError:
            messagebox.showerror("Error","Division by zero is not allowed")











    # , =
    entryfeild =customtkinter.CTkEntry(buttons_frame,font=('arial',20,'bold'),text_color='white',fg_color='black',border_color='white',width=280,height=50,bg_color='black')
    entryfeild.grid(row =0,column=0,pady=10,padx=10,columnspan=4)

    button7=customtkinter.CTkButton(buttons_frame,text='7',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('7'))
    button7.grid(row=1,column=0)
    button8=customtkinter.CTkButton(buttons_frame,text='8',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('8'))
    button8.grid(row=1,column=1)
    button9=customtkinter.CTkButton(buttons_frame,text='9',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('9'))
    button9.grid(row=1,column=2)
    buttonplus=customtkinter.CTkButton(buttons_frame,text='+',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('+'))
    buttonplus.grid(row=1,column=3)

    button4=customtkinter.CTkButton(buttons_frame,text='4',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('4'))
    button4.grid(row=2,column=0,pady=10)
    button5=customtkinter.CTkButton(buttons_frame,text='5',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('5'))
    button5.grid(row=2,column=1)
    button6=customtkinter.CTkButton(buttons_frame,text='6',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('6'))
    button6.grid(row=2,column=2)
    buttonminus=customtkinter.CTkButton(buttons_frame,text='-',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('-'))
    buttonminus.grid(row=2,column=3)

    button1=customtkinter.CTkButton(buttons_frame,text='1',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('1'))
    button1.grid(row=3,column=0)
    button2=customtkinter.CTkButton(buttons_frame,text='2',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('2'))
    button2.grid(row=3,column=1)
    button3=customtkinter.CTkButton(buttons_frame,text='3',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('3'))
    button3.grid(row=3,column=2)
    buttonmultiply=customtkinter.CTkButton(buttons_frame,text='*',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('*'))
    buttonmultiply.grid(row=3,column=3)

    button0=customtkinter.CTkButton(buttons_frame,text='0',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('0'))
    button0.grid(row=4,column=0,pady=10)
    buttondot=customtkinter.CTkButton(buttons_frame,text='.',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',command=lambda : click('.'))
    buttondot.grid(row=4,column=1)
    buttonclear=customtkinter.CTkButton(buttons_frame,text='C',
                                        font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',fg_color='red',hover_color='red4',command=clear)
    buttonclear.grid(row=4,column=2)
    buttondivision=customtkinter.CTkButton(buttons_frame,text='/',font=('arial',20,'bold'),width=60,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('/'))
    buttondivision.grid(row=4,column=3)

    bequall=customtkinter.CTkButton(buttons_frame,text='=',font=('arial',30,'bold'),width=280,bg_color='black',cursor='hand2',fg_color='green',hover_color='green2',command=answer)
    bequall.grid(row=5,column=0,pady=10,columnspan=4)



















