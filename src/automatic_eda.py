import pandas as pd
from pandas_profiling import ProfileReport
import sweetviz as sv
from pathlib import Path
from config.config import load_config


class AutomaticEDA:
    def __init__(self, path, filename):
        self.config = load_config()
        self.data = self.__load_data(path, filename)

    def __load_data(self, path: str, filename: str):
        if self.config['data']['type_data'] == 'csv':
            return pd.read_csv(path + filename, sep='/t')
        elif self.config['data']['type_data'] == 'excel':
            return pd.read_excel(
                path + filename)  # , sheet_name='name' (use when there are few sheets in the same file)
        else:
            print('The input file has to be csv or excel')

    def __check_target(self):
        """ Function that check if the target from config.yaml exists, if not, use the rule to create it"""
        targetcol = self.config['automatic_eda']['target_colname']
        if not targetcol in self.data.columns:
            # self.data[targetcol] = eval(self.config['automatic_eda']['target_rule'])
            print('Target not defined')

    def make_profile(self):
        """ Automatic EDA using Pandas Profiling and/or Sweetviz"""
        title = self.config['report']['title']
        filename = self.config['data']['filename'].rsplit('.', 1)[0]
        if self.config['automatic_eda']['use_pdprofile']:  # Pandas Profiling
            profile = ProfileReport(
                self.data, title=title + filename + '_pandas_profile', explorative=True
            )
            profile.to_file(Path(self.config['data']['root_path'] + self.config['data'][
                'data_path'] + "output/" + filename + "_report.html"))
        if self.config['automatic_eda']['use_sweetviz']:  # Sweetviz
            self.__check_target()
            self.data = pd.read_excel(
                '/Users/nurimateos/PycharmProjects/forecasting/data/Exercise - Daily Sales - FOR CANDIDATE-SENT - SHORT.xlsx',
                sheet_name='Daily Sales')
            sweet_report = sv.analyze(self.data)
            sv.analyze([self.data, "Data"], target_feat=self.config['automatic_eda']['target_colname'])
            sweet_report.show_notebook()
            sweet_report.show_html(self.config['data']['root_path'] + self.config['data'][
                'data_path'] + "output/" + filename + '_sweetviz.html')
