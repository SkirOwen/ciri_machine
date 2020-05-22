# ciri_machine
## Installation

```bash
git clone https://github.com/SkirOwen/ciri_machine.git
```  

### Requirements

It is better to use `Anaconda` and then run:

```
pip install -r requirements.txt
```
If you don't have `Anaconda`:
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
lockdown_split(date_of_lockdown, lockdown_by_country=True, drop_no_lc=False, selected_data=None, country=None, to_csv=False, file_name=None)
``` 
Create two `dateframes`, one from day:0 to the `date_of_lockdown`(excl.) and one from `date_of_lockdown`(incl.) to now, with the mean of the `selected_data` (see above) and the mean of the `Growth Factor` during that time.

`date_of_lockdown` is in iso-format: `YYYY-MM-DD`  
`lockdown_by_country` split acording to the date of lokcdown for each country, if no lockdown the uses date_of_lockdown  
`drop_no_lc` drop countries with no lockdown_date  
`selected_data` see above  
`country` specific country/region (no states) if `None` than do it for all of them  
`to_csv` output to a csv in `./dataset/csv_report` with the name `"before/after_" + file_name + ".csv"`

Example of one of the two dataframe (`"after_2020-03-17.csv`, generated on the `2020-05-22`), `lockdown_by_country = False`:  

| Country       | Cases | Deaths | Growth Factor | New Cases | New Deaths |
| --------------|:-----:| ------:| -------------:| ---------:| ----------:|
| "Afghanistan" | 8145  | 187    | 1.38632113090 | 124.98461 | 2.87692307 |
| "Albania"     | 964   | 31     | 1.35124607203 | 14.046153 | 0.46153846 |
| "Algeria"     | 7542  | 568    | 1.30118394495 | 115.2     | 8.67692307 |

<img src="https://github.com/SkirOwen/ciri_machine/blob/master/logo/growth_factor.png" width="200"></img>  
`N` is the number of new cases on the day `d`  

### ClusteringCOVID19
#### clustering

```python
clustering(lockdown_date, csv_name=None, label_countries=False, x_ax="Cases", y_ax="New Cases", k=3, omitted_country="France", graph_type="log", backend="plt", doubling=2, **kwargs)
``` 

Create clustering from the data from `lockdown_split` and ouptut a graph  
`lockdown_date` date of lcd for the name of a file for a specific date  
`csv_name` overwrite the name of the file for a specific one  
`label_countries` put the country names on the graph  
`x_ax` specifies the x axis to use  
`y_ax` specifies the y axis to use  
`k` number of cluster  
`omitted_country` is the country you want to test and as to be omitted from the training (value stored in `delted_row`)  
`graph_type` graph type to plot, `linear`, `semilogx`, `semilogy`, `log`  
`backend` ploting backend `plt` or `sns` *(`sns` does not yet configured for colours from clustering, recommand using `plt` for now)*  
`doubling` number of day to double the x axis data, only for "Cases" vs "New Cases" and "Deaths" vs "New Deaths"  
`kwargs` parameters to be passed to `lockdown_split` 

Graph with plt:  
![alt text](https://github.com/SkirOwen/ciri_machine/blob/master/logo/graph_plt.png "Graph with plt")  


### Report PDF

[Report](https://github.com/SkirOwen/ciri_machine/blob/master/logo/ciri.pdf)  
