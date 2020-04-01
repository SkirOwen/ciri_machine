import os
import requests
from bs4 import BeautifulSoup as BS
import wget

# DATASET_DIR = os.dir

url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
r = requests.get(url, allow_redirects=True)

soup = BS(r.text)

situation_reports_links = []
available_sr_name = []

for link in soup.find_all("a"):
	try:
		if link.get("href")[1] == "d":
			situation_reports_links.append(link.get("href"))
	except IndexError:
		continue

for sr in situation_reports_links:
	available_sr_name.append(sr[52:83])



