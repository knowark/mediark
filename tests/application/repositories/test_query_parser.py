from pytest import fixture
from unittest.mock import Mock
from mediark.application.utilities.query_parser import QueryParser


@fixture
def parser() -> QueryParser:
    return QueryParser()


def test_expression_parser_object_creation(parser):
    assert isinstance(parser, QueryParser)


def test_expression_parser_parse_tuple(parser):
    filter_tuple_list = [
        (('field', '=', 9), lambda obj: obj.field == 9, Mock(field=9)),
        (('field', '!=', 9), lambda obj: obj.field != 9, Mock(field=8)),
        (('field', '>', 9), lambda obj: obj.field > 9, Mock(field=10)),
        (('field', '<', 9), lambda obj: obj.field < 9, Mock(field=8)),
        (('field', '<=', 9), lambda obj: obj.field <= 9, Mock(field=8)),
        (('field', '>=', 9), lambda obj: obj.field >= 9, Mock(field=10)),
        (('field', 'in', [1, 2, 3]), lambda obj: obj.field in [1, 2, 3],
         Mock(field=2)),
    ]

    for test_tuple in filter_tuple_list:
        filter_tuple = test_tuple[0]
        expected_function = test_tuple[1]
        mock_object = test_tuple[2]

        function = parser._parse_term(filter_tuple)

        assert callable(function) is True
        assert function(mock_object) is True
        assert function(mock_object) == expected_function(mock_object)


def test_expression_parser_parse_single_term(parser):
    domain = [('field', '=', 7)]

    def expected(obj):
        return getattr(obj, 'field') == 7

    mock_object = Mock()
    mock_object.field = 7

    function = parser.parse(domain)

    assert callable(function) is True
    assert function(mock_object) is True
    assert function(mock_object) == expected(mock_object)

    mock_object.field = 5
    assert function(mock_object) is False


def test_expression_parser_default_join(parser):
    stack = [lambda obj: obj.field2 != 8, lambda obj: obj.field == 7]

    def expected(obj):
        return (obj.field == 7 and obj.field2 != 8)

    result_stack = parser._default_join(stack)

    mock_object = Mock()
    mock_object.field = 7
    mock_object.field2 = 9

    assert isinstance(result_stack, list) is True
    assert result_stack[0](mock_object) == expected(mock_object)
    assert result_stack[0](mock_object) is True

    mock_object.field = 5
    assert result_stack[0](mock_object) is False


def test_query_parser_parse_multiple_terms(parser):
    test_domains = [
        ([('field', '=', 7), ('field2', '!=', 8)],
            lambda obj: (obj.field2 != 8 and obj.field == 7),
            Mock(field=7, field2=8)),
        ([('field', '=', 7), ('field2', '!=', 8), ('field3', '>=', 9)],
            (lambda obj: (obj.field2 != 8 and
                          obj.field == 7 and obj.field3 >= 9)),
            Mock(field=7, field2=5, field3=9)),
        (['|', ('field', '=', 7), ('field2', '!=', 8)],
            lambda obj: (obj.field2 != 8 or obj.field == 7),
            Mock(field=7, field2=8)),
        (['|', ('field', '=', 7), '!', ('field2', '!=', 8),
            ('field3', '>=', 9)],
            (lambda obj: (obj.field == 7 or
                          not obj.field2 != 8 and obj.field3 >= 9)),
            Mock(field=7, field2=8, field3=9)),
        (['!', ('field', '=', 7)],
            lambda obj: (not obj.field == 7),
            Mock(field=7)),
    ]

    for test_domain in test_domains:
        result = parser.parse(test_domain[0])
        expected = test_domain[1]
        obj = test_domain[2]
        assert callable(result) is True
        assert result(obj) == expected(obj)


def test_expression_parser_with_empty_list(parser):
    domain = []
    result = parser.parse(domain)
    mock_object = Mock()
    mock_object.field = 7
    assert result(mock_object) is True


def test_string_parser_with_lists_of_lists(parser):
    domain = [['field', '=', 7], ['field2', '!=', 8]]

    def expected(obj):
        return (obj.field == 7 and obj.field2 != 8)

    result = parser.parse(domain)

    mock_object = Mock()
    mock_object.field = 7
    mock_object.field2 = 9

    assert result(mock_object) is True
    assert result(mock_object) == expected(mock_object)
