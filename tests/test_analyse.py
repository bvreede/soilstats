import json
import pandas as pd
import pytest

# ruff: noqa: D101, D102

class TestAnalyse():
    @pytest.fixture
    def patched_sc(self, sc, monkeypatch):
        def jsondata(sc):
            with open("tests/data/large.json") as f:
                return json.load(f)

        monkeypatch.setattr("soilstats.soilgrids.SoilGrids.get", jsondata)
        sc.get_data()
        yield sc

    def test_df(self, patched_sc):
        assert isinstance(patched_sc.df, pd.DataFrame)
        assert patched_sc.df.shape == (120, 9)

    def test_top_property(self, patched_sc):
        top = patched_sc.top_property()
        assert isinstance(top, pd.DataFrame)
        assert top.shape == (20, 5)
        assert top.columns.tolist() == ['lat', 'lon', 'units', 'property', 'values.mean']
