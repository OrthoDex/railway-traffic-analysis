## Railway Traffic Data Analysis

Analyzing over 28k rows of railway traffic density.

Each notebook in the notebooks folder is a different analysis on the railway traffic data.

The data was collected through the [planitmetro](https://planitmetro.com/data) web site, which hosts several datasets provided by the Washington Metropolitan Area Transit Authority data. This data has been cleaned up -stations which did not have any information about time were removed from the database. The dataset consists of over 28000 rows, each representing a group of 5 time peaks for a single station, identifying the number of average rides each day at 5 distinct times of the day (AM_PEAK, PM_PEAK, MIDDAY, LAATE NIGHT PEAK, EVENING). The data is accumulated for a period of approximately 6 years from Sept 2010 to Jan 2016.

To understand the 'distance' or correlation between stations, we increase the distance between two stations based on the overall variation between the %change in Passenger Density. For example, if a Station A has 2 data values (Passenger Density) - 4000 & 5000, it means an increase of 25%. Similarly, Station B having 2 data values - 400 & 500, also has an increase of 25%. Thus, both these stations have the same variation and thus could belong to the same cluster. Initially, we pre-process the data and compute the distance matrix.

We used Agglomerative Clustering on the distance matrix to find 10 clusters (default), and plot the Passenger Density with time.

We then compare the no of clusters with the cluster cohesion measure (Silhouette score & Calinski-Harabaz Index). 

## Authors:
Ilesha Garg
Ishaan Malhi

## Results

The results are quite interesting, the cohesion measure itself falls with an increase in the number of clusters.
When the number of clusters is 2, they show the maximum cohesion and when we look at the heatmaps, it becomes easy to understand why. The heatmaps have multiple lines of a darker shade (higher distance measures) cutting across a background of a lower shade (low distance measures).

## Tools
Application: 
- Jupyter Notebook running Python 3 kernel.
- Pandas
- Matplotlib with Seaborn

### Sckit Learn modules:
- Agglomerative Clustering
- BIRCH
- Silhouette Coefficient
- Calinski-Harabaz Index
