import os
from datetime import date

# TODO: fix the directory import either by doing a test of is DATASET_DIR exist and giving the path from
#  the start or doing ciri.py and execute with python -m ciri.py *****

DATASET_DIR = "./dataset"
PDF_DIR = os.path.join(DATASET_DIR, "pdf_reports")
CSV_DIR = os.path.join(DATASET_DIR, "csv_reports")


def initialise_directory():
    global DATASET_DIR
    global PDF_DIR
    global CSV_DIR

    if not os.path.isdir(DATASET_DIR):
        DATASET_DIR = "./dataset"
        print(
            f"Reports will be written to {DATASET_DIR + os.sep}"
        )

    PDF_DIR = os.path.join(DATASET_DIR, "pdf_reports")
    CSV_DIR = os.path.join(DATASET_DIR, "csv_reports")

    for folder in [PDF_DIR, CSV_DIR]:
        if folder != "" and not os.path.exists(folder):
            os.makedirs(folder)


url_who = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
WARNING_CHECK_MESSAGE = """
Everything seems to be good!
Though, this only check if there are the same number of report then days since 21 Jan 2020.
There might be duplicates and this message would still be raised, but it's unlikely.
"""

WARNING_DUPLICATE_REPORT = """
Uh-oh, there is something wrong, there are more file than it suppose to.
Check duplicate function has not ye been introduce, sorry, you'll have to do it by hand :(
"""

BEGIN_DATE = date(2020, 1, 21)


if not DATASET_DIR:
    initialise_directory()
