import pandas as pd


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
        # call regression.R and return results
        return NotImplemented

    @property
    def stats(self):
        """Return model statistics."""
        # process stats to dictionary
        return self._stats
