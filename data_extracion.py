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
        # process_data

    # TODO: Here cases and deaths are on the same csv
    else:  # selected_region == "US"
        data_type = 'deaths' if selected_data == 'Reported Deaths' else 'cases'
        url = url_us_data
        df = pd.read_csv(url)

    row = df.iloc[116, 4:]
    print(row)
    row.plot()
    plt.show()
    # fig = px.line(df, x=str(df.iloc[0, 4:]), y=df.iloc[1:, 4:], title="test")
    # fig.show()

def process_data(df, selected_region, *args):
	dates = []
	region = df.loc[selected_region]
