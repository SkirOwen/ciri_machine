import os
from datetime import date

import requests
from bs4 import BeautifulSoup as BS

DATASET_DIR = ""
url_who = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
WARNING_CHECK_MESSAGE ="""
Everything seems to be good.
Though, this only check if there are the same number of report then days since 21 Jan 2020.
There might be duplicate, but it's unlikely.
"""


def initialise_directory():
	global DATASET_DIR
	
	if not os.path.isdir(DATASET_DIR):
		DATASET_DIR = "./dataset"
	
	DATASET_DIR = os.path.normcase("./dataset")
	if DATASET_DIR != "" and not os.path.exists(DATASET_DIR):
		os.makedirs(DATASET_DIR)


def get_link_sr(url=url_who):
	r = requests.get(url, allow_redirects=True)
	
	soup = BS(r.text, features="lxml")
	
	situation_reports_links = []
	available_sr_name = []
	
	for link in soup.find_all("a"):
		try:
			if link.get("href")[1] == "d":
				situation_reports_links.append(link.get("href"))
		except IndexError:
			continue
	
	situation_reports_links = list(dict.fromkeys(situation_reports_links))
	
	for sr in situation_reports_links:
		sr_name = sr.split("/")[-1].split("?")[0]
		available_sr_name.append(sr_name)
	
	return situation_reports_links, available_sr_name


def download_report():
	k = 0
	situation_reports_links, available_sr_name = get_link_sr()
	
	for dl_link, name, i in zip(situation_reports_links, available_sr_name, range(len(available_sr_name), 0, -1)):
		FILE_DIR = os.path.join(DATASET_DIR, name)
		if not os.path.exists(FILE_DIR):
			url_dl = "https://who.int" + dl_link
			report = requests.get(url_dl)
			
			with open(FILE_DIR, "wb") as f:
				f.write(report.content)
			
			print("Situation report - ", i, ":  downloaded as ", name)
			k += 1
	
	print("%d situation reports downloaded" % k)


def check_new_report(download=False):
	begin = date(2020, 1, 21)
	today = date.today()
	days_since_begin = abs(today - begin).days
	
	number_sr_downloaded = len(os.listdir(DATASET_DIR))
	
	if number_sr_downloaded <= days_since_begin:
		print("There might be a new situation report.")
		if download:
			download_report()
		return True
	else:
		print(WARNING_CHECK_MESSAGE)
