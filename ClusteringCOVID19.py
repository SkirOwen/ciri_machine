from cirilib.imports import *
from sklearn.cluster import KMeans
from matplotlib import style

sns.set(style="whitegrid")
style.use("bmh")


def clustering(lockdown_date, k=3, backend="sns"):
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
        df = df_before_after[i]

        print("DATABASE OVERVIEW :")
        print(df.head)

        # Plot the data
        # plt.subplot(221)
        # plt.scatter(df['Infections'],df['Deces'],c='b')
        # plt.title("$Représentation$ $2D$ $de$ $la$ $BDD$")
        # plt.xlabel('$Nombre$ $de$ $cas$ $infectés$')
        # plt.ylabel('$Nombre$ $de$ $morts$')

        # Let k assume a value
        # k = 3

        # Create an instance of the KMeans class with a cluster size of 3
        kmeans = KMeans(n_clusters=k)

        # Create a matrix containing all points
        Countries = list(df['Country'])
        X = np.array(list(zip(df['Cases'], df['Deaths'])))

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

            ax[i].scatter(df['Cases'], df['Deaths'], c=colors)
            ax[i].scatter(Centroids[:, 0], Centroids[:, 1], marker='*', c='black', s=20)

        else:
            clarity_ranking = COUNTRIES
            sns.scatterplot(x="Cases", y="Deaths", hue="Country", palette="ch:r=-.2,d=.3_r", size="Growth Factor",
                            hue_order=clarity_ranking, data=df, ax=ax[i]).legend_.remove()

        # Print out the clusters to which point belongs
        print("CLUSTERS TO WHICH POINT BELONGS :")
        for j, labels in enumerate(labels):
            spacing = "\t" * 2 * int(labels)
            print(spacing + "|" + Countries[j].ljust(32) + str(X[j]).ljust(17) + " Cluster " + str(int(labels)) + "|")

        # Before was the training part
        # Testing part for FRANCE
        # Making predictions
        print("**********************************************************************")
        Cases = 4501
        Deaths = 91
        print("PREDICTION FOR FRANCE", before_after[i][1:-2],  lockdown_date, ":")
        print("Cases:", Cases)
        print("Dead:", Deaths)
        cluster = kmeans.predict([[Cases, Deaths]])[0]
        plt.scatter(Cases, Deaths, c='#fac205')
        print("Cluster : ", flatui[cluster])
        print("**********************************************************************")
        if not created:
            print(WARNING_OLD_CSV)

    plt.show()
    return


if __name__ == "__main__":
    # lockdown_date in format iso: YYYY-MM-DD
    lockdown_date = "2020-03-15"
    clustering(lockdown_date, backend="plt")
