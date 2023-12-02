from fpdf import FPDF
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk

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
    lines.append("Supply Invoice")
    if date_input == '':    
        now = datetime.now() # current date and time
        lines.append(now.strftime(" %B %d, %Y"))
    else:
        date_object = datetime.strptime(date_input, '%m/%d/%Y') #use date provided
        lines.append(date_object.strftime(" %B %d, %Y"))
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

def CreatePDF(inputList, fullList, filename, num):
    pdf = FPDF()
    pdf.set_auto_page_break(True)
    pdf.add_page()
    pdf.set_font("Times", size = 20)

    #Add the Logo
    pdf.image('bethelLogo.png', x = 20, y = 10, w = 45, h = 30.5, type = 'PNG',)
    pdf.cell(0, 20, txt = "", ln = 2, align = 'L')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    pdf.cell(0, 20, txt = getDateText(inputList[0])[0] + "                                  " + getDateText(inputList[0])[1], ln = 2, align = 'C')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    pdf.set_font("Times", size = 12)
    BethelLines = getBethelText(num)
    ResidentLines = getResidentText(inputList[1], inputList[2], inputList[3], inputList[4], inputList[5], inputList[6],)

    #Create Bethel number in PDF
    pdf.cell(90, 5, txt = BethelLines[0], ln = 2, align = 'L')
    pdf.multi_cell(90, 5, txt = BethelLines[1], align = 'L')
    pdf.cell(200, 10, txt = "", ln = 2, align = 'L')

    #Create Resident and Responsible Party in PDF
    pdf.cell(90, 5, txt = ResidentLines[0], ln = 2, align = 'L')
    pdf.multi_cell(90, 5, txt = ResidentLines[1], align = 'L')
    pdf.cell(0, 10, txt = "", ln = 2, align = 'L')
    for item in fullList:
        text = ""
        if isinstance(item['price'], float):
            text = item['item'] + " :           " + '$' + fixPriceFormat(str(item['price']))
            pdf.cell(85, 10, txt = text, ln = 2, align = 'R')
            pdf.cell(0, 5, txt = "", ln = 2, align = 'L')
        elif item['price'] == "N/A":
            text = item['item'] + " :                " + str(item['price'])
            pdf.cell(85, 10, txt = text, ln = 2, align = 'R')
            pdf.cell(0, 5, txt = "", ln = 2, align = 'L')
        else:
            text = item['item'] + " :"
            pdf.cell(90, 10, txt = text, ln = 2, align = 'C')
            iter = 0
            for cost in item['price']:

                if len(item['date']) > 0:
                    text = item['date'][iter] + '  -  ' + '$' + fixPriceFormat(str(cost))
                else:
                    text = '$' + fixPriceFormat(str(cost))

                pdf.cell(85, 5, txt = text, ln = 2, align = 'R')
                pdf.cell(0, 3, txt = "", ln = 2, align = 'L')
                iter += 1
            pdf.cell(0, 2, txt = "", ln = 2, align = 'L')
    pdf.output(filename)

def getListValues(frame3, incIS):
    priceList = []
    dateList = []
    iPriceList = []
    descriptionList = []

    for index, frame in enumerate(frame3.winfo_children()): # for each frame holding a list of entries
        for entry in frame.winfo_children(): # for each entry in the list frame
            if(entry.winfo_class() == "Entry"): # do this only for entries
                value = str(entry.get())

                #print('index', index)
                #print('value', value)

                if incIS == '1': # If incontinent Supplies is checked

                    if index == 2: # this is the index for price list frame
                        priceList.append(float(value))
                    if index == 3: # this is the index for date list frame
                        dateList.append(value)
                    if index == 5: # this is the index for iprice list frame
                        iPriceList.append(float(value))
                    if index == 6: # this is the index for description list frame
                        descriptionList.append(value)
                
                else: # If unchecked
                    if index == 1: # this is the index for price list frame
                        priceList.append(float(value))
                    if index == 2: # this is the index for date list frame
                        dateList.append(value)
    return [priceList, dateList, iPriceList, descriptionList]

def getGeneralInfo(frame):
    list = []
    for entry in frame.winfo_children(): # for each entry in the list frame
            if(entry.winfo_class() == "Entry"): # do this only for entries
                value = str(entry.get())
                list.append(value)
    return list

