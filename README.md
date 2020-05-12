# ciri_machine
## Installation

```bash
git clone https://github.com/SkirOwen/ciri_machine.git
```  

### Requirements

It is better to use `Anaconda` and then run:

```
pip3 install -r requirements.txt
```
## Data Sources
US data come from     [NYTimes](https://github.com/nytimes/covid-19-data)  
Non-US data come from [(CSSE) Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)  
Thanks to both of them!

## Using cirilib
### data_extraction
#### pull_data

```python
pull_data(selected_data, selected_region, process=True, state=None, drop_fips=True, date_as_index=False)
``` 
will output a table for a country/region as follow:
`selected_data`is either `"Confirmed Cases"` or `"Reported Deaths"`  
  
| dates       | selected_data |
| ----------- |:-------------:|
| 2020-01-21  | 0             |
| 2020-01-22  | 1             |
| 2020-01-23  | 1             |

*Here `selected_data` is either `cases` or `deaths`*

`dates` can be put as index with `date_as_index=True`
`selected_region` can be any country or region (in the databases)  
If a specific US Sates is wanted you need to put `Selected_region = "US"` and `state = "the_specific_state"`  
`fips` can be left in for US States by setting `drop_fips=False`  

If `selected_data = None` then the output will be, for the selected country/region: 
| dates       | cases | deaths |
| ----------- |:-----:| ------:|
| 2020-01-21  | 0     | 0      |
| 2020-01-22  | 1     | 0      |
| 2020-01-23  | 1     | 0      |

#### lockdown_split

```python
lockdown_split(date_of_lockdown, selected_data=None, country=None, to_csv=False)
``` 
Create two `dateframes`, one from day:0 to the `date_of_lockdown`(excl.) and one from `date_of_lockdown`(incl.) to now, with the mean of the `selected_data` (see above) and the mean of the `Growth Factor` during that time.

`date_of_lockdown` is in iso-format: `YYYY-MM-DD`  
`selected_data` see above  
`country` specific country/region (no states) if `None` than do it for all of them  
`to_csv` output to a csv in `./dataset/csv_report` with the name `"before/after_" + date_of_lockdown + ".csv"`

Example of one of the two dataframe (`"after_2020-03-15.csv`, generated on the `2020-05-12`):  

| Country       | Cases  | Deaths | Growth Factor |
| --------------|:------:| ------:| -------------:|
| "Afghanistan" | 65885  | 1975   | 1.42478086576 |
| "Albania"     | 26855  | 1156   | 1.13824134829 |
| "Algeria"     | 129216 | 14775  | 1.32983989418 |

<img src="https://github.com/SkirOwen/ciri_machine/blob/master/logo/growth_factor.png" width="200"></img>  
`N` is the number of new cases on the day `d`  

### ClusteringCOVID19
#### clustering

```python
clustering(lockdown_date, k=3, omitted_country="France", backend="sns")
``` 

Create clustering from the data from `lockdown_split` and ouptut a graph  
`k` number of cluster  
`backend` ploting backend `plt` or `sns` *(`sns` does not yet configured for colours from clustering, recommand using `plt` for now)*  
`omitted_country` is the country you want to test and as to be omitted from the training (value stored in `delted_row`)  

Graph with plt:  
![alt text](https://github.com/SkirOwen/ciri_machine/blob/master/logo/graph_plt.png "Graph with plt")  

Graph with sns:    
![alt text](https://github.com/SkirOwen/ciri_machine/blob/master/logo/graph_sns.png "Graph with sns")

### Report PDF

[Report](https://github.com/SkirOwen/ciri_machine/blob/master/logo/ciri.pdf)  
