from automatic_eda import AutomaticEDA
from manual_eda import ManualEDA
from config.config import load_config
import os

if __name__ == '__main__':
    config = load_config()
    list_datafiles = os.listdir(config['data']['root_path'] + config['data']['data_path'])
    datafiles_to_study = list(set(list_datafiles).intersection(config['data']['filenames']))
    if config['automatic_eda']['use_automatic']:
        automatic_eda = AutomaticEDA(config['data']['root_path'] +
                                     config['data']['data_path'],
                                     config['data']['filename'])
        automatic_eda.make_profile()
    else:
        manual_eda = ManualEDA(config['data']['root_path'] + config['data']['data_path'], config['data']['filename'])
        df_nulls = manual_eda.filter_by_nulls(config['manual_eda']['trigger_nulls'],
                                              config['manual_eda']['remove_nulls'])
        corr_matrix, corr_values, big_positive_corr, big_negative_corr = manual_eda.filter_by_correlations(
            config['manual_eda']['trigger_correlation'])