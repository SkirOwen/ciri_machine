import numpy as np
import pandas as pd
from tqdm import tqdm
# os and datetime are in constants
from cirilib.constants import *


def pull_data(selected_data, selected_region, process=True, state=None, drop_fips=True, date_as_index=False):
    if selected_region != "US":
        url = ""
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

            df_processed = df1.assign(deaths=df2.region)

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
def process_data(df, selected_region, *args):
    k, k_d = 4, 4  # start column for the dates
    selected_region = "Taiwan*" if selected_region == "Taiwan" else selected_region
    selected_region = "United Kingdom" if selected_region == "UK" else selected_region

    if selected_region in PROVINCE_REGION:
        region = df.loc[df["Province/State"] == selected_region]
    else:
        region = df.loc[(df["Country/Region"] == selected_region) & (df["Province/State"].isna())]
        if region.empty:  # do the sum for country with only regions, e.g Canada, USA
            region = df.loc[(df["Country/Region"] == selected_region)].groupby("Country/Region", as_index=False).sum()
            k = 3
    dates = list(df.iloc[0:0, k_d:])
    dates_iso = [date_to_iso(i) for i in dates]

    return pd.DataFrame(data={"date": dates_iso, "cases": region.values[0][k:]}, dtype=np.int64)


def date_to_iso(date_us_with_slash: str):  # /!\ Cannot take years before 2000. reversed 2k bug ;)
    d = date_us_with_slash.split("/")
    day = d[1]
    month = d[0]
    year = "20" + d[2]
    return year + "-" + month.zfill(2) + "-" + day.zfill(2)


def lockdown_split(date_of_lockdown, selected_data=None, country=None, to_csv=False):
    """
    index_country   | cases before  | deaths before | growth rate | AND
                    | cases after   | deaths before | growth rate |
    """
    country = COUNTRIES if country is None else [country]
    df_before = pd.DataFrame(columns=["Country", "Cases", "Deaths", "Growth Factor"])
    df_after = pd.DataFrame(columns=["Country", "Cases", "Deaths", "Growth Factor"])

    pbar = tqdm(country)
    for name in country:
        pbar.set_description("Processing %s" % name)

        df = pull_data(selected_data, name)

        lockdown_index = df.date[df.date == date_of_lockdown].index.tolist()[0]

        cases_before = df.iloc[:lockdown_index, 1].sum()
        cases_after = df.iloc[lockdown_index:, 1].sum()

        deaths_before = df.iloc[:lockdown_index, 2].sum()
        deaths_after = df.iloc[lockdown_index:, 2].sum()

        growth_rate_before = []
        growth_rate_after = []

        for i in range(2, lockdown_index):
            delta_n_d = ((df.iloc[:lockdown_index, 1])[i]) - ((df.iloc[:lockdown_index, 1])[i - 1])
            delta_n_d1 = ((df.iloc[:lockdown_index, 1])[i - 1]) - ((df.iloc[:lockdown_index, 1])[i - 2])
            if np.isinf(delta_n_d / delta_n_d1) or np.isnan(delta_n_d / delta_n_d1):
                continue
            growth_rate_before.append(delta_n_d / delta_n_d1)

        for i in range(lockdown_index, len(df)):
            delta_n_d = ((df.iloc[lockdown_index - 2:, 1])[i]) - ((df.iloc[lockdown_index - 2:, 1])[i - 1])
            delta_n_d1 = ((df.iloc[lockdown_index - 2:, 1])[i - 1]) - ((df.iloc[lockdown_index - 2:, 1])[i - 2])
            if np.isinf(delta_n_d / delta_n_d1) or np.isnan(delta_n_d / delta_n_d1):
                continue
            growth_rate_after.append(delta_n_d / delta_n_d1)

        growth_rate_before_mean = np.nanmean(growth_rate_before)
        growth_rate_after_mean = np.nanmean(growth_rate_after)

        a = pd.DataFrame([[name, cases_before, deaths_before, growth_rate_before_mean]],
                         columns=["Country", "Cases", "Deaths", "Growth Factor"])

        df_before = df_before.append(a, ignore_index=True)
        df_after = df_after.append(pd.DataFrame([[name, cases_after, deaths_after, growth_rate_after_mean]],
                                     columns=["Country", "Cases", "Deaths", "Growth Factor"]), ignore_index=True)

        pbar.update(1)
    pbar.close()

    if to_csv:
        df_before.to_csv(os.path.join(CSV_DIR, "before_" + date_of_lockdown + ".csv"), index=False)
        df_after.to_csv(os.path.join(CSV_DIR, "after_" + date_of_lockdown + ".csv"), index=False)

    return df_before, df_after


if __name__ == "__main__":
    test = lockdown_split("2020-03-15", to_csv=True)
    print(test[0])
    print(test[1])

    # df = pull_data("Confirmed Cases", "Italy")
    # dfm = pull_data("Reported Deaths", "Italy")
    # dfuk = pull_data("Confirmed Cases", "UK")
    # print(df)
    # sns.lineplot(data=df)
    # sns.lineplot(data=dfm)
    # sns.lineplot(data=dfuk)
    # plt.show()
