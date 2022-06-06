# FORECASTING

This is a code for a forecasting model with python.

## Installation

Use the 'requeriments.txt' file to install all the dependencies required.

```bash
pip install requeriments.txt
```

## Usage
With the main code:
```python
from src.exploratory.automatic_eda import AutomaticEDA
from src.exploratory.manual_eda import ManualEDA
from src.config.config import load_config
from src.utils import load_pickle

if __name__ == '__main__':
    config = load_config()
    if config['automatic_eda']['use_automatic']:
        automatic_eda = AutomaticEDA(config['data']['root_path'] +
                                     config['data']['data_path'],
                                     config['data']['filename'])
        automatic_eda.make_profile()
    elif config['manual_eda']['use_manual']:
        manual_eda = ManualEDA(config['data']['root_path'] + config['data']['data_path'], config['data']['filename'])
        df_nulls = manual_eda.filter_by_nulls(config['manual_eda']['trigger_nulls'],
                                              config['manual_eda']['remove_nulls'])
        corr_matrix, corr_values, big_positive_corr, big_negative_corr = manual_eda.filter_by_correlations(
            config['manual_eda']['trigger_correlation'])
    else:
        data = load_pickle(config['data_pickle']['pathfile'] + config['data_pickle']['filename'])
```

## Configurations

Use the *config.yaml* file to change any input parameter.


## Data

You need to dump the file with the input data into the *forecasting folder*, in the folder *data*. 

The outputs folders will be generated automatically stored.