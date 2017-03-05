
import pandas as pd
import numpy as np
import json
import glob
import os

print "Getting data"

first_name = glob.glob(os.path.join('social-security-first-names/', '*.txt'))
for file in first_name:
	year = int(file[-8:-4])
	if year == 1917:
		data = pd.read_csv(file, header=None, names=["name", "gender", "num"])
		data["year"] = year
	if year >= 1918:
		dat = pd.read_csv(file, header=None, names=["name", "gender", "num"])
		dat["year"] = year
		data = data.append(dat, ignore_index = True)

data["age"] = np.subtract(2017,data["year"])
data["Age_Range"] = ""
ranges = [(x-1, x+4) for x in range(1,100,5)]
for rang in ranges:
	data["Age_Range"][np.multiply(data["age"] > rang[0], data["age"] <= rang[1])] = str(rang[0]) + " to " + str(rang[1])
data["first_name"] = [x.lower() for x in data["name"]]

print "Gender frequency"
gender_total = data.groupby(["first_name","gender"], as_index = False).agg({'num':'sum'})
a_pct = gender_total[["first_name","num"]].groupby("first_name", as_index = False).agg({'num':'sum'}).rename(columns={"num":"total"})
gender_total = gender_total.merge(a_pct, on = "first_name", how = "left")
gender_total["name_pct"] = np.divide(gender_total["num"].astype(float), gender_total["total"])
gender_total = gender_total.pivot(index="first_name", columns="gender", values="name_pct")
gender_total = gender_total.fillna(0).reset_index()

print "Gender by Age frequency"
ga_total = data.groupby(["first_name","gender","Age_Range"], as_index = False).agg({'num':'sum'})
a2_pct = ga_total[["first_name","gender","num"]].groupby(["first_name","gender"], as_index = False).agg({'num':'sum'}).rename(columns={"num":"total"})
ga_total = ga_total.merge(a2_pct, on = ["first_name","gender"], how = "left")
ga_total["name_pct"] = np.divide(ga_total["num"].astype(float), ga_total["total"])
ga_total["Age_Range_Gender"] = [x + "_" + y for x,y in zip(ga_total["gender"], ga_total["Age_Range"])]
ga_total = ga_total.drop(["Age_Range","gender"], 1)
ga_total = ga_total.pivot(index="first_name", columns="Age_Range_Gender", values="name_pct")
ga_total = ga_total.fillna(0).reset_index()
all_pct = gender_total.merge(ga_total, on = "first_name", how = "left")
all_pct.to_csv('first_name_pct.csv', index = False)

print "Getting data"

data = pd.read_csv('census-2010-surnames/Names_2010Census.csv')
data["last_name"] = [x.lower() if type(x) is not float else "" for x in data["name"]]
data = data[data["last_name"] != ""]
data = data[["last_name", "pctwhite", "pctblack", "pctapi", "pctaian", "pct2prace", "pcthispanic"]]
data_list = data.values.tolist()
rows = []
for i in range(len(data_list)):
	count_s = 0
	nums = []
	count_a = 0
	for j in range(1,len(data_list[i])):
		if data_list[i][j] == '(S)': 
			count_s += 1
			nums.append(j)
		else: 
			data_list[i][j] = float(data_list[i][j])
			count_a += data_list[i][j]
	if count_s > 0:
		tofill = (100 - count_a) / count_s
		for j in nums:
			data_list[i][j] = tofill
data = pd.DataFrame(data_list, columns=["last_name", "pctwhite", "pctblack", "pctapi", "pctaian", "pct2prace", "pcthispanic"])
data.to_csv('last_name_pct.csv', index = False)