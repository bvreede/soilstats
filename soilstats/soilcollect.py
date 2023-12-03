import random
import pandas as pd
from .soildata import SoilData


class SoilCollect:
    """Class for collecting soil data for multiple locations within a grid."""

    def __init__(self, properties, depths, values, lat_bounds, lon_bounds, n = 50):
        """Set up SoilGrids data query for multiple points within an area.

        For available properties, depths, and values to return:
        consult the SoilGrids API documentation
        (https://rest.isric.org/soilgrids/v2.0/docs#/default/query_layer_properties_properties_query_get).

        Args:
            properties (str or list): soil properties to query; e.g. ["clay", "sand"]
            depths (str or list): depth range(s); e.g. ["0-5cm", "0-30cm"]
            values (str or list): values to return; e.g. "mean"
            lat_bounds (list[floats]): boundaries for latitude; e.g. [50, 55]
            lon_bounds (list[floats]): boundaries for longitude; e.g. [10, 15]
            n (int, optional): number of locations to sample within the boundaries. Defaults to 50.
        """
        self._properties = properties
        self._depths = depths
        self._values = values

        self._locations = self._random_points(lat_bounds, lon_bounds, n)
        self._sdpoints = self._init_soildata()

    def get_data(self):
        """Return data from the SoilGrids API as a data frame."""
        dfs = [sd.get_data() for sd in self._sdpoints]
        return pd.concat(dfs, ignore_index=True)

    def _init_soildata(self):
        """Initialize SoilData objects for each location."""
        return [SoilData(lat, lon,
                         properties=self._properties,
                         depths=self._depths,
                         values=self._values) for lat, lon in self._locations]

    @property
    def locations(self):
        """Return locations."""
        return self._locations

    @property
    def soildatapoints(self):
        """Return SoilData objects."""
        return self._sdpoints

    @classmethod
    def _random_points(cls, lat_bounds, lon_bounds, n):
        """Generate random locations within the specified boundaries."""
        min_lat, max_lat = cls._verify_bounds(lat_bounds, "lat")
        min_lon, max_lon = cls._verify_bounds(lon_bounds, "lon")
        lats = [random.uniform(min_lat, max_lat) for _ in range(n)]
        lons = [random.uniform(min_lon, max_lon) for _ in range(n)]
        return list(zip(lats, lons))

    @classmethod
    def _verify_bounds(cls, bounds, datatype):
        #TODO boundaries should also work on spherical earth!
        if len(bounds) != 2:
            raise IndexError(f"{datatype}_bounds requires 2 values, got {len(bounds)}")
        minvalue = SoilData._verify(min(bounds), datatype)
        maxvalue = SoilData._verify(max(bounds), datatype)
        return minvalue, maxvalue









