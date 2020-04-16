import os
from datetime import date

# Possible change: change the directory import either by doing a test of is DATASET_DIR exist and giving the path from
#  the start or doing ciri.py and execute with python -m ciri.py *****

WHO_DIR = "./dataset"
PDF_DIR = os.path.join(WHO_DIR, "pdf_reports")
CSV_DIR = os.path.join(WHO_DIR, "csv_reports")

DATASET_DIR = "./data_repo_JH"


def initialise_directory():
    global WHO_DIR
    global PDF_DIR
    global CSV_DIR

    if not os.path.isdir(WHO_DIR):
        WHO_DIR = "./dataset"
        print(
            f"Reports will be written to {WHO_DIR + os.sep}"
        )

    PDF_DIR = os.path.join(WHO_DIR, "pdf_reports")
    CSV_DIR = os.path.join(WHO_DIR, "csv_reports")

    for folder in [PDF_DIR, CSV_DIR]:
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)


url_who = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"

url_us_data = "https://github.com/nytimes/covid-19-data"

url_jh_cases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                  "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv "

url_jh_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                  "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv "


WARNING_CHECK_MESSAGE = """
Everything seems to be good!
Though, this only check if there are the same number of report then days since 21 Jan 2020.
There might be duplicates and this message would still be raised, but it's unlikely.
"""

WARNING_DUPLICATE_REPORT = """
Uh-oh, there is something wrong, there are more file than it suppose to.
Check duplicate function has not ye been introduce, sorry, you'll have to do it by hand :(
"""

# Not taking the first letter since it could not have been converted properly
TABLE_START_WORD = ["rovince", "erritory", "egion", "rea"]

BEGIN_DATE = date(2020, 1, 21)

PROVINCE_REGION = [
    "Australian Capital Territory",
    "New South Wales",
    "Northern Territory",
    "Queensland",
    "South Australia",
    "Tasmania",
    "Victoria",
    "Western Australia",
    "Alberta",
    "British Columbia",
    "Grand Princess",
    "Manitoba",
    "New Brunswick",
    "Newfoundland and Labrador",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Quebec",
    "Saskatchewan",
    "Anhui",
    "Beijing",
    "Chongqing",
    "Fujian",
    "Gansu",
    "Guangdong",
    "Guangxi",
    "Guizhou",
    "Hainan",
    "Hebei",
    "Heilongjiang",
    "Henan",
    "Hong Kong",
    "Hubei",
    "Hunan",
    "Inner Mongolia",
    "Jiangsu",
    "Jiangxi",
    "Jilin",
    "Liaoning",
    "Macau",
    "Ningxia",
    "Qinghai",
    "Shaanxi",
    "Shandong",
    "Shanghai",
    "Shanxi",
    "Sichuan",
    "Tianjin",
    "Tibet",
    "Xinjiang",
    "Yunnan",
    "Zhejiang",
    "Faroe Islands",
    "Greenland",
    "French Guiana",
    "French Polynesia",
    "Guadeloupe",
    "Mayotte",
    "New Caledonia",
    "Reunion",
    "Saint Barthelemy",
    "St Martin",
    "Martinique",
    "Aruba",
    "Curacao",
    "Sint Maarten",
    "Bermuda",
    "Cayman Islands",
    "Channel Islands",
    "Gibraltar",
    "Isle of Man",
    "Montserrat",
    "Diamond Princess",
    "Recovered",
    "Northwest Territories",
    "Yukon",
    "Anguilla",
    "British Virgin Islands",
    "Turks and Caicos Islands",
    "Bonaire, Sint Eustatius and Saba",
    "Falkland Islands (Malvinas)",
    "Saint Pierre and Miquelon",
]
