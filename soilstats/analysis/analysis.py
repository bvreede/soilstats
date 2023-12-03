class Analyse:
    """Mixin class with analysis methods for soil data."""

    @property
    def df(self):
        """Data from the SoilGrids API as a pandas DataFrame."""
        return self.get_data()

    def get_data(self):
        """Return data from the SoilGrids API as a data frame."""
        return NotImplemented

    def regression(self):
        """Perform regression analysis."""
        return NotImplemented

    def summary(self):
        """Return summary statistics."""
        self.df
