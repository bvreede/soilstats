from .model import Model


class Analyse:
    """Mixin class with analysis methods for soil data."""
    # column names used in the analysis
    _grouping = ["lat", "lon", "units"] # standard grouping for all methods
    _valuename = "values." # e.g. "values.mean"
    _propertyname = "property"
    _depthname = "depth"

    @property
    def df(self):
        """Data from the SoilGrids API as a pandas DataFrame."""
        return self.get_data()

    def get_data(self):
        """Return data from the SoilGrids API as a data frame."""
        return NotImplemented

    def top_property(self, properties = None, value = "mean"):
        """Return dataframe with the highest scoring properties for each coordinate."""
        properties = self.properties if properties is None else properties
        valuecol = f"{self._valuename}{value}"

        df = self._select_content(self.df, self._propertyname, properties)
        df = self._numeric_and_remove_nans(df, valuecol)

        max_indices = df.groupby(self._grouping)[valuecol].idxmax(skipna=True)
        columns = self._grouping + [self._propertyname, valuecol]

        return df.loc[max_indices, columns].reset_index(drop=True)


    def max_values(self, properties = None, value = "mean"):
        """Return a dataframe with the highest values per property for each coordinate.

        Given multiple depths in the data frame, this method will return the highest value for each location.

        Args:
            properties (list, optional): properties to include. Defaults to None, which includes all properties.
            value (str, optional): value to consider. Defaults to "mean".
        """
        properties = self.properties if properties is None else properties
        valuecol = f"{self._valuename}{value}"

        df = self._select_content(self.df, self._propertyname, properties)
        df = self._numeric_and_remove_nans(df, valuecol)

        grouping = self._grouping + [self._propertyname]

        max_indices = df.groupby(grouping)[valuecol].idxmax(skipna=True)
        columns = self._grouping + [self._propertyname, self._depthname, valuecol]

        return df.loc[max_indices, columns].reset_index(drop=True)

    def mean_values(self, properties = None, value = "mean"):
        """Return a dataframe with the average values per property for each coordinate.

        Given multiple depths in the data frame, this method will return averages for each location.

        Args:
            properties (list, optional): properties to include. Defaults to None, which includes all properties.
            value (str, optional): value to consider. Defaults to "mean".
        """
        properties = self.properties if properties is None else properties
        valuecol = f"{self._valuename}{value}"

        df = self._select_content(self.df, self._propertyname, properties)
        df = self._numeric_and_remove_nans(df, valuecol)

        grouping = self._grouping + [self._propertyname]

        return df.groupby(grouping).agg({valuecol: "mean"}).reset_index()

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

    def regression(self, formula):
        """Perform regression analysis."""
        df = self._pivot_for_model(self.df)
        return Model(formula = formula, data = df)

    def summary(self):
        """Return summary statistics."""
        return NotImplemented

    @classmethod
    def _pivot_for_model(cls, df):
        """Perform a pivot on the data frame to prepare for regression analysis."""
        # TODO remove hardcoded variable names
        pivot = (df.groupby(['lat', 'lon', 'property'])
                .agg(value=('values.mean', 'max'))
                .pivot_table(index=['lat', 'lon'], columns='property', values='value')
        .reset_index())
        properties = df['property'].unique()
        for property in properties:
            pivot = cls._numeric_and_remove_nans(pivot, property)
        return pivot
