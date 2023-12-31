import time
import requests


class SoilGrids:
    """Connection to SoilGrids API."""
    api = "https://rest.isric.org/soilgrids/"
    api_version = "v2.0"
    db = ["properties", "query"]

    def __init__(self,
                 lat: float,
                 lon: float,
                 properties: list,
                 depths: list,
                 values: list):
        """Initialize an API request to SoilGrids.

        Args:
            lat (float): latitude
            lon (float): longitude
            properties (list): list of soil properties to query
            depths (list): list of soil depths to query
            values (list): list of values to query
        """
        self.lat = lat
        self.lon = lon
        self.properties = properties
        self.depths = depths
        self.values = values

    def get(self):
        """Get json data from SoilGrids API."""
        response_code = 429
        # always add a short delay to avoid overloading the API
        time.sleep(15)
        while response_code == 429:
            response = requests.get(self.url)
            response_code = response.status_code
            if response_code == 429:
                time.sleep(30)
        if response.status_code == 200:
            return requests.get(self.url).json()
        else:
            raise ValueError(f"The SoilGrids API call failed with status code {response.status_code}")

    @property
    def url(self):
        """Return URL for SoilGrids API given a specific request."""
        properties = "&".join([f"property={p}" for p in self.properties])
        depths = "&".join([f"depth={d}" for d in self.depths])
        values = "&".join([f"value={v}" for v in self.values])
        return f"{self.api_url}lon={self.lon}&lat={self.lat}&{properties}&{depths}&{values}"

    @property
    def api_url(self):
        """Return URL for SoilGrids API database and version."""
        dbjoined = '/'.join(self.db)
        return f"{self.api}{self.api_version}/{dbjoined}?"


