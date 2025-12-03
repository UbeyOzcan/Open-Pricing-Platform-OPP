import pandas as pd
import numpy as np

class GLMHandler:
    def __init__(self, model):
        self.model = model

    def params_tab(self):
        df_params = pd.DataFrame(self.model.params).reset_index().rename(
            columns={'index': 'Variable', 0: 'Beta'})
        df_params_exp = pd.DataFrame(np.exp(self.model.params)).reset_index().rename(
            columns={'index': 'Variable', 0: 'Exp(Beta)'})
        df_pvalues = pd.DataFrame(round(self.model.pvalues, 4)).reset_index().rename(
            columns={'index': 'Variable', 0: 'P-Value'})

        df_summary_params = pd.merge(df_params, df_params_exp, on='Variable')
        df_summary_params = pd.merge(df_summary_params, df_pvalues, on='Variable')

        return df_summary_params

    def deviance_reduction(self):
        pass

    def residual_plot(self):
        pass

    def aic_bic_tab(self):
        pass

    def estimates_std(self):
        pass

    def fitted_obs_var_plot(self, var:str):
        pass

    def impact_plot_ref_model(self):
        pass

    def impact_plot_models(self):
        pass