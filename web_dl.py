from cirilib.imports import *
from tqdm import tqdm
from datetime import date
import requests


import cirilib.constants as c


url_who = c.url_who
PDF_DIR = c.PDF_DIR


# TODO: get name of last downloaded, to pass to export_from_pdf


def get_link_sitrep_who(url=url_who):
    from bs4 import BeautifulSoup as BS

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


def download_who_report():
    """
    Download sitrep from who in PDF file format
    """
    import warnings

    warnings.warn("download_who_report is deprecated and has been replaced by the John Hopkins database and nytimes, "
                  "use pull_data instead", DeprecationWarning)
    k = 0
    situation_reports_links, available_sr_name = get_link_sitrep_who()

    for dl_link, name, i in zip(situation_reports_links, available_sr_name, range(len(available_sr_name), 0, -1)):
        FILE_DIR = os.path.join(PDF_DIR, name)
        if not os.path.exists(FILE_DIR):
            url_dl = "https://who.int" + dl_link
            # report = requests.get(url_dl)
            report = requests.get(url_dl, stream=True)

            # Total size
            total_size = int(report.headers.get('content-length', 0))
            block_size = 1024  # 1 Kib
            t = tqdm(total=total_size, unit='iB', unit_scale=True)

            with open(FILE_DIR, "wb") as f:
                for data in report.iter_content(block_size):
                    # f.write(report.content)
                    t.update(len(data))
                    f.write(data)
            t.close()

            if total_size != 0 and t.n != total_size:
                print("ERROR, something went wrong")
            else:
                print("Situation report - ", i, ":  downloaded as ", name)
            k += 1

    print("%d situation reports downloaded" % k)


def check_new_report_who(download=False):
    """
    Compute with the number of days elapsed, i.e if today is 2 Apr 2020 then it is only gonna tell
    that it might be a new sitrep for 2020-04-02 iff it is run after 2020-04-02; this is logical.
    """
    today = date.today()
    days_since_begin = abs(today - c.BEGIN_DATE).days

    number_sr_downloaded = len(os.listdir(PDF_DIR))

    if number_sr_downloaded < days_since_begin:
        print("There might be a new situation report.")
        if download:
            download_who_report()
        return True
    elif number_sr_downloaded > days_since_begin:
        print(c.WARNING_DUPLICATE_REPORT)
    else:
        print(c.WARNING_CHECK_MESSAGE)
        return False


if __name__ == "__main__":
    check_new_report_who(download=True)
