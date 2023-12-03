import json
from contextlib import nullcontext as does_not_raise
import pandas as pd
import pytest
from soilstats.soildata import SoilData

# ruff: noqa: D101, D102

class TestSoilData:
    @pytest.mark.parametrize("args, lat_expect, value_expect, error", [
    ([50,10, "mean"], 50, ["mean"], does_not_raise()),
    ([50,10, ["mean"]], 50, ["mean"], does_not_raise()),
    ([50,250, ["mean"]], None, ["mean"], pytest.raises(ValueError)),
    ([-100,10, ["mean"]], None, ["mean"], pytest.raises(ValueError)),
    ([50,"text", ["mean"]], None, ["mean"], pytest.raises(TypeError)),
])
    def test_constructor(self, args, lat_expect, value_expect, error):
        lat, lon, values = args
        with error:
            sd = SoilData(
                lat=lat,
                lon=lon,
                properties="clay",
                depths="0-30cm",
                values=values
            )
            assert sd.lat == lat_expect
            assert sd.values == value_expect

    def test_get_data(self, sd_large): #TODO: monkeypatch the test instead of calling the API
        df = sd_large.get_data()
        assert isinstance(df, pd.DataFrame)

        # check cleaning functionality
        assert "units" in df.columns
        assert "depth" in df.columns
        assert list(df.columns[:3]) == ["lat", "lon", "property"]

    def test_empty_data(self, sd_empty, monkeypatch):
        def empty_json(sd_empty):
            with open("tests/data/empty.json") as f:
                return json.load(f)

        monkeypatch.setattr("soilstats.soilgrids.SoilGrids.get", empty_json)

        with pytest.warns(match = "No data found"):
            df = sd_empty.get_data()
        assert df.empty

