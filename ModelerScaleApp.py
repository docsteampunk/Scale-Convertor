import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import csv

SCALE_FILE = 'scales.csv'

fieldNames = ['scale', 'isFavorite', 'isAuto', 'position']
autoStartValues = ['','']
data = []
dataValues = []

class popupScale():
    def __init__(self, owner) -> None:
        self.owner = owner
        self.popup = Toplevel(root)
        self.popup.geometry("200x150")
        self.popup.title("Add Scale")

        self.label = Label(self.popup, text="Scale 1:")
        self.entry = Entry(self.popup)
        self.buttonScale = Button(self.popup, text='Add Scale', command=lambda : addScale(self.entry, self.popup))

        self.popup.columnconfigure(0, weight = 1)
        self.popup.columnconfigure(1, weight = 1)
        self.popup.rowconfigure(0, weight=3)
        self.popup.rowconfigure(1, weight=1)

        self.label.grid(row=0, column=0, sticky='e')
        self.entry.grid(row=0, column=1, sticky='w')
        self.buttonScale.grid(row=1, column=0, columnspan=2)

def addScale(entryBox, previousBox):
    textValue = entryBox.get()

    if (textValue == ''):
        showErrorBox('Please enter a number.', previousBox)
        entryBox.set('')
        return
    else:
        isValid = True

        try:
            float(textValue)
        except(ValueError):
            isValid = False

        if (isValid == False):
            showErrorBox('Please enter a number.', previousBox)
            entryBox.set('')
        else:
            numberValue = float(textValue)

            if (numberValue <= 0):
                showErrorBox('Please enter a number greater than 0.', previousBox)
                entryBox.set('')
            else:
                scaleValue = '1:' + textValue

                if (scaleValue in data):
                    showErrorBox('Scale already entered, please enter a different scale.', previousBox)
                else:
                    newValue = {"scale": str(scaleValue), "isFavorite":'false', "isAuto":'false', "isFirst":'false'}

                    with open(SCALE_FILE, 'a', newline='\n') as csvFile:
                        newWriter = csv.DictWriter(csvFile, fieldnames=fieldNames)
                        newWriter.writerow(newValue)
                        csvFile.close()

                    previousBox.destroy()
                    data.clear()
                    getScaleList()

def bringToFront(previousBox):
    previousBox.attributes('-topmost', True)
    previousBox.attributes('-topmost', False)

def showMsgBox(messageData, previousBox):
    response = messagebox.showinfo(message=messageData)
    if (response):
        bringToFront(previousBox)

def showErrorBox(messageData, previousBox):
    response = messagebox.showerror(message=messageData)
    if (response):
        bringToFront(previousBox)

def saveAsAutostart():
    scaleUnit_B = comboBox_B.get()
    scaleUnit_T = comboBox_T.get()
    
    resetAll()

    if (scaleUnit_B == scaleUnit_T):
        updateRow(scaleUnit_B, 3)
    else:
        updateRow(scaleUnit_B, 1)
        updateRow(scaleUnit_T, 2)


