# Water and Energy in Norway

ADD A PICTURE/VIDEO SELECTING THE DIFFERENT SELECTBOXES/CHECKBOX AND MOVING THE HOVER LABEL
**WATER FILLING CAPACITY PLOTS**
**ELECTRICITY PRICES PLOT**

## Project's Overview

*"Water and energy are linked"* as many authors in different bibliographies affirm. This link is even more "visible" in Norway, where hydropower is the primary energy source in this country (give a value). Therefore, due to my interest in the environmental field and Data Analysis I created this project using the Python libraries StreamLit and plotly to visualise **interactive plots** of:
  1. The water filling capacity of lakes in the five regions of Norway (i.e., Oslo, Kristiansand, Trondheim, Tromsø and Bergen) over the years.
  2. The last year's water filling capacity of lakes compared with historical values.
  3. Electricity prices from the current and next day. 
  
## Installation

This runs in any operatining system and can be installed via `pip` directly from GitHub

```
$ pip install git+https://github.com/MariaaAT/magasinstatistikk.git
```

## For developers
### Water Filling Capactity

There are two different functions to plotting in `magasinstatistikk_pyplot.py`.

The function `filling_capacity` will plot the water filling capacity from the different regions of Norway over the years, whereas the function `filled_plot` will draw the last year's water filling capacity compared with historical values. 

### Electricity Prices

The function `price_plot` is used and can be found in `electricity_prices.py`

## Lessons learnt

- [x] Data Analysis using Pandas and Jupyter Notebook.
- [x] Data Visualitation using StreamLit and plotly.
- [x] Transforming data from APIs.

## Future challenges

*"Perfection is attained by slow degrees; it requires the hand of time."*
                                                                        - *Voltaire*

The following improvements are expected to make:
- [ ] Include historical values from electricity prices.
- [ ] Combine filling capacity data with electricity prices and search for correlations.
- [ ] Observe how climate change has affected, affects and will affect these two studied fields.




