from apispec import APISpec, BasePlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.yaml_utils import load_yaml_from_docstring
from .schemas import MediaSchema


class ResourcePlugin(BasePlugin):

    def init_spec(self, spec):
        super().init_spec(spec)
        self.spec = spec
        self.methods = [
            'get', 'post', 'put', 'patch',
            'delete', 'head', 'options', 'trace']

    def path_helper(self, path, operations=None, resource=None, **kwargs):
        if not resource:
            return

        for method in operations or self.methods:
            function = getattr(resource, method, None)
            if not function:
                continue
            operation = load_yaml_from_docstring(function.__doc__)
            if operation:
                operations[method] = operation


def create_spec() -> APISpec:
    spec = APISpec(
        title="Mediark",
        version="1.1.0",
        openapi_version="3.0.2",
        plugins=[MarshmallowPlugin(), ResourcePlugin()],
        info=dict(
            description="Media Management Server.",
            contact=dict(
                name="Knowark",
                url="https://www.knowark.com"
            )))

    _register_schemas(spec)

    return spec


def _register_schemas(spec):
    spec.components.schema("Media", schema=MediaSchema)
