import pandas as pd


def pandas_df_display_setting():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 1500)
    pd.set_option('display.max_colwidth', 500)
