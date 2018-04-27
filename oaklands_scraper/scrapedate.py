
# Alameda County property assessors office scrape dates of tax payments for the last 5 years. 
# website: http://www.acgov.org/MS/prop/index.aspx

import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import datetime


prop_list = pd.read_csv('property_list.csv', header=0)
print(prop_list)
output = [('APN', ' yr0.0', ' yr0.5', ' yr1.0', ' yr1.5', ' yr2.0', ' yr2.5', ' yr3.0', ' yr3.5', ' yr4.0', ' yr4.5', ' yr5.0', ' yr5.5')]

# dont pop up the browser window
options = Options()
options.add_argument('--headless')

for apn in prop_list['apn_number']:
	date_list = []
	date_list.append(apn)
	
	website = "https://www.acgov.org/ptax_pub_app/RealSearch.do?displayApn={}&situsStreetNumber=&situsStreetName=&situsStreetSuffix=+&situsUnitNumber=&situsCity=+&showHistory=Y&searchBills=Search".format(apn)
	driver = webdriver.Firefox(options=options)
	driver.get(website)

	# xpath is a pretty brute force hack, tried to use find_element table[@id:x] but it kept returning " ". could try to troubleshoot this more. 
	path_list = [
		# 2017-2018
		"/html/body/div[1]/div[4]/div/form/table[5]/tbody/tr[2]/td/table/tbody/tr[5]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[5]/tbody/tr[2]/td/table/tbody/tr[6]/td[6]",
		# 2016-2017
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[5]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[6]/td[6]",
		# 2015-2016
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[10]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[11]/td[6]",
		# 2014-2015
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[15]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[16]/td[6]",
		# 2013-2014
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[20]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[21]/td[6]",
		# 2012-2013
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[25]/td[6]",
		"/html/body/div[1]/div[4]/div/form/table[6]/tbody/tr[2]/td/table/tbody/tr[26]/td[6]"
		]

	for payment in path_list:
		# locate payment date
		date = driver.find_element_by_xpath(payment).text

		# edit string
		date = date.replace(',', '')
		date = date.replace('Paid','')
		date = date.replace('     ','')

		date_list.append(date)

	driver.close()

	print date_list
	output.append(date_list)


# generate dataframe and then export to csv
output = pd.DataFrame(output)
output.to_csv('output.csv', index=False, header=False)
print output

