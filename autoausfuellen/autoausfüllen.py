import cv2
import matplotlib as mp
import tkinter as tk
import os
import pywinauto
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

a = 4
print(f'\n{a}\nHello World')

#Loop
for i in range(4):
    print(i+1)

# Inside window function
def window(root):
    label = tk.Label(root, text="Straße")
    label.pack()
    entry = tk.Entry(root)
    entry.pack()

    label = tk.Label(root, text="Hausnummer")
    label.pack()
    entry2 = tk.Entry(root)
    entry2.pack()

    label = tk.Label(root, text="PLZ")
    label.pack()
    entry3 = tk.Entry(root)
    entry3.pack()

    label = tk.Label(root, text="Ort")
    label.pack()
    entry4 = tk.Entry(root)
    entry4.pack()

    label = tk.Label(root, text="Ortsteil 1")
    label.pack()
    entry5 = tk.Entry(root)
    entry5.pack()

    label = tk.Label(root, text="Ortsteil 2")
    label.pack()
    entry6 = tk.Entry(root)
    entry6.pack()

    label = tk.Label(root, text="Wohneinheiten")
    label.pack()
    entry7 = tk.Entry(root)
    entry7.pack()

    # Parameters
    entry.insert(0, "Juliusstraße")
    entry2.insert(0, 0)
    entry3.insert(0, 65428)
    entry4.insert(0, "Rüsselsheim am Main")
    entry5.insert(0, "Eselswiese")
    entry6.insert(0, "Eselswiese")
    entry7.insert(0, 1)
    fetch = [entry.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get()]

    def refresh():
        # Delete fetch list
        fetch.clear()
        fetch1 = entry.get()
        fetch2 = entry2.get()
        fetch3 = entry3.get()
        fetch4 = entry4.get()
        fetch5 = entry5.get()
        fetch6 = entry6.get()
        fetch7 = entry7.get()
        #insert into fetch list 
        fetch.append(fetch1)
        fetch.append(fetch2)
        fetch.append(fetch3)
        fetch.append(fetch4)
        fetch.append(fetch5)
        fetch.append(fetch6)
        fetch.append(fetch7)


    def next():
        # Take int from 2nd entry
        number = int(entry2.get())
        # Delete 2nd entry
        entry2.delete(0, tk.END)
        # Fill 2nd entry with text
        entry2.insert(0, number + 2) 
        return root
    

    # insert button
    button = tk.Button(root, text="+2 Haus Nr.", command=lambda: [next(), refresh()])
    button.pack()

    button2 = tk.Button(root, text="Insert", command=lambda: insert(fetch))
    button2.pack()
    #return root 


def insert(fetch):
    print(f'\nFetched data:\n{fetch}\n')
    # Open images
    step1 = cv2.imread('weiter.JPG', cv2.IMREAD_UNCHANGED)
    # Display images
    cv2.imshow('Image', step1)
    
    goto()

    # go to microsoft edge window
    #os.system("start msedge")
    # go to the opened tab
    #os.system("start msedge https://www.google.com")
    
    #entry = tk.Entry(root)
    #entry.pack()
    
    
def goto():
    windows = gw.getWindowsWithTitle('msedge.exe')

    if windows:
        # Focus on the first window with the title
        window = windows[0]
        window.activate()

        # You might need to use pywinauto to interact further
        app = pywinauto.Application().connect(handle=window._hWnd)
        browser = app.window(handle=window._hWnd)
        browser.set_focus()
    else:
        print("No window found with the specified title.")
    



# Tkinter window
root = tk.Tk()
root.title("Hello World")
root.geometry("300x400")
# Keep window above everything
root.attributes("-topmost", True)
window(root)

root.mainloop()

