from soilstats.soilgrids import SoilGrids

# ruff: noqa: D101, D102

class TestSoilGrids:
    def test_constructor(self):
        sg = SoilGrids(lat=56, lon=9,
                       properties=["clay", "ocs", "sand", "silt"],
                       depths=["0-30cm"],
                       values=["mean"])
        assert sg.lat == 56
        assert sg.values == ["mean"]

    def test_url(self):
        sg = SoilGrids(lat=56, lon=9,
                       properties=["clay", "ocs", "sand", "silt"],
                       depths=["0-30cm"],
                       values=["mean"])
        assert sg.url == "https://rest.isric.org/soilgrids/v2.0/properties/query?lon=9&lat=56&property=clay&property=ocs&property=sand&property=silt&depth=0-30cm&value=mean"

    # def test_get(self):
    #    lat = 56
    #    lon = 9
    #    sg = SoilGrids(lat, lon,
    #                   properties=["clay", "ocs", "sand", "silt"],
    #                   depths=["0-30cm"],
    #                   values=["mean"])
    #    response = sg.get()
    #    assert response["geometry"]["coordinates"] == [lon, lat]
    #    assert isinstance(response["properties"]["layers"], list)

