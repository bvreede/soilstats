import pytest
from soilstats.soildata import SoilData


@pytest.fixture
def sd_large() -> SoilData:
    """SoilData object with large data set."""
    return SoilData(lat = 56.225297,
            lon = 8.662215,
            properties=['clay', 'sand', 'silt', "nitrogen"],
            depths=["0-5cm", "0-30cm", "5-15cm", "60-100cm"],
            values="mean")

@pytest.fixture
def sd_empty() -> SoilData:
    """SoilData object with empty data set."""
    return SoilData(lat = 56.225297,
                    lon = 8.662215,
                    properties='clay',
                    depths='0-30cm',
                    values="mean")

