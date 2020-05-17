from cirilib.imports import *
from sklearn.cluster import KMeans
from matplotlib import style

sns.set(style="whitegrid")
style.use("bmh")

# TODO: gorwth factor changed test and plot somehow ?????


def clustering(lockdown_date, k=3, omitted_country="France", backend="sns"):
    before_after = ["$before$ ", "$after$ "]

    try:
        df1 = pd.read_csv(os.path.join(CSV_DIR, "before_" + lockdown_date + ".csv"))
        df2 = pd.read_csv(os.path.join(CSV_DIR, "after_" + lockdown_date + ".csv"))
        df_before_after = (df1, df2)
        created = False
    except FileNotFoundError:
        created = True
        df_before_after = lockdown_split(lockdown_date, to_csv=True)

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
        X = np.array(list(zip(df['Cases'], df['New Cases'])))

        # Train the model
        kmeans = kmeans.fit(X)

        # Assign a label to all of the points
        labels = kmeans.predict(X)

        # Get the centroids
        Centroids = kmeans.cluster_centers_

        # Print the clusters label and centroids
        print("LABELS :")
        print(labels)
        print("CENTROIDS LOCATIONS :")
        print(Centroids)

        flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]

        if backend == "plt":
            # Plot the points and centroids on a scatter plot
            # And map the labels to colors

            colors = [flatui[i] for i in labels]

            ax[i].set(title=("$State$ " + before_after[i] + lockdown_date), xlabel="$Confirmed$ $Cases$",
                      ylabel="$Reported$ $Deaths$")

            ax[i].scatter(np.log(df['Cases']), np.log(df['New Cases']), c=colors)
            ax[i].scatter(np.log(Centroids[:, 0]), np.log(Centroids[:, 1]), marker='*', c='black', s=20)

        else:
            clarity_ranking = COUNTRIES
            sns.scatterplot(x="Cases", y="Deaths", hue="Country", palette="ch:r=-.2,d=.3_r", size="Growth Factor",
                            hue_order=clarity_ranking, sizes=(10, 75), data=df, ax=ax[i]).legend_.remove()

        # Print out the clusters to which point belongs
        print("CLUSTERS TO WHICH POINT BELONGS TO :")
        for j, labels in enumerate(labels):
            spacing = "\t" * 2 * int(labels)
            print(spacing + "|" + Countries[j].ljust(32) + str(X[j]).ljust(17) + " Cluster " + str(int(labels)) + "|")

        # Before was the training part
        # Testing part for FRANCE
        # Making predictions
        print("----------------------------------------------------------------------")
        Cases = np.log(deleted_row.iloc[0]["Cases"])
        Deaths = np.log(deleted_row.iloc[0]["New Cases"])
        print("PREDICTION FOR", omitted_country.upper(), before_after[i][1:-2],  lockdown_date, ":")
        print("Cases:", Cases)
        print("Dead:", Deaths)
        cluster = kmeans.predict([[Cases, Deaths]])[0]
        ax[i].scatter(Cases, Deaths, c='#fac205')
        print("Cluster : ", flatui[cluster])
        print("----------------------------------------------------------------------")
        if not created:
            print(WARNING_OLD_CSV)

    plt.show()
    return


if __name__ == "__main__":
    # lockdown_date in format iso: YYYY-MM-DD
    lockdown_date = "2020-04-15"
    clustering(lockdown_date, backend="plt")
