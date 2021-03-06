from cirilib.imports import *
from sklearn.cluster import KMeans
from matplotlib import style

sns.set(style="whitegrid")
style.use("bmh")


# TODO: annotate when drop_no_lc is True is wrong


def clustering(lockdown_date, csv_name=None, label_countries=False, x_ax="Cases", y_ax="New Cases", k=3,
               omitted_country="France", graph_type="log", backend="plt", doubling=2, **kwargs):
    """
    Create and plot clustering using kmeans using the pd.DataFrame from data_extraction.lockdown_split function.
    Print =data= for 'omitted_country' with the predicted cluster ???

    Parameters
    ----------
    lockdown_date : str
                    Date in ISO format: YYYY-MM-DD
    csv_name : {"lockdown", lockdown_date}, optional
               file name of the csv, if None then csv_name = lockdown (the default is None)
    label_countries: bool, optional
                     Put countries name on the plot (the default is False)
    x_ax : {'Cases', 'Deaths', 'Growth Factor', 'New Cases'}, optional
           x axis values for the graph (the default is 'Cases')
    y_ax : {'Cases', 'Deaths', 'Growth Factor', 'New Cases'}, optional
           y axis values for the graph (the default is 'New Cases')
    k : int, optional
        Number of clusters (the default is 3)
    omitted_country : str, optional
                      (the default is 'France')
    graph_type : {'linear', 'semilog', 'logsemi', 'log'}, optional
                 type of graph representation (logsemi is where x is linear and y is log) (the default is 'log')
    backend : {'plt', 'sns'} , optional
              type of graph, 'plt' for matplotlib.pyplot, 'sns' for seaborn (the default is 'plt')
    doubling : int, optional
               number to change the 'doubling' day time of confirmed cases (the default is 2)
    kwarg : key, value mappings
            Other keywors arguments are passed down to
            `data_extraction`

    Yields
    ------
    plt.subplot

    Warnings
    --------
    Seaborn is not fully implemented yet, better to use backend='plt'
    """
    graph_types = ["linear", "semilogx", "semilogy", "log"]
    if graph_type not in graph_types:
        raise ValueError("Invalid graph type. Expected one of: %s" % graph_types)

    axis_types = ["Cases", "Deaths", "Growth Factor", "New Cases"]
    if x_ax not in axis_types or y_ax not in axis_types:
        raise ValueError("Invalid axis type. Expected one of: %s" % axis_types)

    before_after = ["$before$ ", "$after$ "]
    size_marker = 50
    csv_name = lockdown_date if csv_name is None else csv_name

    try:
        df1 = pd.read_csv(os.path.join(CSV_DIR, "before_" + csv_name + ".csv"))
        df2 = pd.read_csv(os.path.join(CSV_DIR, "after_" + csv_name + ".csv"))
        df_before_after = (df1, df2)
        created = False
    except FileNotFoundError:
        created = True
        lck_b_ctr = kwargs.get("lockdown_by_country", False)
        dnl = kwargs.get("drop_no_lc", False)
        sl_dt = kwargs.get("selected_data", None)
        ctr = kwargs.get("country", None)
        t_cs = kwargs.get("to_csv", True)
        fl_nm = kwargs.get("file_name", csv_name)
        dsb = kwargs.get("data_split_before", False)
        df_before_after = lockdown_split(lockdown_date, lockdown_by_country=lck_b_ctr, drop_no_lc=dnl,
                                         selected_data=sl_dt, country=ctr, to_csv=t_cs, file_name=fl_nm,
                                         data_split_before=dsb)

    fig, ax = plt.subplots(ncols=2)
    fig.subplots_adjust(hspace=0.5)

    for i in range(2):
        df = df_before_after[i].dropna()
        deleted_row = df[df["Country"] == omitted_country]
        deleted_row_index = deleted_row.index
        df = df.drop(deleted_row_index)

        print("DATABASE OVERVIEW :")
        print(df.head)

        # Create an instance of the KMeans class with a cluster size of 3
        kmeans = KMeans(n_clusters=k)

        # Create a matrix containing all points
        Countries = list(df['Country'])
        X = np.array(list(zip(df[x_ax], df[y_ax])))

        # Train the model
        kmeans = kmeans.fit(X)

        # Assign a label to all of the points
        labels = kmeans.predict(X)

        # Get the centroids
        Centroids = kmeans.cluster_centers_

        # Print the clusters label and centroids
        print("LABELS: ")
        print(labels)
        print("CENTROIDS LOCATIONS: ")
        print(Centroids)

        flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]

        # setting the graph type
        if graph_type == "linear":
            x_scale = "linear"
            y_scale = "linear"

        elif graph_type == "semilogx":
            x_scale = "log"
            y_scale = "linear"

        elif graph_type == "semilogy":
            x_scale = "linear"
            y_scale = "log"

        else:  # graph_type == "log"
            x_scale = "log"
            y_scale = "log"

        if backend == "plt":
            # Plot the points and centroids on a scatter plot
            # And map the labels to colors

            colors = [flatui[i] for i in labels]

            ax[i].set(title=("$State$ " + before_after[i] + "$" + lockdown_date + "$"), xlabel="$" + x_ax + "$",
                      ylabel="$" + y_ax + "$")

            ax[i].scatter(df[x_ax], df[y_ax], c=colors, s=df["Growth Factor"] * size_marker)
            ax[i].scatter(Centroids[:, 0], Centroids[:, 1], marker='*', c='black', s=20)
            if label_countries:
                for r, txt in enumerate(Countries):
                    ax[i].annotate(txt, (list(df[x_ax])[r], list(df[y_ax])[r]), size=10)

            if (x_ax == "Cases" or x_ax == "Deaths") and (y_ax == "New Cases" or
                                                          y_ax == "New Deaths") and (graph_type == "log" or
                                                                                     graph_type == "linear"):
                max_y = max(df[y_ax]) * 2 * doubling
                ax[i].plot([k * 1 / (2 * doubling) for k in range(0, 1000000) if k <= max_y],
                           '--', color='grey', label=(doubling, 'Day Doubling Time of Confirmed Cases'))
            ax[i].set_xscale(x_scale)
            ax[i].set_yscale(y_scale)
            ax[i].set_xlim(np.min(df[x_ax]))
            ax[i].set_ylim(0.01)

        else:
            # doesn't do everything, better to use plt
            clarity_ranking = COUNTRIES
            sns.scatterplot(x=df[x_ax], y=df[y_ax], hue="Country", palette="ch:r=-.2,d=.3_r", size="Growth Factor",
                            hue_order=clarity_ranking, sizes=(10, 75), data=df, ax=ax[i]).legend_.remove()

        # Print out the clusters to which point belongs
        print("CLUSTERS TO WHICH POINT BELONGS TO :")
        for j, labels in enumerate(labels):
            spacing = "\t" * 2 * int(labels)
            print(spacing + "|" + Countries[j].ljust(32) + str(X[j]).ljust(17) + " Cluster " + str(int(labels)) + "|")

        # Before was the training part
        # Testing part for omitted_country
        # Making predictions
        print("----------------------------------------------------------------------")
        # TODO: this is not a prediction at all!
        print("PREDICTION FOR", omitted_country.upper(), before_after[i][1:-2], lockdown_date, ":")
        x_value = deleted_row.iloc[0][x_ax]
        y_value = deleted_row.iloc[0][y_ax]
        print(x_ax + ":", x_value)
        print(y_ax + ":", y_value)
        cluster = kmeans.predict([[x_value, y_value]])[0]
        ax[i].scatter(x_value, y_value, c='#fac205', s=deleted_row.iloc[0]["Growth Factor"] * size_marker)
        print("Cluster : ", flatui[cluster])
        print("----------------------------------------------------------------------")
        if not created:
            print(WARNING_OLD_CSV)

    if __name__ == "__main__":
        plt.show()

    return fig, ax


class Clustering:
    def __init__(self, lockdown_date, csv_name=None, label_countries=False, x_ax="Cases", y_ax="New Cases", k=3,
                 omitted_country="France", graph_type="log", backend="plt", doubling=2, **kwargs):
        self.lockown_date = lockdown_date
        self.csv_name = csv_name
        self.label_contries = label_countries
        self.x_ax = x_ax
        self.y_ax = y_ax
        self.omitted_country = omitted_country
        self.graph_type = graph_type
        self.backend = backend
        self.doubling = doubling
        self.kwargs = kwargs

    def k_compute(self):
        pass

    def plotting(self):
        pass


if __name__ == "__main__":
    lockdown = "2020-03-17"
    name = "lockdown"
    clustering(lockdown, name, lockdown_by_country=True, label_countries=False,
               x_ax="Cases", y_ax="New Cases", backend="plt",
               graph_type="log", kwargs={})
