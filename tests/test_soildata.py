from contextlib import nullcontext as does_not_raise
import pandas as pd
import pytest
from soilstats.soildata import SoilData

# ruff: noqa: D101, D102

class TestSoilData:
    @pytest.mark.parametrize("args, lat_expect, value_expect, error", [
    ([50,10,"clay", "0-30cm", "mean"], 50, ["mean"], does_not_raise()),
    ([50,10,"clay", "0-30cm", ["mean"]], 50, ["mean"], does_not_raise()),
    ([50,250,"clay", "0-30cm", ["mean"]], None, ["mean"], pytest.raises(ValueError)),
    ([-100,10,"clay", "0-30cm", ["mean"]], None, ["mean"], pytest.raises(ValueError)),
    ([50,"text","clay", "0-30cm", ["mean"]], None, ["mean"], pytest.raises(TypeError)),
])
    def test_constructor(self, args, lat_expect, value_expect, error):
        lat, lon, properties, depths, values = args
        with error:
            sd = SoilData(
                lat=lat,
                lon=lon,
                properties=properties,
                depths=depths,
                values=values
            )
            assert sd.lat == lat_expect
            assert sd.values == value_expect

    def test_get_data(self): #TODO: monkeypatch the test instead of calling the API
        sd = SoilData(
            lat=50,
            lon=10,
            properties="clay",
            depths="0-5cm",
            values="mean"
        )
        df = sd.get_data()
        assert isinstance(df, pd.DataFrame)

    def test_clean_data(self):  #TODO: monkeypatch the test instead of calling the API
        sd = SoilData(lat = 56.225297,
                lon = 8.662215,
                properties=['clay', 'sand', 'silt', "nitrogen"],
                depths=["0-5cm", "0-30cm", "5-15cm", "60-100cm"],
                values="mean")
        df = sd.get_data()
        assert "units" in df.columns
        assert "depth" in df.columns
        assert list(df.columns[:3]) == ["lat", "lon", "property"]

    def test_empty_data(self):  #TODO: monkeypatch the test instead of calling the API
        sd = SoilData(lat = 56.225297,
                lon = 8.662215,
                properties='clay',
                depths='0-30cm',
                values="mean")
        df = sd.get_data()
        assert df.empty








