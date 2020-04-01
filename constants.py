import os

DATASET_DIR = ""

url_who = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports"
WARNING_CHECK_MESSAGE = """
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