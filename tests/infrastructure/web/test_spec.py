from pytest import fixture
from apispec import APISpec
from mediark.infrastructure.web.spec import create_spec, ResourcePlugin


@fixture
def spec():
    spec = create_spec()
    return spec


@fixture
def resource():

    class MockResource:

        async def get(self):
            """
            ---
            summary: Return all items.
            tags:
            - Items
            responses:
            200:
                description: "Successful response"
                content:
                application/json:
                    schema:
                    type: array
                    items:
                        $ref: '#/components/schemas/Item'
            """

        def post(self):
            """
            No Operation. Comment Only.
            """

    return MockResource()


def test_spec(spec):
    assert spec is not None
    assert isinstance(spec, APISpec)


def test_spec_resource_plugin_path_helper(spec, resource):
    plugin = ResourcePlugin()
    plugin.init_spec(spec)

    operations = {}
    plugin.path_helper('/resource', operations=operations, resource=resource)

    assert 'get' in operations


def test_spec_resource_plugin_no_resource(spec, resource):
    plugin = ResourcePlugin()

    result = plugin.path_helper('/resource')

    assert result is None
