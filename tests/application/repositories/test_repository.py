from mediark.application.repositories.repository import Repository


def test_repository_methods() -> None:
    methods = Repository.__abstractmethods__  # type: ignore
    assert 'get' in methods
    assert 'add' in methods
    assert 'search' in methods
    assert 'remove' in methods
