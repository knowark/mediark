from mediark.application.services import IdService, StandardIdService


def test_id_service() -> None:
    methods = IdService.__abstractmethods__  # type: ignore
    assert 'generate_id' in methods


def test_memory_id_service_implementation() -> None:
    assert issubclass(StandardIdService, IdService)


def test_memory_id_service_generate_id() -> None:
    id_service = StandardIdService()
    result = id_service.generate_id()

    assert isinstance(result, str)
    assert len(result) == 36
