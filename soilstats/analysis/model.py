import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri


class Model:
    """Model class for analysis."""
    def __init__(self,
                 formula: str,
                 data: pd.DataFrame):
        """Model class for analysis.

        Args:
            formula (str): model formula
            data (pd.DataFrame): data for analysis
        """
        self.formula = formula
        self.data = data
        self._stats = self._run()

    def _run(self):
        """Run the model."""
        with open('soilstats/analysis/regression.R', 'r') as f:
            ro.r(f.read())
            r_reg = ro.r['regression']
        with (ro.default_converter + pandas2ri.converter).context():
            df_r = ro.conversion.get_conversion().py2rpy(self.data)
            stats = r_reg(df_r, self.formula)
        self._rsquared = stats["rsquared"][0]
        self._intercept = stats["intercept"][0]
        self._slope = stats["slope"][0]

    @property
    def stats(self):
        """Return model statistics."""
        return {
            "r_squared": self._rsquared,
            "intercept": self._intercept,
            "slope": self._slope
        }