def resetAll():
    with open(SCALE_FILE, 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()

        for item in range(len(dataValues)):
            newItem = {}
            newItem['scale'] = dataValues[item][0]
            newItem['isFavorite'] = dataValues[item][1]
            newItem['isAuto'] = 'false'
            newItem['position'] = 0
            writer.writerow(newItem)
        csvFile.close()

def updateRow(scaleValue, position):
    with open(SCALE_FILE, 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()

        for item in range(len(dataValues)):
            newItem = {}
            newItem['scale'] = dataValues[item][0]
            newItem['isFavorite'] = dataValues[item][1]

            if (dataValues[item][0] == scaleValue):
                print(scaleValue)
                newItem['isAuto'] = 'true'
                newItem['position'] = position
            else:
                newItem['isAuto'] = dataValues[item][2]
                newItem['position'] = dataValues[item][3]
            
            writer.writerow(newItem)
        csvFile.close()

def exitApplication():
    exit(1)

def search(event):
    value = event.widget.get()

    if (value == ''):
        event.widget['values'] = data
    else:
        newData = []

        for item in data:
            if (value.lower() in item.lower()):
                newData.append(item)

        event.widget['values'] = newData

def getScaleList():
    favoritesList = []
    otherList = []

    with open(SCALE_FILE, 'r') as csvFile:
        reader = csv.DictReader(csvFile)

        for scaleData in reader:
            if (scaleData.get('isAuto') == 'true'):
                if (int(scaleData.get('position')) == 1):
                    autoStartValues[0] = scaleData.get('scale')
                elif (int(scaleData.get('position')) == 2):
                    autoStartValues[1] = scaleData.get('scale')
                else:
                    autoStartValues[0] = scaleData.get('scale')
                    autoStartValues[1] = scaleData.get('scale')

            if (scaleData.get('isFavorite') is True):
                favoritesList.append(scaleData.get('scale'))
            else:
                otherList.append(scaleData.get('scale'))

            dataValues.append([scaleData.get('scale'),scaleData.get('isFavorite'),scaleData.get('isAuto'),scaleData.get('position')])
        csvFile.close()

    favoritesList = sorted(favoritesList, key=lambda x: float(x.split(':')[1]))
    otherList = sorted(otherList, key=lambda x: float(x.split(':')[1]))

    data.extend(favoritesList)
    data.extend(otherList)

def doConversion():
    scaleUnit_B = scale_B.get()
    scaleUnit_T = scale_T.get()

    scaleValue_B = valueEntry_B.get()

    scaleInfo_B = comboBox_B.get()
    scaleInfo_T = comboBox_T.get()

    isValid = True

    try:
        float(scaleValue_B)
    except(ValueError):
        isValid = False

    if (isValid != True):
        showErrorBox("Please enter valid scale numbers.", root)
        return

    if ((scaleInfo_B in data) and (scaleInfo_T in data)):
        scaleOperator_B = float(scaleInfo_B.split(':')[1])
        scaleOperator_T = float(scaleInfo_T.split(':')[1])

        scaleConvertor = scaleOperator_B / scaleOperator_T

        if (scaleUnit_B == scaleUnit_T):
            newValue = scaleConvertor * float(scaleValue_B)
            setText(newValue)
        else:
            convertorValue = float(scaleValue_B)

            match(scaleUnit_B):
                case "CM":
                    convertorValue = convertorValue * 10
                case "M":
                    convertorValue = convertorValue * 1000;
                case "KM":
                    convertorValue = convertorValue * 100000;
                case "IN":
                    convertorValue = convertorValue * 25.4;
                case "FT":
                    convertorValue = convertorValue * 304.8;
                case "MI":
                    convertorValue = convertorValue * 1609344;
    
            convertorValue = scaleConvertor * convertorValue

            match(scaleUnit_T):
                case "CM":
                    convertorValue = convertorValue / 10
                case "M":
                    convertorValue = convertorValue / 1000;
                case "KM":
                    convertorValue = convertorValue / 100000;
                case "IN":
                    convertorValue = convertorValue / 25.4;
                case "FT":
                    convertorValue = convertorValue / 304.8;
                case "MI":
                    convertorValue = convertorValue / 1609344;
    
            setText(convertorValue)



                    
    else:
        showErrorBox("Please set a valid scale.", root)
        return

def setText(text):
    valueEntry_T.config(state=NORMAL)
    valueEntry_T.delete(0, END)
    valueEntry_T.insert(0, text)
    valueEntry_T.config(state='readonly')

def doReversion():
    scaleInfo_B = comboBox_B.get()
    scaleInfo_T = comboBox_T.get()

    if ((scaleInfo_B in data) and (scaleInfo_T in data)):
        comboBox_B.set(scaleInfo_T)
        comboBox_T.set(scaleInfo_B)
    else:
        showErrorBox("Unable to swap scales. Please make sure scales are valid.", root)

def doPopupScale():
    popupScale(root)

class MenuBar():
    def __init__(self, owner):
        self.owner = owner

        self.menu = Menu(self.owner)
        self.owner.config(menu = self.menu)

        self.submenu = Menu(self.menu, tearoff="off")
        self.menu.add_cascade(label="Settings", menu=self.submenu)
        self.submenu.add_command(label="Add Scale",command=doPopupScale, accelerator="Ctrl+A")
        self.submenu.add_command(label="Set As Autostart", command=saveAsAutostart, accelerator="Ctrl+S")
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit", command=exitApplication)


getScaleList()

root = tk.Tk()

root.geometry("500x250")
root.title("Scale Convertor")

scale_B = StringVar()
scale_B.set('')
scale_T = StringVar()
scale_T.set('')

root.bind("<Control-A>", popupScale)
root.bind("<Control-S>", saveAsAutostart)

comboBox_B = ttk.Combobox(root, values=data)
comboBox_T = ttk.Combobox(root, values=data)

menu = MenuBar(root)

if (autoStartValues[0] != ''):
    comboBox_B.set(autoStartValues[0])
else:
    comboBox_B.set('Search')

if (autoStartValues[1] != ''):
    comboBox_T.set(autoStartValues[1])
else:
    comboBox_T.set('Search')

comboBox_B.bind('<KeyRelease>', search)
comboBox_T.bind('<KeyRelease>', search)

convertScale = Button(root, text='Convert Scale', command=doConversion)
reverseScale = Button(root, text='Reverse', command=doReversion)

text_B = Label(root, text="Convert From:")
text_T = Label(root, text="Convert To:")

scaleOptions = ["MM", "CM", "M", "KM", "IN", "FT", "MI"]

scale_B.set(scaleOptions[0])
scale_T.set(scaleOptions[0])

valueEntry_B = Entry(root)
valueEntry_T = Entry(root, state='readonly')

selectScale_B = OptionMenu(root, scale_B, *scaleOptions)
selectScale_T = OptionMenu(root, scale_T, *scaleOptions)

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 1)
root.columnconfigure(3, weight = 1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=4)
root.rowconfigure(2, weight=2)

text_B.grid(row= 0, column=0, columnspan=2)
text_T.grid(row= 0, column=2, columnspan=2)

comboBox_B.grid(row= 1, column=0, columnspan=2, sticky='n')
comboBox_T.grid(row= 1, column=2, columnspan=2, sticky='n')

valueEntry_B.grid(row= 1, column=0, columnspan=2)
valueEntry_T.grid(row= 1, column=2, columnspan=2)

selectScale_B.grid(row= 1, column=0, columnspan=2, sticky='s')
selectScale_T.grid(row= 1, column=2, columnspan=2, sticky='s')

convertScale.grid(row=2, column=0, columnspan=2, sticky='n')
reverseScale.grid(row=2, column=2, columnspan=2, sticky='n')

root.mainloop()
