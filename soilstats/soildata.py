import pandas as pd
from .soilgrids import SoilGrids


class SoilData:
    """Class for collecting and analyzing soil data."""

    _property_key = "properties"
    _layer_key = "layers"
    _record_path = ["depths"]
    _meta = ["name", ["unit_measure", "mapped_units"]]

    _boundaries = {
        "lat": (-90, 90),
        "lon": (-180, 180)
    }

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

    def set_boundaries(self):
        """Set boundaries for soil data collection."""
        return NotImplemented

    def get_data(self):
        """Get soil data from the SoilGrids API and return a data frame."""
        sg = SoilGrids(self.lat, self.lon,
                       properties=self.properties,
                       depths=self.depths,
                       values=self.values)
        # for verification purposes, the URL is stored as an attribute
        self.url = sg.url

        response = sg.get().json()
        layers = response[self._property_key][self._layer_key]
        return pd.json_normalize(layers,
                                 record_path=self._record_path,
                                 meta=self._meta)

    def analyze(self):
        """Analyze soil data."""
        return NotImplemented

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
