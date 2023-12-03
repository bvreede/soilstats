class Analyse:
    """Mixin class with analysis methods for soil data."""
    # column names used in the analysis
    _grouping = ["lat", "lon", "units"]
    _valuename = "values."
    _propertyname = "property"

    @property
    def df(self):
        """Data from the SoilGrids API as a pandas DataFrame."""
        return self.get_data()

    def get_data(self):
        """Return data from the SoilGrids API as a data frame."""
        return NotImplemented

    def top_property(self, properties = None, value = "mean"):
        """Return dataframe with the highest values for each location."""
        if properties is None:
            properties = self.properties

        valuecol = f"{self._valuename}{value}"
        df = self._select_content(self.df, self._propertyname, properties)
        df = self._numeric_and_remove_nans(df, valuecol)

        max_indices = df.groupby(self._grouping)[valuecol].idxmax(skipna=True)
        columns = self._grouping + [self._propertyname, valuecol]

        return df.loc[max_indices, columns].reset_index(drop=True)

    @classmethod
    def _numeric_and_remove_nans(cls, df, col):
        """Convert specific column to numeric and remove NaNs."""
        df[col] = df[col].astype(float)
        df.dropna(subset=[col], inplace=True)
        return df

    @classmethod
    def _select_content(cls, df, col, content):
        """Select rows with specific content in a column."""
        return df[df[col].isin(content)]

    def regression(self):
        """Perform regression analysis."""
        return NotImplemented

    def summary(self):
        """Return summary statistics."""
        self.df
