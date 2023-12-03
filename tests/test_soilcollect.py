from contextlib import nullcontext as does_not_raise
import pytest
from soilstats.soilcollect import SoilCollect

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


