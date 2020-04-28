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
        df_processed = df.drop([data_type], axis=1)  # drop the other column, see data_type
        if drop_fips:    #
            df_processed = df_processed.drop(["fips"], axis=1)
            
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
    dates = df.iloc[0:0, k:]
    # Really ugly, need to rework that better and speed it
    return pd.DataFrame(data={"dates": list(dates), "region": region.values[0][k:]})


if __name__ == "__main__":
    df = pull_data("Confirmed Cases", "US")
    print(df)
    # sns.lineplot(data=df)
