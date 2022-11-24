from nhtsa_ciss_python.scene_diagram import BlitzReader


def test_metadata():

    reader = BlitzReader("tests/20201010130.blz")

    meta = reader.read_metadata()

    assert isinstance(meta, dict)


def test_gosmodels():

    reader = BlitzReader("tests/20201010130.blz")

    models = reader.get_vehicles()

    assert isinstance(models, list)
