import tkinter as tk
from time import strftime, time
from tkinter import messagebox
import json

def fout():
    global data
    with open("data.json", "w") as fout:
        json.dump(data, fout)

def fin():
    global data
    with open("data.json", "r") as fin:
        data = json.load(fin)
    
def update_record(data):
    lb_display_record.insert(0,data["Record"][0][0])

def update_analysis(data):
    try:
        per_T1=round(data["T1"][0]/(data["T1"][0]+data["T2"][0]+data["T3"][0])*100, 2)
        lbl_T1["text"]=f'MANDATORY: {data["T1"][0]} ({per_T1}% totally)'
    except:
        pass
    
    try:    
        per_T2=round(data["T2"][0]/(data["T1"][0]+data["T2"][0]+data["T3"][0])*100, 2)
        lbl_T2["text"]=f'WASTED: {data["T2"][0]} ({per_T2}% totally)'
    except:
        pass
    try:
        per_T3=round(data["T3"][0]/(data["T1"][0]+data["T2"][0]+data["T3"][0])*100, 2)
        lbl_T3["text"] = f'Need considering: {data["T3"][0]} ({per_T3}% totally)'
    except:
        pass

    try:
        lbl_income_display["text"] = f'INCOME: {data["Income"][0]}'
    except:
        pass

    try:
        lbl_balance["text"]=f'BALANCE: {data["Balance"]}'
    except:
        pass

def add_expense(event):
    global data
    amount = ent_expense_amount.get()
    x = ent_exp_q1.get()
    y = ent_exp_q2.get()
    z = ent_exp_q3.get()
    type = ""
    this_month = strftime("%m/%Y")
    curtime = strftime("%m/%d/%Y, %H:%M:%S")

    try:
        fin()
        amount = int(amount)
        if x == "Y" or x == "y":
            if y == "Y" or y == "y":
                type = "mandatory"
            if y == "N" or y == "n":
                type = "needs considering"
        if x == "N" or x == "n":
            if z == "Y" or z == "y":
                type = "needs considering"
            if z == "N" or z == "n":
                type = "wasted"
    
        if this_month not in data["Month"]:
            data["Month"].insert(0, this_month)
            data["Record"].insert(0, [[curtime, amount, type]])
            data["T1"].insert(0,0)
            data["T2"].insert(0,0)
            data["T3"].insert(0,0)
        elif len(data["T1"]) != len(data["Month"]) +1:
            data["Record"].insert(0, [[curtime, amount, type]])
            data["T1"].insert(0,0)
            data["T2"].insert(0,0)
            data["T3"].insert(0,0)
        else:
            data["Record"][0].insert(0,[curtime, amount, type])
            
        data["Balance"] -= amount
        if type == "mandatory":
            data["T1"][0] += amount
        elif type == "wasted":
            data["T2"][0] += amount
        else:
            data["T3"][0] += amount
        
        fout()   
        print(data) 
        update_analysis(data)
        update_record(data)
        ent_expense_amount.delete(0,"end")
        ent_exp_q1.delete(0,"end")
        ent_exp_q2.delete(0,"end")
        ent_exp_q3.delete(0,"end")

    except:
        messagebox.showerror("Wrong type!!", "Input what you are asked to.")

def add_income(event):
    global data
    income = ent_income_amount.get()

    try:     
        fin()
        income = int(income)
        this_month = strftime("%m/%Y")
        if this_month not in data["Month"]:
            data["Month"].insert(0,this_month)
            data["Income"].insert(0,income)
        elif len(data["Income"]) != len(data["Month"]) +1:
            data["Income"].insert(0,income)
        else:
            data["Income"][0] += income
        data["Balance"] += income
        update_analysis(data)
        fout()
    except:
       messagebox.showerror("Wrong type!!", "You must input a number")
    ent_income_amount.delete(0,"end")
    print(data)

