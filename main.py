import pandas as pd
file_name = "data.csv"
#data = pd.read_csv(file_name)

def remove_file(unique_id):
	global file_name
	datas = pd.read_csv(file_name,index_col ="Unique_ID")
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


def send_file(unique_id):
	global file_name
	data = pd.read_csv(file_name)
	data.loc[data["Unique_ID"] == unique_id,'Status'] = "OUT"
	data.loc[data["Unique_ID"] == unique_id,'Date_of_file_out'] = "edited"
	data.to_csv(file_name,header=True,index=False)

def recieve_file(unique_id):
	global file_name
	data = pd.read_csv(file_name)
	data.loc[data["Unique_ID"] == unique_id,'Status'] = "IN"
	data.loc[data["Unique_ID"] == unique_id,'Date_of_file_in'] = "edited"
	data.to_csv(file_name,header=True,index=False)



#add_new_file(45,"neww","12/32/12","neww","neww","neww")
#remove_file(49)
#send_file(48)
#recieve_file(48)

