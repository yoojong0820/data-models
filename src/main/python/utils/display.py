import numpy as np
import pandas as pd


def pandas_df_display_setting():
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 100)
    pd.set_option('display.width', 1500)
    pd.set_option('display.max_colwidth', 500)


def numpy_array_display_setting():
    np.set_printoptions(
        edgeitems=30,
        linewidth=100000,
        formatter=dict(float=lambda x: "%.3g" % x)
    )