def show_analysis(event):
    
    lb_display_record.grid_forget()
    btn_record["bg"]="#557A95"
    btn_record["fg"]="#5d5c61"
    btn_record.bind("<Button-1>", show_record)
    
    lbl_display_add.grid_forget()
    btn_add["bg"]="#557A95"
    btn_add["fg"]="#5d5c61"
    btn_add.bind("<Button-1>", show_add)

    lbl_display_analysis.grid(row=2, columnspan=3)
    btn_analysis["fg"]="#557A95"
    btn_analysis["bg"]="#5d5c61"
    btn_analysis.unbind("<Button-1>")

def show_add(evnet):
    
    lb_display_record.grid_forget()
    btn_record["bg"]="#557A95"
    btn_record["fg"]="#5d5c61"
    btn_record.bind("<Button-1>", show_record)
   
    lbl_display_analysis.grid_forget()
    btn_analysis["bg"]="#557A95"
    btn_analysis["fg"]="#5d5c61"
    btn_analysis.bind("<Button-1>", show_analysis)


    lbl_display_add.grid(row=2, columnspan=3)
    btn_add["fg"]="#557A95"
    btn_add["bg"]="#5d5c61"
    btn_add.unbind("<Button-1>")

def show_record(event):
    lbl_display_analysis.grid_forget()
    btn_analysis["bg"]="#557A95"
    btn_analysis["fg"]="#5d5c61"
    btn_analysis.bind("<Button-1>", show_analysis)

    lbl_display_add.grid_forget()
    btn_add["bg"]="#557A95"
    btn_add["fg"]="#5d5c61"
    btn_add.bind("<Button-1>", show_add)

    lb_display_record.grid(row=2, columnspan=3)
    btn_record["fg"]="#557A95"
    btn_record["bg"]="#5d5c61"
    btn_record.unbind("<Button-1>")

def show_ent_income(event):
    lbl_expense.grid_forget()
    btn_expense.bind("<Button-1>", show_ent_expense)
    btn_income.unbind("<Button-1>")
    btn_income['fg']="#557A95"
    btn_income['bg']="#5d5c61"
    btn_expense['bg']="#557A95"
    btn_expense['fg']="#5d5c61"
    lbl_income.grid(row=1, columnspan=2)

def show_ent_expense(event):
    lbl_income.grid_forget()
    btn_income.bind("<Button-1>", show_ent_income)
    btn_expense['fg']="#557A95"
    btn_expense['bg']="#5d5c61"
    btn_income['bg']="#557A95"
    btn_income['fg']="#5d5c61"
    btn_expense.unbind("<Button-1>")
    
    lbl_expense.grid(row=1, columnspan=2)

#Data

data ={}


with open("data.json", "r") as r_f:
    data = json.load(r_f)

#Data:end


window = tk.Tk()
window.geometry("330x560+5+5")
#window.resizable(False,False)
window.title("Student Financial Wellbeing")

lbl_month = tk.Label(text=f'{strftime("%m/%Y")}' , font="Cascadia", fg="#5d5c61", background= "#7395AE",width=29, height=2)
lbl_month.grid(row=0, columnspan=3)


#Block of buttons
btn_record = tk.Button(text="Record", font="Cascadia", fg="#557A95", bg= "#5d5c61", width=9)
btn_record.grid(row=1, column=0)

btn_analysis = tk.Button(text="Analysis", font="Cascadia", fg="#5d5c61", bg= "#557A95", width=9)
btn_analysis.grid(row=1, column=1)
btn_analysis.bind("<Button-1>", show_analysis)

btn_add = tk.Button(text="Add", font="Cascadia", fg="#5d5c61", bg= "#557A95", width=9)
btn_add.grid(row=1, column=2)
btn_add.bind("<Button-1>", show_add)

#Display information part
## Display record:
lb_display_record = tk.Listbox(width=50, height=25)
lb_display_record.grid(row=2, columnspan=3)

## Display analysis
lbl_display_analysis = tk.Label(text=" ", height=27, width=46)

lbl_balance = tk.Label(master=lbl_display_analysis, text='BALANCE: 0',width=46, fg="black")
lbl_balance.pack()

