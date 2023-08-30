import tkinter as tk

def window_widget():
    
    win=tk.Tk()
    win.title("LogHelper Widget")
    win.geometry("600x400")
    win.resizable(False,False)
    win.iconbitmap('icon.ico')

    projectName = tk.Entry().pack(side="left",fill="x")
    projectLabel = tk.Label(win,text="Enter Project Name").pack(side="left",fill="x")
    phase = tk.Entry().pack()
    phaseLabel = tk.Label(win,text="Enter Project Name").pack()
    submitbutton = tk.Button(win,text="Submit",command=run).pack()
    
    win.mainloop()
    
def run():
    #邏輯寫上面


    print("go")

window_widget()