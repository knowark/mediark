from mediark.application.domain.services import Token


def test_token_creation() -> None:
    value = "X8tnyt7"

    token = Token(value=value)

    assert token.value == value
    assert isinstance(token.value, str)