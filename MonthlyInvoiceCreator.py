# Monthly Invoice
from fpdf import FPDF
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk
from dateutil.relativedelta import *

def getFileDir():
    file = open("PATH.txt", 'r')
    path = file.read()
    file.close()
    return path

def setFileDir(newPath):
    #Delete File name at the end of the file path to save the folder the previous file was saved in
    list = newPath.split('"\"')
    list.pop()
    newWord = ""
    for dir in list:
        newWord = dir + '"\"'
    file = open("PATH.txt", 'w')
    file.write(newWord)
    file.close()

def fixPriceFormat(price):
    list = price.split(".")
    if len(list[1]) < 2:
        price = price + '0'
    return price

def getDateText(date_input):
    lines = []
    lines.append("Invoice Date:")
    if date_input == '':    
        now = datetime.now() # current date and time
        lines.append(now.strftime("%m/%d/%Y"))
    else:
        date_object = datetime.strptime(date_input, '%m/%d/%Y') #use date provided
        lines.append(date_object.strftime(" %m/%d/%Y"))
    return lines

def getBethelText(bethel_no):
    lines = []
    addresses = ["\t\t\t\t\t\t\t\t\t\t\t\t\t\t11524 Prospect Place\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tGlenn Dale, MD 20769\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tUnited States", "\t\t\t\t\t\t\t\t\t\t\t\t\t\t1416 King's Manor Drive\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tBowie, MD 20721\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tUnited States", "\t\t\t\t\t\t\t\t\t\t\t\t\t\t10100 Cleary Lane\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tBowie, MD 29721\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tUnited States"]
    lines.append("\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + "Bethel Assisted Living Homes " + bethel_no + ' LLC')
    lines.append(addresses[int(bethel_no) - 1] )     
    return lines 

def getResidentText(resident, responsibleParty, address, city, state, zip):
    lines = []
    address = "\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + address + "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + city + ", " + state + " " + zip + "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\tUnited States"
    lines.append("\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + resident + '/' + responsibleParty)
    lines.append(address)
    return lines

def CreatePDF(inputList, filename, num,):

    BethelLines = getBethelText(num)
    ResidentLines = getResidentText(inputList[2], inputList[3], inputList[4], inputList[5], inputList[6], inputList[7])
    Cost = inputList[8]

    pdf = FPDF()
    pdf.set_auto_page_break(True)
    pdf.add_page()
    pdf.set_font("Times", size = 25)

    #Add the Logo
    pdf.image('bethelLogo.png', x = 20, y = 10, w = 60, h = 40, type = 'PNG',)
    pdf.set_font("Times", size = 20)
    pdf.cell(0, 5, txt = "Invoice", ln = 2, align = "R")
    pdf.set_font("Times", size = 14)
    pdf.multi_cell(0, 5, "\nBalance Due:\n" + Cost, align = 'R')
    pdf.cell(0, 20, txt = "", ln = 2, align = 'L')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    pdf.set_font("Times", size = 12)

    #Create Bethel number Section in PDF
    pdf.cell(90, 5, txt = BethelLines[0], ln = 2, align = 'L')
    pdf.multi_cell(90, 5, txt = BethelLines[1], align = 'L')
    pdf.cell(200, 10, txt = "", ln = 2, align = 'L')

    #Create Resident and Responsible Party Section in PDF
    pdf.cell(60, 5, txt = "\t\t\t\t\t\t\t\t\t\t\t\t\t\tBill To" + "                                                                                   " + getDateText(inputList[0])[0] + "             " + getDateText(inputList[0])[1], ln = 1, align = 'L')

    pdf.cell(0, 5, txt = ResidentLines[0] + "", ln = 2, align = 'L')
    pdf.multi_cell(90, 5, txt = ResidentLines[1], align = 'L')
    pdf.cell(0, 0, txt = "Due Date:              " + inputList[1]  + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", ln = 2, align = 'R')
    
    pdf.cell(0, 25, txt = "", ln = 2, align = 'L')

    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tItem Description                                     Qty                            Rate                          Amount", ln = 2, align='L')
    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t__________________________________________________________________________", ln = 2, align='L')
    pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tMonthly Care                                           1                            "+ Cost +"                       " + Cost, ln = 2, align='L')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\t                                                                           Subtotal                 " +  Cost, ln = 2, align='L')
    pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\t                                                                            Total                     " +  Cost, ln = 2, align='L')

    pdf.cell(0, 20, txt = "", ln = 2, align = 'L')

    pdf.set_font("Times", size=12)
    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\tNotes", ln = 2, align='L')
    pdf.set_font("Times", size=10)
    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tThanks for your business.", ln = 2, align='L')

    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')

    pdf.set_font("Times", size=12)
    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\tTerms & Conditions", ln = 2, align='L')
    pdf.set_font("Times", size=10)
    pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tDue on reciept", ln = 2, align='L')

    pdf.output(filename)

def CreateMultiPDF(inputList, filename, num):

    BethelLines = getBethelText(num)
    ResidentLines = getResidentText(inputList[1], inputList[2], inputList[3], inputList[4], inputList[5], inputList[6])
    Cost = inputList[7]

    dates = []
    fileDateList = []

    date_object = datetime.strptime(inputList[0], '%m/%d/%Y') # current date and time

    

    for _ in range(12):
        thisList = []

        fileDateList.append(date_object.strftime("%b%Y"))

        thisList.append(date_object.strftime("%m/23/%Y"))

        date_object = date_object+relativedelta(months=+1)

        thisList.append(date_object.strftime("%m/01/%Y"))

        

        dates.append(thisList)

    print(fileDateList)

    for iter in range(1, 13):
        pdf = FPDF()
        pdf.set_auto_page_break(True)
        pdf.add_page()
        pdf.set_font("Times", size = 25)

        #Add the Logo
        pdf.image('bethelLogo.png', x = 20, y = 10, w = 60, h = 40, type = 'PNG',)
        pdf.set_font("Times", size = 20)
        pdf.cell(0, 5, txt = "Invoice", ln = 2, align = "R")
        pdf.set_font("Times", size = 14)
        pdf.multi_cell(0, 5, "\nBalance Due:\n" + Cost, align = 'R')
        pdf.cell(0, 20, txt = "", ln = 2, align = 'L')
        pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
        pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
        pdf.set_font("Times", size = 12)

        #Create Bethel number Section in PDF
        pdf.cell(90, 5, txt = BethelLines[0], ln = 2, align = 'L')
        pdf.multi_cell(90, 5, txt = BethelLines[1], align = 'L')
        pdf.cell(200, 10, txt = "", ln = 2, align = 'L')

        #Create Resident and Responsible Party Section in PDF
        pdf.cell(60, 5, txt = "\t\t\t\t\t\t\t\t\t\t\t\t\t\tBill To" + "                                                                                   " + "Invoice Date:" + "             " + dates[iter-1][0], ln = 1, align = 'L')

        pdf.cell(0, 5, txt = ResidentLines[0] + "", ln = 2, align = 'L')
        pdf.multi_cell(90, 5, txt = ResidentLines[1], align = 'L')
        pdf.cell(0, 0, txt = "Due Date:              " + dates[iter-1][1]  + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", ln = 2, align = 'R')
        
        pdf.cell(0, 25, txt = "", ln = 2, align = 'L')

        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tItem Description                                     Qty                            Rate                          Amount", ln = 2, align='L')
        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t__________________________________________________________________________", ln = 2, align='L')
        pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tMonthly Care                                           1                            "+ Cost +"                       " + Cost, ln = 2, align='L')
        pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
        pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\t                                                                           Subtotal                 " +  Cost, ln = 2, align='L')
        pdf.cell(0, 10, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\t                                                                            Total                     " +  Cost, ln = 2, align='L')

        pdf.cell(0, 20, txt = "", ln = 2, align = 'L')

        pdf.set_font("Times", size=12)
        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\tNotes", ln = 2, align='L')
        pdf.set_font("Times", size=10)
        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tThanks for your business.", ln = 2, align='L')

        pdf.cell(0, 10, txt = "", ln = 2, align = 'L')

        pdf.set_font("Times", size=12)
        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\tTerms & Conditions", ln = 2, align='L')
        pdf.set_font("Times", size=10)
        pdf.cell(0, 5, txt= "\t\t\t\t\t\t\t\t\t\t\t\t\t\tDue on reciept", ln = 2, align='L')

        pdf.output(filename.split(".")[0] + "(" + fileDateList[iter-1] + ")."  + filename.split(".")[1])

def getGeneralInfo(frame):
    list = []
    for entry in frame.winfo_children(): # for each entry in the list frame
            if(entry.winfo_class() == "Entry"): # do this only for entries
                value = str(entry.get())
                list.append(value)
    return list

def createLabelFrame(container, year):
    s = ttk.Style()
    s.configure('Label.TFrame', background='lightgrey')

    frame = ttk.Frame(container, padding='5', style="Label.TFrame",)

    if year == '1':
        label = ttk.Label(frame, text="Start Date - (mm/dd/yyyy):", width=30, style="TLabel")
        label.grid(row=0,column=0,)

    else:
        label = ttk.Label(frame, text="Date of Invoice:", width=30, style="TLabel")
        label.grid(row=0,column=0,)

    if year != '1':
        label = ttk.Label(frame, text="Invoice Due Date (mm/dd/yyyy):", width=30, style="TLabel")
        label.grid(row=1,column=0,)

    label = ttk.Label(frame, text="Resident:", width=30, style="TLabel")
    label.grid(row=2,column=0,)

    label = ttk.Label(frame, text="Responsible Party:", width=30, style="TLabel")
    label.grid(row=3,column=0,)

    label = ttk.Label(frame, text="Responsible Party Street Address:", width=30, style="TLabel")
    label.grid(row=4,column=0,)

    label = ttk.Label(frame, text="City:", width=30, style="TLabel")
    label.grid(row=5,column=0,)

    label = ttk.Label(frame, text="State:", width=30, style="TLabel")
    label.grid(row=6,column=0,)

    label = ttk.Label(frame, text="Zip:", width=30, style="TLabel")
    label.grid(row=7,column=0,)

    label = ttk.Label(frame, text="Monthly Cost (X.XX):", width=30, style="TLabel")
    label.grid(row=8,column=0,)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame

def createInputFrame(container, year):

    def callback(input): # for zipcode
        if input.isdigit() and len(input) < 6:
            return True
        if input == "":
            return True
        else:
            return False
    
    def callback2(input): # for State
        if input.isalpha() and len(input) < 3:
            return True
        if input == "":
            return True
        else:
            return False

    def PriceBox(event):
        entry = event.widget
        price = entry.get()
        dollars = price.split('.')[0]
        cents = price.split('.')[1]

        if event.char.isdigit() or event.char == '\b':
            if price == "0.00" and event.char.isdigit(): # empty
                entry.delete(0, "end")
                entry.insert(0, '0.0')
            
            elif price[0] == '0' and price[2] == '0' and event.char.isdigit(): # has 2 zeroes
                entry.delete(0, "end")
                entry.insert(0, "0." + price[3])

            elif price[0] == '0' and event.char.isdigit(): # 1 zero
                entry.delete(0, "end")
                entry.insert(0, price[2] + '.' + price[3])

            elif event.char.isdigit():
                dollars = dollars + cents[0]
                cents = cents[1]
        
                entry.delete(0, tk.END)
                entry.insert(0, dollars + '.' + cents)

            elif price == "0.00" and event.char == '\b': # empty
                entry.delete(0, "end")
                entry.insert(0, '0.000')
            
            elif event.char == '\b' and len(price) == 4 and price[0] + price[2] == '00':
                entry.delete(0, "end")
                entry.insert(0, '0.000')

            elif event.char == '\b' and len(price) == 4:
                entry.delete(len(price) - 3, len(price) - 2)
                entry.insert(len(price) - 4, '.')
                entry.insert(0, '0')

            elif event.char == '\b' and len(price) > 4:
                entry.delete(len(price) - 3, len(price) - 2)
                entry.insert(len(price) - 4, '.')

            elif event.char == '\b' and len(price) == 4 and price[0] == '0':
                entry.delete(0, tk.END)
                entry.insert(0, '0' + '.' + '0' + cents[3])

            elif event.char == '\b' and len(price) == 4 and price[0] == '0' and price[2 == '0']:
                entry.delete(0, tk.END)
                entry.insert(0, "0.00")
            
            elif len(price) - len(entry.get()) > 1 or len(price) - len(entry.get()) < -1 or entry.get().find('.') == -1:
                entry.delete(0, tk.END)
                entry.insert(0, price)
        
        else:
            return "break"


    reg = container.register(callback)
    reg2 = container.register(callback2)

    s = ttk.Style()
    s.configure('Input.TFrame', background='lightgrey')
    frame = ttk.Frame(container, padding='5', style="Input.TFrame")

    # Create Entry Space for Date
    date = tk.StringVar(frame)
    now = datetime.now() # current date and time

    InvoiceDateEntry = tk.Entry(frame, width = 45, bg="white", )
    InvoiceDateEntry.grid(row = 0, column = 1)
    InvoiceDateEntry.insert(0, now.strftime("%m/23/%Y")) # Put date for today in the date box
    

    if year != '1':
        dueDateEntry = tk.Entry(frame, width = 45, bg="white", )
        dueDateEntry.grid(row = 1, column = 1)
        dueDateEntry.insert(0, (now+relativedelta(months=+1)).strftime("%m/01/%Y")) # Put date for today in the date box
    
    # Create Entry Space for Resident
    resident = tk.StringVar(frame)
    ResidentEntry = tk.Entry(frame, width = 45, bg="white")
    ResidentEntry.grid(row = 2, column = 1)

    # Create Entry Space for Responsible Party
    responsibleParty = tk.StringVar(frame)
    responsiblePartyEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyEntry.grid(row = 3, column = 1)

    # Create Entry Space for Responsible Party
    responsiblePartyAddress = tk.StringVar(frame)
    responsiblePartyAddressEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyAddressEntry.grid(row = 4, column = 1)
    
    responsiblePartyCity = tk.StringVar(frame)
    responsiblePartyCityEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyCityEntry.grid(row = 5, column = 1)

    responsiblePartyState = tk.StringVar(frame)
    responsiblePartyStateEntry = tk.Entry(frame, width = 45, bg="white", validate = "key", validatecommand = (reg2, '%P'))
    responsiblePartyStateEntry.grid(row = 6, column = 1)

    responsiblePartyZip = tk.StringVar(frame)
    responsiblePartyZipEntry = tk.Entry(frame, width = 45, bg="white", validate = "key", validatecommand = (reg, '%P'))
    responsiblePartyZipEntry.grid(row = 7, column = 1)

    
    monthlyCost = tk.StringVar(frame)

    monthlyCostEntry = tk.Entry(frame, width = 45, bg="white",)
    monthlyCostEntry.grid(row = 8, column = 1)
    monthlyCostEntry.insert(0, "0.00")
    monthlyCostEntry.bind('<Key>', PriceBox)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
    return frame

def createFrame2(container, num, year): # Holds Just Single Entries
    def clear_frame2():
        container.unbind('<Return>')
        for widgets in container.winfo_children():
            widgets.destroy()
        # Create Page 1
        Frame1 = createFrame1(root)
        Frame1.grid(column=0, row=0, columnspan=2)

    def createInvoice(): # inputList, fullList, filename

        generalInfoList = getGeneralInfo(inputFrame)

        filename = filedialog.asksaveasfilename(title = "Save Invoice As", filetypes = (("PDF Files", "*.pdf*"), ("all files", "*.*")), defaultextension=".pdf", initialdir=getFileDir(),)
        setFileDir(filename)
        if year == "1":
            CreateMultiPDF(generalInfoList, filename, num)
        else:
            CreatePDF(generalInfoList, filename, num)

    def focusNextEntry(event):
        thisWidget = event.widget
        while thisWidget.tk_focusNext().winfo_class() != "Entry":
            thisWidget = thisWidget.tk_focusNext()
        thisWidget.tk_focusNext().focus()

    container.bind('<Return>', focusNextEntry)
    s = ttk.Style()
    s.configure('TButton',anchor='n')
    s.configure('Window2.TFrame', background='lightgrey')
    s.configure('b1.TButton',  background="lightgrey", anchor="W")
    frame = ttk.Frame(container, width='600', height=1000, padding='5', style='Window2.TFrame',)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=2)

    label = ttk.Label(frame, text="Resident Information", width=20, anchor='n', font=('48'), justify="center", style="TLabel",)
    label.grid(row=0, column=0,columnspan=2)

    labelFrame = createLabelFrame(frame, year)
    labelFrame.grid(row=2, column=0, columnspan=1)

    inputFrame = createInputFrame(frame, year)
    inputFrame.grid( row=2, column=1,)

    goBack = ttk.Button(frame, text = 'Go Back', style='b1.TButton', command=clear_frame2)
    goBack.grid(row=3, column=0, columnspan=1)

    submit = ttk.Button(frame, text = 'Create Invoice', style='b1.TButton', command=createInvoice)
    submit.grid(row=3, column=1, columnspan=1)
    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
    spacer = ttk.Label(frame, text="", width=15, anchor='n', font='14', justify="center", style="TLabel")
    spacer.grid(row=1, column=0,columnspan=2, pady=3)
    return frame



def createFrame1(container): # Holds initial survey to generate page 2   
    def clear_frame():       
        container.unbind('<Return>')

        for widgets in container.winfo_children():
            widgets.destroy()

        num = bethelNumber.get()
        year = numInvoices.get()

        # Create Page 2 first frame
        Frame2 = createFrame2(container, num, year)
        Frame2.grid(column=0, row=0,columnspan=2)
        Frame2.grid_propagate(0) 

    def clear_frame_wEnter(event):
        container.unbind('<Return>')   
        for widgets in container.winfo_children():
            widgets.destroy()
        
        num = bethelNumber.get()
        year = numInvoices.get()

        # Create Page 2  frame
        Frame2 = createFrame2(container, num, year)
        Frame2.grid(column=0, row=0,)
        Frame2.grid_propagate(0)

    container.bind('<Return>', clear_frame_wEnter)
    s = ttk.Style()
    s.configure("Window1.TFrame", background='lightgrey',)
    s.configure('RadioStyle.TRadiobutton', font=('', 10), background="lightgrey", justify="center")
    s.configure('b1.TButton', background="lightgrey")
    frame = ttk.Frame(container, style="Window1.TFrame", width=1175, height=600)

    # Create Radio Buttons for Bethel Number
    bethelNumber = tk.StringVar(frame, value=1)
    bethelRadio1 = ttk.Label(frame, text="Which Bethel are you creating this invoice for?", font=('14'))
    bethelRadio1.grid(row = 1, column = 0, )
    bethelRadio2 = ttk.Radiobutton(frame,text="1",value="1",variable=bethelNumber, style='RadioStyle.TRadiobutton')
    bethelRadio2.grid(row = 1, column = 1)
    bethelRadio3 = ttk.Radiobutton(frame,text="2",value="2",variable=bethelNumber, style='RadioStyle.TRadiobutton')
    bethelRadio3.grid(row = 1, column = 2)
    bethelRadio4 = ttk.Radiobutton(frame,text="3",value="3",variable=bethelNumber, style='RadioStyle.TRadiobutton')
    bethelRadio4.grid(row = 1, column = 3)

    # Create Radio Buttons for Podiatry
    numInvoices = tk.StringVar(frame)
    numInvoicesButton = tk.Checkbutton(frame, variable=numInvoices, text="Print invoices for a whole year?", font=('14'), background='lightgrey')
    numInvoicesButton.deselect()
    numInvoicesButton.grid(row = 2, column = 0, columnspan='4')

    submit = ttk.Button(frame, text = "Next", command=clear_frame, style='b1.TButton')
    submit.grid(row=4, column=0, columnspan='4')

    for widget in frame.winfo_children():
        widget.grid(padx=5, pady=15)
    return frame

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1175x600')
    root.resizable(False, True)
    root.title('Bethel Assisted Living Homes Invoice Creator')
    root.configure(background='lightgrey')

    # Set the Program's Icon
    photo = tk.PhotoImage(file = 'bethelLogo.png')
    root.wm_iconphoto(False, photo)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)
    s = ttk.Style()
    s.configure("TLabel", background="lightgrey")

    # Create Page 1
    Frame1 = createFrame1(root)
    Frame1.grid(column=0, row=0, columnspan=2)

    root.mainloop()