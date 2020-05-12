##############################################################################
#                  Clustering Using K-means in Scikit-Learn
##############################################################################
#                           COVID 19 - 15/03/2020
##############################################################################

from cirilib.imports import *
# from data_extracion import *
from sklearn.cluster import KMeans
from matplotlib import style

sns.set(style="whitegrid")
style.use("bmh")

lockdown_date = "2020-03-15"
# Let k assume a value
k = 3


def clustering(lockdown_date, k=3, backend="sns"):
    before_after = ["$before$ ", "$after$ "]

    try:
        df1 = pd.read_csv(os.path.join(CSV_DIR, "before_" + lockdown_date + ".csv"))
        df2 = pd.read_csv(os.path.join(CSV_DIR, "after_" + lockdown_date + ".csv"))
        df_before_after = (df1, df2)
        print("\33[31m", "The data has been extracted from already existing files, consider regenerating them!", "\33[0m")
    except FileNotFoundError:
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
        for i, labels in enumerate(labels):
            spacing = "\t" * 2 * int(labels)
            print(spacing + "|" + Countries[i].ljust(32) + str(X[i]).ljust(17) + " Cluster " + str(int(labels)) + "|")

        # Before was the training part
        # Testing part for FRANCE
        # Making predictions
        print("**********************************************************************")
        Cases = 4501
        Deaths = 91
        print("PREDICTION FOR FRANCE before", lockdown_date, ":")
        print("Infected : 4501")
        print("Dead : 91")
        cluster = kmeans.predict([[Cases, Deaths]])[0]
        plt.scatter(Cases, Deaths, c='#fac205')
        print("Cluster : ", flatui[cluster])
        print("**********************************************************************")

    plt.show()
    return

###############################################################################
#                  Clustering Using K-means in Scikit-Learn
###############################################################################
#                          COVID 19 - 10/05/2020
###############################################################################
# # Import the data in a dataframe
# # df = pd.read_csv("COVID_10052020_Cumul.csv", sep=';')
# # Print the data
# df = df_before_after[1]
# print("DATABASE OVERVIEW :")
# print(df.head)
#
# # Plot the data
# # plt.subplot(223)
# # plt.scatter(df['Infections'],df['Deces'],c='b')
# # plt.title("$Représentation$ $2D$ $de$ $la$ $BDD$")
# # plt.xlabel('$Nombre$ $de$ $cas$ $infectés$')
# # plt.ylabel('$Nombre$ $de$ $morts$')
#
# # Let k assume a value
# k = 3
#
# # Create an instance of the KMeans class with a cluster size of 3
# kmeans = KMeans(n_clusters=k)
#
# # Create a matrix containing all points
# Countries = list(df['Country'])
# X = np.array(list(zip(df['Cases'], df['Deaths'])))
#
# # Train the model
# kmeans = kmeans.fit(X)
#
# # Assign a label to all of the points
# labels = kmeans.predict(X)
#
# # Get the centroids
# Centroids = kmeans.cluster_centers_
#
# # Print the clusters label and centroids
# print("LABELS :")
# print(labels)
# print("CENTROIDS LOCATIONS :")
# print(Centroids)
#
# # Plot the points and centroids on a scatter plot
# # And map the labels to colors
# flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
# colors = [flatui[i] for i in labels]
#
# plt.subplot(122)
# plt.title("$State$ $after$ " + lockdown_date)
# plt.scatter(df['Cases'], df['Deaths'], c=colors)
# plt.xlabel('$Confirmed$ $Cases$')
# plt.ylabel('$Reported$ $Deaths$')
#
# plt.scatter(Centroids[:, 0], Centroids[:, 1], marker='*', c='black', s=20)
#
# # Print out the clusters to which point belongs
# print("CLUSTERS TO WHICH POINT BELONGS :")
# for i, labels in enumerate(labels):
#     print(Countries[i] + str(X[i]), "Cluster " + str(int(labels)))
#
# # Before was the training part
# # Testing part for FRANCE
# # Making predictions
# print("**********************************************************************")
# Cases = 138888
# Deaths = 26707
# print("PREDICTION FOR FRANCE before", lockdown_date, ":")
# print("Infected : 176970")
# print("Dead : 26380")
# cluster = kmeans.predict([[Cases, Deaths]])[0]
# plt.scatter(Cases, Deaths, c='#fac205')
# print("Cluster : ", flatui[cluster])
# print("**********************************************************************"

# plt.show()


if __name__ == "__main__":
    clustering(lockdown_date, backend="plt")
