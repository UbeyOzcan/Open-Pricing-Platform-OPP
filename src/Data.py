import pandas as pd
from typing import List
import numpy as np

class Analyzer:
    def __init__(self,df:pd.DataFrame):
        self.df = df

    def univariate(self, x:str, y:List[str], exposure:List[str]) -> pd.DataFrame:
        univariate = self.df.groupby(x).agg({y[0] : 'sum',
                                             exposure[0] : 'sum',
                                             y[1] : 'sum',
                                             exposure[1] : 'sum'})
        univariate = univariate.reset_index()
        return univariate

    def get_vars(self, y:List[str], exposure:List[str]) -> list:
        ls = [*y, *exposure]
        ls = list(set(ls))
        cols = self.df.columns.tolist()
        cols = list(filter(lambda item: item not in ls, cols))
        return cols

    def calc_freq_sev(self, df:pd.DataFrame, y:List[str], exposure:List[str]) -> pd.DataFrame:
        df['Frequency'] = df[y[0]]/df[exposure[0]]
        df['Severity'] = np.where(df[exposure[1]].sum() == 0, 0, df[y[1]]/df[exposure[1]])
        df['Risk Premium'] = df['Frequency'] * df['Severity']
        return df