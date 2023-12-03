import warnings
import pandas as pd
from .soilgrids import SoilGrids


class SoilData:
    """Class for collecting and analyzing soil data."""

    # keys to select the appropriate data from the API response
    _property_key = "properties"
    _layer_key = "layers"
    _record_path = ["depths"]
    _meta = ["name", ["unit_measure", "mapped_units"]]

    # geo boundaries for verification
    _boundaries = {
        "lat": (-90, 90),
        "lon": (-180, 180)
    }

    # used in _clean_data to rename columns
    _clean_columns = {
        "label": "depth",
        "name": "property",
        "unit_measure.mapped_units": "units"
    }

    # used in _clean_data to reorder columns
    _first_columns = ["lat", "lon", "property"]

    def __init__(self,
                 lat: float,
                 lon: float,
                 properties: list,
                 depths: list,
                 values: list):
        """Initialize class."""
        self.lat = self._verify(lat, "lat")
        self.lon = self._verify(lon, "lon")
        self.properties = self._enlist(properties)
        self.depths = self._enlist(depths)
        self.values = self._enlist(values)

        # set up soilgrid object and store the URL for verification purposes
        self._sg = self._setup_soilgrid()
        self.url = self._sg.url

    def get_data(self):
        """Return data from the SoilGrids API as a data frame."""
        if not hasattr(self, "_df"):
            self._get_data()
        if self._df.empty:
            line1 = f"No data found for ({self.lat}, {self.lon})"
            line2 = f"with properties = {self.properties}, depths = {self.depths}, values = {self.values}."
            line3 = f"Verify the URL: {self.url}"
            warnings.warn(f"{line1} {line2}\n{line3}")
        return self._df

    def _get_data(self):
        """Get data from the SoilGrids API.

        Use the properties to call the SoilGrids API.
        Generate a data frame fom the API response.
        """
        response = self._sg.get()
        layers = response[self._property_key][self._layer_key]
        self._df = pd.json_normalize(layers,
                                 record_path=self._record_path,
                                 meta=self._meta)
        self._clean_data()

    def _clean_data(self):
        """Clean up the data frame.

        - rename obscurely named columns
        - add latitude and longitude
        - reorder columns to increase readability
        """
        self._df.rename(columns=self._clean_columns, inplace=True)
        if not self._df.empty:
            self._df['lat']=self.lat
            self._df['lon']=self.lon
        for col in self._first_columns[::-1]:
            try:
                self._df.insert(0, col, self._df.pop(col))
            except KeyError:
                continue

    def _setup_soilgrid(self):
        """Initialize SoilGrids object."""
        return SoilGrids(self.lat, self.lon,
                properties=self.properties,
                depths=self.depths,
                values=self.values)

    @classmethod
    def _verify(cls, value, datatype):
        """Verify that latitude/longitude are within boundaries."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{datatype} must be numeric")
        left, right = cls._boundaries[datatype]
        if not left <= value <= right:
            raise ValueError(f"{datatype} must be between {left} and {right}")
        return value

    @classmethod
    def _enlist(cls, value):
        """Enlist value if it is not a list."""
        return value if isinstance(value, list) else [value]
