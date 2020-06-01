import numpy as np
import pandas as pd
from tqdm import tqdm
# os and datetime are in constants
from cirilib.constants import *


def pull_data(selected_data, selected_region, process=True, state=None, drop_fips=True, date_as_index=False):
    """
    Extracted data form the John Hopkins or NYTimes (if US) database for COVID-19

    Parameters
    __________
    selected_data : str, {'Confirmed Cases', 'Reported Deaths', None}
                    Date to be extracted, if None the it is both.
    selected_region : str
                      Region/Country to be extracted
    process : bool, optional
              if the DataFrame extracted will go through process_data function (the default is True)
    state : str, optional
            Extract data from the US state selected (the default is None)
    drop_fips : bool, optional
                drop fips data of the state, ONLY WORKS IF A STATE IS SELECTED (the default is False)
    date_as_index : bool, optional
                    set the data as index (the default is False)

    Returns
    _______
    df_processed : DataFrame
                   like this: index(could be date) | (date) | selected_data
    """
    if selected_region != "US":
        if selected_data == "Confirmed Cases":
            url = url_jh_cases
        elif selected_data == "Reported Deaths":
            url = url_jh_deaths
        elif selected_data is None:
            url = url_jh_cases
            df1 = pd.read_csv(url)
            df1 = process_data(df1, selected_region)
            url = url_jh_deaths
            df2 = pd.read_csv(url)
            df2 = process_data(df2, selected_region)

            df_processed = df1.assign(deaths=df2.selected_data)

        else:
            print("Please select either 'Confirmed Cases' or 'Reported Deaths'")
            return
        df = pd.read_csv(url)
        if process and selected_data:
            df_processed = process_data(df, selected_region)

    else:  # selected_region == "US"
        data_type = 'cases' if selected_data == 'Reported Deaths' else 'deaths'
        if state is None:  # pd US full
            df = pd.read_csv(url_us_data)
        else:  # do for the states
            df = pd.read_csv(url_us_states)
            df = df.loc[df["state"] == state]
            df = df.drop(["state"], axis=1)
            if drop_fips:  # drop_fips = False if you need to cross-ref with other data
                df = df.drop(["fips"], axis=1)
        if selected_data:
            df_processed = df.drop([data_type], axis=1)  # drop the other column, see data_type
        else:
            df_processed = df

    if date_as_index:
        df_processed = df_processed.set_index("date")
    return df_processed


# processing data for JH
def process_data(df, selected_region):
    """
    Only for data from a John Hopkins' database-like
    Create a pd.DataFrame frame of the Country/Region selected, as follow:
    index | date | selected_data

    date is in the ISO format

    Parameters
    ----------
    df : pd.DataFrame
         DataFrame like the ones from the pull_data() function, i.e John Hopkins COVID-19 cases.
    selected_region : str
                      String of the country or regions or states that is present in df.

    Yields
    ------
    pd.DataFrame
    index | date | selected_region
    """
    k, k_d = 4, 4  # start column for the dates
    selected_region = "Taiwan*" if selected_region == "Taiwan" else selected_region
    selected_region = "United Kingdom" if selected_region == "UK" else selected_region

    if selected_region in PROVINCE_REGION:
        region = df.loc[df["Province/State"] == selected_region]
    else:
        region = df.loc[(df["Country/Region"] == selected_region) & (df["Province/State"].isna())]
        if region.empty:  # do the sum for country with only regions, e.g Canada
            region = df.loc[(df["Country/Region"] == selected_region)].groupby("Country/Region", as_index=False).sum()
            k = 3
    dates = list(df.iloc[0:0, k_d:])
    dates_iso = [date_to_iso(i) for i in dates]

    return pd.DataFrame(data={"date": dates_iso, "selected_data": region.values[0][k:]}, dtype=np.int64)


