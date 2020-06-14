import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

df_original = pd.read_excel('Premium_test.xlsx')
df_xlsx = df_original.copy()
col, row = df_xlsx.shape
df_xlsx.insert(2, 'non_empty_count', (df_xlsx.apply(lambda x: x.count(), axis=1)))
df_xlsx.insert(3, 'Total', (df_xlsx.sum(axis=1) - df_xlsx['non_empty_count']))
df_xlsx.insert(4, 'Average', (df_xlsx['Total'] / (df_xlsx['non_empty_count'] - 2)))
#print(df_xlsx)
df_xlsx_t = df_xlsx.T
df_xlsx_t = df_xlsx_t.reset_index()
df_xlsx_t.rename(columns={'index':'Raw_Date'}, inplace = True)
df_xlsx_t.insert(1, 'Date', (df_xlsx_t.Raw_Date.str.split(",",expand=True,)[0]))
df_xlsx_t.insert(2, 'Time', (df_xlsx_t.Raw_Date.str.split(",",expand=True,)[1]))
#print(df_xlsx_t)


tmp_df_1 = df_xlsx_t.iloc[0:5]
tmp_df_1 = tmp_df_1.drop(columns = ['Raw_Date', 'Time'])
#print(tmp_df_1)
tmp_df_1_t = tmp_df_1.set_index('Date').transpose()
#print(tmp_df_1_t)
tmp_df_2 = df_xlsx_t.iloc[5:df_xlsx_t.shape[0]]
tmp_df_2 = tmp_df_2.reset_index(drop=True)
tmp_df_4 = tmp_df_2.copy()
tmp_df_4 = tmp_df_4.drop(columns = ['Raw_Date', 'Time'])
#print(tmp_df_4)
tmp_df_3 = pd.DataFrame((list(dict.fromkeys(tmp_df_2['Date']))), columns = ['Date'])
tmp_df_2 = tmp_df_2.groupby(tmp_df_2.index // 4).sum()
tmp_df_2 = tmp_df_2.drop(columns = ['Raw_Date', 'Date', 'Time'])
tmp_df_2 = tmp_df_2.div(4)
tmp_df_2 = pd.concat([tmp_df_3,tmp_df_2], axis = 1)
#print(tmp_df_2)
tmp_df_com_avg = tmp_df_1.iloc[4:]
tmp_df_com_avg = tmp_df_com_avg.reset_index(drop=True)
tmp_df_com_avg = tmp_df_com_avg.append([tmp_df_com_avg]*(tmp_df_2.shape[0] - 1),ignore_index=True)
#print(tmp_df_com_avg)
tmp_df_2_t = tmp_df_2.set_index('Date').transpose()
#print(tmp_df_2_t)
#-----------------------------------------------------------------------------------------------------------------
def one_stn_all_day_avg(stn_no):
	#one station, all day average
	#station starts from 1
	y1 = tmp_df_2.iloc[:, stn_no]
	#print(y)
	stn_det = tmp_df_1.iloc[0,(stn_no)] + ': ' + tmp_df_1.iloc[1,(stn_no)]
	x1 = tmp_df_2.iloc[:, 0]
	z1 = tmp_df_com_avg.iloc[:, stn_no]
	title_1 = tmp_df_1.iloc[1,(stn_no)]
	store_1 = str(stn_no-1) + '/'
	#print(x)
	#print(z)
	plt.plot(x1,y1, marker='o')
	plt.plot(z1, 'r--', label='Average Price')
	plt.legend()
	plt.title('Price for the station ' + stn_det)
	plt.xlabel('Dates')
	plt.xticks(x1, rotation=70)
	plt.ylabel('Price in cents')
	plt.gcf().subplots_adjust(bottom=.15)
	script_dir_1 = os.path.dirname(__file__)
	results_dir_1 = os.path.join(script_dir_1, store_1)
	name_1 = 'premium4'
	plt.savefig(results_dir_1 + name_1)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def all_stn_one_day_avg():
	#all station one day
	x2 = df_xlsx['Address']
	#print(x)
	y2 = df_xlsx.iloc[:,-1]
	#print(y)
	z2 = df_xlsx['Average']
	#print (z)
	title_2 = df_xlsx.columns[-1]
	#store_2 = title_2 +'/'
	#print(title)
	plt.plot(x2,y2, marker='o')
	plt.plot(z2, 'r--', marker='o', label='Average')
	plt.legend()
	plt.title('Premium Prices for all the stations for ' + title_2)
	plt.xlabel('Address')
	plt.ylabel('Price in cents')
	plt.xticks(x2, rotation=90)
	plt.gcf().subplots_adjust(bottom=.45)
	#script_dir_2 = os.path.dirname(__file__)
	#results_dir_2 = os.path.join(script_dir_2, store_2)
	name_2 = 'premium2'
	plt.savefig(name_2)

#-----------------------------------------------------------------------------------------------------------------
def one_stn_n_day_split(stn_no, no_of_days):
	#station starts from 1
	tmp_df = df_xlsx[df_xlsx.columns[-(no_of_days*4):]]
	#print(tmp_df)
	x3 = tmp_df.iloc[(stn_no-1)]
	x3 = x3.reset_index() 
	x3.columns = ['Date', 'Average']
	#print(x)
	y3 = x3.copy()
	y3.loc[y3['Average'] > 0, 'Average'] = df_xlsx['Average'][(stn_no-1)]
	#print(y)
	#####average
	title_3 = df_xlsx['Address'][(stn_no-1)]
	store_3 = str(stn_no-1) +'/'
	#print(title)
	plt.plot(x3['Date'],x3['Average'], marker = 'o')
	plt.plot(y3['Date'],y3['Average'], 'r--', label='Average')
	plt.legend()
	plt.xlabel('Date and Time')
	plt.ylabel('Price in cents')
	plt.xticks(x3['Date'], rotation=40)
	plt.title('Prices for station '+title_3+ ' for last ' +str(no_of_days)+ ' days')
	plt.gcf().subplots_adjust(bottom=.2)
	script_dir_3 = os.path.dirname(__file__)
	results_dir_3 = os.path.join(script_dir_3, store_3)
	name_3 = 'premium3'
	plt.savefig(results_dir_3 + name_3)

#----------------------------------------------------------------------------------------------------------------------
def one_stn_last_day_split(stn_no):
	#station starts from 1
	tmp_df_last = df_xlsx[df_xlsx.columns[-4:]]
	#print(tmp_df)
	x4 = tmp_df_last.iloc[(stn_no-1)]
	x4 = x4.reset_index()
	x4.columns = ['Date', 'Average']
	#print(x)
	y4 = x4.copy()
	y4.loc[y4['Average'] > 0, 'Average'] = df_xlsx['Average'][(stn_no-1)]
	#print(y)
	#####average
	title_4 = df_xlsx['Address'][(stn_no-1)]
	store_4 = str(stn_no-1) + '/'
	#print(title)
	plt.plot(x4['Date'],x4['Average'], marker = 'o')
	plt.plot(y4['Date'],y4['Average'], 'r--', label='Average')
	plt.legend()
	plt.xlabel('Date and Time')
	plt.ylabel('Price in cents')
	plt.title('Prices for station '+ title_4)
	script_dir_4 = os.path.dirname(__file__)
	results_dir_4 = os.path.join(script_dir_4, store_4)
	name_4 = 'premium1'
	plt.savefig(results_dir_4 + name_4)


#------------------------------------------------------------------------------------------------------------------------------------------------
def one_company_average(company):
	new_df = df_xlsx.loc[(df_xlsx['Station'] == company)]
	if (len(new_df) > 1):
	#from this data, display address vs average
		plt.plot(new_df['Address'], new_df['Average'], marker = 'o')
		plt.xlabel('Address')
		plt.xticks(new_df['Address'], rotation=60)
		plt.ylabel('Price in cents')
		plt.title(company +' all stations average comparision')
		plt.gcf().subplots_adjust(bottom=.4)
		#script_dir_5 = os.path.dirname(__file__)
		#results_dir_5 = os.path.join(script_dir_5, 'one_company_average/')
		plt.savefig('Premium ' + company)




cunt = ['Petro Canada', '7-Eleven', 'Esso', "Mac's", 'Super Store', 'Shell', 'XTR', 'Pioneer', 'Canadian Tyre', 'Costco']

#one_stn_last_day_split(28)

#one_stn_n_day_split(28,3)
#one_stn_all_day_avg(28)

#one_company_average('Petro Canada')

#all_stn_one_day_avg()
