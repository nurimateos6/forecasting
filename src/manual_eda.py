import pandas as pd
from config.config import load_config
import seaborn as sns
import matplotlib.pyplot as plt
import utils as ut


class ManualEDA:
    def __init__(self, path, filename):
        self.config = load_config()
        self.data = self.__load_data(path, filename)

    def __load_data(self, path: str, filename: str):
        if self.config['data']['type_data'] == 'csv':
            return pd.read_csv(path + filename, sep='/t')
        elif self.config['data']['type_data'] == 'excel':
            return pd.read_excel(path + filename)
        else:
            print('The input file has to be csv or excel')
            return None

    def __null_values(self):
        """ Function that genereates a dataframe with the number of nulls in each coluns and the total % of null in
        each columns """
        if self.data.isnull().values.any():
            print(f'The total number of null values {self.data.isnull().values.sum()} in {len(self.data.columns)} columns \n')
            df_nulls = pd.DataFrame(self.data[self.data.columns[self.data.isnull().any()]].isnull().sum())
            df_percentage_nulls_per_column = (self.data[self.data.columns[self.data.isnull().any()]].isnull().sum()*100/len(self.data)).round(3) 
            results = pd.concat([df_nulls, df_percentage_nulls_per_column], axis=1, ignore_index=True)      
            results.columns = ['nulls', '%']      
            results = results.sort_values(by=['nulls'], ascending=False)
            ut.missing_bars(self.data, figsize=(10, 15), style='ggplot', dict_var=dict(enumerate(self.data.columns)))
            return results
    
    def __remove_col(self, cols):
        for col in cols:
            del self.data[col]
            
    def remove_nulls(self, trigger_nulls: float):
        """ Function that returns a dataframe with the columns that have a % of null values greater than a given
        value """
        stadistics_nulls = self.__null_values()
        return stadistics_nulls[stadistics_nulls['%']> trigger_nulls]
            
    def filter_by_nulls(self, trigger_nulls: float, remove_nulls: False):
        """ Function that returns a dataframe with the columns that have a % of null values greater than a given
        value """
        stadistics_nulls = self.__null_values()
        if not stadistics_nulls.empty and remove_nulls:
            self.__remove_col(stadistics_nulls.index) 
        return stadistics_nulls[stadistics_nulls['%']> trigger_nulls]
    
    def __correlation(self):
        corr_matrix = self.data.corr(method=self.config['manual_eda']['correlation_method']).round(2)
        fig, ax = plt.subplots(figsize=(15, 15))
        sns.heatmap(corr_matrix, annot=True, linewidths=4, ax=ax)
        plt.title('Correlation matrix')
        filename = self.config['data']['filename'].rsplit('.', 1)[0]
        plt.savefig(self.config['data']['data_path'] + 'output\\' + filename + '_correlation_matrix.png')
        corr_values = corr_matrix.unstack().sort_values(kind='quicksort')
        return corr_matrix, corr_values
    
    def filter_by_correlations(self, trigger_correlation: float):
        corr_matrix, corr_values = self.__correlation()
        big_positive_corr = corr_values[corr_values > trigger_correlation].sort_values(ascending=False)
        big_negative_corr = corr_values[corr_values < -trigger_correlation].sort_values(ascending=False)
        return corr_matrix, corr_values, big_positive_corr, big_negative_corr
    
    



