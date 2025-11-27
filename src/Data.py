import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class Analyzer:
    def __init__(self,df:pd.DataFrame):
        self.df = df

    def univariate(self, x:str, y:str, exposure:str) -> pd.DataFrame:
        univariate = self.df.groupby(x).agg({y : 'sum',
                                             exposure : 'sum'})
        univariate = univariate.reset_index()
        return univariate

    def get_vars(self, y:str, exposure:str) -> list:
        ls = [y, exposure]
        ls = list(set(ls))
        cols = self.df.columns.tolist()
        cols = list(filter(lambda item: item not in ls, cols))
        return cols

    def calc_resp(self, df:pd.DataFrame, y:str, exposure:str, model_name:str) -> pd.DataFrame:
        df[model_name] = np.where(df[exposure].sum() == 0, 0, df[y]/df[exposure])
        return df

    def plot_univariate(self, df:pd.DataFrame, x:str, exposure:str, model_name:str) -> object:

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df[x], y=df[model_name], name=model_name, mode="lines"),
            secondary_y=True
        )

        fig.add_trace(
            go.Bar(x=df[x], y=df[exposure], name=exposure),
            secondary_y=False
        )

        fig.update_xaxes(title_text=x)

        # Set y-axes titles
        fig.update_yaxes(title_text=exposure, secondary_y=False)
        fig.update_yaxes(title_text=model_name, secondary_y=True)
        return fig
