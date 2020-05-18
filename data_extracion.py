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


def lockdown_split(date_of_lockdown, selected_data=None, country=None, to_csv=False):
    """
    Create two DataFrames, one before and up to date_of_lockdown (not included), one after up to now (included) (or end
    of the outbreak).
    The DataFrames is as follow (with the default parameters):
    Index | Country | Cases | Deaths | Growth Factor | New Cases | New Deaths

    Parameters
    ----------
    date_of_lockdown : str
                       Must be ISO format: YYYY-MM-DD
    selected_data : str, optional
                    Confirmed Cases or Reported Deaths, if None the both, Confirmed Cases then Reported Deaths
    country : str, optional
              If you want for a specific country, if None than for every country in COUNTRIES (the default is None)
    to_csv : bool, optional
             export the generated DataFrame to two.csv, by default it is in './dataset/csv_report'
             named: before_'date_of_lockdown'.csv and after_'date_of_lockdown'.csv (the default is False)

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

        # Get the index corresponding to the date of lockdown
        lockdown_index = df.date[df.date == date_of_lockdown].index.tolist()[0]

        cases_before = df.iloc[:lockdown_index, 1][lockdown_index - 1]
        cases_after = df.iloc[lockdown_index:, 1][len(df) - 1] - df.iloc[:lockdown_index, 1][lockdown_index - 1]

        deaths_before = df.iloc[:lockdown_index, 2][lockdown_index - 1]
        deaths_after = df.iloc[lockdown_index:, 2][len(df) - 1] - df.iloc[:lockdown_index, 2][lockdown_index - 1]

        # Initialise growth rate
        growth_rate_before = []
        growth_rate_after = []

        # Initialise new cases, before as to have some data already inside since I am using the already present for
        # loop after
        new_cases_before = [((df.iloc[:lockdown_index, 1])[0]),
                            ((df.iloc[:lockdown_index, 1])[1]) - ((df.iloc[:lockdown_index, 1])[0])]
        new_cases_after = []

        # idem
        new_deaths_before = [((df.iloc[:lockdown_index, 2])[0]),
                             ((df.iloc[:lockdown_index, 2])[1]) - ((df.iloc[:lockdown_index, 2])[0])]
        new_deaths_after = []

        for i in range(2, lockdown_index):
            delta_n_d = ((df.iloc[:lockdown_index, 1])[i]) - ((df.iloc[:lockdown_index, 1])[i - 1])
            new_cases_before.append(delta_n_d)
            delta_n_d1 = ((df.iloc[:lockdown_index, 1])[i - 1]) - ((df.iloc[:lockdown_index, 1])[i - 2])

            new_deaths_before.append(((df.iloc[:lockdown_index, 2])[i]) - ((df.iloc[:lockdown_index, 2])[i - 1]))

            if delta_n_d1 == 0 or np.isnan(delta_n_d / delta_n_d1) or (delta_n_d / delta_n_d1) < 0:
                continue
            growth_rate_before.append(delta_n_d / delta_n_d1)

        for i in range(lockdown_index, len(df)):
            delta_n_d = ((df.iloc[lockdown_index - 2:, 1])[i]) - ((df.iloc[lockdown_index - 2:, 1])[i - 1])
            new_cases_after.append(delta_n_d)
            delta_n_d1 = ((df.iloc[lockdown_index - 2:, 1])[i - 1]) - ((df.iloc[lockdown_index - 2:, 1])[i - 2])

            new_deaths_after.append(((df.iloc[lockdown_index - 2:, 2])[i]) - ((df.iloc[lockdown_index - 2:, 2])[i - 1]))

            if delta_n_d1 == 0 or np.isnan(delta_n_d / delta_n_d1) or (delta_n_d / delta_n_d1) < 0:
                continue
            growth_rate_after.append(delta_n_d / delta_n_d1)

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

        a = pd.DataFrame(
            [[name, cases_before, deaths_before, growth_rate_before_mean, new_cases_before_mean,
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
        df_before.to_csv(os.path.join(CSV_DIR, "before_" + date_of_lockdown + ".csv"), index=False)
        df_after.to_csv(os.path.join(CSV_DIR, "after_" + date_of_lockdown + ".csv"), index=False)

    return df_before, df_after


if __name__ == "__main__":
    test = lockdown_split("2020-04-15", to_csv=True)
    print(test[0])
    print(test[1])

    # import seaborn as sns
    # import matplotlib.pyplot as plt

    # df = pull_data("Confirmed Cases", "France", date_as_index=True)
    # dfm = pull_data("Reported Deaths", "Italy")
    # dfuk = pull_data("Confirmed Cases", "UK")
    # print(df)
    # sns.lineplot(data=df)
    # sns.lineplot(data=dfm)
    # sns.lineplot(data=dfuk)
    # plt.show()
