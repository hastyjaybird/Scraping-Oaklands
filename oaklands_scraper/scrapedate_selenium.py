
# Alameda County property assessors office scrape dates of tax payments for the last 5 years. 
# website: http://www.acgov.org/MS/prop/index.aspx

import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException

apn_file = 'property_list.csv'
output_file = 'output.csv'


def apn_list(apn_file):
	prop_list = pd.read_csv(apn_file, header=0)
	return prop_list

def grabdates(apn_file):
	# Selenium acts like a browser (in this case, firefox) as a mask to get around websites that may have security against bots. While it may not be as fast as Beautiful Soup, its at least better supported and fairly robust. (Really I just wanted to learn how to use Selenium) 

	# dont pop up the browser window
	options = Options()
	options.add_argument('--headless')

	# set up headers for output file.
	output_list = [('APN', ' yr0.0', ' yr0.5', ' yr1.0', ' yr1.5', ' yr2.0', ' yr2.5', ' yr3.0', ' yr3.5', ' yr4.0', ' yr4.5', ' yr5.0', ' yr5.5')]

	for apn in apn_list(apn_file)['apn_number']:
		# create an empty list
		date_list = []
		
		date_list.append(apn)
		
		website = "https://www.acgov.org/ptax_pub_app/RealSearch.do?displayApn={}&situsStreetNumber=&situsStreetName=&situsStreetSuffix=+&situsUnitNumber=&situsCity=+&showHistory=Y&searchBills=Search".format(apn)
		# website = "http://www.tylerboots.com"
		driver = webdriver.Firefox(options=options)
		
		print "grabbing website"
		try:
			driver.get(website)
		except WebDriverException:
			print "NOPE!"
			export_to_csv(output_list)
			raise 

		print "grabbed website"

		# needs a time out when connection isnt made. 
		#d

		# xpath is a pretty brute force hack, tried to use find_element table[@id:x] but it kept returning " ". ideally re-write to make it more stable. 

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
			try:
				# locate payment date
				date = driver.find_element_by_xpath(payment).text
			except NoSuchElementException:
				export_to_csv(output_list)
				raise

			# edit string
			date = date.replace(',', '')
			date = date.replace('Paid','')
			date = date.replace('     ','')

			#add dates to a list 
			date_list.append(date)

		driver.close()
	
		print date_list

		output_list.append(date_list)
		export_to_csv(output_list)

def export_to_csv(output_list):
	# generate dataframe and then export to csv
	output_df = pd.DataFrame(output_list)
	output_df.to_csv(output_file, index=False, header=False)
	# print output_df

		
grabdates(apn_file)