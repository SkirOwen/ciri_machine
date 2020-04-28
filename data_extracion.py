from cirilib.imports import *
# TODO: something with the dates format, possibly change them to days??


def pull_data(selected_data, selected_region, state=None, drop_fips=True):
    if selected_region != "US":
        url = ""
        if selected_data == "Confirmed Cases":
            url = url_jh_cases
        elif selected_data == "Reported Deaths":
            url = url_jh_deaths
        else:
            print("Please select either 'Confirmed Cases' or 'Reported Deaths'")
            return
        df = pd.read_csv(url)
        df_processed = process_data(df, selected_region)

    else:  # selected_region == "US"
        data_type = 'cases' if selected_data == 'Reported Deaths' else 'deaths'
        if state is None:   # pd US full
            df = pd.read_csv(url_us_data)
        else:   # do for the states
            df = pd.read_csv(url_us_states)
            df = df.loc[df["state"] == state]
            df = df.drop(["state"], axis=1)
            if drop_fips:  # drop_fips = False if you need to cross-ref with other data
                df = df.drop(["fips"], axis=1)
        df_processed = df.drop([data_type], axis=1)  # drop the other column, see data_type
    
    df_processed = df_processed.set_index("date")
    return df_processed


# processing data for JH
def process_data(df, selected_region, *args):
    k = 4   # start column for the dates
    selected_region = "Taiwan*" if selected_region == "Taiwan" else selected_region
    
    if selected_region in PROVINCE_REGION:
        region = df.loc[df["Province/State"] == selected_region]
    else:
        region = df.loc[(df["Country/Region"] == selected_region) & (df["Province/State"].isna())]
        if region.empty:    # do the sum for country with only regions, e.g Canada, USA
            region = df.loc[(df["Country/Region"] == selected_region)].groupby("Country/Region", as_index=False).sum()
            k = 3
    dates = list(df.iloc[0:0, k:])
    dates_iso = [date_to_iso(i) for i in dates]
    
    return pd.DataFrame(data={"date": dates_iso, "region": region.values[0][k:]})


def date_to_iso(date_us_with_slash: str):   # /!\ Cannot take years before 2000. reversed 2k bug ;)
    d = date_us_with_slash.split("/")
    day = d[1]
    month = d[0]
    year = "20" + d[2]
    return year + "-" + month + "-" + day


if __name__ == "__main__":
    df = pull_data("Confirmed Cases", "US")
    print(df)
    # sns.lineplot(data=df)
