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

url_us_data = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv"

url_us_states = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"

url_jh_cases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
               "/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv "

url_jh_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                "/csse_covid_19_time_series/time_series_covid19_deaths_global.csv "

WARNING_OLD_CSV = """
\33[3m\33[93m The data has been extracted from already existing files, consider regenerating them! \33[0m
"""

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

COUNTRIES = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia',
    'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
    'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria',
    'Burkina Faso', 'Burma', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic',
    'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica',
    "Cote d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Diamond Princess', 'Djibouti', 'Dominica',
    'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini',
    'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada',
    'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India',
    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
    'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Liberia', 'Libya', 'Liechtenstein',
    'Lithuania', 'Luxembourg', 'MS Zaandam', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
    'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
    'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway',
    'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar',
    'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
    'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan',
    'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan*', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
    'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'US', 'Uganda', 'Ukraine', 'United Arab Emirates',
    'United Kingdom', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'West Bank and Gaza', 'Western Sahara', 'Yemen',
    'Zambia', 'Zimbabwe'
]

PROVINCE_REGION = [
    "Australian Capital Territory", "New South Wales", "Northern Territory", "Queensland", "South Australia",
    "Tasmania", "Victoria", "Western Australia", "Alberta", "British Columbia", "Grand Princess", "Manitoba",
    "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Ontario", "Prince Edward Island", "Quebec",
    "Saskatchewan", "Anhui", "Beijing", "Chongqing", "Fujian", "Gansu", "Guangdong", "Guangxi", "Guizhou", "Hainan",
    "Hebei", "Heilongjiang", "Henan", "Hong Kong", "Hubei", "Hunan", "Inner Mongolia", "Jiangsu", "Jiangxi", "Jilin",
    "Liaoning", "Macau", "Ningxia", "Qinghai", "Shaanxi", "Shandong", "Shanghai", "Shanxi", "Sichuan", "Tianjin",
    "Tibet", "Xinjiang", "Yunnan", "Zhejiang", "Faroe Islands", "Greenland", "French Guiana", "French Polynesia",
    "Guadeloupe", "Mayotte", "New Caledonia", "Reunion", "Saint Barthelemy", "St Martin", "Martinique", "Aruba",
    "Curacao", "Sint Maarten", "Bermuda", "Cayman Islands", "Channel Islands", "Gibraltar", "Isle of Man", "Montserrat",
    "Diamond Princess", "Recovered", "Northwest Territories", "Yukon", "Anguilla", "British Virgin Islands",
    "Turks and Caicos Islands", "Bonaire, Sint Eustatius and Saba", "Falkland Islands (Malvinas)",
    "Saint Pierre and Miquelon", ]

STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
    'District of Columbia', 'Florida', 'Georgia', 'Guam', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
    'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
    'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Northern Mariana Islands', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico',
    'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]

LOCKDOWN_DATE = {
    "Albania": "2020-03-13",
    "Algeria": "2020-03-23",
    "Argentina": "2020-03-19",
    "Armenia": "2020-03-24",
    "Australia": "2020-03-23",
    "Austria": "2020-03-16",
    "Azerbaijan": "2020-03-31",
    "Bangladesh": "2020-03-26",
    "Barbados": "2020-03-28",
    "Belgium": "2020-03-18",
    "Bermuda": "2020-04-04",
    "Bolivia": "2020-03-22",
    "Botswana": "2020-04-02",
    "Brazil": "2020-03-24",
    "Colombia": "2020-03-25",
    "Republic of the Congo": "2020-03-31",
    "Costa Rica": "2020-03-23",
    "Croatia": "2020-03-18",
    "Czech Republic": "2020-03-16",
    "Ecuador": "2020-03-16",
    "El Salvador": "2020-03-12",
    "Eritrea": "2020-04-02",
    "Fiji": "2020-03-20",
    "Finland": "2020-03-27",
    "France": "2020-03-17",
    "Georgia": "2020-03-31",
    "Germany": "2020-03-23",
    "Ghana": "2020-03-30",
    "Greece": "2020-03-23",
    "Guernsey": "2020-03-25",
    "Honduras": "2020-03-20",
    "Hungary": "2020-03-28",
    "India": "2020-03-25",
    "Iran": "2020-03-14",
    "Iraq": "2020-03-22",
    "Ireland": "2020-03-12",
    "Israel": "2020-04-02",
    "Italy": "2020-03-09",
    "Jamaica": "2020-04-15",
    "Jordan": "2020-03-18",
    "Kosovo": "2020-03-14",
    "Kuwait": "2020-03-14",
    "Lebanon": "2020-03-15",
    "Liberia": "2020-03-23",
    "Libya": "2020-03-22",
    "Lithuania": "2020-03-16",
    "Madagascar": "2020-03-23",
    "Malaysia": "2020-03-18",
    "Mongolia": "2020-03-10",
    "Montenegro": "2020-03-24",
    "Morocco": "2020-03-19",
    "Namibia": "2020-03-27",
    "Nepal": "2020-03-24",
    "New Zealand": "2020-03-26",
    "Nigeria": "2020-03-30",
    "Northern Cyprus": "2020-03-30",
    "Oman": "2020-04-16",
    "Pakistan": "2020-03-24",
    "Panama": "2020-03-25",
    "Papua New Guinea": "2020-03-24",
    "Paraguay": "2020-03-20",
    "Peru": "2020-03-16",
    "Philippines": "2020-03-27",
    "Poland": "2020-03-13",
    "Portugal": "2020-03-19",
    "Qatar": "2020-03-11",
    "Romania": "2020-03-25",
    "Russia": "2020-03-28",
    "Rwanda": "2020-03-21",
    "Samoa": "2020-03-26",
    "San Marino": "2020-03-14",
    "Saudi Arabia": "2020-03-29",
    "Serbia": "2020-03-15",
    "Singapore": "2020-04-07",
    "South Africa": "2020-03-26",
    "Spain": "2020-03-14",
    "Thailand": "2020-03-25",
    "Trinidad and Tobago": "2020-03-17",
    "Tunisia": "2020-03-22",
    "Turkey": "2020-04-23",
    "Ukraine": "2020-03-17",
    "United Arab Emirates": "2020-03-26",
    "United Kingdom": "2020-03-23",
    "United States": "2020-03-24",
    "Wisconsin": "2020-03-24",
    "Venezuela": "2020-03-17",
    "Zimbabwe": "2020-03-30"
}