def createLabelFrame(container, incPod):
    s = ttk.Style()
    s.configure('Label.TFrame', background='lightgrey')

    frame = ttk.Frame(container, padding='5', style="Label.TFrame",)

    label = ttk.Label(frame, text="Date - (mm/dd/yyyy):", width=25, style="TLabel")
    label.grid(row=0,column=0,)

    label = ttk.Label(frame, text="Resident:", width=25, style="TLabel")
    label.grid(row=1,column=0,)

    label = ttk.Label(frame, text="Responsible Party:", width=25, style="TLabel")
    label.grid(row=2,column=0,)

    label = ttk.Label(frame, text="Responsible Party Address:", width=25, style="TLabel")
    label.grid(row=3,column=0,)

    label = ttk.Label(frame, text="City:", width=25, style="TLabel")
    label.grid(row=4,column=0,)

    label = ttk.Label(frame, text="State:", width=25, style="TLabel")
    label.grid(row=5,column=0,)

    label = ttk.Label(frame, text="Zip:", width=25, style="TLabel")
    label.grid(row=6,column=0,)

    label = ttk.Label(frame, text="Medication Supplier:", width=25, style="TLabel")
    label.grid(row=7,column=0,)

    if incPod == '1':
        label = ttk.Label(frame, text="Podiatry Costs (X.XX):", width=25, style="TLabel")
        label.grid(row=8,column=0,)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame

def createInputFrame(container, incPod):

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

    # Create Entry Space for Resident
    date = tk.StringVar(frame)
    now = datetime.now() # current date and time

    DateEntry = tk.Entry(frame, width = 45, bg="white", )
    DateEntry.grid(row = 0, column = 1)
    DateEntry.insert(0, now.strftime("%m/%d/%Y")) # Put date for today in the date box
    
    # Create Entry Space for Resident
    resident = tk.StringVar(frame)
    ResidentEntry = tk.Entry(frame, width = 45, bg="white")
    ResidentEntry.grid(row = 1, column = 1)

    # Create Entry Space for Responsible Party
    responsibleParty = tk.StringVar(frame)
    responsiblePartyEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyEntry.grid(row = 2, column = 1)

    # Create Entry Space for Responsible Party
    responsiblePartyAddress = tk.StringVar(frame)
    responsiblePartyAddressEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyAddressEntry.grid(row = 3, column = 1)
    
    responsiblePartyCity = tk.StringVar(frame)
    responsiblePartyCityEntry = tk.Entry(frame, width = 45, bg="white")
    responsiblePartyCityEntry.grid(row = 4, column = 1)

    responsiblePartyState = tk.StringVar(frame)
    responsiblePartyStateEntry = tk.Entry(frame, width = 45, bg="white", validate = "key", validatecommand = (reg2, '%P'))
    responsiblePartyStateEntry.grid(row = 5, column = 1)

    responsiblePartyZip = tk.StringVar(frame)
    responsiblePartyZipEntry = tk.Entry(frame, width = 45, bg="white", validate = "key", validatecommand = (reg, '%P'))
    responsiblePartyZipEntry.grid(row = 6, column = 1)

    # Create Entry Space for Medication/Medicaiton Supplier
    supplier = tk.StringVar(frame)
    supplierEntry = tk.Entry(frame, width = 45, bg="white")
    supplierEntry.grid(row = 7, column = 1)
    
    if incPod == '1':
        podiatry = tk.StringVar(frame)

        podiatryEntry = tk.Entry(frame, width = 45, bg="white",)
        podiatryEntry.grid(row = 8, column = 1)
        podiatryEntry.insert(0, "0.00")
        podiatryEntry.bind('<Key>', PriceBox)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)
    return frame

