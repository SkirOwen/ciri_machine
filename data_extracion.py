from cirilib.imports import *


def pull_data(selected_data, selected_region, update_selected_countries=True):
    # console.log('pulling', selected_data, ' for ', selected_region)
    if selected_region != "US":
        url = ""
        if selected_data == "Confirmed Cases":
            url = url_jh_cases
        elif selected_data == "Reported Deaths":
            url = url_jh_deaths
        else:
            return
        df = pd.read_csv(url)
    
    # TODO: Here cases and deaths are on the same csv
    else:  # selected_region == "US"
        data_type = 'deaths' if selected_data == 'Reported Deaths' else 'cases'
        url = url_us_data
        df = pd.read_csv(url)
    
    return process_data(df, selected_region)


def process_data(df, selected_region, *args):
    k = 4
    if selected_region in PROVINCE_REGION:
        region = df.loc[df["Province/State"] == selected_region]
    else:
        region = df.loc[(df["Country/Region"] == selected_region) & (df["Province/State"].isna())]
        
        if region.empty:
            region = df.loc[(df["Country/Region"] == selected_region)].groupby("Country/Region", as_index=False).sum()
            k = 3

    dates = df.iloc[0:0, k:]
    
    # Really ugly, need to rework that better and speed it
    return pd.DataFrame(data={"dates": list(dates), "region": region.values[0][k:]})


if __name__ == "__main__":
    df = pull_data("Confirmed Cases", "United Kingdom")
    # sns.lineplot(data=df)
