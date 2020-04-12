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

# Need to be updated 'manually' if there are new countries that have become infected since 2020-04-01, sitrep 72
# TODO: Figure out what to do about 'territories**'
REGIONS = {
    'Western Pacific Region': ['China', 'Republic of Korea', 'Australia', 'Malaysia', 'Japan', 'Philippines',
                               'Singapore', 'New Zealand', 'Viet Nam', 'Brunei Darussalam', 'Cambodia',
                               'Mongolia', "Lao People's", 'Democratic Republic', 'Fiji', 'Papua New Guinea',
                               'Territories**', 'Guam', 'French Polynesia', 'New Caledonia', 'Northern Mariana',
                               'Islands', '(Commonwealth of', 'the)'],
    'European Region': ['Italy', 'Spain', 'Germany', 'France', 'The United Kingdom', 'Switzerland', 'Turkey',
                        'Belgium', 'Netherlands', 'Austria', 'Portugal', 'Israel', 'Norway', 'Sweden', 'Czechia',
                        'Ireland', 'Denmark', 'Russian Federation', 'Poland', 'Romania', 'Luxembourg', 'Finland',
                        'Greece', 'Iceland', 'Serbia', 'Croatia', 'Slovenia', 'Estonia', 'Ukraine', 'Lithuania',
                        'Armenia', 'Hungary', 'Bosnia and\rHerzegovina', 'Bulgaria', 'Latvia', 'Andorra', 'Slovakia',
                        'Republic of Moldova', 'Kazakhstan', 'North Macedonia', 'Azerbaijan', 'Cyprus', 'Albania',
                        'San Marino', 'Uzbekistan', 'Malta', 'Belarus', 'Georgia', 'Kyrgyzstan', 'Montenegro',
                        'Liechtenstein', 'Monaco', 'Holy See', 'Territories**', 'Faroe Islands', 'Kosovo[1]',
                        'Gibraltar', 'Jersey', 'Guernsey', 'Isle of Man', 'Greenland'],
    'South-East Asia Region': ['Thailand', 'India', 'Indonesia', 'Sri Lanka', 'Bangladesh', 'Maldives', 'Myanmar',
                               'Nepal', 'Bhutan', 'Timor-Leste'],
    'Eastern Mediterranean Region': ['Iran (Islamic Republic\rof)', 'Pakistan', 'Saudi Arabia', 'Qatar', 'Egypt',
                                     'Iraq', 'United Arab Emirates', 'Morocco', 'Bahrain', 'Lebanon', 'Tunisia',
                                     'Kuwait', 'Jordan', 'Oman', 'Afghanistan', 'Djibouti', 'Libya',
                                     'Syrian Arab Republic', 'Sudan', 'Somalia', 'erritories**',
                                     'occupied Palestinian\rterritory'],
    'Region of the Americas': ['United States of\rAmerica', 'Canada',  'Brazil', 'Chile', 'Ecuador',
                               'Dominican Republic', 'Mexico', 'Peru', 'Panama', 'Argentina', 'Colombia', 'Uruguay',
                               'Costa Rica', 'Cuba', 'Honduras', 'Venezuela (Bolivarian\rRepublic of)',
                               'Bolivia (Plurinational\rState of)', 'Trinidad and Tobago', 'Paraguay', 'Guatemala',
                               'Jamaica', 'Barbados', 'El Salvador', 'Haiti', 'Bahamas', 'Guyana', 'Dominica',
                               'Grenada', 'Saint Lucia', 'Saint Kitts and Nevis', 'Suriname', 'Antigua and Barbuda',
                               'Nicaragua', 'Belize', 'Saint Vincent and the\rGrenadines', 'Territories**',
                               'Puerto Rico', 'Martinique', 'Guadeloupe', 'Aruba', 'French Guiana',
                               'United States Virgin\rIslands', 'Bermuda', 'Saint Martin', 'Cayman Islands',
                               'Curaçao', 'Saint Barthélemy', 'Sint Maarten', 'Montserrat',
                               'Turks and Caicos\rIslands', 'British Virgin Islands', 'Anguilla'],
    'African Region': ['South Africa', 'Algeria', 'Burkina Faso', 'Senegal', 'Cote d’Ivoire', 'Ghana', 'Mauritius',
                       'Cameroon', 'Nigeria', 'Democratic Republic', 'of the Congo', 'Rwanda', 'Madagascar', 'Kenya',
                       'Zambia', 'Togo', 'Uganda', 'Ethiopia', 'Niger', 'Congo', 'United Republic of', 'Tanzania',
                       'Mali', 'Guinea', 'Equatorial Guinea', 'Namibia', 'Benin', 'Eswatini', 'Guinea-Bissau',
                       'Mozambique', 'Seychelles', 'Zimbabwe', 'Angola', 'Chad', 'Gabon', 'Central African',
                       'Republic', 'Eritrea', 'Cabo Verde', 'Mauritania', 'Botswana', 'Gambia', 'Liberia', 'Burundi',
                       'Sierra Leone', 'Territories**', 'Réunion', 'Mayotte']
}
