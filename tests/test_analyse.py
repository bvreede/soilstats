import json
import pandas as pd
from soilstats.soilcollect import SoilCollect

# ruff: noqa: D101, D102

class TestAnalyse:
    def test_top_property(self, monkeypatch):
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

        assert isinstance(sc.df, pd.DataFrame)

        top = sc.top_property()
        assert isinstance(top, pd.DataFrame)
        assert top.shape == (20, 5)
        assert top.columns.tolist() == ['lat', 'lon', 'units', 'property', 'values.mean']
