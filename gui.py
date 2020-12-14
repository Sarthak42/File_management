import tkinter
import pandas as pd
from tkinter import scrolledtext
from tkinter import *


file_name = "data.csv"
pd.set_option('max_columns', None)
add_win = None
add_win_childs=[None] * 6
remove_win=None
remove_win_childs=[None] * 1

def remove_file(unique_id):
	global file_name
	datas = pd.read_csv(file_name,index_col ="Unique_ID")
	print(datas)
	datas.drop([unique_id], inplace = True)
	datas.to_csv(file_name,header=True)

def add_new_file(unique_id,rank_and_name,date_of_birth,recieved_from_where,reason,remarks):
	df2 = pd.DataFrame({"Unique_ID":unique_id,
						"Rank_and_name":rank_and_name,
						"Date_of_birth":date_of_birth,
						"Status":"IN",
						"Date_of_file_out":None,
						"Date_of_file_in":None,
						"To_whom":None,
						"Reason_for_going":None,
						"Recieved_from_where":recieved_from_where,
						"Reason":reason,
						"Remarks":remarks},index=[0]) 
	df2.to_csv(file_name, mode='a', header=False,index=False)

def add():
	global add_win,add_win_childs
	add_win=tkinter.Tk()
	add_win.resizable(False, False)
	names = ['Unique_ID','Rank_and_name','Date_of_birth','Recieved_from_where','Reason','Remarks']
	r = 0
	for c in names:
	    tkinter.Label(add_win,font=('',20,''),text=c, width=15).grid(row=r,column=0)
	    add_win_childs[r] = tkinter.Entry(add_win,font=('',20,''),width=15)
	    add_win_childs[r].grid(row=r,column=1)
	    r = r + 1
	tkinter.Button(add_win,font=('',20,'bold'), text ="ADD", command = add_close).grid(row=r,column=0,columnspan=2)
	add_win.mainloop()

def add_close():
	global add_win,add_win_childs
	add_new_file(add_win_childs[0].get(),add_win_childs[1].get(),add_win_childs[2].get(),add_win_childs[3].get(),add_win_childs[4].get(),add_win_childs[5].get())
	add_win.destroy()
	root.mainloop()

def remove():
	global remove_win,remove_win_childs
	remove_win=tkinter.Tk()
	remove_win.resizable(False, False)
	tkinter.Label(remove_win,font=('',20,''),text="Unique_ID", width=15).grid(row=0,column=0)
	remove_win_childs[0] = tkinter.Entry(remove_win,font=('',20,''),width=15)
	remove_win_childs[0].grid(row=0,column=1)
	tkinter.Button(remove_win,font=('',20,'bold'), text ="REMOVE", command = remove_close).grid(row=1,column=0,columnspan=2)
	remove_win.mainloop()

def remove_close():
	global remove_win,remove_win_childs
	remove_file(remove_win_childs[0].get())
	remove_win.destroy()
	root.mainloop(0)
	pass

def send():
	print("SEND")

def recieve():
	print("RECEIVE")

def show_in():
	btm_pane     = PanedWindow()
	data = pd.read_csv(file_name)
	data = data.loc[data["Status"] == "IN"]
	table1 = scrolledtext.ScrolledText(btm_pane)
	btm_pane.add(table1)
	table1.insert(tkinter.INSERT,data)
	btm_pane.grid(row=5,column=0,rowspan=5,columnspan=5)

def show_out():
	btm_pane     = PanedWindow()
	data = pd.read_csv(file_name)
	data = data.loc[data["Status"] == "OUT"]
	table1 = scrolledtext.ScrolledText(btm_pane)
	btm_pane.add(table1)
	table1.insert(tkinter.INSERT,data)
	btm_pane.grid(row=5,column=0,rowspan=5,columnspan=5)


root = tkinter.Tk()
root.geometry("900x800+50+50")
root.resizable(False, False)

tkinter.Label(root, text="IN  : 5 ",font=('',20,'')).grid(row=0,column=0)
tkinter.Label(root, text="OUT : 5",font=('',20,'')).grid(row=1,column=0)

tkinter.Label(root, text="Railway Protection Force",font=('',25,'bold')).grid(row=0,column=1)
tkinter.Label(root, text="Western Railway",font=('',25,'bold')).grid(row=1,column=1)
tkinter.Label(root, text="Division Sr.DSC/BCT",font=('',25,'bold')).grid(row=2,column=1)

add_btn      = tkinter.Button(root,font=('',25,'bold'), text ="ADD NEW FILE", command = add).grid(row=3,column=0)
remove_btn   = tkinter.Button(root,font=('',25,'bold'), text ="REMOVE FILE", command = remove).grid(row=3,column=1)
send_btn     = tkinter.Button(root,font=('',25,'bold'), text ="SEND FILE", command = send).grid(row=3,column=2)
receive_btn  = tkinter.Button(root,font=('',25,'bold'), text ="RECEIVE FILE", command = recieve).grid(row=4,column=0)
in_btn    = tkinter.Button(root,font=('',25,'bold'), text ="IN", command = show_in).grid(row=4,column=1)
out_btn   = tkinter.Button(root,font=('',25,'bold'), text ="OUT", command = show_out).grid(row=4,column=2)

root.mainloop()