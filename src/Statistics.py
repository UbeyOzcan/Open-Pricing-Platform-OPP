import pandas as pd
from typing import List

class Stat:
    def __init__(self, df:pd.DataFrame):
        self.df = df

    def response_dist(self, y:str, model:str) -> pd.DataFrame:
        out = self.df.groupby(y).agg({y : 'count'}).rename(columns={y : 'count'})
        return out