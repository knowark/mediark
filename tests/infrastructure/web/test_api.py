from json import loads
from flask import Flask


def test_api_images_search(app: Flask) -> None:
    response = app.get('/images?filter=[["reference", "=", "ABC"]]')
    data = str(response.data, 'utf-8')
    data_dict = loads(data)
    assert data
    assert len(data_dict) == 1


def test_api_audios_search(app: Flask) -> None:
    response = app.get('/audios?filter=[["reference", "=", "XYZ"]]')
    data = str(response.data, 'utf-8')
    data_dict = loads(data)
    assert data
    assert len(data_dict) == 1
