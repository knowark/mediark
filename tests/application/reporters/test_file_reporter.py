from mediark.application.reporters import FileReporter


def test_file_reporter_instantiation(file_reporter):
    assert isinstance(file_reporter, FileReporter)


async def test_file_reporter_load(file_reporter):
    uri = 'images/abcd1234.jpg'
    result = await file_reporter.load(uri)
    assert isinstance(result, dict)
    assert result == {'body': b''}


# async def test_mediark_reporter_search_audios(mediark_reporter):
#     result = await mediark_reporter.search_audios([])
#     assert len(result) == 2