def date_to_iso(date_us_with_slash: str):  # /!\ Cannot take years before 2000. reversed 2k bug ;)
    """
    Transform a date into the ISO format.

    Parameters
    ----------
    date_us_with_slash : str
                         date in the format M/D/YYYY
    Yields
    ------
    str
        date in format ISO YYYY-MM-DD
    """
    d = date_us_with_slash.split("/")
    day = d[1]
    month = d[0]
    year = "20" + d[2]
    return year + "-" + month.zfill(2) + "-" + day.zfill(2)


def lockdown_split(date_of_lockdown, lockdown_by_country=True, drop_no_lc=False, selected_data=None, country=None, to_csv=False,
                   file_name=None, data_split_before=False):
    """
    Create two DataFrames, one before and up to date_of_lockdown (not included), one after up to now (included) (or end
    of the outbreak).
    The DataFrames is as follow (with the default parameters):
    Index | Country | Cases | Deaths | Growth Factor | New Cases | New Deaths

    Parameters
    ----------
    date_of_lockdown : str
                       Must be ISO format: YYYY-MM-DD
    lockdown_by_country : bool, optional
                          Get the lockdown date for each country that are in LOCKDOWN_DATE, if not takes the
                          date_of_lockdown (the default is True)
    drop_no_lc : bool, optional
                 drop countries that are not in LOCKDOWN_DATE
    selected_data : str, optional
                    Confirmed Cases or Reported Deaths, if None the both, Confirmed Cases then Reported Deaths
    country : str or None, optional
              If you want for a specific country, if None than for every country in COUNTRIES (the default is None)
    to_csv : bool, optional
             export the generated DataFrame to two.csv, by default it is in './dataset/csv_report'
    file_name : str or None, optional
                specify the name of the file to export to with the prefix 'before_' and 'after_',
                if None then the name is: before_'date_of_lockdown'.csv and after_'date_of_lockdown'.csv
                (the default is None)
    data_split_before : bool, optional
                        if True after the data after is only from the date of the lockdown, whereas if False it
                        is from the beginning (the default is False)

    Returns
    -------
    df_before : pd.DataFrame
    df_after : pd.DataFrame
    """
    country = COUNTRIES if country is None else [country]
    df_before = pd.DataFrame(columns=["Country", "Cases", "Deaths", "Growth Factor", "New Cases", "New Deaths"])
    df_after = pd.DataFrame(columns=["Country", "Cases", "Deaths", "Growth Factor", "New Cases", "New Deaths"])

    pbar = tqdm(country)
    for name in country:
        pbar.set_description("Processing " + name.ljust(24))

        df = pull_data(selected_data, name)

        if drop_no_lc and name not in LOCKDOWN_DATE.keys():
            pbar.update(1)
            continue

        date_of_lockdown = LOCKDOWN_DATE[name] if (name in LOCKDOWN_DATE.keys()
                                                   and lockdown_by_country) is True else date_of_lockdown

        # Get the index corresponding to the date of lockdown
        lockdown_index = df.date[df.date == date_of_lockdown].index.tolist()[0]

        # Variable for the cases and death list
        cases_lst = df.iloc[:, 1]
        death_lst = df.iloc[:, 2]

        cases_before = cases_lst[lockdown_index - 1]
        deaths_before = death_lst[lockdown_index - 1]

        if data_split_before:
            cases_after = cases_lst[len(df) - 1]
            deaths_after = death_lst[len(df) - 1]

        else:
            cases_after = cases_lst[len(df) - 1] - cases_lst[lockdown_index - 1]
            deaths_after = death_lst[len(df) - 1] - death_lst[lockdown_index - 1]

        # Initialise growth rate
        growth_rate_before, growth_rate_after = [], []

        # Initialise new cases, before as to have some data already inside since I am using the already present for
        # loop after
        new_cases = [(cases_lst[0]), (cases_lst[1]) - (cases_lst[0])]
        new_deaths = [(death_lst[0]), (death_lst[1]) - (death_lst[0])]

        for i in range(2, len(df)):
            delta_n_d = (cases_lst[i]) - (cases_lst[i - 1])
            new_cases.append(delta_n_d)
            delta_n_d1 = (cases_lst[i - 1]) - (cases_lst[i - 2])

            new_deaths.append((death_lst[i]) - (death_lst[i - 1]))

            if delta_n_d1 == 0 or np.isnan(delta_n_d / delta_n_d1) or (delta_n_d / delta_n_d1) < 0:
                continue
            if i < lockdown_index:
                growth_rate_before.append(delta_n_d / delta_n_d1)
            else:
                growth_rate_after.append(delta_n_d / delta_n_d1)

        new_cases_before = new_cases[:lockdown_index]
        new_cases_after = new_cases[lockdown_index:]
        new_deaths_before = new_deaths[:lockdown_index]
        new_deaths_after = new_deaths[lockdown_index:]

        # Test to avoid doing a mean of empty list and getting an NaN as output
        if growth_rate_before:
            growth_rate_before_mean = np.nanmean(growth_rate_before)
        else:
            growth_rate_before_mean = 0.0
        if growth_rate_after:
            growth_rate_after_mean = np.nanmean(growth_rate_after)
        else:
            growth_rate_after_mean = 0.0

        new_cases_before_mean = np.nanmean(new_cases_before)
        new_cases_after_mean = np.nanmean(new_cases_after)

        new_deaths_before_mean = np.nanmean(new_deaths_before)
        new_deaths_after_mean = np.nanmean(new_deaths_after)

        a = pd.DataFrame([[name, cases_before, deaths_before, growth_rate_before_mean, new_cases_before_mean,
                           new_deaths_before_mean]],
                         columns=["Country", "Cases", "Deaths", "Growth Factor", "New Cases", "New Deaths"])

        df_before = df_before.append(a, ignore_index=True)
        df_after = df_after.append(
            pd.DataFrame([[name, cases_after, deaths_after, growth_rate_after_mean, new_cases_after_mean,
                           new_deaths_after_mean]],
                         columns=["Country", "Cases", "Deaths", "Growth Factor", "New Cases", "New Deaths"]),
            ignore_index=True)

        pbar.update(1)
    pbar.close()

    if to_csv:
        if lockdown_by_country:
            file_name_out_bf = "before_lockdown.csv" if file_name is None else "before_" + file_name + ".csv"
            file_name_out_af = "after_lockdown.csv" if file_name is None else "after_" + file_name + ".csv"
            outfile1 = os.path.join(CSV_DIR, file_name_out_bf)
            outfile2 = os.path.join(CSV_DIR, file_name_out_af)
        else:
            file_name_out_bf = "before_" + date_of_lockdown + ".csv" if file_name is None else "before_" + file_name + ".csv"                                                                            ".csv"
            file_name_out_af = "after_" + date_of_lockdown + ".csv" if file_name is None else "after_" + file_name + ".csv"
            outfile1 = os.path.join(CSV_DIR, file_name_out_bf)
            outfile2 = os.path.join(CSV_DIR, file_name_out_af)

        df_before.to_csv(outfile1, index=False)
        df_after.to_csv(outfile2, index=False)

    return df_before, df_after


if __name__ == "__main__":
    # print(os.path.join(os.path.dirname(os.path.abspath(__file__)), CSV_DIR))
    print(CSV_DIR)
    lockdown_date = "2020-03-17"
    test = lockdown_split(lockdown_date, country="Italy", lockdown_by_country=True, drop_no_lc=True,
                          to_csv=True, file_name="test")
    # print(test[0])
    # print(test[1])

    # import seaborn as sns
    # import matplotlib.pyplot as plt
    #
    # df = pd.read_csv(os.path.join(CSV_DIR, "before_" + lockdown_date + ".csv"))
    # deleted_row = df[df["Country"] == "US"]
    # deleted_row_index = deleted_row.index
    # df = df.drop(deleted_row_index)
    # # df = pull_data("Confirmed Cases", "France", date_as_index=True)
    # # dfm = pull_data("Reported Deaths", "Italy")
    # # dfuk = pull_data("Confirmed Cases", "UK")
    # # print(df)
    # sns.scatterplot(x="Cases", y="New Cases", data=df)
    # # sns.lineplot(data=dfm)
    # # sns.lineplot(data=dfuk)
    # plt.show()
