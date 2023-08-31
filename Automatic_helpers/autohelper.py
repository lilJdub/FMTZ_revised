import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

win=tk.Tk()
win.title("LogHelper Widget")
win.geometry("600x400")
win.resizable(False,False)
win.iconbitmap('icon.ico')



projectLabel = tk.Label(win,text="Enter Project Name")
projectLabel.pack(side="top",anchor="center",pady=20)

projectName = tk.Entry()
projectName.pack(side="top",anchor="center",pady=20)

phaseLabel = tk.Label(win,text="Enter Phase Name")
phaseLabel.pack(side="top",anchor="center",pady=20)

phase=ttk.Combobox(win,values=["DB","SI","PV","MV"],state="readonly")
phase.pack(side="top",anchor="center",pady=20)

def run():
    pn=projectName.get()
    ph=phase.get()
    if pn and ph != "":
        return 0
    else:
        mb.showerror(title="redo input",message="There's been an misinput. Try again")
        
submitbutton = tk.Button(win,text="Submit",command=run)
submitbutton.pack(side="top",anchor="center",pady=20)


win.mainloop()
