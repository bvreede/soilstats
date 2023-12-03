from contextlib import nullcontext as does_not_raise
import pandas as pd
import pytest
from soilstats.soilcollect import SoilCollect
import json

# ruff: noqa: D101, D102

class TestSoilCollect:

    @pytest.mark.parametrize("lat_bounds, n, error", [
    ([50, 55], 10, does_not_raise()),
    ([0, 90], 10, does_not_raise()),
    ([50,250], 10, pytest.raises(ValueError)),
    ([1], 1, pytest.raises(IndexError)),
    ])
    def test_constructor(self, lat_bounds, n, error):
        with error:
            sc = SoilCollect(properties=["clay", "ocs", "sand", "silt"],
                             depths=["0-30cm"],
                             values=["mean"],
                            lat_bounds=lat_bounds,
                            lon_bounds=[10, 15],
                            n=n)
            assert len(sc.locations) == n
            assert len(sc.locations[0]) == 2


    def test_get_data(self, sd_large, monkeypatch):
        def large_json(sd_large):
            with open("tests/data/large.json") as f:
                return json.load(f)

        monkeypatch.setattr("soilstats.soilgrids.SoilGrids.get", large_json)

        sc = SoilCollect(properties=['clay', 'sand', 'silt', "nitrogen"],
                         depths=["0-5cm", "0-30cm", "5-15cm", "60-100cm"],
                         values="mean",
                         lat_bounds=[55, 57],
                         lon_bounds=[8, 10],
                         n=10)

        df = sc.get_data()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (120, 9)
