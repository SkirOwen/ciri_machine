import os
import requests
from bs4 import BeautifulSoup as BS

DATASET_DIR = os.path.normcase("./dataset")
if DATASET_DIR != "" and not os.path.exists(DATASET_DIR):
	os.makedirs(DATASET_DIR)

url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"

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
	
k = 0

for dl_link, name, i in zip(situation_reports_links, available_sr_name, range(len(available_sr_name), 0, -1)):
	FILE_DIR = os.path.join(DATASET_DIR, name)
	if not os.path.exists(FILE_DIR):
		
		url_dl = "https://who.int" + dl_link
		report = requests.get(url_dl)
		
		with open(FILE_DIR, "wb") as f:
			f.write(report.content)
			
		print("Situation report - ", i, "downloaded as ", name)
		k += 1
		
print("%d situation reports downloaded" % k)