lbl_income_display = tk.Label(master=lbl_display_analysis, text='INCOME: 0',width=46, fg="green")
lbl_income_display.pack()

lbl_T1 = tk.Label(master=lbl_display_analysis, text='MANDATORY: 0 (0% totally)',width=46, fg= "#379683") 
lbl_T1.pack()

lbl_T2 = tk.Label(master=lbl_display_analysis, text='WASTED: 0 (0% totally)',width=46, fg="red")
lbl_T2.pack()

lbl_T3 = tk.Label(master=lbl_display_analysis, text='Need considering: 0 (0% totally)',width=46, fg="#577A95")
lbl_T3.pack()


## Display add
lbl_display_add = tk.Label(text=" ", height=27, width=46)

### Button classifying
btn_income = tk.Button(master=lbl_display_add, text= "INCOME",  font="Cascadia", fg="#5d5c61", bg= "#557A95", width=14)
btn_income.grid(row=0, column=0)
btn_income.bind("<Button-1>", show_ent_income)

btn_expense = tk.Button(master=lbl_display_add, text= "EXPENSE",  font="Cascadia", fg="#557A95", bg= "#5d5c61", width=14)
btn_expense.grid(row=0, column=1)
### Display income entry
lbl_income = tk.Label(master=lbl_display_add, width=46, height=10)
#lbl_income.grid(row=1, columnspan=2)
ent_income_amount = tk.Entry(master=lbl_income, width = 30 )
ent_income_amount.grid(row=0, columnspan=2,column=0)

btn_income_commit = tk.Button(master=lbl_income, width=15, text="COMMIT",  fg="#5d5c61", bg= "#557A95")
btn_income_commit.grid(row=0,column=2, columnspan=1)
btn_income_commit.bind("<Button-1>", add_income)


### Display expense entry
lbl_expense = tk.Label(master=lbl_display_add, width=46, height=10)
lbl_expense.grid(row=1, columnspan=2)

ent_expense_amount = tk.Entry(master= lbl_expense, width = 30)
ent_expense_amount.grid(row=0, column=1, columnspan=2)

lbl_amount = tk.Label(master=lbl_expense, width = 17, text = "Amount (int):")
lbl_amount.grid(row=0, column=0, columnspan=1)

lbl_exp_q1 = tk.Label(master=lbl_expense, width=30, text="Is this madatory?(Y/N)")
lbl_exp_q1.grid(row=1,column=0, columnspan=2)
ent_exp_q1 = tk.Entry(master=lbl_expense, width=15)
ent_exp_q1.grid(row=1,column=2)

lbl_exp_q2 = tk.Label(master=lbl_expense, width=30, text="Cheapest choice?(Y/N)")
lbl_exp_q2.grid(row=2,column=0, columnspan=2)
ent_exp_q2 = tk.Entry(master=lbl_expense, width=15)
ent_exp_q2.grid(row=2,column=2)

lbl_exp_q3 = tk.Label(master=lbl_expense, width=30, text="Does this bring about values?(Y/N)")
lbl_exp_q3.grid(row=3,column=0, columnspan=2)
ent_exp_q3 = tk.Entry(master=lbl_expense, width=15)
ent_exp_q3.grid(row=3,column=2)

btn_expense_commit = tk.Button(master=lbl_expense, width=43, text= "COMMIT", fg="#5d5c61", bg= "#557A95")
btn_expense_commit.grid(row=4, columnspan=3)
btn_expense_commit.bind("<Button-1>", add_expense)

#Display inflation.
lbl_display_value = tk.Label(text= " ", bg= "#7395AE", height=4, width=46)
lbl_display_value.grid(row=3, columnspan=3)


lbl_placeholder = tk.Label(text= " ", bg= "#7395AE", height=30, width=46)
lbl_placeholder.grid(row=4, columnspan=3)

# Load data to gui
update_analysis(data)
lb_display_record.delete(0,"end")
for x in data["Record"][0]:
    lb_display_record.insert("end",x)


window.mainloop()