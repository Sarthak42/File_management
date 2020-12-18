import tkinter
import pandas as pd
from tkinter import scrolledtext
from tkinter import *
from datetime  import datetime

file_name = "data.csv"
pd.set_option('max_columns', None)
pd.set_option('max_rows', None)
message_win=None
add_win = None
add_win_childs=[None] * 6
remove_win=None
remove_win_childs=[None] * 1
send_win=None
send_win_childs=[None] * 3
receive_win=None
receive_win_childs=[None] * 1
search_win=None
search_win_childs=[None] * 11

def refresh_no():
	global file_name
	data = pd.read_csv(file_name)
	no_of_files_in.set("IN : "+str(len(data.loc[data["Status"]=="IN"])))
	no_of_files_out.set("OUT : "+str(len(data.loc[data["Status"]=="OUT"])))

def send_file(unique_id,reason_for_going,to_whom):
	global file_name
	data = pd.read_csv(file_name)
	if(len(data.loc[data["Unique_ID"] == unique_id])==1):
		if(data.loc[data["Unique_ID"] == unique_id,['Status']].values[0][0]=="IN"):
			data.loc[data["Unique_ID"] == unique_id,'Status'] = "OUT"
			data.loc[data["Unique_ID"] == unique_id,'Reason_for_going'] = reason_for_going
			data.loc[data["Unique_ID"] == unique_id,'To_whom'] = to_whom
			now = datetime.now().strftime(r"%d/%m/%Y")
			data.loc[data["Unique_ID"] == unique_id,'Date_of_file_out'] = now
			data.to_csv(file_name,header=True,index=False)
		else:
			message("FILE ALREADY OUT")
	elif len(data.loc[data["Unique_ID"]==unique_id]) > 1:
		message("MORE THAN 1 ENTRYIES FOUND")
	else:
		message("NO FILE FOUND WITH Unique_ID: "+unique_id)

def recieve_file(unique_id):
	global file_name
	data = pd.read_csv(file_name)
	if(len(data.loc[data["Unique_ID"] == unique_id])==1):
		if(data.loc[data["Unique_ID"] == unique_id,['Status']].values[0][0]=="OUT"):
			data.loc[data["Unique_ID"] == unique_id,'Status'] = "IN"
			now = datetime.now().strftime(r"%d/%m/%Y")
			data.loc[data["Unique_ID"] == unique_id,'Date_of_file_in'] = now
			data.to_csv(file_name,header=True,index=False)
		else:
			message("FILE ALREADY IN")
	elif len(data.loc[data["Unique_ID"]==unique_id]) > 1:
		message("MORE THAN 1 ENTRYIES FOUND")
	else:
		message("NO FILE FOUND WITH Unique_ID: "+unique_id)

def remove_file(unique_id):
	global file_name
	data = pd.read_csv(file_name)
	if len(data.loc[data["Unique_ID"]==unique_id]) == 1:
		datas = pd.read_csv(file_name,index_col ="Unique_ID")
		datas.drop([unique_id], inplace = True)
		datas.to_csv(file_name,header=True)
	elif len(data.loc[data["Unique_ID"]==unique_id]) > 1:
		message("MORE THAN 1 ENTRYIES FOUND. DELETE MANUALLY")
	else:
		message("NO FILE FOUND WITH Unique_ID: "+unique_id)


def add_new_file(unique_id,rank_and_name,date_of_birth,recieved_from_where,reason,remarks):
	global file_name
	if(unique_id=="" or rank_and_name=="" or date_of_birth=="" or recieved_from_where==""):
		message("Data Field Empty")
	else:
		data = pd.read_csv(file_name)
		if len(data.loc[data["Unique_ID"]==unique_id]) == 0:
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
		else:
			message("FILE ALREADY EXISTS")

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
	refresh_no()
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
	try:
		remove_file(remove_win_childs[0].get())
	except Exception as e:
		message(e)
	remove_win.destroy()
	refresh_no()
	root.mainloop()

def send():
	global send_win,send_win_childs
	send_win=tkinter.Tk()
	send_win.resizable(False, False)
	tkinter.Label(send_win,font=('',20,''),text="Unique_ID", width=15).grid(row=0,column=0)
	send_win_childs[0] = tkinter.Entry(send_win,font=('',20,''),width=15)
	send_win_childs[0].grid(row=0,column=1)
	tkinter.Label(send_win,font=('',20,''),text="Reason_for_going", width=15).grid(row=1,column=0)
	send_win_childs[1] = tkinter.Entry(send_win,font=('',20,''),width=15)
	send_win_childs[1].grid(row=1,column=1)
	tkinter.Label(send_win,font=('',20,''),text="To_whom", width=15).grid(row=2,column=0)
	send_win_childs[2] = tkinter.Entry(send_win,font=('',20,''),width=15)
	send_win_childs[2].grid(row=2,column=1)
	tkinter.Button(send_win,font=('',20,'bold'), text ="SEND", command = send_close).grid(row=3,column=0,columnspan=2)
	send_win.mainloop()