def createListFrame(container, listname):

    def PriceBox(event):
        entry = event.widget
        price = entry.get()
        dollars = price.split('.')[0]
        cents = price.split('.')[1]

       # print("event.char = ", event.char)
       # print("entry.get() = ", entry.get())
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


    s = ttk.Style()
    s.configure('b2.TButton',anchor='n', background="lightgrey", height=1, width=2, justify='center')
    s.configure('List.TFrame', background='lightgrey')
    frame  = ttk.Frame(container, width='125', height=1000, padding='5', style="List.TFrame") # Holds Price Label
    frame2 = ttk.Frame(container, width='125', height=1000, padding='5', style="List.TFrame") # Holds Date Label
    frame3 = ttk.Frame(container, width='50', height=1000, padding='5', style="List.TFrame") # Holds Button

    if listname == 'Medications':
        label = ttk.Label(frame, text="Cost (X.XX)", width=20, anchor='n', style="TLabel", )
        label.pack(pady=5)
        label = ttk.Label(frame2, text="Date (mm/dd/yyyy)", width=20, anchor='n', style="TLabel",)
        label.pack(pady=5)
    else:
        label = ttk.Label(frame, text="Cost - (X.XX)", width=20, anchor='n', style="TLabel",)
        label.pack(pady=5)
        label = ttk.Label(frame2, text="Supply Description", width=20, anchor='n', style="TLabel",)
        label.pack(pady=5)

    podiatryc = tk.Entry(frame, width = 30, bg="white",)
    podiatryc.pack(pady=5, side="top")
    podiatryc.insert(0, "0.00")
    podiatryc.bind('<Key>', PriceBox)

    podiatryd = tk.Entry(frame2, width = 30, bg="White", )
    podiatryd.pack(pady=5, side="top")
    

    def myClick():
        podiatryc = tk.Entry(frame, width = 30, bg="white", )
        podiatryc.pack(pady=5, side="top")
        podiatryc.insert(0, "0.00")
        podiatryc.bind('<Key>', PriceBox)

        podiatryd = tk.Entry(frame2, width = 30, bg="White",)
        podiatryd.pack(pady=5, side="top")


    def myClick2():
        if(len(frame.winfo_children()) > 2):
            entry1 = frame.winfo_children()[ len(frame.winfo_children()) - 1 ]
            entry1.destroy()
            entry2 = frame2.winfo_children()[ len(frame2.winfo_children()) - 1 ]
            entry2.destroy()

    add = ttk.Button(frame3, text = "+", command=lambda: myClick(), style="b2.TButton",)
    add.grid(row=0, column=0, ipady=1, ipadx=2)
    remove = ttk.Button(frame3, text = "-", command=lambda: myClick2(), style="b2.TButton")
    remove.grid(row=1, column=0, ipady=1, ipadx=2)
    for widget in frame3.winfo_children():
        widget.grid(padx=0, pady=5,)
    return [frame, frame2, frame3]

def createFrame2(container, num, incPod, incIS, frame3): # Holds Just Single Entries
    def clear_frame2():
        container.unbind('<Return>')
        for widgets in container.winfo_children():
            widgets.destroy()
        # Create Page 1
        Frame1 = createFrame1(root)
        Frame1.grid(column=0, row=0, columnspan=2)

    def createInvoice(): # inputList, fullList, filename
        fullList = []
        total = 0.00
        completeTotal = 0.00
        EntryLists = getListValues(frame3, incIS) 
        generalInfoList = getGeneralInfo(inputFrame)
        thisItem = {"item": generalInfoList[7] + ' Medications' ,"price": EntryLists[0], "date": EntryLists[1]}
        fullList.append(thisItem)
        for price in thisItem["price"]: # calculate Medication total
            total += price
        thisItem = {"item": "Medications Total", "price": round(total, 2), "date": []} # turn it into an item
        fullList.append(thisItem)# add it to the list for invoice
        completeTotal += total # add this total to the complete price
        total = 0.00 # reset total

        if incPod == '1': # if Podiatry Cost was included
            thisItem = {"item": 'Podiatry' ,"price": float(generalInfoList[8]), "date": []}
            completeTotal += thisItem["price"]

        else:
            thisItem = {"item": 'Podiatry' ,"price": 'N/A', "date": []}
        
        fullList.append(thisItem)

        if len(EntryLists[2]) > 0:
            thisItem = {"item": 'Incontinent Supplies' ,"price": EntryLists[2], "date": EntryLists[3]}
            
            fullList.append(thisItem)

            for price in thisItem["price"]: # calculate Incontinent Supplies total
                total += price

            thisItem = {"item": "Supplies Total", "price": round(total, 2), "date": []} # turn it into an item
            fullList.append(thisItem)# add it to the list for invoice
            completeTotal += total # add this total to the complete price

        else:
            thisItem = {"item": 'Incontinent Supplies' ,"price": 'N/A', "date": []}
            fullList.append(thisItem)

        thisItem = {"item": "Total", "price": round(completeTotal, 2), "date": []}
        fullList.append(thisItem)
        filename = filedialog.asksaveasfilename(title = "Save Invoice As", filetypes = (("PDF Files", "*.pdf*"), ("all files", "*.*")), defaultextension=".pdf", initialdir=getFileDir(),)
        setFileDir(filename)
        CreatePDF(generalInfoList, fullList, filename, num)

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
    frame = ttk.Frame(container, width='475', height=1000, padding='5', style='Window2.TFrame',)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(0, weight=2)

    label = ttk.Label(frame, text="General Information", width=15, anchor='n', font=('48'), justify="center", style="TLabel",)
    label.grid(row=0, column=0,columnspan=2)

    labelFrame = createLabelFrame(frame, incPod)
    labelFrame.grid(row=2, column=0, columnspan=1)

    inputFrame = createInputFrame(frame, incPod)
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

