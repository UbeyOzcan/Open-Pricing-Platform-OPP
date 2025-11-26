import pandas as pd
from typing import List
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.figure_factory import create_distplot
from scipy.stats import gamma, lognorm

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

    def plot_univariate(self, df:pd.DataFrame, x:str, metric:str, exposure:List[str]) -> object:
        exp = exposure[1] if metric == 'Severity' else exposure[0]

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df[x], y=df[metric], name=metric, mode="lines"),
            secondary_y=True
        )

        fig.add_trace(
            go.Bar(x=df[x], y=df[exp], name=exp),
            secondary_y=False
        )

        fig.update_xaxes(title_text=x)

        # Set y-axes titles
        fig.update_yaxes(title_text=exp, secondary_y=False)
        fig.update_yaxes(title_text=metric, secondary_y=True)
        return fig

    def plot_density(self, x:list) -> object:
        x = np.log(x)
        group_labels = ['distplot example']
        fig = create_distplot([x], group_labels, show_hist=False, show_rug=False)
        return fig

    def fit_gamma(self, x) -> dict:
        shape, loc, scale = gamma.fit(x)
        return {"shape" : shape, "loc" : loc, "scale" : scale}

    def fit_lognormal(self, x) -> dict:
        s, loc, scale = lognorm.fit(x)
        return {"s" : s, "loc" : loc, "scale" : scale}

    def simulate_gamma(self, params:list):
        num = np.random.gamma(shape=params["shape"], scale=params["scale"], size=1000)
        return np.log(num)

    def simulate_lognormal(self, params:list):
        num = np.random.lognormal(mean=np.log(params["scale"]), sigma=params["s"], size=1000)
        return np.log(num)