def send_close():
	global send_win,send_win_childs
	send_file(send_win_childs[0].get(),send_win_childs[1].get(),send_win_childs[2].get())
	send_win.destroy()
	refresh_no()
	root.mainloop()

def recieve():
	global receive_win,receive_win_childs
	receive_win=tkinter.Tk()
	receive_win.resizable(False, False)
	tkinter.Label(receive_win,font=('',20,''),text="Unique_ID", width=15).grid(row=0,column=0)
	receive_win_childs[0] = tkinter.Entry(receive_win,font=('',20,''),width=15)
	receive_win_childs[0].grid(row=0,column=1)
	tkinter.Button(receive_win,font=('',20,'bold'), text ="RECEIVE", command = recieve_close).grid(row=1,column=0,columnspan=2)
	receive_win.mainloop()

def recieve_close():
	global receive_win,receive_win_childs
	recieve_file(receive_win_childs[0].get())
	receive_win.destroy()
	refresh_no()
	root.mainloop()
	

def show_in():
	refresh_no()
	btm_pane     = PanedWindow()
	data = pd.read_csv(file_name)
	data = data.loc[data["Status"] == "IN",['Unique_ID','Rank_and_name','Date_of_birth','Remarks','Recieved_from_where','Reason']]
	table1 = scrolledtext.ScrolledText(btm_pane)
	btm_pane.add(table1)
	table1.insert(tkinter.INSERT,data)
	btm_pane.grid(row=5,column=0,rowspan=5,columnspan=5)

def show_out():
	refresh_no()
	btm_pane     = PanedWindow()
	data = pd.read_csv(file_name)
	data = data.loc[data["Status"] == "OUT",['Unique_ID','Rank_and_name','Date_of_birth','To_whom','Reason_for_going','Remarks']]
	table1 = scrolledtext.ScrolledText(btm_pane)
	btm_pane.add(table1)
	table1.insert(tkinter.INSERT,data)
	btm_pane.grid(row=5,column=0,rowspan=5,columnspan=5)

def message(val):
	global message_win
	message_win = tkinter.Tk()
	tkinter.Label(message_win, text=val,font=('',20,'')).grid(row=0,column=0)
	tkinter.Button(message_win,font=('',25,'bold'), text ="OK", command = message_close).grid(row=1,column=0)
def message_close():
	message_win.destroy()
	root.mainloop()

def search():
	global search_win_childs,search_win,file_name,data_entry
	data = pd.read_csv(file_name)
	if len(data.loc[data["Unique_ID"]==data_entry.get()])==1:
		search_win=tkinter.Tk()
		search_win.resizable(False, False)
		search_win.protocol("WM_DELETE_WINDOW", search_close)
		names = ['Unique_ID','Rank_and_name','Date_of_birth','Recieved_from_where','Reason','Remarks','Status','Date_of_file_in','Date_of_file_out','Reason_for_going','To_whom']
		r = 0
		for c in names:
		    tkinter.Label(search_win,font=('',20,''),text=c, width=15).grid(row=r,column=0)
		    search_win_childs[r] = tkinter.Entry(search_win,font=('',20,''),width=15)
		    search_win_childs[r].grid(row=r,column=1)
		    search_win_childs[r].insert(0,data.loc[data["Unique_ID"]==data_entry.get(),[c]].values[0][0])
		    r = r + 1
		tkinter.Button(search_win,font=('',20,'bold'), text ="EDIT AND SAVE", command = edit).grid(row=r,column=0,columnspan=2)
		search_win.mainloop()
	elif len(data.loc[data["Unique_ID"]==data_entry.get()]) > 1:
		message("MORE THAN 1 ENTRYIES FOUND")
	else:
		message("NO FILE FOUND WITH data: "+data_entry.get())

def edit():
	global file_name,root,search_win_childs,search_win
	data = pd.read_csv(file_name)
	names = ['Unique_ID','Rank_and_name','Date_of_birth','Recieved_from_where','Reason','Remarks','Status','Date_of_file_in','Date_of_file_out','Reason_for_going','To_whom']
	r = 0
	for c in names:
		data.loc[data["Unique_ID"] == data_entry.get(),c] = search_win_childs[r].get()
		r = r+1
	data.to_csv(file_name,header=True,index=False)
	search_win.destroy()
	root.mainloop()

def search_close():
	global root,search_win
	search_win.destroy()
	root.mainloop()

root = tkinter.Tk()
root.geometry("900x800+50+50")
root.resizable(False, False)
no_of_files_in = StringVar()
no_of_files_out = StringVar()
no_of_files_in.set("IN:0")
no_of_files_out.set("OUT:0")
refresh_no()

tkinter.Label(root, textvariable=no_of_files_in,font=('',20,'')).grid(row=0,column=0)
tkinter.Label(root, textvariable=no_of_files_out,font=('',20,'')).grid(row=1,column=0)

search_btn = tkinter.Button(root,font=('',25,'bold'), text ="SEARCH", command = search).grid(row=0,column=2)
data_entry =  tkinter.Entry(root,font=('',20,''),width=10)
data_entry.grid(row=1,column=2)

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