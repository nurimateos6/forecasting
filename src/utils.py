import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.config.config import load_config
import pickle


## CHECK COLUMNS TYPES
def __unique_types_df(data: pd.DataFrame):
    return data.dtypes.unique()


def __check_coltype(data: pd.DataFrame, col: str):
    return data[col].dtypes


def __stadistics_basics(data: pd.DataFrame, col: str):
    mean = data[col].mean()
    median = data[col].median()
    std = data[col]
    return pd.DataFrame({'Mean': mean, 'Median': median, 'Std': std})


# UNIVARIATE FOR NUMERIC COLUMNS
def univariate_numeric(data: pd.DataFrame, col: str):
    stats = __stadistics_basics(data, col)
    val_counts = data[col].value_counts(sort=True)
    tab = pd.crosstab(index=data[col], columns='count')
    tab_percentage = tab / tab.sum()
    return stats, val_counts, tab, tab_percentage


def is_numeric(data: pd.DataFrame, col: str):
    if ((__check_coltype(data, col) == 'float') or (__check_coltype(data, col) == 'int64')):
        return True
    else:
        return False


# MISSING VALUES
def missing_var(data: pd.DataFrame, col: str):
    null_count = data[col].isnull().sum()
    null_perc_null = null_count / (len(data)) * 100
    null_perc_notnull = 100 - null_perc_null
    null_perc = pd.DataFrame(index=['% Null', '% Not Null'], data=[null_perc_null, null_perc_notnull], columns=[col]).T
    return null_perc


# Variables conversion
def col_to_datetime(data: pd.DataFrame, col: str):
    return data[col].apply(pd.to_datetime, infer_datetime_format=True)

def datetimecol_split(data: pd.DataFrame, col: str):
    years = pd.DatetimeIndex(data[col]).year
    months = pd.DatetimeIndex(data[col]).month
    days = pd.DatetimeIndex(data[col]).day


# RELATIONSHIP WITH THE TARGET
def vartargetdistribution(df, var, target, config: dict, bins=50, ax=None, title=None):
    with plt.style.context('ggplot'):
        df[var][df[target] == 0].hist(bins=bins, color="slategray", label='Default', alpha=0.7, ax=ax)
        df[var][df[target] == 1].hist(bins=bins, label=config['automatic_eda']['target_colname'], alpha=0.9, ax=ax)
        if title != None:
            plt.title(title)
        else:
            plt.title(var)
        plt.legend()
        return plt.show()


def boxplot_target(df: pd.DataFrame, col_target: str, col_name: str, dict_var: dict, figsize=(15, 5)):
    with plt.style.context('ggplot'):
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(dict_var[col_name] + ' - ' + col_name, fontsize=16, y=1)
        sns.boxplot(data=df[df[col_target] == 1], x=col_name, color="slategray", ax=axes[0])
        axes[0].set_xlabel(None)
        axes[0].set_title("Target 1")
        sns.boxplot(data=df[df[col_target] == 0], x=col_name, color="slategray", ax=axes[1])
        axes[1].set_xlabel(None)
        axes[1].set_title("Target 0")
        return plt.show()

# VISUALIZATION
def missing_bars(data, dict_var, figsize=(10, 10), style='ggplot', dicc=True):
    with plt.style.context(style):
        null_count = data.isnull().sum()
        null_perc_null = null_count.div(len(data))
        null_perc_notnull = 1 - null_perc_null
        null_perc = pd.DataFrame({'% Null': null_perc_null,
                                  '% Not Null': null_perc_notnull})
        if dicc:
            null_perc.reset_index(inplace=True)
            null_perc['index'].replace(dict_var, inplace=True)
            null_perc.set_index('index', drop=True, inplace=True)

        ax = null_perc.plot(kind='barh', figsize=(figsize),
                            stacked=True,
                            title='% Missings per column', grid=False)
        sns.despine(right=True, top=True, bottom=True)
        ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1), frameon=False);

        for p in ax.patches:
            width = p.get_width()
            if width > 0.03:  # original width > 0.10
                x = p.get_x()
                y = p.get_y()
                height = p.get_height()
                ax.text(x + width / 2., y + height / 2., str(round((width) * 100, 1)) + '%',  # original round = 2
                        fontsize=10, va="center", ha='center', color='white', fontweight='bold')
        config = load_config()
        filename = config['data']['filename'].rsplit('.', 1)[0]
        plt.savefig(config['data']['path'] + 'output\\' + filename + '_missing.png')


## SAVE AND LOAD PICKLE
def save_pickle(filename: str, mydict: dict):
    with open(filename, 'wb') as handle:
        pickle.dump(mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(filename: str):
    with open(filename, 'rb') as handle:
        return pickle.load(handle)