def createFrame3(container, incIS): # Holds set of List Entries

    s = ttk.Style()
    s.configure('Window3.TFrame', background='lightgrey')
    frame = ttk.Frame(container, width=700, height=1000, padding='5', style='Window3.TFrame')    
    label = ttk.Label(frame, text="Medications", width=15, anchor='n', font='48', style="TLabel")
    label.grid(row=0, column=0,columnspan=3)
    if incIS == '1':
        label = ttk.Label(frame, text="Incontinent Supplies", width=20, anchor='n', font='48', style="TLabel")
        label.grid(row=0, column=3,columnspan=3)   
    MedicationFrames = createListFrame(frame, 'Medications',)
    MedicationFrames[0].grid(row=1, column=0,) # Price Entry
    MedicationFrames[1].grid(row=1, column=1)  # Date Entry
    MedicationFrames[2].grid(row=1, column=2)  # Button  
    MedicationFrames[0].pack_propagate(0)
    MedicationFrames[1].pack_propagate(0)
    MedicationFrames[2].grid_propagate(0)

    if incIS == '1':
        SupplyFrames = createListFrame(frame, 'Incontinent Supplies',)
        SupplyFrames[0].grid(row=1, column=3,) # Price Entry
        SupplyFrames[1].grid(row=1, column=4)  # Date Entry
        SupplyFrames[2].grid(row=1, column=5)  # Button     
        SupplyFrames[0].pack_propagate(0)
        SupplyFrames[1].pack_propagate(0)
        SupplyFrames[2].grid_propagate(0)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame

def createFrame1(container): # Holds initial survey to generate page 2   
    def clear_frame():       
        container.unbind('<Return>')

        for widgets in container.winfo_children():
            widgets.destroy()

        num = bethelNumber.get()
        incPod = includePodiatry.get()
        incIS = includeIncontinentSupplies.get()

        # Create Page 2 second frame
        Frame3 = createFrame3(container, incIS)
        Frame3.grid(column=1, row=0,)
        Frame3.grid_propagate(0)

        # Create Page 2 first frame
        Frame2 = createFrame2(container, num, incPod, incIS, Frame3)
        Frame2.grid(column=0, row=0,)
        Frame2.grid_propagate(0) 

    def clear_frame_wEnter(event):
        container.unbind('<Return>')   
        for widgets in container.winfo_children():
            widgets.destroy()
        num = bethelNumber.get()
        incPod = includePodiatry.get()
        incIS = includeIncontinentSupplies.get()

        # Create Page 2 second frame
        Frame3 = createFrame3(container, incIS)
        Frame3.grid(column=1, row=0,)
        Frame3.grid_propagate(0)

        # Create Page 2 first frame
        Frame2 = createFrame2(container, num, incPod, incIS, Frame3)
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
    includePodiatry = tk.StringVar(frame)
    podiatryRadio = tk.Checkbutton(frame, variable=includePodiatry, text="Include Podiatry Visit in the Invoice", font=('14'), background='lightgrey')
    podiatryRadio.deselect()
    podiatryRadio.grid(row = 2, column = 0, columnspan='4')

    # Create Radio Buttons for Incontinent Supplies
    includeIncontinentSupplies = tk.StringVar(frame)
    IncontinentSuppliesRadio = tk.Checkbutton(frame, variable=includeIncontinentSupplies, text="Include Incontinent Supplies in the Invoice", font=('14'), background='lightgrey')
    IncontinentSuppliesRadio.deselect()
    IncontinentSuppliesRadio.grid(row = 3, column = 0, columnspan='4')
    
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